# Déploiement — Sky Perspective

## Comment le projet est organisé

- `_build/*.py` et `build.py` — le code source qui génère le site. C'est ça que
  vous éditez.
- `site/assets/` — CSS, JS, images, séquences vidéo. Écrit à la main, jamais
  regénéré automatiquement.
- `site/*.html` — les pages générées. Elles ne sont **pas** dans le dépôt Git
  (voir `.gitignore`) : GitHub les reconstruit à chaque mise en ligne à partir
  de `_build/`. Vous n'avez jamais à y toucher directement.
- `.github/workflows/deploy.yml` — la recette qui dit à GitHub : « à chaque
  `git push`, lance `python3 build.py` puis mets `site/` en ligne ».

Concrètement : vous modifiez le contenu dans `_build/`, vous poussez, et le
site public se met à jour tout seul en une ou deux minutes.

## 1. Créer le dépôt GitHub

1. Sur [github.com](https://github.com), créez un nouveau dépôt (bouton vert
   **New**). Nom libre, par exemple `sky-perspective-site`.
2. Laissez-le **public** — un dépôt privé demande un abonnement GitHub Pro pour
   publier des pages ; en public, GitHub Pages est gratuit. Rien de sensible
   n'y est exposé : la clé Web3Forms est déjà visible côté visiteur sur la page
   Tarifs, c'est normal pour ce service (elle sert uniquement à recevoir des
   messages, pas à autoriser autre chose).
3. Ne cochez aucune case d'initialisation (pas de README, pas de licence) : le
   dossier en contient déjà.

## 2. Envoyer le projet

Dans ce dossier (`WebSite/`), une fois le dépôt créé sur GitHub :

```bash
git remote add origin https://github.com/<votre-compte>/<nom-du-depot>.git
git branch -M main
git push -u origin main
```

Le premier `git init` et le premier commit ont déjà été faits localement.

## 3. Activer GitHub Pages

1. Sur la page du dépôt GitHub → **Settings** → **Pages** (menu de gauche).
2. Sous **Build and deployment** → **Source**, choisissez **GitHub Actions**
   (pas « Deploy from a branch »).
3. Retournez dans l'onglet **Actions** du dépôt : le premier déploiement se
   lance automatiquement après le push. Une fois vert, votre site est en ligne
   sur `https://<votre-compte>.github.io/<nom-du-depot>/`.

## 4. Nom de domaine personnalisé

Une fois votre domaine acheté (ex. chez OVH, Gandi, Namecheap…) :

**Chez votre registrar**, ajoutez ces enregistrements DNS :

| Type  | Nom / hôte      | Valeur                                                    |
|-------|-----------------|------------------------------------------------------------|
| A     | @ (racine)      | 185.199.108.153                                             |
| A     | @ (racine)      | 185.199.109.153                                             |
| A     | @ (racine)      | 185.199.110.153                                             |
| A     | @ (racine)      | 185.199.111.153                                             |
| CNAME | www             | `<votre-compte>.github.io`                                  |

(Adresses IP officielles de GitHub Pages — elles ne changent pas.)

**Dans le dépôt**, le fichier `site/CNAME` contient déjà `skyperspective.fr`.
Si vous achetez un autre nom de domaine, remplacez son contenu par le vôtre
(une seule ligne, sans `http://` ni `www.`), commitez et poussez.

**Sur GitHub**, Settings → Pages → **Custom domain** : saisissez le même nom
de domaine, validez. Une fois les DNS propagés (de quelques minutes à
48 h), cochez **Enforce HTTPS** — GitHub génère le certificat SSL tout seul.

⚠️ Le nom dans `site/CNAME` et celui saisi dans Settings → Pages doivent être
**identiques**, sinon GitHub écrase l'un avec l'autre au déploiement suivant.

## 5. Éditer le site plus tard

En local, sur cette machine :

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

## Points d'attention déjà connus (voir CLAUDE.md)

- La clé Web3Forms est active : les demandes de devis et messages de contact
  partent réellement. Gmail les classe parfois en indésirables — pensez à
  marquer `notify@web3forms.com` comme non-spam.
- La séquence Avata 2 (page Matériel) ne compte que 35 images ; un ré-export
  plus fourni est prévu.
- L'adresse postale complète (obligatoire en mentions légales pour une
  entreprise individuelle) reste à ajouter.
