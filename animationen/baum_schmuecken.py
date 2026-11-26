"""Baum schmücken: ein kahler Tannenbaum bekommt eine Lichterkette (in Bahnen von unten nach
oben), dann fliegen die Kugeln eine nach der anderen heran, Lametta fällt und glitzert, der Stern
schwebt auf die Spitze, zuletzt landen die Geschenke unter dem Baum – 255 Bilder.
"""
import colorsys
import math

from basis import (B, GELB, GOLD, HELLBLAU, PINK, ROT, WEISS, Bild, dimmen, mischen)

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "baum_schmuecken"
TITEL = "Tannenbaum wird geschmückt"

WAND = (26, 8, 12)
BODEN = (33, 17, 5)
TANNE = (0, 105, 28)
TANNE_HELL = (0, 150, 40)
TANNE_DUNKEL = (0, 62, 18)
STAMM = (41, 21, 5)
LICHT = (255, 200, 80)
SILBER = (190, 210, 255)
RAHMEN = (41, 22, 7)
NACHT = (0, 0, 48)
CX = 32
# halbe Breite je Zeile (y = 2…13): drei Etagen
BREITE = {2: 0, 3: 1, 4: 2, 5: 3, 6: 2, 7: 4, 8: 5, 9: 6, 10: 4, 11: 6, 12: 8, 13: 10}
FLOCKE = (150, 165, 215)
# Schnee vor dem Fenster: (Runden je Durchlauf, Startphase, Spalten im Fenster je Runde). Beide
# Fenster zeigen dieselben Flocken – so bleibt das rechte Fenster für die Kompression eine reine
# Kopie des linken (die Matrix speichert nur 80 KB je Animation).
FLOCKEN = [(3, 1.0, (1, 7, 3)), (4, 7.5, (6, 2, 8, 0))]


def kette():
    """Lichterkette als Spirale: nur die vordere Hälfte jeder Windung, Lichter mit Abstand."""
    punkte = []
    for k in range(600):
        t = k / 600
        y = 13.4 - 10.4 * t
        w = t * 2 * math.pi * 4.5
        if math.cos(w) <= -0.15:                                   # hinter dem Baum
            continue
        hb = BREITE[max(2, min(13, round(y)))]
        p = (CX + round(hb * 0.9 * math.sin(w)), round(y))
        if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) >= 3 or abs(p[1] - q[1]) >= 2 for q in punkte[-3:]) \
                and p not in punkte and abs(p[0] - CX) <= BREITE[p[1]]:
            punkte.append(p)
    return punkte


KETTE = kette()
# Kugeln 2×2: (x, y, Farbe), von unten nach oben
KUGELN = [(24, 12, ROT), (38, 12, (0, 90, 255)), (31, 11, PINK), (28, 8, HELLBLAU), (35, 8, ROT),
          (31, 5, (0, 90, 255)), (35, 11, GELB), (27, 11, (190, 0, 255))]
# Lametta: (x, y oben, Länge)
LAMETTA = [(30, 12, 2), (34, 12, 2), (22, 13, 1), (42, 13, 1), (26, 9, 2), (38, 9, 2), (32, 8, 3),
           (29, 5, 2), (35, 5, 2), (33, 3, 2)]
# Geschenke: (x, Breite, Höhe, Farbe, Band, Bild, ab dem es fällt)
GESCHENKE = [(15, 6, 4, ROT, GELB, 216), (44, 5, 3, (0, 90, 255), WEISS, 223),
             (9, 5, 3, (0, 170, 40), ROT, 230), (50, 6, 5, PINK, GELB, 237)]


