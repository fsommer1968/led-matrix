"""Lichterhaus: ein dunkles Haus mit Treppengiebel wird Licht für Licht geschmückt – Dachkante,
Traufe, Fenster, Tür, Tanne im Garten, Leucht-Rentier –, dann blinkt und läuft alles in Mustern
(Lauflicht, Gruppen im Wechsel, goldene Welle, Regenbogen) – 255 Bilder.
"""
import colorsys
import math

from basis import (B, GELB, GOLD, NACHTBLAU, PINK, ROT, WEISS, Bild, dimmen, regenbogen)

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "lichterhaus"
TITEL = "Haus wird mit Lichterketten geschmückt"

WAND = (33, 23, 21)
DACH = (36, 30, 44)
FENSTER = (120, 75, 20)
TUER = (33, 16, 5)
TANNE = (0, 70, 22)
BODEN = (120, 130, 165)
GRUEN = (0, 220, 60)
BLAU = (0, 90, 255)
EIS = (170, 215, 255)
WARM = (255, 215, 140)
DACHFARBE = {7: ROT, 5: GELB, 4: PINK, 2: BLAU}   # Lichterkette am Dach je Stufe (oberste Zeile)
BUNT5 = [ROT, GELB, GRUEN, BLAU, PINK]
# Die Matrix speichert nur 80 KB je Animation, jedes Bild einzeln komprimiert (spaltenweise):
# Gleiche Spalten (auch im Zweierraster) kosten fast nichts, jede neue Spaltenform und jeder
# einzelne Punkt kostet. Darum hat das Haus einen Treppengiebel statt eines schrägen Dachs, die
# Lichterketten hängen in einem festen Zweierraster, die rechte Fensterhälfte ist spaltengleich
# mit der linken, Welle und Regenbogen laufen von oben nach unten (eine Farbe je Zeile), das
# Rentier ist erst zu sehen, wenn es leuchtet, und die Sterne blinken reihum auf
# (23.11.2026).
STERN = (255, 240, 200)
STERN_AN = 0.2                                # Anteil der Zeit, in der ein Stern leuchtet
# (x, y, Periode in Bildern, Phase 0…1); Perioden teilen 255. Nicht über den Fenstern: Dort ist
# die rechte Haushälfte eine Kopie der linken, ein Stern darüber würde das teuer stören.
STERNE = [(1, 2, 85, 0.00), (14, 1, 51, 0.30), (15, 5, 85, 0.55), (10, 2, 51, 0.80), (49, 2, 51, 0.05),
          (55, 1, 85, 0.70), (62, 0, 51, 0.45), (2, 7, 85, 0.40), (32, 0, 85, 0.20), (58, 3, 51, 0.60)]
HX, HB = 18, 29                               # Hauswand: x 18…46, Zeilen 9…14; Dach bis Zeile 8
# Treppengiebel: (erste Spalte, letzte Spalte, oberste Dachzeile). Die Stufen liegen genau über
# den Abschnitten der Fassade (Rand, Fenster, Wandstreifen, Tür) – so entsteht keine zusätzliche
# Spaltenform.
STUFEN = [(17, 20, 7), (21, 27, 5), (28, 29, 4), (30, 34, 2), (35, 36, 4), (37, 43, 5), (44, 47, 7)]
DACH_OBEN = {x: oben for x0, x1, oben in STUFEN for x in range(x0, x1 + 1)}
FENSTER_X = (22, 38)                          # Fenster 5×3, Zeilen 11…13
TUER_X = 31                                   # Tür 3×5, Zeilen 10…14
SCHORNSTEIN = 35                              # steht auf dem rechten Wandstreifen
TANNE_X = 8
RENTIER_X = 50
RENTIER = [   # schaut nach links zum Haus; n = rote Nase
    "a.a.a.......",
    ".aaa........",
    "..hh........",
    "nhhh........",
    "..hh......b.",
    "..hbbbbbbbb.",
    "..bbbbbbbbb.",
    "...bbbbbbb..",
    "...b.b..b.b.",
    "...b.b..b.b.",
]
TANNE_ZEILEN = ((5, 0), (6, 1), (7, 1), (8, 2), (9, 2), (10, 2), (11, 3), (12, 3), (13, 3))


