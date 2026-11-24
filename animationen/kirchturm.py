"""Kirchturmuhr schlägt Mitternacht: verschneites Dorf bei Nacht, in der Mitte der Kirchturm mit
Haube und großem, hell erleuchtetem Zifferblatt. Der große Zeiger rückt in vier Schritten auf zwölf;
stehen beide oben, schwingt im Schallfenster die Glocke, und zu jedem der zwölf Schläge läuft links
und rechts ein Schallbogen in die Nacht. Dann steigen hinter den Dächern und dem Turm Raketen auf,
ihr Schein färbt den Schnee, in den Häusern gehen die Fenster an. Zum Schluss verglimmt das
Feuerwerk, die Fenster gehen aus, und der große Zeiger läuft im Zeitraffer einmal herum, bis er
wieder zehn vor zwölf steht – 255 Bilder, die Runde geht ohne Sprung in sich über.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Häuser aus zwei Vorlagen (gleiche Häuser ergeben
gleiche Spaltenfolgen und kosten fast nichts), Fenster zwei Spalten breit, vier Sterne, je Rakete
nur acht Funken außen und vier innen. Der Widerschein auf dem Schnee und das Glimmen im
Schallfenster ändern nur Farben und kosten darum keinen Speicher.
"""
import math

from basis import GELB, GOLD, HELLBLAU, LILA, PINK, ROT, TUERKIS, WEISS, Bild, dimmen, mischen

NAME = "kirchturm"
TITEL = "Kirchturmuhr schlägt Mitternacht"

HIMMEL = (0, 0, 14)
SCHNEE = (120, 130, 175)                       # Schnee auf Dächern und Mauern (gedämpft)
DACH = (44, 36, 84)
WAND = (28, 25, 60)
KAMIN = (90, 40, 40)
LICHT = (255, 170, 40)                         # erleuchtetes Fenster
STERN = (255, 240, 200)
STERNE = [(6, 1, 0, 51), (17, 4, 30, 85), (46, 5, 60, 85), (58, 2, 23, 51)]     # x, y, Phase, Periode

# ── Turm (Spalten 27 … 37): g Spitze, h Haube, t Mauer, c Zifferblatt, w Schallfenster ──
TURM_X = 27
TURM = [".....g.....",
        "...hhhhh...",
        ".hhccccchh.",
        "hhccccccchh",
        "tccccccccct",
        "tccccccccct",
        "tccccccccct",
        "tccccccccct",
        "tccccccccct",
        "ttccccccctt",
        "tttcccccttt",
        "ttttttttttt",
        "ttwwwwwwwtt",
        "ttwwwwwwwtt",
        "ttwwwwwwwtt",
        "ttwwwwwwwtt"]
TURMFARBEN = {"g": GOLD, "h": (0, 100, 80), "t": (70, 64, 104), "c": (255, 225, 140), "w": (14, 6, 0)}
MX, MY = 32, 6                                  # Mitte des Zifferblatts
ZEIGER = (0, 0, 0)
BRONZE = (255, 140, 0)
FENSTER_GLUT = (70, 22, 0)                      # Schallfenster, solange die Glocke läutet

# Zeigerformen für das erste Viertel (0, 15, … 75 Grad ab zwölf), von der Mitte aus; die anderen
# Viertel entstehen durch Drehen. Von Hand gesetzt, damit jeder Zeiger gerade aussieht.
VIERTEL = [[(0, -1), (0, -2), (0, -3)], [(0, -1), (0, -2), (1, -3)], [(1, -1), (1, -2), (2, -3)],
           [(1, -1), (2, -2), (3, -3)], [(1, -1), (2, -1), (3, -2)], [(1, 0), (2, 0), (3, -1)]]
KLEIN = [(0, -1), (0, -2)]                      # kleiner Zeiger: kurz vor zwölf steht er schon oben

# Glocke im Schallfenster (7 breit, 4 hoch): Mitte, nach links, nach rechts; b Glocke, k Klöppel
GLOCKE = {0: ["...b...", "..bbb..", ".bbbbb.", "...k..."],
          -1: ["...b...", ".bbb...", "bbbbb..", "....k.."],
          1: ["...b...", "...bbb.", "..bbbbb", "..k...."]}

# ── Dorf: Häuser aus Vorlagen, unterste Zeile = Zeile 15 ──
# s Schnee, d Dach, # Wand, k Kamin, o und p die beiden Fenster (2×2)
GIEBEL = ["...s...",
          "..sds..",
          ".sddds.",
          "sddddds",
          "#oo#pp#",
          "#oo#pp#",
          "#######"]
