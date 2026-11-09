import json
import io
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse

from .models import Project, Diagram, DFDTemplate, ForensicScan
from .dfd_engine import validate_dfd_graph, generate_dfd_from_text, auto_layout_dfd, generate_data_dictionary
from .forensics import run_error_level_analysis, run_noise_and_edge_analysis, analyze_media_forensics


class DFDEngineTests(TestCase):
    def test_valid_dfd_validation(self):
        graph = {
            'nodes': [
                {'id': 'e1', 'type': 'entity', 'label': 'Customer'},
                {'id': 'p1', 'type': 'process', 'number': '1.0', 'label': 'Process Order'},
                {'id': 'd1', 'type': 'datastore', 'number': 'D1', 'label': 'Orders Store'}
            ],
            'edges': [
                {'id': 'f1', 'source': 'e1', 'target': 'p1', 'label': 'Order Form'},
                {'id': 'f2', 'source': 'p1', 'target': 'd1', 'label': 'Save Order'},
                {'id': 'f3', 'source': 'p1', 'target': 'e1', 'label': 'Receipt'},
                {'id': 'f4', 'source': 'd1', 'target': 'p1', 'label': 'Query Order'}
            ]
        }
        res = validate_dfd_graph(graph, level=1)
        self.assertTrue(res['valid'])
        self.assertEqual(len(res['errors']), 0)
        self.assertEqual(res['score'], 100)

    def test_miracle_and_blackhole_detection(self):
        graph = {
            'nodes': [
                {'id': 'p_miracle', 'type': 'process', 'number': '1.0', 'label': 'Miracle Proc'},
                {'id': 'p_blackhole', 'type': 'process', 'number': '2.0', 'label': 'Blackhole Proc'}
            ],
            'edges': [
                {'id': 'f1', 'source': 'p_miracle', 'target': 'p_blackhole', 'label': 'Data Stream'}
            ]
        }
        res = validate_dfd_graph(graph, level=1)
        self.assertFalse(res['valid'])
        # Miracle Proc has output but no input
        # Blackhole Proc has input but no output
        self.assertTrue(any('Miracle' in e for e in res['errors']))
        self.assertTrue(any('Black Hole' in e for e in res['errors']))

    def test_illegal_entity_to_entity_flow(self):
        graph = {
            'nodes': [
                {'id': 'e1', 'type': 'entity', 'label': 'Entity A'},
                {'id': 'e2', 'type': 'entity', 'label': 'Entity B'}
            ],
            'edges': [
                {'id': 'f1', 'source': 'e1', 'target': 'e2', 'label': 'Direct Illegal Flow'}
            ]
        }
        res = validate_dfd_graph(graph, level=1)
        self.assertFalse(res['valid'])
        self.assertTrue(any('Illegal Flow' in e for e in res['errors']))

    def test_nlp_dfd_generation(self):
        prompt = "A hospital appointment management system where patients book appointments, doctors view schedule, and reception manages billing."
        generated = generate_dfd_from_text(prompt)
        self.assertIn('level0', generated)
        self.assertIn('level1', generated)
        self.assertIn('data_dictionary', generated)
        self.assertGreater(len(generated['level0']['nodes']), 1)
        self.assertGreater(len(generated['level1']['nodes']), 3)

    def test_data_dictionary_generation(self):
        graph = {
            'nodes': [
                {'id': 'p1', 'type': 'process', 'number': '1.0', 'label': 'Validate Card'},
                {'id': 'd1', 'type': 'datastore', 'number': 'D1', 'label': 'Card Accounts'}
            ],
            'edges': [
                {'id': 'f1', 'source': 'p1', 'target': 'd1', 'label': 'Account Query'}
            ]
        }
        dict_entries = generate_data_dictionary(graph)
        self.assertGreaterEqual(len(dict_entries), 3)


class ForensicsEngineTests(TestCase):
    def setUp(self):
        # Create a test synthetic image in memory
        self.img = Image.new('RGB', (200, 200), color=(73, 109, 137))

    def test_ela_computation(self):
        ela_img, mean_ela = run_error_level_analysis(self.img)
        self.assertIsNotNone(ela_img)
        self.assertIsInstance(mean_ela, float)

    def test_noise_analysis(self):
        noise_img, mean_edge, var_edge = run_noise_and_edge_analysis(self.img)
        self.assertIsNotNone(noise_img)
        self.assertGreaterEqual(var_edge, 0.0)

    def test_full_forensics_pipeline(self):
        buffer = io.BytesIO()
        self.img.save(buffer, 'JPEG')
        buffer.seek(0)
        buffer.name = 'test_sample.jpg'

        result = analyze_media_forensics(buffer, is_url=False)
        self.assertIn('deepfake_score', result)
        self.assertIn('verdict', result)
        self.assertIn('orig_url', result)
        self.assertIn('ela_url', result)


class ViewAndAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pages_render(self):
        # Canvas Studio
        r1 = self.client.get(reverse('dfd_app:studio'))
        self.assertEqual(r1.status_code, 200)

        # Internet Templates
        r2 = self.client.get(reverse('dfd_app:templates'))
        self.assertEqual(r2.status_code, 200)

        # Forensics Lab
        r3 = self.client.get(reverse('dfd_app:forensics'))
        self.assertEqual(r3.status_code, 200)

        # Documentation Guide
        r4 = self.client.get(reverse('dfd_app:docs'))
        self.assertEqual(r4.status_code, 200)

    def test_api_validate(self):
        payload = {
            'graph_data': {
                'nodes': [{'id': 'p1', 'type': 'process', 'label': 'Auth'}],
                'edges': []
            },
            'level': 0
        }
        resp = self.client.post(
            reverse('dfd_app:api_validate'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('score', data)

    def test_api_generate(self):
        payload = {'prompt': 'Library system where students borrow books'}
        resp = self.client.post(
            reverse('dfd_app:api_generate'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('level0', data)

    def test_api_save_project(self):
        payload = {
            'name': 'Unit Test Project',
            'description': 'Testing DB persistence',
            'notation_style': 'gane_sarson',
            'diagrams': [
                {'level': 0, 'name': 'Context', 'graph_data': {'nodes': [], 'edges': []}}
            ]
        }
        resp = self.client.post(
            reverse('dfd_app:api_save_project'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(Project.objects.filter(name='Unit Test Project').exists())

    def test_api_forensic_scan_sample(self):
        resp = self.client.post(
            reverse('dfd_app:api_forensic_scan'),
            data={'source_type': 'sample', 'sample_type': 'authentic'}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('deepfake_score', data)
        self.assertIn('verdict', data)
