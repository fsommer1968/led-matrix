"""Wichtelwerkstatt: das Fließband bringt Spielzeug (Ball, Ente, Auto, Teddy, Segelboot) im Takt
von Platz zu Platz – der erste Wichtel packt es in ein buntes Paket mit Band, der zweite
drückt den Stempel drauf (goldenes Siegel), dann fährt das Paket hinaus – 255 Bilder.

Takt 51 Bilder (5 Takte = 255, läuft nahtlos): 17 Bilder fährt das Band einen Platz weiter,
34 Bilder steht es, und die Wichtel arbeiten.

Größe (23.11.2026): Die Matrix speichert je Animation nur 80 KB und komprimiert jedes Bild
einzeln, spaltenweise – jede Spalte, die anders aussieht als eine frühere, kostet in allen 255
Bildern. Damit die Werkstatt unter 76000 Bytes bleibt (vorher 123000): beide Wichtel gleich bis
auf die Mützenfarbe (spitze Mütze, grüner Mantel ohne Knopf), Pakete ohne Licht- und Schattenkante,
Tore ohne Pfosten, Lichterkette als Lauflicht (jedes dritte Licht an), Bandmarken nur während der
Fahrt und nur eine je Platz, keine Rollen unter dem Band.
"""
from basis import (B, BLAU, GELB, HAUT, HELLBLAU, LILA, ORANGE, PINK, ROT, TUERKIS, WEISS, Bild)

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "werkstatt"
TITEL = "Wichtelwerkstatt mit Fließband"

WAND = (30, 12, 5)
BALKEN = (33, 16, 5)
HOLZ = (41, 22, 8)
TAKT, FAHRT = 51, 17
NAHT, NAHT_BEI = 17, 2                      # Bandmarke je Platz, mittig zwischen zwei Gegenständen
PLATZ_A, ABSTAND = 11, 17                   # Mitte des ersten Platzes; B = 28, C = 45, hinaus 62
WICHTEL = ["...w...",
           "...c...",
           "..ccc..",
           ".hhhhh.",
           ".hkhkh.",
           ".wwwww.",
           "ggggggg",
           "ggggggg",
           "ggggggg",
           "ggggggg"]
W1 = {"w": WEISS, "c": ROT, "h": HAUT, "k": (40, 20, 10), "g": (0, 160, 50)}
W2 = dict(W1, c=(0, 90, 255))               # gleicher Wichtel mit blauer Mütze (siehe Größe oben)
W1_X, W2_X = 17, 35
SPIELZEUG = [   # Ball, Ente, Auto, Teddy, Segelboot (je 5×5)
    ([".rrr.", "rrrrr", "wwwww", "bbbbb", ".bbb."], {"r": ROT, "w": WEISS, "b": BLAU}),
    ([".yy..", ".ykoo", "yyyy.", "yyyyy", ".yyy."], {"y": GELB, "k": (30, 20, 0), "o": ORANGE}),
    ([".....", ".bbb.", ".bwb.", "bbbbb", ".k.k."], {"b": HELLBLAU, "w": WEISS, "k": (150, 150, 165)}),
    (["b...b", "bbbbb", "bkbkb", "bbhbb", ".bbb."],
     {"b": (200, 105, 30), "k": (0, 0, 0), "h": (255, 190, 110)}),
    (["..w..", ".ww..", "www..", "rrrrr", ".rrr."], {"w": WEISS, "r": ROT}),
]
PAPIER = [(PINK, WEISS), ((0, 170, 30), ROT), (LILA, WEISS), ((0, 110, 255), PINK), (ROT, WEISS)]
LICHTER = [ROT, GELB, HELLBLAU, PINK, TUERKIS, ORANGE, LILA]


