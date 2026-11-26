"""Christkind: Nachts schwebt das Christkind – goldene Locken, weißes Kleid, kleine goldene Flügel –
von links nach rechts über das verschneite Dorf. Über jedem Haus läutet es sein Glöckchen
(Klangstriche), und darunter gehen die Fenster warm an; ein goldener Glitzerschweif folgt ihm.
Ist es fort, gehen die Lichter Haus für Haus wieder aus – 255 Bilder, die Runde schließt nahtlos.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum nur drei Haustypen, deren Gruppe sich alle 27 Spalten
wiederholt (die zweite und dritte Gruppe sind Kopien der ersten und kosten fast nichts, ein
weiteres eigenes Gebäude kostete rund 10 KB), ein gerader Schneeboden, fünf Sterne, kein
Schneefall, im Schweif ein Glitzerpunkt alle zwei Bilder. Die Dächer sind gedämpft, damit das
weiße Kleid das Hellste im Bild bleibt.
"""
import math
import random

from basis import B, HAUT, NACHTBLAU, WEISS, Bild

NAME = "christkind"
TITEL = "Das Christkind kommt"

KANTE = (170, 180, 215)                        # Schnee: Oberkante der Dächer
DACH = (75, 85, 130)                           # Schnee auf dem Dach darunter (gedämpft)
BODEN = (90, 100, 145)                         # Schnee am Boden
DUNKEL = (0, 0, 60)                            # Fenster ohne Licht
GLIMMT = (150, 80, 0)                          # Fenster geht in zwei Stufen an: erst glimmt es
HAAR = (255, 200, 0)
FLUEGEL = (255, 150, 0)
GLOCKE = (255, 225, 40)
KLOEPPEL = (200, 90, 0)
KLANG = (255, 245, 170)
AUGE = (50, 25, 10)
GLITZER = [(255, 245, 170), (255, 200, 40), (170, 110, 0), (80, 50, 0)]     # Schweif: Funke, dann drei Stufen
STERN = (255, 240, 200)
# x, y, Periode, Phase – die Perioden teilen 255, jeder Stern leuchtet die halbe Zeit
STERNE = [(6, 1, 51, 0.0), (23, 3, 85, 0.3), (41, 0, 51, 0.6), (58, 2, 85, 0.8), (33, 5, 85, 0.55)]

# Dorf: drei Haustypen. dach = oberste Dachzeile je Spalte (Schnee), Mauer Zeilen 12–14,
# fenster = linke Spalte je Fenster (2×2 ab Zeile 12), licht = Farbe, wenn es an ist.
MAUER_OBEN, BODEN_Y = 12, 15
TYPEN = {
    "a": {"dach": [11, 10, 9, 9, 9, 10, 11], "mauer": (110, 35, 30), "fenster": [1, 4], "licht": (255, 175, 40)},
    "b": {"dach": [11, 10, 10, 10, 10, 10, 10, 11], "mauer": (56, 64, 110), "fenster": [1, 5],
          "licht": (255, 205, 80)},
    "c": {"dach": [11, 10, 10, 10, 11], "mauer": (45, 88, 72), "fenster": [2], "licht": (255, 150, 20)},
}
# x, Typ: die Gruppe a, b, c wiederholt sich nach 27 Spalten
HAEUSER = [(1, "a"), (10, "b"), (20, "c"), (28, "a"), (37, "b"), (47, "c"), (55, "a")]

# Christkind, Blick nach rechts, 14 breit: g Haar, h Haut, a Auge, w Kleid; der Saum weht in zwei Lagen
KIND = ["....gggg......",
        "...ggghha.....",
        "....gghhh.....",
        "...gggwww.....",
        "....wwwwwwwh..",
        ".....www......",
        "....wwww......"]
SAUM = [["...wwwwww.....", ".wwwwwwww....."],
        ["..wwwwwww.....", "...wwwwww....."]]
# Flügel am Rücken, schlagen ruhig in vier Lagen (auf, Mitte, ab, Mitte): (ab Zeile, Muster)
FLUEGEL_LAGEN = [(1, ["y..", "yy.", "yyy", ".yy"]), (3, ["yy.", "yyy", "yy."]),
                 (4, [".yy", "yyy", "yy.", "y.."]), (3, ["yy.", "yyy", "yy."])]
GLOCKE_X, GLOCKE_Y = 11, 5                     # Aufhängung unter der Hand
KIND_FARBEN = {"g": HAAR, "h": HAUT, "a": AUGE, "w": WEISS, "y": FLUEGEL}
# Klangstriche rechts der Glocke: drei kurze Striche, blinken im Takt des Läutens (je drei Bilder)
KLAENGE = [(4, -1), (5, -2), (4, 1), (5, 1), (4, 3), (5, 4)]

