"""Kamin: prasselndes Feuer, Strümpfe am Sims, Fenster mit Schneefall, Tannenbaum – 255 Bilder.

Ablauf: Feuer zündet (0–30), brennt; Strümpfe wippen; Kerzen auf dem Sims flackern;
ab 120 erscheint ein Geschenk nach dem anderen unter dem Baum.

Die Matrix speichert nur 80 KB je Animation und packt jedes Bild einzeln, Spalte für Spalte:
gleiche Nachbarspalten und Spalten, die es im Bild schon gab, kosten fast nichts, jede neue
Spaltenform rund 4–10 Bytes. Das frühere Feuer (zufälliges Flackern je Pixel) brauchte allein
mehr als den ganzen Speicher. Darum:
- Das Feuer besteht aus Flammenzungen von 2 Spalten Breite; jede Zunge ist allein durch ihre
  Höhe bestimmt (Farbbänder Gelb–Orange–Rot folgen daraus), gleiche Höhen sind gleiche Spalten.
- Zwei Strümpfe hängen vor den Ziegelpfeilern (der rechte ist ein Abbild des linken), einer im
  Zweierraster der Zungen vor dem Feuer; sie wippen senkrecht statt seitlich.
- Wand ohne Streifen, Ziegel nur mit Lagerfugen, Baum in Stufen (rechte Hälfte = linke),
  der Feuerschein färbt den ganzen Boden statt eines Verlaufs.
"""
import math
import random

from basis import (BLAU, BRAUN, BUNT, DUNKELGRUEN, GELB, GOLD, GRUEN, HELLBRAUN, LILA, NACHTBLAU,
                   ORANGE, PINK, ROT, SCHNEEDECKE, TUERKIS, WEISS, Bild, Schnee, mischen)

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "kamin"
TITEL = "Kaminfeuer mit Strümpfen, Fenster und Baum"

WAND = (40, 8, 12)
ZIEGEL = (150, 45, 25)
FUGE = (90, 30, 20)
SIMS = (41, 21, 7)
HOLZ = (33, 15, 4)
BODEN = (33, 15, 5)
MOND = (235, 230, 180)
RUSS = (8, 2, 0)                        # Rückwand der Feueröffnung

OX, OY, OB = 21, 6, 22                  # Öffnung des Kamins: links, oben, Breite (bis Zeile 15)
ZUNGEN = OB // 2                        # Flammenzungen, je 2 Spalten
GLUT_ROT = (150, 15, 0)
FLAMME_ROT = (235, 60, 0)
FLAMME_ORANGE = (255, 150, 0)
FLAMME_GELB = (255, 225, 90)
ZUNGEN_HOEHEN = (0, 1, 2, 3, 5, 7, 9)   # nur diese Höhen: gleiche Zungen wiederholen sich öfter

SCHNEE_DRAUSSEN = Schnee(anzahl=10, saat=3, farbe=(220, 225, 255))
STRUEMPFE = [(17, ROT), (31, GRUEN), (43, ROT)]             # linke Spalte, Farbe: vor den Ziegelpfeilern
#                                                             (rechts = Abbild von links) und mitten vor dem Feuer
BAUM_X = 55                                                 # linke der beiden Mittelspalten
BAUM_STUFEN = [(1, 2), (3, 5), (5, 8), (7, 11)]             # halbe Breite, oberste Zeile (je 3 Zeilen)
#             x, y oben, Breite, Höhe, Paket, Band (alle unter gleich hohen Baumspalten)
GESCHENKE = [(49, 12, 4, 3, PINK, GOLD), (59, 12, 4, 3, TUERKIS, ROT),
             (53, 13, 2, 2, LILA, WEISS), (57, 13, 2, 2, GOLD, BLAU)]
LICHTER = [(1, 3), (3, 6), (5, 9), (7, 12)]                 # halbe Breite der Stufe, Zeile: je Seite eins


def feuer_folge(n):
    """Höhe jeder Flammenzunge je Bild (Zeilen über dem Holz), in der Mitte am höchsten."""
    z = random.Random(1225)
    folge = []
    for f in range(n):
        staerke = min(1.0, (f + 4) / 30)                      # glimmt schon im ersten Bild
        hoehen = []
        for j in range(ZUNGEN):
            rand = abs(j - (ZUNGEN - 1) / 2) / (ZUNGEN / 2)
            grund = (1 - 0.75 * rand * rand) * (5.5 + 1.5 * math.sin(f * 0.7 + j * 1.3))
            soll = staerke * grund + z.choice((-1, 0, 0, 1))
            hoehen.append(min(ZUNGEN_HOEHEN, key=lambda h: abs(h - soll)))
        folge.append(hoehen)
    return folge


FEUER_FOLGE = feuer_folge(255)


def zunge(bild, x, h):
    """Eine Flammenzunge, 2 Spalten breit, h Zeilen hoch über dem Holz (Zeile 15):
    unten gelb, darüber orange und rot, die Spitze dunkelrot."""
    gelb, orange = h // 3, (h + 1) // 3
    for k in range(h):                                        # k = 0 unten
        farbe = (FLAMME_GELB if k < gelb else FLAMME_ORANGE if k < gelb + orange
                 else FLAMME_ROT if k < h - 1 or h < 3 else GLUT_ROT)
        bild.rechteck(x, 14 - k, 2, 1, farbe)


