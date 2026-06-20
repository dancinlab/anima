#!/usr/bin/env python3
"""serve.py — static server + browser auto-open for the architecture viewer.

The architecture SSOT is ARCHITECTURE.json; humans read it through
architecture.html. Browsers block fetch() over file://, so this serves the repo
root over http:// and opens the viewer.

    python3 serve.py            # serve on :8000, open architecture.html
    python3 serve.py 9000       # custom port
"""
import http.server
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
PAGE = "architecture.html"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def end_headers(self):
        # never cache the SSOT / viewer during local editing
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # quiet


def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        url = f"http://127.0.0.1:{PORT}/{PAGE}"
        print(f"[serve] architecture viewer → {url}")
        print(f"[serve] SSOT: ARCHITECTURE.json   (Ctrl-C to stop)")
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[serve] stopped")


if __name__ == "__main__":
    main()
