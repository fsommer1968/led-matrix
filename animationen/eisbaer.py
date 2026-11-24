"""Eisbär: Eisbärin und Junges auf einer Eisscholle im dunklen Polarmeer. Beide schlafen Nase an
Nase (eine Sternschnuppe zieht vorbei), wachen auf und tapsen über das Eis; das Junge hüpft voraus,
springt zu weit, rutscht aus und plumpst ins Wasser (Fontäne, Spritzer, Ringe), paddelt zurück und
klettert wieder hinauf, schüttelt sich; die Mutter schaut zu und stupst es an, dann trotten beide
heim und legen sich wieder nebeneinander. Mond mit Spiegelung, vier Sterne, sanfte Wellen. Die Runde
geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum eine Scholle mit gerader Oberkante, einfarbiges Meer
mit wenigen Wellenkämmen und Lichtern nur im offenen Wasser (immer dieselben Spalten), wenige
Sterne, Bären mit flachem Rücken (gleiche Nachbarspalten), kein Schneefall. Alles, was sich
wiederholt (Wellen, Sterne, Glitzern, Atem), hat eine Periode, die in 255 aufgeht.
"""
import math

from basis import B, NACHTBLAU, Bild, dimmen, sternschnuppe

NAME = "eisbaer"
TITEL = "Eisbärin mit Jungem auf der Eisscholle"

MEER = (0, 24, 78)                             # große Fläche: gedämpft
WELLE = (0, 85, 165)                           # Wellenkamm
LICHT = (0, 50, 120)                           # Lichter auf dem Wasser
EIS_KANTE = (95, 145, 220)                     # Oberkante der Scholle, bläulich (die Bären sind heller)
EIS = (40, 78, 150)
EIS_TIEF = (12, 44, 104)                       # unter Wasser
FELL = (255, 250, 232)
FELL_DUNKEL = (205, 185, 140)                  # abgewandter Lauf, cremefarben
AUGE = (0, 0, 0)
NASE = (45, 45, 58)                            # fast schwarz; ganz schwarz verschwände vor dem Nachthimmel
TROPFEN = (170, 215, 255)
MOND = (240, 230, 170)
MONDLICHT = (175, 165, 110)                    # Spiegelung auf dem Wasser
STERN = (255, 240, 200)
STERNE = [(10, 1, 0, 51), (27, 0, 20, 85), (43, 1, 40, 51), (51, 3, 60, 85)]    # x, y, Phase, Periode (teilt 255)

LINKS, RECHTS = 6, 47                          # Scholle von … bis (Spalten)
EIS_Y, WASSER_Y = 10, 12                       # Oberkante der Scholle, oberste Zeile des Meers
WELLEN_ABSTAND, WELLEN_WEG = 12, 36            # ein Kamm alle 12 Spalten; 36 Spalten je Runde

# Mutter (Blick nach rechts), 16 breit: w Fell, d abgewandter Lauf, e Ohr, a Auge, k Nase
M_RUMPF = ["..wwwwww........", ".wwwwwwwww.e....", "wwwwwwwwwwwwww..", "wwwwwwwwwwwwawwk", ".www.dd.wwwwwww."]
M_STEHT = M_RUMPF + [".ww..dd..ww.....", ".ww..dd..ww....."]
M_WEIT = M_RUMPF + [".ww..dd..ww.....", "ww....dd..ww...."]
M_ENG = M_RUMPF + [".ww..dd..ww.....", "..ww.dd.ww......"]
M_GANG = [M_STEHT, M_WEIT, M_STEHT, M_ENG]
M_DUCKT = M_RUMPF + [".ww..dd..ww....."]                         # beim Aufstehen und Hinlegen
M_SCHAUT = ["..wwwwww...e....", ".wwwwwwwwwwwww..", "wwwwwwwwwwwwawwk", "wwwwwwwwwwwwwww.",
            ".www.dd.www.....", ".ww..dd..ww.....", ".ww..dd..ww....."]       # Kopf gehoben
M_UNTEN = ["..wwwwww........", ".wwwwwwwww......", "wwwwwwwwwww.e...", "wwwwwwwwwwwwwww.",
           ".www.dd.wwwwwawk", ".ww..dd..wwwwww.", ".ww..dd..ww....."]        # Kopf gesenkt
