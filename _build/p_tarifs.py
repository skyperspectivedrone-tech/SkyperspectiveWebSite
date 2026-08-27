# -*- coding: utf-8 -*-
"""Page Tarifs : grille de prix, options, et calculateur de devis en ligne."""
from layout import SITE, icone
import tarifs_config as cfg

ICONES_PRESTATION = {
    "immobilier": "building", "inspection": "shield-check", "commerces": "utensils",
    "sport": "running", "tourisme": "mountain", "scans3d": "box", "chantier": "crane",
}

OPTIONS_CARTES = [
    ("Version verticale 9:16", "Format vertical pour mobile et réseaux sociaux.", "+ 60 €",
     '<rect x="7" y="2.5" width="10" height="19" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/>'
     '<path d="M10.5 5.5h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'),
    ("Déplacement", "Inclus jusqu’à 30 km depuis Montpellier, puis 0,40 €/km.", "0,40 €/km",
     '<path d="M12 21.5s7-6.9 7-11a7 7 0 1 0-14 0c0 4.1 7 11 7 11z" fill="none" stroke="currentColor" stroke-width="1.6"/>'
     '<circle cx="12" cy="10.2" r="2.6" fill="none" stroke="currentColor" stroke-width="1.6"/>'),
    ("Zone aérienne complexe", "Autorisations spécifiques en zone contrôlée ou urbaine.", "+ 10 à 20 %",
     '<path d="M12 2.5 20.5 6v6.5c0 5.2-3.6 8.5-8.5 9.5-4.9-1-8.5-4.3-8.5-9.5V6z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
     '<path d="M12 8v4.5M12 15.6v.1" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'),
    ("Utilisation publicitaire étendue", "TV, cinéma, réseaux, campagne nationale.", "Sur devis",
     '<rect x="2.5" y="4.5" width="19" height="13" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/>'
     '<path d="M10.2 8.6v4.8l4.2-2.4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
     '<path d="M8 21h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'),
    ("Cession de droits étendue", "Cession portant sur les fichiers vidéo bruts.", "Sur devis",
     '<path d="M5.5 2.5h8l5 5v14h-13z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
     '<path d="M13.5 2.5v5h5M8.5 12.5h7M8.5 16.5h7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'),
]


def _grille():
    lignes = ""
    for i, p in enumerate(cfg.PRESTATIONS):
        plancher = cfg.prix_plancher(p)
        suffixe = p.get("suffixe", "").strip(" /")
        unit = f'/{suffixe}' if suffixe else ""
        delai = f" reveal-in--d{i % 4}" if i else ""
        lignes += f"""
        <div class="price-row reveal-in{delai}">
          <span class="price-row__icon icon">{icone(ICONES_PRESTATION.get(p['cle'], 'building'))}</span>
          <div>
            <span class="price-row__name">{p['titre']}</span>
            <p class="price-row__detail">{p['description']}</p>
          </div>
          <div class="price-row__amount">
            <span class="price-row__value">dès {plancher} €</span>
            <span class="price-row__unit">{unit}</span>
          </div>
        </div>"""
    return lignes


def _options_cartes():
    cartes = "".join(
        f"""<div class="option reveal-in">
          <svg viewBox="0 0 24 24" aria-hidden="true">{svg}</svg>
          <h3>{titre}</h3><p>{texte}</p>
          <p class="option__prix">{prix}</p>
        </div>"""
        for titre, texte, prix, svg in OPTIONS_CARTES
    )
    return f"""
        <div class="options-bloc">
          <p class="eyebrow">Options &amp; suppléments</p>
          <h2 class="section-heading__title" style="font-size:var(--fs-h1);margin-top:var(--sp-3)">À la carte, selon votre projet.</h2>
          <div class="options">{cartes}</div>
          <p class="options-bloc__note">Ces options s’ajoutent au tarif de base de la prestation.
            Le déplacement et la complexité de la zone aérienne sont calculés automatiquement
            dans l’estimation ci-dessous.</p>
        </div>"""


