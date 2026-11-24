"""Schlittenflug: Weihnachtsmann mit Rentieren über dem nächtlichen Dorf – 255 Bilder.

Sternenhimmel mit Mond, Dorf mit erleuchteten Fenstern und Rauch aus den Kaminen.
Der Schlitten fliegt zweimal durch (hin und zurück) und wirft Geschenke in die Kamine: sie
fallen senkrecht hinein, es funkt, und die Fenster des Hauses leuchten bunt.
Rudolphs Nase blinkt, hinter dem Schlitten Sternenstaub, dazwischen Sternschnuppen.
"""
import math

from basis import (B, GELB, GRAU, HAUT, HELLBLAU, HELLGRUEN, LILA, NACHTBLAU, PINK, ROT, SCHNEEDECKE,
                   TUERKIS, WEISS, Bild, dimmen, sternschnuppe)

NAME = "schlittenflug"
TITEL = "Schlittenflug über dem nächtlichen Dorf"

FELL = (185, 100, 35)
GEWEIH = (215, 170, 100)
KUFE = (255, 190, 0)
SACK = (150, 95, 30)

RENTIER = [  # schaut nach rechts; Galopp: gestreckt / angezogen; n = Nase
    [".....g.g.", "......ffn", "wffffff..", ".ffffff..", ".f....f..", "f......f."],
    [".....g.g.", "......ffn", "wffffff..", ".ffffff..", "..f..f...", "...ff...."],
]
SCHLITTEN = [  # schaut nach rechts: hinten der Sack, vorn der Weihnachtsmann
    "......rw..",
    ".ss...hh..",
    "ssss.wrrr.",
    "rrrrrrrrrk",
    ".rrrrrrr.k",
    "kkkkkkkkk.",
]
FARBEN = {"g": GEWEIH, "f": FELL, "r": ROT, "w": WEISS, "h": HAUT, "s": SACK, "k": KUFE, "n": FELL}
BREITE = 30                             # Schlitten 10, Leine 1, Rentier 9, Leine 1, Rentier 9

# Die Matrix speichert nur 80 KB je Animation und packt jedes Bild einzeln, Spalte für Spalte: gleiche
# Nachbarspalten und sich wiederholende Spaltenfolgen kosten fast nichts, jede Abweichung ~4 Bytes.
# Darum stehen die Häuser Traufe an Traufe (keine Lücken-Spalte), der Schnee liegt über die ganze
# Dachbreite, die Fenster folgen stur dem Takt "FF.", der Kamin sitzt an einem Dachende, und es
# gibt nur zwei Haus-Sorten im Wechsel (rot, blau, rot, blau, rot): die Wiederholungen sind Abbilder
# der ersten beiden und kosten kaum Speicher – fünf verschiedene Häuser passen nicht in 80 KB.
ROTES_HAUS = (".FF.FF.FFKK", (150, 35, 30), False)
BLAUES_HAUS = ("KK.FF.FF..", (60, 70, 160), True)
HAEUSER = [  # x, Spalten (K Kamin, F Fenster, . Wand), Dachfarbe, Fenster 2 hoch?
    (1, *ROTES_HAUS),
    (14, *BLAUES_HAUS),
    (26, *ROTES_HAUS),
    (39, *BLAUES_HAUS),
    (51, *ROTES_HAUS),
]
SORTE = [0, 1, 0, 1, 0]                 # gleiche Sorte: der Rauch steigt im Gleichtakt
KAMIN_X = [x + muster.index("K") for x, muster, _, _ in HAEUSER]
WAND = (85, 55, 35)
KAMIN = (120, 45, 30)
FENSTER_AN = (255, 190, 50)
FENSTER_MATT = (120, 75, 15)
PAKETE = [PINK, HELLBLAU, TUERKIS, LILA, GELB, HELLGRUEN]
STERNE = [(1, 2, 0, 24), (10, 5, 9, 32), (19, 1, 17, 40), (29, 4, 22, 32), (38, 1, 13, 40),
          (47, 4, 30, 24)]              # x, y, Phase, Periode
STERNLICHT = (255, 240, 200)
STAUB = 4                               # Funken im Schweif des Schlittens
STERN_AB = 0.4                          # Stern leuchtet, solange seine Welle darüber liegt
MOND = (56, 3)
MONDGELB = (245, 235, 170)
OBEN = 12                               # oberste Wandzeile; Dach 11 und 10, Kamin bis 9
KAMIN_OBEN = 9


def sterne(bild, f):
    """Sterne funkeln in drei Stufen und sind etwa die halbe Zeit ganz aus: jeder sichtbare Stern
    kostet in jedem Bild Speicher (rund 1 KB je Stern über die ganze Animation)."""
    for x, y, phase, periode in STERNE:
        v = 0.5 + 0.5 * math.cos(2 * math.pi * (f + phase) / periode)
        if v > STERN_AB:
            bild.setze(x, y, dimmen(STERNLICHT, 0.5 if v < 0.6 else 0.75 if v < 0.85 else 1.0))