M_LIEGT = ["..wwwwww...e....", ".wwwwwwwwwwwww..", "wwwwwwwwwwwwawwk", "wwwwwwwwwwwwwww."]
M_SCHLAEFT = ["..wwwwww........", ".wwwwwwwww.e....", "wwwwwwwwwwwwwww.", "wwwwwwwwwwwwwwwk"]
# Junges (Blick nach rechts), 8 breit
J_RUMPF = ["....ww..", ".wwwwww.", "wwwwwawk", "wwwwwwww"]
J_STEHT = J_RUMPF + [".ww.ww.."]
J_GEHT = J_RUMPF + ["ww...ww."]
J_LIEGT = J_RUMPF
J_SCHLAEFT = [".wwww.e.", "wwwwwwww", "wwwwwwwk"]
J_SITZT = ["..ww....", ".wwww...", ".wwawk..", "wwwww.w.", "wwwwwwww"]      # ausgerutscht, auf dem Po
J_RUDERT = ["..ww..w.", ".wwww.w.", ".wwawkw.", "wwwwww..", "wwwwwww."]     # … und rudert mit den Pfoten
J_SCHWIMMT = [".....ww.", "....wwww", "....wawk", "wwwwwwww"]               # Kopf und Rücken über Wasser
J_TAUCHT = [".....ww.", "....wwww", "....wawk", "..wwwwww"]
J_HAENGT = ["...ww.", ".wwww.", ".wwawk", "wwwwww", "wwwwww", "www...", "www..."]   # Pfoten auf der Kante
J_HALB = ["....ww..", "...wwww.", ".wwwwawk", "wwwwwwww", "wwww.ww.", "ww......", "w......."]

FARBEN = {"w": FELL, "d": FELL_DUNKEL, "e": FELL, "a": AUGE, "k": NASE}

# Ablauf (Bildnummern)
M_X0, M_X1, M_X2 = 6, 17, 22                   # Mutter: Schlafplatz, erster Halt, bei der Kante
J_X0, J_X1, J_RAND = 23, 36, 40                # Junges: Schlafplatz, Spielplatz, an der Kante
J_WACH, J_AUF, J_LOS, J_SPIELT = 8, 14, 18, 58
M_WACH, M_AUF, M_LOS, M_HALT = 16, 24, 28, 76
RUTSCHT, FAELLT, PLATSCH, TAUCHT_AUF = 92, 98, 103, 114
AM_RAND, HALB_OBEN, OBEN, GESCHUETTELT = 152, 160, 168, 184
STUPS, HEIM, M_DAHEIM, J_DAHEIM = 184, 194, 236, 240
M_LEGT_SICH, M_SCHLAF, J_SCHLAF = 240, 246, 247
PLATSCH_X = 53
MOND_X = 59
SCHNUPPE = 250


def gleiten(f, f0, f1, a, b):
    """Wert zwischen a (bei f0) und b (bei f1), davor und danach fest."""
    t = min(1.0, max(0.0, (f - f0) / (f1 - f0)))
    return a + (b - a) * t


def auf_eis(bild, x, zeilen, spiegeln=False, hoch=0):
    """Zeichnet die Figur mit den Füßen auf der Scholle (hoch = Pixel darüber)."""
    bild.figur(round(x), EIS_Y - len(zeilen) - hoch, zeilen, FARBEN, spiegeln)


def bis_wasser(bild, x, y, zeilen, spiegeln=False):
    """Zeichnet nur, was über dem Wasser ist (der Rest ist eingetaucht)."""
    if y < WASSER_Y:
        bild.figur(x, y, zeilen[:WASSER_Y - y], FARBEN, spiegeln)


