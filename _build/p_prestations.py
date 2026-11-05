# -*- coding: utf-8 -*-
"""Page Prestations — grille des six métiers puis détail de chaque prestation.

Vidéos : une prestation affiche sa vidéo dès que site/assets/media/prestations/<id>.mp4
existe (avec son poster <id>.jpg), sinon sa photo. La vidéo tourne en boucle dès qu'elle
est à l'écran (ux.js).
Ajouter ou remplacer une vidéo, puis relancer build.py :

    swift -suppress-warnings _build/video_prestation.swift <id> <source>:<debut>-<fin> [...]

Détail de chaque prestation : vignettes cliquables des films complets (FILMS), ouverts dans
une visionneuse avec le son, suivies d'un encadré « Prochainement », puis des logos des
clients et événements (CONFIANCE). Un film n'apparaît que si son MP4 existe dans
site/assets/media/films/ (produit par _build/films_prestations.sh).
"""
import pathlib, struct
from layout import icone

SITE_DIR = pathlib.Path(__file__).resolve().parent.parent / "site"
MEDIA_DIR = SITE_DIR / "assets" / "media" / "prestations"
FILMS_DIR = SITE_DIR / "assets" / "media" / "films"

# Films complets par prestation : (fichier dans media/films, titre, sous-titre).
FILMS = {
    "immobilier": [("immobilier-villeneuve", "Maison à Villeneuve", "Extérieur et intérieur en FPV"),
                   ("immobilier-bali", "Villa à Bali", "Jardin, piscine et façade")],
    "commerces": [("commerces-voutes", "Restaurant Les Voûtes", "Terrasses et salles voûtées, Caluire")],
    "sport": [("sport-criterium-1", "Critérium des Cévennes — 1", "Épingles en forêt vues du ciel"),
              ("sport-criterium-2", "Critérium des Cévennes — 2", "Routes des gorges, vues du dessus"),
              ("sport-criterium-3", "Critérium des Cévennes — 3", "Poursuite FPV au coucher du soleil"),
              ("sport-favas", "Favas", "Session de drift"),
              ("sport-marbil", "Marbil", "Drift, vues du dessus et poursuite")],
    "tourisme": [("tourisme-bali", "Bali", "Piscines à débordement et rizières"),
                 ("tourisme-carroz", "Les Carroz d’Arâches", "Station de montagne en hiver")],
}

# « Ils m'ont déjà fait confiance » : (fichier dans img/logos, nom en texte alternatif, densité).
# Densité = part de pixels opaques du logo rogné, mesurée une fois (PIL, canal alpha) :
# un logo fin paraît plus petit qu'un logo gras à surface égale, _taille_logo compense.
CONFIANCE = {
    "immobilier": [("guylene-berge.png", "Fanny Gavalda — Guylène Bergé Immobilier", .149)],
    "commerces": [("les-voutes.png", "Restaurant Les Voûtes, Caluire", .232)],
    "sport": [("ffsa.png", "FFSA — rallye de montagne", .596),
              ("criterium-cevennes.png", "Critérium des Cévennes", .213),
              ("favas.png", "Favas", .631), ("marbil.svg", "Marbil", .6)],
    "tourisme": [("cretya.png", "Cretya Jungle Lite by Alas Harum, Bali", .283)],
}

