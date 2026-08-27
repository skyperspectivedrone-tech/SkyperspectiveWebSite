#!/bin/zsh
# Convertit une séquence de rendus 4K en JPEG web (deux tailles).
# Usage : _build/convert_sequences.sh <dossier_source> <nom_sequence> [images_a_ignorer]
# Le troisième argument écarte des images en tête de séquence : un export contient
# parfois la fin du mouvement précédent, ce qui donne un faux départ à l'écran.
set -e
SRC="$1"; NOM="$2"; IGNORER=${3:-0}
DEST="site/assets/media/$NOM"
rm -rf "$DEST"
mkdir -p "$DEST/1280" "$DEST/900"
i=0; vus=0
for f in "$SRC"/*.png; do
  vus=$((vus+1))
  if [ $vus -le $IGNORER ]; then continue; fi
  i=$((i+1))
  n=$(printf "%04d" $i)
  sips -s format jpeg -s formatOptions 62 -Z 1280 "$f" --out "$DEST/1280/$n.jpg" >/dev/null 2>&1
  sips -s format jpeg -s formatOptions 60 -Z 900  "$f" --out "$DEST/900/$n.jpg"  >/dev/null 2>&1
done
echo "$NOM : $i images retenues sur $vus ($IGNORER ignorée(s) en tête)"
