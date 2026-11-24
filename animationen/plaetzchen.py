"""Plätzchen backen, von oben auf den Tisch gesehen: das Nudelholz rollt den Teig aus,
Ausstecher drücken Stern, Herz, Tanne und Mond aus, der Rest-Teig verschwindet, das Blech
glüht im Ofen und die Plätzchen werden goldbraun, zum Schluss bunter Zuckerguss aus dem
Spritzbeutel, Streusel und Glanz – 255 Bilder.
"""
import math
import random

from basis import B, BUNT, WEISS, Bild, mischen

NAME = "plaetzchen"
TITEL = "Plätzchen backen mit Zuckerguss"

TISCH = (46, 22, 8)
MASER = (60, 30, 11)
TEIG = (195, 150, 80)
TEIG_HELL = (250, 220, 150)
SCHNITT = (115, 75, 30)
GEBACKEN = (205, 115, 35)
RAND_GEBACKEN = (150, 70, 15)
BLECH = (34, 34, 46)
STAHL = (205, 205, 220)
STERN = ["....x....",
         "....x....",
         "...xxx...",
         "xxxxxxxxx",
         ".xxxxxxx.",
         "..xxxxx..",
         "..xxxxx..",
         ".xxx.xxx.",
         ".x.....x."]
HERZ = [".xx...xx.",
        "xxxx.xxxx",
        "xxxxxxxxx",
        "xxxxxxxxx",
        "xxxxxxxxx",
        ".xxxxxxx.",
        "..xxxxx..",
        "...xxx...",
        "....x...."]
TANNE = ["....x....",
         "...xxx...",
         "..xxxxx..",
         "...xxx...",
         "..xxxxx..",
         ".xxxxxxx.",
         "..xxxxx..",
         "xxxxxxxxx",
         "...xxx..."]
MOND = ["..xxxx...",
        ".xxxx....",
        "xxxx.....",
        "xxxx.....",
        "xxxx.....",
        "xxxx.....",
        "xxxxx...x",
        ".xxxxxxx.",
        "..xxxxx.."]
FORMEN = [STERN, HERZ, TANNE, MOND]
GUSS = [(255, 235, 60), (255, 30, 110), (0, 210, 60), (130, 220, 255)]
PLATZ = [4, 20, 36, 52]                             # linke Kante der Plätzchen (9 breit)
Y0 = 3                                              # obere Kante

# Ablauf
T_STECHEN, T_REST, T_OFEN, T_GUSS, T_STREUSEL = 50, 110, 125, 185, 233
JE_FORM, JE_GUSS = 15, 12


def drin(form, x, y):
    return 0 <= x < 9 and 0 <= y < 9 and form[y][x] == "x"


