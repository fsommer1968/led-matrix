"""Weihnachtsmarkt: zwei Buden mit Lichterketten, dazwischen ein Karussell mit Pferdchen, ein
Glühweinkessel dampft, Leute schlendern vorbei, Schnee fällt – 255 Bilder.
Alles läuft in ganzen Perioden, das Ende geht nahtlos in den Anfang über.

Die Matrix speichert nur 80 KB je Animation, jedes Bild einzeln komprimiert (spaltenweise, a2pl):
Gleiche Spalten (auch im festen Zweierraster) kosten fast nichts, jede neue Spaltenform kostet
10–20 Bytes. Darum ist alles aus wenigen Spaltenformen gebaut: Markise, Lichterkette und
Karusselldach wechseln spaltenweise (Raster 2), die rechte Bude ist eine genaue Kopie der linken,
und alles Blinken wechselt für die ganze Kette zugleich (23.11.2026).
"""
import colorsys
import math

from basis import (B, GELB, GOLD, HAUT, HELLBLAU, NACHTBLAU, PINK, ROT, SCHNEEDECKE, TUERKIS, WEISS,
                   Bild, dimmen)

NAME = "weihnachtsmarkt"
TITEL = "Weihnachtsmarkt mit Karussell"

N = 255
HOLZ = (120, 65, 20)
HOLZ_HELL = (180, 105, 40)
SCHNEE_DACH = SCHNEEDECKE
CREME = (255, 215, 150)
LICHT = (150, 85, 20)                         # Fenster der Buden, warm erleuchtet
FLOCKE = (150, 165, 215)
KETTE = [GELB, ROT, HELLBLAU, PINK, TUERKIS]
PFERD = ["..c", "ccc", "c.c"]                 # schaut nach rechts, die Stange steckt in der Mitte
PFERDE_FARBE = [WEISS, HELLBLAU, GELB, PINK]
BUDEN_X = (0, 50)                             # gerader Abstand: die zweite Bude ist eine Kopie
BUDE_B = 13
KESSEL_X = 16
DAMPF = 2
KARUSSELL_X = 32
# Leute: (Start-x, Richtung, Mütze, Mantel)
LEUTE = [(22, 1, GELB, PINK), (58, 1, ROT, (0, 110, 255)), (44, -1, WEISS, (170, 0, 255))]
# Flocken: (x, Runden je Durchlauf, Startzeile 0…20)
FLOCKEN = [(14, 3, 2.0), (44, 4, 15.5), (47, 5, 7.0)]


def bude(bild, x0, f):
    """Bude: Schnee und Lichterkette am Dach, gestreifte Markise, helles Fenster, Verkäufer."""
    lampe = KETTE[(f // 17) % len(KETTE)]                          # die Kette wechselt die Farbe
    for k in range(BUDE_B):
        x = x0 + k
        innen = 0 < k < BUDE_B - 1
        bild.setze(x, 5, lampe if k % 2 == 0 else SCHNEE_DACH)
        bild.rechteck(x, 6, 1, 2, ROT if k % 2 == 0 else CREME)
        if innen:
            bild.setze(x, 4, SCHNEE_DACH)
            bild.rechteck(x, 8, 1, 4, LICHT)
            bild.setze(x, 12, HOLZ_HELL)                           # Theke
            bild.rechteck(x, 13, 1, 2, HOLZ)
    for x in (x0 + 6, x0 + 7):                                     # Verkäufer
        bild.setze(x, 8, ROT)
        bild.setze(x, 9, HAUT)
        bild.rechteck(x, 10, 1, 2, (0, 150, 60))


def kessel(bild, x, f):
    """Glühweinkessel über dem Feuer, Dampf steigt in Schwaden auf."""
    flamme = (255, 120, 0) if int(f * 84 / N) % 2 else GELB        # flackert, 42 Wechsel je Durchlauf
    for k in range(4):
        bild.setze(x + k, 10, (230, 0, 50))                        # Glühwein
        bild.setze(x + k, 11, (190, 95, 25))
        bild.rechteck(x + k, 12, 1, 2, (150, 70, 15))
        bild.setze(x + k, 14, flamme)
    for k in range(DAMPF):                                         # Schwaden, 51 Bilder je Aufstieg,
        t = ((f + k * 51 // DAMPF) % 51) / 51                      # alle über der rechten Kante
        y = 9 - round(t * 9)                                       # (dort kostet ein Punkt am wenigsten)
        hell = round((0.75 - 0.6 * t) * 6) / 6
        bild.setze(x + 3, y, dimmen((220, 225, 255), hell))


def karussell(bild, cx, f):
    w0 = 2 * math.pi * 3 * f / N                                   # drei Umdrehungen
    takt = int(f * 50 / N) % 2                                     # Lauflicht: 25 Wechsel je Durchlauf
    for dx in range(-9, 10):                                       # Dach: gestreiftes Zelt, Lichter
        x = cx + dx
        farbe = ROT if dx % 2 == 0 else CREME
        bild.rechteck(x, 2, 1, 2, farbe)
        if (dx + takt) % 2 == 0:
            bild.setze(x, 4, GELB)
    bild.rechteck(cx - 9, 14, 19, 1, (150, 30, 20))                # Boden, so breit wie das Dach
    bild.rechteck(cx, 5, 1, 9, GOLD)                               # Mittelsäule
    for i in range(4):                                             # nur die vorderen Pferde
        s, c = math.sin(w0 + i * math.pi / 2), math.cos(w0 + i * math.pi / 2)
        if c <= 0:
            continue
        x = cx + round(7.4 * s)
        y = 10 + round(math.sin(2 * math.pi * 6 * f / N + i * math.pi / 2))
        bild.rechteck(x, 5, 1, y - 5, dimmen(GOLD, 0.45))
        bild.figur(x - 1, y, PFERD, {"c": PFERDE_FARBE[i]})


def mensch(bild, x, f, muetze, mantel):
    auf = int(f * 42 / N) % 2                                      # Schritt: ganze Figur wippt
    for xx in (x, x + 1):
        bild.setze(xx, 9 - auf, muetze)
        bild.setze(xx, 10 - auf, HAUT)
        bild.rechteck(xx, 11 - auf, 1, 3, mantel)
        bild.rechteck(xx, 14 - auf, 1, 1 + auf, (150, 150, 170))


def schnee(bild, f):
    for i, (x, runden, start) in enumerate(FLOCKEN):
        y = (start + f * runden * 20 / N) % 20 - 2
        dx = round(math.sin(2 * math.pi * (f * 5 / N + i * 0.37)))
        if bild.hole(x + dx, y) == NACHTBLAU:
            bild.setze(x + dx, y, FLOCKE)


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
    for f in range(N):
        bild = Bild(NACHTBLAU)
        for x0 in BUDEN_X:
            bude(bild, x0, f)
        karussell(bild, KARUSSELL_X, f)
        kessel(bild, KESSEL_X, f)
        bild.rechteck(0, 15, B, 1, SCHNEE_DACH)
        for x0, richtung, muetze, mantel in LEUTE:                 # schlendern, eine Runde in 255 Bildern
            x = int((x0 + richtung * f * 72 / N) % 72) - 4
            mensch(bild, x, f, muetze, mantel)
        schnee(bild, f)
        liste.append(bild)
    return _jedes_bild_anders(liste)
