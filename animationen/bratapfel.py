"""Bratapfel und Kakao: im Ofen (Glut flackert hinter der Scheibe) bläht sich ein roter Apfel, die
Schale platzt, Füllung blubbert, Duft steigt auf; daneben wird ein Becher Kakao eingeschenkt,
bekommt eine Sahnehaube, bunte Streusel rieseln, Marshmallows hüpfen hinein – 255 Bilder.

Sparsam gezeichnet (23.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Glut als Band mit zwei hellen Nestern, Rost quer durch
den Ofen, Griff so breit wie das Fenster, Knöpfe und Lampe in denselben Spalten, Becher mit
Streifen statt Punkten.
"""
import math
import random

from basis import B, BUNT, GELB, ROT, WEISS, Bild, dimmen, mischen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "bratapfel"
TITEL = "Bratapfel im Ofen und Kakao mit Sahne"

WAND = (0, 0, 0)
TISCH = (49, 28, 12)
OFEN = (62, 64, 80)
INNEN = (32, 9, 0)                             # Ofenraum: ganz schwacher warmer Schein
INNEN_HELL = (42, 12, 0)
OFEN_HELL = (175, 178, 195)
GLUT = (255, 95, 0)
ROST = (120, 120, 135)                         # Gitterrost quer durch den Ofen
APFEL = (255, 0, 10)
APFEL_GAR = (200, 20, 0)
FUELLUNG = (255, 200, 90)
BLATT = (40, 200, 40)
KAKAO = (41, 21, 8)
TASSE = (0, 120, 235)
TASSE_HELL = (120, 200, 255)
SAHNE = (255, 250, 235)
MALLOWS = [(255, 150, 195), (255, 235, 130), (160, 255, 200)]

AX, AY = 13, 8                                 # Apfel im Ofenfenster
TX = 40                                        # linke Kante des Bechers
EINSCHENKEN, SAHNE_AB, STREUSEL_AB, MALLOW_AB = 46, 52, 104, 150
STREUSEL = [(3, 4, 0), (6, 3, 2), (5, 5, 4), (4, 2, 6), (7, 5, 3), (2, 5, 8), (5, 1, 1)]   # dx, y, Farbe


_z = random.Random(971)
NESTER = [(3 + 2 * _z.randrange(10), 3 + 2 * _z.randrange(10)) for _ in range(128)]   # je zwei Bilder