LANG = [".....kk...",
        ".ssssssss.",
        "sdddddddds",
        "dddddddddd",
        "##oo##pp##",
        "##oo##pp##",
        "##########"]
# x, Vorlage, linkes und rechtes Fenster: (Bild, in dem es angeht, Bild, in dem es ausgeht)
DORF = [(0, GIEBEL, (150, 236), (132, 220)), (8, LANG, (140, 226), (166, 244)),
        (20, GIEBEL, (158, 216), (128, 232)), (38, LANG, (136, 240), (154, 222)),
        (49, GIEBEL, (162, 228), (144, 246)), (57, GIEBEL, (148, 218), (170, 234))]
DORFFARBEN = {"s": SCHNEE, "d": DACH, "#": WAND, "k": KAMIN}
BODEN_Y = 15                                   # zwischen den Häusern: verschneiter Boden

# ── Ablauf ──
ZWOELF = 48                                    # ab hier stehen beide Zeiger oben
SCHLAG = 6                                     # Bilder je Glockenschlag (zwölf Schläge)
RUECK = 224                                    # ab hier läuft der große Zeiger im Zeitraffer herum
VOR = 20                                       # Stellung "zehn vor zwölf" (in 15-Grad-Schritten)

# Raketen: Start, x, Höhe des Platzers, Farbe, Farbe der Mitte, Drehung, Radius
STEIG, BLUETE = 8, 22
RAKETEN = [(116, 12, 4, ROT, GELB, 0.0, 4.6), (126, 50, 3, HELLBLAU, WEISS, 0.4, 4.2),
           (136, 23, 4, GOLD, ROT, 0.2, 5.0), (146, 42, 4, PINK, WEISS, 0.0, 4.6),
           (156, 7, 3, TUERKIS, GELB, 0.4, 4.2), (166, 56, 4, GOLD, PINK, 0.2, 5.0),
           (176, 17, 4, LILA, WEISS, 0.0, 4.6), (186, 46, 3, ROT, GELB, 0.4, 4.2),
           (196, 10, 4, HELLBLAU, WEISS, 0.2, 5.0), (204, 52, 4, GOLD, ROT, 0.0, 4.6),
           (206, 20, 3, PINK, GELB, 0.4, 4.2)]


def _runden(v):
    """Kaufmännisch runden, von null weg (damit links und rechts gleich aussehen)."""
    return int(math.copysign(math.floor(abs(v) + 0.5), v))


def zeiger(bild, stellung):
    """Großer Zeiger in der Stellung 0 … 23 (je 15 Grad ab zwölf, im Uhrzeigersinn)."""
    viertel, rest = divmod(stellung % 24, 6)
    for x, y in VIERTEL[rest]:
        for _ in range(viertel):                                   # Vierteldrehung im Uhrzeigersinn
            x, y = -y, x
        bild.setze(MX + x, MY + y, ZEIGER)


def stellung(f):
    """Großer Zeiger: rückt in vier Schritten auf zwölf, steht, läuft am Schluss im Zeitraffer herum."""
    if f < ZWOELF:
        return VOR + f * (24 - VOR) // ZWOELF
    if f < RUECK:
        return 0
    s = (f - RUECK) / (255 - RUECK)
    return round(VOR * s * s * (3 - 2 * s))


def glocke_lage(f):
    """-1 links, 0 Mitte, 1 rechts; an jedem Umkehrpunkt ein Schlag."""
    t = f - ZWOELF
    if t < 0 or t >= 12 * SCHLAG:
        return 0
    p = t % (2 * SCHLAG)
    if p < 4:
        return -1
    if p < SCHLAG:
        return 0
    if p < SCHLAG + 4:
        return 1
    return 0