SERVICES = [
    {"id": "immobilier", "num": "01", "icon": "building", "titre": "Immobilier, propriété &amp; inspection",
     "court": "Valoriser villas, maisons, domaines et lieux d’exception.",
     "long": "Vidéos et photos aériennes pour révéler un bien sous son meilleur jour — extérieurs, "
             "volumes, environnement. Une prestation pensée aussi bien pour les annonces que pour "
             "la communication d’un promoteur.",
     "image": "assets/img/prestations/immobilier.jpg",
     "livrables": ["Photos HD", "Visite virtuelle 360°", "Inspection de toiture et de façade",
                   "Traversée FPV extérieur / intérieur", "Livraison rapide"],
     "grise": "Stabilisé / FPV"},
    {"id": "commerces", "num": "02", "icon": "utensils", "titre": "Commerces &amp; restaurants",
     "court": "Révéler l’ambiance, l’expérience et le lieu.",
     "long": "Mettre en scène une salle, une terrasse, une vitrine : des images qui donnent envie "
             "d’y être, pensées pour vos réseaux et votre site.",
     "image": "assets/img/prestations/commerces.jpg",
     "livrables": ["Plan de présentation", "Parcours immersif FPV et stabilisé",
                   "Vues extérieur / intérieur", "Séquences produit", "Habillage visuel", "Montage court"],
     "grise": "Stabilisé / FPV"},
    {"id": "sport", "num": "03", "icon": "running", "titre": "Sport &amp; suivi de véhicule",
     "court": "Des images dynamiques et percutantes.",
     "long": "Voiture, moto, VTT : un suivi au plus près de l’action, pensé pour le rythme et la "
             "sensation de vitesse.",
     "image": "assets/img/prestations/sport.jpg",
     "livrables": ["Suivi voiture, moto, vélo", "Plan au sol au plus près de l’action",
                   "Rendu dynamisé FPV", "Clip promotionnel", "Édit court"],
     "grise": "Stabilisé / FPV"},
    {"id": "scans3d", "num": "04", "icon": "box", "titre": "Scans 3D &amp; photogrammétrie",
     "court": "Mesurer et documenter avec précision.",
     "long": "Un maillage 3D texturé et une orthophoto géoréférencée pour mesurer, documenter et "
             "exploiter un site avec précision.",
     "image": "assets/img/prestations/scans3d.jpg",
     "livrables": ["Modélisation 3D", "Orthophoto", "Relevé topographique",
                   "Documentation visuelle exploitable"],
     "grise": "Stabilisé"},
    {"id": "chantier", "num": "05", "icon": "crane", "titre": "Suivi de chantier &amp; BTP",
     "court": "Documenter l’avancement avec clarté et rigueur.",
     "long": "Un point de vue reproduit au fil des mois, pour suivre l’avancement d’un chantier et "
             "communiquer sur son état.",
     "image": "assets/img/prestations/chantier.jpg",
     "livrables": ["Photos de vue régulières", "Photos vue avant / pendant / après",
                   "Time-lapse de chantier", "Relevé et visite photo pour reporting"],
     "grise": "Stabilisé / FPV"},
    {"id": "tourisme", "num": "06", "icon": "mountain", "titre": "Tourisme, patrimoine &amp; communication",
     "court": "Mettre en valeur paysage, destination ou événement.",
     "long": "Paysages, patrimoine, événements : des images qui racontent un territoire et donnent "
             "envie de le découvrir.",
     "image": "assets/img/prestations/tourisme.jpg",
     "livrables": ["Plan large immersif", "Contenu immersif", "Vidéo de présentation",
                   "Capsule réseaux sociaux", "Image storytelling"],
     "grise": "Stabilisé / FPV"},
]

INCLUS = ["Assurance RC Pro", "Repérage terrain", "Format 16/9", "Deux allers-retours de retouche",
          "Options supplémentaires possibles"]

FAQ = [
    ("Faut-il une autorisation ?",
     "Je gère toutes les déclarations et les demandes de vol. En zone contrôlée, veuillez prévoir "
     "un délai de 5 à 10 jours avant intervention."),
    ("Et si la météo est mauvaise ?",
     "En cas de mauvais temps — pluie, brouillard dense, orage, ou vents pouvant atteindre "
     "38 km/h — je ne peux pas intervenir. Report gratuit si les conditions ne sont pas optimales."),
    ("Vous vous déplacez où ?",
     "Partout en France. Mon point de référence est Montpellier : tout déplacement inférieur à "
     "30 km est inclus, au-delà une estimation est prévue dans le calculateur de devis. Si "
     "l’intervention est hors de l’Hérault, les frais de déplacement sont indiqués dans le devis, "
     "en discussion avec vous."),
]

TRUST = [
    ("shield-check", "Télépilote certifié"),
    ("shield", "Conformité européenne"),
    ("building", "Assurance RC Pro"),
    ("spark", "Créativité &amp; exigence"),
    ("compass", "Intervention France"),
]


def _video(s):
    """Chemins (vidéo, poster) de la prestation, ou None si sa vidéo n'existe pas encore."""
    if (MEDIA_DIR / f"{s['id']}.mp4").exists() and (MEDIA_DIR / f"{s['id']}.jpg").exists():
        return f"assets/media/prestations/{s['id']}.mp4", f"assets/media/prestations/{s['id']}.jpg"
    return None


def _media(s, alt):
    """Vidéo en boucle si elle existe, photo sinon. Rien n'est téléchargé avant l'affichage."""
    video = _video(s)
    if not video:
        return f'<img src="{s["image"]}" alt="{alt}" loading="lazy" decoding="async">'
    src, poster = video
    etiquette = f' aria-label="Extrait vidéo — {alt}"' if alt else ' aria-hidden="true"'
    return (f'<video class="boucle-video" src="{src}" poster="{poster}" muted loop playsinline '
            f'preload="none"{etiquette}></video>'
            f'<span class="boucle-video__indice" aria-hidden="true">{icone("play")}</span>')


