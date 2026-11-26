"""Sternschnuppen über dem Winterwald: klare, stille Winternacht. Unten eine verschneite Kuppe,
an beiden Flanken dunkle Tannen als Silhouette, darüber zwölf Sterne, die ab und zu blinzeln (zwei
blitzen mit einem kleinen Strahlenkreuz). Die Mondsichel geht links in der Lücke zwischen den
Tannen auf, wandert langsam im flachen Bogen über den Himmel und geht rechts zwischen den Tannen
wieder unter. Ein Fuchs trottet von rechts auf die Kuppe, setzt sich und schaut in die Nacht.
Dreimal zieht eine Sternschnuppe mit leuchtendem Schweif schräg über den Himmel: erst eine vor ihm
(er hebt den Kopf und schaut ihr nach), dann eine hinter seinem Rücken (er dreht den Kopf über die
Schulter), zuletzt zwei kurz hintereinander. Dazwischen zuckt nur ein Ohr oder die Rutenspitze.
Dann steht er auf und trottet nach links weiter, den beiden letzten hinterher; über der leeren
Kuppe fällt noch eine, die keiner mehr sieht. Anfang und Ende zeigen dieselbe Nacht ohne Mond und
Fuchs, die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum einfarbiger Himmel, die Kuppe in wenigen breiten
Stufen, alle Tannen auf derselben untersten Stufe und die rechte Gruppe als verschobene Kopie der
linken, nur zwölf Sterne (jeder kostet etwa 1 bis 2 KB; gleiche Zeilen sind billiger, die Perioden
teilen 255), kein Schneefall; der Schweif der Sternschnuppe liegt in Zweierspalten, der Mond rückt
nur alle vier Bilder weiter.
"""
import math

from basis import B, H, NACHTBLAU, WEISS, Bild, dimmen

NAME = "sternschnuppen"
TITEL = "Sternschnuppen über dem Winterwald"

KANTE = (215, 225, 250)                        # Oberkante der Kuppe
HANG = (78, 90, 140)                           # darunter gedämpft (große Fläche)
TANNE = (0, 60, 28)                            # dunkle Silhouette
MOND = (240, 230, 170)
STERN = (255, 240, 200)
# helle Sterne: x, y, Phase, Periode (teilt 255), blitzt (mit kleinem Strahlenkreuz)?
HELLE = [(4, 1, 0, 85, True), (23, 2, 20, 51, False), (38, 1, 40, 85, True), (59, 1, 10, 51, False)]
# schwache: x, y, Phase – glimmen einmal in 85 Bildern kurz auf; gleiche Zeilen sparen Speicher,
# die beiden in den Tannenlücken stehen 49 Spalten auseinander wie die Tannen
SCHWACHE = [(9, 4, 30), (19, 6, 70), (21, 8, 40), (31, 4, 5), (41, 6, 15), (45, 8, 50), (47, 3, 20),
            (58, 4, 60)]
FUCHS = (255, 105, 0)
FUCHS_DUNKEL = (160, 60, 0)
AUGE = (30, 12, 0)

# Kuppe: Oberkante je Spalte, in breiten Stufen (von links): (ab Spalte, Zeile)
STUFEN = [(0, 15), (17, 14), (24, 13), (40, 14), (47, 15)]
# Tannen: (Mitte x, Höhe), alle auf der untersten Stufe; die rechte Gruppe ist die linke, um 49
# Spalten verschoben (die Kopie kostet wenig). Zwischen der kleinen und der großen bleibt auf jeder
# Seite eine Lücke, in der der Mond auf- und untergeht
TANNEN = [(1, 10), (6, 7), (13, 11), (50, 10), (55, 7), (62, 11)]
# halbe Breite je Zeile von der Spitze an: Etagen, die unten ausladen und darunter wieder einspringen
ETAGEN = {7: [0, 0, 1, 2, 1, 2, 3],
          10: [0, 0, 1, 1, 2, 1, 2, 3, 2, 3],
          11: [0, 0, 0, 1, 2, 1, 2, 3, 2, 3, 3]}

# Mondsichel (Licht von rechts) und die dunkle Scheibe davor (verdeckt die Sterne)
SICHEL = ["..mm..",
          "...mm.",
          "....mm",
          "....mm",
          "...mm.",
          "..mm.."]
