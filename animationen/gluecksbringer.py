"""Glücksbringer: Kleeblatt, Hufeisen, Glücksschwein und Schornsteinfeger (mit Leiter) fallen
nacheinander groß ins Bild und hüpfen, Glitzersterne funkeln; zum Schluss rahmen Kleeblatt und
Hufeisen ein großes "VIEL", dann Schwein und Schornsteinfeger ein großes "GLÜCK" – 255 Bilder.
"""
import math
import random

from basis import B, GELB, GOLD, ROT, SCHRIFT, WEISS, Bild, mischen
from feuerwerk import jedes_bild_anders

NAME = "gluecksbringer"
TITEL = "Glücksbringer: Kleeblatt, Hufeisen, Schwein, Schornsteinfeger"

HINTERGRUND = (0, 12, 6)

KLEEBLATT = ["....xx.xx....",
             "...xLxxxxx...",
             "...xLxxxxx...",
             ".xx.xxxxx.xx.",
             "xLLx.xxx.xxxx",
             "xLxxx.x.xxxxx",
             ".xxxxxxxxxxx.",
             "xxxxx.x.xxxxx",
             "xLxx.xxx.xxxx",
             ".xx.xLxxxsxx.",
             "...xLxxxxxs..",
             "...xxxxxxx.s.",
             "....xx.xx..s.",
             "..........ss."]
KLEE_FARBEN = {"x": (0, 200, 40), "L": (120, 255, 90), "s": (90, 150, 0)}

HUFEISEN = ["..xxx....xxx..",
            ".wxx......xxx.",
            ".wox......xox.",
            "wxx........xxx",
            "wox........xox",
            "wxx........xxx",
            "wox........xox",
            "wxx........xxx",
            ".wxx......xxx.",
            ".woxx....xxox.",
            "..wxxxxxxxxx..",
            "...xxxxxxxx...",
            ".....xxxx....."]
HUF_FARBEN = {"x": (150, 170, 215), "w": (235, 240, 255), "o": (40, 40, 70)}

SCHWEIN = ["..........e.e..",
           "...pppppppeepp.",
           "t.pppppppppkppn",
           ".tpppppppppppnn",
           "..ppppppppppnon",
           "..pppppppppppn.",
           "..ppppppppppp..",
           "..pp.pp..pp.pp.",
           "..hh.hh..hh.hh."]
SCHWEIN_FARBEN = {"p": (255, 110, 160), "e": (225, 40, 110), "n": (255, 170, 200), "o": (150, 20, 70),
                  "k": (25, 0, 20), "t": (225, 40, 110), "h": (200, 60, 110)}

FEGER = ["..hhhhh......",
         "..hhhhh......",
         "..bbbbb...l.l",
         ".hhhhhhh..lll",
         "..sssss...l.l",
         "..sksks...lll",
         "..sssss...l.l",
         "..rrrrr...lll",
         ".jjjgjjj..l.l",
         "jjjjjjjjjslll",
         "jjjjgjjj..l.l",
         "s.jjjjj...lll",
         "..jj.jj...l.l",
         "..jj.jj...lll"]
FEGER_FARBEN = {"h": (85, 85, 115), "b": (160, 160, 190), "s": (255, 170, 110), "k": (30, 20, 30), "r": ROT,
                "j": (70, 70, 100), "g": GOLD, "l": (215, 125, 35)}

# (Figur, Farben, Platz in der Reihe, Platz neben der Schrift)
FIGUREN = [(KLEEBLATT, KLEE_FARBEN, 0, 2), (HUFEISEN, HUF_FARBEN, 16, 48),
           (SCHWEIN, SCHWEIN_FARBEN, 33, 0), (FEGER, FEGER_FARBEN, 51, 51)]
JE_FIGUR = 40
WELLE = 160
ABGANG = 178                                    # alle tauchen nach unten ab
VIEL = (186, 220)
GLUECK = (224, 256)


# Buchstaben, die fett anders besser lesbar sind: G mit offenem Bauch (sonst wie eine 6), Ü ohne Punkte
FETT = {"G": ["01110", "10001", "10000", "10011", "10001", "10001", "01110"],
        "Ü": ["00000", "00000", "10001", "10001", "10001", "10001", "01110"]}


def fett_text(bild, x, y, text, farbe):
    """5×7-Schrift doppelt hoch und einen Pixel fetter (6 breit, 1 Abstand)."""
    for i, z in enumerate(text):
        c = farbe(i) if callable(farbe) else farbe
        if c is None:
            continue
        for gy, zeile in enumerate(FETT.get(z, SCHRIFT[z])):
            for gx, p in enumerate(zeile):
                if p == "1":
                    bild.rechteck(x + i * 7 + gx, y + gy * 2, 2, 2, c)
        if z == "Ü":                                               # zwei getrennte Punkte
            bild.rechteck(x + i * 7 + 1, y, 1, 2, c)
            bild.rechteck(x + i * 7 + 4, y, 1, 2, c)


