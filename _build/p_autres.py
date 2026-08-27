# -*- coding: utf-8 -*-
"""Accueil et Contact."""
from layout import SITE, icone
import tarifs_config as cfg


def _section_heading(eyebrow, titre, lead=""):
    lead_html = f'<p class="section-heading__lead">{lead}</p>' if lead else ""
    return f"""<header class="section-heading reveal-in">
        <p class="eyebrow">{eyebrow}</p>
        <h2 class="section-heading__title">{titre}</h2>
        {lead_html}
      </header>"""


PILIERS = [
    ("assets/img/air3s-still.jpg", "Précision et stabilité",
     "Plans aériens fluides et maîtrisés pour sublimer vos projets avec une qualité cinéma."),
    ("assets/img/avata2-still.jpg", "Immersion et dynamisme",
     "Plans immersifs et nerveux pour capturer l’adrénaline et raconter autrement."),
    ("assets/img/alpes-sunrise.jpg", "Scan 3D",
     "Un relevé précis pour mesurer, documenter et valoriser chaque site."),
]

DEROULE = [
    ("10 %", "Prise de contact",
     "Vous décrivez votre projet, je valide la faisabilité et vous envoie un devis précis."),
    ("25 %", "Repérage des lieux",
     "Vérification des zones de vol, des accès et des autorisations à obtenir."),
    ("50 %", "Tournage",
     "Prise de vue stabilisée, FPV, ou les deux selon ce qu’il y a à raconter."),
    ("80 %", "Post-production",
     "Montage, étalonnage, sound design."),
    ("99 %", "Livraison",
     "Vous recevez vos fichiers prêts à publier. Un tour de retouches est compris."),
    ("100 %", "Suivi après livraison",
     "Je reste joignable pour un nouveau format ou une question, même une fois le projet terminé."),
]


def _pilier(chemin, titre, texte, i):
    delai = f" reveal-in--d{i}" if i else ""
    return f"""<div class="card card--flush service-card reveal-in{delai}">
          <div class="service-card__media"><img src="{chemin}" alt="" loading="lazy" decoding="async"></div>
          <div class="service-card__body">
            <h3 class="service-card__title">{titre}</h3>
            <p class="service-card__desc">{texte}</p>
          </div>
        </div>"""


def _deroule():
    etapes = "".join(f"""<li class="deroule__etape">
            <span class="deroule__pct">{pct}</span>
            <div class="deroule__corps">
              <span class="deroule__titre">{titre}</span>
              <p class="deroule__texte">{texte}</p>
            </div>
          </li>""" for pct, titre, texte in DEROULE)
    return f'<ol class="deroule">{etapes}</ol>'


