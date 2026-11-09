/**
 * DFD Studio Core Engine
 * Interactive multi-level canvas, Gane-Sarson & Yourdon-DeMarco notation,
 * real-time Software Engineering rule validation, auto-layout, and exporters.
 */

// Global Studio State
const StudioState = {
    projectId: null,
    projectName: "Online Banking & ATM System",
    notationStyle: "gane_sarson",
    currentLevel: 0,
    levels: {
        0: { nodes: [], edges: [] },
        1: { nodes: [], edges: [] },
        2: { nodes: [], edges: [] }
    },
    selected: null, // { type: 'node'|'edge', id: string }
    isConnecting: false,
    connectSource: null,
    zoom: 1.0,
    pan: { x: 0, y: 0 },
    isPanning: false,
    panStart: { x: 0, y: 0 },
    draggingNode: null,
    dragOffset: { x: 0, y: 0 },
    history: []
};

// Initialize Studio on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initDefaultTemplate();
    setupCanvasEvents();
    setupTemplateSelector();
    renderCanvas();
});

function initDefaultTemplate() {
    if (typeof INITIAL_TEMPLATES_DATA !== 'undefined' && INITIAL_TEMPLATES_DATA.length > 0) {
        const urlParams = new URLSearchParams(window.location.search);
        const loadSlug = urlParams.get('load');
        let selectedT = null;
        if (loadSlug) {
            selectedT = INITIAL_TEMPLATES_DATA.find(t => t.slug === loadSlug);
            const sel = document.getElementById('templateSelector');
            if (sel) sel.value = loadSlug;
        }
        if (!selectedT) {
            selectedT = INITIAL_TEMPLATES_DATA[0];
        }
        loadTemplateData(selectedT);
    } else {
        // Fallback minimal Context diagram
        StudioState.levels[0] = {
            nodes: [
                { id: "proc_0", type: "process", number: "0", label: "Core Information System", x: 450, y: 250, width: 220, height: 100 },
                { id: "ent_1", type: "entity", label: "User Client", x: 120, y: 250, width: 150, height: 80 }
            ],
            edges: [
                { id: "e1", source: "ent_1", target: "proc_0", label: "User Requests & Inputs" },
                { id: "e2", source: "proc_0", target: "ent_1", label: "System Response & Confirmation" }
            ]
        };
    }
}

function loadTemplateData(tpl) {
    StudioState.projectName = tpl.title;
    document.getElementById('projectTitleInput').value = tpl.title;
    StudioState.levels[0] = JSON.parse(JSON.stringify(tpl.level0 || { nodes: [], edges: [] }));
    StudioState.levels[1] = JSON.parse(JSON.stringify(tpl.level1 || { nodes: [], edges: [] }));
    StudioState.levels[2] = JSON.parse(JSON.stringify(tpl.level2 || { nodes: [], edges: [] }));
    StudioState.currentLevel = 0;
    StudioState.selected = null;
    StudioState.zoom = 1.0;
    StudioState.pan = { x: 0, y: 0 };
    updateLevelButtons();
    renderCanvas();
    if (window.showToast) window.showToast(`Loaded "${tpl.title}" template!`, 'info');
}

function setupTemplateSelector() {
    const sel = document.getElementById('templateSelector');
    if (!sel) return;
    sel.addEventListener('change', (e) => {
        const slug = e.target.value;
        if (!slug) return;
        const found = INITIAL_TEMPLATES_DATA.find(t => t.slug === slug);
        if (found) {
            loadTemplateData(found);
        }
    });
}

// Level Switching
function switchLevel(lvl) {
    StudioState.currentLevel = lvl;
    StudioState.selected = null;
    updateLevelButtons();
    renderCanvas();
}

function updateLevelButtons() {
    const badge = document.getElementById('activeLevelBadge');
    ['btnLevel0', 'btnLevel1', 'btnLevel2'].forEach((btnId, idx) => {
        const btn = document.getElementById(btnId);
        if (btn) {
            if (idx === StudioState.currentLevel) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        }
    });

    if (badge) {
        if (StudioState.currentLevel === 0) badge.textContent = "Level 0: Context";
        else if (StudioState.currentLevel === 1) badge.textContent = "Level 1: Decomposition";
        else badge.textContent = "Level 2: Sub-process Detail";
    }
}

// SE Notation Switching
function changeNotation(style) {
    StudioState.notationStyle = style;
    renderCanvas();
    if (window.showToast) {
        const name = style === 'gane_sarson' ? 'Gane & Sarson' : 'Yourdon & DeMarco';
        window.showToast(`Switched notation standard to ${name}`, 'secondary');
    }
}

// Current Diagram Getter
function getCurrentGraph() {
    return StudioState.levels[StudioState.currentLevel];
}

