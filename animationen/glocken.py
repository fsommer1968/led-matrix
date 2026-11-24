"""Glocken: zwei goldene Glocken mit Schleife am Tannenzweig schwingen (echt gedreht), bei jedem
Anschlag fliegt eine bunte Note los, dazwischen läuft "KLING GLOECKCHEN" in Farben – 255 Bilder.
"""
import math

from basis import (B, BUNT, DUNKELGRUEN, GOLD, GRUEN, ROT, WEISS, Bild, Sterne, regenbogen,
                   textbreite)

NAME = "glocken"
TITEL = "Schwingende Glocken mit Noten"

GLANZ = (255, 235, 140)
SCHATTEN = (205, 100, 0)
RAND = (255, 185, 30)
KLOEPPEL = (200, 70, 0)
FARBEN = {"g": GOLD, "h": GLANZ, "d": SCHATTEN, "r": RAND, "k": KLOEPPEL}
PROFIL = [1.5, 2.2, 2.6, 2.9, 3.1, 3.6, 4.2]        # halbe Breite der Glocke je Zeile ab der Krone
SCHLEIFE = ["rr...rr", "rrrkrrr", ".r...r."]
NOTEN = [["..nn", "..n.", "..n.", "nnn.", "nnn."],
         [".nnnn", ".n..n", ".n..n", "nn.nn", "nn.nn"]]
HINTERGRUND = (10, 0, 20)
STERNE = Sterne(anzahl=0)                           # drei Sterne zwischen den Glocken (jeder kostet Speicher)
STERNE.sterne = [(31, 2, 13, 24), (40, 0, 16, 32), (23, 4, 32, 40)]     # x, y, Phase, Periode
TEXT = "KLING GLOECKCHEN KLINGELINGELING"
MITTE = (17, 47)                                    # Schrift und Sterne nur zwischen den Glocken
SCHLAEGE = 9                                        # Schwünge je Durchlauf (läuft nahtlos um)
AUSSCHLAG = 0.48


def teil(u, v, kloeppel):
    """Was liegt an der Stelle (u quer, v längs der Achse ab Aufhängung)? None = nichts."""
    if 0 <= v < 1:
        return "g" if abs(u) <= 0.8 else None
    if 1 <= v < 7.4:
        i = min(len(PROFIL) - 2, int(v - 1))
        w = PROFIL[i] + (PROFIL[i + 1] - PROFIL[i]) * min(1.0, v - 1 - i)
        if abs(u) <= w:
            if v >= 6.3:
                return "r"
            if -0.8 * w <= u <= -0.35 * w and 1.6 <= v <= 5.4:
                return "h"
            return "d" if u > 0.5 * w else "g"
    if (u - kloeppel) ** 2 + (v - 8.0) ** 2 <= 1.3:
        return "k"
    return None


def glocke(bild, cx, py, winkel, kloeppel):
    """Glocke um die Aufhängung (cx, py) gedreht; je Pixel 3×3 Proben, die Mehrheit zählt."""
    s, c = math.sin(winkel), math.cos(winkel)
    for y in range(py, py + 11):
        for x in range(cx - 10, cx + 11):
            treffer = {}
            for sy in (-0.33, 0, 0.33):
                for sx in (-0.33, 0, 0.33):
                    dx, dy = x + sx - cx, y + sy - py
                    t = teil(dx * c - dy * s, dx * s + dy * c, kloeppel)
                    if t:
                        treffer[t] = treffer.get(t, 0) + 1
            if sum(treffer.values()) >= 5:
                bild.setze(x, y, FARBEN[max(treffer, key=treffer.get)])


def schleife(bild, cx):
    """Tannenzweig mit roter Schleife über der Glocke."""
    for dx in range(-8, 9):                         # Zickzack mit nur zwei Spaltenmustern (Speicher)
        if abs(dx) > 2:
            bild.setze(cx + dx, abs(dx) % 2, GRUEN)
            bild.setze(cx + dx, 1 - abs(dx) % 2, DUNKELGRUEN if abs(dx) % 2 else None)
    bild.figur(cx - 3, 0, SCHLEIFE, {"r": ROT, "k": GOLD})


def bilder():
    breite = textbreite(TEXT)
    noten = []                                      # [x, y, Farbe, Richtung, Sorte, Alter]
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        stern = Bild(None)
        STERNE.zeichnen(stern, f)
        for y in range(7):
            for xx in range(*MITTE):
                if stern.px[y][xx] is not None:
                    bild.setze(xx, y, stern.px[y][xx])
        # Schrift in der Mitte (nur zwischen den Glocken sichtbar)
        x = B - (f * 2) % (breite + B)
        schrift = Bild(None)
        schrift.text(x, 9, TEXT, lambda i: regenbogen(i * 20 + f * 8))
        for y in range(16):
            for xx in range(*MITTE):
                if schrift.px[y][xx] is not None:
                    bild.setze(xx, y, schrift.px[y][xx])
        phase = 2 * math.pi * SCHLAEGE * f / 255
        for i, cx in enumerate((8, 55)):
            p = phase       # beide im Gleichtakt: die zweite Glocke ist ein Abbild der ersten und
            #                 kostet im Speicher der Matrix (80 KB, jedes Bild einzeln gepackt) fast nichts
            winkel = AUSSCHLAG * math.sin(p)
            glocke(bild, cx, 3, winkel, 1.7 * math.sin(p + 1.2))
            schleife(bild, cx)
            innen = math.sin(p) * (1 if i == 0 else -1)     # > 0: schwingt zur Mitte
            vorher = math.sin(phase - 2 * math.pi * SCHLAEGE / 255) * (1 if i == 0 else -1)
            if innen > 0.9 >= vorher:                       # Anschlag innen: eine Note fliegt los
                n = len(noten) + f // 28
                noten.append([cx + (9 if i == 0 else -12), 3.0, BUNT[(n * 2 + i) % len(BUNT)],
                              1 if i == 0 else -1, n % 2, 0])
            if innen > 0.9:                                 # Anschlag blitzt am Rand
                bild.setze(cx + (1 if i == 0 else -1) * 7, 9, WEISS)
        for n in noten:                                     # Noten steigen wiegend zur Mitte
            bild.figur(round(n[0]), round(n[1] + 0.6 * math.sin(n[5] / 4)), NOTEN[n[4]], {"n": n[2]})
            n[0] += n[3] * 0.3
            n[1] -= 0.22
            n[5] += 1
        noten = [n for n in noten if n[1] > -6]
        liste.append(bild)
    return liste