def _duree_mp4(chemin):
    """Durée « m:ss » lue dans la boîte mvhd du MP4 (sans dépendance)."""
    with open(chemin, "rb") as f:
        while True:
            entete = f.read(8)
            if len(entete) < 8:
                return ""
            taille, nom = struct.unpack(">I4s", entete)
            if taille == 1:
                taille = struct.unpack(">Q", f.read(8))[0] - 8
            if nom == b"moov":
                moov = f.read(taille - 8)
                i = moov.find(b"mvhd")
                version = moov[i + 4]
                if version == 1:
                    echelle, duree = struct.unpack(">IQ", moov[i + 24:i + 36])
                else:
                    echelle, duree = struct.unpack(">II", moov[i + 16:i + 24])
                secondes = round(duree / echelle)
                return f"{secondes // 60}:{secondes % 60:02d}"
            f.seek(taille - 8, 1)


def _films(s):
    """Vignettes des films de la prestation, puis l'encadré « Prochainement »."""
    vignettes = []
    for nom, titre, sous in FILMS.get(s["id"], []):
        video = FILMS_DIR / f"{nom}.mp4"
        if not video.exists():
            continue
        base = f"assets/media/films/{nom}"
        vignettes.append(f"""<li><button type="button" class="film" data-film="{base}.mp4" data-poster="{base}.jpg" data-titre="{titre}">
              <span class="film__media"><img src="{base}-vignette.jpg" alt="" loading="lazy" decoding="async">
                <span class="film__lecture" aria-hidden="true">{icone("play")}</span>
                <span class="film__duree">{_duree_mp4(video)}</span></span>
              <span class="film__titre">{titre}</span><span class="film__sous">{sous}</span>
              <span class="sr-only">— voir le film complet</span>
            </button></li>""")
    vignettes.append(f"""<li class="film film--bientot">
              <span class="film__media"><span class="film__bientot">{icone("clock")}Prochainement</span></span>
              <span class="film__titre">D’autres films arrivent</span><span class="film__sous">Nouveaux tournages en cours de montage</span>
            </li>""")
    return f"""<div class="films">
            <span class="label-mono">Films complets</span>
            <ul class="films__grille">{"".join(vignettes)}</ul>
          </div>"""


def _illustration(s):
    """Photo d'illustration, seulement pour une prestation qui n'a encore aucun film."""
    if any((FILMS_DIR / f"{nom}.mp4").exists() for nom, *_ in FILMS.get(s["id"], [])):
        return ""
    return f"""<div class="media-frame media-frame--4-3">
            <img src="{s['image']}" alt="{s['titre']}" loading="lazy" decoding="async">
            <div class="media-frame__caption"><span class="media-frame__label">{s['titre']}</span></div>
          </div>"""


LOGOS_DIR = SITE_DIR / "assets" / "img" / "logos"
# Surface commune des logos (px²) : celle des logos Sport, validés à environ 130 × 20 px.
# À surface égale, un logo étroit (Cretya, Critérium) n'a pas l'air plus petit qu'un logo long.
# La densité corrige à moitié l'écart avec un logo gras (DENSITE_REF) : en totalité, un tracé
# très fin comme Guylène Bergé doublerait de taille.
AIRE_LOGO = 2600
DENSITE_REF = .6


def _taille_logo(fichier, densite):
    """(largeur, hauteur) d'affichage d'un logo, à surface égale (en-tête PNG ou viewBox SVG)."""
    chemin = LOGOS_DIR / fichier
    if chemin.suffix == ".svg":
        import re
        *_, l, h = (float(v) for v in re.search(r'viewBox="([^"]+)"', chemin.read_text()).group(1).split())
    else:
        l, h = struct.unpack(">II", chemin.read_bytes()[16:24])
    ratio = l / h
    hauteur = min(40, (AIRE_LOGO / ratio) ** .5 * (DENSITE_REF / densite) ** .25)
    return round(hauteur * ratio), round(hauteur)


def _confiance(s):
    logos = CONFIANCE.get(s["id"], [])
    if not logos:
        return ""
    items = "".join('<li><img src="assets/img/logos/{}" alt="{}" title="{}" width="{}" height="{}" loading="lazy"></li>'
                    .format(f, nom, nom, *_taille_logo(f, d)) for f, nom, d in logos)
    return f"""<div class="confiance">
            <p class="confiance__titre">Ils m’ont déjà fait confiance</p>
            <ul class="confiance__logos">{items}</ul>
          </div>"""