// Main Render Loop
function renderCanvas() {
    const graph = getCurrentGraph();
    const container = document.getElementById('nodesContainer');
    const edgesGroup = document.getElementById('edgesGroup');
    const viewport = document.getElementById('canvasViewport');

    if (!container || !edgesGroup) return;

    // Clear existing
    container.innerHTML = '';
    edgesGroup.innerHTML = '';

    // Transform style for pan & zoom
    container.style.transform = `translate(${StudioState.pan.x}px, ${StudioState.pan.y}px) scale(${StudioState.zoom})`;
    container.style.transformOrigin = '0 0';
    edgesGroup.style.transform = `translate(${StudioState.pan.x}px, ${StudioState.pan.y}px) scale(${StudioState.zoom})`;
    edgesGroup.style.transformOrigin = '0 0';
    edgesGroup.setAttribute('transform', `translate(${StudioState.pan.x}, ${StudioState.pan.y}) scale(${StudioState.zoom})`);

    // 1. Render Edges (SVG Bezier curves)
    const nodeMap = {};
    graph.nodes.forEach(n => nodeMap[n.id] = n);

    graph.edges.forEach(edge => {
        const sNode = nodeMap[edge.source];
        const tNode = nodeMap[edge.target];
        if (!sNode || !tNode) return;

        const isSelected = StudioState.selected && StudioState.selected.type === 'edge' && StudioState.selected.id === edge.id;
        renderEdge(edge, sNode, tNode, edgesGroup, isSelected);
    });

    // 2. Render Nodes (DOM elements for crisp text & controls)
    graph.nodes.forEach(node => {
        const isSelected = StudioState.selected && StudioState.selected.type === 'node' && StudioState.selected.id === node.id;
        renderNode(node, container, isSelected);
    });

    // 3. Update Inspector & Validation Stats
    updateInspector();
    updateComponentStats();
    validateActiveDiagram();
}

// Render individual edge
function renderEdge(edge, s, t, svgGroup, isSelected) {
    const sWidth = s.width || 180;
    const sHeight = s.height || 80;
    const tWidth = t.width || 180;
    const tHeight = t.height || 80;

    const sCenterX = s.x + (sWidth / 2);
    const sCenterY = s.y + (sHeight / 2);
    const tCenterX = t.x + (tWidth / 2);
    const tCenterY = t.y + (tHeight / 2);

    // Compute border intersection points
    const p1 = getIntersectionPoint(sCenterX, sCenterY, tCenterX, tCenterY, sWidth, sHeight);
    const p2 = getIntersectionPoint(tCenterX, tCenterY, sCenterX, sCenterY, tWidth, tHeight);

    // Control point for smooth curved Bezier
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const dist = Math.hypot(dx, dy);
    const curvature = Math.min(40, dist * 0.15);
    // Perpendicular offset
    const normX = -dy / (dist || 1);
    const normY = dx / (dist || 1);
    const cx = ((p1.x + p2.x) / 2) + (normX * curvature);
    const cy = ((p1.y + p2.y) / 2) + (normY * curvature);

    const pathD = `M ${p1.x} ${p1.y} Q ${cx} ${cy} ${p2.x} ${p2.y}`;

    // SVG Path
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathD);
    path.setAttribute("class", `flow-path ${isSelected ? 'selected' : ''}`);
    path.setAttribute("marker-end", isSelected ? "url(#arrowhead-selected)" : "url(#arrowhead)");
    path.addEventListener('click', (e) => {
        e.stopPropagation();
        selectElement('edge', edge.id);
    });
    path.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        openEditModal('edge', edge.id);
    });
    svgGroup.appendChild(path);

    // Flow Label centered along the curve
    const labelText = edge.label || "Data Flow";
    const labelX = cx;
    const labelY = cy;

    const textEl = document.createElementNS("http://www.w3.org/2000/svg", "text");
    textEl.setAttribute("x", labelX);
    textEl.setAttribute("y", labelY + 3);
    textEl.setAttribute("text-anchor", "middle");
    textEl.setAttribute("class", "flow-label");
    textEl.textContent = labelText;

    // Background pill
    const estWidth = Math.max(50, labelText.length * 6.8 + 14);
    const estHeight = 20;
    const rectEl = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rectEl.setAttribute("x", labelX - (estWidth / 2));
    rectEl.setAttribute("y", labelY - 11);
    rectEl.setAttribute("width", estWidth);
    rectEl.setAttribute("height", estHeight);
    rectEl.setAttribute("class", "flow-label-bg");

    [rectEl, textEl].forEach(el => {
        el.addEventListener('click', (e) => {
            e.stopPropagation();
            selectElement('edge', edge.id);
        });
        el.addEventListener('dblclick', (e) => {
            e.stopPropagation();
            openEditModal('edge', edge.id);
        });
    });

    svgGroup.appendChild(rectEl);
    svgGroup.appendChild(textEl);
}

function getIntersectionPoint(x1, y1, x2, y2, w, h) {
    const hw = w / 2;
    const hh = h / 2;
    const dx = x2 - x1;
    const dy = y2 - y1;
    if (dx === 0 && dy === 0) return { x: x1, y: y1 };

    const slope = dy / (dx || 0.0001);
    let ix, iy;

    // Check intersection with vertical edges
    if (Math.abs(slope) <= hh / hw) {
        ix = dx > 0 ? x1 + hw : x1 - hw;
        iy = y1 + slope * (ix - x1);
    } else {
        // Horizontal edges
        iy = dy > 0 ? y1 + hh : y1 - hh;
        ix = x1 + (iy - y1) / slope;
    }
    return { x: ix, y: iy };
}

