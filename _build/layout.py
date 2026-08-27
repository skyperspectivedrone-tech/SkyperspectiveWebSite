# -*- coding: utf-8 -*-
"""Gabarit commun — équivalent d'un Layout.astro. Un seul endroit à modifier.
Design importé depuis Claude Design (Sky Perspective Design System) : navy / rouge /
aurore / altitude, Outfit + Manrope + JetBrains Mono."""

SITE = {
    "nom": "Sky Perspective",
    "email": "skyperspectivedrone@gmail.com",
    "tel": "06 47 00 65 41",
    "tel_lien": "+33647006541",
    "ville": "Montpellier (34)",
    "siret": "10863047600019",
    "annee": 2026,
    "url": "https://skyperspective.fr",
}

NAV = [
    ("Accueil", "index.html"),
    ("Prestations", "prestations.html"),
    ("Tarifs", "tarifs.html"),
    ("Matériel", "materiel.html"),
    ("Contact", "contact.html"),
]


def brand(tag="a", href="index.html", chemin="assets/img/logo-blanc.png"):
    attrs = f' href="{href}"' if tag == "a" else ""
    return (f'<{tag} class="brand"{attrs} aria-label="Sky Perspective — accueil">'
            f'<img class="brand__img" src="{chemin}" width="1600" height="281" '
            f'alt="Sky Perspective">'
            f"</{tag}>")


def header(courante):
    liens = "".join(
        f'<a class="nav__link" href="{url}"'
        + (' aria-current="page"' if url == courante else "")
        + f">{libelle}</a>"
        for libelle, url in NAV
    )
    return f"""<header class="site-header" id="site-header">
    {brand()}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-principale">
      <span></span><span class="sr-only">Ouvrir le menu</span>
    </button>
    <nav class="nav" id="nav-principale" aria-label="Navigation principale">
      {liens}
    </nav>
  </header>"""


ICONES = {
    "mail": '<path d="M2 4h16v12H2z" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M2 5l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.4"/>',
    "pin": '<path d="M10 18s6-6.3 6-10a6 6 0 1 0-12 0c0 3.7 6 10 6 10z" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="10" cy="8" r="2.2" fill="none" stroke="currentColor" stroke-width="1.4"/>',
    "tel": '<path d="M4.6 3.4h3.2l1.6 4-2 1.2a10.6 10.6 0 0 0 4 4l1.2-2 4 1.6v3.2c0 .8-.7 1.5-1.5 1.4C7.9 16.2 3.8 12.1 3.2 4.9c-.1-.8.6-1.5 1.4-1.5z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
    "clock": '<circle cx="10" cy="10" r="7.4" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10 5.6V10l3 1.8" fill="none" stroke="currentColor" stroke-width="1.4"/>',
    "arrow-right": '<path d="M4 10h12M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "check": '<path d="M4 10.5 8 14l8-8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "building": '<rect x="4" y="2.5" width="9" height="15" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M13 8h3v9.5H4" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6.5 5.5h1.2M9.5 5.5h1.2M6.5 8.5h1.2M9.5 8.5h1.2M6.5 11.5h1.2M9.5 11.5h1.2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>',
    "utensils": '<path d="M4 3v4M6 3v4M8 3v4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M6 7v10.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M14 3c-2 0-3 2-3 4.5S12 11 14 11" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M14 3v14.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
    "running": '<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="M14.007 5a2 2 0 1 0 4 0a2 2 0 0 0-4 0"/><path d="M7 17l5 1l.75-1.5M18 21v-4l-4-3l1-6"/><path d="M10 12V9l5-1l3 3l3 1M10 5H6m0 5H2"/></g>',
    "box": '<path d="M10 2.5 17.5 6.5 10 10.5 2.5 6.5z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M2.5 6.5v7l7.5 4 7.5-4v-7M10 10.5v7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
    "crane": '<path fill="currentColor" d="M240 80H108.94L87.16 36.42A8 8 0 0 0 80 32H48a8 8 0 0 0-8 8v40H24a8 8 0 0 0 0 16h16v112H24a8 8 0 0 0 0 16h104a8 8 0 0 0 0-16h-16V96h96v88h-16v-8a8 8 0 0 0-16 0v8a16 16 0 0 0 16 16h16a16 16 0 0 0 16-16V96h16a8 8 0 0 0 0-16M56 48h19.06l16 32H56Zm0 160v-48h40v48Zm40-64H56V96h40Z"/>',
    "mountain": '<path d="M2 16 7.5 6l3 5.2L12.5 8 18 16z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><circle cx="14.5" cy="5" r="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/>',
    "shield": '<path d="M10 2.2 17 5.3v5.4c0 4.3-3 7.1-7 7.9-4-.8-7-3.6-7-7.9V5.3z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
    "shield-check": '<path d="M10 2.2 17 5.3v5.4c0 4.3-3 7.1-7 7.9-4-.8-7-3.6-7-7.9V5.3z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M6.8 10 9.2 12.4 13.4 8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "spark": '<path d="M11 2 9.5 8 4 9.5l5.5 1.5L11 17l1.5-6L18 9.5 12.5 8z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
    "compass": '<circle cx="10" cy="10" r="7.6" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12.6 7.4 11 11l-3.6 1.6L9 9z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
}