def _carte_selection(s):
    boucle = " data-boucle" if _video(s) else ""
    return f"""<a class="card card--flush card--interactive service-card detail-select reveal-in" href="#p-{s['id']}"{boucle}>
          <div class="service-card__media">{_media(s, "")}</div>
          <div class="service-card__body">
            <span class="service-card__icon icon">{icone(s['icon'])}</span>
            <h3 class="service-card__title">{s['titre']}</h3>
            <p class="service-card__desc">{s['court']}</p>
          </div>
        </a>"""


def _detail(s, actif=False):
    livrables = "".join(f'<li>{icone("check")}{item}</li>' for item in s["livrables"])
    inclus = "".join(f'<li>{icone("check")}{item}</li>' for item in INCLUS)
    classe = "detail-grid detail-panel is-active" if actif else "detail-grid detail-panel"
    return f"""<div class="{classe}" id="p-{s['id']}" style="scroll-margin-top:calc(var(--nav-h) + 24px)">
        <div class="reveal-in">
          <span class="label-mono">{s['num']} — Détail de la prestation</span>
          <h2 class="detail-grid__title">{s['titre']}</h2>
          <p class="detail-grid__lead">{s['long']}</p>
          <div class="detail-grid__badges">
            <span class="badge badge--neutral">{s['grise']}</span>
            <span class="badge badge--tech">4K 24p · Montage / colorimétrie</span>
          </div>
          <div class="detail-grid__actions">
            <a class="btn btn--primary" href="tarifs.html#devis">Chiffrer cette prestation{icone('arrow-right','btn__arrow')}</a>
            <a class="btn btn--ghost" href="contact.html">Poser une question</a>
          </div>
          <div class="reveal-in">
            <span class="label-mono" style="display:block;margin-top:var(--sp-8);margin-bottom:var(--sp-4)">Livrables inclus</span>
            <ul class="detail-grid__included">{livrables}</ul>
          </div>
        </div>
        <div class="detail-grid__side reveal-in reveal-in--d1">
          {_illustration(s)}
          {_films(s)}
          {_confiance(s)}
          <div class="card">
            <span class="label-mono">Inclus dans toutes les prestations</span>
            <ul class="detail-grid__included">{inclus}</ul>
          </div>
        </div>
      </div>"""


def contenu():
    grille = "".join(_carte_selection(s) for s in SERVICES)
    details = "".join(_detail(s, actif=(i == 0)) for i, s in enumerate(SERVICES))
    faq = "".join(f"""<div class="accordion__item">
        <button type="button" class="accordion__q">{q}<span class="accordion__plus" aria-hidden="true"></span></button>
        <div class="accordion__a"><p>{a}</p></div>
      </div>""" for q, a in FAQ)
    trust = "".join(f"""<div class="trust__item">{icone(ic)}<span>{lib}</span></div>"""
                     for ic, lib in TRUST)

    return f"""    <section class="section" style="padding-top:var(--sp-8)">
      <div class="container">
        <div class="reveal-in">
          <p class="eyebrow">Prestations</p>
          <h1 class="page-hero__title">Des services pensés<br>pour chaque projet</h1>
          <p class="page-hero__lead">Sky Perspective réalise des vidéos aériennes partout en France,
            en alliant plans stabilisés cinématiques et immersifs FPV selon les objectifs et les
            contraintes de chaque projet.</p>
        </div>
        <div class="service-grid service-grid--6">{grille}</div>
      </div>
    </section>

    <div class="container"><div class="horizon-rule reveal-in" aria-hidden="true"></div></div>

    <section class="section section--tight">
      <div class="container">
        <div id="details-wrap">{details}</div>

        <div class="reveal-in" style="margin-top:var(--sp-8)">
          <span class="label-mono" style="font-weight:var(--fw-semibold)">Questions fréquentes</span>
          <div class="accordion">{faq}</div>
        </div>

        <div class="reveal-in trust" style="margin-top:var(--sp-8)">{trust}</div>
        <div class="reveal-in reveal-in--d1" style="margin-top:var(--sp-8);text-align:center">
          <h2 class="cta-band__title" style="text-align:center">Parlons de votre projet</h2>
          <p style="margin-top:var(--sp-4)"><a class="btn btn--primary btn--lg" href="contact.html">
            Me contacter{icone('arrow-right','btn__arrow')}</a></p>
        </div>
      </div>
    </section>

    <dialog class="visionneuse" aria-labelledby="visionneuse-titre">
      <div class="visionneuse__barre">
        <p class="visionneuse__titre" id="visionneuse-titre"></p>
        <button type="button" class="visionneuse__fermer" aria-label="Fermer le film">&times;</button>
      </div>
      <video class="visionneuse__video" controls playsinline preload="none"></video>
    </dialog>"""
