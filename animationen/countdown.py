"""Countdown: große Ziffern zählen von 10 bis 1 herunter (jede schlägt hell auf, der Ring am Rand
läuft ab, die Farbe wandert von Blau nach Rot), die 0 blitzt und zerplatzt, dann Feuerwerk und
groß "PROSIT", danach "NEUJAHR" – 255 Bilder.
"""
import math
import random

from basis import (B, GELB, GOLD, HELLBLAU, ORANGE, PINK, ROT, SCHRIFT, TUERKIS, WEISS, Bild, dimmen, mischen,
                   regenbogen, textbreite)
from feuerwerk import Feuerwerk, jedes_bild_anders

NAME = "countdown"
TITEL = "Countdown 10 bis 0 und PROSIT NEUJAHR"

HIMMEL = (5, 0, 15)
JE_ZAHL = 11                                    # Bilder je Ziffer
NULL = 10 * JE_ZAHL                             # hier erscheint die 0
KNALL = NULL + 12                               # die 0 zerplatzt
PROSIT = (150, 198)                             # von … bis
NEUJAHR = (200, 250)

RAND = [(x, 0) for x in range(B)] + [(B - 1, y) for y in range(1, 16)] + \
       [(x, 15) for x in range(B - 2, -1, -1)] + [(0, y) for y in range(14, 0, -1)]


def ring(bild, anteil, farbe):
    """Lauflicht um den Rand, `anteil` (0..1) noch übrig; die Spitze leuchtet hell."""
    n = round(len(RAND) * anteil)
    start = len(RAND) - n                       # läuft im Uhrzeigersinn ab, von oben links
    for i in range(start, len(RAND)):
        x, y = RAND[i]
        bild.setze(x, y, WEISS if i - start < 3 and anteil < 1 else farbe)


def zahlfarbe(zahl):
    """10 = Blau … 5 = Grün … 1 = Rot: die Farbe zeigt, wie nah die Null ist."""
    return regenbogen((zahl - 1) * 24)


# runde Null ohne Schrägstrich, 15×14 wie die übrigen Ziffern (5×7 mal 3×2)
NULL_GROSS = ["...XXXXXXXXX...", "..XXXXXXXXXXX..", ".XXXX.....XXXX.", "XXX.........XXX", "XXX.........XXX",
              "XXX.........XXX", "XXX.........XXX", "XXX.........XXX", "XXX.........XXX", "XXX.........XXX",
              "XXX.........XXX", ".XXXX.....XXXX.", "..XXXXXXXXXXX..", "...XXXXXXXXX..."]


def grosse_zahl(bild, s, farbe, dy=0):
    x = (B - textbreite(s, 3)) // 2
    for z in s:
        if z == "0":
            bild.figur(x, 1 + dy, NULL_GROSS, {"X": farbe})
        else:
            bild.text(x, 1 + dy, z, farbe, hoch=2, breit=3)
        x += 18


def fett_text(bild, x, y, text, farbe, hoch=2):
    """5×7-Schrift, doppelt hoch und einen Pixel fetter (6 breit, 1 Abstand); liefert die Breite."""
    for i, z in enumerate(text):
        c = farbe(i) if callable(farbe) else farbe
        for gy, zeile in enumerate(SCHRIFT[z]):
            for gx, p in enumerate(zeile):
                if p == "1":
                    bild.rechteck(x + i * 7 + gx, y + gy * hoch, 2, hoch, c)
    return len(text) * 7 - 1