ICONES_VIEWBOX = {"crane": "0 0 256 256", "running": "0 0 24 24"}


def icone(nom, classe=""):
    cls = f' class="{classe}"' if classe else ""
    vb = ICONES_VIEWBOX.get(nom, "0 0 20 20")
    # width/height explicites : sans eux un <svg> sans dimension CSS retombe sur la
    # taille par défaut du navigateur (300×150) au lieu de suivre son contexte.
    return f'<svg{cls} width="20" height="20" viewBox="{vb}" aria-hidden="true">{ICONES[nom]}</svg>'


def footer():
    return f"""<footer class="site-footer">
    <div class="container">
      <ul class="site-footer__band">
        <li>{icone('mail')}<a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        <li>{icone('tel')}<a href="tel:{SITE['tel_lien']}">{SITE['tel']}</a></li>
        <li>{icone('pin')}<span>Basé à {SITE['ville']} — interventions partout en France</span></li>
        <li>{icone('clock')}<span>Réponse sous 24 h</span></li>
      </ul>
      <div class="site-footer__legal">
        <span>© {SITE['annee']} {SITE['nom']} — SIRET {SITE['siret']}</span>
        <nav>
          <a href="mentions-legales.html">Mentions légales</a>
          <a href="confidentialite.html">Confidentialité</a>
        </nav>
      </div>
    </div>
  </footer>"""


SCRIPT_NAV = """<script>
    (function () {
      var bouton = document.querySelector('.nav-toggle');
      var menu = document.getElementById('nav-principale');
      if (!bouton || !menu) return;
      bouton.addEventListener('click', function () {
        var ouvert = bouton.getAttribute('aria-expanded') === 'true';
        bouton.setAttribute('aria-expanded', String(!ouvert));
        menu.classList.toggle('is-open', !ouvert);
      });
    })();
  </script>"""


def _canonique(courante):
    chemin = "" if courante == "index.html" else courante
    return f"{SITE['url']}/{chemin}"


def _jsonld():
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": SITE["nom"],
        "image": f"{SITE['url']}/assets/img/og-image.jpg",
        "url": SITE["url"],
        "telephone": SITE["tel_lien"],
        "email": SITE["email"],
        "description": "Télépilote de drone professionnel à Montpellier : vidéo aérienne "
                        "stabilisée et FPV pour l’immobilier, les commerces, le sport "
                        "mécanique, le suivi de chantier et le tourisme.",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Montpellier",
            "addressRegion": "Occitanie",
            "addressCountry": "FR",
        },
        "areaServed": "France",
        "priceRange": "€€",
    }, ensure_ascii=False)


def page(titre, description, courante, contenu, scripts=""):
    titre_complet = f"{titre} — {SITE['nom']}"
    canonique = _canonique(courante)
    og_image = f"{SITE['url']}/assets/img/og-image.jpg"
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titre_complet}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonique}">
  <link rel="icon" type="image/svg+xml" href="assets/img/logo-icone.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE['nom']}">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="{titre_complet}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonique}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{titre_complet}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500;600&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <script type="application/ld+json">{_jsonld()}</script>
</head>
<body>
  {header(courante)}
  <main id="contenu">
{contenu}
  </main>
  {footer()}
  {SCRIPT_NAV}
  <script src="assets/js/ux.js" defer></script>
  {scripts}
</body>
</html>
"""