def dorf(bild, f, freude):
    """freude[i] = (Bilder seit dem Geschenk, Farbe) oder None."""
    bild.rechteck(0, 15, B, 1, SCHNEEDECKE)
    for i, (x, muster, dach, hoch) in enumerate(HAEUSER):
        b, kamin = len(muster), KAMIN_X[i]
        t = (f + SORTE[i] * 7) % 20                                    # Rauch: ein Wölkchen je Kamin
        if t < 9:
            bild.setze(kamin + (t // 3) % 2, KAMIN_OBEN - 1 - t // 3, dimmen(GRAU, 0.9 - t // 3 * 0.25))
        bild.rechteck(x, OBEN, b, 3, WAND)
        bild.rechteck(x - 1, OBEN - 1, b + 2, 1, dach)               # Dach: Traufe, darüber Schnee
        bild.rechteck(x, OBEN - 2, b, 1, SCHNEEDECKE)
        bild.setze(x - 1, OBEN - 1, SCHNEEDECKE)
        bild.setze(x + b, OBEN - 1, SCHNEEDECKE)
        bild.rechteck(kamin, KAMIN_OBEN, 2, 2, KAMIN)
        fr = freude[i]
        fenster = [x + dx for dx in range(b - 1) if muster[dx:dx + 2] == "FF"]
        for n, wx in enumerate(fenster):                             # Fenster 2 breit
            if fr and fr[0] < 40:                                    # Geschenk da: Fenster blinken bunt
                farbe = fr[1] if (fr[0] // 4) % 2 else WEISS
            else:
                farbe = FENSTER_AN
            bild.rechteck(wx, OBEN + 1, 2, 1, farbe)
            if hoch:
                bild.rechteck(wx, OBEN, 2, 1, farbe)


def sprite_zeichnen(bild, x, y, f, rueckwaerts):
    """Gespann: Schlitten, Leine, zwei Rentiere; x = linke Kante, Breite 30."""
    bein = (f // 3) % 2
    nase = ROT if (f // 4) % 2 else (255, 110, 90)
    teile = [(0, 0, SCHLITTEN, FARBEN), (11, bein, RENTIER[bein], FARBEN),
             (21, 1 - bein, RENTIER[1 - bein], dict(FARBEN, n=nase))]
    for dx, dy, sprite, farben in teile:
        breite = len(sprite[0])
        px = x + (BREITE - dx - breite if rueckwaerts else dx)
        bild.figur(px, y + dy, sprite, farben, spiegeln=rueckwaerts)
    for dx in (10, 20):                                               # Leine
        bild.setze(x + (BREITE - 1 - dx if rueckwaerts else dx), y + 3, KUFE)
    for k in range(1, STAUB + 1):                                     # Sternenstaub hinter dem Schlitten
        if (f + k * 3) % 4 < 2:
            sx = x - k * 2 if not rueckwaerts else x + BREITE - 1 + k * 2
            bild.setze(sx, y + 3 + round(math.sin((f + k * 5) / 2)), dimmen(GELB, 1 - k / 8))


def flug(f, start, rueckwaerts):
    """x des Gespanns oder None; 1 Pixel je Bild."""
    t = f - start
    if not 0 <= t < B + BREITE + 14:
        return None
    return -BREITE - 1 + t if not rueckwaerts else B + 1 - t


def bilder():
    geschenke = []                      # [x, y, farbe, haus]
    freude = [None] * len(HAEUSER)
    funken = []                         # [x, y, alter]
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        sterne(bild, f)
        bild.kreis(*MOND, 2.4, MONDGELB)
        bild.kreis(MOND[0] + 2, MOND[1] - 1, 2, NACHTBLAU)              # Sichel
        sternschnuppe(bild, f, 2, 40, 0)
        sternschnuppe(bild, f, 118, 62, 1)
        sternschnuppe(bild, f, 240, 30, 0)
        for g in geschenke:                                             # fällt senkrecht in den Kamin
            bild.rechteck(g[0], round(g[1]), 2, 2, g[2])
            bild.setze(g[0] + 1, round(g[1]), WEISS)
            g[1] += 0.34
            if g[1] > KAMIN_OBEN - 0.5:                                 # drin: Funken, Haus freut sich
                freude[g[3]] = (0, g[2])
                funken += [[g[0] + dx, KAMIN_OBEN - 1, 0] for dx in (-1, 0, 1, 2)]
        geschenke = [g for g in geschenke if g[1] <= KAMIN_OBEN - 0.5]
        freude = [(fr[0] + 1, fr[1]) if fr else None for fr in freude]
        dorf(bild, f, freude)
        for start, rueck in ((10, False), (128, True)):
            if f == start:
                freude = [None] * len(HAEUSER)
            x = flug(f, start, rueck)
            if x is not None:
                sprite_zeichnen(bild, x, 0, f, rueck)
                sack_x = x + 1 if not rueck else x + BREITE - 3
                for i, haus in enumerate(HAEUSER):                      # Sack über dem Kamin: Geschenk
                    if sack_x == KAMIN_X[i]:
                        geschenke.append([sack_x, 5.0, PAKETE[(i + rueck * 3) % len(PAKETE)], i])
        for fu in funken:
            seite = (-2, -1, 1, 2)[fu[0] % 4]
            bild.setze(fu[0] + seite * fu[2] // 3, fu[1] - fu[2] // 2, WEISS if fu[2] < 3 else GELB)
            fu[2] += 1
        funken = [fu for fu in funken if fu[2] < 6]
        liste.append(bild)
    return liste
