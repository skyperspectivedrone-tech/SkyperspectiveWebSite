# Sky Perspective — Site web

Site vitrine de **Sky Perspective**, télépilote de drone cinématographique (auto-entrepreneur).
Objectif n°1 : **montrer les possibilités de prise de vue** en opposant deux écritures —
le drone stabilisé (DJI Air 3S) et le drone FPV (DJI Avata 2).
Objectif n°2 : générer des demandes de devis qualifiées via un **calculateur en ligne**.

## Identité de l'entreprise

- Raison sociale : **Sky Perspective**
- Statut : auto-entrepreneur
- SIRET : **10863047600019**
- Base : **Montpellier (34)** — interventions dans toute la France
- Contact affiché : **skyperspectivedrone@gmail.com** · **06 47 00 65 41** — réponse sous 24 h
- Domaine cible : `skyperspective.fr`

## Le pilote

Max — 25 ans, diplômé en effets spéciaux (VFX). Sensibilité cinématique et minimaliste.
Modélise, texture et rend en 3D (Maya + Substance Painter). Les rendus 3D des drones
sont produits par lui : c'est un différenciateur, il doit se voir sur le site.

## Matériel réel

- **DJI Air 3S** — stabilisé. Double focale : grand-angle **24 mm** et téléobjectif **70 mm**
  (visibles gravés « E24 / E70 » sur le rendu 3D). C'est l'argument de la page Matériel :
  le choix de focale, pas seulement le vol.
