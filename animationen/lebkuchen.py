"""Lebkuchenhaus: Zuckerguss, bunte Bonbons, Lichterkette am Dach, ein tropfender Eiszapfen,
ein Lebkuchenmann läuft herbei und winkt, Zuckerstangen im Schnee – 255 Bilder.

Die Matrix speichert nur 80 KB je Animation und packt jedes Bild einzeln, Spalte für Spalte.
Darum ist das Haus so gebaut, dass je zwei Nachbarspalten gleich sind (Dachstufen, Lampen,
Bonbons und Fenster sitzen im Zweierraster), die Zuckerstangen laufen im Gleichtakt (die zweite
und dritte sind Abbilder der ersten), und es gibt nur wenige Einzelpixel (sechs Flocken, ein
Eiszapfen an der rechten Dachecke).
"""
from basis import (B, BUNT, GRUEN, NACHTBLAU, ROT, SCHNEEDECKE, WEISS, Bild, Schnee, dimmen)

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "lebkuchen"
TITEL = "Lebkuchenhaus mit Eiszapfen und Lebkuchenmann"

LEBKUCHEN = (58, 30, 8)
DUNKEL = (33, 15, 4)
GUSS = (250, 250, 255)
EIS = (120, 210, 255)
HX, HB = 18, 26                 # Haus links, Breite
DACH_Y = 6                      # Traufe
SCHNEE = Schnee(anzahl=6, saat=33, farbe=(170, 180, 220))
BONBONS = [(4, 5), (8, 3), (12, 1), (16, 3), (20, 5), (12, 5)]      # 2×2 auf dem Dach (dx, y), dx gerade
EISZAPFEN = [HX + HB - 1]                                       # jeder kostet ~1 KB: nur die rechte Dachecke
MANN_X = 53
#  l = Lebkuchen, w = Zuckerguss, a = Auge, r/g = Knöpfe
MANN = ["..lll..", ".lalal.", "..lll..", "wlllllw", "..lrl..", "..lgl..", ".ll.ll.", ".ww.ww."]
MANN_SCHRITT = [MANN[:6] + [".ll.ll.", ".ww...."], MANN[:6] + [".ll.ll.", "....ww."]]
MANN_WINKT = ["..lll.w", ".lalall", "..llll.", "wllll..", "..lrl..", "..lgl..", ".ll.ll.", ".ww.ww."]
MANN_FARBEN = {"l": LEBKUCHEN, "w": GUSS, "a": GUSS, "r": ROT, "g": GRUEN}


def haus(bild, f):
    bild.rechteck(HX + 2, DACH_Y + 1, HB - 4, 15 - DACH_Y - 1, LEBKUCHEN)   # Dach steht 2 über
    for k in range(HB // 2 + 1):                                  # Dach (Giebel) mit Guss-Kante
        y = DACH_Y - k // 2
        for x in (HX + k, HX + HB - 1 - k):
            bild.setze(x, y, GUSS)
        for yy in range(y + 1, DACH_Y + 1):
            bild.setze(HX + k, yy, DUNKEL)
            bild.setze(HX + HB - 1 - k, yy, DUNKEL)
    kx = HX + HB - 8                                              # Kamin mit Schneehaube
    bild.rechteck(kx, 1, 2, 3, (150, 45, 30))
    bild.rechteck(kx, 0, 2, 1, GUSS)
    for i, (dx, y) in enumerate(BONBONS):                         # Bonbons auf dem Dach, Farben wandern
        bild.rechteck(HX + dx, y, 2, 2, BUNT[(i * 2 + f // 24) % len(BUNT)])
    bild.rechteck(HX, DACH_Y + 1, HB, 1, DUNKEL)                  # Lichterkette an der Traufe:
    for n, x in enumerate(range(HX, HX + HB, 4)):                 # 7 Lampen 2 breit, blinken im Wechsel
        if (n + f // 8) % 2:
            bild.rechteck(x, DACH_Y + 1, 2, 1, BUNT[(n + 4 + f // 6) % len(BUNT)])
    tx = HX + HB // 2 - 2                                         # Tür mit Zuckerstangen-Rahmen
    bild.rechteck(tx, 11, 4, 4, DUNKEL)
    bild.rechteck(tx, 10, 4, 1, GUSS)
    for y in range(10, 15):
        bild.setze(tx - 1, y, ROT if y % 2 else WEISS)
        bild.setze(tx + 4, y, ROT if y % 2 else WEISS)
    licht = (255, 200, 70) if (f // 9) % 7 else (255, 150, 30)    # Kerzenlicht, beide Fenster gleich
    licht = dimmen(licht, (1.0, 0.92, 0.96)[f % 3])               # Kerze flackert (jedes Bild anders)
    for wx in (HX + 4, HX + HB - 8):                              # Fenster 4 breit mit Guss-Simsen
        bild.rechteck(wx, 9, 4, 1, GUSS)
        bild.rechteck(wx, 13, 4, 1, GUSS)
        bild.rechteck(wx, 10, 4, 3, licht)


def eiszapfen(bild, f):
    for i, x in enumerate(EISZAPFEN):
        laenge = 1 + (i * 7 + f // 60) % 3                        # wächst langsam
        for y in range(DACH_Y + 2, DACH_Y + 2 + laenge):
            bild.setze(x, y, EIS if y < DACH_Y + 1 + laenge else WEISS)
        t = (f + i * 17) % 34                                     # Tropfen fällt
        if t < 15 - DACH_Y - 2 - laenge:
            bild.setze(x, DACH_Y + 2 + laenge + t, EIS)


STANGE = [".###.", "##.##", "##.##"] + ["##..."] * 7             # ab y 5; Haken nach rechts


def zuckerstange(bild, x, f):
    """2 Pixel dick, schräg gestreift; die Streifen wandern langsam nach oben."""
    for dy, zeile in enumerate(STANGE):
        for dx, c in enumerate(zeile):
            if c == "#":
                bild.setze(x + dx, 5 + dy, ROT if (dx + dy + f // 8) // 2 % 2 else WEISS)


def lebkuchenmann(bild, f):
    """läuft 70–103 von rechts herein, winkt bis 200, hüpft, läuft ab 230 wieder weg."""
    if f < 70:
        return
    if f < 103:
        x = B - (f - 70) // 3
    elif f < 230:
        x = MANN_X
    else:
        x = MANN_X + (f - 230) // 2
    y = 7
    if f < 103 or f >= 230:
        sprite = MANN_SCHRITT[(f // 3) % 2]
    elif f < 200:
        sprite = MANN_WINKT if (f // 6) % 2 else MANN
    else:
        sprite = MANN
        y -= 1 if (f // 4) % 2 else 0                             # hüpft
    bild.figur(x, y, sprite, MANN_FARBEN)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        SCHNEE.zeichnen(bild, f)
        bild.rechteck(0, 15, B, 1, SCHNEEDECKE)
        haus(bild, f)
        eiszapfen(bild, f)
        for x in (2, 10, 46):
            zuckerstange(bild, x, f)
        lebkuchenmann(bild, f)
        liste.append(bild)
    return liste