def fenster(bild, x0, f):
    """Fenster zur Winternacht: draußen schneit es."""
    bild.rechteck(x0, 2, 11, 8, RAHMEN)
    bild.rechteck(x0 + 1, 3, 9, 6, NACHT)
    for runden, phase, spalten in FLOCKEN:                         # 12 Zeilen je Runde, 5 sichtbar
        weg = phase + f * runden * 12 / 255
        x, y = x0 + 1 + spalten[int(weg // 12) % runden], int(weg % 12)
        if bild.hole(x, y) == NACHT:
            bild.setze(x, y, FLOCKE)
    bild.rechteck(x0 + 5, 3, 1, 6, RAHMEN)
    bild.rechteck(x0 + 1, 5, 9, 1, RAHMEN)
    bild.rechteck(x0, 10, 11, 1, RAHMEN)                           # Fensterbank


def baum(bild):
    for y, hb in BREITE.items():
        farbe = TANNE_DUNKEL if y in (6, 10) else TANNE_HELL if y in (5, 9, 13) else TANNE
        bild.rechteck(CX - hb, y, 2 * hb + 1, 1, farbe)
    bild.rechteck(CX - 1, 14, 3, 1, STAMM)
    bild.rechteck(CX - 3, 15, 7, 1, (170, 30, 30))                 # Ständer


def stern(bild, x, y, f, strahlt):
    x, y = int(round(x)), int(round(y))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        bild.setze(x + dx, y + dy, GELB)
    bild.setze(x, y, WEISS)
    if strahlt:
        puls = (f // 4) % 2
        for dx, dy in ((2, 0), (-2, 0)):
            bild.setze(x + dx, y + dy, dimmen(GOLD, 0.9 if puls else 0.4))
        for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            bild.setze(x + dx, y + dy, dimmen(GOLD, 0.4 if puls else 0.9))


def _matrixfarbe(c):
    """Farbe, wie die Matrix sie zeigt (7/4/5 Bit H/S/V, wie hsv16 in pi/matrix_spieler.py)."""
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return round(h * 127) & 0x7F, round(s * 15), round(v * 31)


def _jedes_bild_anders(liste):
    """Gleiche Nachbarbilder legt PIL im GIF zu einem zusammen – dann fehlen Bilder, und die
    Matrix (fester Takt) läuft an ruhigen Stellen schneller. Ein Bild, das seinem Vorgänger
    gleicht, bekommt darum an einem Pixel einen um 1 anderen Farbwert, den die Matrix genauso
    zeigt: im GIF verschieden, auf den LEDs unsichtbar."""
    for vor, bild in zip(liste, liste[1:]):
        if bild.px != vor.px:
            continue
        stellen = ((y, x, k, d) for y in range(16) for x in range(64) for k in range(3)
                   for d in (1, -1))
        for y, x, k, d in stellen:
            c = bild.px[y][x]
            n = tuple(w + d if i == k else w for i, w in enumerate(c))
            if 0 <= n[k] <= 255 and _matrixfarbe(n) == _matrixfarbe(c):
                bild.px[y] = bild.px[y][:x] + [n] + bild.px[y][x + 1:]
                break
    return liste


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(WAND)
        fenster(bild, 2, f)
        fenster(bild, 51, f)
        bild.rechteck(0, 15, B, 1, BODEN)
        baum(bild)
        # 8–76 Lichterkette wächst von unten nach oben, danach funkelt sie ruhig
        n = min(len(KETTE), max(0, (f - 8) * len(KETTE) // 66))
        for i, (x, y) in enumerate(KETTE[:n]):
            if f < 78:
                farbe = WEISS if i >= n - 2 else LICHT
            else:
                farbe = dimmen(LICHT, 0.55 + 0.15 * round(1.5 + 1.5 * math.sin(f / 5 + i * 2.4)))
            bild.setze(x, y, farbe)
        # 150–190 Lametta fällt Faden für Faden und glitzert
        for i, (x, y, laenge) in enumerate(LAMETTA):
            t = f - (150 + i * 4)
            if t < 0:
                continue
            for k in range(laenge):
                if t < 5:                                          # fällt von oben herab
                    yy = y + k - (5 - t) * 2
                else:
                    yy = y + k
                glanz = (f // 3 + i * 2 + k) % 5 == 0
                bild.setze(x, yy, WEISS if glanz else SILBER)
        # 80–148 Kugeln fliegen im Bogen heran, abwechselnd von links und rechts
        for i, (x, y, farbe) in enumerate(KUGELN):
            t = (f - (80 + i * 8)) / 12
            if t < 0:
                continue
            if t < 1:
                x0 = 14 if i % 2 == 0 else 49
                kx = x0 + (x - x0) * t
                ky = 13 + (y - 13) * t - 9 * t * (1 - t)
            else:
                kx, ky = x, y
            bild.rechteck(int(round(kx)), int(round(ky)), 2, 2, farbe)
            if t >= 1:
                bild.setze(kx, ky, mischen(farbe, WEISS, 0.55))   # Glanzlicht
        # 192–214 Stern schwebt im Bogen auf die Spitze, dann strahlt er
        if f >= 192:
            t = min(1.0, (f - 192) / 22)
            sx = 10 + (CX - 10) * t
            sy = 1 + 11 * (1 - t) ** 2
            if t < 1:
                for k in (1, 2, 3):                                # Funkenschweif
                    tk = max(0.0, t - k * 0.05)
                    bild.setze(10 + (CX - 10) * tk, 1 + 11 * (1 - tk) ** 2 + 1, dimmen(GOLD, 0.7 - 0.18 * k))
            stern(bild, sx, sy, f, strahlt=t >= 1)
        # 216–245 Geschenke landen unter dem Baum
        for x, b, h, farbe, band, start in GESCHENKE:
            t = f - start
            if t < 0:
                continue
            y = min(15 - h, -h + t * 3)
            if t in (6, 7) and y == 15 - h:                        # kleiner Hüpfer
                y -= 1
            bild.rechteck(x, y, b, h, farbe)
            bild.rechteck(x + b // 2 - (b % 2 == 0), y, 2 - b % 2, h, band)
            bild.rechteck(x, y + h // 2, b, 1, band)
        liste.append(bild)
    return _jedes_bild_anders(liste)
