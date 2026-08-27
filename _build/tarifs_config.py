# -*- coding: utf-8 -*-
"""Barème du calculateur de devis. Source unique : le HTML et le JS lisent ces valeurs.

Total = (prix de la prestation + supplément de durée) × (1 + complexité)
        + options fixes + déplacement
"""

# Chaque prestation a soit un prix de base, soit une liste de formules.
# `duree` indique si le menu « durée estimée » s'applique.
PRESTATIONS = [
    {
        "cle": "immobilier",
        "titre": "Immobilier &amp; propriété",
        "description": "Maison, villa, bien d’exception, programme immobilier.",
        "formules": [
            ("standard", "Visite virtuelle 360° — bien standard", 200),
            ("prestige", "Visite virtuelle 360° — villa de prestige", 400),
            ("domaine", "Visite virtuelle 360° — domaine ou hôtel", 1000),
        ],
        "duree": False,
    },
    {
        "cle": "inspection",
        "titre": "Inspection toiture &amp; ouvrage d’art",
        "description": "Toiture, façade et ouvrage d’art.",
        "formules": [
            ("survol", "Survol chantier + orthophoto HD", 149),
            ("toiture-200", "Inspection toiture — moins de 200 m²", 49),
            ("toiture-500", "Inspection toiture — 200 à 500 m²", 119),
            ("facade", "Inspection façade ou ouvrage d’art", 99, "apartir"),
        ],
        "duree": False,
    },
    {
        "cle": "commerces",
        "titre": "Commerces &amp; restaurants",
        "description": "Boutique, restaurant, hôtel, domaine, camping.",
        "base": 590,
        "duree": False,
    },
    {
        "cle": "sport",
        "titre": "Sport &amp; suivi de véhicule",
        "description": "Voiture, moto, VTT, événement sportif.",
        "base": 850,
        "duree": True,
    },
    {
        "cle": "tourisme",
        "titre": "Tourisme, patrimoine &amp; communication",
        "description": "Office de tourisme, lieu de tourisme, entreprise.",
        "base": 850,
        "duree": False,
    },
    {
        "cle": "scans3d",
        "titre": "Scans 3D &amp; photogrammétrie",
        "description": "Relevé visuel, modèle 3D de bâtiment et de site.",
        "base": 750,
        "duree": False,
    },
    {
        "cle": "chantier",
        "titre": "Suivi de chantier &amp; BTP",
        "description": "Suivi ponctuel ou régulier avec photos et vidéo.",
        "base": 450,
        "suffixe": " / passage",
        "duree": False,
    },
]

# Supplément de durée — ne s'applique qu'aux prestations marquées `duree`.
# 0 € : la durée est déjà comprise dans le prix de la prestation. None : sur devis.
DUREES = [
    ("2h",   "2 heures ou moins",       0),
    ("3h",   "3 heures",                0),
    ("demi", "Demi-journée — 4 heures", 0),
    ("jour", "Journée complète",        400),
    ("plus", "Plus d’une journée",      None),
]

COMPLEXITES = [
    ("simple",   "Zone dégagée, hors agglomération",          0.0),
    ("modere",   "Zone périurbaine, proximité d’habitations", 0.10),
    ("complexe", "Centre-ville ou espace aérien contrôlé",    0.20),
]

OPTIONS = [
    ("verticale", "Version verticale 9:16 pour mobile", 60, None),
    ("pub",       "Utilisation publicitaire étendue (TV, cinéma, campagne nationale)", None, "devis"),
    ("droits",    "Cession de droits d’exploitation étendue (fichiers vidéo bruts)",   None, "devis"),
]

# Prestations pour lesquelles l'usage publicitaire étendu est systématique.
OPTIONS_IMPOSEES = {
    "pub": {
        "prestations": ["tourisme", "commerces"],
        "explication": "Une diffusion en TV, cinéma ou campagne nationale implique une "
                       "utilisation commerciale plus large du contenu. Ce supplément couvre "
                       "donc cette exploitation publicitaire étendue.",
    },
}

# Déplacement : distance routière réelle depuis le centre de Montpellier, aller simple.
SEUIL_KM = 30
PRIX_KM = 0.40
ALLER_RETOUR = False
DEPART = {"lon": 3.8800, "lat": 43.6083, "libelle": "Place de la Comédie, Montpellier"}
DEPARTEMENT = "34"          # hors de ce département, le déplacement est fixé au cas par cas

INCLUS = ["Assurance RC Pro", "Repérage terrain", "Support post-livraison"]

# ---------------------------------------------------------------------------
# Envoi de la demande de devis.
# Renseigner CLE_FORMULAIRE avec la clé Web3Forms (https://web3forms.com) :
# une adresse e-mail suffit, la clé arrive par retour de mail.
# Tant qu'elle est vide, le bouton bascule sur un e-mail pré-rempli.
# ---------------------------------------------------------------------------
FORMULAIRE = {
    "endpoint": "https://api.web3forms.com/submit",
    "cle": "366edba0-fc9f-4cc2-bb08-3f7f524e9c53",
}

# ---------------------------------------------------------------------------
# Calcul d'itinéraire (distance de déplacement).
# Par défaut : OSRM (router.project-osrm.org), démo publique gratuite et sans
# clé — fonctionne tel quel, mais n'est pas prévue pour un trafic soutenu.
# Renseigner ROUTAGE["cle"] avec une clé openrouteservice.org (gratuite,
# 2000 requêtes/jour, inscription en 2 minutes) fait basculer automatiquement
# le calcul dessus, sans autre changement. Tant qu'elle est vide, OSRM reste
# utilisé — le site fonctionne dans les deux cas.
# ---------------------------------------------------------------------------
ROUTAGE = {
    "cle": "",
}

TYPES_CLIENT = [
    ("particulier",  "Particulier"),
    ("agence",       "Agence immobilière"),
    ("entreprise",   "Entreprise"),
    ("collectivite", "Collectivité"),
    ("association",  "Association"),
]


def prix_plancher(prestation):
    """Prix « à partir de » affiché dans la grille."""
    if "formules" in prestation:
        return min(f[2] for f in prestation["formules"])
    return prestation["base"]


def config_json():
    import json
    prestations = {}
    for p in PRESTATIONS:
        entree = {"duree": p["duree"], "titre": p["titre"]}
        if "formules" in p:
            entree["formules"] = [
                {"cle": f[0], "libelle": f[1], "prix": f[2],
                 "apartir": len(f) > 3 and f[3] == "apartir"}
                for f in p["formules"]
            ]
        else:
            entree["base"] = p["base"]
        prestations[p["cle"]] = entree

    return json.dumps({
        "prestations": prestations,
        "durees": {cle: sup for cle, _, sup in DUREES},
        "complexites": {cle: coef for cle, _, coef in COMPLEXITES},
        "options": {cle: {"prix": prix, "type": typ} for cle, _, prix, typ in OPTIONS},
        "optionsImposees": {
            cle: v["prestations"] for cle, v in OPTIONS_IMPOSEES.items()
        },
        "seuilKm": SEUIL_KM,
        "prixKm": PRIX_KM,
        "allerRetour": ALLER_RETOUR,
        "depart": DEPART,
        "departement": DEPARTEMENT,
        "formulaire": FORMULAIRE,
        "routage": ROUTAGE,
    }, ensure_ascii=False, separators=(",", ":"))
