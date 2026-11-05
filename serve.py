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
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    # Requêtes par plage (« Range: bytes=a-b ») : sans elles, le navigateur ne peut pas se
    # placer au milieu d'une vidéo (aperçu des films à l'instant du poster), comme sur GitHub Pages.
    def send_head(self):
        plage = self.headers.get("Range", "")
        chemin = self.translate_path(self.path)
        if not plage.startswith("bytes=") or not os.path.isfile(chemin):
            return super().send_head()
        taille = os.path.getsize(chemin)
        a, _, b = plage[6:].split(",")[0].strip().partition("-")
        if a:                                   # « a-b » ou « a- »
            debut, fin = int(a), min(int(b), taille - 1) if b else taille - 1
        else:                                   # « -n » : les n derniers octets
            debut, fin = max(0, taille - int(b)), taille - 1
        if debut >= taille:
            self.send_error(416)
            return None
        f = open(chemin, "rb")
        f.seek(debut)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(chemin))
        self.send_header("Content-Range", f"bytes {debut}-{fin}/{taille}")
        self.send_header("Content-Length", str(fin - debut + 1))
        self.end_headers()
        self._reste = fin - debut + 1
        return f

    def copyfile(self, source, destination):
        reste = getattr(self, "_reste", None)
        if reste is None:
            return super().copyfile(source, destination)
        self._reste = None
        while reste > 0:
            bloc = source.read(min(65536, reste))
            if not bloc:
                break
            destination.write(bloc)
            reste -= len(bloc)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), functools.partial(Handler, directory=RACINE)) as httpd:
    print(f"Sky Perspective — http://localhost:{PORT}", flush=True)
    httpd.serve_forever()