def wort(bild, f, text, von, bis, farbe):
    """Buchstaben erscheinen nacheinander (weiß aufblitzend), stehen ruhig, verlöschen gemeinsam.
    Um die Schrift bleibt ein dunkler Saum, damit das Feuerwerk dahinter sie nicht stört."""
    breite = len(text) * 7 - 1
    x0 = (B - breite) // 2
    schrift = Bild(None)
    hell = min(1.0, (bis - f) / 5)
    for i, z in enumerate(text):
        t = f - von - i * 2
        if t < 0:
            continue
        c = WEISS if t < 2 else farbe(i)
        fett_text(schrift, x0 + i * 7, 1, z, dimmen(c, round(hell * 3) / 3))
    for y in range(16):
        for x in range(B):
            if schrift.px[y][x] is None and any(
                    schrift.hole(x + dx, y + dy) is not None for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                bild.setze(x, y, HIMMEL)
    for y in range(16):
        for x in range(B):
            if schrift.px[y][x] is not None:
                bild.setze(x, y, schrift.px[y][x])


def _splitter():
    """Die Null in 2×2-Stücken mit Flugrichtung (vom Mittelpunkt weg) und eigenem Tempo."""
    z = random.Random(0)
    x0 = (B - 15) // 2
    stuecke = []
    for gy in range(0, 14, 2):
        for gx in range(0, 15, 2):
            if NULL_GROSS[gy][gx] == "X" or NULL_GROSS[gy + 1][min(gx + 1, 14)] == "X":
                dx, dy = gx - 7, gy - 6.5
                n = math.hypot(dx, dy) or 1
                stuecke.append((x0 + gx, 1 + gy, dx / n, dy / n, z.uniform(5, 13)))
    return stuecke


SPLITTER = _splitter()


def null_platzt(bild, k):
    """Die Null zerspringt: ihre Stücke fliegen strahlenförmig davon und verglühen."""
    hell = 1 - k / 13
    if hell <= 0:
        return
    weg = 1 - math.exp(-k / 3.5)
    c = WEISS if k < 2 else (GELB if k < 5 else (GOLD if k < 9 else ORANGE))
    c = dimmen(c, round(hell * 6) / 6)
    for x, y, dx, dy, tempo in SPLITTER:
        px = round(x + dx * tempo * weg * 1.6)
        py = round(y + dy * tempo * weg * 0.8 + 0.025 * k * k)
        if k < 5:
            bild.rechteck(px, py, 2, 2, c)
        else:
            bild.setze(px, py, c)


def bilder():
    arten = ("kugel", "doppel", "ring")
    farben = (ROT, GOLD, PINK, HELLBLAU, TUERKIS, GELB)
    mitte = Feuerwerk(saat=7, abstand=(5, 9), y_bereich=(4, 9), start=KNALL - 2, ende=PROSIT[0] - 12,
                      arten=arten, farben=farben)
    # neben der Schrift nur kleine Platzer, die ganz in den Rand passen
    links = Feuerwerk(saat=11, abstand=(13, 20), x_bereich=(3, 6), y_bereich=(4, 10), start=PROSIT[0] - 8,
                      ende=238, arten=arten, farben=farben, radius=(3.4, 4.2))
    rechts = Feuerwerk(saat=12, abstand=(13, 20), x_bereich=(58, 61), y_bereich=(4, 10), start=PROSIT[0] - 2,
                       ende=238, arten=arten, farben=farben, radius=(3.4, 4.2))
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        if f < NULL:
            zahl = 10 - f // JE_ZAHL
            t = f % JE_ZAHL
            farbe = zahlfarbe(zahl)
            ring(bild, 1 - t / JE_ZAHL, dimmen(farbe, 0.45))
            if t < 2:                                              # Aufschlag: fällt herein, weißglühend
                grosse_zahl(bild, str(zahl), mischen(farbe, WEISS, 0.7 - 0.3 * t), dy=(-3, -1)[t])
            else:
                puls = 1.0 if t < 8 else (0.75, 0.5, 0.3)[t - 8]
                grosse_zahl(bild, str(zahl), dimmen(farbe, puls))
        elif f < KNALL:                                            # die 0 blitzt
            g = f - NULL
            an = (g // 2) % 2 == 0
            ring(bild, 1, WEISS if an else GOLD)
            grosse_zahl(bild, "0", WEISS if an else GELB)
        else:
            for fw in (mitte, links, rechts):
                fw.zeichnen(bild, f, boden=15)
            null_platzt(bild, f - KNALL)
            if PROSIT[0] <= f < PROSIT[1]:
                wort(bild, f, "PROSIT", *PROSIT, lambda i: mischen(GOLD, GELB, round(2 + 2 * math.sin(f / 3 - i)) / 4))
            elif NEUJAHR[0] <= f < NEUJAHR[1]:
                wort(bild, f, "NEUJAHR", *NEUJAHR, lambda i: regenbogen(i * 45 + (f // 4) * 15))
        liste.append(bild)
    return jedes_bild_anders(liste, HIMMEL)
