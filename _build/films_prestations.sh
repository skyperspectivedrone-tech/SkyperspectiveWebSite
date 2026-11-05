#!/bin/zsh
# Films complets de la page Prestations (vignettes cliquables du détail), avec leur son.
# Un film = un identifiant, une source entière et l'instant (s) de son image d'attente.
# Toujours la version AVEC musique : le Critérium existe aussi en « sans musique ».
# Sortie : site/assets/media/films/<id>.mp4, <id>.jpg et <id>-vignette.jpg — 720p, ~3 Mbit/s,
# ~23 Mo par minute (rester sous 100 Mo par fichier : limite GitHub, soit ~4 min de film).
# La liste affichée sur la page (titres, ordre) est dans FILMS, _build/p_prestations.py.
#
#     _build/films_prestations.sh                     # tous les films
#     _build/films_prestations.sh tourisme-bali       # un seul
set -e
cd "$(dirname "$0")/.."
D=~/Downloads; M=~/Documents/Drones/Montage; C=~/"Documents/Societe/Devis/Critérium des Cévennes 2026"
ARGS=("$@")
F() {  # F <id> <instant poster> <source>
  [[ ${#ARGS} -eq 0 || " ${ARGS[*]} " == *" $1 "* ]] || return 0
  swift -suppress-warnings _build/video_prestation.swift --film --poster "$2" "$1" "$3"
  # Vignette 640 px pour la grille du détail ; le poster 1280 px sert à la visionneuse.
  sips -s format jpeg -s formatOptions 72 -Z 640 "site/assets/media/films/$1.jpg" \
       --out "site/assets/media/films/$1-vignette.jpg" >/dev/null
}

F immobilier-villeneuve 3.5  "$D/fanny gavalda immobilier.mp4"
F immobilier-bali       51   "$D/portfolio/house.mov"
F commerces-voutes      24.5 "$D/Visite des voutes Caluire v02.MOV"
F sport-criterium-1     17   "$C/Reseau Part1 (avec musique) .mp4"
F sport-criterium-2     18   "$C/Reseau Part2 (avec musique) .mp4"
F sport-criterium-3     12   "$C/Reseau Part3 (avec musique) .mp4"
F sport-favas           6    "$M/FavasV05.mp4"
F sport-marbil          8.5  "$M/marbilv02_instagram.mov"
F tourisme-bali         5    "$D/portfolio/bali.mov"
F tourisme-carroz       92   "$D/portfolio/LES CARROZ D'ARÂCHES.mp4"
