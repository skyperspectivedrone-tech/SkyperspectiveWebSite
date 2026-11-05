# -*- coding: utf-8 -*-
"""Page Réalisations — les tournages réellement effectués par Sky Perspective.

Règle de publication : un projet n'apparaît que si sa photo de couverture existe dans
site/. Tant qu'aucun projet n'est publiable, la page n'est pas générée et le lien
« Réalisations » n'entre pas dans la navigation (aucun lien mort, aucune page vide).

Ajouter un projet :
  1. Accord écrit du client pour diffuser les images.
  2. Couverture et photos compressées dans site/assets/img/realisations/<id>/ :
         sips -s format jpeg -s formatOptions 76 -Z 1600 <source> \\
              --out site/assets/img/realisations/<id>/couverture.jpg
  3. Vidéo sur YouTube en « non répertoriée », identifiant (après « v= ») dans « youtube ».
     Le lecteur ne se charge qu'au clic : aucun appel à YouTube avant.
"""
import pathlib
from layout import icone

SITE_DIR = pathlib.Path(__file__).resolve().parent.parent / "site"

# Libellés « prestation » identiques à ceux des pages Prestations et Tarifs.
PROJETS = [
    {"id": "restaurant", "prestation": "Commerces &amp; restaurants", "ancre": "p-commerces",
     "titre": "Restaurant",            # À compléter : nom du lieu, si le client l'accepte
     "lieu": "",                        # ex. « Montpellier (34) »
     "date": "",                        # ex. « Octobre 2026 »
     "drones": "Stabilisé / FPV",
     "texte": "Une vidéo pour donner envie de pousser la porte : la façade et la terrasse vues "
              "du ciel, puis un parcours en intérieur à travers la salle.",
     "livrables": ["Vidéo de présentation 16:9", "Version verticale pour les réseaux",
                   "Photos aériennes"],
     "couverture": "assets/img/realisations/restaurant/couverture.jpg",
     "youtube": "",
     "photos": []},
    {"id": "maison", "prestation": "Immobilier &amp; propriété", "ancre": "p-immobilier",
     "titre": "Maison individuelle",
     "lieu": "",
     "date": "",
     "drones": "Stabilisé",
     "texte": "Le bien replacé dans son environnement : volumes, jardin, exposition et accès, "
              "pour une annonce qui se distingue dès la première image.",
     "livrables": ["Vidéo de présentation", "Photos aériennes HD"],
     "couverture": "assets/img/realisations/maison/couverture.jpg",
     "youtube": "",
     "photos": []},
    {"id": "drift", "prestation": "Sport &amp; suivi de véhicule", "ancre": "p-sport",
     "titre": "Session de drift",
     "lieu": "",
     "date": "",
     "drones": "FPV",
     "texte": "Le drone colle à la voiture dans chaque glissade : un suivi au ras du sol, au "
              "milieu de la fumée, pour faire ressentir la vitesse.",
     "livrables": ["Clip dynamique", "Édit court pour les réseaux"],
     "couverture": "assets/img/realisations/drift/couverture.jpg",
     "youtube": "",
     "photos": []},
]


def _existe(chemin):
    return (SITE_DIR / chemin).is_file()


def projets_publies():
    return [p for p in PROJETS if _existe(p["couverture"])]


def a_des_videos():
    return any(p["youtube"] for p in projets_publies())


def _media(p):
    alt = f"{p['titre']} — tournage drone Sky Perspective"
    image = (f'<img src="{p["couverture"]}" alt="{alt}" width="1600" height="900" '
             'loading="lazy" decoding="async">')
    if not p["youtube"]:
        return f'<div class="media-frame media-frame--16-9 realisation__media">{image}</div>'
    return f"""<div class="media-frame media-frame--16-9 realisation__media">
            <button type="button" class="lecteur" data-youtube="{p['youtube']}"
                    aria-label="Lire la vidéo : {p['titre']}">
              {image}
              <span class="lecteur__bouton" aria-hidden="true"><svg viewBox="0 0 20 20" width="20" height="20"><path d="M6 4l10 6-10 6z" fill="currentColor"/></svg></span>
            </button>
          </div>"""


def _photos(p):
    if not p["photos"]:
        return ""
    vignettes = "".join(
        f'<a class="realisation__photo" href="{src}" target="_blank" rel="noopener">'
        f'<img src="{src}" alt="{p["titre"]} — photo {i + 1}" loading="lazy" decoding="async"></a>'
        for i, src in enumerate(p["photos"]) if _existe(src))
    return f'<div class="realisation__photos">{vignettes}</div>' if vignettes else ""


def _projet(p, i):
    meta = " · ".join(x for x in (p["lieu"], p["date"]) if x)
    meta_html = f'<p class="label-mono realisation__meta">{meta}</p>' if meta else ""
    livrables = "".join(f'<li>{icone("check")}{item}</li>' for item in p["livrables"])
    classe = "realisation realisation--inverse" if i % 2 else "realisation"
    return f"""<article class="{classe}" id="r-{p['id']}">
        <div class="reveal-in">{_media(p)}{_photos(p)}</div>
        <div class="realisation__texte reveal-in reveal-in--d1">
          <span class="label-mono realisation__num">{i + 1:02d} — {p['prestation']}</span>
          <h2 class="realisation__titre">{p['titre']}</h2>
          {meta_html}
          <p class="realisation__desc">{p['texte']}</p>
          <div class="detail-grid__badges"><span class="badge badge--neutral">{p['drones']}</span></div>
          <ul class="detail-grid__included">{livrables}</ul>
          <div class="detail-grid__actions">
            <a class="btn btn--primary" href="tarifs.html#devis">Un projet similaire ?{icone('arrow-right','btn__arrow')}</a>
            <a class="btn btn--ghost" href="prestations.html#{p['ancre']}">Voir la prestation</a>
          </div>
        </div>
      </article>"""


def contenu():
    projets = "".join(_projet(p, i) for i, p in enumerate(projets_publies()))
    return f"""    <section class="section" style="padding-top:var(--sp-8)">
      <div class="container">
        <div class="reveal-in">
          <p class="eyebrow">Réalisations</p>
          <h1 class="page-hero__title">Mes derniers<br>tournages</h1>
          <p class="page-hero__lead">Des projets réels, filmés et montés par Sky Perspective.
            Chaque client a donné son accord pour que ses images soient présentées ici.</p>
        </div>
        <div class="realisations">{projets}</div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="card card--navy reveal-in cta-band" style="padding:clamp(32px,5vw,72px)">
          <div>
            <h2 class="cta-band__title">Le prochain, c’est le vôtre ?</h2>
            <p class="cta-band__text">Estimez votre budget en quelques clics, ou décrivez-moi
              votre projet — réponse sous 24 h.</p>
          </div>
          <div class="cta-band__actions">
            <a class="btn btn--primary btn--lg" href="tarifs.html#devis">Estimer mon projet
              <span class="btn__arrow">{icone('arrow-right')}</span></a>
            <a class="btn btn--ghost btn--lg" href="contact.html">Me contacter</a>
          </div>
        </div>
      </div>
    </section>"""