START, TEMPO = 8, 0.42                         # ab hier schwebt es herein, Spalten je Bild
X_START = -15
VOR, NACH = 3, 8                               # läutet von so vielen Bildern vor bis nach der Hausmitte
GLIMMEN, HELL = 3, 6                           # so viele Bilder nach der Hausmitte glimmt das Fenster, dann ist es hell
AUS_AB, AUS_ABSTAND = 216, 5                   # ist das Christkind fort, gehen die Lichter Haus für Haus aus
AUS_FOLGE = [3, 0, 5, 2, 6, 1, 4]              # … in loser Folge (man geht schlafen)


def kind_x(f):
    return round(X_START + (f - START) * TEMPO)


def _mitte(nr):
    x, typ = HAEUSER[nr]
    return x + len(TYPEN[typ]["dach"]) // 2


def _an(nr):
    """Bild, in dem die Glocke über der Hausmitte ist."""
    return next(f for f in range(255) if kind_x(f) + GLOCKE_X >= _mitte(nr))


AN = [_an(nr) for nr in range(len(HAEUSER))]


def licht(nr, f):
    """Farbe der Fenster des Hauses in Bild f."""
    aus = AUS_AB + AUS_FOLGE.index(nr) * AUS_ABSTAND
    if f < AN[nr] + GLIMMEN or f >= aus + 3:
        return DUNKEL
    if f < AN[nr] + HELL or f >= aus:
        return GLIMMT
    return TYPEN[HAEUSER[nr][1]]["licht"]


def dorf(bild, f):
    bild.rechteck(0, BODEN_Y, B, 1, BODEN)
    for nr, (x0, typ) in enumerate(HAEUSER):
        t = TYPEN[typ]
        for dx, oben in enumerate(t["dach"]):
            bild.setze(x0 + dx, oben, KANTE)
            bild.rechteck(x0 + dx, oben + 1, 1, MAUER_OBEN - oben - 1, DACH)
            bild.rechteck(x0 + dx, MAUER_OBEN, 1, BODEN_Y - MAUER_OBEN, t["mauer"])
        farbe = licht(nr, f)
        for dx in t["fenster"]:
            bild.rechteck(x0 + dx, MAUER_OBEN, 2, 2, farbe)


def _schweif():
    """Glitzerpunkte: (Bild, x, y) – entstehen hinter dem Christkind und bleiben am Himmel stehen."""
    z = random.Random(24)
    punkte = []
    y_alt = 0
    for f in range(START, 255, SCHWEIF_TAKT):
        x = kind_x(f) - 1
        y = z.choice([r for r in range(2, 9) if abs(r - y_alt) > 1])
        y_alt = y
        if -1 < x < B:
            punkte.append((f, x, y))
    return punkte


SCHWEIF_TAKT, SCHWEIF_DAUER = 2, 18             # alle zwei Bilder ein Punkt, jeder glimmt 18 Bilder
SCHWEIF = _schweif()


def christkind(bild, f):
    x = kind_x(f)
    if x >= B:
        return
    y = 1 if math.sin((f - START) / 40 * 2 * math.pi) < 0 else 0     # schwebt sacht auf und ab
    ab, fluegel = FLUEGEL_LAGEN[(f // 4) % 4]
    bild.figur(x, y + ab, fluegel, KIND_FARBEN)
    bild.figur(x, y, KIND + SAUM[(f // 5) % 2], KIND_FARBEN)
    takt = next(((f - an + VOR) // 3 for an in AN if -VOR <= f - an <= NACH), None)   # None = läutet nicht
    schwung = 0 if takt is None else (-1 if takt % 2 else 1)
    gx, gy = x + GLOCKE_X, y + GLOCKE_Y
    bild.setze(gx, gy, GLOCKE)
    bild.rechteck(gx - 1 + schwung, gy + 1, 3, 1, GLOCKE)
    bild.setze(gx - schwung, gy + 2, KLOEPPEL)
    if takt is not None and takt % 2 == 0:
        for dx, dy in KLAENGE:
            if bild.hole(gx + dx, gy + dy) == NACHTBLAU:             # nur am Himmel, nicht auf den Dächern
                bild.setze(gx + dx, gy + dy, KLANG)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, periode, phase in STERNE:                          # wenige Sterne, blinken reihum
            if (f / periode + phase) % 1 < 0.5:
                bild.setze(x, y, STERN)
        dorf(bild, f)
        for start, x, y in SCHWEIF:                                  # Glitzerschweif verglimmt
            alter = f - start
            if 0 <= alter < SCHWEIF_DAUER:
                bild.setze(x, y, GLITZER[0 if alter < 2 else 1 + alter * 3 // SCHWEIF_DAUER])
        christkind(bild, f)
        liste.append(bild)
    return liste