def schallbogen(bild, f):
    """Zu jedem Schlag ein Bogen nach links und rechts, der wächst und verblasst."""
    for k in range(12):
        t = f - (ZWOELF + k * SCHLAG)
        if 0 <= t < 12:
            farbe = dimmen(GELB, (1.0, 0.75, 0.5, 0.25)[t // 3])
            halb = 1 + t // 6                                      # halbe Höhe des Bogens
            for seite in (-1, 1):
                x = (TURM_X - 1 if seite < 0 else TURM_X + 11) + seite * (1 + t)
                bild.rechteck(x, MY - halb, 1, 2 * halb + 1, farbe)
                bild.setze(x - seite, MY - halb - 1, farbe)
                bild.setze(x - seite, MY + halb + 1, farbe)


def feuerwerk(bild, f):
    """Raketen und Blüten; liefert Stärke (0 … 1) und Farbe des frischesten Platzers für den Widerschein."""
    schein = (0.0, WEISS)
    for start, x, zy, farbe, mitte, dreh, radius in RAKETEN:
        t = f - start
        if t < 0 or t >= STEIG + BLUETE:
            continue
        if t < STEIG:                                              # Rakete steigt hinter den Dächern auf
            s = t / STEIG
            y = round(13 - (13 - zy) * (1 - (1 - s) ** 2))
            bild.setze(x, y, (255, 235, 170))
            bild.setze(x, y + 1, dimmen(GOLD, 0.6))
            bild.setze(x, y + 2, dimmen(GOLD, 0.3))
            continue
        k = t - STEIG                                              # Blüte: acht Funken außen, vier innen

        def ort(i, kk, anteil=1.0):
            r = radius * anteil * (1 - math.exp(-(max(kk, 0) + 0.5) / 3.0))
            w = dreh + i * math.pi / 4
            return x + _runden(r * math.cos(w)), zy + _runden(r * math.sin(w) * 0.85 + 0.008 * kk * kk)

        if k < 8 and 1 - k / 8 > schein[0]:
            schein = (1 - k / 8, farbe)
        h = round((1.0 if k <= 8 else 1 - (k - 8) / (BLUETE - 8)) * 8) / 8     # verglimmt in Stufen
        if h < 0.25:                                               # darunter sind die LEDs praktisch aus
            continue
        for i in range(8):
            if 1 <= k <= 5:                                        # kurzer Schweif, solange die Blüte aufgeht
                bild.setze(*ort(i, k - 1.5), dimmen(farbe, 0.5))
        for i in range(8):
            funkeln = k >= 12 and (i + k // 2) % 2                 # funkelnd verlöschen
            bild.setze(*ort(i, k), dimmen(farbe, max(0.25, h - 0.25) if funkeln else h))
        if 2 <= k < 14:
            for i in range(1, 8, 2):
                bild.setze(*ort(i, k, 0.45), dimmen(mitte, max(0.25, h - 0.25)))
        if k < 2:
            bild.setze(x, zy, WEISS)                               # Blitz in der Mitte
    return schein


def dorf(bild, f, schein=(0.0, WEISS)):
    """Boden und Häuser; der Schnee nimmt kurz die Farbe des frischen Platzers an."""
    staerke = round(schein[0] * 4) / 4
    farben = dict(DORFFARBEN, s=mischen(SCHNEE, schein[1], staerke * 0.45))
    bild.rechteck(0, BODEN_Y, 64, 1, farben["s"])                    # Schnee zwischen den Häusern
    for x0, vorlage, links, rechts in DORF:
        fenster = {"o": links, "p": rechts}
        for dy, zeile in enumerate(vorlage):
            for dx, c in enumerate(zeile):
                if c in farben:
                    farbe = farben[c]
                elif c in fenster:                                   # Fenster gehen der Reihe nach an und aus
                    an, aus = fenster[c]
                    farbe = LICHT if an <= f < aus else WAND
                else:
                    continue
                bild.setze(x0 + dx, 16 - len(vorlage) + dy, farbe)


def turm(bild, f):
    laeutet = ZWOELF <= f < ZWOELF + 12 * SCHLAG                   # dann glimmt das Schallfenster
    bild.figur(TURM_X, 0, TURM, dict(TURMFARBEN, w=FENSTER_GLUT) if laeutet else TURMFARBEN)
    for x, y in KLEIN + [(0, 0)]:
        bild.setze(MX + x, MY + y, ZEIGER)
    zeiger(bild, stellung(f))
    bild.figur(TURM_X + 2, 12, GLOCKE[glocke_lage(f)], {"b": BRONZE, "k": GELB})


def sterne(bild, f):
    """Wenige Sterne, funkeln langsam (die Perioden teilen 255, damit die Runde aufgeht)."""
    for x, y, phase, periode in STERNE:
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        sterne(bild, f)
        schein = feuerwerk(bild, f)
        schallbogen(bild, f)
        dorf(bild, f, schein)
        turm(bild, f)
        liste.append(bild)
    return liste