// Render individual node
function renderNode(node, container, isSelected) {
    const el = document.createElement('div');
    el.id = `node_${node.id}`;
    el.style.left = `${node.x}px`;
    el.style.top = `${node.y}px`;
    el.style.width = `${node.width || 180}px`;
    el.style.height = `${node.height || 80}px`;
    el.style.pointerEvents = 'auto';

    let nodeClass = `dfd-node ${isSelected ? 'selected' : ''} `;

    if (node.type === 'entity') {
        nodeClass += 'node-entity';
        el.className = nodeClass;
        el.innerHTML = `<div><i class="bi bi-person me-1"></i> ${escapeHtml(node.label || 'Entity')}</div>`;
    } else if (node.type === 'process') {
        const num = node.number || (StudioState.currentLevel === 0 ? '0' : '1.0');
        if (StudioState.notationStyle === 'gane_sarson') {
            nodeClass += 'node-process-gane';
            el.className = nodeClass;
            el.innerHTML = `
                <div class="proc-header font-mono">${escapeHtml(num)}</div>
                <div class="proc-body">${escapeHtml(node.label || 'Process')}</div>
            `;
        } else {
            // Yourdon circle
            nodeClass += 'node-process-yourdon';
            el.className = nodeClass;
            el.style.borderRadius = '50%';
            el.innerHTML = `
                <div class="proc-num font-mono">${escapeHtml(num)}</div>
                <div class="proc-text small">${escapeHtml(node.label || 'Process')}</div>
            `;
        }
    } else if (node.type === 'datastore') {
        const dsNum = node.number || 'D1';
        if (StudioState.notationStyle === 'gane_sarson') {
            nodeClass += 'node-datastore-gane';
            el.className = nodeClass;
            el.innerHTML = `
                <div class="ds-id font-mono">${escapeHtml(dsNum)}</div>
                <div class="ds-name">${escapeHtml(node.label || 'Data Store')}</div>
            `;
        } else {
            // Yourdon parallel lines
            nodeClass += 'node-datastore-yourdon';
            el.className = nodeClass;
            el.innerHTML = `<span class="font-mono text-warning me-2">${escapeHtml(dsNum)}</span> ${escapeHtml(node.label || 'Data Store')}`;
        }
    }

    // Node Event Listeners
    el.addEventListener('mousedown', (e) => {
        if (StudioState.isConnecting) {
            handleConnectClick(node.id);
            e.stopPropagation();
            return;
        }
        e.stopPropagation();
        selectElement('node', node.id);
        startDraggingNode(node, e);
    });

    el.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        openEditModal('node', node.id);
    });

    container.appendChild(el);
}

// Drag & Drop Node Movement
function startDraggingNode(node, e) {
    StudioState.draggingNode = node;
    const mouseCanvasX = (e.clientX - StudioState.pan.x) / StudioState.zoom;
    const mouseCanvasY = (e.clientY - StudioState.pan.y) / StudioState.zoom;
    StudioState.dragOffset = {
        x: mouseCanvasX - node.x,
        y: mouseCanvasY - node.y
    };

    function onMouseMove(moveEvent) {
        if (!StudioState.draggingNode) return;
        const currentCanvasX = (moveEvent.clientX - StudioState.pan.x) / StudioState.zoom;
        const currentCanvasY = (moveEvent.clientY - StudioState.pan.y) / StudioState.zoom;
        const newX = Math.round(currentCanvasX - StudioState.dragOffset.x);
        const newY = Math.round(currentCanvasY - StudioState.dragOffset.y);
        StudioState.draggingNode.x = Math.max(10, newX);
        StudioState.draggingNode.y = Math.max(10, newY);

        // Update DOM node position directly for smooth 60fps drag
        const domNode = document.getElementById(`node_${StudioState.draggingNode.id}`);
        if (domNode) {
            domNode.style.left = `${StudioState.draggingNode.x}px`;
            domNode.style.top = `${StudioState.draggingNode.y}px`;
        }
        // Re-render SVG edges connected to this node
        renderOnlyEdges();
    }

    function onMouseUp() {
        StudioState.draggingNode = null;
        window.removeEventListener('mousemove', onMouseMove);
        window.removeEventListener('mouseup', onMouseUp);
        renderCanvas();
    }

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
}

function renderOnlyEdges() {
    const graph = getCurrentGraph();
    const edgesGroup = document.getElementById('edgesGroup');
    if (!edgesGroup) return;
    edgesGroup.innerHTML = '';
    const nodeMap = {};
    graph.nodes.forEach(n => nodeMap[n.id] = n);

    graph.edges.forEach(edge => {
        const sNode = nodeMap[edge.source];
        const tNode = nodeMap[edge.target];
        if (sNode && tNode) {
            const isSelected = StudioState.selected && StudioState.selected.type === 'edge' && StudioState.selected.id === edge.id;
            renderEdge(edge, sNode, tNode, edgesGroup, isSelected);
        }
    });
}

// Selection Handling
function selectElement(type, id) {
    StudioState.selected = { type, id };
    renderCanvas();
}

function clearSelection() {
    StudioState.selected = null;
    renderCanvas();
}

// Canvas Panning and Background Interaction
function setupCanvasEvents() {
    const viewport = document.getElementById('canvasViewport');
    if (!viewport) return;

    viewport.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 0.08 : -0.08;
        zoomCanvas(delta);
    });

    // Keyboard shortcuts (Delete, Escape, Ctrl+Z)
    window.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        if (e.key === 'Delete' || e.key === 'Backspace') {
            if (StudioState.selected) {
                deleteSelectedElement();
            }
        } else if (e.key === 'Escape') {
            if (StudioState.isConnecting) {
                toggleConnectMode(false);
            }
            clearSelection();
        }
    });
}

