"""Eichhörnchen sucht seine Nüsse: verschneiter Waldboden in der Dämmerung, rechts am Rand ein
Baumstamm mit verschneitem Aststumpf. Ein rotbraunes Eichhörnchen hüpft von links herein,
schnuppert, buddelt (Schnee spritzt), findet nichts, dreht sich ratlos um und kratzt sich am Ohr.
An der zweiten Stelle findet es die Nuss, setzt sich auf die Hinterbeine und knabbert, bis sie
aufgegessen ist (Schalenstückchen fallen); dann hüpft es zum Stamm und daran hinauf aus dem Bild.
Ein Windstoß weht Löcher, Aushub und Schalen zu – Anfang und Ende zeigen denselben glatten Schnee,
255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Himmel in waagerechten Streifen (gleiche Spalten), ein
durchgehender Waldsaum, ferne Stämme als schwarze Balken, glatter Schnee in zwei Farben, kein
Schneefall. Das Fell ist mit Absicht kräftig rotbraun: auf den LEDs leuchtet es orange – ein
Eichhörnchen ist so. Stamm und Borke dagegen sehr dunkel, damit sie Holz bleiben.
"""
import math

from basis import B, SCHWARZ, Bild

NAME = "eichhoernchen"
TITEL = "Eichhörnchen sucht seine Nüsse"

# Dämmerung: je Zeile eine Farbe, in deutlichen Stufen (kühl, damit das Fell leuchtet)
HIMMEL = [(10, 18, 62)] * 4 + [(18, 32, 92)] * 3 + [(52, 44, 112)] * 2
SAUM = (0, 46, 30)                             # ferner Waldsaum, Zeilen 9 bis 11
FERN = (4, 6, 16)                              # ferne Stämme als Schattenriss
KANTE = (215, 225, 250)                        # Oberkante der Schneedecke
BODEN = (78, 90, 140)                          # darunter gedämpft (große Fläche)
LOCH = (20, 26, 60)                            # gebuddeltes Loch
STAUB = (235, 240, 255)                        # spritzender Schnee
STAMM = (66, 30, 4)
BORKE = (33, 11, 0)
FELL = (215, 65, 0)                            # kräftiges Rotbraun (gewollt orange auf den LEDs)
DUNKEL = (125, 34, 0)                          # Pinselohren, Pfoten
BAUCH = (255, 235, 210)
NUSS = (230, 185, 85)
SCHALE = (150, 105, 35)

SCHNEE_Y = 12                                  # Oberkante des Schnees; die Füße stehen eine Zeile darüber
STAMM_X = 57                                   # Stamm bis zum rechten Rand
AST_X, AST_Y = 51, 2                           # Aststumpf links am Stamm
FERNE_STAEMME = [(5, 2), (24, 1), (43, 2)]     # x, Breite

# Eichhörnchen (Blick nach rechts): t Schwanz, f Fell, e Pinselohr, a Auge, k Nase, w Bauch, p Pfote, n Nuss
HOCKT = [".ttt........",
         "ttttt.......",
         "tttt.....e..",
         ".ttt....fff.",
         ".ttt..fffafk",
         "..ttffffff..",
         "...ffffwwf..",
         "...ff...ff.."]
SPRUNG = [".ttt.......e..",
          "ttttt.....fff.",
          ".ttttttffffafk",
          "...ttfffffwf..",
          "....ff....ff..",
          "...f........f."]
SCHNUPPERT = [[".ttt.........",
               "ttttt........",
               "tttt.........",
               ".ttt.........",
               ".ttt..fff.e..",
               "..ttffffffff.",
               "...fffffffaf.",
               "...ff...f.ffk"],
              ["ttt..........",
               "tttt.........",
               "tttt.........",
               ".ttt.........",
               ".ttt..fff.e..",
               "..ttffffffff.",
               "...fffffffafk",
               "...ff...f.ff."]]
# beim Buddeln steckt der Kopf im Loch (unterste Zeile liegt in der Schneedecke)
BUDDELT = [["..ttt........",
            ".ttttt.......",
            ".tttt........",
            "..ttt........",
            "..tt.fff.....",
            "...tffffff...",
            "...fffffffe..",
            "...ff..pffff.",
            "..........ff."],
           [".ttt.........",
            "ttttt........",
            "tttt.........",
            ".ttt.........",
            "..tt.fff.....",
            "...tffffff...",
            "...fffffffe..",
            "...ff...pfff.",
            "..........ff."]]
