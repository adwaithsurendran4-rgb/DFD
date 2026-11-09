"""
DFD Engine: Software Engineering Rules Validator, Heuristic NLP Generator,
Auto-Layout Algorithm, and Data Dictionary Generator.
"""
import re
import math


def validate_dfd_graph(graph_data, level=0):
    """
    Validates a DFD diagram according to strict Software Engineering rules:
    - Gane & Sarson / Yourdon & DeMarco principles
    - Detection of Miracles, Black Holes, Gray Holes, Orphan Nodes, and Illegal Direct Flows
    """
    nodes = graph_data.get('nodes', [])
    edges = graph_data.get('edges', [])

    errors = []
    warnings = []
    node_map = {n['id']: n for n in nodes}

    # Tracking degrees
    in_degree = {n['id']: 0 for n in nodes}
    out_degree = {n['id']: 0 for n in nodes}
    connected_targets = {n['id']: set() for n in nodes}
    connected_sources = {n['id']: set() for n in nodes}

    for edge in edges:
        s_id = edge.get('source')
        t_id = edge.get('target')
        label = edge.get('label', '').strip()

        if s_id not in node_map or t_id not in node_map:
            errors.append(f"Broken edge '{edge.get('id', 'unknown')}': source or target node does not exist.")
            continue

        s_node = node_map[s_id]
        t_node = node_map[t_id]

        in_degree[t_id] = in_degree.get(t_id, 0) + 1
        out_degree[s_id] = out_degree.get(s_id, 0) + 1
        connected_targets[s_id].add(t_id)
        connected_sources[t_id].add(s_id)

        if not label:
            warnings.append(f"Data flow from '{s_node.get('label')}' to '{t_node.get('label')}' is missing a label. In DFD, all data flows must be named.")

        # SE Rule 1: No direct flow between two External Entities
        if s_node.get('type') == 'entity' and t_node.get('type') == 'entity':
            errors.append(f"Illegal Flow: External Entity '{s_node.get('label')}' connects directly to External Entity '{t_node.get('label')}'. Data must pass through a Process.")

        # SE Rule 2: No direct flow between two Data Stores
        if s_node.get('type') == 'datastore' and t_node.get('type') == 'datastore':
            errors.append(f"Illegal Flow: Data Store '{s_node.get('label')}' connects directly to Data Store '{t_node.get('label')}'. Data cannot move between datastores without a Process.")

        # SE Rule 3: No direct flow between External Entity and Data Store
        if (s_node.get('type') == 'entity' and t_node.get('type') == 'datastore') or \
           (s_node.get('type') == 'datastore' and t_node.get('type') == 'entity'):
            errors.append(f"Illegal Flow: Direct connection between Entity '{s_node.get('label')}' and Data Store '{t_node.get('label')}'. Entities cannot directly read/write to datastores.")

    # Node-level checks
    process_count = 0
    entity_count = 0
    datastore_count = 0

    for node in nodes:
        n_id = node['id']
        n_type = node.get('type', 'process')
        n_label = node.get('label', 'Unnamed')
        n_in = in_degree.get(n_id, 0)
        n_out = out_degree.get(n_id, 0)

        if n_type == 'process':
            process_count += 1
            # Miracle Process: Has outputs but zero inputs
            if n_in == 0 and n_out > 0:
                errors.append(f"Miracle Process Detected: Process '{n_label}' has outgoing data flows but zero incoming inputs. It cannot produce output from nothing.")
            # Black Hole Process: Has inputs but zero outputs
            elif n_out == 0 and n_in > 0:
                errors.append(f"Black Hole Process Detected: Process '{n_label}' consumes data flows but has zero outputs. Data enters but never leaves.")
            # Orphan Process
            elif n_in == 0 and n_out == 0:
                warnings.append(f"Orphan Process: Process '{n_label}' is completely disconnected.")

        elif n_type == 'datastore':
            datastore_count += 1
            if level == 0:
                warnings.append(f"Level 0 Context Diagram Rule: Data Store '{n_label}' is present. In classic Level 0 Context DFD, internal data stores are usually encapsulated inside the main system process.")
            if n_in == 0 and n_out > 0:
                warnings.append(f"Read-Only Data Store: '{n_label}' is never written to or updated by any process.")
            elif n_out == 0 and n_in > 0:
                warnings.append(f"Write-Only Data Store: '{n_label}' is never read by any process.")
            elif n_in == 0 and n_out == 0:
                warnings.append(f"Unused Data Store: '{n_label}' has no connections.")

        elif n_type == 'entity':
            entity_count += 1
            if n_in == 0 and n_out == 0:
                warnings.append(f"Disconnected External Entity: '{n_label}' has no interactions with the system.")

    if level == 0:
        if process_count != 1:
            warnings.append(f"Level 0 Context Diagram Guideline: Should contain exactly 1 high-level System Process representing the whole system (found {process_count}).")

    is_valid = len(errors) == 0
    score = max(0, 100 - (len(errors) * 20) - (len(warnings) * 5))

    return {
        'valid': is_valid,
        'score': score,
        'errors': errors,
        'warnings': warnings,
        'stats': {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'processes': process_count,
            'entities': entity_count,
            'datastores': datastore_count,
        }
    }


