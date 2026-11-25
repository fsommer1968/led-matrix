"""Krippe: der Stern von Bethlehem zieht mit Schweif über den Himmel und bleibt über dem Stall
stehen, im Stall wird es hell (Maria, Josef, das Kind in der Krippe), die drei Könige ziehen auf
ihren Kamelen als Karawane heran – 255 Bilder.

0–80    Stern zieht von links zum Stall
80–105  Licht geht im Stall an, Strahl vom Stern
70–190  Karawane zieht heran und hält vor dem Stall
190–255 alle stehen still, Stern und Kind strahlen

Sparsam gezeichnet, weil die Matrix je Animation nur 80 KB speichert (Ziel ≤ 76000 Bytes,
siehe groesse.py): flacher Boden, sieben Sterne, Schweif in drei Helligkeitsstufen, Kamele im
Gleichschritt (gleiche Spalten packen sich gut).
"""
import math

from basis import (B, GELB, GOLD, LILA, NACHTBLAU, ROT, WEISS, Bild, Sterne, dimmen, mischen)

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "krippe"
TITEL = "Stern von Bethlehem über dem Stall"

SAND = (95, 68, 28)
SAND_HELL = (140, 104, 48)
BALKEN = (41, 23, 7)
DACH = (49, 31, 10)
STROH = (220, 170, 50)
KAMEL = (66, 46, 21)
KAMEL_DUNKEL = (41, 27, 11)
HAUT = (214, 174, 143)
STERNE = Sterne(anzahl=0)
# Sieben Sterne von Hand verteilt (x, y, Phase, Periode) statt 18 zufälliger: jeder einzelne
# Funkelpunkt kostet in jedem Bild etwa 9 Bytes, die Matrix speichert nur 80 KB je Animation.
STERNE.sterne = [(3, 2, 0, 32), (10, 6, 17, 40), (17, 1, 9, 24), (24, 4, 30, 32),
                 (32, 0, 5, 40), (38, 5, 22, 24), (62, 3, 13, 32)]
STALL_X = 43                                   # linke Kante des Stalls (18 breit)
STERN_ZIEL = (STALL_X + 9, 2)

KAMEL_FIGUR = [  # schaut nach rechts, 11 breit, 9 hoch; König sitzt auf dem Höcker
    [
        "...cc......",
        "...hh...kk.",
        "..mmmm..kkk",
        "..mmmm..k..",
        ".kkkkkkkk..",
        "tkkkkkkkk..",
        ".kkkkkkk...",
        ".k.d..k.d..",
        ".k.d..k.d..",
    ],
    [
        "...cc......",
        "...hh...kk.",
        "..mmmm..kkk",
        "..mmmm..k..",
        ".kkkkkkkk..",
        "tkkkkkkkk..",
        ".kkkkkkk...",
        ".dk...dk...",
        "d..k.d..k..",
    ],
]


def boden(bild):
    """Flacher Sandboden – jede Stufe kostet in allen 255 Bildern Platz (Matrix: 80 KB)."""
    bild.rechteck(0, 14, B, 1, SAND_HELL)
    bild.rechteck(0, 15, B, 1, SAND)


