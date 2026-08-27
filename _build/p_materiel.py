# -*- coding: utf-8 -*-
"""Page Matériel : deux séquences 3D pilotées au scroll, sans hero d'accueil."""
from layout import icone

SEQUENCES = [
    {
        "id": "air3s",
        "base": "assets/media/air3s",
        "images": 81,
        "surtitre": "01 — Stabilisé",
        "etapes": [
            ("DJI Air 3S", "Le regard posé.",
             "Un drone stabilisé taillé pour les mouvements lents et les révélations de "
             "paysage. Là où le FPV cherche la sensation, celui-ci cherche la lisibilité : "
             "un cadre net, une trajectoire maîtrisée, une image qui se regarde."),
            ("Stabilisation trois axes", "La netteté avant tout.",
             "Nacelle stabilisée sur trois axes et capteur d’un pouce : les plans restent "
             "propres même par vent soutenu. L’enregistrement en profil D-Log conserve la "
             "matière dans les hautes lumières et les ombres pour l’étalonnage."),
            ("24 mm et 70 mm", "Le choix de la focale.",
             "Deux focales embarquées, et donc deux façons de raconter la même scène. "
             "Le 24 mm ouvre l’espace et situe le lieu ; le 70 mm isole un détail, compresse "
             "les plans et donne cette texture de cinéma que le grand-angle ne produit jamais."),
        ],
    },
    {
        "id": "avata2",
        "base": "assets/media/avata2",
        "images": 32,
        "surtitre": "02 — FPV",
        "etapes": [
            ("DJI Avata 2", "L’immersion, au plus près.",
             "Un drone FPV pensé pour la vitesse et la proximité. La caméra cesse d’être un "
             "point de vue extérieur : elle devient un regard qui traverse l’espace, à hauteur "
             "d’homme comme au ras du sol."),
            ("Vol en intérieur", "Là où les autres s’arrêtent.",
             "Les protections d’hélices intégrées autorisent le vol en intérieur et les "
             "passages serrés — une porte, un couloir, une cuisine en service — sans risque "
             "pour les lieux ni pour les personnes."),
            ("Un seul plan continu", "De l’extérieur à l’intérieur.",
             "C’est le plan qui fait la différence : le drone part de la rue, franchit la "
             "porte et parcourt l’intérieur sans la moindre coupure. Un mouvement unique qui "
             "présente un bien, un commerce ou une société mieux qu’un montage entier."),
        ],
    },
]


def _reveal(seq, premier=False):
    haut = ('<div class="reveal__vignette reveal__vignette--haut" aria-hidden="true"></div>'
            if premier else "")
    etapes = "".join(
        f"""<article class="reveal__caption">
              <h2 class="reveal__title">{titre}</h2>
              <p class="reveal__tagline">{accroche}</p>
              <p class="reveal__text">{texte}</p>
            </article>"""
        for titre, accroche, texte in seq["etapes"]
    )
    reperes = "".join(
        f'<span class="reveal__marker"><i></i>{i + 1:02d}</span>'
        for i in range(len(seq["etapes"]))
    )
    # Course de défilement calée sur le nombre d'images : ~8 px par image,
    # avec un plancher pour que les trois légendes restent lisibles.
    course = max(420, seq["images"] * 8)
    return f"""    <section class="reveal" data-reveal data-base="{seq['base']}"
             data-count="{seq['images']}" data-frames-json="seq-{seq['id']}"
             style="--course: {course}px" aria-label="{seq['etapes'][0][0]}">
      <div class="reveal__sticky">
        <canvas class="reveal__canvas"></canvas>
        <div class="reveal__scrim"></div>
        {haut}
        <div class="reveal__vignette reveal__vignette--bas" aria-hidden="true"></div>
        <div class="container reveal__content">
          <div class="reveal__col">
            <p class="eyebrow">{seq['surtitre']}</p>
            <div class="reveal__captions">{etapes}</div>
          </div>
          <div class="reveal__markers">{reperes}</div>
        </div>
      </div>
    </section>"""


def contenu():
    reveals = "\n".join(_reveal(seq, i == 0) for i, seq in enumerate(SEQUENCES))
    return f"""{reveals}

    <div class="transition-noir-bleu" aria-hidden="true"></div>

    <section class="section">
      <div class="container">
        <div class="detail-grid reveal-in" style="padding-bottom:var(--sp-8);border-bottom:1px solid var(--border-hairline)">
          <div>
            <span class="label-mono">Post-production</span>
            <h2 class="detail-grid__title">Montage</h2>
            <p class="detail-grid__lead">La retouche photo se fait sous Adobe Lightroom et
              Photoshop. Le montage vidéo, l’étalonnage et le sound design se font
              principalement sous DaVinci Resolve.</p>
          </div>
          <div class="media-frame media-frame--4-3">
            <img src="assets/img/montage-colorimetrie.jpg" alt="Étalonnage colorimétrique d’un plan drone en montage vidéo." loading="lazy" decoding="async">
          </div>
        </div>

        <div class="detail-grid reveal-in" style="padding-top:var(--sp-8)">
          <div>
            <span class="label-mono">Cadre légal</span>
            <h2 class="detail-grid__title">Voler dans les règles</h2>
            <p class="detail-grid__lead">La sécurité fait partie de la prestation. Exploitant
              enregistré auprès de la Direction générale de l’aviation civile, assuré en
              responsabilité civile professionnelle, et vols conduits selon la réglementation
              européenne en vigueur. Les zones sont vérifiées avant chaque mission et les
              autorisations nécessaires sont prises en charge.</p>
          </div>
          <div class="card">
            <span class="label-mono">Inclus</span>
            <ul class="detail-grid__included">
              <li>{icone('check')}Vérification des zones de vol</li>
              <li>{icone('check')}Demandes d’autorisation</li>
              <li>{icone('check')}Assurance RC professionnelle</li>
              <li>{icone('check')}Repérage terrain</li>
            </ul>
          </div>
        </div>

        <div class="reveal-in" style="margin-top:var(--sp-8)"><div class="horizon-rule" aria-hidden="true"></div></div>

        <div class="reveal-in card card--navy cta-band" style="margin-top:var(--sp-8);padding:clamp(32px,5vw,72px)">
          <div>
            <h2 class="cta-band__title">Le bon drone pour votre projet</h2>
            <p class="cta-band__text">Stabilisé, FPV, ou les deux dans un même film : dites-moi
              ce que vous voulez montrer, je vous dis comment le filmer.</p>
          </div>
          <a class="btn btn--primary btn--lg" href="tarifs.html#devis">Demander un devis{icone('arrow-right','btn__arrow')}</a>
        </div>
      </div>
    </section>"""
