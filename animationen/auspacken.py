"""Geschenk auspacken: ein Paket fällt herein und zittert, die Schleife geht auf, der Deckel
springt weg (Konfetti), heraus steigt die Überraschung und hüpft groß daneben: Teddy (winkt),
Spielzeuglok (dampft) und Stern (funkelt); dreimal mit anderen Paketfarben – 255 Bilder.
"""
import math
import random

from basis import BUNT, GELB, GOLD, PINK, ROT, WEISS, Bild, Sterne, dimmen, mischen

NAME = "auspacken"
TITEL = "Geschenk auspacken mit Überraschung"

HINTERGRUND = (10, 0, 22)
STERNE = Sterne(anzahl=9, saat=303, y_max=7)
PX, PB = 12, 16                       # Paket: linke Kante, Breite
MX = PX + PB // 2                     # Mitte (Band liegt auf MX-1, MX)
ZIEL_X = 46                           # hier landet die Überraschung
RUNDEN = [  # Paket, Band, Inhalt
    (ROT, GOLD, "teddy"),
    ((0, 90, 255), PINK, "zug"),
    ((0, 180, 40), GELB, "stern"),
]
TEDDY = [".bb.....bb.",
         "bhhbbbbbhhb",
         "bbbbbbbbbbb",
         ".bbkbbbkbb.",
         ".bbbhhhbbb.",
         ".bbbhnhbbb.",
         "..brrrrrb..",
         "bbbbbrbbbbb",
         "bbbbhhhbbbb",
         ".bbbhhhbbb.",
         ".bbbhhhbbb.",
         ".bbb...bbb."]
TEDDY_FARBEN = {"b": (200, 105, 30), "h": (255, 190, 110), "k": (0, 0, 0), "n": (90, 30, 10),
                "r": (255, 0, 40)}
ZUG = ["..........kk...",
       "rrrrrr....kk...",
       "rwwwwr...gkkg..",
       "rwwwwr.gggggggg",
       "rrrrrrggggggggs",
       "rrrrrrgggggggg.",
       "yyyyyyyyyyyyyyy",
       ".KKK.KKK..KKK..",
       ".KoK.KoK..KoK..",
       ".KKK.KKK..KKK.."]
ZUG_FARBEN = {"k": (120, 120, 140), "r": (255, 0, 20), "w": (120, 220, 255), "g": (0, 190, 70),
              "s": (255, 255, 160), "y": GELB, "K": (110, 110, 130), "o": GOLD}
STERN = [".....y.....",
         ".....y.....",
         "....yyy....",
         "....yyy....",
         "yyyyywyyyyy",
         ".yyywwwyyy.",
         "..yyywyyy..",
         "..yyyyyyy..",
         ".yyyy.yyyy.",
         ".yyy...yyy.",
         "yy.......yy"]
INHALT = {"teddy": TEDDY, "zug": ZUG, "stern": STERN}
SCHLEIFE = [".xx..xx.", "xxxkkxxx", ".xx..xx."]
SCHLEIFE_LOCKER = ["........", "xx.kk.xx", "xxx..xxx"]

# Ablauf je Runde (85 Bilder)
T_ZITTERN, T_SCHLEIFE, T_DECKEL, T_STEIGT, T_HUEPFT, T_LANDET, T_ENDE = 8, 18, 26, 30, 44, 56, 78


def paket(bild, farbe, band, dy, deckel, schleife):
    """deckel = (dx, dy, kipp) oder None (weg); schleife 0 zu, 1 locker, 2 offen, 3 weg."""
    hell, dunkel = mischen(farbe, WEISS, 0.35), dimmen(farbe, 0.6)
    bild.rechteck(PX, 10 + dy, PB, 6, farbe)
    bild.rechteck(PX, 10 + dy, 1, 6, hell)
    bild.rechteck(PX + PB - 1, 10 + dy, 1, 6, dunkel)
    bild.rechteck(MX - 1, 10 + dy, 2, 6, band)
    if deckel is None:
        bild.rechteck(PX, 10 + dy, PB, 1, dunkel)                  # offener Rand
        return
    ddx, ddy, kipp = deckel
    for x in range(PX - 1, PX + PB + 1):                           # Deckel, steht 1 über
        y = round(8 + dy + ddy + (x - MX) * kipp)
        c = band if x in (MX - 1, MX) else None
        bild.setze(x + ddx, y, c or hell)
        bild.setze(x + ddx, y + 1, c or farbe)
    yd = 8 + dy + ddy
    if schleife == 0:
        bild.figur(MX - 4 + ddx, yd - 3, SCHLEIFE, {"x": band, "k": mischen(band, WEISS, 0.5)})
    elif schleife == 1:
        bild.figur(MX - 4 + ddx, yd - 3, SCHLEIFE_LOCKER, {"x": band, "k": mischen(band, WEISS, 0.5)})
    elif schleife == 2:                                            # Bänder hängen über die Kanten
        bild.linie(MX - 2, yd - 1, PX - 2, yd - 1, band)
        bild.linie(MX + 1, yd - 1, PX + PB + 1, yd - 1, band)
        bild.linie(PX - 2, yd, PX - 2, yd + 3, band)
        bild.linie(PX + PB + 1, yd, PX + PB + 1, yd + 3, band)


