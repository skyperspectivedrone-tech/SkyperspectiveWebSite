# -*- coding: utf-8 -*-
"""Page Prestations — grille des six métiers puis détail de chaque prestation."""
from layout import icone

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


def _carte_selection(s):
    return f"""<a class="card card--flush card--interactive service-card detail-select reveal-in" href="#p-{s['id']}">
          <div class="service-card__media"><img src="{s['image']}" alt="" loading="lazy" decoding="async"></div>
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
          <div class="media-frame media-frame--4-3">
            <img src="{s['image']}" alt="{s['titre']}" loading="lazy" decoding="async">
            <div class="media-frame__caption"><span class="media-frame__label">{s['titre']}</span></div>
          </div>
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
    </section>"""
