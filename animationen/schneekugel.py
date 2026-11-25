"""Schneekugel: eine große Glaskugel auf goldenem Sockel, darin ein Haus mit warm leuchtenden
Fenstern und eine Tanne. Die Kugel wird geschüttelt, der Schnee stiebt vom Boden auf, wirbelt im
Kreis durch das Glas und sinkt dann langsam wieder herab – auf das Dach oder vor der Tanne bis zum
Boden. Links und rechts stehen zwei kleine Kugeln mit je einer Tanne still daneben, oben in den
Ecken glimmen vier bunte Lichter. Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ein flacher Schneeboden und ein gerader Sockel (gleiche
Nachbarspalten), die rechte kleine Kugel ist eine Kopie der linken, die große Kugel wird beim
Schütteln als Ganzes verschoben (nicht verzerrt), nur 18 Flocken und nur vier Lichtpunkte (jeder
einzelne Punkt im dunklen Grund kostet rund 8 Bytes je Bild).
"""
import math
import random

from basis import NACHTBLAU, WEISS, Bild, dimmen, mischen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "schneekugel"
TITEL = "Schneekugel wird geschüttelt"

GLAS = (70, 125, 215)                          # Rand der Kugel
GLANZ = (235, 245, 255)                        # Lichtreflex oben links
HIMMEL = (0, 22, 78)                           # in der Kugel: etwas heller als der Grund
BODEN = (215, 225, 250)                        # Schnee am Boden und auf dem Dach
TANNE = (0, 165, 50)
STAMM = (41, 21, 7)
WAND = (215, 35, 20)
DACH = (120, 15, 15)
FENSTER, GLUT = (255, 205, 40), (255, 160, 15)  # warmes Licht, atmet langsam zwischen Gelb und Orange
RING = (255, 185, 30)                          # Sockel: heller Ring, Körper, Fuß
SOCKEL = (190, 105, 0)
FUSS = (120, 62, 0)

# große Kugel, 18 Spalten breit: g Glas, z Glanz, h Himmel, s Schnee, t Tanne, b Stamm,
# w Wand, d Dach, f Fenster, r Ring, k Sockel, u Fuß
GROSS = ["......gggggg......",
         "....zzhhhhhhgg....",
         "...zhhhhhhhhhhg...",
         "..zhhhhhhhhhhhhg..",
         "..ghhshhhhhhhhhg..",
         ".ghhhthhhhssshhhg.",
         ".ghhttthhssssshhg.",
         ".ghhttthdddddddhg.",
         ".ghtttttwffwffwhg.",
         ".ghtttttwffwffwhg.",
         ".ghhhbhhwwwwwwwhg.",
         "..gssssssssssssg..",
         "..gssssssssssssg..",
         ".rrrrrrrrrrrrrrrr.",
         ".kkkkkkkkkkkkkkkk.",
         "uuuuuuuuuuuuuuuuuu"]
# kleine Kugel, 10 Spalten breit, steht in den Zeilen 6 bis 15
KLEIN = ["...gggg...",
         "..zhhhhg..",
         ".ghhtthhg.",
         ".ghhtthhg.",
         ".ghtttthg.",
         ".gssssssg.",
         "..gssssg..",
         ".rrrrrrrr.",
         ".kkkkkkkk.",
         "uuuuuuuuuu"]
X_GROSS, X_KLEIN = 23, (4, 50)
FREI = "htb"                                   # hier sieht man Flocken: vor Himmel und Tanne, nicht vor dem Haus
# Lichter oben in den Ecken: x, y, Farbe, Phase (jedes glimmt im Takt von 85 Bildern einmal dunkler)
LICHTER = [(2, 2, (255, 40, 0), 5), (17, 1, (255, 190, 30), 33),
           (46, 1, (0, 210, 70), 62), (61, 2, (0, 120, 255), 76)]

RUHE, SCHUETTELN, TAKT, HUB = 8, 48, 8, 3      # Bilder still; Schütteln: Dauer, Takt in Bildern, Ausschlag in Spalten
ENDE = RUHE + SCHUETTELN
FLOCKEN, SAAT = 18, 245
MITTE_X, MITTE_Y, WEIT_X, WEIT_Y = 8.5, 4.2, 5.7, 3.1   # Wirbel über Haus und Tanne (Spalte/Zeile der Kugel)
DREHEN = 0.13                                  # Wirbel: Bogenmaß je Bild, klingt nach dem Schütteln ab
GRUND = 10.4                                   # von hier steigt der Schnee auf
SINKEN, FALL = 100, (0.07, 0.11)               # Beginn des Sinkens über so viele Bilder gestreut; Zeilen je Bild
LIEGT_AB = 242                                 # spätestens hier liegt alles (mit SAAT 245 schon ab Bild 233)