def _calculateur():
    prestations = "".join(
        f'<option value="{p["cle"]}">{p["titre"]}</option>' for p in cfg.PRESTATIONS
    )
    complexites = "".join(
        f'<option value="{cle}">{lib}</option>' for cle, lib, _ in cfg.COMPLEXITES
    )
    durees = "".join(f'<option value="{cle}">{lib}</option>' for cle, lib, _ in cfg.DUREES)

    types_client = "".join(
        f'<option value="{cle}">{lib}</option>' for cle, lib in cfg.TYPES_CLIENT
    )

    cases = ""
    for cle, lib, prix, _typ in cfg.OPTIONS:
        impose = cfg.OPTIONS_IMPOSEES.get(cle)
        info = ""
        if impose:
            info = (f'<button type="button" class="info" aria-expanded="false" '
                    f'aria-controls="info-{cle}" aria-label="En savoir plus">?</button>'
                    f'<span class="info__bulle" id="info-{cle}" role="note" hidden>'
                    f'{impose["explication"]}</span>')
        cases += f"""<label class="case" data-case="{cle}">
              <input type="checkbox" data-option="{cle}" data-libelle="{lib}">
              <span class="case__texte">{lib}{info}</span>
              <span class="case__prix">{"+ " + str(prix) + " €" if prix else "Sur devis"}</span>
            </label>"""

    recap = "".join(
        f'<li><span>{lib}</span><strong data-recap="{cle}">—</strong></li>'
        for cle, lib in [
            ("prestation", "Type de prestation"),
            ("complexite", "Complexité"),
            ("duree", "Durée estimée"),
            ("options", "Options"),
            ("deplacement", "Déplacement"),
        ]
    )
    inclus = " · ".join(cfg.INCLUS)

    return f"""
        <section class="devis-bloc" id="devis" aria-labelledby="devis-titre">
          <header class="devis-bloc__entete reveal-in">
            <p class="eyebrow">Calculer votre devis en ligne</p>
            <h2 class="section-heading__title" id="devis-titre" style="font-size:var(--fs-h1);margin-top:var(--sp-3)">Estimez votre projet.</h2>
            <p class="devis-bloc__intro">Répondez à quelques questions, une à la fois.
              Votre estimation se complète à mesure, à droite.</p>
          </header>
          <div class="devis reveal-in reveal-in--d1">
            <div class="devis__form">
              <div class="etapes">

                <div class="etape" data-etape="prestation" hidden>
                  <p class="champ">
                    <label for="dv-prestation">Type de prestation</label>
                    <select id="dv-prestation"><option value="">Sélectionnez…</option>{prestations}</select>
                  </p>
                </div>

                <div class="etape" data-etape="formule" hidden>
                  <p class="champ">
                    <label for="dv-formule">Formule</label>
                    <select id="dv-formule"><option value="">Sélectionnez…</option></select>
                  </p>
                </div>

                <div class="etape" data-etape="adresse" hidden>
                  <div class="champ champ--adresse">
                    <label for="dv-adresse">Adresse du lieu de tournage</label>
                    <input id="dv-adresse" type="text" autocomplete="off" spellcheck="false"
                           placeholder="Commencez à saisir une adresse…"
                           aria-expanded="false" aria-autocomplete="list"
                           role="combobox" aria-controls="dv-suggestions">
                    <ul class="suggestions" id="dv-suggestions" role="listbox" hidden></ul>
                    <span class="champ__aide">Facultatif — sans adresse, le déplacement
                      restera à préciser.</span>
                  </div>
                  <p class="champ champ--secours" id="dv-secours" hidden>
                    <label for="dv-km">Distance depuis Montpellier (km)</label>
                    <input id="dv-km" type="number" min="0" step="1" inputmode="numeric"
                           placeholder="Ex. 72">
                    <span class="champ__aide">Le calcul automatique n’est pas disponible ici :
                      saisissez la distance routière.</span>
                  </p>
                </div>

                <div class="etape" data-etape="complexite" hidden>
                  <p class="champ">
                    <label for="dv-complexite">Complexité de la zone aérienne</label>
                    <select id="dv-complexite"><option value="">Sélectionnez…</option>{complexites}</select>
                  </p>
                </div>

                <div class="etape" data-etape="duree" hidden>
                  <p class="champ">
                    <label for="dv-duree">Durée estimée</label>
                    <select id="dv-duree"><option value="">Sélectionnez…</option>{durees}</select>
                  </p>
                </div>

                <div class="etape" data-etape="options" hidden>
                  <fieldset class="cases">
                    <legend>Options &amp; suppléments</legend>
                    {cases}
                  </fieldset>
                </div>

                <div class="etape" data-etape="coordonnees" hidden>
                  <h3 class="etape__titre">Vos coordonnées</h3>
                  <p class="etape__intro">Votre estimation est prête. Laissez-moi de quoi vous
                    recontacter : je vous réponds sous 24 h avec un devis précis.</p>

                  <div class="formulaire">
                    <div class="formulaire__grille">
                      <p class="champ"><label for="dv-prenom">Prénom *</label>
                        <input id="dv-prenom" type="text" autocomplete="given-name" required></p>
                      <p class="champ"><label for="dv-nom">Nom *</label>
                        <input id="dv-nom" type="text" autocomplete="family-name" required></p>
                      <p class="champ"><label for="dv-email">E-mail *</label>
                        <input id="dv-email" type="email" autocomplete="email" required></p>
                      <p class="champ"><label for="dv-tel">Téléphone *</label>
                        <input id="dv-tel" type="tel" autocomplete="tel" required></p>
                      <p class="champ"><label for="dv-type">Vous êtes *</label>
                        <select id="dv-type" required><option value="">Sélectionnez…</option>{types_client}</select></p>
                      <p class="champ" id="dv-societe-champ" hidden>
                        <label for="dv-societe">Raison sociale *</label>
                        <input id="dv-societe" type="text" autocomplete="organization"></p>
                      <p class="champ"><label for="dv-date">Date ou période souhaitée</label>
                        <input id="dv-date" type="text" placeholder="Ex. deuxième quinzaine de mai"></p>
                    </div>

                    <p class="champ"><label for="dv-projet">Décrivez votre projet</label>
                      <textarea id="dv-projet" rows="4"
                        placeholder="Ce que vous souhaitez montrer, les contraintes du lieu, vos délais…"></textarea></p>

                    <label class="case case--engagement">
                      <input type="checkbox" id="dv-autorisation" required>
                      <span class="case__texte">Je dispose de l’autorisation du propriétaire des
                        lieux pour la prise de vue. *</span>
                    </label>
                    <label class="case case--engagement">
                      <input type="checkbox" id="dv-consentement" required>
                      <span class="case__texte">J’accepte que ces informations soient utilisées
                        pour traiter ma demande. *</span>
                    </label>

                    <input type="checkbox" id="dv-botcheck" class="sr-only" tabindex="-1"
                           autocomplete="off" aria-hidden="true">
                    <p class="formulaire__etat" id="dv-etat" role="status"></p>
                  </div>
                </div>

                <div class="etape etape--fin" data-etape="fin" hidden>
                  <h3>Demande envoyée.</h3>
                  <p>Merci, j’ai bien reçu votre projet et votre estimation. Je vous réponds
                    sous 24 h avec un devis précis. À très vite.</p>
                </div>
              </div>

              <div class="etapes__pied">
                <button type="button" class="btn btn--ghost btn--sm" id="dv-retour">← Retour</button>
                <button type="button" class="btn btn--primary btn--sm" id="dv-suivant">Continuer →</button>
                <p class="etapes__progression">
                  <span id="dv-progression">Étape 1</span>
                  <i><b id="dv-jauge"></b></i>
                </p>
              </div>
            </div>

            <aside class="devis__recap">
              <h3>Récapitulatif estimatif</h3>
              <ul class="devis__lignes">{recap}</ul>
              <p class="devis__total">
                <span>Total estimatif</span>
                <strong id="dv-total" aria-live="polite">—</strong>
              </p>
              <a class="btn btn--primary devis__envoi" id="dv-envoyer"
                 data-email="{SITE['email']}" href="mailto:{SITE['email']}">Envoyer ma demande →</a>
              <p class="devis__mention" id="dv-mention">Commencez par choisir le type de prestation.</p>
              <p class="devis__inclus"><span>Inclus dans toutes les prestations :</span> {inclus}</p>
            </aside>
          </div>
        </section>
        <script type="application/json" id="devis-config">{cfg.config_json()}</script>"""


def contenu():
    return f"""    <section class="section" style="padding-top:var(--sp-8);padding-bottom:var(--sp-7)">
      <div class="container">
        <div class="reveal-in">
          <p class="eyebrow">Tarifs</p>
          <h1 class="page-hero__title">Des tarifs clairs.<br>Une offre adaptée.</h1>
          <p class="page-hero__lead">Des images professionnelles, pensées pour valoriser vos
            projets et raconter votre histoire. Les prises de vue stabilisées et FPV peuvent
            être combinées selon votre projet, sans supplément automatique.</p>
        </div>
        <div class="reveal-in reveal-in--d1" style="margin-top:var(--sp-8)">{_grille()}</div>
      </div>
    </section>

    <div class="container"><div class="horizon-rule reveal-in" aria-hidden="true"></div></div>

    <section class="section">
      <div class="container">{_calculateur()}</div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="container"><div class="reveal-in">{_options_cartes()}</div></div>
    </section>"""
