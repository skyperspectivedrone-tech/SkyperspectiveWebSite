# -*- coding: utf-8 -*-
"""Décline le logo (marine + rouge sur transparence) en version blanche pour fond sombre.
Pas de dépendance externe : décodage / réencodage PNG en Python pur."""
import zlib, struct, sys


def lire_png(chemin):
    data = open(chemin, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "PNG attendu"
    pos, idat, entete = 8, b"", None
    while pos < len(data):
        taille = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        contenu = data[pos + 8:pos + 8 + taille]
        pos += 12 + taille
        if typ == b"IHDR":
            entete = struct.unpack(">IIBBBBB", contenu)
        elif typ == b"IDAT":
            idat += contenu
        elif typ == b"IEND":
            break
    largeur, hauteur, profondeur, couleur, _, _, entrelace = entete
    assert (profondeur, couleur, entrelace) == (8, 6, 0), \
        f"attendu RGBA 8 bits non entrelacé, reçu {profondeur=} {couleur=} {entrelace=}"
    return largeur, hauteur, zlib.decompress(idat)


def defiltrer(largeur, hauteur, brut, bpp=4):
    ligne_octets = largeur * bpp
    sortie = bytearray(hauteur * ligne_octets)
    precedente = bytearray(ligne_octets)
    pos = 0
    for y in range(hauteur):
        filtre = brut[pos]; pos += 1
        ligne = bytearray(brut[pos:pos + ligne_octets]); pos += ligne_octets
        if filtre == 1:
            for i in range(bpp, ligne_octets):
                ligne[i] = (ligne[i] + ligne[i - bpp]) & 255
        elif filtre == 2:
            for i in range(ligne_octets):
                ligne[i] = (ligne[i] + precedente[i]) & 255
        elif filtre == 3:
            for i in range(ligne_octets):
                gauche = ligne[i - bpp] if i >= bpp else 0
                ligne[i] = (ligne[i] + ((gauche + precedente[i]) >> 1)) & 255
        elif filtre == 4:
            for i in range(ligne_octets):
                a = ligne[i - bpp] if i >= bpp else 0
                b = precedente[i]
                c = precedente[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                ligne[i] = (ligne[i] + pred) & 255
        elif filtre != 0:
            raise ValueError(f"filtre PNG inconnu : {filtre}")
        sortie[y * ligne_octets:(y + 1) * ligne_octets] = ligne
        precedente = ligne
    return sortie


def recolorer(pixels, blanc=(255, 255, 255), rouge=(0xD6, 0x28, 0x28)):
    """Le trait rouge du logo garde sa couleur, tout le reste devient blanc."""
    for i in range(0, len(pixels), 4):
        if pixels[i + 3] == 0:
            continue
        r, v, b = pixels[i], pixels[i + 1], pixels[i + 2]
        est_rouge = r > 90 and r > v + 40 and r > b + 40
        cible = rouge if est_rouge else blanc
        pixels[i], pixels[i + 1], pixels[i + 2] = cible
    return pixels


def ecrire_png(chemin, largeur, hauteur, pixels, bpp=4):
    ligne_octets = largeur * bpp
    brut = bytearray()
    for y in range(hauteur):
        brut.append(0)
        brut += pixels[y * ligne_octets:(y + 1) * ligne_octets]

    def morceau(typ, contenu):
        return (struct.pack(">I", len(contenu)) + typ + contenu
                + struct.pack(">I", zlib.crc32(typ + contenu) & 0xFFFFFFFF))

    entete = struct.pack(">IIBBBBB", largeur, hauteur, 8, 6, 0, 0, 0)
    donnees = zlib.compress(bytes(brut), 9)
    open(chemin, "wb").write(b"\x89PNG\r\n\x1a\n" + morceau(b"IHDR", entete)
                             + morceau(b"IDAT", donnees) + morceau(b"IEND", b""))


if __name__ == "__main__":
    source, destination = sys.argv[1], sys.argv[2]
    largeur, hauteur, brut = lire_png(source)
    pixels = recolorer(defiltrer(largeur, hauteur, brut))
    ecrire_png(destination, largeur, hauteur, pixels)
    import os
    print(f"✓ {destination} — {largeur}×{hauteur} — {os.path.getsize(destination) // 1024} Ko")