def schwung(f):
    """Auslenkung der großen Kugel, -1 … 1: schnell an, hält, klingt aus."""
    t = f - RUHE
    if not 0 <= t < SCHUETTELN:
        return 0.0
    huelle = min(1.0, (t + 1) / 4, (SCHUETTELN - t) / 14)
    return huelle * math.sin(2 * math.pi * t / TAKT)


def weich(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def flockenbahnen():
    """Je Bild die Orte der Flocken in der großen Kugel (None: liegt am Boden).

    Jede Flocke hat ihre eigene Kreisbahn (so ballen sie sich nicht am Glas): Sie steigt vom Boden
    in die Bahn, dreht mit dem Wasser, und wenn es zur Ruhe kommt, sinkt sie – jede zu ihrer Zeit –
    leicht pendelnd, bis sie auf Dach oder Boden liegen bleibt."""
    z = random.Random(SAAT)
    innen = [[i for i, c in enumerate(zeile) if c not in ".gzrku"] for zeile in GROSS]
    flocken = []
    for i in range(FLOCKEN):
        flocken.append({"start": RUHE + 1 + z.randrange(16), "x0": 3.0 + 12 * (i + z.random()) / FLOCKEN,
                        "bahn": math.sqrt((i + 0.6) / FLOCKEN), "winkel": z.uniform(0, 2 * math.pi),
                        "dreh": z.uniform(0.8, 1.2), "sinkt": ENDE + 6 + z.randrange(SINKEN),
                        "fall": z.uniform(*FALL), "phase": z.uniform(0, 2 * math.pi),
                        "tief": 0.0, "liegt": False})
    bahnen, gedreht = [], 0.0
    for f in range(255):
        if f >= RUHE + 2:
            gedreht += DREHEN * min(1.0, (f - RUHE - 2) / 8) * math.exp(-max(0, f - ENDE) / 40)
        stoss = schwung(f - 2)                                       # das Wasser schwappt der Kugel nach
        orte = []
        for fl in flocken:
            if f < fl["start"] or fl["liegt"]:
                orte.append(None)
                continue
            ruhig = weich((f - fl["sinkt"]) / 30)                    # 0 im Wirbel, 1 im Sinken
            fl["tief"] += fl["fall"] * ruhig
            w = fl["winkel"] + fl["dreh"] * gedreht
            bahn = fl["bahn"] * (1 + 0.12 * math.sin(f / 7 + fl["phase"]))
            x = MITTE_X + WEIT_X * bahn * math.cos(w) - 1.6 * stoss + 0.7 * ruhig * math.sin(f / 13 + fl["phase"])
            y = MITTE_Y - WEIT_Y * bahn * math.sin(w) + fl["tief"]
            hoch = weich((f - fl["start"]) / 12)                     # vom Boden in die Bahn
            x = fl["x0"] + (x - fl["x0"]) * hoch
            y = GRUND + (y - GRUND) * hoch
            zeile = min(12, max(1, int(round(y))))
            x = min(innen[zeile][-1], max(innen[zeile][0], x))       # bleibt im Glas
            if (ruhig > 0.3 and GROSS[zeile][int(round(x))] not in FREI) or f >= LIEGT_AB:
                fl["liegt"] = True                                   # gelandet: gehört wieder zur Schneedecke
                orte.append(None)
            else:
                orte.append((x, y))
        bahnen.append(orte)
    return bahnen


def kugel(bild, x0, y0, zeilen, farben, flocken=()):
    """Zeichnet eine Kugel aus ihrem Muster, die Flocken darin nur vor Himmel und Tanne."""
    bild.figur(x0, y0, zeilen, farben)
    for ort in flocken:
        if ort:
            fx, fy = int(round(ort[0])), int(round(ort[1]))
            if 0 <= fy < len(zeilen) and zeilen[fy][fx] in FREI:
                bild.setze(x0 + fx, y0 + fy, WEISS)


def bilder():
    bahnen = flockenbahnen()
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        atem = (f + 12) % 51                                         # 51 und 85 teilen 255: die Runde schließt
        licht = mischen(FENSTER, GLUT, 1.0 if 36 <= atem < 46 else 0.5 if 33 <= atem < 49 else 0.0)
        farben = {"g": GLAS, "z": GLANZ, "h": HIMMEL, "s": BODEN, "t": TANNE, "b": STAMM, "w": WAND,
                  "d": DACH, "f": licht, "r": RING, "k": SOCKEL, "u": FUSS}
        for x, y, farbe, phase in LICHTER:
            t = (f + phase) % 85
            bild.setze(x, y, dimmen(farbe, 0.4 if 3 <= t < 17 else 0.7 if t < 20 else 1.0))
        for x in X_KLEIN:                                            # zwei kleine Kugeln, stehen still
            kugel(bild, x, 6, KLEIN, farben)
        kugel(bild, X_GROSS + round(HUB * schwung(f)), 0, GROSS, farben, bahnen[f])
        liste.append(bild)
    return liste
