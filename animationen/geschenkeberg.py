"""Geschenkeberg: neben dem geschmückten Baum fallen Pakete in allen Farben herab und stapeln
sich Reihe für Reihe zu einem Berg (jedes federt beim Aufsetzen kurz nach), ganz oben landet
ein Stern, dann glitzert der ganze Berg und löst sich funkelnd auf – 255 Bilder.

Größe (23.11.2026): Die Matrix speichert je Animation nur 80 KB und komprimiert jedes Bild
einzeln, spaltenweise – jede Spalte, die anders aussieht als eine frühere, kostet in allen 255
Bildern. Damit der Berg unter 76000 Bytes bleibt (vorher 130000): die Pakete stehen in sechs
Türmen genau übereinander (12 statt 15, dafür alle 7 breit; Band 1 breit mit Knoten obenauf, ohne
Licht- und Schattenkante), der Baum ist einfarbig grün (ohne dunklen Rand und helle Tupfen), seine
Lichter blinken (an/aus statt vier Helligkeiten), und am Ende verschwinden die Pakete einzeln mit
einem Funken – Baum und Boden bleiben stehen (vorher löste sich alles in Rauschen auf).
"""
import math
import random

from basis import (B, BLAU, BRAUN, BUNT, GELB, GOLD, HELLBLAU, LILA, ORANGE, PINK, ROT, TUERKIS,
                   WEISS, Bild, dimmen)

NAME = "geschenkeberg"
TITEL = "Geschenkeberg unter dem Baum"

HINTERGRUND = (14, 3, 10)
BODEN = (75, 36, 14)
BAUM_X = 8
BAUMGRUEN = (0, 150, 30)
HALB = [1, 2, 3, 2, 3, 4, 5, 4, 5, 6, 7, 8]           # halbe Breite des Baums je Zeile ab y = 2
LICHTER = [(8, 3), (6, 5), (10, 6), (7, 8), (11, 9), (4, 9), (9, 11), (5, 12), (13, 12), (2, 13), (8, 13)]
PAPIER = [(ROT, GELB), ((0, 80, 255), WEISS), ((0, 180, 40), ROT), (PINK, WEISS), (LILA, GELB),
          (ORANGE, BLAU), (HELLBLAU, ROT), (TUERKIS, PINK), (GELB, ROT)]
# Pakete (x, breite, höhe), Reihe für Reihe von unten; alle gleich breit und genau übereinander
REIHEN = [
    [(19, 7, 4), (26, 7, 3), (33, 7, 4), (40, 7, 3), (47, 7, 4), (54, 7, 3)],
    [(26, 7, 4), (33, 7, 3), (40, 7, 4), (47, 7, 3)],
    [(33, 7, 3), (40, 7, 3)],
]
TAKT = 15                                   # Bilder zwischen zwei Paketen
STERN_AB = 190
GIPFEL_X = 39                               # hier landet der Stern
G = 0.36                                    # Fallbeschleunigung (Pixel je Bild²)
WEG_AB = 244                                # ab hier verschwinden Stern und Pakete
GLITZER = 4                                 # weiße Glitzerpunkte auf dem fertigen Berg


