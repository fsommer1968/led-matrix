"""Schwarzwälder Kuckucksuhr: ein Häuschen mit verschneitem Dach an der Stubenwand, darunter schwingt
das Pendel zwischen zwei Tannenzapfen-Gewichten. Der große Zeiger rückt vor; steht er oben (drei Uhr),
springt das Türchen im Giebel auf, der Kuckuck fährt am Messingarm heraus und ruft dreimal (Schnabel
auf, Flügel hoch, zwei Noten je Ruf), dann fährt er wieder hinein und das Türchen geht zu. Links und
rechts ein Fenster: Tanne im Schnee, Flocken fallen, rechts steht der Mond. Die Runde geht ohne
Sprung in sich über (17 Pendelschwingungen, ein Zeigerumlauf, Flocken in ganzen Durchläufen) –
255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum eine einfarbige Wand, zwei gleiche Fenster mit denselben
Flocken (das zweite ist bis auf den Mond eine Kopie des ersten), ein Dach in Stufen von je zwei
gleichen Spalten, Holz in einer Farbe und Flocken, die in ihrer Spalte bleiben.
"""
import math

from basis import GELB, GOLD, ORANGE, SCHWARZ, Bild, dimmen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "kuckucksuhr"
TITEL = "Schwarzwälder Kuckucksuhr"

WAND = (0, 0, 0)                               # Stubenwand schwarz: Braun auf Stufe 3 verschmolz mit dem Gehäuse (25.11.2026)
HOLZ = (33, 15, 3)                             # Häuschen (große Fläche, gedämpft)
DACH = (215, 225, 250)                         # Schnee auf dem Dach
TUER = (66, 35, 9)
BLATT = (215, 195, 135)                        # Zifferblatt
ZEIGER_STUNDE = (200, 0, 0)
STANGE = (74, 57, 17)                        # Messing: Pendelstange und Arm des Kuckucks
ZAPFEN = (58, 30, 8)
ZAPFEN_DUNKEL = (33, 16, 4)
KETTE = (130, 130, 140)
RAHMEN = (49, 26, 9)
HIMMEL = (0, 0, 60)
BODEN = (150, 160, 200)
FLOCKE = (170, 180, 215)
MOND = (240, 225, 150)
TANNE = (0, 110, 40)
VOGEL = (0, 190, 255)
FLUEGEL = (0, 80, 200)

CX = 32                                        # Mitte der Uhr
FENSTER = (2, 50)                              # linke Kante der beiden Fenster (12 breit)
# Flocken im Fenster: Spalte im Fenster, Durchläufe je Runde, Anfangshöhe
FLOCKEN = [(1, 11, 6.3), (3, 9, 1.7), (5, 12, 3.5), (8, 10, 2.1), (10, 8, 5.8)]

RUNDE = 255
PENDEL = 15                                    # Bilder je Schwingung, 17 Schwingungen je Runde
RUF_AB = 96                                    # hier springt der Zeiger auf zwölf
OBEN = 70                                      # so lange bleibt er dort (Auftritt des Kuckucks)
RUF = 14                                       # Bilder je Ruf
RUFE = (14, 28, 42)                            # Beginn der drei Rufe nach RUF_AB
WEG = 7                                        # so weit fährt der Kuckuck heraus

# Spitzen des großen Zeigers, 16 Stellungen im Uhrzeigersinn ab zwölf
SPITZEN = [(0, -3), (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3),
           (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3)]

# Kuckuck (Blick nach rechts): k Körper, f Flügel, a Auge, s Schnabel
KUCKUCK_ZU = [".....", ".kkk.", "ffkas", "fffk."]
KUCKUCK_AUF = [".f...", "ffkks", ".kka.", ".kkks"]                  # ruft: Schnabel auf, Flügel hoch
NOTE = [".nn", ".n.", "nn."]


def fenster(bild, x0, f, mond=False):
    """Fenster 12×11 mit Sims: Rahmen, Nachthimmel, Schnee, eine Tanne und ein paar Flocken."""
    bild.rechteck(x0, 2, 12, 11, RAHMEN)
    bild.rechteck(x0 - 1, 12, 14, 1, RAHMEN)
    bild.rechteck(x0 + 1, 3, 10, 7, HIMMEL)
    bild.rechteck(x0 + 1, 10, 10, 2, BODEN)
    for k in range(5):                                               # Tanne: zwei Stufen
        halb = (k + 1) // 2
        bild.rechteck(x0 + 6 - halb, 5 + k, 2 * halb + 1, 1, TANNE)
    bild.setze(x0 + 6, 4, BODEN)                                     # Schneehaube
    if mond:
        bild.rechteck(x0 + 8, 3, 2, 2, MOND)
    for dx, runden, hoehe in FLOCKEN:                                # fallen nur vor dem Himmel
        y = 3 + int(hoehe + f * runden * 7 / RUNDE) % 7
        if bild.hole(x0 + dx, y) == HIMMEL:
            bild.setze(x0 + dx, y, FLOCKE)


