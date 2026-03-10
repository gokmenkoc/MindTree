"""
MindTree Backend — Flask REST API
Provides full CRUD for infinite nested nodes, tags, search, and stars.
Data persists in JSON file (no database required).
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import uuid
import time
from datetime import datetime

app = Flask(__name__, static_folder='../frontend')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# ─── SEED DATA ─────────────────────────────────────────────────────────────────

SEED_DATA = {
    "nodes": {
        "root": {
            "id": "root",
            "content": "My MindTree",
            "note": "",
            "children": ["node-1", "node-2", "node-3"],
            "parent": None,
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": [],
            "color": None
        },
        "node-1": {
            "id": "node-1",
            "content": "🚀 Getting Started",
            "note": "Welcome to MindTree — your infinite nested workspace.",
            "children": ["node-1-1", "node-1-2", "node-1-3"],
            "parent": "root",
            "completed": False,
            "starred": True,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": ["#guide"],
            "color": None
        },
        "node-1-1": {
            "id": "node-1-1",
            "content": "Press Enter to create a new item",
            "note": "",
            "children": [],
            "parent": "node-1",
            "completed": True,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": [],
            "color": None
        },
        "node-1-2": {
            "id": "node-1-2",
            "content": "Press Tab to indent, Shift+Tab to outdent",
            "note": "",
            "children": [],
            "parent": "node-1",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": [],
            "color": None
        },
        "node-1-3": {
            "id": "node-1-3",
            "content": "Click any bullet to zoom into that node",
            "note": "",
            "children": [],
            "parent": "node-1",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": [],
            "color": None
        },
        "node-2": {
            "id": "node-2",
            "content": "📋 Work Projects",
            "note": "",
            "children": ["node-2-1", "node-2-2"],
            "parent": "root",
            "completed": False,
            "starred": True,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": ["#work"],
            "color": None
        },
        "node-2-1": {
            "id": "node-2-1",
            "content": "Q2 Planning @team #priority(high)",
            "note": "Review with leadership before end of month.",
            "children": ["node-2-1-1", "node-2-1-2"],
            "parent": "node-2",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": ["@team", "#priority"],
            "color": None
        },
        "node-2-1-1": {
            "id": "node-2-1-1",
            "content": "Draft roadmap slides",
            "note": "",
            "children": [],
            "parent": "node-2-1",
            "completed": True,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": [],
            "color": None
        },
        "node-2-1-2": {
            "id": "node-2-1-2",
            "content": "Schedule stakeholder review",
            "note": "",
            "children": [],
            "parent": "node-2-1",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": [],
            "color": None
        },
        "node-2-2": {
            "id": "node-2-2",
            "content": "Hiring pipeline #hr @alice",
            "note": "",
            "children": [],
            "parent": "node-2",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": ["#hr", "@alice"],
            "color": None
        },
        "node-3": {
            "id": "node-3",
            "content": "💡 Ideas & Notes",
            "note": "",
            "children": ["node-3-1", "node-3-2"],
            "parent": "root",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": ["#ideas"],
            "color": None
        },
        "node-3-1": {
            "id": "node-3-1",
            "content": "Build a personal knowledge management system",
            "note": "Explore Zettelkasten and PKM methodologies.",
            "children": [],
            "parent": "node-3",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": ["#ideas"],
            "color": None
        },
        "node-3-2": {
            "id": "node-3-2",
            "content": "Read: The Extended Mind by Annie Murphy Paul",
            "note": "",
            "children": [],
            "parent": "node-3",
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": ["#reading"],
            "color": None
        }
    },
    "starred_nodes": ["node-1", "node-2"],
    "settings": {
        "theme": "dark",
        "font_size": 15
    }
}

# ─── DATA LAYER ────────────────────────────────────────────────────────────────

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(SEED_DATA)
        return SEED_DATA
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_tags(content):
    import re
    # Match tags and mentions supporting Unicode characters (Turkish etc.)
    # Python 3 re module \w matches Unicode letters by default
    return list(set(re.findall(r'[#@][\w.-]+', content)))

# ─── ROUTES ────────────────────────────────────────────────────────────────────

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "version": "v2-import-debug", "timestamp": time.time()})

# Get full tree
@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    data = load_data()
    return jsonify({
        "nodes": data["nodes"],
        "starred_nodes": data.get("starred_nodes", []),
        "settings": data.get("settings", {})
    })

# Get single node
@app.route('/api/nodes/<node_id>', methods=['GET'])
def get_node(node_id):
    data = load_data()
    node = data["nodes"].get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(node)

# Create node
@app.route('/api/nodes', methods=['POST'])
def create_node():
    data = load_data()
    body = request.json
    node_id = "node-" + str(uuid.uuid4())[:8]
    parent_id = body.get("parent_id", "root")
    insert_after = body.get("insert_after")  # sibling id to insert after
    content = body.get("content", "")

    new_node = {
        "id": node_id,
        "content": content,
        "note": body.get("note", ""),
        "children": [],
        "parent": parent_id,
        "completed": False,
        "starred": False,
        "collapsed": False,
        "created_at": time.time(),
        "updated_at": time.time(),
        "tags": extract_tags(content),
        "color": None
    }

    data["nodes"][node_id] = new_node

    # Add to parent's children
    if parent_id in data["nodes"]:
        siblings = data["nodes"][parent_id]["children"]
        if insert_after and insert_after in siblings:
            idx = siblings.index(insert_after)
            siblings.insert(idx + 1, node_id)
        else:
            siblings.append(node_id)

    save_data(data)
    return jsonify(new_node), 201

# Update node
@app.route('/api/nodes/<node_id>', methods=['PUT'])
def update_node(node_id):
    data = load_data()
    if node_id not in data["nodes"]:
        return jsonify({"error": "Node not found"}), 404

    node = data["nodes"][node_id]
    body = request.json

    for field in ["content", "note", "completed", "starred", "collapsed", "color"]:
        if field in body:
            node[field] = body[field]

    if "content" in body:
        node["tags"] = extract_tags(body["content"])

    node["updated_at"] = time.time()

    # Handle starring
    if "starred" in body:
        starred = data.get("starred_nodes", [])
        if body["starred"] and node_id not in starred:
            starred.append(node_id)
        elif not body["starred"] and node_id in starred:
            starred.remove(node_id)
        data["starred_nodes"] = starred

    save_data(data)
    return jsonify(node)

# Delete node (recursive)
@app.route('/api/nodes/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    data = load_data()
    if node_id not in data["nodes"] or node_id == "root":
        return jsonify({"error": "Cannot delete"}), 400

    def collect_ids(nid):
        ids = [nid]
        for child in data["nodes"].get(nid, {}).get("children", []):
            ids.extend(collect_ids(child))
        return ids

    ids_to_delete = collect_ids(node_id)
    parent_id = data["nodes"][node_id].get("parent")

    # Remove from parent
    if parent_id and parent_id in data["nodes"]:
        data["nodes"][parent_id]["children"] = [
            c for c in data["nodes"][parent_id]["children"] if c != node_id
        ]

    # Delete all descendants
    for nid in ids_to_delete:
        data["nodes"].pop(nid, None)
        if nid in data.get("starred_nodes", []):
            data["starred_nodes"].remove(nid)

    save_data(data)
    return jsonify({"deleted": ids_to_delete})

# Move node (indent/outdent/reorder)
@app.route('/api/nodes/<node_id>/move', methods=['PUT'])
def move_node(node_id):
    data = load_data()
    if node_id not in data["nodes"] or node_id == "root":
        return jsonify({"error": "Cannot move"}), 400

    body = request.json
    action = body.get("action")  # indent, outdent, up, down
    node = data["nodes"][node_id]
    current_parent_id = node["parent"]

    if action == "indent":
        # Make child of previous sibling
        siblings = data["nodes"][current_parent_id]["children"]
        idx = siblings.index(node_id)
        if idx == 0:
            return jsonify({"error": "No previous sibling"}), 400
        new_parent_id = siblings[idx - 1]
        siblings.remove(node_id)
        data["nodes"][new_parent_id]["children"].append(node_id)
        node["parent"] = new_parent_id

    elif action == "outdent":
        if not current_parent_id or current_parent_id == "root":
            return jsonify({"error": "Already at root"}), 400
        grandparent_id = data["nodes"][current_parent_id]["parent"]
        if not grandparent_id:
            return jsonify({"error": "No grandparent"}), 400

        # Remove from current parent
        data["nodes"][current_parent_id]["children"].remove(node_id)
        # Insert after current parent in grandparent
        gp_children = data["nodes"][grandparent_id]["children"]
        parent_idx = gp_children.index(current_parent_id)
        gp_children.insert(parent_idx + 1, node_id)
        node["parent"] = grandparent_id

    elif action == "up":
        siblings = data["nodes"][current_parent_id]["children"]
        idx = siblings.index(node_id)
        if idx > 0:
            siblings[idx], siblings[idx - 1] = siblings[idx - 1], siblings[idx]

    elif action == "down":
        siblings = data["nodes"][current_parent_id]["children"]
        idx = siblings.index(node_id)
        if idx < len(siblings) - 1:
            siblings[idx], siblings[idx + 1] = siblings[idx + 1], siblings[idx]

    node["updated_at"] = time.time()
    save_data(data)
    return jsonify(data["nodes"][node_id])

# Search
@app.route('/api/search', methods=['GET'])
def search():
    data = load_data()
    query = request.args.get('q', '').lower().strip()
    if not query:
        return jsonify([])

    results = []
    for node in data["nodes"].values():
        if node["id"] == "root":
            continue
        text = (node["content"] + " " + node.get("note", "")).lower()
        if query in text:
            # Build breadcrumb path
            path = []
            pid = node.get("parent")
            while pid and pid in data["nodes"]:
                path.insert(0, data["nodes"][pid]["content"])
                pid = data["nodes"][pid].get("parent")
            results.append({**node, "path": path})

    return jsonify(results[:50])

# Get all unique tags
@app.route('/api/tags', methods=['GET'])
def get_tags():
    data = load_data()
    tags = set()
    for node in data["nodes"].values():
        tags.update(node.get("tags", []))
    return jsonify(sorted(list(tags)))

# Settings
@app.route('/api/settings', methods=['GET', 'PUT'])
def settings():
    data = load_data()
    if request.method == 'PUT':
        data["settings"].update(request.json)
        save_data(data)
    return jsonify(data.get("settings", {}))

# ─── BULK IMPORT/EXPORT ────────────────────────────────────────────────────────

@app.route('/api/export', methods=['GET'])
def export_tree():
    data = load_data()
    nodes = data["nodes"]
    node_id = request.args.get('node_id', 'root')
    
    def format_node(nid, level=0):
        node = nodes.get(nid)
        if not node:
            return ""
            
        if nid == "root":
            lines = []
            children = node.get("children", [])
            for i, child_id in enumerate(children):
                lines.append(format_node(child_id, 0))
                if i < len(children) - 1:
                    lines.append("---")
            return "\n".join(lines)
        
        indent = "  " * level
        line = f"{indent}{node['content']}"
        if node.get("note"):
            line += f"\n{indent}  [note]: {node['note']}"
        
        child_lines = [format_node(cid, level + 1) for cid in node.get("children", [])]
        if child_lines:
            return line + "\n" + "\n".join(filter(None, child_lines))
        return line

    export_node = nodes.get(node_id)
    if not export_node:
        return jsonify({"error": "Node not found"}), 404
        
    content = format_node(node_id, 0)
    filename = f"mindtree_export_{node_id}.txt" if node_id != 'root' else "mindtree_export.txt"
    return content, 200, {'Content-Type': 'text/plain', 'Content-Disposition': f'attachment; filename={filename}'}

@app.route('/api/import', methods=['POST'])
def import_tree():
    print(f"DEBUG: Import triggered. Query args: {request.args}")
    data = load_data()
    parent_id = request.args.get('parent_id', 'root')
    print(f"DEBUG: Looking for parent_id: {parent_id} in {list(data['nodes'].keys())[:5]}... (total {len(data['nodes'])})")
    if parent_id not in data["nodes"]:
        print(f"DEBUG: Parent {parent_id} NOT FOUND. Returning 404.")
        return jsonify({"error": "Parent not found"}), 404
        
    text = request.data.decode('utf-8')
    lines = text.split('\n')
    
    stack = [(parent_id, -1)]  # (id, indent_level)
    imported_count = 0
    
    for line in lines:
        if not line.strip():
            continue
            
        stripped = line.strip()
        if stripped in ["---", "...", "***", "==="] or (len(stripped) >= 3 and all(c == stripped[0] for c in stripped) and stripped[0] in "-.*="):
            stack = [(parent_id, -1)]
            continue
            
        indent = len(line) - len(line.lstrip())
        is_note = False
        if stripped.startswith("[note]:"):
            is_note = True
            stripped = stripped[len("[note]:"):].strip()
        
        while len(stack) > 1 and stack[-1][1] >= indent:
            stack.pop()
            
        current_parent_id = stack[-1][0]
        
        if is_note:
            if current_parent_id in data["nodes"] and current_parent_id != parent_id:
                data["nodes"][current_parent_id]["note"] = stripped
            continue

        node_id = "node-" + str(uuid.uuid4())[:8]
        new_node = {
            "id": node_id,
            "content": stripped,
            "note": "",
            "children": [],
            "parent": current_parent_id,
            "completed": False,
            "starred": False,
            "collapsed": False,
            "created_at": time.time(),
            "updated_at": time.time(),
            "tags": extract_tags(stripped),
            "color": None
        }
        
        data["nodes"][node_id] = new_node
        if current_parent_id in data["nodes"]:
            data["nodes"][current_parent_id]["children"].append(node_id)
            
        stack.append((node_id, indent))
        imported_count += 1
        
    save_data(data)
    return jsonify({"status": "success", "count": imported_count})

if __name__ == '__main__':
    print("🌳 MindTree API starting on http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