def raum(bild, f, weg):
    bild.rechteck(0, 0, B, 1, BALKEN)
    for i, x in enumerate(range(3, B, 8)):                         # Lichterkette als Lauflicht
        if not 41 <= x <= 49 and (f // 12 + i) % 3 == 0:           # Platz für den Stempel
            bild.setze(x, 1, LICHTER[i % len(LICHTER)])
    bild.rechteck(0, 12, B, 1, (120, 120, 135))                    # Fließband
    bild.rechteck(0, 13, B, 1, (60, 60, 72))
    if f % TAKT < FAHRT:                                           # Marken laufen mit, solange es fährt
        for x in range(B):
            if (x - weg) % NAHT == NAHT_BEI:
                bild.setze(x, 12, (65, 65, 78))


def tor(bild, x0):
    """Kasten, hinter dem das Band herein- und hinausläuft."""
    bild.rechteck(x0, 4, 6, 8, (60, 30, 10))
    bild.rechteck(x0, 4, 6, 1, HOLZ)


def paket(bild, cx, nr, zeilen=6, band_v=6, band_h=7, siegel=0):
    """Paket 7×6 auf dem Band (y 6–11); zeilen/band_* = wie weit schon eingepackt; siegel 0…2."""
    farbe, band = PAPIER[nr]
    x0 = cx - 3
    bild.rechteck(x0, 6, 7, zeilen, farbe)
    bild.rechteck(cx, 6, 1, min(band_v, zeilen), band)
    if zeilen >= 3:
        bild.rechteck(x0, 8, band_h, 1, band)
    if siegel:                                                     # goldenes Siegel 3×3
        bild.rechteck(cx - 1, 7, 3, 3, WEISS if siegel == 2 else (255, 200, 0))
        bild.setze(cx, 8, (255, 200, 0) if siegel == 2 else (255, 255, 160))


def wichtel(bild, x0, farben, hopst=0):
    bild.figur(x0, 2 - hopst, WICHTEL, farben)


def arm(bild, x0, y0, x1, y1, farbe):
    bild.linie(x0, y0, x1, y1, farbe)
    bild.setze(x1, y1, HAUT)


def bilder():
    liste = []
    for f in range(255):
        takt, p = divmod(f, TAKT)
        faehrt = p < FAHRT
        q = p - FAHRT                                              # Bilder seit dem Halt (Arbeit)
        versatz = max(0, FAHRT - 1 - p)                            # so weit fehlt noch zum Platz
        weg = takt * FAHRT + min(p + 1, FAHRT)                     # zurückgelegter Bandweg
        bild = Bild(WAND)
        raum(bild, f, weg)
        cb, cc = PLATZ_A + ABSTAND, PLATZ_A + 2 * ABSTAND          # Plätze B und C
        # Gegenstände auf dem Band: Platz 0 = A (Spielzeug), 1 = B (einpacken), 2 = C (stempeln), 3 = hinaus
        for platz in range(4):
            nr = (takt - platz) % 5
            cx = PLATZ_A + platz * ABSTAND - versatz
            zeilen, farben = SPIELZEUG[nr]
            wippen = 1 if platz == 0 and not faehrt and q in (2, 3, 8, 9) else 0
            if platz == 0:
                bild.figur(cx - 2, 7 - wippen, zeilen, farben)
            elif platz == 1:
                if faehrt or q < 4:
                    bild.figur(cx - 2, 7, zeilen, farben)
                elif q < 10:                                       # Papier senkt sich über das Spielzeug
                    bild.figur(cx - 2, 7, zeilen, farben)
                    paket(bild, cx, nr, zeilen=q - 3, band_v=0, band_h=0)
                else:                                              # Band herum: erst längs, dann quer
                    paket(bild, cx, nr, band_v=min(6, (q - 10) * 2), band_h=max(0, min(7, (q - 13) * 2)))
                    if 17 <= q < 21:                               # fertig: Glanz
                        for dx, dy in ((-4, 5), (4, 5), (-4, 11), (4, 11)):
                            bild.setze(cx + dx, dy, WEISS if q % 2 else GELB)
            elif platz == 2:
                siegel = 0 if faehrt or q < 12 else 2 if q < 17 else 1
                paket(bild, cx, nr, siegel=siegel)
            else:
                paket(bild, cx, nr, siegel=2 if (f // 6) % 4 == 0 else 1)
        tor(bild, 0)
        tor(bild, B - 6)
        # Wichtel stehen vorn: was auf dem Band fährt, zieht hinter ihnen vorbei
        freude1 = 1 if not faehrt and q in (22, 23, 26, 27) else 0
        freude2 = 1 if not faehrt and q in (20, 21, 24, 25) else 0
        wichtel(bild, W1_X, W1, freude1)
        wichtel(bild, W2_X, W2, freude2)
        # Wichtel 1 packt ein: Arm folgt der Arbeit
        sx, sy = W1_X + 6, 8
        if faehrt or q >= 21:
            arm(bild, sx, sy, sx + 1, 10, W1["g"])                 # Arm hängt
        elif q < 4:
            papier = PAPIER[(takt - 1) % 5][0]
            arm(bild, sx, sy, sx + 1, 5 - q // 2, W1["g"])         # hebt das Papier
            bild.rechteck(cb - 3, 4 - q // 2, 7, 2, papier)
        elif q < 10:
            arm(bild, sx, sy, cb - 4, 5 + (q - 3), W1["g"])        # zieht es herunter
        else:
            arm(bild, sx, sy, cb - 4, 7 + (q // 2) % 3, W1["g"])   # bindet das Band
        # Wichtel 2 stempelt
        if faehrt or q < 10 or q >= 19:
            sy_st = 0
        elif q in (10, 18):
            sy_st = 2
        else:
            sy_st = 4
        bild.rechteck(cc - 1, sy_st, 3, 2, (255, 30, 30))          # Stempelkissen rot
        bild.rechteck(cc, sy_st - 2, 1, 2, HOLZ)                   # Griff
        arm(bild, W2_X + 6, 8, cc - 2, sy_st + 1, W2["g"])
        if not faehrt and 11 <= q < 14:                            # Stempel sitzt: Funken
            for dx, dy in ((-5, 4), (5, 4), (-6, 7), (6, 7)):
                bild.setze(cc + dx, dy, GELB)
        liste.append(bild)
    return liste
