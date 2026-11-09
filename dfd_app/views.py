import os
import io
import json
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Project, Diagram, DFDTemplate, ForensicScan
from .dfd_engine import validate_dfd_graph, generate_dfd_from_text, auto_layout_dfd, generate_data_dictionary
from .templates_data import INTERNET_TEMPLATES
from .forensics import analyze_media_forensics


def studio_view(request):
    """Main interactive DFD canvas and modeling workspace."""
    # Seed templates if not yet in database
    if DFDTemplate.objects.count() == 0:
        for t_data in INTERNET_TEMPLATES:
            DFDTemplate.objects.create(
                slug=t_data['slug'],
                title=t_data['title'],
                category=t_data['category'],
                summary=t_data['summary'],
                description=t_data.get('description', ''),
                level0_data=t_data['level0'],
                level1_data=t_data['level1'],
                data_dictionary=generate_data_dictionary(t_data['level1'])
            )

    templates = DFDTemplate.objects.all()
    projects = Project.objects.order_by('-updated_at')[:10]

    # Default initial diagram to load: Online Banking or first template
    initial_template = templates.filter(slug='online-banking-atm').first() or templates.first()

    context = {
        'page_title': 'DFD Studio — Interactive Data Flow Diagram Canvas',
        'templates': templates,
        'projects': projects,
        'initial_template': initial_template,
        'templates_json': json.dumps([{
            'slug': t.slug,
            'title': t.title,
            'category': t.category,
            'summary': t.summary,
            'level0': t.level0_data,
            'level1': t.level1_data,
            'data_dictionary': t.data_dictionary
        } for t in templates])
    }
    return render(request, 'dfd/studio.html', context)


def templates_view(request):
    """Curated internet templates gallery with filtering and previews."""
    category = request.GET.get('category', 'all')
    templates = DFDTemplate.objects.all()
    if category != 'all':
        templates = templates.filter(category__iexact=category)

    categories = list(DFDTemplate.objects.values_list('category', flat=True).distinct())

    context = {
        'page_title': 'DFD Internet Templates Repository',
        'templates': templates,
        'categories': categories,
        'selected_category': category,
        'templates_json': json.dumps([{
            'slug': t.slug,
            'title': t.title,
            'category': t.category,
            'summary': t.summary,
            'description': t.description,
            'level0': t.level0_data,
            'level1': t.level1_data,
            'data_dictionary': t.data_dictionary
        } for t in templates])
    }
    return render(request, 'dfd/templates.html', context)


def forensics_view(request):
    """DeepFake Detection Forensics Lab."""
    recent_scans = ForensicScan.objects.all()[:8]
    context = {
        'page_title': 'DFD Lab — DeepFake Detection & Media Forensics',
        'recent_scans': recent_scans
    }
    return render(request, 'dfd/forensics.html', context)


def docs_view(request):
    """Software Engineering DFD Guide & Axioms Reference."""
    context = {
        'page_title': 'Software Engineering DFD Architecture & Notation Guide'
    }
    return render(request, 'dfd/docs.html', context)


# ==========================================
# REST API ENDPOINTS
# ==========================================

@api_view(['POST'])
def api_validate(request):
    """Validates diagram data against DFD software engineering rules."""
    graph_data = request.data.get('graph_data', {})
    level = int(request.data.get('level', 0))
    result = validate_dfd_graph(graph_data, level=level)
    return Response(result)


@api_view(['POST'])
def api_generate(request):
    """Generates Level 0 and Level 1 DFDs from natural language requirements."""
    prompt = request.data.get('prompt', '').strip()
    system_name = request.data.get('system_name', None)

    if not prompt:
        return Response({'error': 'Please provide a system description or requirement prompt.'}, status=400)

    generated = generate_dfd_from_text(prompt, system_name=system_name)
    return Response(generated)


@api_view(['POST'])
def api_autolayout(request):
    """Applies clean layered auto-layout to given graph data."""
    graph_data = request.data.get('graph_data', {})
    width = int(request.data.get('width', 1200))
    height = int(request.data.get('height', 750))
    arranged = auto_layout_dfd(graph_data, width=width, height=height)
    return Response(arranged)


