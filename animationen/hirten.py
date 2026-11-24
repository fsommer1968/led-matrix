"""Hirten auf dem Feld: Schafe grasen am Lagerfeuer, plötzlich wird es hell, ein Engel erscheint
mit Lichtschein; der Stern geht auf und die Hirten ziehen mit den Schafen hinterher – 255 Bilder.
"""
import colorsys
import math
import random

from basis import (B, GELB, GOLD, NACHTBLAU, WEISS, Bild, dimmen, mischen)

NAME = "hirten"
TITEL = "Hirten auf dem Feld, Engel erscheint"

WIESE = (6, 48, 14)
WIESE_KANTE = (20, 95, 30)
WIESE_LICHT = (70, 130, 40)
WOLLE = (235, 235, 225)
SCHAF_KOPF = (165, 115, 80)
SCHAF_BEIN = (120, 85, 60)
HAUT = (235, 165, 115)
STAB = (150, 90, 35)
LICHT = (255, 200, 80)
FLUEGEL = (150, 200, 255)
BODEN = 13                                    # oberste Zeile der Wiese; Füße stehen auf Zeile 12
# Die Matrix speichert nur 80 KB je Animation, jedes Bild einzeln komprimiert (spaltenweise):
# Einzelne Punkte und weiche Verläufe sind teuer, gleiche Nachbarspalten fast umsonst. Darum
# blinken die Sterne reihum auf (jeder ist nur einen Teil der Zeit an). Beim Engel wird der ganze
# Himmel hell (eine Farbe kostet nichts) und ein Lichtstrahl in zwei Stufen fällt bis auf die
# Wiese – statt eines weichen runden Verlaufs (23.11.2026).
STERN = (255, 240, 200)
STERN_AN = 0.30                               # Anteil der Zeit, in der ein Stern leuchtet
# (x, y, Periode in Bildern, Phase 0…1) – Perioden teilen 255, die Schleife läuft nahtlos
STERNE = [(2, 5, 85, 0.00), (59, 0, 51, 0.35), (39, 1, 85, 0.60), (5, 1, 51, 0.80), (12, 4, 85, 0.25),
          (51, 5, 51, 0.10), (63, 7, 85, 0.45), (49, 2, 85, 0.90), (43, 4, 51, 0.55), (33, 5, 85, 0.15),
          (25, 3, 51, 0.70), (56, 2, 85, 0.75), (20, 0, 85, 0.50), (36, 0, 51, 0.20), (29, 6, 85, 0.35),
          (46, 7, 51, 0.95)]
HIMMEL_HELL = 0.15                            # Himmel beim Engel: so viel vom LICHT
# Lichtstrahl: (halbe Breite, Stärke), von außen nach innen
SCHEIN = [(9, 0.27), (6, 0.42)]
WIESE_HELL = (0.65, 1.0)                      # wie stark die Wiese unter den beiden Stufen leuchtet
WIESE_HELL_SONST = 0.35                       # … und überall sonst

# Schaf 7×5, schaut nach rechts: steht, grast, läuft (2 Schritte)
SCHAF = {
    "steht": [".wwww..", "wwwwwkk", "wwwwwk.", ".wwww..", ".l..l.."],
    "grast": [".wwww..", "wwwww..", "wwwwwk.", ".wwwwkk", ".l..l.."],
    "lauf0": [".wwww..", "wwwwwkk", "wwwwwk.", ".wwww..", "l....l."],
    "lauf1": [".wwww..", "wwwwwkk", "wwwwwk.", ".wwww..", "..ll..."],
}
# Hirte 6×9 mit Stab (Krümme oben), Kopftuch t, Gesicht h, Umhang u, Füße b
HIRTE = {
    "steht": ["....cc", ".tt.c.", ".hh.c.", "uuuhc.", "uuu.c.", "uuu.c.", "uuu.c.", "uuu.c.", "bbb.c."],
    "lauf0": ["....cc", ".tt.c.", ".hh.c.", "uuuhc.", "uuu.c.", "uuu.c.", "uuu.c.", "uuu.c.", "bbb.c."],
    "lauf1": ["....cc", ".tt.c.", ".hh.c.", "uuuhc.", "uuu.c.", "uuu.c.", "uuu.c.", "uuu.c.", ".b..c."],
    "staunt": ["h...cc", "htt.c.", "uhh.c.", "uuuhc.", "uuu.c.", "uuu.c.", "uuu.c.", "uuu.c.", "bbb.c."],
    "kniet": ["......", "......", "h...cc", "htt.c.", "uhh.c.", "uuuhc.", "uuu.c.", "uuuuc.", "uuuuc."],
    "sitzt": ["......", "......", ".tt...", ".hh...", "uuu...", "uuuh..", "uuu...", "uuuuu.", "kkk.b."],
}
# (x, Umhang, Kopftuch): zwei stehen links, einer sitzt am Feuer
HIRTEN = [(1, (40, 140, 60), (220, 130, 40)), (8, (60, 70, 200), (230, 230, 230)),
          (15, (170, 50, 25), (220, 190, 140))]
