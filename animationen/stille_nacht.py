"""Stille Nacht: ruhiges Bild – links die Krippe in voller Höhe mit schlafendem Kind und
leuchtendem Heiligenschein, Kerzen links und rechts davon; rechts erscheinen langsam "STILLE"
und danach "NACHT" in Gold – 255 Bilder.
"""
import colorsys
import math
import random

from basis import GELB, GOLD, Bild, dimmen, mischen, textbreite

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "stille_nacht"
TITEL = "Stille Nacht: Kind in der Krippe, Kerzenlicht"

HIMMEL = (0, 0, 20)
HOLZ = (49, 26, 8)
HOLZ_DUNKEL = (33, 17, 5)
STROH = (230, 180, 40)
TUCH = (240, 240, 250)
TUCH_SCHATTEN = (150, 170, 220)
HAUT = (214, 171, 143)
SCHEIN = (255, 210, 90)
WACHS = (235, 225, 200)
TEXT_X0, TEXT_X1 = 28, 63                     # Platz für die Wörter rechts
KX, KY = 7, 6                                 # Mitte des Kopfes
# (x, y, Phase) – wenige ruhige Sterne, über und unter der Schrift und über der Krippe. Jeder
# leuchtet nur einen Teil der Zeit (STERN_AB): Die Matrix speichert nur 80 KB je Animation, und
# jeder einzelne Punkt kostet in jedem Bild rund 5 Bytes (23.11.2026).
STERNE = [(13, 1, 0), (19, 4, 9), (25, 2, 17), (31, 1, 5), (40, 14, 21), (47, 0, 13), (55, 13, 2),
          (61, 1, 26), (33, 13, 30), (52, 2, 19)]
STERN_AB = 0.5                                # Stern ist an, solange seine Helligkeit darüber liegt
STERN_RUNDEN = 5                              # so oft leuchtet jeder Stern je Durchlauf auf
SCHIMMER_STUFEN = 1                           # Schrift: zwei Goldtöne (heller Schimmer wandert)


def krippe(bild, f):
    puls = round((0.5 + 0.5 * math.sin(f / 10)) * 4) / 4
    for y in range(1, 10):                                        # Heiligenschein: goldene Scheibe
        for x in range(2, 14):
            d = math.hypot(x - KX, y - KY)
            if d < 2.3:
                bild.setze(x, y, GELB)
            elif d < 3.4:
                bild.setze(x, y, mischen(GOLD, GELB, puls))
            elif d < 4.4 and puls >= 0.5 and bild.hole(x, y) == HIMMEL:   # weicher Rand, atmet
                bild.setze(x, y, dimmen(GOLD, 0.2 + 0.2 * puls))
    # Stroh mit Halmen, Trog, gekreuzte Beine
    bild.rechteck(4, 8, 6, 1, STROH)
    bild.rechteck(4, 9, 16, 1, STROH)
    for x, y in ((3, 8), (4, 7), (19, 8), (20, 8), (20, 7)):
        bild.setze(x, y, STROH)
    bild.rechteck(3, 10, 18, 1, HOLZ)
    bild.rechteck(4, 11, 16, 1, HOLZ)
    bild.rechteck(5, 12, 14, 1, HOLZ_DUNKEL)
    for x0 in (7, 16):
        for k in (-1, 0, 1):
            bild.setze(x0 + k, 14 + k, HOLZ)
            bild.setze(x0 - k, 14 + k, HOLZ)
    # Kind: Kopf, gewickelt in ein weißes Tuch
    bild.rechteck(10, 6, 6, 1, TUCH)
    if (f // 24) % 2:                                             # atmet ruhig
        bild.rechteck(11, 5, 4, 1, TUCH)
    bild.rechteck(9, 7, 9, 1, TUCH)
    bild.rechteck(9, 8, 10, 1, TUCH_SCHATTEN)
    bild.rechteck(KX - 1, KY - 1, 3, 3, HAUT)


def kerze(bild, x, oben, f, saat):
    z = random.Random(saat + f // 3)
    bild.rechteck(x, oben, 2, 16 - oben, WACHS)
    seite = z.choice((0, 0, 1))
    for dx in (-1, 0, 1, 2):                                      # warmer Schein
        for dy in (-3, -2, -1):
            if bild.hole(x + dx, oben + dy) == HIMMEL:
                bild.setze(x + dx, oben + dy, (70, 30, 0))
    bild.setze(x, oben - 1, GELB)
    bild.setze(x + 1, oben - 1, GELB if seite else (255, 150, 0))
    bild.setze(x + seite, oben - 2, (255, 170, 0))
    if z.random() < 0.5:
        bild.setze(x + seite, oben - 3, (255, 110, 0))


def wort(bild, text, f, von, bis):
    """Buchstabe für Buchstabe einblenden, golden schimmern, am Ende gemeinsam ausblenden."""
    x = TEXT_X0 + (TEXT_X1 - TEXT_X0 - textbreite(text) + 1) // 2

    def farbe(i):
        ein = max(0.0, min(1.0, (f - von - i * 7) / 8))
        aus = max(0.0, min(1.0, (bis - f) / 10))
        schimmer = round((0.5 + 0.5 * math.sin(f / 7 - i * 0.9)) * SCHIMMER_STUFEN) / SCHIMMER_STUFEN
        return mischen(HIMMEL, mischen(GOLD, (255, 225, 120), schimmer), round(ein * aus * 8) / 8)

    bild.text(x, 4, text, farbe)


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
        bild = Bild(HIMMEL)
        for x, y, phase in STERNE:
            h = 0.5 + 0.5 * math.cos((f + phase * 4) / 255 * 2 * math.pi * STERN_RUNDEN)
            if h > STERN_AB:
                bild.setze(x, y, dimmen((255, 240, 200), round(h * 5) / 5))
        krippe(bild, f)
        kerze(bild, 0, 10, f, 1)                                  # gleich hoch: die zweite Kerze
        kerze(bild, 23, 10, f, 5)                                 # ist fast eine Kopie der ersten
        if 60 <= f < 146:
            wort(bild, "STILLE", f, 60, 146)
        elif f >= 150:
            wort(bild, "NACHT", f, 150, 255)
        liste.append(bild)
    return _jedes_bild_anders(liste)