def accueil():
    piliers = "".join(_pilier(c, t, x, i) for i, (c, t, x) in enumerate(PILIERS))
    return f"""    <section class="hero">
      <img class="hero__decor" src="assets/img/hero-alpes.jpg" width="1600" height="900"
           alt="Sommet alpin enneigé au lever du soleil, photographié au drone."
           fetchpriority="high" decoding="async">
      <div class="hero__voile" aria-hidden="true"></div>
      <div class="hero__voile--bas" aria-hidden="true"></div>
      <div class="hero__voile--haut" aria-hidden="true"></div>
      <div class="hero__contenu">
        <div class="hero__kicker"><i></i><span class="label-mono">Télépilote de drone · Montpellier</span></div>
        <h1 class="hero__titre">Des images,<br>une perspective,<br>votre histoire.</h1>
        <p class="hero__lead">Pilote de drone professionnel, je transforme vos projets en images
          spectaculaires et immersives.</p>
        <div class="hero__actions">
          <a class="btn btn--primary btn--lg" href="tarifs.html#devis">Estimer mon projet
            <span class="btn__arrow">{icone('arrow-right')}</span></a>
          <a class="btn btn--ghost btn--lg" href="prestations.html">Voir les prestations</a>
        </div>
        <div class="hero__stats">
          <div class="stat"><div class="stat__value">6</div><div class="stat__label">Prestations</div></div>
          <span class="stat-divider" aria-hidden="true"></span>
          <div class="stat"><div class="stat__value">72<span class="stat__unit">h</span></div>
            <div class="stat__label">Livraison</div><div class="stat__note">(ou plus selon le projet)</div></div>
          <span class="stat-divider" aria-hidden="true"></span>
          <div class="stat"><div class="stat__value">4K<span class="stat__unit">24p</span></div>
            <div class="stat__label">Format natif</div></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        {_section_heading("Ce que je fais", "Trois façons de voir votre projet")}
        <div class="service-grid">{piliers}</div>
      </div>
    </section>

    <div class="container"><div class="horizon-rule reveal-in" aria-hidden="true"></div></div>

    <section class="section" data-theme="light">
      <div class="container">
        <div class="detail-grid" style="align-items:start">
          <div>
            {_section_heading("Méthode", "Comment ça se passe",
              "Chaque projet suit le même chemin. Vous savez à tout moment où en est le vôtre.")}
          </div>
          <div class="reveal-in reveal-in--d1">{_deroule()}</div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="card card--navy reveal-in cta-band" style="padding:clamp(32px,5vw,72px)">
          <div>
            <h2 class="cta-band__title">Un projet en tête ?</h2>
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


CONTACT_INFOS = [
    ("mail", "E-mail", SITE["email"]),
    ("tel", "Téléphone", SITE["tel"]),
    ("pin", "Zone", "Montpellier (34) · interventions partout en France"),
    ("clock", "Disponibilité", "Semaine et week-end, sur rendez-vous"),
]


def contact():
    lignes = "".join(f"""<div class="contact-info__row">
              <span class="contact-info__icon">{icone(ic)}</span>
              <div>
                <span class="label-mono contact-info__label">{lib}</span>
                <span class="contact-info__value">{val}</span>
              </div>
            </div>""" for ic, lib, val in CONTACT_INFOS)

    contact_config = ('{"endpoint":"' + cfg.FORMULAIRE["endpoint"] + '","cle":"'
                       + cfg.FORMULAIRE["cle"] + '","email":"' + SITE["email"] + '"}')

    return f"""    <section class="section" style="padding-top:var(--sp-8)">
      <div class="container">
        <div class="contact-grid">
          <div>
            <div class="reveal-in">
              <p class="eyebrow">Contact</p>
              <h1 class="page-hero__title">Parlons de votre projet</h1>
              <p class="page-hero__lead">Je réponds sous 24 h, le devis est gratuit et sans
                engagement.</p>
            </div>
            <div class="contact-info reveal-in reveal-in--d1">{lignes}</div>
          </div>

          <div class="reveal-in reveal-in--d1">
            <div class="card" style="padding:clamp(24px,3vw,40px)">
              <form id="contact-form" novalidate style="display:grid;gap:var(--sp-5)">
                <div class="formulaire__grille">
                  <p class="champ"><label for="ct-nom">Nom</label>
                    <input id="ct-nom" type="text" autocomplete="name" placeholder="Marie Dubois" required></p>
                  <p class="champ"><label for="ct-tel">Téléphone</label>
                    <input id="ct-tel" type="tel" autocomplete="tel" placeholder="06 12 34 56 78" required></p>
                </div>
                <p class="champ"><label for="ct-email">E-mail</label>
                  <input id="ct-email" type="email" autocomplete="email" placeholder="marie@agence.fr" required>
                  <span class="champ__aide">Je ne transmets votre adresse à personne.</span></p>
                <p class="champ"><label for="ct-projet">Le projet</label>
                  <textarea id="ct-projet" rows="5" placeholder="Le lieu, la date souhaitée, ce que la vidéo doit montrer."></textarea></p>
                <input type="checkbox" id="ct-botcheck" class="sr-only" tabindex="-1" autocomplete="off" aria-hidden="true">
                <button type="submit" id="ct-envoyer" class="btn btn--primary btn--lg" style="width:100%" disabled>
                  Envoyer<span class="btn__arrow">{icone('arrow-right')}</span></button>
                <p class="formulaire__etat" id="ct-etat" role="status"></p>
              </form>
              <div id="ct-envoye" hidden style="display:grid;gap:var(--sp-4)">
                <span style="color:var(--accent-hover)">{icone('check')}</span>
                <h3 class="etape--fin h3" style="margin:0">Message envoyé</h3>
                <p style="color:var(--text-body)">Je vous réponds sous 24 heures. Si c’est urgent, appelez-moi
                  directement au {SITE['tel']}.</p>
              </div>
              <script type="application/json" id="contact-config">{contact_config}</script>
            </div>
          </div>
        </div>
      </div>
    </section>"""