# sitzend: links der Schwanz (5 Spalten), rechts Kopf und Leib (6 Spalten) – getrennt austauschbar
SCHWANZ = [".ttt.", "ttttt", "tttt.", "ttt..", "ttt..", ".tt..", ".ttt.", "..ttf", "...ff"]
SCHWANZ_ZUCKT = ["ttt..", "tttt.", "tttt."]
LEIB = ["..e.e.", "..fff.", "..fafk", ".fff..", "ffwp..", "ffww..", "fffw..", "ffff..", "ffff.."]
KOPF_LINKS = [".e.e..", ".fff..", "kfaf.."]
KOPF_KRATZT = ["..e.ep", "..fffp", "..fafk"]
# Nuss vor dem Mund (2 = ganz, 1 = halb, 0 = aufgegessen), abwechselnd am Mund und in den Pfoten
KNABBERT = {2: [["..fann", ".fffnn", "ffwp.."], ["..fafk", ".fffnn", "ffwpnn"]],
            1: [["..fan.", ".fffn.", "ffwp.."], ["..fafk", ".fffn.", "ffwpn."]],
            0: [["..fafk", ".fffp.", "ffw..."], ["..fafk", ".fff..", "ffwp.."]]}
# am Stamm (Kopf oben, Pfoten rechts am Holz): gestreckt und zusammengezogen
KLETTERT_LANG = ["..k...",
                 ".ff..p",
                 "efaff.",
                 ".ffwf.",
                 "..fw..",
                 "..ff..",
                 "..ff..",
                 "..fff.",
                 ".tfffp",
                 "tttf..",
                 "ttt...",
                 "ttt...",
                 ".tt..."]
KLETTERT_KURZ = ["..k...",
                 ".ff..p",
                 "efaff.",
                 ".ffwf.",
                 ".fffw.",
                 ".ffffp",
                 ".tff..",
                 "ttt...",
                 "ttt...",
                 "ttt...",
                 ".tt..."]
FARBEN = {"t": FELL, "f": FELL, "e": DUNKEL, "a": SCHWARZ, "k": DUNKEL, "w": BAUCH, "p": DUNKEL,
          "n": NUSS}

# Drehbuch
X1, X2, X3 = 8, 30, 42                         # linke Kante der Figur an Stelle 1, Stelle 2, vor dem Stamm
REIN, SCHN1, BUD1, LEER, RATLOS = 4, 28, 42, 68, 76
WEITER, SCHN2, BUD2, FUND, KNABBERN = 100, 124, 133, 155, 162
WEG, ANSPRUNG, AM_STAMM, KLETTERN, WIND = 202, 218, 222, 226, 238
SATZ = 8                                       # Bilder je Hüpfer
WIND_TEMPO = 4.7
SCHALEN = [(14, 10), (16, 11), (13, 10), (17, 11)]     # wo die Schalenstückchen landen: dx, Zeile
LOCH_DX = 10                                   # das Loch liegt so weit rechts von der linken Kante der Figur


