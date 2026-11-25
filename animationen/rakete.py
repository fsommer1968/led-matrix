"""Raketen starten aus der Flasche: vier Sektflaschen stecken im Schnee, in jeder eine Rakete mit
Stab. Eine Hand hält ein brennendes Streichholz nacheinander an die Zündschnüre, Funken sprühen,
die Rakete zischt mit Funkenschweif hoch und platzt oben – als Stern, Kugel, Goldregen und
Doppelring, jede in ihrer Farbe; die Blüte sinkt langsam und verglimmt, der Schnee leuchtet kurz
mit, aus der leeren Flasche steigt ein Rauchwölkchen. Zum Schluss steckt die Hand von oben neue
Raketen in die Flaschen, und die Runde geht ohne Sprung von vorn los – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum vier gleiche Flaschen, wenige Funken je Blüte, vier
Helligkeitsstufen, vier Sterne, Hand und Ärmel aus gleichen Spalten.
"""
import math

from basis import (B, BLAU, GELB, GOLD, HAUT, HELLBLAU, HELLGRUEN, LILA, ORANGE, ROT, WEISS, Bild,
                   dimmen, mischen)
from feuerwerk import jedes_bild_anders

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "rakete"
TITEL = "Raketen starten aus der Flasche"

HIMMEL = (0, 0, 14)
SCHNEE = (110, 120, 165)                        # Schneelinie am Boden
GLAS = (0, 150, 50)                             # Flasche
GLANZ = (110, 240, 130)
ETIKETT = (200, 190, 150)
FOLIE = (255, 180, 0)
STAB = (66, 42, 17)
SCHNUR = (170, 170, 170)                        # Zündschnur
HOLZ = (74, 57, 34)                          # Streichholz
FLAMME = (255, 235, 150)
AERMEL = BLAU
RAUCH = (60, 60, 75)
STERN = (255, 240, 200)
STERNE = [(2, 4, 40), (18, 1, 0), (34, 3, 17), (50, 0, 34)]          # x, y, Phase (Periode 51)
STUFEN = (1.0, 0.7, 0.45, 0.25)                 # Helligkeiten der Funken (hält die Palette klein)
# Funken um das brennende Ende der Zündschnur, vier Bilder im Wechsel (dx, dy)
SPRUEHEN = [((-1, -1), (0, 1)), ((-2, 0), (0, -1)), ((-1, 1), (-1, -2)), ((0, -1), (-2, 1))]

# Flasche 5×7 (steckt mit der untersten Zeile im Schnee): g Folie, f Glas, h Glanz, e Etikett
FLASCHE = [".ggg.", ".ggg.", ".fff.", "fhfff", "feeef", "feeef", "fffff"]
FLASCHE_Y = 9
# Rakete 3×3: k Spitze, r Rumpf; darunter der Stab – ein Pixel sichtbar, der Rest in der Flasche
RAKETE = [".k.", "rrr", "rrr"]
RAKETE_Y = 5                                    # Spitze der Rakete, wenn sie in der Flasche steckt
STAB_LANG = 6

FLASCHEN_X = [10, 26, 42, 58]                   # Mitte der Flaschen
# je Rakete: Rumpf, Spitze, Blüte, Farbe der Blüte, zweite Farbe
RAKETEN = [(ROT, GELB, "stern", ROT, GELB), (HELLBLAU, WEISS, "kugel", HELLBLAU, (160, 230, 255)),
           (GELB, ROT, "gold", GOLD, GELB), (LILA, HELLGRUEN, "doppel", LILA, HELLGRUEN)]

# Ablauf je Rakete (Bilder ab ihrem Beginn)
ERSTE, ABSTAND = 2, 36                          # Beginn der ersten, Abstand der Raketen
DA, BRENNT, SCHUB, AB = 9, 11, 21, 23           # Streichholz da, Schnur brennt, Schub, hebt ab
STEIGT = 5                                      # so viele Bilder (und Pixel) steigt sie
PLATZT = AB + STEIGT                            # Bild des Platzens
DAUER = {"stern": 30, "kugel": 30, "gold": 38, "doppel": 30}         # so lange leuchtet die Blüte
PLATZ_Y = 3                                     # Mitte der Blüte
RAUCH_DAUER = 12
NEU_AB, NEU_ABSTAND, NEU_HOCH = 164, 19, 14     # neue Raketen: Beginn, Abstand, Weg von oben


def flasche(bild, x):
    bild.figur(x - 2, FLASCHE_Y, FLASCHE, {"g": FOLIE, "f": GLAS, "h": GLANZ, "e": ETIKETT})


