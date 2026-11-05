# -*- coding: utf-8 -*-
"""Génère site/*.html — équivalent du build Astro, sans dépendance."""
import sys, os, pathlib, datetime
sys.path.insert(0, "_build")
import layout
from layout import page, SITE
import p_prestations, p_autres, p_legal, p_materiel, p_tarifs, p_realisations

SORTIE = pathlib.Path("site")

PAGES = [
    ("index.html", "Pilote de drone cinématographique à Montpellier",
     "Sky Perspective, télépilote de drone à Montpellier : vidéo aérienne stabilisée et FPV "
     "pour l’immobilier, les commerces, le sport mécanique et le suivi de chantier.",
     p_autres.accueil),
    ("prestations.html", "Prestations drone",
     "Vidéo aérienne pour l’immobilier, les commerces, le sport mécanique, le suivi de chantier, "
     "les scans 3D et le tourisme. Prestations drone stabilisé et FPV partout en France.",
     p_prestations.contenu),
    ("realisations.html", "Réalisations",
     "Les tournages drone réalisés par Sky Perspective : restaurant, immobilier, drift. "
     "Vidéos et photos aériennes stabilisées et FPV.",
     p_realisations.contenu),
    ("tarifs.html", "Tarifs",
     "Tarifs de prestation drone : immobilier à partir de 450 €, commerces 590 €, "
     "sport mécanique 850 €, suivi de chantier 450 € par passage.",
     p_tarifs.contenu),
    ("materiel.html", "Matériel & savoir-faire",
     "DJI Air 3S double focale 24 et 70 mm, DJI Avata 2 FPV : le matériel et le cadre "
     "réglementaire des tournages Sky Perspective.",
     p_materiel.contenu),
    ("contact.html", "Contact",
     "Contactez Sky Perspective, télépilote de drone à Montpellier. Réponse sous 24 h.",
     p_autres.contact),
    ("mentions-legales.html", "Mentions légales",
     "Mentions légales de Sky Perspective, télépilote de drone à Montpellier.",
     p_legal.mentions_legales),
    ("confidentialite.html", "Confidentialité",
     "Politique de confidentialité et de protection des données de Sky Perspective.",
     p_legal.confidentialite),
]

def main():
    SORTIE.mkdir(exist_ok=True)
    # Pas de projet publiable → ni page, ni lien dans la navigation (aucun lien mort).
    if not p_realisations.projets_publies():
        PAGES[:] = [pg for pg in PAGES if pg[0] != "realisations.html"]
        layout.NAV[:] = [lien for lien in layout.NAV if lien[1] != "realisations.html"]
        (SORTIE / "realisations.html").unlink(missing_ok=True)
        print("  ⚠ Réalisations : aucune couverture trouvée, page non publiée")
    for fichier, titre, description, rendu in PAGES:
        scripts = ""
        if fichier == "materiel.html":
            scripts = '<script src="assets/js/reveal.js" defer></script>'
        elif fichier == "tarifs.html":
            scripts = '<script src="assets/js/devis.js" defer></script>'
        elif fichier == "realisations.html" and p_realisations.a_des_videos():
            scripts = '<script src="assets/js/realisations.js" defer></script>'
        elif fichier == "contact.html":
            scripts = '<script src="assets/js/contact.js" defer></script>'
        html = page(titre, description, fichier, rendu(), scripts)
        (SORTIE / fichier).write_text(html, encoding="utf-8")
        print(f"  ✓ site/{fichier}  ({len(html) // 1024} Ko)")

    ecrire_sitemap()
    ecrire_robots()


def ecrire_sitemap():
    aujourdhui = datetime.date.today().isoformat()
    urls = []
    for fichier, *_ in PAGES:
        chemin = "" if fichier == "index.html" else fichier
        priorite = "1.0" if fichier == "index.html" else "0.6"
        urls.append(f"""  <url>
    <loc>{SITE['url']}/{chemin}</loc>
    <lastmod>{aujourdhui}</lastmod>
    <priority>{priorite}</priority>
  </url>""")
    contenu = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    (SORTIE / "sitemap.xml").write_text(contenu, encoding="utf-8")
    print("  ✓ site/sitemap.xml")


def ecrire_robots():
    contenu = f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n"
    (SORTIE / "robots.txt").write_text(contenu, encoding="utf-8")
    print("  ✓ site/robots.txt")


if __name__ == "__main__":
    main()