def inhalt(bild, art, cx, y_unten, f, lebendig):
    """Überraschung mit der Unterkante y_unten, mittig um cx; lebendig = bewegt sich."""
    zeilen = INHALT[art]
    x0 = round(cx - len(zeilen[0]) / 2)
    y0 = round(y_unten) - len(zeilen) + 1
    if art == "teddy":
        bild.figur(x0, y0, zeilen, TEDDY_FARBEN)
        if lebendig and (f // 5) % 2:                              # winkt mit dem rechten Arm
            bild.rechteck(x0 + 9, y0 + 7, 2, 2, HINTERGRUND)
            bild.rechteck(x0 + 10, y0 + 5, 2, 2, TEDDY_FARBEN["b"])
            bild.setze(x0 + 11, y0 + 4, TEDDY_FARBEN["b"])
    elif art == "zug":
        bild.figur(x0, y0, zeilen, ZUG_FARBEN)
        if lebendig:
            for rx in (2, 6, 11):                                  # Speichen drehen sich
                dx, dy = ((0, -1), (1, 0), (0, 1), (-1, 0))[(f // 2) % 4]
                bild.setze(x0 + rx + dx, y0 + 8 + dy, WEISS)
            for k in range(3):                                     # Dampfwölkchen
                a = (f + k * 5) % 15
                if y0 - 1 - a // 2 >= 0:
                    bild.rechteck(x0 + 10 - a // 3, y0 - 1 - a // 2, 2 if a < 9 else 1, 1,
                                  dimmen((230, 230, 255), 1 - a / 18))
    else:
        farben = {"y": (255, 235, 120) if (f // 4) % 3 == 0 else GELB, "w": WEISS}
        bild.figur(x0, y0, zeilen, farben)
        if lebendig:                                               # Strahlen blitzen
            for k, (dx, dy) in enumerate(((-3, 1), (13, 2), (-2, 9), (12, 8), (5, -2))):
                if (f // 3 + k * 2) % 5 < 2:
                    bild.setze(x0 + dx, y0 + dy, WEISS)


def bilder():
    z = random.Random(5)
    konfetti = []
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        STERNE.zeichnen(bild, f)
        runde, t = divmod(f, 85)
        farbe, band, art = RUNDEN[runde]
        hoehe = len(INHALT[art])
        # Paket fällt herein, zittert
        dy = -round(18 * (1 - (t / 6) ** 2)) if t < 6 else (-1 if t == 6 else 0)
        zittern = (1 if (t // 2) % 2 else -1) if T_ZITTERN <= t < T_SCHLEIFE and (t - T_ZITTERN) % 5 < 4 else 0
        # Überraschung: steigt aus dem Paket, hüpft nach rechts, zeigt sich
        if T_STEIGT <= t < T_HUEPFT:
            a = (t - T_STEIGT) / (T_HUEPFT - T_STEIGT)
            y_start, y_oben = 10 + hoehe, max(hoehe - 1, 9)
            inhalt(bild, art, MX, y_start + (y_oben - y_start) * a, f, False)
        # Paket (verdeckt den unteren Teil der Überraschung)
        if t < T_DECKEL:
            deckel = (0, 0, 0.0)
        elif t < T_DECKEL + 8:
            k = t - T_DECKEL
            deckel = (-round(k * 1.5), -round(k * 2.4 - k * k * 0.12), -k * 0.07)
        else:
            deckel = None
        schleife = 0 if t < T_SCHLEIFE else 1 if t < T_SCHLEIFE + 4 else 2 if t < T_DECKEL else 3
        p = Bild(None)
        paket(p, farbe, band, dy, deckel, schleife)
        for y in range(16):
            for x in range(-1, 40):
                c = p.hole(x, y)
                if c is not None:
                    bild.setze(x + zittern, y, c)
        if T_HUEPFT <= t < T_LANDET:                               # Sprung im Bogen
            a = (t - T_HUEPFT) / (T_LANDET - T_HUEPFT)
            y_oben = max(hoehe - 1, 9)
            y = y_oben + (15 - y_oben) * a - 5 * math.sin(math.pi * a)
            inhalt(bild, art, MX + (ZIEL_X - MX) * a, y, f, False)
        elif t >= T_LANDET:
            federn = {1: 1, 2: 2, 3: 1}.get(t - T_LANDET, 0)       # kleiner Hüpfer nach der Landung
            schweben = round(1.5 + 1.5 * math.sin(f / 5)) if art == "stern" else 0
            inhalt(bild, art, ZIEL_X, 15 - federn - schweben, f, True)
        # Konfetti: beim Deckel und bei der Landung
        if t == T_DECKEL + 1:
            for _ in range(22):
                konfetti.append([MX, 8, z.uniform(-1.6, 1.9), z.uniform(-1.5, -0.3),
                                 BUNT[z.randrange(len(BUNT))], 24])
        if t == T_LANDET:
            for _ in range(12):
                konfetti.append([ZIEL_X, 13, z.uniform(-1.8, 1.8), z.uniform(-1.4, -0.4),
                                 BUNT[z.randrange(len(BUNT))], 16])
        for k in konfetti:
            bild.setze(k[0], k[1], k[4])
            k[0] += k[2]
            k[1] += k[3]
            k[3] += 0.1
            k[5] -= 1
        konfetti = [k for k in konfetti if k[5] > 0 and k[1] < 16]
        if t >= T_ENDE:                                            # sanft ausblenden
            for y in range(16):
                for x in range(64):
                    bild.px[y][x] = dimmen(bild.px[y][x], max(0.0, 1 - (t - T_ENDE + 1) / 7))
        liste.append(bild)
    return liste