def stall(bild, f, licht):
    x0 = STALL_X
    innen = mischen((14, 8, 2), (95, 46, 4), licht)
    bild.rechteck(x0 + 2, 9, 14, 5, innen)                         # Innenraum
    for k in range(4):                                             # Strohdach
        bild.linie(x0 + 2 * k, 8 - k, x0 + 17 - 2 * k, 8 - k, DACH if k >= 1 else BALKEN)
    bild.rechteck(x0 + 1, 9, 1, 5, BALKEN)                         # Pfosten
    bild.rechteck(x0 + 16, 9, 1, 5, BALKEN)
    if licht <= 0.3:
        return
    h = min(1, (licht - 0.3) / 0.5)
    blau = dimmen((40, 90, 255), h)
    # Maria (links, blau, kniet)
    bild.rechteck(x0 + 4, 10, 2, 4, blau)
    bild.setze(x0 + 6, 12, blau)
    bild.setze(x0 + 6, 13, blau)
    bild.setze(x0 + 5, 9, dimmen(HAUT, h))
    bild.setze(x0 + 4, 9, blau)
    # Josef (rechts, grün, mit Stab)
    gruen = dimmen((0, 170, 70), h)
    bild.rechteck(x0 + 12, 10, 2, 4, gruen)
    bild.setze(x0 + 12, 9, dimmen(HAUT, h))
    bild.setze(x0 + 13, 9, dimmen((150, 90, 40), h))
    bild.rechteck(x0 + 14, 9, 1, 5, dimmen((230, 190, 120), h))
    # Krippe mit Kind
    bild.rechteck(x0 + 8, 12, 3, 1, dimmen(STROH, h))
    bild.setze(x0 + 7, 11, dimmen(STROH, h))
    bild.setze(x0 + 11, 11, dimmen(STROH, h))
    bild.setze(x0 + 8, 13, dimmen(BALKEN, h))
    bild.setze(x0 + 10, 13, dimmen(BALKEN, h))
    puls = (0.8, 1.0, 0.9, 1.0)[(f // 5) % 4]
    bild.rechteck(x0 + 8, 11, 3, 1, dimmen(WEISS, h * puls))
    if h >= 1:                                                     # Heiligenschein
        bild.rechteck(x0 + 8, 10, 3, 1, dimmen(GELB, 0.75 * puls))
        bild.setze(x0 + 9, 9, dimmen(GELB, 0.45 * puls))


def stern(bild, x, y, f, schweif):
    stufe = (f // 3) % 4                                           # ruhiges Funkeln
    lang = (3, 4, 3, 2)[stufe] if schweif else (2, 3, 2, 2)[stufe]
    for d in range(1, lang + 1):
        c = dimmen(GELB, (1.0, 0.75, 0.45, 0.25)[d - 1])
        for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
            bild.setze(x + dx, y + dy, c)
    diag = dimmen(GOLD, (0.5, 0.8, 0.5, 0.3)[stufe])
    for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        bild.setze(x + dx, y + dy, diag)
    bild.setze(x, y, WEISS)
    for k in range(schweif):                                       # Schweif nach links oben
        bild.setze(x - 3 - k, y - 1 - k // 4, dimmen(GOLD, (0.8, 0.5, 0.25)[k // 4]))
        if k % 2 == 0 and k < schweif - 2:
            bild.setze(x - 3 - k, y - k // 4, dimmen(GOLD, (0.45, 0.25, 0.12)[k // 4]))


def ohne_doppelte(liste):
    """Pillow legt gleiche Nachbarbilder im GIF zusammen – dann wären es weniger als 255 Bilder.
    Ist ein Bild gleich seinem Vorgänger, ändert ein Punkt unsichtbar die Farbe (Blau um 1)."""
    for i in range(1, len(liste)):
        if liste[i].px == liste[i - 1].px:
            r, g, b = liste[i].px[1][1]
            liste[i].px[1][1] = (r, g, b + 1 if b < 255 else b - 1)
    return liste


def bilder():
    liste = []
    gewaender = [ROT, LILA, (0, 190, 150)]
    for f in range(255):
        bild = Bild(NACHTBLAU)
        STERNE.zeichnen(bild, f)
        boden(bild)
        # Stern zieht 0–80 von links herüber und bleibt über dem Stall
        t = min(1, f / 80)
        weich = t * t * (3 - 2 * t)
        sx = round(-4 + (STERN_ZIEL[0] + 4) * weich)
        sy = round(5 - 3 * t - 1.5 * math.sin(math.pi * t))
        licht = 0.0 if f < 80 else min(1, (f - 80) / 25)
        stall(bild, f, licht)
        if f >= 80:                                                # Lichtstrahl auf den Giebel
            for y in range(sy + 1, 5):
                bild.setze(sx, y, dimmen(GELB, 0.5 if (y + f // 4) % 2 else 0.3))
        stern(bild, sx, sy, f, 9 if f < 76 else max(0, 9 - (f - 76)))
        # Karawane: drei Könige auf Kamelen, 13 Pixel Abstand
        weg = min(40, (f - 70) / 3) if f >= 70 else None
        if weg is not None:
            laeuft = weg < 40
            for i in range(3):
                x = round(-11 + weg) - i * 13
                gang = (f // 5) % 2 if laeuft else 0    # alle im Gleichschritt: gleiche Spalten
                nick = 1 if not laeuft and (f - 190 - i * 14) % 64 in range(40, 52) else 0
                bild.figur(x, 5, KAMEL_FIGUR[gang],
                           {"k": KAMEL, "d": KAMEL_DUNKEL, "t": KAMEL_DUNKEL, "c": GOLD, "h": HAUT,
                            "m": gewaender[i]})
                if nick:                                           # König verneigt sich
                    bild.rechteck(x + 3, 5, 2, 2, NACHTBLAU)
                    bild.rechteck(x + 5, 6, 2, 1, HAUT)
                    bild.setze(x + 7, 6, GOLD)
        liste.append(bild)
    return ohne_doppelte(liste)