function onCanvasMouseDown(e) {
    if (e.target.id === 'canvasViewport' || e.target.id === 'svgEdgesLayer') {
        if (StudioState.isConnecting) {
            toggleConnectMode(false);
            return;
        }
        clearSelection();
        // Start Canvas Panning
        StudioState.isPanning = true;
        StudioState.panStart = {
            x: e.clientX - StudioState.pan.x,
            y: e.clientY - StudioState.pan.y
        };
        const viewport = document.getElementById('canvasViewport');
        viewport.classList.add('panning');

        function onPanMove(moveEvent) {
            if (!StudioState.isPanning) return;
            StudioState.pan.x = moveEvent.clientX - StudioState.panStart.x;
            StudioState.pan.y = moveEvent.clientY - StudioState.panStart.y;
            const container = document.getElementById('nodesContainer');
            const edgesGroup = document.getElementById('edgesGroup');
            if (container) {
                container.style.transform = `translate(${StudioState.pan.x}px, ${StudioState.pan.y}px) scale(${StudioState.zoom})`;
            }
            if (edgesGroup) {
                edgesGroup.style.transform = `translate(${StudioState.pan.x}px, ${StudioState.pan.y}px) scale(${StudioState.zoom})`;
                edgesGroup.setAttribute('transform', `translate(${StudioState.pan.x}, ${StudioState.pan.y}) scale(${StudioState.zoom})`);
            }
        }

        function onPanUp() {
            StudioState.isPanning = false;
            viewport.classList.remove('panning');
            window.removeEventListener('mousemove', onPanMove);
            window.removeEventListener('mouseup', onPanUp);
        }

        window.addEventListener('mousemove', onPanMove);
        window.addEventListener('mouseup', onPanUp);
    }
}

// Zoom
function zoomCanvas(delta) {
    StudioState.zoom = Math.min(2.0, Math.max(0.4, StudioState.zoom + delta));
    const txt = document.getElementById('zoomLevelText');
    if (txt) txt.textContent = `${Math.round(StudioState.zoom * 100)}%`;
    renderCanvas();
}

function resetCanvasZoom() {
    StudioState.zoom = 1.0;
    StudioState.pan = { x: 0, y: 0 };
    const txt = document.getElementById('zoomLevelText');
    if (txt) txt.textContent = `100%`;
    renderCanvas();
}

// Adding Elements
function addNode(type) {
    const graph = getCurrentGraph();
    const newId = `${type}_${Date.now().toString(36)}`;
    let label = 'New Node';
    let number = '';
    let w = 180, h = 80;

    if (type === 'entity') {
        label = `External Entity ${graph.nodes.filter(n => n.type === 'entity').length + 1}`;
    } else if (type === 'process') {
        const procCount = graph.nodes.filter(n => n.type === 'process').length;
        number = StudioState.currentLevel === 0 ? '0' : `${procCount + 1}.0`;
        label = `Process ${number}`;
        if (StudioState.currentLevel === 0) {
            label = StudioState.projectName;
            w = 220; h = 100;
        }
    } else if (type === 'datastore') {
        const dsCount = graph.nodes.filter(n => n.type === 'datastore').length;
        number = `D${dsCount + 1}`;
        label = `Data Store ${number}`;
        w = 200; h = 65;
    }

    // Place near center of visible viewport
    const x = Math.round((-StudioState.pan.x + 400) / StudioState.zoom);
    const y = Math.round((-StudioState.pan.y + 250) / StudioState.zoom);

    graph.nodes.push({
        id: newId,
        type: type,
        number: number,
        label: label,
        x: Math.max(50, x),
        y: Math.max(50, y),
        width: w,
        height: h
    });

    selectElement('node', newId);
    if (window.showToast) window.showToast(`Added ${type}: "${label}"`, 'success');
}

// Connect Flow Mode (Drawing arrows between nodes)
function toggleConnectMode(forceState) {
    if (typeof forceState === 'boolean') {
        StudioState.isConnecting = forceState;
    } else {
        StudioState.isConnecting = !StudioState.isConnecting;
    }

    const btn = document.getElementById('btnConnectMode');
    const lbl = document.getElementById('connectModeLabel');
    const viewport = document.getElementById('canvasViewport');

    if (StudioState.isConnecting) {
        StudioState.connectSource = null;
        if (btn) btn.className = 'btn btn-sm btn-warning w-100 py-2 fw-bold shadow-sm';
        if (lbl) lbl.textContent = 'Click Source Node...';
        if (viewport) viewport.classList.add('connecting');
        if (window.showToast) window.showToast('Select Source Node to begin data flow arrow', 'warning');
    } else {
        StudioState.connectSource = null;
        if (btn) btn.className = 'btn btn-sm btn-outline-warning w-100 py-2';
        if (lbl) lbl.textContent = 'Connect Data Flow (Arrow)';
        if (viewport) viewport.classList.remove('connecting');
    }
}

function handleConnectClick(nodeId) {
    if (!StudioState.isConnecting) return;

    if (!StudioState.connectSource) {
        // First click: select source
        StudioState.connectSource = nodeId;
        const lbl = document.getElementById('connectModeLabel');
        if (lbl) lbl.textContent = 'Click Target Node...';
        if (window.showToast) window.showToast('Now click Target Node to connect', 'info');
    } else {
        // Second click: select target
        const sourceId = StudioState.connectSource;
        const targetId = nodeId;

        if (sourceId === targetId) {
            if (window.showToast) window.showToast('Cannot connect a node to itself', 'warning');
            return;
        }

        const flowLabel = prompt("Enter Data Flow Label (e.g. 'User Credentials', 'Payment Receipt', 'Transaction Record'):", "Data Flow");
        if (flowLabel !== null) {
            const graph = getCurrentGraph();
            const newEdgeId = `edge_${Date.now().toString(36)}`;
            graph.edges.push({
                id: newEdgeId,
                source: sourceId,
                target: targetId,
                label: flowLabel.trim() || "Data Flow"
            });
            toggleConnectMode(false);
            selectElement('edge', newEdgeId);
            if (window.showToast) window.showToast(`Connected flow: "${flowLabel}"`, 'success');
        } else {
            toggleConnectMode(false);
        }
    }
}

