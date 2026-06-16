#!/usr/bin/env python3
"""serve.py — tiny static server for the anima ARCHITECTURE tree viewer.

The architecture SSOT is ARCHITECTURE.json (parsed by AI/tools); humans read it
through ARCHITECTURE.html. Browsers block `fetch()` over file://, so the viewer
must be served over http. This standard-library server (http.server + webbrowser)
serves the repo root and auto-opens ARCHITECTURE.html (c4 standard).

    python3 serve.py            # serve on 127.0.0.1:8000, open ARCHITECTURE.html
    python3 serve.py 9000       # pick a port
    python3 serve.py --no-open  # don't auto-open the browser

Ctrl-C to stop.
"""
import http.server
import os
import socket
import socketserver
import sys
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = "ARCHITECTURE.html"
DEFAULT_PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # never cache — the JSON SSOT is edited in place
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("  " + (fmt % args) + "\n")


def pick_port(requested):
    """Return `requested` if free, else the next free port (up to +20)."""
    for port in range(requested, requested + 21):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return requested


def main(argv):
    port = DEFAULT_PORT
    do_open = True
    for arg in argv:
        if arg in ("--no-open", "-n"):
            do_open = False
        elif arg.isdigit():
            port = int(arg)
        elif arg in ("-h", "--help"):
            print(__doc__)
            return 0

    if not os.path.exists(os.path.join(ROOT, PAGE)):
        sys.stderr.write("error: %s not found next to serve.py\n" % PAGE)
        return 1

    port = pick_port(port)
    url = "http://127.0.0.1:%d/%s" % (port, PAGE)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        print("anima architecture viewer — serving %s" % ROOT)
        print("  %s" % url)
        print("  (SSOT = ARCHITECTURE.json · Ctrl-C to stop)")
        if do_open:
            threading.Timer(0.4, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