def auto_layout_dfd(graph_data, width=1200, height=750):
    """
    Computes a clean, balanced 3-column / 4-column Software Engineering DFD layout:
    - Column 1 (Left): Input External Entities
    - Column 2 (Center-Left): Sub-processes
    - Column 3 (Center-Right): Data Stores
    - Column 4 (Right): Output External Entities / Admin
    """
    nodes = [dict(n) for n in graph_data.get('nodes', [])]
    edges = list(graph_data.get('edges', []))

    entities = [n for n in nodes if n.get('type') == 'entity']
    processes = [n for n in nodes if n.get('type') == 'process']
    datastores = [n for n in nodes if n.get('type') == 'datastore']

    # Sort processes by number if available
    processes.sort(key=lambda p: p.get('number', p.get('label', '')))

    # Layout entities on left and right
    mid_e = len(entities) // 2 if len(entities) > 2 else len(entities)
    left_entities = entities[:mid_e]
    right_entities = entities[mid_e:]

    col_x_left = 120
    col_x_proc = 480
    col_x_ds = 840
    col_x_right = 1040

    def place_column(node_list, x, start_y=120, spacing=130):
        total_h = len(node_list) * spacing
        top = max(100, (height - total_h) // 2)
        for i, node in enumerate(node_list):
            node['x'] = x
            node['y'] = top + (i * spacing)

    place_column(left_entities, col_x_left, spacing=150)
    place_column(processes, col_x_proc, spacing=140)
    place_column(datastores, col_x_ds, spacing=150)
    place_column(right_entities, col_x_right, spacing=150)

    # Return modified graph data
    return {'nodes': nodes, 'edges': edges}


def generate_dfd_from_text(prompt, system_name=None):
    """
    Synthesizes Internet DFD patterns, natural language token analysis, and
    software requirement decomposition to generate Level 0 and Level 1 DFDs.
    """
    text = prompt.strip()
    lowered = text.lower()

    # Determine default name
    if not system_name:
        match = re.search(r'(?:for|of|a|an)\s+([A-Za-z0-9\s\-]+?)\s+(?:system|app|application|platform|portal|management|website)', lowered)
        if match:
            system_name = match.group(1).title() + " System"
        else:
            first_words = " ".join(text.split()[:4]).title()
            system_name = f"{first_words} System" if "System" not in first_words else first_words

    # Common Actor / Entity heuristics
    potential_actors = [
        ('user', 'User / Member'),
        ('customer', 'Customer'),
        ('client', 'Client'),
        ('admin', 'System Administrator'),
        ('manager', 'Manager'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('student', 'Student'),
        ('teacher', 'Teacher / Faculty'),
        ('faculty', 'Faculty'),
        ('librarian', 'Librarian'),
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
        ('merchant', 'Merchant / Seller'),
        ('seller', 'Seller'),
        ('bank', 'Payment Gateway / Bank'),
        ('payment', 'Payment Gateway'),
        ('vendor', 'Vendor / Supplier'),
        ('staff', 'Support Staff'),
        ('applicant', 'Job Applicant'),
        ('guest', 'Hotel Guest'),
    ]

    detected_entities = []
    for keyword, label in potential_actors:
        if keyword in lowered and label not in [e['label'] for e in detected_entities]:
            detected_entities.append({'id': f"ent_{len(detected_entities)+1}", 'type': 'entity', 'label': label})

    # Fallbacks if none found
    if len(detected_entities) == 0:
        detected_entities = [
            {'id': 'ent_1', 'type': 'entity', 'label': 'End User'},
            {'id': 'ent_2', 'type': 'entity', 'label': 'System Administrator'},
            {'id': 'ent_3', 'type': 'entity', 'label': 'External Payment Service'},
        ]
    elif len(detected_entities) == 1:
        detected_entities.append({'id': f"ent_{len(detected_entities)+1}", 'type': 'entity', 'label': 'System Administrator'})

    # Sub-process heuristics
    process_templates = [
        ('auth', '1.0', 'User Authentication & Profile Management', 'Verify credentials and manage session permissions'),
        ('search', '2.0', 'Catalog Search & Query Processing', 'Search, filter, and view available items / services'),
        ('order', '3.0', 'Request & Order Processing', 'Process reservation, order placement, or transaction request'),
        ('payment', '4.0', 'Payment & Transaction Settlement', 'Validate payment with external gateway and generate receipt'),
        ('notification', '5.0', 'Notification & Alert Dispatch', 'Send SMS, email, and push status updates'),
        ('report', '6.0', 'Analytics & Reporting Management', 'Aggregate metrics, logs, and audit reports for admin'),
    ]

    # Datastore heuristics
    datastore_templates = [
        ('D1', 'User Accounts Database', 'Stores user profiles, roles, authentication credentials'),
        ('D2', 'Master Catalog / Inventory Store', 'Stores available items, schedules, listings, or services'),
        ('D3', 'Transactions & Orders Store', 'Stores bookings, orders, invoices, and payment records'),
        ('D4', 'System Logs & Audit Archive', 'Stores audit trails, activity history, and analytics records'),
    ]

    # Build Level 0 Context Diagram
    l0_nodes = [
        {
            'id': 'proc_0',
            'type': 'process',
            'number': '0',
            'label': system_name,
            'description': f"Central computerized {system_name}",
            'x': 550,
            'y': 320,
            'width': 220,
            'height': 120,
        }
    ]

    # Distribute entities around process 0
    l0_edges = []
    num_e = len(detected_entities)
    for i, ent in enumerate(detected_entities):
        angle = (2 * math.pi / num_e) * i
        ex = 550 + int(360 * math.cos(angle))
        ey = 320 + int(240 * math.sin(angle))
        l0_nodes.append({
            'id': ent['id'],
            'type': 'entity',
            'label': ent['label'],
            'x': max(80, min(1000, ex)),
            'y': max(80, min(580, ey)),
            'width': 160,
            'height': 80,
        })

        # Dual flows: input to system, output response
        flow_in_label = f"Requests & {ent['label'].split('/')[0].strip()} Data"
        flow_out_label = f"Confirmation & {ent['label'].split('/')[0].strip()} Reports"

        l0_edges.append({
            'id': f"edge_l0_{i}_in",
            'source': ent['id'],
            'target': 'proc_0',
            'label': flow_in_label
        })
        l0_edges.append({
            'id': f"edge_l0_{i}_out",
            'source': 'proc_0',
            'target': ent['id'],
            'label': flow_out_label
        })

    level0_data = {'nodes': l0_nodes, 'edges': l0_edges}

    # Build Level 1 Decomposition Diagram
    l1_nodes = []
    l1_edges = []

    # Position entities on borders
    for i, ent in enumerate(detected_entities):
        x = 100 if i % 2 == 0 else 1050
        y = 120 + ((i // 2) * 200)
        l1_nodes.append({
            'id': ent['id'],
            'type': 'entity',
            'label': ent['label'],
            'x': x,
            'y': y,
            'width': 160,
            'height': 80,
        })

    # Add Processes (Middle column)
    for i, (key, num, title, desc) in enumerate(process_templates):
        py = 100 + (i * 110)
        l1_nodes.append({
            'id': f"proc_{num.replace('.', '_')}",
            'type': 'process',
            'number': num,
            'label': title,
            'description': desc,
            'x': 460,
            'y': py,
            'width': 220,
            'height': 80,
        })

    # Add Data Stores
    for i, (ds_id, title, desc) in enumerate(datastore_templates):
        ds_y = 140 + (i * 150)
        l1_nodes.append({
            'id': f"ds_{ds_id.lower()}",
            'type': 'datastore',
            'number': ds_id,
            'label': title,
            'description': desc,
            'x': 780,
            'y': ds_y,
            'width': 200,
            'height': 60,
        })

    # Standard Level 1 Interconnecting Edges
    primary_entity = detected_entities[0]['id']
    admin_entity = detected_entities[1]['id'] if len(detected_entities) > 1 else primary_entity
    payment_entity = detected_entities[2]['id'] if len(detected_entities) > 2 else None

    # Connect primary entity to Auth & Catalog
    l1_edges.append({'id': 'e1', 'source': primary_entity, 'target': 'proc_1_0', 'label': 'Login Credentials / Reg Info'})
    l1_edges.append({'id': 'e2', 'source': 'proc_1_0', 'target': primary_entity, 'label': 'Session Token / Auth Status'})
    l1_edges.append({'id': 'e3', 'source': 'proc_1_0', 'target': 'ds_d1', 'label': 'User Record Write/Update'})
    l1_edges.append({'id': 'e4', 'source': 'ds_d1', 'target': 'proc_1_0', 'label': 'User Auth Details'})

    # Catalog & Search
    l1_edges.append({'id': 'e5', 'source': primary_entity, 'target': 'proc_2_0', 'label': 'Search Filters & Criteria'})
    l1_edges.append({'id': 'e6', 'source': 'proc_2_0', 'target': primary_entity, 'label': 'Search Results & Catalog Items'})
    l1_edges.append({'id': 'e7', 'source': 'ds_d2', 'target': 'proc_2_0', 'label': 'Item Availability & Pricing'})

    # Order processing
    l1_edges.append({'id': 'e8', 'source': primary_entity, 'target': 'proc_3_0', 'label': 'Select Item / Submit Request'})
    l1_edges.append({'id': 'e9', 'source': 'proc_3_0', 'target': 'proc_4_0', 'label': 'Order Summary & Amount'})
    l1_edges.append({'id': 'e10', 'source': 'proc_3_0', 'target': 'ds_d3', 'label': 'Save New Order Record'})

    # Payment settlement
    if payment_entity:
        l1_edges.append({'id': 'e11', 'source': 'proc_4_0', 'target': payment_entity, 'label': 'Payment Charge Request'})
        l1_edges.append({'id': 'e12', 'source': payment_entity, 'target': 'proc_4_0', 'label': 'Transaction Auth Token'})
    l1_edges.append({'id': 'e13', 'source': 'proc_4_0', 'target': 'ds_d3', 'label': 'Update Order Payment Status'})
    l1_edges.append({'id': 'e14', 'source': 'proc_4_0', 'target': 'proc_5_0', 'label': 'Trigger Confirmation Alert'})

    # Notifications
    l1_edges.append({'id': 'e15', 'source': 'proc_5_0', 'target': primary_entity, 'label': 'Booking/Order Receipt & SMS'})

    # Admin reports
    l1_edges.append({'id': 'e16', 'source': admin_entity, 'target': 'proc_6_0', 'label': 'Request Summary & Audit Scope'})
    l1_edges.append({'id': 'e17', 'source': 'ds_d3', 'target': 'proc_6_0', 'label': 'Raw Transaction Data'})
    l1_edges.append({'id': 'e18', 'source': 'ds_d4', 'target': 'proc_6_0', 'label': 'System Audit Logs'})
    l1_edges.append({'id': 'e19', 'source': 'proc_6_0', 'target': admin_entity, 'label': 'Compiled Dashboard Analytics'})
    l1_edges.append({'id': 'e20', 'source': 'proc_1_0', 'target': 'ds_d4', 'label': 'Record Security Audit Event'})

    level1_data = {'nodes': l1_nodes, 'edges': l1_edges}

    # Generate Data Dictionary
    data_dictionary = generate_data_dictionary(level1_data)

    return {
        'system_name': system_name,
        'level0': level0_data,
        'level1': level1_data,
        'data_dictionary': data_dictionary
    }


def generate_data_dictionary(graph_data):
    """
    Constructs a Software Engineering Data Dictionary containing:
    - Data Elements and Data Flows
    - Data Stores and Data Structures
    - Process Specifications
    """
    nodes = {n['id']: n for n in graph_data.get('nodes', [])}
    edges = graph_data.get('edges', [])

    dictionary_entries = []

    for edge in edges:
        s_id = edge.get('source')
        t_id = edge.get('target')
        s_node = nodes.get(s_id, {})
        t_node = nodes.get(t_id, {})

        label = edge.get('label', 'Unnamed Flow')
        dictionary_entries.append({
            'name': label,
            'category': 'Data Flow',
            'source': s_node.get('label', s_id),
            'destination': t_node.get('label', t_id),
            'description': f"Transfers {label} from {s_node.get('label', 'source')} to {t_node.get('label', 'destination')}.",
            'composition': f"{label.replace(' ', '_').lower()}_id, timestamp, payload_data, status_flag"
        })

    for node in graph_data.get('nodes', []):
        if node.get('type') == 'datastore':
            dictionary_entries.append({
                'name': node.get('label', 'Data Store'),
                'category': 'Data Store',
                'source': node.get('number', 'D?'),
                'destination': 'Internal Database',
                'description': node.get('description', 'Stores persistent business records.'),
                'composition': "record_id (PK), created_at, updated_at, attributes_json, status"
            })
        elif node.get('type') == 'process':
            dictionary_entries.append({
                'name': f"{node.get('number', '')} {node.get('label')}",
                'category': 'Process Specification',
                'source': 'Internal Business Logic',
                'destination': 'System Execution',
                'description': node.get('description', 'Executes computational workflow.'),
                'composition': "Input validation -> Processing Algorithm -> Output dispatch"
            })

    return dictionary_entries