def wand(bild, f):
    schein = 0.0 if f < 20 else 0.3 + 0.1 * round(math.sin(f / 3))      # Feuerschein auf dem Boden
    bild.rechteck(0, 0, 64, 15, WAND)
    bild.rechteck(0, 15, 64, 1, mischen(BODEN, (230, 80, 0), schein))


def fenster(bild, f):
    bild.rechteck(2, 2, 13, 10, NACHTBLAU)
    bild.rechteck(12, 2, 3, 3, MOND)                          # Mond am Fensterrahmen
    SCHNEE_DRAUSSEN.zeichnen(bild, f, nur_auf={NACHTBLAU})
    bild.rechteck(2, 10, 13, 2, SCHNEEDECKE)                  # Schnee auf dem Fensterbrett
    for y in (1, 6, 12):
        bild.rechteck(1, y, 15, 1, HELLBRAUN)
    for x in (1, 8, 15):
        bild.rechteck(x, 1, 1, 12, HELLBRAUN)


def kamin(bild, f):
    bild.rechteck(17, 5, 30, 11, ZIEGEL)                      # Ziegel mit Lagerfugen
    for y in (7, 10, 13):
        bild.rechteck(17, y, 30, 1, FUGE)
    bild.rechteck(OX, OY, OB, 10, RUSS)
    glut = f >= 12 and random.Random(f // 3).random() < 0.4     # das Holz glüht ab und zu auf
    bild.rechteck(OX, 15, OB, 1, mischen(HOLZ, FLAMME_ROT, 0.5) if glut else HOLZ)
    for j, h in enumerate(FEUER_FOLGE[f]):
        zunge(bild, OX + 2 * j, h)
    k, t = divmod(f - 34, 13)                                 # ab und zu steigt ein Funke auf
    if k >= 0 and t < 5:
        x, y = OX + 3 + (k * 7) % 16, 10 - t
        if bild.hole(x, y) == RUSS:
            bild.setze(x, y, FLAMME_GELB if t < 2 else FLAMME_ORANGE if t < 4 else FLAMME_ROT)
    bild.rechteck(16, 3, 32, 1, HELLBRAUN)                    # Sims
    bild.rechteck(16, 4, 32, 1, SIMS)


def kerzen(bild, f):
    z = random.Random(f // 2)
    flamme = GELB if z.random() < 0.7 else ORANGE             # Flammen flackern (beide gleich)
    for x in (16, 47):                                        # an den Enden des Simses
        bild.rechteck(x, 1, 1, 2, WEISS)
        bild.setze(x, 0, flamme)


def struempfe(bild, f):
    for i, (x, farbe) in enumerate(STRUEMPFE):
        lang = math.sin((f + i % 2 * 13) / 11) > 0.5          # wippt: streckt sich um eine Zeile
        streifen = WEISS if (f // 16 + i) % 2 else farbe
        bild.rechteck(x, 5, 2, 1, WEISS)                      # Bündchen
        bild.rechteck(x, 6, 2, 2 + lang, farbe)
        bild.rechteck(x, 7, 2, 1, streifen)
        bild.rechteck(x, 8 + lang, 4, 2, farbe)               # Fuß


def baum(bild, f):
    for halb, oben in BAUM_STUFEN:                            # vier Stufen, unten je ein Schatten
        bild.rechteck(BAUM_X + 1 - halb, oben, 2 * halb, 14 - oben, GRUEN)
    for halb, oben in BAUM_STUFEN:
        bild.rechteck(BAUM_X + 1 - halb, oben + 2, 2 * halb, 1, DUNKELGRUEN)
    bild.rechteck(BAUM_X, 14, 2, 1, BRAUN)
    puls = (f // 5) % 2                                       # Stern
    bild.rechteck(BAUM_X, 0, 2, 2, GELB if puls else GOLD)
    for k, (halb, y) in enumerate(LICHTER):                   # Lichter 2 breit, links und rechts
        blitz = (f + k * 11) % 40 < 2                         # gleich: wechseln die Farbe, funkeln
        farbe = WEISS if blitz else BUNT[(k * 2 + f // 32) % len(BUNT)]
        bild.rechteck(BAUM_X + 1 - halb, y, 2, 1, farbe)
        bild.rechteck(BAUM_X - 1 + halb, y, 2, 1, farbe)


def geschenke(bild, f):
    for i, (x, y, b, h, paket, band) in enumerate(GESCHENKE):
        start = 120 + i * 25
        if f < start:
            continue
        if f - start < 6:                                     # erscheint mit Funkeln
            if (f - start) % 2:
                bild.rechteck(x, y + h - 2, b, 1, WEISS)
            continue
        bild.rechteck(x, y, b, h, paket)
        bild.rechteck(x, y + (h - 1) // 2, b, 1, band)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild()
        wand(bild, f)
        fenster(bild, f)
        kamin(bild, f)
        kerzen(bild, f)
        struempfe(bild, f)
        baum(bild, f)
        geschenke(bild, f)
        liste.append(bild)
    return liste
