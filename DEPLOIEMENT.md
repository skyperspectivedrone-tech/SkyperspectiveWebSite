# Déploiement — Sky Perspective

Guide pas à pas pour publier le site. Suivez les étapes dans l'ordre : chacune
dépend de la précédente.

## Comment le projet est organisé

- `_build/*.py` et `build.py` — le code source qui génère le site. C'est ça que
  vous éditez (textes, prix, options de configuration).
- `site/assets/` — CSS, JS, images, séquences vidéo. Écrit à la main, jamais
  regénéré automatiquement.
- `site/*.html` — les pages générées. Elles ne sont **pas** dans le dépôt Git
  (voir `.gitignore`) : GitHub les reconstruit à chaque mise en ligne à partir
  de `_build/`. Vous n'avez jamais à y toucher directement.
- `.github/workflows/deploy.yml` — la recette qui dit à GitHub : « à chaque
  `git push` sur `main`, lance `python3 build.py` puis mets `site/` en ligne ».

Concrètement : vous modifiez le contenu dans `_build/`, vous poussez, et le
site public se met à jour tout seul en une ou deux minutes — sans jamais
avoir besoin de régénérer `site/*.html` vous-même avant de pousser.

---

## Étape 1 — Créer le dépôt GitHub

1. Sur [github.com](https://github.com), créez un nouveau dépôt (bouton vert
   **New**). Nom libre, par exemple `sky-perspective-site`.
2. Laissez-le **public** — un dépôt privé demande un abonnement GitHub Pro
   pour publier des pages ; en public, GitHub Pages est gratuit. Rien de
   sensible n'y est exposé : les clés Web3Forms et openrouteservice (étape 5)
   sont par nature visibles côté visiteur, comme sur n'importe quel site
   statique — c'est normal, elles ne donnent accès à rien d'autre qu'à
   recevoir des messages ou calculer un itinéraire.
3. Ne cochez aucune case d'initialisation (pas de README, pas de licence) : le
   dossier en contient déjà.

## Étape 2 — Envoyer le projet sur GitHub

Dans ce dossier (`WebSite/`), une fois le dépôt créé sur GitHub :

```bash
git remote add origin https://github.com/<votre-compte>/<nom-du-depot>.git
git branch -M main
git push -u origin main
```

Le premier `git init` et les premiers commits ont déjà été faits localement —
cette commande envoie tout ce qui existe déjà sur cette machine.

## Étape 3 — Activer GitHub Pages

1. Sur la page du dépôt GitHub → **Settings** → **Pages** (menu de gauche).
2. Sous **Build and deployment** → **Source**, choisissez **GitHub Actions**
   (pas « Deploy from a branch »).
3. Retournez dans l'onglet **Actions** du dépôt : le premier déploiement se
   lance automatiquement après le push. Comptez 1 à 2 minutes. Une fois la
   coche verte affichée, votre site est en ligne sur
   `https://<votre-compte>.github.io/<nom-du-depot>/`.
4. Ouvrez cette adresse et vérifiez que tout s'affiche correctement (menu,
   images, vidéos) avant de continuer.

À ce stade le site est **public et fonctionnel**, avec un nom d'adresse
provisoire en `github.io`. Les étapes suivantes sont des réglages
complémentaires — rien n'empêche de les faire plus tard, mais mieux vaut ne
pas les oublier.

---

## Étape 4 — Nom de domaine personnalisé (optionnel mais recommandé)

Le fichier `site/CNAME` contient déjà `skyperspective.fr` — c'est le domaine
prévu dans le projet. **Vérifiez d'abord qu'il est toujours libre** avant de
l'acheter (les noms en `.fr` partent vite).

### Où acheter

N'importe quel registrar sérieux convient ; pour un `.fr`, les plus courants :

- **OVHcloud** (ovhcloud.com) — français, référence historique pour le `.fr`.
- **Gandi.net** — français aussi, interface simple, pas de vente forcée
  d'options.
- **Namecheap** (namecheap.com) — anglophone, souvent moins cher, fonctionne
  très bien pour un `.fr` également.

Comptez 8 à 15 € par an pour un `.fr`. Achetez uniquement le nom de domaine —
aucun hébergement n'est nécessaire, GitHub Pages s'en charge gratuitement.

### Si le nom choisi est différent

Si `skyperspective.fr` n'est plus disponible et que vous achetez autre chose,
remplacez le contenu de `site/CNAME` par le nouveau nom (une seule ligne,
sans `http://` ni `www.`), puis commitez et poussez.

### Configuration DNS

**Chez votre registrar**, dans la gestion des enregistrements DNS du domaine,
ajoutez :

| Type  | Nom / hôte      | Valeur                                                    |
|-------|-----------------|------------------------------------------------------------|
| A     | @ (racine)      | 185.199.108.153                                             |
| A     | @ (racine)      | 185.199.109.153                                             |
| A     | @ (racine)      | 185.199.110.153                                             |
| A     | @ (racine)      | 185.199.111.153                                             |
| CNAME | www             | `<votre-compte>.github.io`                                  |

(Adresses IP officielles de GitHub Pages — elles ne changent pas, à copier
telles quelles.)