ENGEL = [
    ["....ggg....", "f...hhh...f", "ff..hhh..ff", "fff.www.fff", ".fffwwwfff.", "..fwwwwwf..",
     "...wwwww...", "..wwwwwww.."],
    ["....ggg....", "....hhh....", "....hhh....", "..ffwwwff..", ".fffwwwfff.", "ffffwwwffff",
     "ff.wwwww.ff", "..wwwwwww.."],
]
# (x, schaut in Ruhe nach rechts, schaut beim Engel nach rechts, Takt fürs Grasen)
SCHAFE = [(29, False, True, 0), (48, True, False, 3), (57, False, False, 1)]
FEUER_X = 24
ENGEL_X = 37
STERN_X = 59
START_ZUG = 158                               # ab hier ziehen alle dem Stern nach


def feuer(bild, f, glut):
    """Lagerfeuer 5 breit: Scheite, darüber drei Zeilen Flammen; glut 1 → 0 brennt herunter."""
    z = random.Random(f // 2)
    x = FEUER_X
    for dx in (-2, -1, 0, 1, 2):                                  # Scheite
        bild.setze(x + dx, 12, (140, 60, 15))
    bild.setze(x - 2, 11, (140, 60, 15))
    bild.setze(x + 2, 11, (140, 60, 15))
    if glut <= 0.05:
        bild.setze(x, 12, (150, 30, 0) if (f // 6) % 2 else (90, 20, 0))
        return
    for dx in (-1, 0, 1):                                         # Glut und untere Flamme
        bild.setze(x + dx, 11, (255, 60, 0) if z.random() < 0.7 else (255, 120, 0))
    if glut > 0.3:
        seite = z.choice((-1, 0, 1))
        bild.setze(x, 10, (255, 140, 0))
        bild.setze(x + seite, 10, (255, 110, 0))
        bild.setze(x + z.choice((-1, 0, 0, 1)), 9, GELB if z.random() < 0.6 else (255, 150, 0))
    if glut > 0.7 and z.random() < 0.5:
        bild.setze(x + z.choice((-1, 0, 1)), 8, (255, 170, 0))
    schein = mischen(WIESE_KANTE, (200, 90, 10), round(glut * 4) / 4 * 0.5)
    for dx in (-2, -1, 0, 1, 2):                                  # Feuerschein auf der Wiese, nur
        bild.setze(x + dx, BODEN, schein)                         # unter dem Feuer (kostet kaum)


def sterne(bild, f):
    for x, y, periode, phase in STERNE:
        t = abs((f / periode + phase) % 1 - 0.5) / STERN_AN       # 0 = Mitte des Aufleuchtens
        if t < 0.5:
            bild.setze(x, y, STERN if t < 0.25 else dimmen(STERN, 0.5))


def stufe(x, mitte, f):
    """Stufe des Lichtstrahls in Spalte x (0 außen, 1 innen) oder None; der Strahl atmet."""
    d = abs(x - mitte) - round(math.sin(f / 5))
    treffer = [k for k, (hb, _) in enumerate(SCHEIN) if d <= hb]
    return treffer[-1] if treffer else None


def stern(bild, sx, sy, f):
    puls = (f // 5) % 2
    for k in range(1, 4):                                         # Schweif nach links oben
        bild.setze(sx - 1 - k, sy - (k + 1) // 2, dimmen(GOLD, 0.6 - 0.1 * k))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        bild.setze(sx + dx, sy + dy, GELB)
    for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        bild.setze(sx + dx, sy + dy, dimmen(GOLD, 0.8 if puls else 0.35))
    for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        bild.setze(sx + dx, sy + dy, dimmen(GOLD, 0.3 if puls else 0.6))
    bild.setze(sx, sy, WEISS)


def _matrixfarbe(c):
    """Farbe, wie die Matrix sie zeigt (7/4/5 Bit H/S/V, wie hsv16 in led/pi/matrix_spieler.py)."""
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
    for f in range(255):
        hell = 0.0                                                # Licht des Engels 0…1
        if 58 <= f < 146:
            hell = min(1.0, (f - 58) / 16) if f < 130 else (146 - f) / 16
        hell = round(hell * 8) / 8
        bild = Bild(mischen(NACHTBLAU, dimmen(LICHT, HIMMEL_HELL), hell))
        if hell < 0.4:                                            # das Licht überstrahlt die Sterne
            sterne(bild, f)
        # Engel: schwebt von oben herein (58–76), bleibt, steigt wieder auf (130–146)
        ex, ey = ENGEL_X, 0
        if 58 <= f < 76:
            ey = -(76 - f) // 2
        elif 130 <= f < 146:
            ey = -(f - 130) // 2
        for x in range(B):                                        # Lichtstrahl um den Engel, Wiese
            k = stufe(x, ex + 5, f) if hell > 0 else None
            nah = WIESE_HELL_SONST * hell
            if k is not None:
                for y in range(BODEN):
                    bild.setze(x, y, mischen(NACHTBLAU, dimmen(LICHT, SCHEIN[k][1]), hell))
                nah = WIESE_HELL[k] * hell
            bild.setze(x, BODEN, mischen(WIESE_KANTE, WIESE_LICHT, nah))
            for y in range(BODEN + 1, 16):
                bild.setze(x, y, mischen(WIESE, WIESE_KANTE, nah * 0.7))
        weg = max(0, (f - START_ZUG) * 2 // 3)
        if f >= 138:                                              # Stern geht auf und bleibt
            stern(bild, STERN_X, max(2, 12 - (f - 138) // 2), f)
        # Schafe (laufen voraus)
        for i, (sx, rechts, zum_engel, takt) in enumerate(SCHAFE):
            if weg:
                pose, rechts = f"lauf{((f + i * 2) // 3) % 2}", True
            elif 62 <= f < START_ZUG:                             # schauen zum Engel, dann zum Stern
                pose, rechts = "steht", zum_engel if f < 146 else True
            else:
                pose = "grast" if ((f + takt * 13) // 13) % 4 in (0, 1) else "steht"
            bild.figur(sx + weg, 8, SCHAF[pose], {"w": WOLLE, "k": SCHAF_KOPF, "l": SCHAF_BEIN},
                       spiegeln=not rechts)
        # Hirten: zwei stehen, einer sitzt am Feuer; beim Engel staunen sie, einer kniet
        for i, (hx, umhang, tuch) in enumerate(HIRTEN):
            if weg:
                pose = f"lauf{((f + i * 3) // 4) % 2}"
            elif 68 <= f < 146:
                pose = ("staunt", "kniet", "staunt")[i]
            elif f >= 146:
                pose = "steht"
            else:
                pose = "sitzt" if i == 2 else "steht"
            bild.figur(hx + weg, 4, HIRTE[pose],
                       {"t": tuch, "h": HAUT, "u": umhang, "c": STAB, "b": (120, 85, 60),
                        "k": (110, 70, 35)})
        feuer(bild, f, max(0.0, min(1.0, (235 - f) / 40)))
        if 58 <= f < 146:
            bild.figur(ex, ey, ENGEL[(f // 6) % 2], {"g": GELB, "h": HAUT, "w": WEISS, "f": FLUEGEL})
        liste.append(bild)
    return _jedes_bild_anders(liste)