SCHEIBE = [".dddd.",
           "dddddd",
           "dddddd",
           "dddddd",
           "dddddd",
           ".dddd."]

# Fuchs (Blick nach links): f Fell, w weiß, a Auge, d Läufe
SITZT = [".f.f....",
         ".faf....",
         "wwff....",
         "..wff...",
         "..wfff..",
         "..fffffw"]
HALB = [".f.f....",                           # Schnauze etwas gehoben
        "wfaf....",
        ".wff....",
        "..wff...",
        "..wfff..",
        "..fffffw"]
HOCH = ["w..f....",                           # Kopf im Nacken, Schnauze nach oben
        ".wff....",
        ".faf....",
        "..wff...",
        "..wfff..",
        "..fffffw"]
ZURUECK = ["..f.f...",                        # Kopf über die Schulter nach rechts gedreht
           "..faf...",
           "..ffww..",
           "..wff...",
           "..wfff..",
           "..fffffw"]
ZURUECK_HOCH = ["..f..w..",
                "..ffw...",
                "..faf...",
                "..wff...",
                "..wfff..",
                "..fffffw"]
WEDELT = [".f.f....",                         # Rutenspitze hebt sich
          ".faf....",
          "wwff....",
          "..wff...",
          "..wfffw.",
          "..fffff."]
LAUSCHT = ["...f....",                        # ein Ohr zuckt
           ".faf....",
           "wwff....",
           "..wff...",
           "..wfff..",
           "..fffffw"]
TROTT_A = [".f.f.......",
           "wfaf.....fw",
           ".ffffffff..",
           "..wfffff...",
           "..d.d.d.d.."]
TROTT_B = [".f.f.......",
           "wfaf......w",
           ".fffffffff.",
           "..wfffff...",
           "...d.d.d..."]
HOCKT = [".f.f.......",                     # zwischen Stehen und Sitzen: Hinterteil gesenkt
         "wfaf.......",
         ".fffff.....",
         "..wffffff..",
         "..d.fffffw."]
FUCHS_FARBEN = {"f": FUCHS, "w": WEISS, "a": AUGE, "d": FUCHS_DUNKEL}

# Drehbuch
FUCHS_SITZT, FUCHS_GEHT = 42, 196             # bleibt stehen / steht wieder auf
SITZ_X = 30                                    # linke Spalte des sitzenden Fuchses
MOND_VON, MOND_WEG = -3, 66                    # linke Spalte der Sichel am Anfang, Weg bis zum Ende
# Sternschnuppen: (Start, x, y, Richtung, Länge in Bildern) – zwei Spalten und eine Zeile je Bild
SCHNUPPEN = [(54, 36, 0, -1, 7), (104, 41, 0, 1, 9), (160, 22, 0, -1, 7), (170, 30, 0, -1, 8),
             (240, 44, 0, -1, 6)]                                # die letzte sieht keiner mehr
SCHWEIF = [WEISS, (190, 215, 255), (110, 150, 255), (50, 80, 210), (20, 35, 120), (12, 20, 72)]
# Kopfhaltung im Sitzen: (von, bis, Figur); sonst SITZT. Er bemerkt eine Schnuppe zwei Bilder nach
# ihrem Start, folgt ihr mit dem Kopf und schaut ihr noch eine Weile nach
BLICKE = [(56, 58, HALB), (58, 64, HOCH), (64, 73, HALB),
          (84, 88, WEDELT), (96, 98, LAUSCHT),
          (106, 108, ZURUECK), (108, 115, ZURUECK_HOCH), (115, 125, ZURUECK),
          (134, 136, LAUSCHT), (146, 150, WEDELT),
          (162, 164, HALB), (164, 169, HOCH), (169, 173, HALB), (173, 179, HOCH), (179, 189, HALB)]


def hang_y(x):
    y = STUFEN[0][1]
    for ab, zeile in STUFEN:
        if x >= ab:
            y = zeile
    return y


def tanne(bild, x, hoehe):
    """Tannen-Silhouette in Etagen, steht direkt auf dem Schnee."""
    fuss = hang_y(x)
    for k, halb in enumerate(ETAGEN[hoehe]):
        bild.rechteck(x - halb, fuss - hoehe + k, 2 * halb + 1, 1, TANNE)