def rakete(bild, x, hoch, rumpf, spitze, schnur=2):
    """Rakete, um `hoch` Pixel über ihrem Platz in der Flasche; der Stab ist nur über der
    Flasche zu sehen. Links hängt die Zündschnur (so viele Pixel sind noch da)."""
    unten = RAKETE_Y + len(RAKETE) - hoch                            # erste Zeile unter dem Rumpf
    for y in range(unten, min(FLASCHE_Y, unten + STAB_LANG)):
        bild.setze(x, y, STAB)
    bild.figur(x - 1, RAKETE_Y - hoch, RAKETE, {"k": spitze, "r": rumpf})
    for k in range(schnur):
        bild.setze(x - 2 - k, unten + k, SCHNUR)


def hand(bild, x, y, von_oben=False):
    """Hand 3×2 (x, y = links oben), der Ärmel reicht bis zum unteren oder oberen Bildrand."""
    bild.rechteck(x, y, 3, 2, HAUT)
    if von_oben:
        bild.rechteck(x, 0, 3, max(0, y), AERMEL)
    else:
        bild.rechteck(x, y + 2, 3, 16 - y - 2, AERMEL)


def streichholz(bild, x, y, f):
    """Hand mit schräg gehaltenem Streichholz; (x, y) ist die Flamme."""
    hand(bild, x - 5, y + 2)
    bild.setze(x - 2, y + 2, HOLZ)
    bild.setze(x - 1, y + 1, HOLZ)
    bild.setze(x, y, FLAMME)
    bild.setze(x, y - 1, ORANGE if (f // 2) % 2 else GOLD)


def _funke(bild, x, y, farbe, h):
    """Funke in der Helligkeit h, gerundet auf eine der vier Stufen; sehr schwache fallen weg."""
    if h >= 0.2:
        bild.setze(x, y, dimmen(farbe, min(STUFEN, key=lambda s: abs(s - h))))


def bluete(bild, x, art, farbe, farbe2, k):
    """Blüte k Bilder nach dem Platzen: breitet sich aus, sinkt und verglimmt."""
    cy, dauer = PLATZ_Y, DAUER[art]
    if k < 2:                                                        # Blitz
        for d in range(k + 2):
            for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
                bild.setze(x + dx, cy + dy, WEISS)
        return
    schwer = 0.018 if art == "gold" else 0.009

    def ort(winkel, anteil=1.0, kk=k):
        r = 5.4 * anteil * (1 - math.exp(-(kk + 0.5) / 3.0))
        return x + r * math.cos(winkel), cy + r * math.sin(winkel) * 0.75 + schwer * kk * kk

    def hell(i):
        """Erst voll, im letzten Teil in drei Stufen verglimmend; jeder Funke etwas versetzt."""
        rest = (dauer - k - i % 3) / (dauer * 0.6)
        return 1.0 if rest >= 1 else 0.7 if rest > 0.66 else 0.45 if rest > 0.33 else 0.25 if rest > 0 else 0

    if art == "stern":                                               # acht Strahlen, die zu Punkten werden
        for i in range(8):
            w = i * math.pi / 4
            if k < 8:
                _funke(bild, *ort(w, 0.4), farbe2, 1.0)
            if k < 16:
                _funke(bild, *ort(w, 0.7), farbe, 1.0 if k < 10 else 0.45)
            _funke(bild, *ort(w), mischen(farbe, WEISS, 0.4) if k < 5 else farbe, hell(i))
    elif art == "kugel":                                             # Ring und heller Kern
        for i in range(12):
            w = i * math.pi / 6 + 0.26
            if k < 8:                                                # frisch: kurze Strahlen
                _funke(bild, *ort(w, 1.0, k - 1.5), farbe, 0.45)
            _funke(bild, *ort(w), farbe, hell(i))
        for i in range(5):
            _funke(bild, *ort(i * math.pi / 2.5, 0.45), farbe2, hell(i))
    elif art == "gold":                                              # Goldregen: Funken mit Schweif
        c = GELB if k < 8 else farbe if k < 22 else ORANGE
        for i in range(10):
            w = (i + 0.5) * math.pi / 5
            a = (1.0, 0.75, 1.0, 0.75, 1.0, 0.8, 1.0, 0.8, 1.0, 0.8)[i]
            for zurueck, anteil in ((4, 0.45), (2, 0.7), (0, 1.0)):
                if k - zurueck >= 1:
                    _funke(bild, *ort(w, a, k - zurueck), c, hell(i) * anteil)
    else:                                                            # Doppelring in zwei Farben
        for i in range(10):
            _funke(bild, *ort(i * math.pi / 5), farbe, hell(i))
        for i in range(6):
            _funke(bild, *ort(i * math.pi / 3 + 0.5, 0.5), farbe2, hell(i))


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        for x, y, phase in STERNE:                                   # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % 51 < 30 else 0.5))
        schnee = SCHNEE
        vorn = []                                                    # Raketen: x, Höhe, Farben, Zeit
        holz, haende = None, []                                      # Streichholz (x der Flamme), Hände von oben
        for i, (x, (rumpf, spitze, art, farbe, farbe2)) in enumerate(zip(FLASCHEN_X, RAKETEN)):
            t = f - ERSTE - i * ABSTAND                              # Zeit seit dem Beginn dieser Rakete
            k = t - PLATZT
            if 0 <= k < DAUER[art]:                                  # Blüte hinter den Flaschen
                bluete(bild, x, art, farbe, farbe2, k)
                if k < 9:                                            # der Schnee leuchtet mit
                    schnee = mischen(SCHNEE, farbe, (0.6, 0.4, 0.2)[k // 3])
            if 0 <= k < RAUCH_DAUER:                                 # Rauch aus der leeren Flasche
                bild.setze(x + (k // 3) % 2, FLASCHE_Y - 1 - k // 3, RAUCH)
            n = f - NEU_AB - i * NEU_ABSTAND                         # neue Rakete kommt von oben
            if t < AB:
                vorn.append((x, 0, rumpf, spitze, t))
            elif t < PLATZT:
                vorn.append((x, t - AB + 1, rumpf, spitze, t))
            elif n >= 0:
                hoch = max(0, NEU_HOCH - n)
                vorn.append((x, hoch, rumpf, spitze, -1))
                if n <= NEU_HOCH + 1:                                # Hand hält die Rakete am Rumpf
                    haende.append((x + 2 + (n > NEU_HOCH), RAKETE_Y + 1 - hoch))
                elif n < NEU_HOCH + 6:                               # lässt los und zieht sich zurück
                    haende.append((x + 3, RAKETE_Y + 1 - 2 * (n - NEU_HOCH - 1)))
            # Streichholz: kommt von links, hält die Flamme an die Schnur, weicht zurück
            if 0 <= t < ABSTAND:
                ziel = x - 4
                if t < DA:
                    von = ziel - 18 if i else -2
                    hx = von + (ziel - von) * (1 - (1 - t / DA) ** 2)
                else:
                    hx = ziel - min(2, max(0, t - BRENNT - 1))
                holz = round(hx)
            elif i == 3 and ABSTAND <= t < ABSTAND + 12:             # nach der letzten: rechts hinaus
                holz = x - 6 + (t - ABSTAND + 1) * 2
        bild.rechteck(0, 15, B, 1, schnee)
        for x in FLASCHEN_X:
            flasche(bild, x)
        for x, hoch, rumpf, spitze, t in vorn:
            unten = RAKETE_Y + len(RAKETE) - hoch                    # Zeile unter dem Rumpf
            schnur = 2 if t < BRENNT + 5 else 1 if t < SCHUB else 0
            rakete(bild, x, hoch, rumpf, spitze, schnur)
            if BRENNT <= t < SCHUB:                                  # Schnur brennt ab: Funke wandert zur Rakete
                fx, fy = x - 1 - schnur, unten - 1 + schnur
                bild.setze(fx, fy, WEISS if f % 2 else GELB)
                for dx, dy in SPRUEHEN[f % 4]:
                    bild.setze(fx + dx, fy + dy, ORANGE)
            elif SCHUB <= t < PLATZT:                                # Schub: Funken unter der Rakete
                s = 1 if f % 2 else -1
                bild.setze(x - 1, unten, GELB)
                bild.setze(x + 1, unten, GELB)
                if hoch < 3:                                         # sprühen seitlich über die Flasche
                    bild.setze(x - 2, FLASCHE_Y - (s > 0), ORANGE)
                    bild.setze(x + 2, FLASCHE_Y - (s < 0), ORANGE)
                if hoch > 0:
                    bild.setze(x + s, unten + 1, ORANGE)
                if hoch > 1:
                    bild.setze(x - s, unten + 2, dimmen(ORANGE, 0.45))
        for hx, hy in haende:
            hand(bild, hx, hy, von_oben=True)
        if holz is not None:
            streichholz(bild, holz, FLASCHE_Y, f)
        liste.append(bild)
    return jedes_bild_anders(liste, HIMMEL)
