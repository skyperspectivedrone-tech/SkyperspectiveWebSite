#!/bin/zsh
# Montages vidéo de la page Prestations — un plan = "<source>:<debut>-<fin>" (secondes).
# Pour retoucher un montage : modifier ses plans ici, relancer ce script, puis python3 build.py.
# Sources : dossier Téléchargements (jamais dans le dépôt).
# Durée d'un plan : 1,5 à 2 s (décision validée). Plusieurs bornes sont calées pour
# s'arrêter avant une coupe ou un fondu de la vidéo source.
#
#     _build/montages_prestations.sh            # tous les montages
#     _build/montages_prestations.sh sport      # un seul
set -e
cd "$(dirname "$0")/.."
D=~/Downloads
V() { swift -suppress-warnings _build/video_prestation.swift "$@"; }
voulu() { [[ ${#ARGS} -eq 0 || " ${ARGS[*]} " == *" $1 "* ]]; }
ARGS=("$@")

# Sport : poursuites vues de derrière, puis plans vus du dessus.
if voulu sport; then
  F="$D/por floflo.mov"; T="$D/video voiture 3.mp4"; R="$D/video drift 2.MOV"
  C="$D/video voiture .mp4"; G="$D/video voiture 2.mp4"
  V sport "$F:23.6-25.3" "$T:24.1-25.8" "$R:13.0-14.7" "$F:31.6-33.3" \
          "$T:28.6-30.3" "$R:16.6-18.3" "$F:26.0-27.6" "$F:40.4-42.0" \
          "$R:8.0-9.8" "$C:16.0-17.8" "$R:20.5-22.3" "$G:17.2-19.0"
fi

# Commerces & restaurants : Les Voûtes, du titre sur la Saône jusqu'à la salle voûtée.
if voulu commerces; then
  L="$D/Visite des voutes Caluire v02.MOV"
  V commerces "$L:1.8-3.6" "$L:6.6-8.3" "$L:9.0-10.7" "$L:23.6-25.3" "$L:37.5-39.2" \
              "$L:42.1-43.8" "$L:51.6-53.3" "$L:54.6-56.3" "$L:57.4-59.1" "$L:61.6-63.4"
fi

# Immobilier : deux biens entremêlés, un plan sur deux — la maison (approche aérienne,
# traversée intérieure, piscine) et la villa de Bali (portail, piscine, pavillon, jardin).
# Villa : le plan de la maison éclairée s'arrête à 13,2 s, un fondu commence juste après.
if voulu immobilier; then
  M="$D/fanny gavalda immobilier.mp4"; H="$D/portfolio/house.mov"
  V immobilier "$M:0.2-1.8" "$H:0.3-1.9" "$M:3.0-4.6" "$H:11.6-13.2" "$M:4.9-6.5" \
               "$H:15.6-17.2" "$M:7.0-8.6" "$H:26.0-27.6" "$M:13.0-14.6" "$H:38.0-39.6" \
               "$M:24.4-26.0" "$H:46.0-47.6" "$M:28.5-30.1" "$H:51.0-52.6" "$M:47.6-49.4" \
               "$H:60.0-62.0"
fi

# Tourisme : Bali et Les Carroz d'Arâches entremêlés — piscines et rizières, sommets,
# forêt et village, jusqu'au coucher de soleil. Le titre incrusté (6 à 10 s) est évité.
if voulu tourisme; then
  B="$D/portfolio/bali.mov"; C="$D/portfolio/LES CARROZ D'ARÂCHES.mp4"
  V tourisme "$B:0.3-2.0" "$C:27.5-29.2" "$B:4.2-5.9" "$C:33.6-35.3" "$B:18.2-19.9" \
             "$C:18.5-20.2" "$B:12.0-13.7" "$C:54.5-56.2" "$B:24.0-25.7" "$C:45.5-47.2" \
             "$B:33.5-35.2" "$C:92.0-93.7" "$C:134.0-135.7" "$C:141.0-142.6"
fi