def schnuppe(bild, f, start, x0, y0, richtung, laenge):
    """Sternschnuppe schräg nach unten: je Bild eine Zeile tiefer und zwei Spalten weiter; der
    Schweif (je Zeile zwei gleiche Spalten) verglüht am Ende der Bahn."""
    t = f - start
    if t < 0 or t >= laenge + len(SCHWEIF):
        return
    for k, farbe in enumerate(SCHWEIF):
        n = t - k                                                    # Zeile dieses Schweifstücks
        if 0 <= n < laenge:
            bild.setze(x0 + richtung * 2 * n, y0 + n, farbe)
            bild.setze(x0 + richtung * (2 * n + 1), y0 + n, farbe)


def mond(bild, f):
    """Die Sichel steigt links zwischen den Tannen auf, zieht im flachen Bogen über den Himmel und
    geht rechts unter; an beiden Enden der Runde steht sie unter dem Horizont. Die Zeile hängt an
    der Spalte: die Sichel rückt immer zugleich seitwärts und in der Höhe weiter."""
    x = round(MOND_VON + MOND_WEG * f / 254)
    a = (x - MOND_VON) / MOND_WEG
    y = max(0, round(15 - 15.6 * math.sin(math.pi * a) ** 0.6))
    bild.figur(x, y, SCHEIBE, {"d": NACHTBLAU})
    bild.figur(x, y, SICHEL, {"m": MOND})


def auf_hang(bild, x0, zeilen, farben):
    """Zeichnet den trottenden Fuchs in zwei starren Hälften: die vordere steht auf der Stufe unter
    den Vorderläufen, die hintere auf der unter den Hinterläufen – an einer Stufe steigt erst der
    Vorderkörper, dann folgt das Hinterteil (der Kopf bleibt dabei ganz)."""
    for dx in range(len(zeilen[0])):
        bezug = x0 + (3 if dx < 6 else 7)
        boden = hang_y(max(0, min(B - 1, bezug)))
        for dy, zeile in enumerate(zeilen):
            if zeile[dx] != ".":
                bild.setze(x0 + dx, boden - len(zeilen) + dy, farben[zeile[dx]])


def fuchs(bild, f):
    """Kommt von rechts, sitzt auf der Kuppe und zieht nach links weiter."""
    if f < FUCHS_SITZT or f >= FUCHS_GEHT + 2:                       # trottet, eine Spalte je Bild
        x = SITZ_X + (FUCHS_SITZT - f if f < FUCHS_SITZT else FUCHS_GEHT + 2 - f)
        if -11 < x < B:
            auf_hang(bild, x, TROTT_A if (f // 3) % 2 else TROTT_B, FUCHS_FARBEN)
    elif f < FUCHS_SITZT + 2 or f >= FUCHS_GEHT:                     # bleibt stehen, setzt sich / steht auf
        hockt = f in (FUCHS_SITZT + 1, FUCHS_GEHT)
        bild.figur(SITZ_X, hang_y(SITZ_X) - 5, HOCKT if hockt else TROTT_B, FUCHS_FARBEN)
    else:                                                            # sitzt und schaut
        figur = SITZT
        for von, bis, blick in BLICKE:
            if von <= f < bis:
                figur = blick
        bild.figur(SITZ_X, hang_y(SITZ_X) - 6, figur, FUCHS_FARBEN)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase in SCHWACHE:
            bild.setze(x, y, dimmen(STERN, 0.8 if (f + phase) % 85 < 3 else 0.45))
        for x, y, phase, periode, blitzt in HELLE:                   # funkeln: blinzeln kurz, zwei blitzen
            t = (f + phase) % periode
            bild.setze(x, y, dimmen(STERN, 0.5 if t < 3 else 1.0))
            if blitzt and periode // 2 <= t < periode // 2 + 3:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    bild.setze(x + dx, y + dy, dimmen(STERN, 0.6 if t == periode // 2 + 1 else 0.3))
        mond(bild, f)
        for schnuppe_ in SCHNUPPEN:
            schnuppe(bild, f, *schnuppe_)
        for x, hoehe in TANNEN:
            tanne(bild, x, hoehe)
        for x in range(B):
            y0 = hang_y(x)
            bild.setze(x, y0, KANTE)
            for y in range(y0 + 1, H):
                bild.setze(x, y, HANG)
        fuchs(bild, f)
        liste.append(bild)
    return liste