- **DJI Avata 2** — FPV, immersif, vol en intérieur (protections d'hélices orange).

⚠️ Ne jamais écrire « Mavic 3 » : le drone stabilisé est un **Air 3S**.
Le fichier `../Model3d/mavic3.mb` porte un nom trompeur.

## Cibles

Agences immobilières · Commerces & restaurants · Sport mécanique ·
Suivi de chantier (seule prestation récurrente) · Tourisme & patrimoine ·
Modélisation 3D & photogrammétrie.

## Identité de marque

| Rôle | Hex |
|---|---|
| Fond principal (bleu marine très sombre) | `#0A1424` |
| Accent / CTA / trait signature | `#D62828` |
| Texte secondaire, séparateurs | `#E6E6E6` |
| Texte principal | `#FFFFFF` |

- **Fond ambiant animé** (`fond_anime()` dans `layout.py`, styles `.fond`) : le marine uni
  est remplacé par quatre nappes radiales très étalées, en dérive lente (34 à 46 s, alternée).
  Trois nappes bleues, plus **une nappe chaude ambrée en bas** qui réchauffe le pied des pages.
  Saturations basses et opacités faibles (0,30 à 0,50) : on cherche une atmosphère, pas un
  aplat coloré. Ne pas monter en saturation — la demande explicite est « pas agressive,
  professionnel, ni pop art ni enfantin ».
  L'**entrée progressive** (`.fond--apparition`, 1,7 s) ne joue **que sur l'accueil** ; les
  autres pages affichent le dégradé sans animation d'apparition. Dans la maquette, l'entrée
  ne se déclenche que si l'on arrive directement sur `#accueil`.
  Le pied de page est passé en fond translucide pour laisser passer la nappe chaude.
- **Typographie : Montserrat**, titres en majuscules, letter-spacing large (comme le logo).
- Le rouge est le **système d'accent** : boutons CTA, puces de listes, numéros de section,
  accroches sous les titres, filets de séparation. Jamais en aplat large ni en fond de bloc.
- Motifs de fond (décision validée) :
  - **Lignes de perspective en éventail** du logo → matériel, prestations, tarifs,
    contact. Motif dominant du site.
  - **Photo du hero d'accueil** : `photo-alpes.png` (2,1 Mo, prise au drone par Max),
    compressée en `site/assets/img/hero-alpes.jpg` — 1600 × 900, 271 Ko.
    Regénérer après tout changement de la source :

        sips -s format jpeg -s formatOptions 76 -Z 1600 photo-alpes.png \
             --out site/assets/img/hero-alpes.jpg

    Cadrage `object-position: 62% 40%` pour garder le sommet et le soleil. Deux voiles
    superposés assurent la lisibilité du texte à gauche et le raccord avec l'en-tête et
    la suite de la page ; sur mobile le voile passe en vertical.
    Le décor de crêtes dessiné en SVG qui tenait lieu de provisoire a été supprimé.
  - **Détourages produit** : `site/assets/img/air3s.png` et `avata2.webp`, posés sur les deux
    blocs drone de l'accueil (`.service__media--produit`). Ils flottent sur le fond, sans
    cadre, avec une ombre portée — sans elle ils semblent collés. Les deux formats diffèrent :
    une scène de hauteur commune les recentre pour éviter un bloc deux fois plus haut.
    Le visuel officiel de l'Avata est bien plus lumineux que celui de l'Air 3S
    (luminance moyenne 85 contre 56) : il porte `.est-eclairci`, qui applique
    `brightness(0.66)` **avant** l'ombre portée, sinon l'ombre s'éclaircit aussi.
    Mesurer plutôt que régler à l'œil quand deux visuels doivent s'accorder.
    `_build/rogner_png.py` rogne les marges transparentes d'un PNG sans dépendance
    (l'Air 3S est passé de 900 × 900 à 900 × 296) :

        cd _build && python3 rogner_png.py <source.png> <destination.png>
  - **Courbes topographiques** discrètes → suivi de chantier, immobilier.
    La page Tarifs utilise l'éventail sur **toute la hauteur de page** (`page-pattern`),
    pas seulement le hero.
  - Opacité ≤ 6 %, jamais les deux motifs sur une même page.
- Valeurs : précision, sécurité, perspective, rigueur.

Fichiers logo :
- `Logo_Official.png` — logo complet 8180×1437, **transparent mais artwork bleu marine** :
  réservé aux fonds clairs (carte de visite, devis, factures).
- `site/assets/img/logo-blanc.png` — déclinaison blanche avec trait rouge conservé, générée
  par `_build/recolor_logo.py` (décodage/réencodage PNG en Python pur, sans dépendance).
  **C'est la version utilisée sur le site**, en-tête et pied de page.
  Régénérer après toute modification du logo source :

      sips -Z 1600 Logo_Official.png --out /tmp/logo_src.png
      python3 _build/recolor_logo.py /tmp/logo_src.png site/assets/img/logo-blanc.png

- `Logo_Official` (PDF), `Exemple usage logo.png` (planche de charte).
- `Logo/Edition_logo_svg.svg` — vectoriel mais lettrage en texte vivant « Briller-Light »,
  police absente des navigateurs. Inutilisable tel quel ; le PNG blanc le remplace.

## Règles de contenu

- Ton professionnel mais accessible. Phrases courtes, pas de jargon inutile.
- **Jamais de lorem ipsum** — contenu réaliste en français.
- Ne jamais présenter une vidéo de banque d'images comme une réalisation Sky Perspective.
- Franchise en base de TVA. La mention « TVA non applicable, art. 293 B du CGI » figure
  **sur les devis et factures uniquement**, plus dans le pied de page (décision validée) ;
  elle reste rédigée en toutes lettres dans la page Mentions légales.
  Ne pas afficher « HT » seul dans les tarifs, qui laisse croire qu'une TVA s'ajoutera.

## Règles techniques

Le site est en **HTML et CSS écrits à la main**, destinés à Astro. Ni React, ni Tailwind,
ni TypeScript. Décliner les composants tiers qui les exigent (shadcn et assimilés) et
reproduire le rendu nativement : une dépendance de ce poids ne se justifie pas pour un
bloc d'interface, et imposerait de réécrire le reste du site pour rester cohérent.

- **Mobile-first**, responsive sur tous les écrans.
- Performance prioritaire (site vidéo) :
  - vidéo hero < 3 Mo, muette, sans piste audio, avec `poster` ;
  - sur mobile : image fixe au lieu de la vidéo hero ;
  - jamais plus d'une vidéo en autoplay par écran visible.
- Respecter `prefers-reduced-motion` sur toutes les animations.
- Accessibilité : contrastes AA minimum, alternatives textuelles, navigation clavier.

## Stack (décision validée)

- **Astro**, sortie 100 % statique.
- Hébergement : **GitHub Pages**, déploiement par GitHub Actions à chaque push.
- Contraintes : dépôt < 1 Go, aucun fichier > 100 Mo.
  - **Ne jamais committer les PNG 4K sources ni les zips.** Ils restent hors dépôt.
  - Seuls les dérivés web (WebP redimensionnés, MP4 compressés) entrent dans le dépôt.
  - Vidéos de réalisations : YouTube/Vimeo non répertorié, lite-embed au clic.
- Pages sur dépôt privé = compte GitHub Pro requis, sinon dépôt public.
- Domaine branché via un fichier `CNAME`.

## Arborescence (décision validée)

```
/                    Accueil
/prestations         Page unique — les 6 prestations en blocs alternés
/materiel            ★ section scroll 3D + cadre légal
/tarifs              ★ grille + calculateur de devis
/contact
/mentions-legales  /confidentialite
```

Navigation : **ACCUEIL · PRESTATIONS · TARIFS · MATÉRIEL · CONTACT** + bouton
**DEVIS GRATUIT** encadré à droite.

**Pas de page Réalisations en V1** : aucun lien mort, aucune mention « bientôt disponible ».
Elle sera créée après les premiers tournages réels.

## Page Prestations

Référence de structure : `exemples/exemple page prestation .png` — à suivre fidèlement.

1. **Hero** — filet rouge + surtitre « NOS PRESTATIONS DRONE », H1 sur deux lignes,
   paragraphe de positionnement, deux boutons (rouge plein « Demander un devis » +
   contour « Me contacter »), visuel aérien à droite en fondu vers le fond.
2. **Six blocs prestations**, image et texte **alternés gauche/droite**. Chaque bloc :
   numéro en rouge · titre en capitales · accroche courte en rouge · paragraphe ·
   colonne « Livrables inclus » à puces rouges · bouton CTA.
   Ordre et numérotation : 01 Immobilier & propriété · 02 Commerces & restaurants ·
   03 Sport & suivi de véhicule · 04 Scans 3D & photogrammétrie ·
   05 Suivi de chantier & BTP · 06 Tourisme, patrimoine & communication.
   ⚠️ La maquette inverse 05 et 06 : corriger pour que la numérotation suive l'ordre d'affichage.
3. **Déroulé d'une prestation** (`.deroule`, données dans `DEROULE`) : six jalons exprimés
   en pourcentage d'avancement, reliés par un fil rouge — prise de contact 10 %, repérage
   25 %, tournage 50 %, post-production 80 %, livraison 99 %, suivi après livraison 100 %.
   Seul le 99 % de la livraison vient de l'utilisateur ; les autres valeurs sont à valider.
   Le fil passe à la verticale sous 620 px.
4. **Bandeau réassurance**, cinq items à icône : Télépilote certifié · Conformité européenne ·
   Assurance RC Pro · Créativité & exigence · Intervention France.
5. **CTA final** « PARLONS DE VOTRE PROJET » + bouton rouge fléché.

Les libellés de prestations doivent être **identiques** entre `/prestations` et `/tarifs`.
Nommage retenu : « Scans 3D & photogrammétrie » et « Suivi de chantier & BTP ».

Les visuels d'illustration ne sont pas des réalisations : aucune légende, aucun nom de client,
aucune formulation laissant croire qu'ils ont été tournés par Sky Perspective.
Ils sont remplacés par de vraies images au fil des tournages.

## Page Matériel

**Pas de hero d'accueil** (décision validée) : la page s'ouvre directement sur le premier
reveal. Ordre : **DJI Air 3S**, puis **DJI Avata 2** en dessous, puis le bloc « Montage »
en attente et le cadre légal.

Chaque reveal fait `100vh + --course`, où `--course` est **calée sur le nombre d'images**
(~8 px par image, plancher 420 px) : 648 px pour l'Air 3S et ses 81 images, 420 px pour
l'Avata 2 et ses 35. Le défilement doit rester court — quelques crans de molette par
séquence, pas des dizaines. La section contient un `<canvas>` collé à l'écran :
la position de défilement détermine l'image affichée dans la séquence, et fait défiler
trois légendes calées sur le mouvement. Le remplissage est de type « cover » (jamais de
bande vide), un dégradé latéral garantit la lisibilité du texte, et des repères 01/02/03
indiquent la progression.

Le mouvement n'est **pas un turntable** : c'est un **reveal** — le drone émerge du noir,
jusqu'au gros plan final sur les objectifs, qui sert d'ancrage au discours sur le choix
de focale (24 mm / 70 mm, gravés « E24 / E70 » sur le rendu).

Moteur : `site/assets/js/reveal.js`. Points sensibles déjà traités :
- pas de scrub sur `<video>` (saccadé sur iOS, dépendant des images-clés) ;
- `requestAnimationFrame` est gelé quand le document est masqué (onglet en arrière-plan,
  panneau intégré) : le rendu bascule alors en synchrone, sinon le canvas reste noir ;
- préchargement progressif des images voisines pour éviter les trous au défilement.
  ⚠️ **Toute image chargée doit porter un `onload` qui relance le rendu**, préchargée ou non.
  Sans cela, une image encore en cours de décodage au moment où le rendu la réclame est
  abandonnée, et plus rien ne redessine tant que le visiteur ne rescrolle pas : canvas noir.
  C'est le bug qui a fait passer l'effet pour non fonctionnel ;
- `prefers-reduced-motion` : la section devient statique, légendes empilées ;
- le canvas est dimensionné à zéro tant que sa page est masquée (maquette à navigation
  interne) : le rendu se redéclenche dès que la taille redevient valide, sinon l'image
  n'apparaît jamais.

### Raccords de la page Matériel

Toute la zone de reveal repose sur du **noir pur** (`.reveal { background: #000 }`) et non
sur le marine : les rendus sont sur fond noir, et toute couleur intermédiaire créait une
couture visible entre les sections. Le voile de lisibilité est lui aussi basé sur du noir.

Trois fondus assurent la continuité :
- `.reveal__vignette--haut` (première séquence seulement) : marine → transparent, se marie
  avec l'en-tête ;
- `.reveal__vignette--bas` (chaque séquence) : transparent → noir, garantit que le bas de
  chaque section est noir pur quelle que soit l'image affichée ;
- `.transition-noir-bleu` : noir → marine sur 34 vh, seul retour à la couleur de marque.

⚠️ Ne pas remettre de marine dans cette zone : c'est ce qui produisait la bande claire
coincée entre deux noirs.

### Séquences

Sources 4K dans `Render_air3s.zip` (81 images) et `Render_avata2.zip` (35 images).
Converties en JPEG web par `_build/convert_sequences.sh` (sips sait lire le WebP mais
**pas l'écrire** ; sans transparence sur des rendus sombres, le JPEG est équivalent) :

    _build/convert_sequences.sh <dossier_source> <nom_sequence> [images_a_ignorer]

Commandes réellement utilisées :

    _build/convert_sequences.sh <sources>/Render_air3s  air3s
    _build/convert_sequences.sh <sources>/Render_avata2 avata2 3

**Une séquence doit toujours commencer sur du noir pur** : c'est le principe même du reveal.
Vérifier le poids des premières images — une image nettement plus lourde que les suivantes
trahit du contenu parasite.

Sortie dans `site/assets/media/<nom>/1280/` et `/900/` — 1280 px pour le desktop,
900 px en dessous de 900 px de large. Poids actuel : environ 3,6 Mo + 1,9 Mo.
Les PNG 4K et les zips ne doivent **jamais** entrer dans le dépôt.

Ne pas verrouiller le défilement de la page (`position: fixed` sur le `body` pour capter
la molette) : cela emprisonne le visiteur, casse le clavier et les lecteurs d'écran, et
coûte des visites sur un site commercial. Le `<canvas>` collant obtient le même rendu.

⚠️ **32 images pour l'Avata 2 reste trop peu** : le mouvement sautera au défilement.
Ré-export d'environ 120 images attendu.

## Page Tarifs

Grille publique (prix de départ) :

| Prestation | À partir de |
|---|---|
| Immobilier & propriété | 450 € |
| Commerces & restaurants | 590 € |
| Sport & suivi de véhicule | 850 € |
| Tourisme, patrimoine & communication | 850 € |
| Modélisation 3D & photogrammétrie | 750 € |
| Suivi de chantier | 450 € / passage |

Options :
- Version verticale 9:16 supplémentaire — **+ 60 €**
- Déplacement — inclus jusqu'à 30 km depuis Montpellier, puis **0,60 €/km**
- Zone aérienne complexe (autorisations spécifiques) — **+ 10 à 20 %**
- Utilisation publicitaire étendue (TV, cinéma, campagnes nationales) — sur devis
- Cession des droits d'exploitation étendue (lieu, durée, média) — sur devis

Inclus dans tous les forfaits : assurance RC Pro · repérage terrain · support post-livraison.

Message clé à conserver : **« Une prestation. Deux façons de filmer. »** — le client paie
son projet et son niveau de production, pas le nombre de drones utilisés.

### Calculateur de devis — en place

Barème centralisé dans `_build/tarifs_config.py` : le HTML **et** le JavaScript lisent les
mêmes valeurs (exportées en JSON dans `#devis-config`). Ne jamais dupliquer un prix ailleurs.

    Total = (prix de la prestation + supplément de durée) × (1 + complexité)
            + options fixes + déplacement

**Aucun prix n'apparaît dans les menus** (décision validée) : les montants ne se révèlent
que dans le récapitulatif, ligne par ligne.

**Menus dépendants du type de prestation :**
- *Immobilier & propriété* → menu **Formule** : visite virtuelle 360° bien standard 200 € ·
  villa de prestige 400 € · domaine ou hôtel 1 000 €.
- *Inspection* → menu **Formule** : survol chantier + orthophoto HD 149 € ·
  toiture < 200 m² 49 € · toiture 200–500 m² 119 € · façade ou ouvrage d'art
  **à partir de** 99 €.
- *Sport & suivi de véhicule* → seul type à afficher le menu **Durée estimée**.
- Tous les autres : ni formule ni durée, la durée est comprise dans le prix.

**La durée est un supplément, jamais un prix de remplacement** : moins d'une journée → 0 €
(compris dans la prestation) · journée complète → **+ 400 €** · au-delà → sur devis.
Référence : sport & suivi de véhicule + journée complète = 850 + 400 = **1 250 €**.

**Parcours par étapes** (décision validée) : une seule question à l'écran, le menu disparaît
dès la réponse et laisse place à la suivante. Ordre : prestation → formule → adresse →
complexité → durée → options → écran de fin. Les étapes « formule » et « durée » sont
retirées du parcours quand elles ne s'appliquent pas, et la numérotation se recalcule.
Bouton **Retour** à chaque étape, jauge de progression, avance automatique après un choix.

**Options imposées** : `OPTIONS_IMPOSEES` dans la configuration. L'usage publicitaire étendu
est coché d'office et non décochable pour *Tourisme* et *Commerces & restaurants*, avec la
mention « Inclus pour cette prestation » et une bulle d'explication derrière un point
d'interrogation. Une option cochée automatiquement est relâchée si l'on change de prestation ;
une option cochée par le visiteur est conservée.

**Déplacement — aller simple, 0,40 €/km.** Le visiteur saisit son adresse ; le trajet est
mesuré **par la route**, jamais à vol d'oiseau :
- géocodage par l'**API Adresse** (`api-adresse.data.gouv.fr`) — service public, gratuit,
  sans clé, CORS ouvert ; autocomplétion clavier et souris. La requête porte un **biais de
  proximité** (`&lat=&lon=` sur Montpellier) : sans lui, « place de la mairie » remontait
  des communes de toute la France avant celles de l'Hérault ;
- itinéraire par **OSRM** (`router.project-osrm.org`), variante la plus courte retenue ;
- ≤ 30 km → **Inclus** ; au-delà → **distance × 0,40 €**, aller simple, sans franchise déduite ;
- hors département 34 → **À déterminer**.

⚠️ OSRM est un serveur de démonstration, non prévu pour un usage de production soutenu.
Avant mise en ligne, prévoir un fournisseur avec quota (OpenRouteService, Geoapify).

**Repli sans réseau** : la disponibilité du géocodage est sondée **dès l'arrivée sur l'étape
adresse**, pas au premier caractère saisi. Si l'appel échoue — c'est le cas dans la maquette
Artifact, dont la politique de sécurité interdit tout appel externe — le champ « distance en
km » apparaît immédiatement et le calcul se poursuit à l'identique. Aucune capacité Artifact
ne permet d'appeler une API tierce.

⚠️ **L'étape adresse n'est jamais bloquante.** Elle l'a été, et le visiteur se retrouvait
enfermé : bouton « Continuer » désactivé, aucun champ de secours visible, aucune explication.
Sans adresse, le déplacement affiche « À préciser » et figure dans les réserves sous le total.

Le total reste **toujours chiffré**, sauf s'il n'y a rien à chiffrer du tout : afficher
« 0,00 € » laisserait croire que la prestation est offerte. Les réserves sont listées
sous le total.

### Envoi de la demande — formulaire Web3Forms

Dernière étape du parcours : un formulaire de coordonnées, puis un écran de confirmation.
Champs (décision validée) : prénom, nom, e-mail, téléphone, type de client, raison sociale
si professionnel, date souhaitée, description du projet, **case d'autorisation du
propriétaire des lieux**, consentement RGPD. Les champs obligatoires bloquent le bouton
d'envoi tant qu'ils ne sont pas remplis ; la raison sociale n'apparaît et n'est exigée que
pour un client professionnel. Un piège à robots invisible (`#dv-botcheck`) filtre le spam.

L'e-mail reçu contient les coordonnées **et** le récapitulatif chiffré complet, sans que le
visiteur ait à recopier quoi que ce soit.

⚠️ **`FORMULAIRE["cle"]` est vide** dans `_build/tarifs_config.py`. Y coller la clé Web3Forms
(https://web3forms.com — une adresse e-mail suffit, aucune inscription). Tant qu'elle est
vide, le bouton bascule automatiquement sur un `mailto:` pré-rempli, avec un message
d'explication. Même repli si l'appel réseau échoue.

Requête : `POST` en **`application/json`** — la documentation l'impose pour les appels
JavaScript, le multipart et l'urlencoded sont réservés aux envois de formulaire natifs.
Champs : `access_key`, `subject`, `from_name`, `name`, `email`, `message` ;
réponse `{success, message}`.

Envoi réel vérifié : les messages arrivent bien, mais **Gmail les classe en indésirables**.
Le remède est côté boîte de réception, pas côté code : marquer comme non-spam, ajouter
`notify@web3forms.com` aux contacts, et créer un filtre « ne jamais envoyer aux spams ».
Les essais depuis le site utilisaient l'adresse de Sky Perspective comme adresse du client,
ce qui aggrave le classement — un vrai visiteur écrira depuis une adresse tierce.

La page Confidentialité mentionne Web3Forms comme sous-traitant.

`site/assets/js/devis.js` — chargé uniquement sur la page Tarifs.

## Chaîne de production locale (provisoire)

Node.js et Homebrew ne sont pas installés sur la machine : Astro ne peut pas encore tourner.
En attendant, le site est généré en HTML statique par un mini-build Python, dont la structure
calque déjà celle d'Astro (un gabarit + des pages), pour un portage direct plus tard.

- `_build/layout.py` → gabarit commun (en-tête, pied de page, motifs, icônes) = `Layout.astro`
- `_build/p_prestations.py`, `_build/p_autres.py` → contenu des pages = `src/pages/*.astro`
- `build.py` → génère `site/*.html`
- `serve.py` → serveur statique local sur le port 4321

Régénérer et prévisualiser :

    python3 build.py           # génère site/*.html
    python3 build_artifact.py  # génère maquette.html (fichier unique autonome)
    python3 serve.py           # http://localhost:4321

⚠️ Le processus de prévisualisation n'a pas accès au dossier `Documents` : la copie servie
vit dans le scratchpad de session, synchronisée par `rsync` après chaque build.

Bascule vers Astro dès que Node est installé : le HTML et le CSS se transposent tels quels,
`layout.py` devient `Layout.astro`, chaque fonction de page devient un fichier `.astro`.

## Points en attente

- Adresse postale complète, obligatoire dans les mentions légales pour une entreprise
  individuelle (seule « Montpellier (34) » y figure aujourd'hui).
- Séquences 3D : ré-export d'environ 120 images par drone depuis le logiciel de montage.
  ffmpeg n'est pas nécessaire, `sips` (livré avec macOS) suffit au redimensionnement
  et à la conversion WebP.
- `brew install ffmpeg` pour traiter les séquences 3D.
