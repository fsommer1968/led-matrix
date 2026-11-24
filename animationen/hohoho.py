"""HO HO HO: große, fette Buchstaben springen herein und hüpfen paarweise im Lach-Takt
(HO – HO – HO), bei jeder Landung platzt Konfetti und das Paar wechselt die Farbe; der
Zuckerstangen-Rahmen läuft ruhig um. Danach "FROHE WEIHNACHTEN" in gleich großer Schrift mit
Zuckerstangen-Streifen – 255 Bilder.

0–124   HO HO HO
124–255 FROHE WEIHNACHTEN läuft durch
"""
import random

from basis import (B, GOLD, HELLBLAU, PINK, ROT, WEISS, Bild, dimmen)

NAME = "hohoho"
TITEL = "HO HO HO mit Zuckerstangen-Rahmen"

HINTERGRUND = (12, 0, 4)
GRUEN = (0, 220, 40)
RAHMEN_WEISS = (210, 210, 210)
PALETTE = [ROT, GRUEN, GOLD, WEISS, PINK, HELLBLAU]
ENDE_HO = 124
TAKT = 36                                        # ein Lacher: drei Paare je 12 Bilder

# fette Buchstaben, 10 hoch, Strichstärke 2
GROSS = {
    "H": ["11...11", "11...11", "11...11", "11...11", "1111111", "1111111", "11...11", "11...11",
          "11...11", "11...11"],
    "O": [".11111.", "1111111", "11...11", "11...11", "11...11", "11...11", "11...11", "11...11",
          "1111111", ".11111."],
}
LAUF = {
    "F": ["111111", "111111", "11....", "11....", "11111.", "11111.", "11....", "11....", "11....",
          "11...."],
    "R": ["11111.", "111111", "11..11", "11..11", "111111", "11111.", "11.11.", "11..11", "11..11",
          "11..11"],
    "O": [".1111.", "111111", "11..11", "11..11", "11..11", "11..11", "11..11", "11..11", "111111",
          ".1111."],
    "H": ["11..11", "11..11", "11..11", "11..11", "111111", "111111", "11..11", "11..11", "11..11",
          "11..11"],
    "E": ["111111", "111111", "11....", "11....", "11111.", "11111.", "11....", "11....", "111111",
          "111111"],
    "W": ["11...11", "11...11", "11...11", "11...11", "11.1.11", "11.1.11", "11.1.11", "1111111",
          "1111111", ".11.11."],
    "I": ["1111", "1111", ".11.", ".11.", ".11.", ".11.", ".11.", ".11.", "1111", "1111"],
    "N": ["11...11", "111..11", "111..11", "1111.11", "11.1.11", "11.1111", "11..111", "11..111",
          "11...11", "11...11"],
    "A": [".1111.", "111111", "11..11", "11..11", "11..11", "111111", "111111", "11..11", "11..11",
          "11..11"],
    "C": [".1111.", "111111", "11..11", "11....", "11....", "11....", "11....", "11..11", "111111",
          ".1111."],
    "T": ["111111", "111111", "..11..", "..11..", "..11..", "..11..", "..11..", "..11..", "..11..",
          "..11.."],
    " ": ["..."] * 10,
}
TEXT = "FROHE WEIHNACHTEN"
TEXT_BREITE = sum(len(LAUF[z][0]) + 2 for z in TEXT) - 2
RAND = [(x, 0) for x in range(B)] + [(B - 1, y) for y in range(1, 16)] + \
       [(x, 15) for x in range(B - 2, -1, -1)] + [(0, y) for y in range(14, 0, -1)]


def rahmen(bild, f):
    """Zuckerstangen-Rahmen: rot/weiß, wandert alle zwei Bilder um einen Punkt."""
    for i, (x, y) in enumerate(RAND):
        bild.setze(x, y, ROT if (i + f // 2) % 6 < 3 else RAHMEN_WEISS)


def glyphe(bild, x, y, zeilen, farbe):
    """farbe: Farbe oder f(gx, gy) → Farbe; zeichnet nur innerhalb des Rahmens."""
    for gy, zeile in enumerate(zeilen):
        for gx, p in enumerate(zeile):
            if p == "1" and 1 <= x + gx < B - 1 and 1 <= y + gy < 15:
                bild.setze(x + gx, y + gy, farbe(gx, gy) if callable(farbe) else farbe)


def konfetti(funken, z, x, y, anzahl=12):
    for _ in range(anzahl):
        funken.append([x + z.uniform(-5, 5), y + z.uniform(-1, 1), z.uniform(-1.5, 1.5),
                       z.uniform(-0.7, 0.3), PALETTE[z.randrange(len(PALETTE))], 0])


def ohne_doppelte(liste):
    """Pillow legt gleiche Nachbarbilder im GIF zusammen – dann wären es weniger als 255 Bilder.
    Ist ein Bild gleich seinem Vorgänger, ändert ein Punkt unsichtbar die Farbe (Blau um 1)."""
    for i in range(1, len(liste)):
        if liste[i].px == liste[i - 1].px:
            r, g, b = liste[i].px[1][1]
            liste[i].px[1][1] = (r, g, b + 1 if b < 255 else b - 1)
    return liste


def bilder():
    z = random.Random(99)
    funken = []
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        if f < ENDE_HO:
            for i, c in enumerate("HOHOHO"):
                paar = i // 2
                x = 6 + paar * 19 + (i % 2) * 8
                start = i * 4
                if f < start:
                    continue
                t = f - start
                lach = f - 30 - paar * 12 - (i % 2) * 2             # Lach-Takt ab Bild 30
                runde = max(0, lach) // TAKT if f >= 30 else -1
                if t < 8:                                           # springt von unten herein
                    hoch = (-10, -5, -1, 2, 3, 3, 2, 1)[t]
                elif lach >= 0 and lach % TAKT < 9:
                    hoch = (1, 2, 3, 3, 3, 2, 2, 1, 0)[lach % TAKT]
                else:
                    hoch = 0
                if f >= ENDE_HO - 14:                               # fallen am Ende nacheinander weg
                    g = f - (ENDE_HO - 14) - i
                    hoch = -(g * g) // 3 if g > 0 else hoch
                gelandet = runde + (1 if lach >= 0 and lach % TAKT >= 8 else 0) if f >= 30 else 0
                farbe = PALETTE[(i % 2 + 2 * gelandet + (paar if gelandet else 0)) % len(PALETTE)]
                if (t == 8 or (lach >= 0 and lach % TAKT == 8)) and i % 2 == 0 and f < ENDE_HO - 16:
                    konfetti(funken, z, x + 7, 3)
                glyphe(bild, x, 3 - hoch, GROSS[c], farbe)
        else:
            g = f - ENDE_HO
            x = B - 2 - (g * 3) // 2
            for c in TEXT:
                glyphe(bild, x, 3, LAUF[c], lambda gx, gy: ROT if (gx + gy) % 5 == 0 else WEISS)
                x += len(LAUF[c][0]) + 2
        for s in funken:
            if 1 <= s[0] < B - 1 and 1 <= s[1] < 15:
                bild.setze(s[0], s[1], dimmen(s[4], 1 if s[5] < 12 else 1 - (s[5] - 11) / 7))
            s[0] += s[2]
            s[1] += s[3]
            s[3] += 0.1
            s[5] += 1
        funken = [s for s in funken if s[5] < 17]
        rahmen(bild, f)
        liste.append(bild)
    return ohne_doppelte(liste)