def huepfen(t, x_von, x_bis, saetze):
    """t = Bilder seit Beginn → (x, Höhe, Figur): kurz ducken, dann ein flacher Satz."""
    k = min(saetze - 1, t // SATZ)
    u = (t - k * SATZ) / SATZ
    weite = (x_bis - x_von) / saetze
    if u < 0.3:
        return round(x_von + k * weite), 0, HOCKT
    v = (u - 0.3) / 0.7
    return round(x_von + (k + v) * weite), round(3 * math.sin(math.pi * v)), SPRUNG


def sitzend(kopf=None, mitte=None, zuckt=False):
    schwanz, leib = list(SCHWANZ), list(LEIB)
    if zuckt:
        schwanz[0:3] = SCHWANZ_ZUCKT
    if kopf:
        leib[0:3] = kopf
    if mitte:
        leib[2:5] = mitte
    return [s + l for s, l in zip(schwanz, leib)]


def stellen(bild, x, figur, hoch=0, spiegeln=False):
    """Figur mit den Füßen auf den Schnee stellen (hoch = Höhe im Sprung)."""
    tief = 1 if figur in BUDDELT else 0                              # Buddeln: Kopf im Loch
    bild.figur(x, SCHNEE_Y - len(figur) + tief - hoch, figur, FARBEN, spiegeln)


def loch(bild, hx, tiefe):
    """Loch im Schnee (tiefe 0–3) mit dem Aushub daneben."""
    if tiefe >= 1:
        bild.rechteck(hx, SCHNEE_Y, 2 if tiefe == 1 else 3, 1, LOCH)
    if tiefe >= 2:
        bild.setze(hx + 3, SCHNEE_Y - 1, KANTE)
    if tiefe >= 3:
        bild.rechteck(hx, SCHNEE_Y + 1, 3, 1, LOCH)
        bild.rechteck(hx + 3, SCHNEE_Y - 1, 3, 1, KANTE)


def spritzen(bild, t, hx):
    """Schnee spritzt aus dem Loch: alle zwei Bilder ein Bröckchen im Bogen, abwechselnd vor und zurück."""
    for k, (vx, vy) in enumerate([(1.3, -2.0), (-1.1, -2.5), (2.0, -1.4), (-1.9, -1.9), (0.6, -2.8),
                                  (-0.5, -2.2)]):
        u = (t - k * 2) % 12
        if u < 7 and t >= k * 2:
            x = hx + 1 + vx * u
            y = SCHNEE_Y - 1 + vy * u + 0.35 * u * u
            if y < SCHNEE_Y and bild.hole(x, y) not in (FELL, DUNKEL, BAUCH, SCHWARZ):
                bild.setze(x, y, STAUB)


def loch_tiefe(f, beginn):
    t = f - beginn
    return 0 if t < 3 else 1 if t < 9 else 2 if t < 16 else 3


def landschaft():
    bild = Bild()
    for y, farbe in enumerate(HIMMEL):
        bild.rechteck(0, y, B, 1, farbe)
    bild.rechteck(0, 9, B, 3, SAUM)
    for x, breite in FERNE_STAEMME:
        bild.rechteck(x, 0, breite, SCHNEE_Y, FERN)
    bild.rechteck(0, SCHNEE_Y, B, 1, KANTE)
    bild.rechteck(0, SCHNEE_Y + 1, B, 3, BODEN)
    bild.rechteck(STAMM_X, 0, B - STAMM_X, SCHNEE_Y, STAMM)
    bild.rechteck(STAMM_X + 2, 0, 1, SCHNEE_Y, BORKE)
    bild.rechteck(STAMM_X + 5, 0, 1, SCHNEE_Y, BORKE)
    bild.rechteck(AST_X, AST_Y, STAMM_X - AST_X, 1, STAMM)           # Aststumpf mit Schneehaube
    bild.rechteck(AST_X, AST_Y - 1, STAMM_X - AST_X, 1, KANTE)
    bild.setze(STAMM_X - 1, SCHNEE_Y - 1, STAMM)                     # Wurzelanlauf, davor etwas Schnee
    bild.setze(STAMM_X - 2, SCHNEE_Y - 1, KANTE)
    return bild


def eichhoernchen(bild, f):
    if f < REIN:
        return
    if f < SCHN1:                                                    # hüpft herein
        x, hoch, figur = huepfen(f - REIN, X1 - 24, X1 - 3, 3)
        stellen(bild, x, figur, hoch)
    elif f < BUD1:                                                   # schnuppert sich voran
        t = f - SCHN1
        stellen(bild, X1 - 3 + min(3, t // 4), SCHNUPPERT[(t // 2) % 2])
    elif f < LEER:                                                   # buddelt
        stellen(bild, X1, BUDDELT[(f // 2) % 2])
    elif f < RATLOS:                                                 # nichts drin
        stellen(bild, X1, HOCKT if f < LEER + 3 else SCHNUPPERT[(f // 2) % 2])
    elif f < WEITER:                                                 # setzt sich auf und schaut sich um
        t = f - RATLOS
        if 9 <= t < 16:                                              # dreht sich ganz um, schaut über die Schulter
            stellen(bild, X1 + 3, sitzend(KOPF_LINKS if t >= 13 else None), spiegeln=True)
        else:                                                        # Kopf nach links, kratzt sich am Ohr
            kopf = KOPF_LINKS if 3 <= t < 7 else KOPF_KRATZT if t >= 18 and (t // 2) % 2 else None
            stellen(bild, X1, sitzend(kopf, zuckt=t >= 20))
    elif f < SCHN2:                                                  # zur zweiten Stelle
        x, hoch, figur = huepfen(f - WEITER, X1, X2 - 2, 3)
        stellen(bild, x, figur, hoch)
    elif f < BUD2:
        t = f - SCHN2
        stellen(bild, X2 - 2 + min(2, t // 4), SCHNUPPERT[(t // 2) % 2])
    elif f < FUND:
        stellen(bild, X2, BUDDELT[(f // 2) % 2])
    elif f < KNABBERN:                                               # die Nuss!
        stellen(bild, X2, HOCKT if f < FUND + 4 else SCHNUPPERT[0])
    elif f < WEG:                                                    # knabbert, die Nuss wird kleiner
        t = f - KNABBERN
        gross = 2 if t < 20 else 1 if t < 32 else 0
        stellen(bild, X2, sitzend(mitte=KNABBERT[gross][(t // 3) % 2], zuckt=t % 10 >= 8))
    elif f < ANSPRUNG:                                               # zum Stamm
        x, hoch, figur = huepfen(f - WEG, X2, X3, 2)
        stellen(bild, x, figur, hoch)
    elif f < AM_STAMM:                                               # Satz an den Stamm
        t = f - ANSPRUNG
        stellen(bild, X3 + t // 2, HOCKT if t == 0 else SPRUNG, (0, 1, 3, 4)[t])
    elif f < KLETTERN:                                               # hängt am Stamm
        bild.figur(STAMM_X - 6, 1, KLETTERT_KURZ, FARBEN)
    else:                                                            # den Stamm hinauf
        t = f - KLETTERN
        oben = -2 - 3 * (t // 4)
        bild.figur(STAMM_X - 6, oben, KLETTERT_LANG if t % 4 < 2 else KLETTERT_KURZ, FARBEN)


def bilder():
    grund = landschaft()
    liste = []
    for f in range(255):
        bild = Bild()
        bild.px = [zeile[:] for zeile in grund.px]
        wind_x = int(-6 + (f - WIND) * WIND_TEMPO)                   # Windstoß weht die Löcher zu
        for beginn, x0 in ((BUD1, X1), (BUD2, X2)):
            hx = x0 + LOCH_DX
            t = loch_tiefe(f, beginn)
            if f >= WIND:
                t = 0 if wind_x - 8 > hx else min(t, 1) if wind_x > hx else t
            loch(bild, hx, t)
        if FUND <= f < FUND + 6:                                     # die Nuss liegt im Loch
            bild.rechteck(X2 + LOCH_DX, SCHNEE_Y, 2, 1, NUSS)
        eichhoernchen(bild, f)
        if BUD1 <= f < LEER:
            spritzen(bild, f - BUD1, X1 + LOCH_DX)
        if BUD2 <= f < FUND:
            spritzen(bild, f - BUD2, X2 + LOCH_DX)
        if KNABBERN <= f:                                            # Schalenstückchen fallen und bleiben liegen
            for k, (dx, y) in enumerate(SCHALEN):
                t = f - KNABBERN - 5 - k * 8
                if 0 <= t < y - 6:
                    bild.setze(X2 + 11 + (dx - 11) * t / (y - 6), 6 + t, SCHALE)
                elif t >= y - 6 and not (f >= WIND and wind_x > X2 + LOCH_DX):
                    bild.setze(X2 + dx, y, SCHALE)
        if WIND <= f:                                                # Schneefahne über dem Boden
            for k in range(5):
                for x in (wind_x - k * 3, wind_x - k * 3 - 1)[:2 - k % 2]:      # unten Striche, oben Punkte
                    if x < STAMM_X - 2:
                        bild.setze(x, SCHNEE_Y - 1 - k % 2, STAUB)
        liste.append(bild)
    return liste