def hintergrund(bild, f):
    for x, y, phase, periode in STERNE:                              # wenige Sterne, funkeln langsam
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    sternschnuppe(bild, (f - SCHNUPPE) % 255, 0, 46, 0, laenge=7)       # über den Schlafenden, über die Naht
    bild.kreis(MOND_X, 2, 2.2, MOND)
    bild.rechteck(0, WASSER_Y, B, 16 - WASSER_Y, MEER)
    glitzern = (f // 17) % 3                                         # Mond spiegelt sich, ruhiges Glitzern
    if glitzern != 2:
        bild.rechteck(MOND_X - 1, WASSER_Y + 1, 3, 1, MONDLICHT)
    if glitzern != 1:
        bild.rechteck(MOND_X - 1, WASSER_Y + 3, 3, 1, dimmen(MONDLICHT, 0.6))
    schub = f * WELLEN_WEG // 255
    for x in list(range(LINKS)) + list(range(RECHTS + 1, B)):        # Wellen nur im offenen Wasser
        ort = (x - schub) % WELLEN_ABSTAND
        if 1 <= ort < 5:
            bild.setze(x, WASSER_Y - 1, WELLE)                       # Kamm
        if ort < 6:
            bild.setze(x, WASSER_Y, LICHT)                           # … mit hellem Fuß
        if ort in (8, 9, 10):
            bild.setze(x, WASSER_Y + 2, LICHT)                       # Licht im Wellental
    bild.rechteck(LINKS + 1, EIS_Y, RECHTS - LINKS, 1, EIS_KANTE)
    bild.rechteck(LINKS, EIS_Y + 1, RECHTS - LINKS + 1, 2, EIS)
    bild.rechteck(LINKS + 1, EIS_Y + 3, RECHTS - LINKS - 1, 1, EIS_TIEF)


def atem(f):
    """Im Schlaf hebt und senkt sich der Rücken (läuft über die Naht der Runde hinweg)."""
    return ((f - M_SCHLAF) % 255 // 8) % 2


def mutter(bild, f):
    if f < M_WACH or f >= M_SCHLAF:
        figur = M_SCHLAEFT if atem(f) else ["................"] + M_SCHLAEFT[1:]
        auf_eis(bild, M_X0, figur)
    elif f < M_AUF or f >= M_LEGT_SICH + 2:
        auf_eis(bild, M_X0, M_LIEGT)
    elif f < M_AUF + 2 or f >= M_LEGT_SICH:
        auf_eis(bild, M_X0, M_DUCKT)
    elif f < M_LOS or f >= M_DAHEIM:
        auf_eis(bild, M_X0, M_STEHT)
    elif f < M_HALT:                                                 # tapst dem Jungen nach
        auf_eis(bild, gleiten(f, M_LOS, M_HALT, M_X0, M_X1), M_GANG[(f // 4) % 4])
    elif f < RUTSCHT + 3:
        auf_eis(bild, M_X1, M_STEHT)
    elif f < PLATSCH + 8:                                            # merkt auf
        auf_eis(bild, M_X1, M_SCHAUT)
    elif f < 132:                                                    # geht zur Kante
        auf_eis(bild, gleiten(f, PLATSCH + 8, 132, M_X1, M_X2), M_GANG[(f // 4) % 4])
    elif f < AM_RAND:                                                # schaut dem Jungen zu
        auf_eis(bild, M_X2, M_STEHT)
    elif f < OBEN:                                                   # beugt sich zu ihm hinunter
        auf_eis(bild, M_X2, M_UNTEN)
    elif f < STUPS:
        auf_eis(bild, M_X2, M_STEHT)
    elif f < HEIM - 2:                                               # stupst das Junge an
        auf_eis(bild, M_X2, M_UNTEN)
    elif f < HEIM:
        auf_eis(bild, M_X2, M_STEHT)
    else:                                                            # heim
        auf_eis(bild, gleiten(f, HEIM, M_DAHEIM, M_X2, M_X0), M_GANG[(f // 4) % 4], spiegeln=True)


def junges(bild, f):
    if f < J_WACH or f >= J_SCHLAF:
        auf_eis(bild, J_X0, J_SCHLAEFT, spiegeln=True)
    elif f < J_AUF or f >= J_DAHEIM + 2:
        auf_eis(bild, J_X0, J_LIEGT, spiegeln=True)
    elif f < J_LOS:
        auf_eis(bild, J_X0, J_STEHT, spiegeln=f < J_LOS - 2)
    elif f < J_SPIELT:                                               # trabt voraus
        schritt = (f // 4) % 2
        auf_eis(bild, gleiten(f, J_LOS, J_SPIELT, J_X0, J_X1), J_GEHT if schritt else J_STEHT, hoch=schritt)
    elif f < RUTSCHT:                                                # spielt: drei Hopser, der dritte zu weit
        nr, t = divmod(f - J_SPIELT, 12)
        hoch = round(3.2 * math.sin(math.pi * min(t, 9) / 9))
        x = round(gleiten(t, 0, 9, J_X1, J_RAND)) if nr == 2 else J_X1
        auf_eis(bild, x, J_STEHT if hoch == 0 else J_GEHT, spiegeln=nr == 1, hoch=hoch)   # der zweite zur Mutter
    elif f < FAELLT:                                                 # rutscht aus, auf dem Po zur Kante
        x = round(gleiten(f, RUTSCHT, FAELLT, J_RAND, J_RAND + 5))
        auf_eis(bild, x, J_RUDERT if (f // 2) % 2 else J_SITZT)
        bild.setze(x - 1 - f % 2, EIS_Y - 1, EIS_KANTE)              # Eis stäubt
    elif f < PLATSCH + 2:                                            # über die Kante und hinein
        t = f - FAELLT
        bis_wasser(bild, J_RAND + 5 + t, EIS_Y - 5 + round(0.3 * t * t), J_RUDERT if (f // 2) % 2 else J_SITZT)
    elif f < TAUCHT_AUF:
        pass                                                         # unter Wasser
    elif f < AM_RAND:                                                # taucht auf und paddelt zurück
        x = round(gleiten(f, TAUCHT_AUF + 8, AM_RAND, 55, RECHTS + 1))
        tief = max(0, 3 - (f - TAUCHT_AUF))
        paddelt = (f // 4) % 2
        bis_wasser(bild, x, WASSER_Y - 4 + tief, J_TAUCHT if paddelt or tief else J_SCHWIMMT, spiegeln=True)
        if paddelt and not tief:                                     # Pfoten spritzen
            bild.setze(x - 1, WASSER_Y - 1, TROPFEN)
    elif f < HALB_OBEN:
        bild.figur(RECHTS - 1, EIS_Y - 5, J_HAENGT, FARBEN, spiegeln=True)
    elif f < OBEN:
        bild.figur(RECHTS - 5, EIS_Y - 5, J_HALB, FARBEN, spiegeln=True)
    elif f < GESCHUETTELT:                                           # schüttelt sich
        nass = OBEN + 3 <= f < GESCHUETTELT - 3
        auf_eis(bild, J_RAND + (nass and (f // 2) % 2), J_STEHT, spiegeln=True)
        if nass:
            for k in range(3):
                bild.setze(J_RAND - 1 + k * 4 + (f + k) % 3, EIS_Y - 6 - (f + k) % 2 * 2, TROPFEN)
    elif f < HEIM + 4:
        auf_eis(bild, J_RAND, J_STEHT, spiegeln=True)
    else:                                                            # trottet der Mutter nach
        x = gleiten(f, HEIM + 4, J_DAHEIM, J_RAND, J_X0)
        auf_eis(bild, x, J_GEHT if (f // 3) % 2 else J_STEHT, spiegeln=True)


def spritzer(bild, f):
    """Wasser spritzt auf, wo das Junge eintaucht; danach laufen zwei Ringe auseinander."""
    t = f - PLATSCH
    if 0 <= t < 4:                                                   # Fontäne
        bild.rechteck(PLATSCH_X - 1, WASSER_Y - 2 - 2 * min(t, 2), 3, 2 + 2 * min(t, 2), TROPFEN)
        bild.rechteck(PLATSCH_X, WASSER_Y - 1 - 2 * min(t, 2), 1, 1 + 2 * min(t, 2), FELL)
    if 2 <= t < 14:
        for k in range(5):
            w = math.pi * (0.2 + 0.6 * k / 4)
            x = PLATSCH_X + math.cos(w) * t * 0.8
            y = WASSER_Y - 5 - math.sin(w) * t * 1.3 + 0.12 * t * t
            if y < WASSER_Y:
                bild.setze(x, y, dimmen(TROPFEN, 1 - max(0, t - 6) / 12))
    if 2 <= t < 12:
        for richtung in (-1, 1):
            x = PLATSCH_X + richtung * (1 + t * 0.7)
            if x > RECHTS:
                bild.rechteck(round(x), WASSER_Y, 2, 1, WELLE)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        hintergrund(bild, f)
        mutter(bild, f)
        junges(bild, f)
        spritzer(bild, f)
        liste.append(bild)
    return liste