def lampen():
    """Alle Lichter als (x, y, Gruppe, Farbe) und die Reihenfolge des Aufhängens als Schritte
    (ein Schritt = Liste von Lampen-Nummern, die zusammen angehen)."""
    lampen, schritte = [], []

    def dazu(punkte, gruppe, farbe, je_schritt=1):
        for k in range(0, len(punkte), je_schritt):
            schritt = []
            for n, (x, y) in enumerate(punkte[k:k + je_schritt]):
                f = farbe(k + n, x, y) if callable(farbe) else farbe
                schritt.append(len(lampen))
                lampen.append((x, y, gruppe, f))
            schritte.append(schritt)

    bunt = lambda i, x, y: BUNT5[i % 5]                             # noqa: E731
    dazu([(x, DACH_OBEN[x]) for x in range(HX + 1, HX + HB - 1, 2)], 0,
         lambda i, x, y: DACHFARBE[y])                              # Dachkante, je Stufe eine Farbe
    dazu([(x, 9) for x in range(HX + 1, HX + HB - 1, 2)], 1, EIS)   # Traufe: Eiszapfen-Lichter
    for fx in FENSTER_X:                                            # Fensterrahmen
        rahmen = [(fx - 1 + 2 * k, 10) for k in range(4)] + [(fx + 5, 12)]
        rahmen += [(fx + 5 - 2 * k, 14) for k in range(4)] + [(fx - 1, 12)]
        dazu(rahmen, 2, ROT)
    tx = TUER_X
    dazu([(tx - 1, 14), (tx - 1, 12), (tx - 1, 10), (tx + 3, 10), (tx + 3, 12), (tx + 3, 14)], 3, GRUEN)
    tanne = [(8, 6), (9, 8), (7, 9), (10, 10), (8, 11), (6, 11), (11, 12), (9, 13), (7, 13), (5, 13)]
    dazu(tanne[::-1], 4, bunt)
    dazu([(TANNE_X, 4)], 4, GELB)                                   # Stern auf der Tanne
    rentier = [(RENTIER_X + dx, 5 + dy) for dx in range(11, -1, -1) for dy in range(9, -1, -1)
               if dx < len(RENTIER[dy]) and RENTIER[dy][dx] != "."]
    dazu(rentier, 5, lambda i, x, y: ROT if RENTIER[y - 5][x - RENTIER_X] == "n" else WARM, je_schritt=3)
    return lampen, schritte


LAMPEN, SCHRITTE = lampen()
AUFBAU = 128                                  # so viele Bilder dauert das Schmücken


def sterne(bild, f):
    for x, y, periode, phase in STERNE:
        t = abs((f / periode + phase) % 1 - 0.5) / STERN_AN       # 0 = Mitte des Aufleuchtens
        if t < 0.5:
            bild.setze(x, y, STERN if t < 0.25 else dimmen(STERN, 0.5))


def haus(bild):
    bild.rechteck(HX, 9, HB, 6, WAND)
    for x, oben in DACH_OBEN.items():                              # Dach
        bild.rechteck(x, oben, 1, 9 - oben, DACH)
    if SCHORNSTEIN:
        bild.rechteck(SCHORNSTEIN, 1, 2, DACH_OBEN[SCHORNSTEIN] - 1, WAND)
    for fx in FENSTER_X:
        bild.rechteck(fx, 11, 5, 3, FENSTER)
    bild.rechteck(TUER_X, 10, 3, 5, TUER)
    for y, r in TANNE_ZEILEN:                                      # Tanne im Garten
        bild.rechteck(TANNE_X - r, y, 2 * r + 1, 1, TANNE)
    bild.setze(TANNE_X, 14, TUER)
    bild.rechteck(0, 15, B, 1, BODEN)


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
    seit = {}                                                      # Lampe → Bild, in dem sie anging
    for f in range(255):
        bild = Bild(NACHTBLAU)
        sterne(bild, f)
        haus(bild)
        fertig = min(len(SCHRITTE), (f - 4) * len(SCHRITTE) // (AUFBAU - 8)) if f > 4 else 0
        for schritt in SCHRITTE[:fertig]:
            for nr in schritt:
                seit.setdefault(nr, f)
        for nr, start in seit.items():
            x, y, gruppe, eigen = LAMPEN[nr]
            if f < AUFBAU:                                         # geht an: kurz weiß aufblitzen
                farbe = WEISS if f - start < 2 else eigen
            elif f < AUFBAU + 6:                                   # alles fertig: einmal hell auf
                farbe = WEISS if (f - AUFBAU) < 3 else eigen
            elif f < 166:                                          # Lauflicht: weiße Streifen wandern
                farbe = WEISS if ((x - f) // 2) % 8 == 0 else eigen   # nach rechts durch alle Ketten
            elif f < 200:                                          # Gruppen blinken im Wechsel
                farbe = eigen if (gruppe + (f - 166) // 6) % 2 == 0 else None
            elif f < 228:                                          # goldene Welle von oben nach unten
                welle = 0.5 + 0.5 * math.sin(y / 2 - (f - 200) / 2.5)
                farbe = dimmen(GOLD if welle < 0.8 else GELB, round((0.25 + 0.75 * welle) * 6) / 6)
            else:                                                  # Regenbogen zieht von oben durch
                farbe = regenbogen(y * 24 - (f - 228) * 14)
            bild.setze(x, y, farbe)
        liste.append(bild)
    return _jedes_bild_anders(liste)