// Edit Modal Handling
function openEditModal(type, id) {
    const graph = getCurrentGraph();
    const modalEl = document.getElementById('editElementModal');
    if (!modalEl) return;

    const titleEl = document.getElementById('editElementTitle');
    const numInput = document.getElementById('editNumberInput');
    const numGroup = document.getElementById('editNumberGroup');
    const lblInput = document.getElementById('editLabelInput');
    const descInput = document.getElementById('editDescInput');
    const descGroup = document.getElementById('editDescGroup');

    if (type === 'node') {
        const node = graph.nodes.find(n => n.id === id);
        if (!node) return;
        titleEl.textContent = `Edit ${node.type.toUpperCase()}: ${node.label}`;
        lblInput.value = node.label || '';
        numInput.value = node.number || '';
        descInput.value = node.description || '';

        if (node.type === 'entity') {
            numGroup.style.display = 'none';
        } else {
            numGroup.style.display = 'block';
        }
        descGroup.style.display = 'block';
    } else {
        const edge = graph.edges.find(e => e.id === id);
        if (!edge) return;
        titleEl.textContent = `Edit Data Flow`;
        lblInput.value = edge.label || '';
        numGroup.style.display = 'none';
        descGroup.style.display = 'none';
    }

    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

function saveElementEdit() {
    if (!StudioState.selected) return;
    const { type, id } = StudioState.selected;
    const graph = getCurrentGraph();

    const lblInput = document.getElementById('editLabelInput').value.trim();
    const numInput = document.getElementById('editNumberInput').value.trim();
    const descInput = document.getElementById('editDescInput').value.trim();

    if (type === 'node') {
        const node = graph.nodes.find(n => n.id === id);
        if (node) {
            node.label = lblInput || node.label;
            node.number = numInput;
            node.description = descInput;
        }
    } else {
        const edge = graph.edges.find(e => e.id === id);
        if (edge) {
            edge.label = lblInput || edge.label;
        }
    }

    const modalEl = document.getElementById('editElementModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();

    renderCanvas();
    if (window.showToast) window.showToast('Element updated successfully', 'success');
}

function deleteSelectedElement() {
    if (!StudioState.selected) return;
    const { type, id } = StudioState.selected;
    const graph = getCurrentGraph();

    if (type === 'node') {
        graph.nodes = graph.nodes.filter(n => n.id !== id);
        // Also remove any edges connected to this node
        graph.edges = graph.edges.filter(e => e.source !== id && e.target !== id);
    } else {
        graph.edges = graph.edges.filter(e => e.id !== id);
    }

    StudioState.selected = null;
    const modalEl = document.getElementById('editElementModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();

    renderCanvas();
    if (window.showToast) window.showToast('Element deleted', 'secondary');
}

// Inspector Drawer Updates
function updateInspector() {
    const drawerProps = document.getElementById('inspectorProperties');
    const typeBadge = document.getElementById('selectionTypeBadge');
    if (!drawerProps || !typeBadge) return;

    if (!StudioState.selected) {
        typeBadge.textContent = "No Selection";
        typeBadge.className = "badge bg-secondary rounded-pill";
        drawerProps.innerHTML = `<p class="text-secondary small">Click on any Entity, Process, Data Store, or Data Flow to view and edit its software engineering attributes.</p>`;
        return;
    }

    const { type, id } = StudioState.selected;
    const graph = getCurrentGraph();

    if (type === 'node') {
        const node = graph.nodes.find(n => n.id === id);
        if (!node) return;

        typeBadge.textContent = node.type.toUpperCase();
        typeBadge.className = node.type === 'entity' ? 'badge bg-info' : (node.type === 'process' ? 'badge bg-primary' : 'badge bg-success');

        drawerProps.innerHTML = `
            <div class="mb-2">
                <label class="form-label small text-secondary fw-semibold mb-1">Label</label>
                <input type="text" class="form-control form-control-sm" value="${escapeHtml(node.label)}" onchange="updateSelectedNodeProp('label', this.value)">
            </div>
            ${node.type !== 'entity' ? `
            <div class="mb-2">
                <label class="form-label small text-secondary fw-semibold mb-1">Number / ID</label>
                <input type="text" class="form-control form-control-sm font-mono" value="${escapeHtml(node.number || '')}" onchange="updateSelectedNodeProp('number', this.value)">
            </div>` : ''}
            <div class="mb-2">
                <label class="form-label small text-secondary fw-semibold mb-1">Description / Spec</label>
                <textarea class="form-control form-control-sm" rows="2" onchange="updateSelectedNodeProp('description', this.value)">${escapeHtml(node.description || '')}</textarea>
            </div>
            <div class="d-flex gap-2 mt-3">
                <button class="btn btn-sm btn-outline-danger w-100" onclick="deleteSelectedElement()"><i class="bi bi-trash me-1"></i> Delete Node</button>
            </div>
        `;
    } else {
        const edge = graph.edges.find(e => e.id === id);
        if (!edge) return;

        const sNode = graph.nodes.find(n => n.id === edge.source);
        const tNode = graph.nodes.find(n => n.id === edge.target);

        typeBadge.textContent = "DATA FLOW";
        typeBadge.className = "badge bg-warning text-dark";

        drawerProps.innerHTML = `
            <div class="mb-2">
                <label class="form-label small text-secondary fw-semibold mb-1">Flow Label</label>
                <input type="text" class="form-control form-control-sm" value="${escapeHtml(edge.label)}" onchange="updateSelectedEdgeProp('label', this.value)">
            </div>
            <div class="small text-secondary mb-1">Source: <span class="fw-semibold text-white">${escapeHtml(sNode ? sNode.label : edge.source)}</span></div>
            <div class="small text-secondary mb-2">Destination: <span class="fw-semibold text-white">${escapeHtml(tNode ? tNode.label : edge.target)}</span></div>
            <div class="d-flex gap-2 mt-3">
                <button class="btn btn-sm btn-outline-danger w-100" onclick="deleteSelectedElement()"><i class="bi bi-trash me-1"></i> Delete Flow</button>
            </div>
        `;
    }
}

function updateSelectedNodeProp(prop, val) {
    if (!StudioState.selected || StudioState.selected.type !== 'node') return;
    const graph = getCurrentGraph();
    const node = graph.nodes.find(n => n.id === StudioState.selected.id);
    if (node) {
        node[prop] = val;
        renderCanvas();
    }
}

function updateSelectedEdgeProp(prop, val) {
    if (!StudioState.selected || StudioState.selected.type !== 'edge') return;
    const graph = getCurrentGraph();
    const edge = graph.edges.find(e => e.id === StudioState.selected.id);
    if (edge) {
        edge[prop] = val;
        renderCanvas();
    }
}

function updateComponentStats() {
    const graph = getCurrentGraph();
    const nEntities = graph.nodes.filter(n => n.type === 'entity').length;
    const nProcesses = graph.nodes.filter(n => n.type === 'process').length;
    const nStores = graph.nodes.filter(n => n.type === 'datastore').length;
    const nEdges = graph.edges.length;

    const elE = document.getElementById('statEntities');
    const elP = document.getElementById('statProcesses');
    const elS = document.getElementById('statStores');
    const elF = document.getElementById('statEdges');

    if (elE) elE.textContent = nEntities;
    if (elP) elP.textContent = nProcesses;
    if (elS) elS.textContent = nStores;
    if (elF) elF.textContent = nEdges;
}

// Rule Validation (AJAX or Local Heuristic)
async function validateActiveDiagram() {
    const graph = getCurrentGraph();
    const alertsBox = document.getElementById('validationAlertsBox');
    const scoreBadge = document.getElementById('scoreBadge');
    if (!alertsBox) return;

    try {
        const response = await fetch('/api/validate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                graph_data: graph,
                level: StudioState.currentLevel
            })
        });

        const data = await response.json();
        const score = data.score || 100;

        if (scoreBadge) {
            scoreBadge.textContent = `${score} / 100`;
            scoreBadge.className = score >= 90 ? 'badge bg-success fs-6' : (score >= 65 ? 'badge bg-warning text-dark fs-6' : 'badge bg-danger fs-6');
        }

        if (data.valid && (!data.warnings || data.warnings.length === 0)) {
            alertsBox.innerHTML = `
                <div class="alert alert-success py-2 px-3 small mb-2 d-flex align-items-center gap-2">
                    <i class="bi bi-check-circle-fill fs-5 text-success"></i>
                    <div>All Gane-Sarson & Yourdon rules satisfied! No miracles or black holes.</div>
                </div>
            `;
        } else {
            let html = '';
            if (data.errors && data.errors.length > 0) {
                data.errors.forEach(err => {
                    html += `
                        <div class="alert alert-danger py-1 px-2 small mb-1 d-flex align-items-center gap-2">
                            <i class="bi bi-x-circle-fill text-danger"></i>
                            <div>${escapeHtml(err)}</div>
                        </div>
                    `;
                });
            }
            if (data.warnings && data.warnings.length > 0) {
                data.warnings.forEach(warn => {
                    html += `
                        <div class="alert alert-warning py-1 px-2 small mb-1 d-flex align-items-center gap-2 text-dark">
                            <i class="bi bi-exclamation-triangle-fill text-warning"></i>
                            <div>${escapeHtml(warn)}</div>
                        </div>
                    `;
                });
            }
            alertsBox.innerHTML = html;
        }
    } catch (e) {
        console.warn("Validation check fallback:", e);
    }
}