def uhr(bild, zeiger, tuer):
    """Häuschen mit Schneedach, Türchen (tuer = sichtbare Spalten, 0 = offen) und Zifferblatt."""
    bild.rechteck(CX - 1, 0, 3, 1, DACH)
    for y in range(1, 5):                                            # Giebel: je Zeile zwei Spalten breiter
        halb = 2 * y - 1
        bild.rechteck(CX - halb - 2, y, 2 * halb + 5, 1, DACH)
        bild.rechteck(CX - halb, y, 2 * halb + 1, 1, HOLZ)
    bild.rechteck(CX - 7, 5, 15, 7, HOLZ)
    bild.rechteck(CX - 1, 1, 3, 3, SCHWARZ)                          # Öffnung …
    bild.rechteck(CX - 1, 1, tuer, 3, TUER)                          # … und Türchen (Angel links)
    if tuer == 0:
        bild.rechteck(CX - 2, 2, 1, 2, TUER)                         # aufgeklappt neben der Öffnung
    bild.kreis(CX, 8, 3, BLATT)
    bild.linie(CX + 1, 8, CX + 2, 8, ZEIGER_STUNDE)                  # kleiner Zeiger steht auf drei
    dx, dy = SPITZEN[zeiger]
    bild.linie(CX, 8, CX + dx, 8 + dy, SCHWARZ)


def pendel(bild, f):
    """Pendel schwingt gleichmäßig um drei Spalten nach jeder Seite, außen eine Zeile höher."""
    dx = round(3 * math.sin(2 * math.pi * f / PENDEL))
    oben = 12 if abs(dx) == 3 else 13
    if oben == 13:
        bild.setze(CX + (1 if dx > 0 else -1 if dx < 0 else 0), 12, STANGE)
    bild.rechteck(CX + dx - 1, oben, 3, 3, GOLD)


def gewichte(bild):
    for x in (CX - 7, CX + 7):                                       # Tannenzapfen an kurzer Kette
        bild.setze(x, 12, KETTE)
        bild.rechteck(x - 1, 13, 3, 2, ZAPFEN)
        bild.setze(x, 15, ZAPFEN_DUNKEL)


def bilder():
    liste = []
    for f in range(RUNDE):
        bild = Bild(WAND)
        t = (f - RUF_AB) % RUNDE
        for x0 in FENSTER:
            fenster(bild, x0, f, mond=x0 > CX)
        zeiger = 0 if t < OBEN else 1 + (t - OBEN) * 15 // (RUNDE - OBEN)
        tuer = 3 if t < 3 or t >= 67 else max(0, 5 - t, t - 64)
        uhr(bild, zeiger, tuer)
        gewichte(bild)
        pendel(bild, f)
        # Kuckuck: fährt an der Stange heraus, ruft, fährt hinein
        if 6 <= t < 65:
            weg = min(WEG, t - 5, 64 - t)
            ruf = [t - r for r in RUFE if 0 <= t - r < RUF]
            auf = bool(ruf) and (ruf[0] < 4 or 5 <= ruf[0] < 9)
            x0 = CX - 3 + weg + auf                                  # beim Rufen nickt er nach vorn
            for x in range(CX + 2, x0):                              # Stange vom Türchen zum Vogel
                bild.setze(x, 2, STANGE)
            zeilen = KUCKUCK_AUF if auf else KUCKUCK_ZU
            farben = {"k": VOGEL, "f": FLUEGEL, "a": SCHWARZ, "s": ORANGE}
            for dy, zeile in enumerate(zeilen):
                for dx, c in enumerate(zeile):
                    if c != "." and x0 + dx >= CX - 1:               # hinter der Türkante verdeckt
                        bild.setze(x0 + dx, dy, farben[c])
            for r in RUFE:                                           # zwei Noten je Ruf, treiben nach rechts
                for k, (beginn, y) in enumerate(((0, 0), (5, 3))):
                    alter = t - r - beginn
                    if 0 <= alter < 9:
                        farbe = dimmen(GELB if k == 0 else ORANGE, 1.0 if alter < 6 else 0.5)
                        bild.figur(CX + 11 + k + alter // 3, y, NOTE, {"n": farbe})
        liste.append(bild)
    return liste
