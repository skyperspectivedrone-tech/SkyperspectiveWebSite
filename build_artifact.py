# -*- coding: utf-8 -*-
"""Assemble les 5 pages en un fichier unique et autonome, navigable côté client.
Sert de maquette consultable et commentable dans Claude."""
import sys, pathlib, re, base64, json
sys.path.insert(0, "_build")
import layout
import p_prestations, p_autres, p_legal, p_materiel, p_tarifs

CSS = pathlib.Path("site/assets/css/style.css").read_text(encoding="utf-8")

REVEAL_JS = pathlib.Path("site/assets/js/reveal.js").read_text(encoding="utf-8")
DEVIS_JS = pathlib.Path("site/assets/js/devis.js").read_text(encoding="utf-8")


def sequence_json(nom, total, taille="900"):
    """Séquence d'images embarquée en data URI (l'artifact doit être autonome)."""
    uris = []
    for i in range(1, total + 1):
        octets = pathlib.Path(f"site/assets/media/{nom}/{taille}/{i:04d}.jpg").read_bytes()
        uris.append("data:image/jpeg;base64," + base64.b64encode(octets).decode("ascii"))
    return json.dumps(uris, separators=(",", ":"))


AIR3S_IMG = ("data:image/png;base64,"
             + base64.b64encode(pathlib.Path("site/assets/img/air3s.png").read_bytes()).decode("ascii"))
AVATA_IMG = ("data:image/webp;base64,"
             + base64.b64encode(pathlib.Path("site/assets/img/avata2.webp").read_bytes()).decode("ascii"))

_hero = pathlib.Path("site/assets/img/hero-alpes.jpg").read_bytes()
HERO_IMG = "data:image/jpeg;base64," + base64.b64encode(_hero).decode("ascii")

_contact = pathlib.Path("site/assets/media/air3s/1280/0058.jpg").read_bytes()
CONTACT_IMG = "data:image/jpeg;base64," + base64.b64encode(_contact).decode("ascii")

_logo = pathlib.Path("site/assets/img/logo-blanc.png").read_bytes()
LOGO_DATA_URI = "data:image/png;base64," + base64.b64encode(_logo).decode("ascii")

PAGES = [
    ("accueil",     "Accueil",     p_autres.accueil),
    ("prestations", "Prestations", p_prestations.contenu),
    ("tarifs",      "Tarifs",      p_tarifs.contenu),
    ("materiel",    "Matériel",    p_materiel.contenu),
    ("contact",     "Contact",     p_autres.contact),
]

ANNEXES = [
    ("mentions-legales", p_legal.mentions_legales),
    ("confidentialite",  p_legal.confidentialite),
]

FICHIER_VERS_ANCRE = {
    "index.html": "#accueil",
    "prestations.html": "#prestations",
    "tarifs.html": "#tarifs",
    "tarifs.html#devis": "#tarifs",
    "materiel.html": "#materiel",
    "contact.html": "#contact",
    "mentions-legales.html": "#mentions-legales",
    "confidentialite.html": "#confidentialite",
}


def interne(html):
    """Liens de fichiers en ancres, et logo embarqué : le fichier doit rester autonome."""
    html = html.replace('src="assets/img/logo-blanc.png"', f'src="{LOGO_DATA_URI}"')
    html = html.replace('src="assets/media/air3s/1280/0058.jpg"', f'src="{CONTACT_IMG}"')
    html = html.replace('src="assets/img/hero-alpes.jpg"', f'src="{HERO_IMG}"')
    html = html.replace('src="assets/img/air3s.png"', f'src="{AIR3S_IMG}"')
    html = html.replace('src="assets/img/avata2.webp"', f'src="{AVATA_IMG}"')
    for fichier, ancre in sorted(FICHIER_VERS_ANCRE.items(), key=lambda kv: -len(kv[0])):
        html = html.replace(f'href="{fichier}"', f'href="{ancre}"')
    return html


def nav():
    liens = "".join(
        f'<a class="nav__link" href="#{cle}" data-page="{cle}">{libelle}</a>'
        for cle, libelle, _ in PAGES
    )
    return f"""<header class="site-header">
  <div class="container site-header__inner">
    {interne(layout.brand(href="#accueil"))}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-principale">
      <span></span><span class="sr-only">Ouvrir le menu</span>
    </button>
    <nav class="nav" id="nav-principale" aria-label="Navigation principale">
      {liens}
    </nav>
  </div>
</header>"""


def main():
    sections = "\n".join(
        f'<div class="page" id="{cle}" data-page="{cle}" hidden>\n{interne(rendu())}\n</div>'
        for cle, _, rendu in PAGES
    ) + "\n" + "\n".join(
        f'<div class="page" id="{cle}" data-page="{cle}" hidden>\n{interne(rendu())}\n</div>'
        for cle, rendu in ANNEXES
    )
    footer = interne(layout.footer())

    sequences = "\n".join(
        f'<script type="application/json" id="seq-{seq["id"]}">'
        f'{sequence_json(seq["id"], seq["images"])}</script>'
        for seq in p_materiel.SEQUENCES
    )

    html = f"""<title>Sky Perspective</title>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
{CSS}
.page[hidden] {{ display: none; }}
</style>

{layout.fond_anime(False)}
{nav()}
<main id="contenu">
{sections}
</main>
{footer}

{sequences}

<script>
{REVEAL_JS}
</script>

<script>
{DEVIS_JS}
</script>

<script>
(function () {{
  var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
  var liens = Array.prototype.slice.call(document.querySelectorAll('.nav__link'));
  var menu = document.getElementById('nav-principale');
  var bouton = document.querySelector('.nav-toggle');

  function afficher(cle, defiler) {{
    var trouvee = false;
    pages.forEach(function (page) {{
      var actif = page.dataset.page === cle;
      page.hidden = !actif;
      if (actif) trouvee = true;
    }});
    if (!trouvee) return afficher('accueil', defiler);
    liens.forEach(function (lien) {{
      if (lien.dataset.page === cle) lien.setAttribute('aria-current', 'page');
      else lien.removeAttribute('aria-current');
    }});
    document.title = 'Sky Perspective';
    if (defiler) window.scrollTo({{ top: 0, behavior: 'instant' }});
    window.dispatchEvent(new Event('resize'));
    window.dispatchEvent(new Event('scroll'));
    if (menu) menu.classList.remove('is-open');
    if (bouton) bouton.setAttribute('aria-expanded', 'false');
  }}

  function depuisHash(defiler) {{
    afficher((location.hash || '#accueil').slice(1), defiler);
  }}

  window.addEventListener('hashchange', function () {{ depuisHash(true); }});
  depuisHash(false);
  if ((location.hash || '#accueil') === '#accueil') {{
    var fond = document.querySelector('.fond');
    if (fond) fond.classList.add('fond--apparition');
  }}

  if (bouton && menu) {{
    bouton.addEventListener('click', function () {{
      var ouvert = bouton.getAttribute('aria-expanded') === 'true';
      bouton.setAttribute('aria-expanded', String(!ouvert));
      menu.classList.toggle('is-open', !ouvert);
    }});
  }}
}})();
</script>
"""
    sortie = pathlib.Path("maquette.html")
    sortie.write_text(html, encoding="utf-8")
    print(f"✓ {sortie} — {len(html) // 1024} Ko")


if __name__ == "__main__":
    main()