// Auto-Layout Execution
async function autoLayoutCurrentLevel() {
    const graph = getCurrentGraph();
    try {
        const response = await fetch('/api/autolayout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                graph_data: graph,
                width: 1200,
                height: 700
            })
        });
        const arranged = await response.json();
        if (arranged && arranged.nodes) {
            StudioState.levels[StudioState.currentLevel] = arranged;
            renderCanvas();
            if (window.showToast) window.showToast('Hierarchical auto-layout applied!', 'success');
        }
    } catch (e) {
        console.error("Auto-layout failed:", e);
    }
}

// AI Generator
function openAIGeneratorModal() {
    const modalEl = document.getElementById('aiGeneratorModal');
    if (!modalEl) return;
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

function setAIPrompt(text) {
    document.getElementById('aiPromptInput').value = text;
}

async function executeAIGeneration() {
    const prompt = document.getElementById('aiPromptInput').value.trim();
    const systemName = document.getElementById('aiSystemNameInput').value.trim();
    const btn = document.getElementById('btnExecuteAI');

    if (!prompt) {
        alert("Please enter a system requirement description.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Synthesizing DFD...`;

    try {
        const response = await fetch('/api/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ prompt, system_name: systemName })
        });

        const data = await response.json();
        if (data.level0 && data.level1) {
            StudioState.projectName = data.system_name || "Generated System";
            document.getElementById('projectTitleInput').value = StudioState.projectName;
            StudioState.levels[0] = data.level0;
            StudioState.levels[1] = data.level1;
            StudioState.currentLevel = 0;
            updateLevelButtons();
            renderCanvas();

            const modalEl = document.getElementById('aiGeneratorModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            if (window.showToast) window.showToast(`Successfully generated "${StudioState.projectName}" DFD!`, 'success');
        } else {
            alert(data.error || "Generation failed.");
        }
    } catch (e) {
        alert("AI Generation request failed: " + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i class="bi bi-cpu"></i> Generate DFD`;
    }
}

// Data Dictionary Modal
async function openDataDictionaryModal() {
    const modalEl = document.getElementById('dataDictionaryModal');
    const tableBody = document.getElementById('dictTableBody');
    const sysTitle = document.getElementById('dictSystemTitle');
    if (!modalEl || !tableBody) return;

    sysTitle.textContent = `${StudioState.projectName} — Software Engineering Data Dictionary`;

    const graph = getCurrentGraph();
    tableBody.innerHTML = `<tr><td colspan="5" class="text-center py-3 text-secondary">Loading dictionary entries...</td></tr>`;

    const modal = new bootstrap.Modal(modalEl);
    modal.show();

    try {
        const response = await fetch('/api/data-dictionary/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ graph_data: graph })
        });
        const data = await response.json();
        const entries = data.entries || [];

        if (entries.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-secondary">No data elements found. Add processes, datastores, and labeled data flows to populate the dictionary.</td></tr>`;
            return;
        }

        let html = '';
        entries.forEach(item => {
            const catBadge = item.category === 'Data Flow' ? 'badge bg-warning text-dark' : (item.category === 'Data Store' ? 'badge bg-success' : 'badge bg-primary');
            html += `
                <tr>
                    <td class="fw-bold">${escapeHtml(item.name)}</td>
                    <td><span class="${catBadge}">${escapeHtml(item.category)}</span></td>
                    <td class="font-mono small">${escapeHtml(item.source)}</td>
                    <td class="font-mono small">${escapeHtml(item.destination)}</td>
                    <td class="small text-secondary font-mono">${escapeHtml(item.composition)}</td>
                </tr>
            `;
        });
        tableBody.innerHTML = html;
    } catch (e) {
        tableBody.innerHTML = `<tr><td colspan="5" class="text-danger py-3">Failed to load data dictionary: ${escapeHtml(e.message)}</td></tr>`;
    }
}

function printDataDictionary() {
    window.print();
}

function exportDataDictionaryCSV() {
    const table = document.getElementById('dictTable');
    if (!table) return;
    let csv = [];
    for (let row of table.rows) {
        let cols = [];
        for (let cell of row.cells) {
            cols.push('"' + cell.innerText.replace(/"/g, '""') + '"');
        }
        csv.push(cols.join(','));
    }
    const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${StudioState.projectName.replace(/\s+/g, '_')}_Data_Dictionary.csv`;
    a.click();
}

// Project Persistence (Save to Database)
function openSaveModal() {
    document.getElementById('saveProjectNameInput').value = StudioState.projectName;
    const modalEl = document.getElementById('saveProjectModal');
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

async function executeSaveProject() {
    const name = document.getElementById('saveProjectNameInput').value.trim() || "Untitled DFD";
    const desc = document.getElementById('saveProjectDescInput').value.trim();

    const payload = {
        name: name,
        description: desc,
        notation_style: StudioState.notationStyle,
        project_id: StudioState.projectId,
        diagrams: [
            { level: 0, name: "Level 0 Context Diagram", graph_data: StudioState.levels[0] },
            { level: 1, name: "Level 1 Decomposition Diagram", graph_data: StudioState.levels[1] },
            { level: 2, name: "Level 2 Detailed Diagram", graph_data: StudioState.levels[2] }
        ]
    };

    try {
        const response = await fetch('/api/projects/save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(payload)
        });
        const res = await response.json();
        if (res.status === 'success') {
            StudioState.projectId = res.project_id;
            StudioState.projectName = name;
            document.getElementById('projectTitleInput').value = name;
            const modalEl = document.getElementById('saveProjectModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            if (window.showToast) window.showToast(res.message, 'success');
        }
    } catch (e) {
        alert("Failed to save project: " + e.message);
    }
}

// Exporters: PNG, SVG, JSON
function exportDiagram(format) {
    const graph = getCurrentGraph();
    const title = (StudioState.projectName || "DFD").replace(/[^a-zA-Z0-9_-]/g, '_');
    const levelStr = `Level_${StudioState.currentLevel}`;

    if (format === 'json') {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
            projectName: StudioState.projectName,
            notationStyle: StudioState.notationStyle,
            currentLevel: StudioState.currentLevel,
            levels: StudioState.levels
        }, null, 2));
        const dl = document.createElement('a');
        dl.setAttribute("href", dataStr);
        dl.setAttribute("download", `${title}_${levelStr}.json`);
        dl.click();
        if (window.showToast) window.showToast('Project JSON exported!', 'success');
        return;
    }

    if (format === 'svg') {
        const svgContent = generateStandaloneSVG();
        const blob = new Blob([svgContent], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${title}_${levelStr}.svg`;
        a.click();
        if (window.showToast) window.showToast('Vector SVG exported!', 'success');
        return;
    }

    if (format === 'png') {
        exportPNG(title, levelStr);
    }
}

function exportPNG(title, levelStr) {
    const svgContent = generateStandaloneSVG();
    const img = new Image();
    const blob = new Blob([svgContent], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    img.onload = function() {
        const canvas = document.createElement('canvas');
        canvas.width = 1600;
        canvas.height = 1000;
        const ctx = canvas.getContext('2d');
        // Background
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);

        const pngUrl = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = pngUrl;
        a.download = `${title}_${levelStr}.png`;
        a.click();
        URL.revokeObjectURL(url);
        if (window.showToast) window.showToast('High-Resolution PNG exported!', 'success');
    };
    img.src = url;
}

function generateStandaloneSVG() {
    const graph = getCurrentGraph();
    let minX = 9999, minY = 9999, maxX = -9999, maxY = -9999;
    graph.nodes.forEach(n => {
        minX = Math.min(minX, n.x);
        minY = Math.min(minY, n.y);
        maxX = Math.max(maxX, n.x + (n.width || 180));
        maxY = Math.max(maxY, n.y + (n.height || 80));
    });

    const pad = 80;
    const viewBoxX = Math.max(0, minX - pad);
    const viewBoxY = Math.max(0, minY - pad);
    const viewBoxW = Math.max(1200, (maxX - minX) + (pad * 2));
    const viewBoxH = Math.max(800, (maxY - minY) + (pad * 2));

    const edgesGroup = document.getElementById('edgesGroup').innerHTML;

    let nodesSvg = '';
    graph.nodes.forEach(n => {
        const w = n.width || 180;
        const h = n.height || 80;
        if (n.type === 'entity') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" rx="4" fill="#0369a1" stroke="#38bdf8" stroke-width="2"/>
                    <text x="${w/2}" y="${h/2 + 5}" text-anchor="middle" fill="#f0f9ff" font-family="sans-serif" font-weight="bold" font-size="13">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'process') {
            const num = n.number || '0';
            if (StudioState.notationStyle === 'gane_sarson') {
                nodesSvg += `
                    <g transform="translate(${n.x}, ${n.y})">
                        <rect width="${w}" height="${h}" rx="14" fill="#4338ca" stroke="#818cf8" stroke-width="2"/>
                        <rect width="${w}" height="22" rx="14" fill="rgba(0,0,0,0.3)"/>
                        <text x="${w/2}" y="16" text-anchor="middle" fill="#c7d2fe" font-family="monospace" font-size="11">${escapeHtml(num)}</text>
                        <text x="${w/2}" y="${(h/2) + 12}" text-anchor="middle" fill="#eef2ff" font-family="sans-serif" font-weight="bold" font-size="12">${escapeHtml(n.label)}</text>
                    </g>
                `;
            } else {
                const r = Math.min(w, h) / 2;
                nodesSvg += `
                    <g transform="translate(${n.x + r}, ${n.y + r})">
                        <circle r="${r}" fill="#4338ca" stroke="#818cf8" stroke-width="2"/>
                        <text x="0" y="-8" text-anchor="middle" fill="#c7d2fe" font-family="monospace" font-size="11">${escapeHtml(num)}</text>
                        <line x1="-${r*0.7}" y1="-2" x2="${r*0.7}" y2="-2" stroke="rgba(255,255,255,0.3)"/>
                        <text x="0" y="14" text-anchor="middle" fill="#eef2ff" font-family="sans-serif" font-weight="bold" font-size="11">${escapeHtml(n.label)}</text>
                    </g>
                `;
            }
        } else if (n.type === 'datastore') {
            const dsNum = n.number || 'D1';
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" fill="#047857" stroke="#34d399" stroke-width="2"/>
                    <rect width="40" height="${h}" fill="rgba(0,0,0,0.3)"/>
                    <text x="20" y="${h/2 + 5}" text-anchor="middle" fill="#a7f3d0" font-family="monospace" font-size="12">${escapeHtml(dsNum)}</text>
                    <text x="${(w + 40)/2}" y="${h/2 + 5}" text-anchor="middle" fill="#ecfdf5" font-family="sans-serif" font-weight="bold" font-size="12">${escapeHtml(n.label)}</text>
                </g>
            `;
        }
    });

    return `
    <svg xmlns="http://www.w3.org/2000/svg" width="${viewBoxW}" height="${viewBoxH}" viewBox="${viewBoxX} ${viewBoxY} ${viewBoxW} ${viewBoxH}">
        <style>
            .flow-path { stroke: #94a3b8; stroke-width: 2.2; fill: none; }
            .flow-label { font-family: sans-serif; font-size: 11px; font-weight: 600; fill: #ffffff; }
            .flow-label-bg { fill: #0f172a; stroke: #475569; stroke-width: 1px; rx: 4px; ry: 4px; }
        </style>
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
            </marker>
        </defs>
        <rect x="${viewBoxX}" y="${viewBoxY}" width="${viewBoxW}" height="${viewBoxH}" fill="#0b1120"/>
        <g id="exportedEdges">${edgesGroup}</g>
        <g id="exportedNodes">${nodesSvg}</g>
    </svg>
    `;
}

function importJSONFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (data.levels) {
                StudioState.projectName = data.projectName || "Imported Project";
                document.getElementById('projectTitleInput').value = StudioState.projectName;
                StudioState.notationStyle = data.notationStyle || "gane_sarson";
                StudioState.levels = data.levels;
                StudioState.currentLevel = data.currentLevel || 0;
                updateLevelButtons();
                renderCanvas();
                if (window.showToast) window.showToast('Project imported successfully!', 'success');
            } else {
                alert("Invalid DFD JSON file structure.");
            }
        } catch (err) {
            alert("Error parsing JSON file: " + err.message);
        }
    };
    reader.readAsText(file);
}

// Helpers
function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function getCsrfToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}