def fall(t):
    """Höhe über dem Boden beim Hereinfallen: Sturz, dann zwei kleiner werdende Hüpfer."""
    if t < 7:
        return round(18 * (1 - (t / 7) ** 2))
    if t < 13:
        return round(3 * math.sin(math.pi * (t - 7) / 6))
    if t < 17:
        return round(1.4 * math.sin(math.pi * (t - 13) / 4))
    return 0


def hopser(t, hoehe=2, dauer=6):
    return round(hoehe * math.sin(math.pi * t / dauer)) if 0 <= t < dauer else 0


def zeichne_figur(bild, f, i, x, hoch):
    figur, farben = FIGUREN[i][0], FIGUREN[i][1]
    y = 16 - len(figur) - hoch
    bild.figur(x, y, figur, farben)
    if i == 1:                                                     # Glanz läuft über das Hufeisen
        k = (f // 2) % 24
        bahn = [(1, 8), (0, 7), (0, 5), (0, 3), (1, 1), (2, 0)]
        if k < len(bahn):
            bild.setze(x + bahn[k][0], y + bahn[k][1], WEISS)
            bild.setze(x + 13 - bahn[k][0], y + bahn[k][1], WEISS)
    if i == 2 and (f // 6) % 2:                                    # Ringelschwanz wackelt
        bild.setze(x, y + 2, HINTERGRUND)
        bild.setze(x, y + 4, SCHWEIN_FARBEN["t"])
    if i == 2 and f % 50 in (30, 31):                              # blinzelt
        bild.setze(x + 11, y + 2, SCHWEIN_FARBEN["p"])


def glitzer(bild, f, sterne):
    """Kleine Sterne (Punkt → Kreuz → Punkt) an freien Stellen."""
    for x, y, start, farbe in sterne:
        t = f - start
        if not 0 <= t < 8:
            continue
        kreuz = [(0, 0)] + ([(1, 0), (-1, 0), (0, 1), (0, -1)] if 2 <= t < 6 else [])
        if all(bild.hole(x + dx, y + dy) in (HINTERGRUND, None) for dx in range(-2, 3) for dy in range(-2, 3)):
            for dx, dy in kreuz:
                bild.setze(x + dx, y + dy, farbe if (dx, dy) != (0, 0) else WEISS)


def bilder():
    z = random.Random(13)
    sterne = [(z.randrange(1, B - 1), z.randrange(1, 15), s, z.choice((GELB, GOLD, (120, 255, 90))))
              for s in range(4, 252, 2)]
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        for i, (figur, farben, platz, rand) in enumerate(FIGUREN):
            start = i * JE_FIGUR
            if f < start:
                continue
            x = platz
            if f < ABGANG:
                hoch = fall(f - start)
                if f - start >= 17:                                # steht: ab und zu ein Hüpfer
                    hoch = hopser((f + i * 9) % 36, 1, 5)
                if f >= WELLE:                                     # alle da: La Ola, zweimal
                    hoch = max(hopser(f - WELLE - i * 3, 3, 7), hopser(f - WELLE - 9 - i * 3, 3, 7))
            elif f < VIEL[0]:
                hoch = -2 * (f - ABGANG + 1)                       # taucht ab
            else:
                x = rand
                von, bis = VIEL if i < 2 else GLUECK
                if not von <= f < bis:
                    continue
                hoch = min(0, -16 + 3 * (f - von), -16 + 3 * (bis - 1 - f) if bis < 255 else 0)
                if hoch == 0:
                    hoch = hopser((f - von + i * 11) % 22, 2, 6)
            if hoch > -16:
                zeichne_figur(bild, f, i, x, hoch)
        for text, (von, bis), x0 in (("VIEL", VIEL, 18), ("GLÜCK", GLUECK, 16)):
            if von + 3 <= f < bis - 2:
                def farbe(k):
                    t = f - von - 3 - k * 2
                    if t < 0:
                        return None
                    if t < 2:
                        return WEISS
                    return mischen(GOLD, GELB, round(2 + 2 * math.sin(f / 3.5 - k * 1.2)) / 4)
                fett_text(bild, x0, 1, text, farbe)
        glitzer(bild, f, sterne)
        liste.append(bild)
    return jedes_bild_anders(liste, HINTERGRUND)
