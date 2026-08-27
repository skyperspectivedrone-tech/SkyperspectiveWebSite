# -*- coding: utf-8 -*-
"""Rogne les marges transparentes d'un PNG RGBA. Sans dépendance externe."""
import sys
from recolor_logo import lire_png, defiltrer, ecrire_png


def rogner(source, destination, seuil=8, marge=6):
    largeur, hauteur, brut = lire_png(source)
    pixels = defiltrer(largeur, hauteur, brut)
    ligne = largeur * 4

    haut, bas, gauche, droite = hauteur, -1, largeur, -1
    for y in range(hauteur):
        base = y * ligne
        for x in range(largeur):
            if pixels[base + x * 4 + 3] > seuil:
                if y < haut: haut = y
                if y > bas: bas = y
                if x < gauche: gauche = x
                if x > droite: droite = x

    if bas < 0:
        raise ValueError("image entièrement transparente")

    haut = max(0, haut - marge); gauche = max(0, gauche - marge)
    bas = min(hauteur - 1, bas + marge); droite = min(largeur - 1, droite + marge)
    nl, nh = droite - gauche + 1, bas - haut + 1

    sortie = bytearray(nl * nh * 4)
    for y in range(nh):
        src = (haut + y) * ligne + gauche * 4
        sortie[y * nl * 4:(y + 1) * nl * 4] = pixels[src:src + nl * 4]

    ecrire_png(destination, nl, nh, sortie)
    return (largeur, hauteur), (nl, nh)


if __name__ == "__main__":
    avant, apres = rogner(sys.argv[1], sys.argv[2])
    print(f"{avant[0]}×{avant[1]} → {apres[0]}×{apres[1]}")