**Sur GitHub**, Settings → Pages → **Custom domain** : saisissez le même nom
de domaine, validez. Une fois les DNS propagés (de quelques minutes à
48 h — souvent moins d'une heure en pratique), cochez **Enforce HTTPS** :
GitHub génère le certificat SSL tout seul, gratuitement.

⚠️ Le nom dans `site/CNAME` et celui saisi dans Settings → Pages doivent être
**identiques**, sinon GitHub écrase l'un avec l'autre au déploiement suivant.

---

## Étape 5 — Faire fonctionner le calcul de déplacement en ligne

La page Tarifs calcule le trajet routier réel entre Montpellier et l'adresse
saisie par le visiteur, pour ajouter les frais de déplacement au devis. Deux
services externes gratuits s'en chargent, et **aucun des deux n'exige de
compte pour que le site fonctionne dès la mise en ligne** :

- **Géocodage de l'adresse** (transformer le texte tapé en coordonnées) :
  l'API Adresse du gouvernement français. Gratuite, sans clé, aucune action
  requise.
- **Calcul du trajet routier** (la distance réelle par la route) : par défaut
  OSRM, un serveur de démonstration public — gratuit, sans clé, et qui
  fonctionne très bien pour un site avec peu de visites. Sa seule limite :
  ce n'est pas un service prévu pour absorber beaucoup de trafic soutenu, et
  rien ne garantit sa disponibilité à long terme.

**Le site est donc utilisable tel quel dès la publication**, calcul de
déplacement compris. La suite de cette étape est une amélioration à faire
quand vous en avez le temps, pas un blocage avant mise en ligne.

### Passer sur un service avec quota garanti

Pour plus de robustesse, openrouteservice.org offre un plan gratuit
(2000 requêtes par jour, largement suffisant) avec une clé personnelle :

1. Allez sur [openrouteservice.org](https://openrouteservice.org), cliquez sur
   **Sign in** puis **Sign up** et créez un compte (e-mail + mot de passe,
   gratuit).
2. Une fois connecté, vous arrivez sur votre tableau de bord (« Dashboard »).
   Cherchez un bouton du type **Request a token** / **Create token**, choisissez
   le plan **Free** — l'intitulé exact peut varier légèrement selon les mises
   à jour du site, mais l'idée est toujours « créer une clé API gratuite ».
   Un jeton (clé) est généré immédiatement, sous forme d'une longue chaîne de
   caractères.
3. Copiez cette clé.
4. Ouvrez `_build/tarifs_config.py` dans ce dossier, cherchez ce bloc vers la
   fin du fichier :

   ```python
   ROUTAGE = {
       "cle": "",
   }
   ```

   et collez votre clé entre les guillemets :

   ```python
   ROUTAGE = {
       "cle": "votre-cle-openrouteservice-ici",
   }
   ```
5. Enregistrez, puis :

   ```bash
   git add _build/tarifs_config.py
   git commit -m "Active openrouteservice pour le calcul de déplacement"
   git push
   ```

Le calculateur bascule automatiquement sur ce service dès que la clé est
renseignée — aucun autre changement n'est nécessaire. Tant qu'elle reste
vide, le site continue de fonctionner avec OSRM exactement comme avant.

### Vérifier que ça marche une fois en ligne

Une fois le site publié (étape 3), allez sur `/tarifs.html#devis`, choisissez
n'importe quelle prestation, avancez jusqu'à l'étape « Adresse du lieu de
tournage », tapez une adresse à plus de 30 km de Montpellier (ex. « Nîmes »
ou « Béziers ») et sélectionnez une suggestion. Le champ « Déplacement » du
récapitulatif doit afficher une distance en kilomètres et un montant en
euros, et ce montant doit se retrouver dans le total en bas. C'est exactement
ce qui a été testé en local avant cette publication.

---

## Étape 6 — Vérifier la réception des demandes (Web3Forms)

Le formulaire de contact et le calculateur de devis envoient réellement les
demandes par e-mail via Web3Forms — la clé est déjà configurée, rien à faire
côté technique. Un seul point d'attention :

⚠️ **Gmail classe parfois ces e-mails en indésirables.** Dès la première
demande reçue (ou en vous envoyant un test depuis le site), pensez à :
1. Marquer le message comme non-spam.
2. Ajouter `notify@web3forms.com` à vos contacts.
3. Créer un filtre Gmail « ne jamais envoyer aux spams » pour cet expéditeur.

---

## Étape 7 — Modifier le site après publication

En local, sur cette machine, pour prévisualiser avant de pousser :

```bash
python3 build.py     # régénère site/*.html à partir de _build/
python3 serve.py      # prévisualisation sur http://localhost:4321
```

Modifiez les textes, prix ou images dans `_build/*.py` (ou les fichiers dans
`site/assets/` pour le CSS, le JS ou les visuels), vérifiez en local, puis :

```bash
git add -A
git commit -m "Description du changement"
git push
```

GitHub Actions reconstruit et republie automatiquement — pas besoin de
regénérer `site/*.html` vous-même avant de pousser, l'usine s'en charge.
Comptez une à deux minutes entre le `push` et la mise à jour visible en ligne.

---

## Points d'attention déjà connus (voir CLAUDE.md)

- La séquence Avata 2 (page Matériel) ne compte que 35 images ; un ré-export
  plus fourni est prévu pour un mouvement plus fluide.
- L'adresse postale complète (obligatoire en mentions légales pour une
  entreprise individuelle) reste à ajouter.
