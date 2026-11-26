#!/usr/bin/env python3
"""Farbtafel für die Surplife-Matrix: zeigt, wie die 16-Bit-Farben (7 Bit Farbton, 4 Bit Sättigung,
5 Bit Helligkeit) auf den LEDs wirken.

Die Seiten werden direkt als Matrix-Farbcodes gebaut, ohne Umweg über RGB, damit jede Stufe genau
einmal vorkommt. Die Vorschau rechnet dieselben Codes linear nach RGB zurück; der Vergleich mit
der echten Matrix zeigt, ob die Matrix eine Helligkeitskurve hat (dunkle Stufen wirken heller als
in der Vorschau) und welche Stufen sich auf den LEDs noch unterscheiden.

Seiten:
  1 Helligkeit   Stufe 0–31 von links nach rechts (je 2 Spalten): weiß, rot, grün, blau
  2 Farbtöne     128 Farbtöne (je halbe Spalte): oben voll, Mitte halbe Helligkeit, unten halbe Sättigung
  3 Projekt      die Grundfarben aus led/animationen/basis.py als Felder (oben 10, unten 10)
  4 Dunkel       Stufe 1–8 (je 8 Spalten) in weiß, rot, grün, blau: die Töne der Nachthimmel

Aufruf:  farbtafel.py vorschau DATEI.png          alle Seiten untereinander, 10-fach
         farbtafel.py zeigen SEITE [--hell 67]    Seite auf die Matrix laden (Wächter vorher stoppen!)
"""
import argparse
import asyncio
import colorsys
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matrix_spieler import BREITE, HOEHE, hsv16  # noqa: E402

# Grundfarben wie in led/animationen/basis.py (dort nicht importierbar: Pillow-frei halten)
PROJEKT = [(0, 0, 22), (140, 150, 190), (190, 200, 235), (90, 90, 100), (255, 170, 110),
           (110, 50, 10), (170, 90, 30), (0, 90, 20), (0, 170, 0), (255, 150, 0),
           (255, 90, 0), (255, 0, 0), (150, 0, 20), (255, 0, 160), (170, 0, 255),
           (0, 60, 255), (0, 200, 255), (0, 255, 170), (255, 210, 0), (255, 255, 255)]


def code(h, s, v):
    """Farbton 0–127, Sättigung 0–15, Helligkeit 0–31 → 16-Bit-Code der Matrix."""
    return (h & 0x7F) << 9 | (s & 0x0F) << 5 | (v & 0x1F)


def rgb(c):
    """16-Bit-Code → RGB, linear (so sähe es aus, wenn die Matrix keine Kurve hätte)."""
    r, g, b = colorsys.hsv_to_rgb((c >> 9) / 127, ((c >> 5) & 15) / 15, (c & 31) / 31)
    return round(r * 255), round(g * 255), round(b * 255)


BAENDER = [(0, 0), (0, 15), (42, 15), (85, 15)]      # weiß, rot, grün, blau: (Farbton, Sättigung)
# Seite 6 (25.11.2026: Braun und Haut wirkten auf den LEDs orange): Kandidaten (Farbton, Sättigung,
# Helligkeit), Feld 1 = bisheriger Wert (BRAUN (110,50,10) bzw. HAUT (255,170,110))
BRAUN_WAHL = [(8, 14, 13), (8, 15, 6), (8, 12, 5), (7, 15, 4), (9, 10, 4), (6, 15, 3), (10, 12, 3), (8, 8, 5)]
HAUT_WAHL = [(9, 9, 31), (9, 6, 31), (9, 5, 26), (8, 4, 31), (10, 5, 22), (8, 6, 18), (11, 4, 28), (9, 3, 24)]


def seite(n):
    """Liste von HOEHE Zeilen à BREITE Codes."""
    z = [[0] * BREITE for _ in range(HOEHE)]
    for y in range(HOEHE):
        for x in range(BREITE):
            if n == 1:
                h, s = BAENDER[y // 4]
                z[y][x] = code(h, s, x // 2)
            elif n == 2:
                h = x * 2 + (y % 2)                    # halbe Spalte: gerade/ungerade Zeilen
                z[y][x] = code(h, 15, 31) if y < 8 else code(h, 15, 16) if y < 12 else code(h, 8, 31)
            elif n == 3:
                i = (y // 8) * 10 + min(x // 6, 9) if 2 <= x < 62 else None
                z[y][x] = hsv16(*PROJEKT[(y // 8) * 10 + (x - 2) // 6]) if i is not None else 0
            elif n == 4:
                h, s = BAENDER[y // 4]
                z[y][x] = code(h, s, 1 + x // 8)
            elif n == 5:                               # vier große weiße Blöcke: Stufe 31, 16, 8, 3
                z[y][x] = code(0, 0, (31, 16, 8, 3)[x // 16]) if x % 16 < 14 else 0
            elif n == 6:                               # Auswahl: oben 8 Brauntöne, unten 8 Hauttöne
                if x % 8 == 7 or y == 7 or y == 8:
                    z[y][x] = 0
                else:
                    z[y][x] = code(*(BRAUN_WAHL if y < 7 else HAUT_WAHL)[x // 8])
    return z


def bild_bytes(z):
    """Zeilen mit Codes → 2048 Bytes spaltenweise (wie matrix_upload.bild_spaltenweise)."""
    out = bytearray()
    for x in range(BREITE):
        for y in range(HOEHE):
            out += z[y][x].to_bytes(2, "big")
    return bytes(out)


def vorschau(pfad, faktor=10):
    from PIL import Image
    seiten = [seite(n) for n in (1, 2, 3, 4)]
    luecke = 4
    im = Image.new("RGB", (BREITE * faktor, len(seiten) * (HOEHE * faktor + luecke)), (60, 60, 60))
    for k, z in enumerate(seiten):
        for y in range(HOEHE):
            for x in range(BREITE):
                farbe = rgb(z[y][x])
                for dy in range(faktor - 1):
                    for dx in range(faktor - 1):
                        im.putpixel((x * faktor + dx, k * (HOEHE * faktor + luecke) + y * faktor + dy), farbe)
    im.save(pfad)


async def zeigen(n, hell, name):
    from matrix_spieler import Matrix
    from matrix_upload import hochladen
    b = bild_bytes(seite(n))
    m = Matrix(name)
    await m.verbinden()
    try:
        await hochladen(m, [b, b], 75, hell)           # zwei gleiche Bilder: Standbild
        await asyncio.sleep(1)
    finally:
        await m.trennen()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("was", choices=["vorschau", "zeigen"])
    p.add_argument("ziel", help="PNG-Datei (vorschau) oder Seite 1–4 (zeigen)")
    p.add_argument("--hell", type=int, default=100)
    p.add_argument("-n", "--name", default=os.environ.get("MATRIX_NAME") or "IOTBT1A2")
    a = p.parse_args()
    if a.was == "vorschau":
        vorschau(a.ziel)
    else:
        import logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
        asyncio.run(zeigen(int(a.ziel), a.hell, a.name))
