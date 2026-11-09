/**
 * DFD Studio Core Engine — Full User-Defined & Predefined Suite
 * Comprehensive diagramming symbols (Process, Entity, DataStore, Database, Decision, Cloud, Document, Note, Text, Boundary),
 * Interactive connection drawing from anchor ports, 8-point shape resizing,
 * in-place inline double-click editing, real-time Inspector editing, custom symbol creator,
 * undo/redo history, Gane-Sarson & Yourdon notation, SE rule verification, and standalone exporters.
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
    activeTool: 'pointer', // 'pointer' | 'connector' | 'text'
    isConnecting: false,
    connectSource: null,
    snapToGrid: true,
    gridSize: 10,

    // Interactive Connection Drawing (from ports)
    drawingConnection: null, // { sourceNode, sourcePort, startX, startY }

    // Canvas Navigation
    zoom: 1.0,
    pan: { x: 0, y: 0 },
    isPanning: false,
    panStart: { x: 0, y: 0 },
    draggingNode: null,
    dragOffset: { x: 0, y: 0 },

    // Undo / Redo History Stack
    history: [],
    historyIndex: -1,
    maxHistory: 30
};

// Initialize Studio on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initDefaultTemplate();
    setupCanvasEvents();
    setupTemplateSelector();
    pushHistoryState();
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
        loadTemplateData(selectedT, false);
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

// User-Defined Blank Architecture
function newBlankDiagram() {
    const title = prompt("Enter Name for Your Custom Architecture / Diagram:", "My Custom Architecture");
    if (!title) return;

    StudioState.projectId = null;
    StudioState.projectName = title.trim();
    const titleInput = document.getElementById('projectTitleInput');
    if (titleInput) titleInput.value = StudioState.projectName;

    StudioState.levels = {
        0: {
            nodes: [
                { id: "proc_0", type: "process", number: "0", label: StudioState.projectName, x: 420, y: 220, width: 220, height: 100 }
            ],
            edges: []
        },
        1: { nodes: [], edges: [] },
        2: { nodes: [], edges: [] }
    };
    StudioState.currentLevel = 0;
    StudioState.selected = null;
    StudioState.zoom = 1.0;
    StudioState.pan = { x: 0, y: 0 };

    const sel = document.getElementById('templateSelector');
    if (sel) sel.value = "";

    updateLevelButtons();
    pushHistoryState();
    renderCanvas();
    if (window.showToast) window.showToast(`Created new blank user diagram: "${StudioState.projectName}"`, 'success');
}

// Load Predefined Architecture
function loadTemplateData(tpl, recordHistory = true) {
    StudioState.projectName = tpl.title;
    const titleInput = document.getElementById('projectTitleInput');
    if (titleInput) titleInput.value = tpl.title;
    StudioState.levels[0] = JSON.parse(JSON.stringify(tpl.level0 || { nodes: [], edges: [] }));
    StudioState.levels[1] = JSON.parse(JSON.stringify(tpl.level1 || { nodes: [], edges: [] }));
    StudioState.levels[2] = JSON.parse(JSON.stringify(tpl.level2 || { nodes: [], edges: [] }));
    StudioState.currentLevel = 0;
    StudioState.selected = null;
    StudioState.zoom = 1.0;
    StudioState.pan = { x: 0, y: 0 };
    updateLevelButtons();
    if (recordHistory) pushHistoryState();
    renderCanvas();
    if (window.showToast) window.showToast(`Loaded "${tpl.title}" template!`, 'info');
}

// Load Saved Custom Project
async function loadSavedUserProject(projectId) {
    if (!projectId) return;
    try {
        const res = await fetch(`/api/projects/${projectId}/`);
        const data = await res.json();
        if (data && data.diagrams) {
            StudioState.projectId = data.id;
            StudioState.projectName = data.name;
            const titleInput = document.getElementById('projectTitleInput');
            if (titleInput) titleInput.value = data.name;

            data.diagrams.forEach(d => {
                if (StudioState.levels[d.level] !== undefined) {
                    StudioState.levels[d.level] = d.graph_data;
                }
            });
            StudioState.currentLevel = 0;
            StudioState.selected = null;
            updateLevelButtons();
            pushHistoryState();
            renderCanvas();
            if (window.showToast) window.showToast(`Loaded custom project "${data.name}"`, 'success');
        }
    } catch (e) {
        console.error("Failed to load saved project:", e);
    }
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

// History Management (Undo / Redo)
function pushHistoryState() {
    if (StudioState.historyIndex < StudioState.history.length - 1) {
        StudioState.history = StudioState.history.slice(0, StudioState.historyIndex + 1);
    }
    const snapshot = JSON.stringify(StudioState.levels);
    StudioState.history.push(snapshot);
    if (StudioState.history.length > StudioState.maxHistory) {
        StudioState.history.shift();
    }
    StudioState.historyIndex = StudioState.history.length - 1;
}

function undo() {
    if (StudioState.historyIndex > 0) {
        StudioState.historyIndex--;
        StudioState.levels = JSON.parse(StudioState.history[StudioState.historyIndex]);
        StudioState.selected = null;
        renderCanvas();
        if (window.showToast) window.showToast('Undo', 'secondary');
    }
}

function redo() {
    if (StudioState.historyIndex < StudioState.history.length - 1) {
        StudioState.historyIndex++;
        StudioState.levels = JSON.parse(StudioState.history[StudioState.historyIndex]);
        StudioState.selected = null;
        renderCanvas();
        if (window.showToast) window.showToast('Redo', 'secondary');
    }
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

    if (!container || !edgesGroup) return;

    // Clear existing (preserve previewConnectionPath)
    container.innerHTML = '';
    const previewEl = document.getElementById('previewConnectionPath');
    edgesGroup.innerHTML = '';
    if (previewEl) edgesGroup.appendChild(previewEl);

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

    // 2. Render Nodes (DOM elements with anchor ports & 8-point resize handles)
    graph.nodes.forEach(node => {
        const isSelected = StudioState.selected && StudioState.selected.type === 'node' && StudioState.selected.id === node.id;
        renderNode(node, container, isSelected);
    });

    // 3. Update Inspector & Validation Stats
    updateInspector();
    updateComponentStats();
    validateActiveDiagram();
}

// Render individual edge (smooth Bezier arrow with editable label)
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
        startInlineEditEdge(edge.id, cx, cy);
    });
    svgGroup.appendChild(path);

    // Flow Label centered along curve
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
    const estWidth = Math.max(50, labelText.length * 7 + 16);
    const estHeight = 22;
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
            startInlineEditEdge(edge.id, labelX, labelY);
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

    if (Math.abs(slope) <= hh / hw) {
        ix = dx > 0 ? x1 + hw : x1 - hw;
        iy = y1 + slope * (ix - x1);
    } else {
        iy = dy > 0 ? y1 + hh : y1 - hh;
        ix = x1 + (iy - y1) / slope;
    }
    return { x: ix, y: iy };
}

// Render individual node with all symbols, ports, and resize handles
function renderNode(node, container, isSelected) {
    const el = document.createElement('div');
    el.id = `node_${node.id}`;
    el.style.left = `${node.x}px`;
    el.style.top = `${node.y}px`;
    el.style.width = `${node.width || 180}px`;
    el.style.height = `${node.height || 80}px`;
    el.style.pointerEvents = 'auto';

    if (node.fontSize) {
        el.style.fontSize = node.fontSize;
    }

    let nodeClass = `dfd-node ${isSelected ? 'selected' : ''} `;

    // Apply custom colors if specified
    if (node.fillColor) {
        el.style.backgroundColor = node.fillColor;
    }
    if (node.borderColor) {
        el.style.borderColor = node.borderColor;
    }

    // Symbol Rendering for ALL Types
    if (node.type === 'entity') {
        nodeClass += 'node-entity';
        el.className = nodeClass;
        el.innerHTML = `<div><i class="bi bi-person me-1"></i> <span class="node-label-span">${escapeHtml(node.label || 'Entity')}</span></div>`;
    } else if (node.type === 'process') {
        const num = node.number || (StudioState.currentLevel === 0 ? '0' : '1.0');
        if (StudioState.notationStyle === 'gane_sarson') {
            nodeClass += 'node-process-gane';
            el.className = nodeClass;
            el.innerHTML = `
                <div class="proc-header font-mono">${escapeHtml(num)}</div>
                <div class="proc-body node-label-span">${escapeHtml(node.label || 'Process')}</div>
            `;
        } else {
            // Yourdon circle
            nodeClass += 'node-process-yourdon';
            el.className = nodeClass;
            el.style.borderRadius = '50%';
            el.innerHTML = `
                <div class="proc-num font-mono">${escapeHtml(num)}</div>
                <div class="proc-text small node-label-span">${escapeHtml(node.label || 'Process')}</div>
            `;
        }
    } else if (node.type === 'datastore') {
        const dsNum = node.number || 'D1';
        if (StudioState.notationStyle === 'gane_sarson') {
            nodeClass += 'node-datastore-gane';
            el.className = nodeClass;
            el.innerHTML = `
                <div class="ds-id font-mono">${escapeHtml(dsNum)}</div>
                <div class="ds-name node-label-span">${escapeHtml(node.label || 'Data Store')}</div>
            `;
        } else {
            // Yourdon parallel lines
            nodeClass += 'node-datastore-yourdon';
            el.className = nodeClass;
            el.innerHTML = `<span class="font-mono text-warning me-2">${escapeHtml(dsNum)}</span> <span class="node-label-span">${escapeHtml(node.label || 'Data Store')}</span>`;
        }
    } else if (node.type === 'database') {
        nodeClass += 'node-database';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span"><i class="bi bi-server me-1"></i> ${escapeHtml(node.label || 'Database')}</div>`;
    } else if (node.type === 'decision') {
        nodeClass += 'node-decision';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span"><i class="bi bi-diamond me-1"></i> ${escapeHtml(node.label || 'Decision')}</div>`;
    } else if (node.type === 'cloud') {
        nodeClass += 'node-cloud';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span"><i class="bi bi-cloud me-1"></i> ${escapeHtml(node.label || 'Cloud Service')}</div>`;
    } else if (node.type === 'document') {
        nodeClass += 'node-document';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span"><i class="bi bi-file-earmark-text me-1"></i> ${escapeHtml(node.label || 'Document')}</div>`;
    } else if (node.type === 'note') {
        nodeClass += 'node-note';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span"><i class="bi bi-sticky me-1"></i> ${escapeHtml(node.label || 'Note')}</div>`;
    } else if (node.type === 'text') {
        nodeClass += 'node-text';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span">${escapeHtml(node.label || 'Text Label')}</div>`;
    } else if (node.type === 'boundary') {
        nodeClass += 'node-boundary';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span"><i class="bi bi-bounding-box-circles me-1"></i> ${escapeHtml(node.label || 'System Boundary')}</div>`;
    } else {
        nodeClass += 'node-entity';
        el.className = nodeClass;
        el.innerHTML = `<div class="node-label-span">${escapeHtml(node.label || 'Component')}</div>`;
    }

    // DRAW.IO FEATURE: 4 Connection Ports (North, South, East, West)
    ['n', 's', 'e', 'w'].forEach(pos => {
        const port = document.createElement('div');
        port.className = `connection-port port-${pos}`;
        port.dataset.port = pos;
        port.title = "Drag to draw connection arrow";
        port.addEventListener('mousedown', (e) => {
            e.stopPropagation();
            startPortDrawing(node, pos, e);
        });
        el.appendChild(port);
    });

    // DRAW.IO FEATURE: 8 Resize Handles on Selection
    if (isSelected) {
        ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'].forEach(dir => {
            const handle = document.createElement('div');
            handle.className = `resize-handle resize-handle-${dir}`;
            handle.dataset.dir = dir;
            handle.addEventListener('mousedown', (e) => {
                e.stopPropagation();
                startNodeResize(node, dir, e);
            });
            el.appendChild(handle);
        });
    }

    // Node Event Listeners: Select, Move, and Double-click Inline Edit
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

    // Double-click Inline Label Editing directly on canvas
    el.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        startInlineEditNode(node.id, el);
    });

    container.appendChild(el);
}

// Interactive Connection Drawing with Mouse Drag
function startPortDrawing(sourceNode, port, e) {
    const sWidth = sourceNode.width || 180;
    const sHeight = sourceNode.height || 80;
    let startX = sourceNode.x + (sWidth / 2);
    let startY = sourceNode.y + (sHeight / 2);

    if (port === 'n') { startY = sourceNode.y; }
    else if (port === 's') { startY = sourceNode.y + sHeight; }
    else if (port === 'w') { startX = sourceNode.x; }
    else if (port === 'e') { startX = sourceNode.x + sWidth; }

    StudioState.drawingConnection = {
        sourceNode: sourceNode,
        sourcePort: port,
        startX: startX,
        startY: startY
    };

    const previewPath = document.getElementById('previewConnectionPath');
    if (previewPath) {
        previewPath.style.display = 'block';
        previewPath.setAttribute('d', `M ${startX} ${startY} L ${startX} ${startY}`);
    }

    const viewport = document.getElementById('canvasViewport');
    if (viewport) viewport.classList.add('connecting');

    function onDrawingMove(moveEvent) {
        if (!StudioState.drawingConnection) return;
        const curCanvasX = (moveEvent.clientX - StudioState.pan.x) / StudioState.zoom;
        const curCanvasY = (moveEvent.clientY - StudioState.pan.y) / StudioState.zoom;

        const sx = StudioState.drawingConnection.startX;
        const sy = StudioState.drawingConnection.startY;
        const dx = curCanvasX - sx;
        const dy = curCanvasY - sy;
        const dist = Math.hypot(dx, dy);
        const curvature = Math.min(35, dist * 0.12);
        const normX = -dy / (dist || 1);
        const normY = dx / (dist || 1);
        const cx = ((sx + curCanvasX) / 2) + (normX * curvature);
        const cy = ((sy + curCanvasY) / 2) + (normY * curvature);

        if (previewPath) {
            previewPath.setAttribute('d', `M ${sx} ${sy} Q ${cx} ${cy} ${curCanvasX} ${curCanvasY}`);
        }
    }

    function onDrawingUp(upEvent) {
        window.removeEventListener('mousemove', onDrawingMove);
        window.removeEventListener('mouseup', onDrawingUp);

        if (previewPath) {
            previewPath.style.display = 'none';
            previewPath.setAttribute('d', '');
        }
        if (viewport) viewport.classList.remove('connecting');

        if (!StudioState.drawingConnection) return;
        const srcNode = StudioState.drawingConnection.sourceNode;
        StudioState.drawingConnection = null;

        const upCanvasX = (upEvent.clientX - StudioState.pan.x) / StudioState.zoom;
        const upCanvasY = (upEvent.clientY - StudioState.pan.y) / StudioState.zoom;

        const graph = getCurrentGraph();
        const targetNode = graph.nodes.find(n => {
            if (n.id === srcNode.id) return false;
            const nw = n.width || 180;
            const nh = n.height || 80;
            return (upCanvasX >= n.x && upCanvasX <= n.x + nw &&
                    upCanvasY >= n.y && upCanvasY <= n.y + nh);
        });

        if (targetNode) {
            const newEdgeId = `edge_${Date.now().toString(36)}`;
            const newEdge = {
                id: newEdgeId,
                source: srcNode.id,
                target: targetNode.id,
                label: "Data Flow"
            };
            graph.edges.push(newEdge);
            pushHistoryState();
            selectElement('edge', newEdgeId);

            // Compute midpoint and open inline label editing immediately
            const midX = (srcNode.x + targetNode.x) / 2 + 60;
            const midY = (srcNode.y + targetNode.y) / 2 + 30;
            startInlineEditEdge(newEdgeId, midX, midY);

            if (window.showToast) window.showToast(`Connected flow: ${srcNode.label} ➔ ${targetNode.label}`, 'success');
        }
    }

    window.addEventListener('mousemove', onDrawingMove);
    window.addEventListener('mouseup', onDrawingUp);
}

// 8-Point Interactive Node Resizing
function startNodeResize(node, dir, e) {
    const startClientX = e.clientX;
    const startClientY = e.clientY;
    const origX = node.x;
    const origY = node.y;
    const origW = node.width || 180;
    const origH = node.height || 80;

    function onResizeMove(moveEvent) {
        const deltaX = (moveEvent.clientX - startClientX) / StudioState.zoom;
        const deltaY = (moveEvent.clientY - startClientY) / StudioState.zoom;

        let newX = origX;
        let newY = origY;
        let newW = origW;
        let newH = origH;

        if (dir.includes('e')) {
            newW = Math.max(70, origW + deltaX);
        }
        if (dir.includes('s')) {
            newH = Math.max(40, origH + deltaY);
        }
        if (dir.includes('w')) {
            const possibleW = origW - deltaX;
            if (possibleW >= 70) {
                newW = possibleW;
                newX = origX + deltaX;
            }
        }
        if (dir.includes('n')) {
            const possibleH = origH - deltaY;
            if (possibleH >= 40) {
                newH = possibleH;
                newY = origY + deltaY;
            }
        }

        if (StudioState.snapToGrid) {
            newX = Math.round(newX / StudioState.gridSize) * StudioState.gridSize;
            newY = Math.round(newY / StudioState.gridSize) * StudioState.gridSize;
            newW = Math.round(newW / StudioState.gridSize) * StudioState.gridSize;
            newH = Math.round(newH / StudioState.gridSize) * StudioState.gridSize;
        }

        node.x = newX;
        node.y = newY;
        node.width = newW;
        node.height = newH;

        const domNode = document.getElementById(`node_${node.id}`);
        if (domNode) {
            domNode.style.left = `${node.x}px`;
            domNode.style.top = `${node.y}px`;
            domNode.style.width = `${node.width}px`;
            domNode.style.height = `${node.height}px`;
        }
        renderOnlyEdges();
    }

    function onResizeUp() {
        window.removeEventListener('mousemove', onResizeMove);
        window.removeEventListener('mouseup', onResizeUp);
        pushHistoryState();
        renderCanvas();
    }

    window.addEventListener('mousemove', onResizeMove);
    window.addEventListener('mouseup', onResizeUp);
}

// In-Place Inline Text Editing on Canvas
function startInlineEditNode(nodeId, nodeEl) {
    const graph = getCurrentGraph();
    const node = graph.nodes.find(n => n.id === nodeId);
    if (!node) return;

    const existing = nodeEl.querySelector('.inline-node-editor');
    if (existing) return;

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'inline-node-editor';
    input.value = node.label || '';

    let saved = false;
    function commit() {
        if (saved) return;
        saved = true;
        const val = input.value.trim();
        if (val && val !== node.label) {
            node.label = val;
            pushHistoryState();
            updateInspector();
        }
        if (input.parentNode) input.parentNode.removeChild(input);
        renderCanvas();
    }

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            commit();
        } else if (e.key === 'Escape') {
            saved = true;
            if (input.parentNode) input.parentNode.removeChild(input);
            renderCanvas();
        }
    });

    input.addEventListener('blur', commit);

    nodeEl.appendChild(input);
    input.focus();
    input.select();
}

function startInlineEditEdge(edgeId, x, y) {
    const graph = getCurrentGraph();
    const edge = graph.edges.find(e => e.id === edgeId);
    if (!edge) return;

    const container = document.getElementById('nodesContainer');
    if (!container) return;

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'inline-edge-editor';
    input.value = edge.label || '';
    input.style.left = `${x}px`;
    input.style.top = `${y}px`;

    let saved = false;
    function commit() {
        if (saved) return;
        saved = true;
        const val = input.value.trim();
        if (val && val !== edge.label) {
            edge.label = val;
            pushHistoryState();
            updateInspector();
        }
        if (input.parentNode) input.parentNode.removeChild(input);
        renderCanvas();
    }

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            commit();
        } else if (e.key === 'Escape') {
            saved = true;
            if (input.parentNode) input.parentNode.removeChild(input);
            renderCanvas();
        }
    });

    input.addEventListener('blur', commit);

    container.appendChild(input);
    input.focus();
    input.select();
}

// Drag & Drop Node Movement with Snap-to-Grid
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
        let newX = Math.round(currentCanvasX - StudioState.dragOffset.x);
        let newY = Math.round(currentCanvasY - StudioState.dragOffset.y);

        if (StudioState.snapToGrid) {
            newX = Math.round(newX / StudioState.gridSize) * StudioState.gridSize;
            newY = Math.round(newY / StudioState.gridSize) * StudioState.gridSize;
        }

        StudioState.draggingNode.x = Math.max(10, newX);
        StudioState.draggingNode.y = Math.max(10, newY);

        const domNode = document.getElementById(`node_${StudioState.draggingNode.id}`);
        if (domNode) {
            domNode.style.left = `${StudioState.draggingNode.x}px`;
            domNode.style.top = `${StudioState.draggingNode.y}px`;
        }
        renderOnlyEdges();
    }

    function onMouseUp() {
        if (StudioState.draggingNode) {
            pushHistoryState();
        }
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

    const previewEl = document.getElementById('previewConnectionPath');
    edgesGroup.innerHTML = '';
    if (previewEl) edgesGroup.appendChild(previewEl);

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

// Drag and Drop from Palette to Canvas
function onPaletteDragStart(e, type) {
    e.dataTransfer.setData('text/plain', type);
}

function onCanvasDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
}

function onCanvasDrop(e) {
    e.preventDefault();
    const type = e.dataTransfer.getData('text/plain');
    if (!type) return;

    let canvasX = (e.clientX - StudioState.pan.x) / StudioState.zoom;
    let canvasY = (e.clientY - StudioState.pan.y) / StudioState.zoom;

    if (StudioState.snapToGrid) {
        canvasX = Math.round(canvasX / StudioState.gridSize) * StudioState.gridSize;
        canvasY = Math.round(canvasY / StudioState.gridSize) * StudioState.gridSize;
    }

    addNode(type, canvasX, canvasY);
}

// Quick Color Styling
function setSelectionColor(fillColor, borderColor) {
    if (!StudioState.selected || StudioState.selected.type !== 'node') {
        if (window.showToast) window.showToast('Please select a shape first to color it', 'warning');
        return;
    }
    const graph = getCurrentGraph();
    const node = graph.nodes.find(n => n.id === StudioState.selected.id);
    if (!node) return;

    node.fillColor = fillColor;
    node.borderColor = borderColor || fillColor;
    pushHistoryState();
    renderCanvas();
    if (window.showToast) window.showToast('Updated shape color', 'success');
}

// Duplicate Selected Element
function duplicateSelectedElement() {
    if (!StudioState.selected || StudioState.selected.type !== 'node') {
        if (window.showToast) window.showToast('Select a shape to duplicate (Ctrl+D)', 'info');
        return;
    }
    const graph = getCurrentGraph();
    const original = graph.nodes.find(n => n.id === StudioState.selected.id);
    if (!original) return;

    const newId = `${original.type}_${Date.now().toString(36)}`;
    const cloned = JSON.parse(JSON.stringify(original));
    cloned.id = newId;
    cloned.x += 30;
    cloned.y += 30;
    cloned.label = `${original.label} (Copy)`;

    graph.nodes.push(cloned);
    pushHistoryState();
    selectElement('node', newId);
    if (window.showToast) window.showToast(`Duplicated: ${cloned.label}`, 'success');
}

// Snap-to-Grid Toggle
function toggleSnapGrid() {
    StudioState.snapToGrid = !StudioState.snapToGrid;
    const btn = document.getElementById('btnSnapGrid');
    if (btn) {
        if (StudioState.snapToGrid) {
            btn.classList.add('btn-primary');
            btn.classList.remove('btn-outline-secondary');
        } else {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-secondary');
        }
    }
    if (window.showToast) window.showToast(`Grid Snapping: ${StudioState.snapToGrid ? 'ON (10px)' : 'OFF'}`, 'info');
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

    // Keyboard Shortcuts
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
        } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {
            e.preventDefault();
            if (e.shiftKey) {
                redo();
            } else {
                undo();
            }
        } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') {
            e.preventDefault();
            redo();
        } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'd') {
            e.preventDefault();
            duplicateSelectedElement();
        } else if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
            // Nudge selected node
            if (StudioState.selected && StudioState.selected.type === 'node') {
                e.preventDefault();
                const graph = getCurrentGraph();
                const node = graph.nodes.find(n => n.id === StudioState.selected.id);
                if (node) {
                    const step = e.shiftKey ? 10 : 2;
                    if (e.key === 'ArrowLeft') node.x -= step;
                    if (e.key === 'ArrowRight') node.x += step;
                    if (e.key === 'ArrowUp') node.y -= step;
                    if (e.key === 'ArrowDown') node.y += step;
                    renderCanvas();
                }
            }
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

// Adding Elements for ALL Types
function addNode(type, customX = null, customY = null, customProps = {}) {
    const graph = getCurrentGraph();
    const newId = `${type}_${Date.now().toString(36)}`;
    let label = customProps.label || 'New Node';
    let number = customProps.number || '';
    let w = customProps.width || 180, h = customProps.height || 80;
    let fillColor = customProps.fillColor || null;
    let borderColor = customProps.borderColor || null;

    if (type === 'entity') {
        label = label === 'New Node' ? `External Entity ${graph.nodes.filter(n => n.type === 'entity').length + 1}` : label;
    } else if (type === 'process') {
        const procCount = graph.nodes.filter(n => n.type === 'process').length;
        number = StudioState.currentLevel === 0 ? '0' : `${procCount + 1}.0`;
        label = label === 'New Node' ? `Process ${number}` : label;
        if (StudioState.currentLevel === 0) {
            label = StudioState.projectName;
            w = 220; h = 100;
        }
    } else if (type === 'datastore') {
        const dsCount = graph.nodes.filter(n => n.type === 'datastore').length;
        number = `D${dsCount + 1}`;
        label = label === 'New Node' ? `Data Store ${number}` : label;
        w = 200; h = 65;
    } else if (type === 'database') {
        label = label === 'New Node' ? `Database Storage` : label;
        w = 170; h = 80;
    } else if (type === 'decision') {
        label = label === 'New Node' ? `Decision / Rule` : label;
        w = 150; h = 90;
    } else if (type === 'cloud') {
        label = label === 'New Node' ? `Cloud Service / API` : label;
        w = 190; h = 75;
    } else if (type === 'document') {
        label = label === 'New Node' ? `Report / Document` : label;
        w = 160; h = 80;
    } else if (type === 'note') {
        label = label === 'New Node' ? `Specification Note` : label;
        w = 170; h = 90;
    } else if (type === 'text') {
        label = label === 'New Node' ? `Floating Text Label` : label;
        w = 160; h = 45;
    } else if (type === 'boundary') {
        label = label === 'New Node' ? `Subsystem Boundary` : label;
        w = 320; h = 220;
    }

    let x = customX !== null ? customX : Math.round((-StudioState.pan.x + 380) / StudioState.zoom);
    let y = customY !== null ? customY : Math.round((-StudioState.pan.y + 220) / StudioState.zoom);

    if (StudioState.snapToGrid) {
        x = Math.round(x / StudioState.gridSize) * StudioState.gridSize;
        y = Math.round(y / StudioState.gridSize) * StudioState.gridSize;
    }

    graph.nodes.push({
        id: newId,
        type: type,
        number: number,
        label: label,
        x: Math.max(20, x),
        y: Math.max(20, y),
        width: w,
        height: h,
        fillColor: fillColor,
        borderColor: borderColor
    });

    pushHistoryState();
    selectElement('node', newId);
    if (window.showToast) window.showToast(`Added ${type}: "${label}"`, 'success');
}

// User-Defined Custom Symbol Modal Handlers
function openCustomSymbolModal() {
    const modalEl = document.getElementById('customSymbolModal');
    if (!modalEl) return;
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

function executeCreateCustomSymbol() {
    const label = document.getElementById('customSymLabel').value.trim() || "Custom Component";
    const shape = document.getElementById('customSymShape').value;
    const color = document.getElementById('customSymColor').value;
    const w = parseInt(document.getElementById('customSymW').value) || 180;
    const h = parseInt(document.getElementById('customSymH').value) || 80;

    addNode(shape, null, null, {
        label: label,
        fillColor: color,
        borderColor: color,
        width: w,
        height: h
    });

    const modalEl = document.getElementById('customSymbolModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();
}

// Connect Flow Mode (Drawing arrows between nodes via button)
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
        if (btn) btn.classList.add('btn-warning', 'text-dark');
        if (lbl) lbl.textContent = 'Click Source Node...';
        if (viewport) viewport.classList.add('connecting');
        if (window.showToast) window.showToast('Click Source Node (or drag from any blue port dot)', 'info');
    } else {
        StudioState.connectSource = null;
        if (btn) btn.classList.remove('btn-warning', 'text-dark');
        if (lbl) lbl.textContent = 'Draw Arrow / Flow';
        if (viewport) viewport.classList.remove('connecting');
    }
}

function handleConnectClick(nodeId) {
    if (!StudioState.isConnecting) return;

    if (!StudioState.connectSource) {
        StudioState.connectSource = nodeId;
        const lbl = document.getElementById('connectModeLabel');
        if (lbl) lbl.textContent = 'Click Target Node...';
        if (window.showToast) window.showToast('Now click Target Node to connect', 'info');
    } else {
        const sourceId = StudioState.connectSource;
        const targetId = nodeId;

        if (sourceId === targetId) {
            if (window.showToast) window.showToast('Cannot connect a node to itself', 'warning');
            return;
        }

        const flowLabel = prompt("Enter Data Flow Label (e.g. 'User Credentials', 'Payment Receipt'):", "Data Flow");
        if (flowLabel !== null) {
            const graph = getCurrentGraph();
            const newEdgeId = `edge_${Date.now().toString(36)}`;
            graph.edges.push({
                id: newEdgeId,
                source: sourceId,
                target: targetId,
                label: flowLabel.trim() || "Data Flow"
            });
            pushHistoryState();
            toggleConnectMode(false);
            selectElement('edge', newEdgeId);
            if (window.showToast) window.showToast(`Connected flow: "${flowLabel}"`, 'success');
        } else {
            toggleConnectMode(false);
        }
    }
}

// Edit Modal Handling (Secondary dialog for detailed properties)
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

    pushHistoryState();
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
        graph.edges = graph.edges.filter(e => e.source !== id && e.target !== id);
    } else {
        graph.edges = graph.edges.filter(e => e.id !== id);
    }

    pushHistoryState();
    StudioState.selected = null;
    const modalEl = document.getElementById('editElementModal');
    if (modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
    }

    renderCanvas();
    if (window.showToast) window.showToast('Element deleted', 'secondary');
}

// Inspector Drawer Updates — Real-Time Live Text & Style Editing
function updateInspector() {
    const drawerProps = document.getElementById('inspectorProperties');
    const typeBadge = document.getElementById('selectionTypeBadge');
    if (!drawerProps || !typeBadge) return;

    if (!StudioState.selected) {
        typeBadge.textContent = "No Selection";
        typeBadge.className = "badge bg-secondary rounded-pill";
        drawerProps.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-cursor-fill fs-3 text-secondary opacity-50 mb-2 d-block"></i>
                <p class="text-secondary small mb-1">Click on any symbol or arrow to edit text, change dimensions, or customize colors.</p>
                <p class="text-secondary opacity-75" style="font-size:0.75rem;">Tip: You can also <strong>double-click</strong> directly on the canvas to edit text inline!</p>
            </div>
        `;
        return;
    }

    const { type, id } = StudioState.selected;
    const graph = getCurrentGraph();

    if (type === 'node') {
        const node = graph.nodes.find(n => n.id === id);
        if (!node) return;

        typeBadge.textContent = node.type.toUpperCase();
        typeBadge.className = node.type === 'entity' ? 'badge bg-info' : (node.type === 'process' ? 'badge bg-primary' : (node.type === 'database' ? 'badge bg-teal' : 'badge bg-success'));

        drawerProps.innerHTML = `
            <div class="mb-3">
                <label class="form-label small text-secondary fw-bold mb-1">Text / Label</label>
                <input type="text" class="form-control form-control-sm" value="${escapeHtml(node.label)}" oninput="updateSelectedNodeProp('label', this.value)" placeholder="Enter label">
            </div>

            ${node.type === 'process' || node.type === 'datastore' ? `
            <div class="mb-3">
                <label class="form-label small text-secondary fw-bold mb-1">ID / Process Number</label>
                <input type="text" class="form-control form-control-sm font-mono" value="${escapeHtml(node.number || '')}" oninput="updateSelectedNodeProp('number', this.value)" placeholder="e.g. 1.0, D1">
            </div>` : ''}

            <div class="mb-3">
                <label class="form-label small text-secondary fw-bold mb-1">Font Size</label>
                <select class="form-select form-select-sm" onchange="updateSelectedNodeProp('fontSize', this.value)">
                    <option value="0.75rem" ${node.fontSize === '0.75rem' ? 'selected' : ''}>Small (12px)</option>
                    <option value="0.85rem" ${!node.fontSize || node.fontSize === '0.85rem' ? 'selected' : ''}>Standard (14px)</option>
                    <option value="1rem" ${node.fontSize === '1rem' ? 'selected' : ''}>Medium (16px)</option>
                    <option value="1.2rem" ${node.fontSize === '1.2rem' ? 'selected' : ''}>Large (19px)</option>
                    <option value="1.4rem" ${node.fontSize === '1.4rem' ? 'selected' : ''}>Title (22px)</option>
                </select>
            </div>

            <div class="mb-3">
                <label class="form-label small text-secondary fw-bold mb-1">Shape Fill Color</label>
                <div class="d-flex align-items-center gap-1 mb-2">
                    <span class="color-swatch" style="background:#0284c7;" onclick="setSelectionColor('#0284c7', '#38bdf8')" title="Blue"></span>
                    <span class="color-swatch" style="background:#4f46e5;" onclick="setSelectionColor('#4f46e5', '#818cf8')" title="Indigo"></span>
                    <span class="color-swatch" style="background:#059669;" onclick="setSelectionColor('#059669', '#34d399')" title="Emerald"></span>
                    <span class="color-swatch" style="background:#d97706;" onclick="setSelectionColor('#d97706', '#fbbf24')" title="Amber"></span>
                    <span class="color-swatch" style="background:#e11d48;" onclick="setSelectionColor('#e11d48', '#fb7185')" title="Rose"></span>
                    <span class="color-swatch" style="background:#7c3aed;" onclick="setSelectionColor('#7c3aed', '#c084fc')" title="Purple"></span>
                    <span class="color-swatch" style="background:#0d9488;" onclick="setSelectionColor('#0d9488', '#2dd4bf')" title="Teal"></span>
                    <span class="color-swatch" style="background:#334155;" onclick="setSelectionColor('#334155', '#64748b')" title="Slate"></span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="small text-secondary" style="font-size:0.75rem;">Custom Color:</span>
                    <input type="color" class="form-control form-control-color form-control-sm" value="${node.fillColor || '#0369a1'}" onchange="setSelectionColor(this.value, this.value)">
                </div>
            </div>

            <div class="row g-2 mb-3">
                <div class="col-6">
                    <label class="form-label small text-secondary fw-bold mb-1">Width (px)</label>
                    <input type="number" class="form-control form-control-sm" value="${node.width || 180}" onchange="updateSelectedNodeProp('width', parseInt(this.value) || 180)">
                </div>
                <div class="col-6">
                    <label class="form-label small text-secondary fw-bold mb-1">Height (px)</label>
                    <input type="number" class="form-control form-control-sm" value="${node.height || 80}" onchange="updateSelectedNodeProp('height', parseInt(this.value) || 80)">
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label small text-secondary fw-bold mb-1">Specification / Details</label>
                <textarea class="form-control form-control-sm" rows="2" oninput="updateSelectedNodeProp('description', this.value)" placeholder="Detailed specifications">${escapeHtml(node.description || '')}</textarea>
            </div>

            <div class="d-flex gap-2 mt-3 pt-2 border-top border-secondary border-opacity-25">
                <button class="btn btn-sm btn-outline-info w-50" onclick="duplicateSelectedElement()"><i class="bi bi-copy me-1"></i> Duplicate</button>
                <button class="btn btn-sm btn-outline-danger w-50" onclick="deleteSelectedElement()"><i class="bi bi-trash me-1"></i> Delete</button>
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
            <div class="mb-3">
                <label class="form-label small text-secondary fw-bold mb-1">Flow Label (Double-click arrow to edit)</label>
                <input type="text" class="form-control form-control-sm" value="${escapeHtml(edge.label)}" oninput="updateSelectedEdgeProp('label', this.value)" placeholder="Enter flow label">
            </div>
            <div class="card bg-body-tertiary p-2 border-0 mb-3 small">
                <div class="text-secondary mb-1">Source: <span class="fw-semibold text-white">${escapeHtml(sNode ? sNode.label : edge.source)}</span></div>
                <div class="text-secondary">Target: <span class="fw-semibold text-white">${escapeHtml(tNode ? tNode.label : edge.target)}</span></div>
            </div>
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
        // Fast DOM update for label to avoid re-rendering entire canvas on every keystroke
        if (prop === 'label') {
            const domNode = document.getElementById(`node_${node.id}`);
            if (domNode) {
                const span = domNode.querySelector('.node-label-span');
                if (span) span.textContent = val;
            }
        } else {
            renderCanvas();
        }
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
    const nStores = graph.nodes.filter(n => n.type === 'datastore' || n.type === 'database').length;
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
            pushHistoryState();
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
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Analyzing & Generating DFD...`;

    try {
        const response = await fetch('/api/generate-dfd/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                prompt: prompt,
                system_name: systemName || "Custom AI Architecture"
            })
        });
        const data = await response.json();

        if (data.status === 'success') {
            StudioState.projectName = data.project_name || "AI Generated System";
            document.getElementById('projectTitleInput').value = StudioState.projectName;
            StudioState.levels[0] = data.levels[0] || { nodes: [], edges: [] };
            StudioState.levels[1] = data.levels[1] || { nodes: [], edges: [] };
            StudioState.levels[2] = data.levels[2] || { nodes: [], edges: [] };
            StudioState.currentLevel = 0;
            StudioState.selected = null;
            pushHistoryState();
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
        ctx.fillStyle = "#0f172a";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);

        const pngUrl = canvas.toDataURL("image/png");
        const a = document.createElement('a');
        a.href = pngUrl;
        a.download = `${title}_${levelStr}.png`;
        a.click();
        URL.revokeObjectURL(url);
        if (window.showToast) window.showToast('High-Res PNG exported!', 'success');
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
        const fill = n.fillColor || (n.type === 'entity' ? '#0369a1' : (n.type === 'process' ? '#4338ca' : (n.type === 'database' ? '#0f766e' : '#047857')));
        const stroke = n.borderColor || (n.type === 'entity' ? '#38bdf8' : (n.type === 'process' ? '#818cf8' : (n.type === 'database' ? '#2dd4bf' : '#34d399')));

        if (n.type === 'entity') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" rx="4" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
                    <text x="${w/2}" y="${h/2 + 5}" text-anchor="middle" fill="#f0f9ff" font-family="sans-serif" font-weight="bold" font-size="13">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'process') {
            const num = n.number || '0';
            if (StudioState.notationStyle === 'gane_sarson') {
                nodesSvg += `
                    <g transform="translate(${n.x}, ${n.y})">
                        <rect width="${w}" height="${h}" rx="14" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
                        <rect width="${w}" height="22" rx="14" fill="rgba(0,0,0,0.3)"/>
                        <text x="${w/2}" y="16" text-anchor="middle" fill="#c7d2fe" font-family="monospace" font-size="11">${escapeHtml(num)}</text>
                        <text x="${w/2}" y="${(h/2) + 12}" text-anchor="middle" fill="#eef2ff" font-family="sans-serif" font-weight="bold" font-size="12">${escapeHtml(n.label)}</text>
                    </g>
                `;
            } else {
                nodesSvg += `
                    <g transform="translate(${n.x}, ${n.y})">
                        <ellipse cx="${w/2}" cy="${h/2}" rx="${w/2}" ry="${h/2}" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
                        <text x="${w/2}" y="${h/2 - 4}" text-anchor="middle" fill="#c7d2fe" font-family="monospace" font-size="11">${escapeHtml(num)}</text>
                        <text x="${w/2}" y="${h/2 + 14}" text-anchor="middle" fill="#eef2ff" font-family="sans-serif" font-weight="bold" font-size="12">${escapeHtml(n.label)}</text>
                    </g>
                `;
            }
        } else if (n.type === 'datastore') {
            const dsNum = n.number || 'D1';
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" rx="2" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
                    <rect width="40" height="${h}" fill="rgba(0,0,0,0.25)"/>
                    <text x="20" y="${h/2 + 4}" text-anchor="middle" fill="#a7f3d0" font-family="monospace" font-size="11">${escapeHtml(dsNum)}</text>
                    <text x="${(w + 40)/2}" y="${h/2 + 4}" text-anchor="middle" fill="#ecfdf5" font-family="sans-serif" font-size="12">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'database') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" rx="12" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
                    <text x="${w/2}" y="${h/2 + 4}" text-anchor="middle" fill="#ccfbf1" font-family="sans-serif" font-weight="bold" font-size="12">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'decision') {
            const pts = `${w/2},0 ${w},${h/2} ${w/2},${h} 0,${h/2}`;
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <polygon points="${pts}" fill="${n.fillColor || '#6d28d9'}" stroke="${n.borderColor || '#a78bfa'}" stroke-width="2"/>
                    <text x="${w/2}" y="${h/2 + 4}" text-anchor="middle" fill="#f5f3ff" font-family="sans-serif" font-weight="bold" font-size="12">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'cloud') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" rx="30" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
                    <text x="${w/2}" y="${h/2 + 4}" text-anchor="middle" fill="#f0f9ff" font-family="sans-serif" font-size="12">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'document') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" rx="4" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
                    <text x="${w/2}" y="${h/2 + 4}" text-anchor="middle" fill="#f8fafc" font-family="sans-serif" font-size="12">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'note') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" fill="${n.fillColor || '#fef08a'}" stroke="${n.borderColor || '#facc15'}" stroke-width="1"/>
                    <text x="10" y="24" fill="#854d0e" font-family="sans-serif" font-size="11">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'text') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <text x="5" y="${h/2 + 4}" fill="#f8fafc" font-family="sans-serif" font-size="13">${escapeHtml(n.label)}</text>
                </g>
            `;
        } else if (n.type === 'boundary') {
            nodesSvg += `
                <g transform="translate(${n.x}, ${n.y})">
                    <rect width="${w}" height="${h}" rx="8" fill="rgba(56, 189, 248, 0.05)" stroke="${n.borderColor || '#38bdf8'}" stroke-width="2" stroke-dasharray="6,4"/>
                    <text x="12" y="20" fill="#38bdf8" font-family="sans-serif" font-weight="bold" font-size="11">${escapeHtml(n.label)}</text>
                </g>
            `;
        }
    });

    return `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBoxX} ${viewBoxY} ${viewBoxW} ${viewBoxH}" width="${viewBoxW}" height="${viewBoxH}">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
                </marker>
                <marker id="arrowhead-selected" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#38bdf8" />
                </marker>
            </defs>
            <style>
                .flow-path { stroke: #94a3b8; stroke-width: 2.2; fill: none; }
                .flow-label { font-family: sans-serif; font-size: 11px; font-weight: bold; fill: #ffffff; }
                .flow-label-bg { fill: #0f172a; stroke: #475569; stroke-width: 1px; rx: 4px; }
            </style>
            <rect x="${viewBoxX}" y="${viewBoxY}" width="${viewBoxW}" height="${viewBoxH}" fill="#0f172a"/>
            <g id="exportEdges">${edgesGroup}</g>
            <g id="exportNodes">${nodesSvg}</g>
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
                pushHistoryState();
                updateLevelButtons();
                renderCanvas();
                if (window.showToast) window.showToast('Project imported successfully!', 'success');
            } else {
                alert("Invalid DFD project JSON format.");
            }
        } catch (err) {
            alert("Failed to parse JSON: " + err.message);
        }
    };
    reader.readAsText(file);
}

// Mermaid.js Syntax Generator
function openMermaidModal() {
    const graph = getCurrentGraph();
    let syntax = 'graph TD\n';

    graph.nodes.forEach(n => {
        const safeId = n.id.replace(/[^a-zA-Z0-9]/g, '_');
        const safeLabel = (n.label || '').replace(/"/g, "'");
        if (n.type === 'entity') {
            syntax += `    ${safeId}["[Entity] ${safeLabel}"]\n`;
        } else if (n.type === 'process') {
            const num = n.number || '0';
            syntax += `    ${safeId}(("${num}: ${safeLabel}"))\n`;
        } else if (n.type === 'datastore' || n.type === 'database') {
            syntax += `    ${safeId}[("[(DataStore)] ${safeLabel}")]\n`;
        } else if (n.type === 'decision') {
            syntax += `    ${safeId}{"${safeLabel}"}\n`;
        } else {
            syntax += `    ${safeId}["${safeLabel}"]\n`;
        }
    });

    graph.edges.forEach(e => {
        const s = e.source.replace(/[^a-zA-Z0-9]/g, '_');
        const t = e.target.replace(/[^a-zA-Z0-9]/g, '_');
        const lbl = (e.label || '').replace(/"/g, "'");
        syntax += `    ${s} -->|${lbl}| ${t}\n`;
    });

    const modalEl = document.getElementById('mermaidModal');
    const codeEl = document.getElementById('mermaidCodeBlock');
    if (codeEl) codeEl.textContent = syntax;
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

function copyMermaidCode() {
    const code = document.getElementById('mermaidCodeBlock').textContent;
    navigator.clipboard.writeText(code).then(() => {
        if (window.showToast) window.showToast('Mermaid syntax copied to clipboard!', 'info');
    });
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
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        const [k, v] = c.trim().split('=');
        if (k === 'csrftoken') return decodeURIComponent(v);
    }
    return '';
}