def rand(form, x, y):
    """Randpixel der Form (hat einen Nachbarn außerhalb)."""
    return drin(form, x, y) and not all(drin(form, x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def tisch(bild):
    """Holzmaserung als durchgehende Linien: Die Matrix komprimiert jedes Bild einzeln und
    spaltenweise; die frühere gestrichelte Maserung machte jede Spalte anders und kostete in
    allen Bildern rund 80 Bytes (zusammen 84000 statt höchstens 76000, (23.11.2026)."""
    for y in (1, 5, 6, 10, 14):
        bild.rechteck(0, y, B, 1, MASER)


def teigplatte(bild, halb_b, halb_h, farbe=TEIG):
    for y in range(16):
        for x in range(B):
            dx, dy = (x - 31.5) / halb_b, (y - 7.5) / halb_h
            d = dx ** 4 + dy ** 4
            if d <= 1:
                bild.setze(x, y, farbe)


def nudelholz(bild, x):
    x = round(x)
    bild.rechteck(x - 1, 0, 2, 16, (120, 65, 25))                  # Griffe
    bild.rechteck(x - 2, 2, 4, 12, (205, 140, 65))
    bild.rechteck(x - 2, 2, 1, 12, (245, 195, 115))
    bild.rechteck(x + 1, 2, 1, 12, (150, 90, 35))


def plaetzchen(bild, i, innen, kante, dy=0):
    for y in range(9):
        for x in range(9):
            if drin(FORMEN[i], x, y):
                bild.setze(PLATZ[i] + x, Y0 + y + dy, kante if rand(FORMEN[i], x, y) else innen)


def ausstecher(bild, i, dy, dx=0):
    for y in range(9):
        for x in range(9):
            if rand(FORMEN[i], x, y):
                bild.setze(PLATZ[i] + x + dx, Y0 + y + dy, STAHL)


def spritzbeutel(bild, x, y, farbe):
    bild.setze(x, y, farbe)
    for k in range(1, 5):                                          # schräg nach rechts oben gehalten
        bild.rechteck(x + k, y - k - (k > 2), 2 if k < 3 else 3, 2 if k < 3 else 3, WEISS)
    bild.setze(x + 1, y - 1, (200, 200, 215))


def bilder():
    z = random.Random(77)
    streusel = []
    for i in range(4):                                             # 2–3 Streusel auf dem Guss
        innen = [(x, y) for y in range(9) for x in range(9)
                 if drin(FORMEN[i], x, y) and not rand(FORMEN[i], x, y)]
        z.shuffle(innen)
        andere = [c for c in BUNT + [WEISS] if c != GUSS[i]]
        streusel.append([(x, y, andere[z.randrange(len(andere))]) for x, y in innen[:min(3, len(innen) // 5)]])
    liste = []
    for f in range(255):
        bild = Bild(TISCH)
        tisch(bild)
        if f < T_STECHEN:                                          # Teig ausrollen
            a = min(1.0, f / 42)
            a = a * a * (3 - 2 * a)
            halb_b = 6 + 24.5 * a
            teigplatte(bild, halb_b, 5 + a, mischen((170, 125, 60), TEIG, round(a * 6) / 6))
            if f < 46:
                nudelholz(bild, 31.5 + (halb_b - 1) * math.sin(f * 2 * math.pi / 23))
            else:
                nudelholz(bild, 31.5 + (f - 45) * 9)               # rollt hinaus
        elif f < T_OFEN:                                           # ausstechen, dann Rest weg
            rest = max(0.0, min(1.0, (f - T_REST) / 10))
            if rest < 1:
                teigplatte(bild, 30.5, 6, mischen(TEIG, TISCH, rest))
            g = f - T_STECHEN
            for i in range(4):
                h = g - i * JE_FORM
                if h >= 9:                                         # ausgestochen
                    plaetzchen(bild, i, TEIG_HELL, mischen(SCHNITT, TEIG_HELL, rest))
                elif h >= 5:                                       # Ausstecher drückt
                    plaetzchen(bild, i, WEISS if h < 7 else TEIG_HELL, STAHL)
                if 0 <= h < 5:
                    ausstecher(bild, i, -(12 - h * 3))             # kommt von oben
                elif 9 <= h < 14:
                    ausstecher(bild, i, -(h - 8) * 3, dx=1)        # hebt ab
        elif f < T_GUSS:                                           # im Ofen
            g = f - T_OFEN
            an = min(1.0, g / 6, (T_GUSS - 1 - f) / 6)
            glut = an * (0.75 + 0.25 * math.sin(g / 3))
            bild.rechteck(0, 0, B, 16, mischen(BLECH, (120, 14, 0), 0.5 * an))
            for y in (0, 1, 14, 15):                               # Heizstäbe oben und unten
                for x in range(B):
                    wellig = 0.8 + 0.2 * math.sin(x / 2 + g / 2 + y)
                    bild.setze(x, y, mischen(BLECH, (255, 70, 0) if y in (0, 15) else (255, 150, 0),
                                             round(glut * wellig * 12) / 12))
            braun = min(1.0, (g // 4) / 12)                         # in 12 Stufen goldbraun
            for i in range(4):
                plaetzchen(bild, i, mischen(TEIG_HELL, GEBACKEN, braun), mischen(TEIG_HELL, RAND_GEBACKEN, braun))
        else:                                                      # Zuckerguss, Streusel, Glanz
            g = f - T_GUSS
            for i in range(4):
                plaetzchen(bild, i, GEBACKEN, RAND_GEBACKEN)
                h = g - i * JE_GUSS
                if h < 0:
                    continue
                zeilen = min(9, h + 1)
                for y in range(zeilen):
                    for x in range(9):
                        if drin(FORMEN[i], x, y) and not rand(FORMEN[i], x, y):
                            bild.setze(PLATZ[i] + x, Y0 + y, GUSS[i])
                s = (f - T_STREUSEL - i * 2) // 2                   # Streusel fallen nacheinander
                for k, (x, y, c) in enumerate(streusel[i]):
                    if s >= k:
                        bild.setze(PLATZ[i] + x, Y0 + y, c)
            i = g // JE_GUSS
            if i < 4:                                              # Spritzbeutel über dem Plätzchen
                h = g % JE_GUSS
                zeile = min(8, h)
                spalten = [x for x in range(9) if drin(FORMEN[i], x, zeile) and not rand(FORMEN[i], x, zeile)] or [4]
                x = spalten[0] if h % 2 else spalten[-1]
                spritzbeutel(bild, PLATZ[i] + x, Y0 + zeile, GUSS[i])
            if f >= T_STREUSEL + 10:                               # Glanz wandert über die Plätzchen
                i = ((f - T_STREUSEL - 10) // 3) % 4
                gx, gy = PLATZ[i] + 4 + (i % 2) * 2 - 1, Y0 + 3 + (i // 2)
                bild.setze(gx, gy, WEISS)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    bild.setze(gx + dx, gy + dy, mischen(bild.hole(gx + dx, gy + dy) or WEISS, WEISS, 0.35))
        liste.append(bild)
    return liste