@api_view(['POST'])
def api_data_dictionary(request):
    """Generates a structured Software Engineering Data Dictionary."""
    graph_data = request.data.get('graph_data', {})
    dictionary = generate_data_dictionary(graph_data)
    return Response({'entries': dictionary})


@api_view(['POST'])
def api_save_project(request):
    """Persists a DFD project and diagrams to the database."""
    name = request.data.get('name', 'Untitled DFD Project')
    description = request.data.get('description', '')
    notation_style = request.data.get('notation_style', 'gane_sarson')
    project_id = request.data.get('project_id')
    diagrams_data = request.data.get('diagrams', [])

    if project_id:
        project = Project.objects.filter(id=project_id).first()
        if project:
            project.name = name
            project.description = description
            project.notation_style = notation_style
            project.save()
        else:
            project = Project.objects.create(name=name, description=description, notation_style=notation_style)
    else:
        project = Project.objects.create(name=name, description=description, notation_style=notation_style)

    # Save diagrams
    for d in diagrams_data:
        level = int(d.get('level', 0))
        d_name = d.get('name', f"Level {level} Diagram")
        graph = d.get('graph_data', {})
        diag, _ = Diagram.objects.update_or_create(
            project=project,
            level=level,
            defaults={'name': d_name, 'graph_data': graph}
        )

    return Response({
        'status': 'success',
        'project_id': str(project.id),
        'name': project.name,
        'message': f"Project '{project.name}' successfully saved!"
    })


@api_view(['GET'])
def api_load_project(request, project_id):
    """Loads a saved project by ID."""
    project = get_object_or_404(Project, id=project_id)
    diagrams = project.diagrams.all()
    diagram_list = [{
        'id': str(d.id),
        'level': d.level,
        'name': d.name,
        'graph_data': d.graph_data
    } for d in diagrams]

    return Response({
        'id': str(project.id),
        'name': project.name,
        'description': project.description,
        'notation_style': project.notation_style,
        'diagrams': diagram_list
    })


@api_view(['POST'])
def api_forensic_scan(request):
    """DeepFake detection analysis on uploaded image, URL, or demo sample."""
    try:
        source_type = request.data.get('source_type', 'upload')

        if source_type == 'sample':
            sample_type = request.data.get('sample_type', 'authentic')
            sample_filename = 'sample_authentic.jpg' if sample_type == 'authentic' else 'sample_manipulated.jpg'
            sample_path = os.path.join(settings.BASE_DIR, 'static', 'samples', sample_filename)
            with open(sample_path, 'rb') as f:
                file_content = io.BytesIO(f.read())
                file_content.name = sample_filename
                result = analyze_media_forensics(file_content, is_url=False)
            scan = ForensicScan.objects.create(
                title=f"Demo Sample: {sample_filename}",
                source_type='sample',
                deepfake_score=result['deepfake_score'],
                verdict=result['verdict'],
                analysis_details=result
            )
        elif source_type == 'url':
            image_url = request.data.get('url', '').strip()
            if not image_url:
                return Response({'error': 'Please provide a valid image URL.'}, status=400)
            result = analyze_media_forensics(image_url, is_url=True)
            scan = ForensicScan.objects.create(
                title=f"URL Scan: {image_url.split('/')[-1][:30] or 'Web Image'}",
                source_type='url',
                source_url=image_url,
                deepfake_score=result['deepfake_score'],
                verdict=result['verdict'],
                analysis_details=result
            )
        else:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({'error': 'No image file uploaded.'}, status=400)
            result = analyze_media_forensics(uploaded_file, is_url=False)
            scan = ForensicScan.objects.create(
                title=f"File Scan: {uploaded_file.name}",
                source_type='upload',
                deepfake_score=result['deepfake_score'],
                verdict=result['verdict'],
                analysis_details=result
            )

        result['scan_id'] = str(scan.id)
        return Response(result)
    except Exception as e:
        return Response({'error': f"Forensic analysis failed: {str(e)}"}, status=500)
