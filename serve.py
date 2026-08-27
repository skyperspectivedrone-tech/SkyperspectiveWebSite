# -*- coding: utf-8 -*-
"""Petit serveur statique local pour prévisualiser site/."""
import functools, http.server, socketserver, os

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
PORT = 4321


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".html": "text/html; charset=utf-8",
                      ".svg": "image/svg+xml"}

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), functools.partial(Handler, directory=RACINE)) as httpd:
    print(f"Sky Perspective — http://localhost:{PORT}", flush=True)
    httpd.serve_forever()
