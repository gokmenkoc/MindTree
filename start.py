#!/usr/bin/env python3
"""
MindTree Startup Script
Launches the Flask API and opens the frontend in a browser.
"""
import subprocess
import sys
import os
import time
import threading
import webbrowser

def start_api():
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    subprocess.run([sys.executable, 'app.py'], cwd=backend_dir)

def open_browser():
    time.sleep(1.5)
    url = 'http://127.0.0.1:5000'
    webbrowser.open(url)
    print(f"\n✅ Opened: {url}")
    print("📡 API:    http://127.0.0.1:5000/api/health")
    print("\nPress Ctrl+C to stop.\n")

if __name__ == '__main__':
    print("🌳 MindTree starting...")
    threading.Thread(target=open_browser, daemon=True).start()
    start_api()
