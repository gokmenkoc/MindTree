# 🌳 MindTree (Zoomy) — Architecture & Setup Guide

## What is MindTree?
A fully self-hosted, infinitely nested outliner — inspired by WorkFlowy — that runs locally on your machine. No cloud, no subscription, no data leaving your computer.

<img width="917" height="705" alt="image" src="https://github.com/user-attachments/assets/ac3dcadf-6ccf-47d3-b3cc-2c0eccfa3b91" />

---

## Architecture

```
mindtree/
├── backend/
│   ├── app.py          ← Flask REST API (Python)
│   └── data.json       ← Auto-created on first run (your data)
├── frontend/
│   └── index.html      ← Complete single-file app (HTML/CSS/JS)
├── start.py            ← One-command launcher
└── README.md           ← This file
```

### Stack
| Layer     | Technology          | Why                                      |
|-----------|---------------------|------------------------------------------|
| Backend   | Python + Flask      | Zero-config, runs everywhere             |
| Storage   | JSON file           | No database to install or maintain       |
| Frontend  | Vanilla HTML/CSS/JS | Fast, no build step, works offline       |
| Fonts     | Google Fonts CDN    | Syne + DM Sans + DM Mono                 |

### API Endpoints
| Method | Endpoint                   | Description                  |
|--------|----------------------------|------------------------------|
| GET    | /api/nodes                 | Fetch all nodes              |
| GET    | /api/nodes/:id             | Fetch single node            |
| POST   | /api/nodes                 | Create node                  |
| PUT    | /api/nodes/:id             | Update node content/state    |
| DELETE | /api/nodes/:id             | Delete node + descendants    |
| PUT    | /api/nodes/:id/move        | Move (indent/outdent/up/down)|
| GET    | /api/search?q=             | Full-text search             |
| GET    | /api/tags                  | All unique tags              |
| GET    | /api/settings              | Get settings                 |
| PUT    | /api/settings              | Update settings              |

### Data Model
```json
{
  "id":         "node-abc123",
  "content":    "My item text #tag @mention",
  "note":       "Optional note/annotation",
  "children":   ["node-xyz", "node-def"],
  "parent":     "root",
  "completed":  false,
  "starred":    false,
  "collapsed":  false,
  "tags":       ["#tag", "@mention"],
  "created_at": 1704067200.0,
  "updated_at": 1704067200.0
}
```

---

## Setup & Running

### Requirements
- Python 3.8+ (already installed on most systems)
- pip

### Install
```bash
pip install flask flask-cors
```

### Run
```bash
python start.py
```
This starts the API on port 5000 and opens the frontend in your browser.

**Or run separately:**
```bash
# Terminal 1 - API
cd backend && python app.py

# Then open in browser
open frontend/index.html        # macOS
xdg-open frontend/index.html   # Linux
start frontend/index.html       # Windows
```

---

## Keyboard Shortcuts
| Key             | Action                        |
|-----------------|-------------------------------|
| Enter           | Create new item below         |
| Tab             | Indent (nest deeper)          |
| Shift+Tab       | Outdent (move up a level)     |
| Alt+↑ / Alt+↓   | Move item up/down             |
| Ctrl+Enter      | Toggle complete               |
| Ctrl+K          | Command palette               |
| Ctrl+F          | Focus search                  |
| Backspace       | Delete empty item             |
| Esc             | Zoom out / close overlay      |
| ?               | Show keyboard help            |
| Click bullet    | Zoom into node                |

---

## Features
- ✅ Infinite nested outlining
- ✅ Zoom / hoist into any node
- ✅ Breadcrumb navigation
- ✅ #tag and @mention tagging
- ✅ Full-text search with highlighting
- ✅ Star any item (pinned sidebar + panel)
- ✅ Collapse/expand branches
- ✅ Complete/uncomplete items
- ✅ Right-click context menu
- ✅ Command palette (Ctrl+K)
- ✅ Drag-free keyboard move (Alt+arrows)
- ✅ Offline fallback with localStorage cache
- ✅ Auto-save (600ms debounce)
- ✅ Status bar (item count, done, starred)
- ✅ Tag browser panel
- ✅ Dark theme with Syne + DM Sans fonts

---

## Extending MindTree

### Add a new API endpoint
Edit `backend/app.py`. All data goes through `load_data()` / `save_data()`.

### Add a new view
Add a `<div id="my-panel">` in `index.html`, register it in `setView()`.

### Change the color theme
Edit the CSS variables in `:root {}` at the top of `index.html`.

### Add real database
Replace `load_data()` / `save_data()` with SQLite via `flask_sqlalchemy`.

---

## Data Backup
Your data lives in `backend/data.json`. Back it up by copying this file. It's plain JSON — readable and editable in any text editor.

---

*Built with Python Flask + Vanilla JS — no frameworks, no build step, no cloud.*