def ofen(bild, f):
    bild.rechteck(1, 2, 30, 13, OFEN)
    bild.rechteck(3, 4, 21, 10, INNEN_HELL if (f // 9) % 2 else INNEN)   # Fenster, der Schein atmet
    # Glut am Boden: durchgehendes Band, das pulsiert, dazu zwei helle Nester, die springen
    # (jede Spalte einzeln flackern zu lassen kostet beim Komprimieren zu viel)
    grund = (0.5, 0.62, 0.74, 0.62)[(f // 3) % 4]
    bild.rechteck(3, 13, 21, 1, dimmen(GLUT, grund))
    for x in NESTER[f // 2]:
        bild.rechteck(x, 13, 2, 1, GLUT)
    bild.rechteck(3, 3, 21, 1, OFEN_HELL)                            # Griff über dem Fenster
    for ky in (5, 9):                                                # Drehknöpfe
        bild.rechteck(26, ky, 3, 2, OFEN_HELL)
    bild.rechteck(26, 12, 3, 1, dimmen(ROT, 0.55 + 0.45 * ((f // 8) % 2)))   # Heizlampe


APFEL_FORM = [
    ["aa.aa", "gaaaa", "aaaaa", "aaaaa", ".aaa."],
    [".aa.aa.", "agaaaaa", "agaaaaa", "aaaaaaa", "aaaaaaa", ".aaaaa."],
    ["..aa.aa..", ".agaaaaa.", "aggaaaaaa", "aaaaaaaaa", "aaaaaaaaa", ".aaaaaaa.", "..aaaaa.."],
]


def apfel(bild, f):
    """Apfel wird größer (drei Stufen), dann dunkler; Risse, Füllung quillt und blubbert."""
    gar = min(1.0, max(0.0, (f - 95) / 100))
    farbe = mischen(APFEL, APFEL_GAR, round(gar * 4) / 4)
    form = APFEL_FORM[0 if f < 30 else 1 if f < 70 else 2]
    if 30 <= f < 34 or 70 <= f < 74:                                 # kurzer Ruck beim Aufblähen
        form = APFEL_FORM[2 if f >= 70 else 1] if f % 2 else APFEL_FORM[1 if f >= 70 else 0]
    breite, hoehe = len(form[0]), len(form)
    oben = 12 - hoehe
    bild.rechteck(3, 12, 21, 1, ROST)                                # Rost unter dem Apfel, über der Glut
    bild.figur(AX - breite // 2, oben, form, {"a": farbe, "g": mischen(farbe, WEISS, 0.5)})
    bild.setze(AX, oben, (150, 90, 30))                              # Stiel in der Mulde
    bild.setze(AX, oben - 1, (150, 90, 30))
    if f < 150:
        bild.setze(AX + 1, oben - 1, BLATT)
        bild.setze(AX + 2, oben - 1, BLATT)
    if f > 110:                                                      # Schale platzt: goldene Risse
        bild.setze(AX + 1, 8, FUELLUNG)
        bild.setze(AX + 2, 9, FUELLUNG)
        if f > 130:
            bild.setze(AX - 1, 10, FUELLUNG)
            bild.setze(AX + 3, 8, dimmen(FUELLUNG, 0.75))
    if f > 150:                                                      # Füllung quillt oben heraus und blubbert
        bild.rechteck(AX - 1, oben, 3, 1, FUELLUNG)
        bild.setze(AX, oben - 1, FUELLUNG)
        blase = (f // 4) % 4
        if blase < 3:
            bild.setze(AX - 1 + blase, oben - 1, mischen(FUELLUNG, WEISS, 0.5))
        if f > 175:                                                  # Saft läuft herunter
            for k in range(min(3, (f - 175) // 10) + 1):
                bild.setze(AX - 3, oben + 2 + k, FUELLUNG)
    for k in range(3):                                               # Duft steigt aus dem Ofen
        t = (f + k * 11) % 33
        if f > 60:
            bild.setze(8 + k * 6 + round(math.sin((t + k * 5) / 4)), 1 - t // 17,
                       dimmen((255, 220, 170), 0.5 - 0.15 * (t // 11)))


def becher(bild, f):
    bild.rechteck(TX, 7, 11, 8, TASSE)
    bild.rechteck(TX + 1, 14, 9, 1, dimmen(TASSE, 0.6))               # Boden abgerundet
    bild.setze(TX, 14, WAND)
    bild.setze(TX + 10, 14, WAND)
    for y in range(9, 13):                                           # Henkel
        bild.setze(TX + 13, y, TASSE)
    bild.rechteck(TX + 11, 8, 2, 1, TASSE)
    bild.rechteck(TX + 11, 13, 2, 1, TASSE)
    bild.rechteck(TX, 10, 11, 1, TASSE_HELL)                         # heller Streifen (statt Punkten)
    bild.rechteck(TX, 7, 11, 1, TASSE_HELL)                          # Rand
    if f < EINSCHENKEN:                                              # Kakao wird eingeschenkt
        breit = 2 if f < EINSCHENKEN - 8 else 1
        bild.rechteck(TX + 5, 0, breit, 7, KAKAO)
        for y in range(0, 7):
            if (y - f) % 4 == 0:
                bild.setze(TX + 5, y, mischen(KAKAO, WEISS, 0.35))    # Strahl fließt
        if f > 6 and f % 5 < 2:
            bild.setze(TX + 4 + (f * 3) % 4, 6, KAKAO)                # Spritzer
    if f > 20:
        bild.rechteck(TX + 1, 7, 9, 1, KAKAO)
    if f >= SAHNE_AB:                                                # Sahnehaube wächst Stufe um Stufe
        stufen = min(5, (f - SAHNE_AB) // 9 + 1)
        for k in range(stufen):
            halb = 4 - k
            y = 7 - k
            bild.rechteck(TX + 5 - halb, y, 2 * halb + 1, 1, SAHNE)
        if stufen == 5:
            bild.setze(TX + 4, 3, SAHNE)                              # Zipfel neigt sich
    for i, (dx, y, farbe) in enumerate(STREUSEL):                    # Streusel rieseln von oben
        start = STREUSEL_AB + i * 6
        if f >= start:
            fall = min(y, -1 + (f - start))
            bild.setze(TX + dx, fall, BUNT[farbe])
    # Marshmallows liegen rechts auf dem Tisch und hüpfen einer nach dem anderen auf die Sahne
    ziele = [(TX + 1, 5), (TX + 8, 5), (TX + 5, 1)]
    for i, farbe in enumerate(MALLOWS):
        lx, ly = (58, 11) if i == 0 else (58, 13) if i == 1 else (55, 13)   # Stapel auf dem Tisch
        start = MALLOW_AB + i * 30
        t = f - start
        if t < 0:
            wackeln = -1 if 0 > t > -6 and t % 2 else 0               # nimmt Anlauf
            bild.rechteck(lx, ly + wackeln, 2, 2, farbe)
        elif t < 16:
            a = t / 16
            zx, zy = ziele[i]
            x = lx + (zx - lx) * a
            y = ly + (zy - ly) * a - 26 * a * (1 - a)
            bild.rechteck(round(x), round(max(-1, y)), 2, 2, farbe)
        else:
            zx, zy = ziele[i]
            bild.rechteck(zx, zy + (1 if t < 18 else 0), 2, 2, farbe)
            if t < 20:                                               # Sahne spritzt
                bild.setze(zx - 1, zy - 1 + t - 16, SAHNE)
                bild.setze(zx + 2, zy - 1 + t - 16, SAHNE)
    if f > EINSCHENKEN:                                              # Dampf über dem Kakao
        for k in range(2):
            t = (f + k * 13) % 26
            bild.setze(TX - 1 + k * 12 + round(math.sin(t / 3)), 5 - t // 5,
                       dimmen(WEISS, 0.4 - 0.1 * (t // 9)))
    if f > 236 and (f // 3) % 2:                                     # fertig: Glitzern
        bild.setze(TX + 5, 0, GELB)
        bild.setze(TX - 2, 3, GELB)
        bild.setze(TX + 12, 4, GELB)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(WAND)
        ofen(bild, f)
        apfel(bild, f)
        becher(bild, f)
        bild.rechteck(0, 15, B, 1, TISCH)
        liste.append(bild)
    return liste