def baum(bild, f, fest):
    for r, w in enumerate(HALB):
        bild.rechteck(BAUM_X - w, 2 + r, 2 * w + 1, 1, BAUMGRUEN)
    bild.rechteck(BAUM_X - 1, 14, 3, 1, BRAUN)
    bild.rechteck(BAUM_X - 1, 1, 3, 1, GELB)                       # Stern auf der Spitze
    bild.setze(BAUM_X, 0, GELB)
    bild.setze(BAUM_X, 1, WEISS if (f // 5) % 2 else GELB)
    for k, (x, y) in enumerate(LICHTER):                           # Lichter blinken, jedes in seinem Takt
        if fest or math.sin(f / 5 + k * 2.1) > -0.5:
            bild.setze(x, y, BUNT[(k * 4) % len(BUNT)])


def plan():
    """Liste (start, x, breite, höhe, papier, band, y_unten) – jedes Paket ruht auf dem darunter."""
    z = random.Random(8)
    oben = [15] * B                                               # erste belegte Zeile je Spalte
    pakete = []
    start = 4
    for reihe in REIHEN:
        fertig = []
        for x, b, h in reihe:
            unten = min(oben[x:x + b]) - 1
            fertig.append((x, b, h, unten))
        for x, b, h, unten in fertig:
            for xx in range(x, x + b):
                oben[xx] = unten - h + 1
        folge = list(fertig)
        z.shuffle(folge)
        for x, b, h, unten in folge:
            while True:                                           # Nachbarn in anderen Farben
                papier, band = PAPIER[z.randrange(len(PAPIER))]
                gipfel_gelb = x <= GIPFEL_X < x + b and GELB in (papier, band)   # Stern soll abstechen
                if not gipfel_gelb and all(
                        p[4] != papier or not (p[1] - 1 <= x + b and x <= p[1] + p[2] + 1
                                               and abs(p[6] - unten) <= 5) for p in pakete):
                    break
            pakete.append((start, x, b, h, papier, band, unten))
            start += TAKT
    return pakete, (GIPFEL_X, min(oben[GIPFEL_X - 1:GIPFEL_X + 2]) - 1)


PAKETE, GIPFEL = plan()


def fall(t, ziel, start_y=-1):
    """Unterkante nach t Bildern freiem Fall bis ziel; federt nach dem Aufsetzen einmal nach."""
    y = start_y + 0.5 * G * t * t
    if y < ziel:
        return round(y), False
    t_land = math.ceil(math.sqrt(2 * (ziel - start_y) / G))
    return ziel - (1 if t - t_land in (1, 2) else 0), t - t_land < 4


def paket(bild, x, b, h, papier, band, unten):
    oben = unten - h + 1
    bild.rechteck(x, oben, b, h, papier)
    bx, bb = x + (b - 1) // 2, 2 - b % 2                           # Band mittig (1 oder 2 breit)
    bild.rechteck(bx, oben - 1, bb, h + 1, band)                   # mit Knoten obenauf


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        bild.rechteck(0, 15, B, 1, BODEN)
        baum(bild, f, f >= STERN_AB + 12)
        weg = max(0, f - WEG_AB)                                   # 0…10: so viele Schritte sind fort
        staub, funken = [], []
        for nr, (start, x, b, h, papier, band, unten) in enumerate(PAKETE):
            if f < start:
                continue
            geht = 2 + (len(PAKETE) - 1 - nr) * 8 // len(PAKETE)   # zuletzt gefallene zuerst
            if weg >= geht:
                if weg == geht:                                    # verschwindet mit einem Funken
                    funken += [(x + 1, unten - h + 1, GELB), (x + 4, unten - 1, WEISS)]
                continue
            y, eben_gelandet = fall(f - start, unten)
            paket(bild, x, b, h, papier, band, y)
            if eben_gelandet and y == unten:
                staub.append((x - 1, unten))
                staub.append((x + b, unten))
        for x, y in staub:
            if bild.hole(x, y) == HINTERGRUND:
                bild.setze(x, y, (150, 140, 120))
        for x, y, farbe in funken:
            bild.setze(x, y, farbe)
        if STERN_AB <= f and weg < 2:                              # Stern auf dem Gipfel
            gx, gy = GIPFEL
            y, _ = fall(f - STERN_AB, gy - 1, start_y=-2)
            t = f - STERN_AB - 9
            bild.setze(gx, y, WEISS)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                bild.setze(gx + dx, y + dy, GELB)
            if t >= 0:
                if (f // 3) % 2:
                    for dx, dy in ((2, -1), (-2, -1), (2, 1), (-2, 1)):
                        bild.setze(gx + dx, y + dy, GOLD)
                if t < 10:                                        # Strahlenkranz beim Aufsetzen
                    for k in range(10):
                        w = k * math.pi / 5
                        r = 2 + t * 0.9
                        bild.setze(gx + r * 1.6 * math.cos(w), y - abs(r * 0.9 * math.sin(w)) + 1,
                                   dimmen(GELB, 1 - t // 3 * 0.25))
                z = random.Random(f // 3)                         # der Berg glitzert
                for _ in range(GLITZER):
                    _, x, b, h, _, _, unten = PAKETE[z.randrange(len(PAKETE))]
                    bild.setze(x + z.randrange(b), unten - z.randrange(h), WEISS)
        liste.append(bild)
    return liste
