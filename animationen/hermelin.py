"""Hermelin im Schnee: weite Schneefläche am frühen Abend, ein Zaunpfahl mit einem Rotkehlchen, ein
kahler Busch, ein paar Grashalme. Das Hermelin im weißen Winterfell ist im Schnee unsichtbar – man
sieht nur zwei schwarze Augen, die Nasenspitze und die schwarze Schwanzspitze. Es taucht auf, sieht
sich um, huscht zum Busch, macht Männchen und taucht ab; neben dem Pfahl taucht es wieder auf, das
Rotkehlchen fliegt erschrocken davon. Beim großen Satz sieht man kurz den Umriss als zarten
Schatten. Dann taucht ein zweites Hermelin auf, beide machen Männchen und verschwinden; der Vogel
kehrt auf den Pfahl zurück. Anfang und Ende zeigen dasselbe stille Bild – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Himmel in waagerechten Streifen (gleiche Spalten), der
Horizont in wenigen langen Stufen, eine einzige gedämpfte Schneefarbe, und vom Hermelin wirklich
nur die vier schwarzen Punkte.
"""
import math

from basis import B, H, SCHWARZ, Bild

NAME = "hermelin"
TITEL = "Hermelin im Schnee"

# früher Abend: oben dunkelblau, am Horizont ein warmer Streifen (je Zeile eine Farbe)
HIMMEL = [(8, 12, 45), (14, 19, 60), (30, 27, 74), (64, 40, 82), (115, 60, 80), (170, 92, 68),
          (170, 92, 68)]
KANTE = (215, 225, 250)                        # Oberkante der Schneedecke
SCHNEE = (78, 90, 140)                         # darunter gedämpft (große Fläche)
WEHE = (112, 126, 178)                         # Kamm einer nahen Schneewehe
STAUB = (165, 178, 225)                        # aufstiebender Schnee
FELL = (116, 130, 182)                         # Umriss im Sprung: nur ein Hauch heller als der Schnee
SCHATTEN = (58, 68, 112)                       # Schatten unter dem Sprung
HOLZ = (100, 58, 24)
ZWEIG = (88, 52, 26)
GRAS = (135, 105, 30)
FEDER = (150, 96, 44)
FLUEGEL = (205, 150, 90)
BRUST = (255, 95, 0)

# Horizont: Oberkante des Schnees, wenige lange Stufen (bis x, Zeile)
HORIZONT = [(5, 7), (14, 6), (26, 5), (44, 6), (58, 5), (64, 6)]
# nahe Schneewehen: (von x, bis x, Zeile)
WEHEN = [(0, 7, 13), (8, 18, 14), (19, 27, 15), (36, 42, 11), (43, 52, 10), (53, 63, 11)]
PFAHL_X, PFAHL_OBEN, PFAHL_UNTEN = 8, 5, 10    # zwei Spalten breit, Schneehaube darüber
PFAHL_FERN = (20, 4, 7)                        # ferner Pfahl: x, oben, unten
GRAESER = [(3, 12, 2), (29, 9, 2), (31, 9, 1), (44, 14, 2), (46, 14, 1), (61, 14, 2)]     # x, Fuß, Höhe
BUSCH_X, BUSCH_Y = 53, 5
BUSCH = ["s..s.s.",
         "z.sz.z.",
         ".zz.zz.",
         "..zzz..",
         "...z..."]

# Rotkehlchen (Blick nach rechts)
SITZT = [".ff", "ffr"]
FLIEGT = [[".w..", "fffr", "...."], ["....", "fffr", ".w.."]]
VOGEL_FARBEN = {"f": FEDER, "r": BRUST, "w": FLUEGEL}
VOGEL_X, VOGEL_Y = PFAHL_X - 1, PFAHL_OBEN - 3

# Sprung (Blick nach rechts): f Fell, a Auge, n Nase, t Schwanzspitze
SATZ_AUF = ["........faf.", ".....ffffffn", "..ffffff....", "ttff........"]
SATZ_OBEN = ["...ffffff...", ".fffffffaf..", "ttf....ffffn"]
SATZ_AB = ["ttff........", "..ffffff....", ".....fffaf..", "........fffn"]
SATZ_FARBEN = {"f": FELL, "a": SCHWARZ, "n": SCHWARZ, "t": SCHWARZ}

# Drehbuch
A_AUF, A_LAUF, A_HALT, A_AB = 10, 35, 55, 82                         # erstes Auftauchen, Lauf zum Busch
A_X0, A_X1, A_Y = 30, 49, 12
B_AUF, B_VOGEL, B_LAUF, B_SATZ, B_LANDUNG = 104, 113, 132, 150, 163  # am Pfahl, Vogel flieht, Satz
B_X0, B_X1, B_X2, B_Y = 17, 33, 49, 13
C_AUF, D_AUF, CD_HOCH, CD_AB = 180, 186, 197, 215                    # zwei Hermeline
C_X, C_Y, D_X, D_Y = 22, 12, 42, 11
VOGEL_ZURUECK, VOGEL_LANDET, VOGEL_DREHT = 222, 245, 250


def horizont(x):
    for bis, y in HORIZONT:
        if x <= bis:
            return y
    return HORIZONT[-1][1]


def hermelin(bild, x, y, blick=0, hoch=0, augen=True, nase=True, schwanz=None, schwanz_y=1):
    """Nur das Schwarze: zwei Augen, darunter die Nase (blick -1/0/1 = schaut links/her/rechts),
    und die Schwanzspitze (schwanz = Seite -1/1, zwei Punkte breit). hoch = Männchen."""
    if nase:
        bild.setze(x + 2 * blick, y - hoch, SCHWARZ)
    if augen:
        bild.setze(x - 1, y - hoch - 1, SCHWARZ)
        bild.setze(x + 1, y - hoch - 1, SCHWARZ)
    if schwanz:
        weit = 3 if hoch > 1 else 5
        bild.setze(x + schwanz * weit, y + schwanz_y, SCHWARZ)
        bild.setze(x + schwanz * (weit + 1), y + schwanz_y, SCHWARZ)


def auftauchen(bild, t, x, y, seite, blick=0):
    """Erst die Nase (Schnee rieselt zur Seite), dann die Augen, zuletzt die Schwanzspitze
    (t = Bilder seit Beginn)."""
    if t < 2:
        bild.setze(x - 2, y - 1 + t, STAUB)
        bild.setze(x + 2, y - 1 + t, STAUB)
    hermelin(bild, x, y, blick, augen=t >= 3, schwanz=seite if t >= 6 else None)


def abtauchen(bild, t, x, y, seite):
    """Kopf voran in den Schnee: Augen zu, Nase weg, die Schwanzspitze stellt sich auf und
    verschwindet im Loch, etwas Schnee stiebt (t = Bilder seit Beginn, bis 7)."""
    if t < 2:
        hermelin(bild, x, y, augen=False, schwanz=seite)
    elif t == 2:
        bild.setze(x + seite * 2, y - 1, SCHWARZ)
        bild.setze(x + seite * 2, y - 2, SCHWARZ)
    elif t == 3:
        bild.setze(x + seite, y - 1, SCHWARZ)
        bild.setze(x + seite, y, SCHWARZ)
    elif t == 4:
        bild.setze(x, y, SCHWARZ)
    if 2 <= t < 7:
        bild.setze(x - (t - 1), y - 1 - t % 2, STAUB)
        bild.setze(x + (t - 1), y - 1 - (t + 1) % 2, STAUB)


def maennchen(t, dauer):
    """Höhe des Kopfes über dem Boden: aufrichten, stehen, wieder hinunter."""
    return min(4, 1 + t * 3 // 2, 1 + (dauer - 1 - t) * 3 // 2) if 0 <= t < dauer else 0


def laufen(bild, t, x, y, richtung):
    """Huschen: Kopf und Schwanzspitze wippen gegeneinander."""
    wipp = (t // 2) % 2
    bild.setze(x + 2 * richtung, y - wipp, SCHWARZ)
    bild.setze(x - 1, y - wipp - 1, SCHWARZ)
    bild.setze(x + 1, y - wipp - 1, SCHWARZ)
    bild.setze(x - richtung * 7, y + wipp, SCHWARZ)
    bild.setze(x - richtung * 8, y + wipp, SCHWARZ)


def satz(bild, x, y, figur, bis_x=B, bis_y=H):
    """Umriss im Sprung, die Nase auf (x, y); rechts von bis_x und unter bis_y steckt er im Schnee."""
    zeile_n = next(i for i, z in enumerate(figur) if "n" in z)
    for dy, zeile in enumerate(figur):
        for dx, c in enumerate(zeile):
            px, py = x - len(zeile) + 1 + dx, y - zeile_n + dy
            if c != "." and px <= bis_x and py <= bis_y:
                bild.setze(px, py, SATZ_FARBEN[c])


def blick_folge(t, folge):
    """folge = [(bis t, blick, augen)] → (blick, augen)."""
    for bis, blick, augen in folge:
        if t < bis:
            return blick, augen
    return 0, True


def erstes(bild, f):
    if A_AUF <= f < A_LAUF:                                          # taucht auf und sieht sich um
        t = f - A_AUF
        blick, augen = blick_folge(t, [(8, 0, True), (13, -1, True), (18, 1, True), (20, 0, True),
                                       (22, 0, False), (25, 1, True)])
        if t < 8:
            auftauchen(bild, t, A_X0, A_Y, -1)
        else:
            hermelin(bild, A_X0, A_Y, blick, augen=augen, schwanz=-1)
    elif f < A_HALT:                                                 # huscht zum Busch
        t = f - A_LAUF
        laufen(bild, t, A_X0 + round((A_X1 - A_X0) * t / (A_HALT - A_LAUF)), A_Y, 1)
    elif f < A_AB:                                                   # macht Männchen und sieht sich um
        t = f - A_HALT
        blick, augen = blick_folge(t, [(4, 0, True), (10, -1, True), (16, 1, True), (18, 0, True),
                                       (20, 0, False), (27, 0, True)])
        hermelin(bild, A_X1, A_Y, blick, maennchen(t - 3, 21), augen, schwanz=-1)
    elif f < A_AB + 7:
        abtauchen(bild, f - A_AB, A_X1, A_Y, -1)
    elif B_AUF <= f < B_LAUF:                                        # taucht am Pfahl auf, der Vogel flieht
        t = f - B_AUF
        if t < 8:
            auftauchen(bild, t, B_X0, B_Y, 1, -1 if t >= 5 else 0)
        else:
            blick, augen = blick_folge(t, [(14, -1, True), (19, 0, True), (25, 1, True), (28, 1, True)])
            hermelin(bild, B_X0, B_Y, blick, maennchen(t - 9, 17), augen, schwanz=1)
    elif f < B_SATZ:                                                 # nimmt Anlauf
        t = f - B_LAUF
        laufen(bild, t, B_X0 + round((B_X1 - B_X0) * t / (B_SATZ - B_LAUF)), B_Y, 1)
    elif f < B_LANDUNG:                                              # der große Satz: Umriss als Schatten
        t = (f - B_SATZ) / (B_LANDUNG - 1 - B_SATZ)
        x = B_X1 + round((B_X2 - B_X1) * t)
        y = B_Y - round(4 * math.sin(math.pi * t))
        bild.rechteck(x - 8, B_Y + 1, 6, 1, SCHATTEN)
        satz(bild, x, y, SATZ_AUF if t < 0.35 else (SATZ_OBEN if t < 0.7 else SATZ_AB))
    elif f < B_LANDUNG + 3:                                          # Kopf voran in den Schnee
        k = f - B_LANDUNG + 1
        satz(bild, B_X2 + k, B_Y + k, SATZ_AB, B_X2 + 1, B_Y)
    elif f < B_LANDUNG + 8:
        abtauchen(bild, f - B_LANDUNG - 1, B_X2, B_Y, -1)
    elif C_AUF <= f < CD_AB + 7:                                     # taucht noch einmal auf …
        t = f - C_AUF
        if t < 8:
            auftauchen(bild, t, C_X, C_Y, -1)
        elif f < CD_AB:
            blick, augen = blick_folge(f - CD_HOCH, [(-7, 0, True), (6, 1, True), (11, 0, True),
                                                     (13, 0, False), (18, 1, True)])
            hermelin(bild, C_X, C_Y, blick, maennchen(f - CD_HOCH, 16), augen, schwanz=-1)
        else:
            abtauchen(bild, f - CD_AB, C_X, C_Y, -1)


def zweites(bild, f):
    """… und ein zweites Hermelin gesellt sich dazu."""
    if D_AUF <= f < CD_AB + 3:
        t = f - D_AUF
        if t < 8:
            auftauchen(bild, t, D_X, D_Y, 1, -1 if t >= 5 else 0)
        elif f < CD_AB - 4:
            blick, augen = blick_folge(f - CD_HOCH, [(7, -1, True), (9, -1, False), (14, 0, True)])
            hermelin(bild, D_X, D_Y, blick, maennchen(f - CD_HOCH - 2, 13), augen, schwanz=1)
        else:
            abtauchen(bild, f - (CD_AB - 4), D_X, D_Y, 1)


def vogel(bild, f):
    if B_VOGEL <= f < VOGEL_ZURUECK:                                 # flieht nach rechts über den Himmel
        t = f - B_VOGEL
        x = VOGEL_X + round(t * 2.5)
        y = max(0, min(3, round(1 - 1.3 * math.sin(t / 3.5)))) if t > 1 else VOGEL_Y - t - 1
        if x < B:
            bild.figur(x, y - 1, FLIEGT[(t // 2) % 2], VOGEL_FARBEN)
    elif VOGEL_ZURUECK <= f < VOGEL_LANDET:                          # kehrt von rechts zurück
        t = VOGEL_LANDET - f
        x = VOGEL_X + round(t * 2.5)
        y = max(0, min(3, round(1 + 1.3 * math.sin(t / 3.5)))) if t > 2 else VOGEL_Y - t
        if x < B:
            bild.figur(x - 1, y - 1, FLIEGT[(t // 2) % 2], VOGEL_FARBEN, spiegeln=True)
    else:                                                            # sitzt auf dem Pfahl
        links = VOGEL_LANDET <= f < VOGEL_DREHT or 48 <= f < 70
        hupf = 1 if f in (B_VOGEL - 3, B_VOGEL - 2) else 0           # erschrickt
        bild.figur(VOGEL_X, VOGEL_Y - hupf, SITZT, VOGEL_FARBEN, spiegeln=links)


def landschaft(bild):
    for x in range(B):
        y0 = horizont(x)
        for y in range(y0):
            bild.setze(x, y, HIMMEL[y])
        bild.setze(x, y0, KANTE)
    for von, bis, y in WEHEN:
        bild.rechteck(von, y, bis - von + 1, 1, WEHE)
    x, oben, unten = PFAHL_FERN
    bild.rechteck(x, oben, 1, unten - oben + 1, HOLZ)
    bild.rechteck(PFAHL_X, PFAHL_OBEN, 2, PFAHL_UNTEN - PFAHL_OBEN + 1, HOLZ)
    bild.rechteck(PFAHL_X, PFAHL_OBEN - 1, 2, 1, KANTE)
    for x, fuss, hoehe in GRAESER:
        bild.rechteck(x, fuss - hoehe + 1, 1, hoehe, GRAS)
    bild.figur(BUSCH_X, BUSCH_Y, BUSCH, {"z": ZWEIG, "s": KANTE})


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(SCHNEE)
        landschaft(bild)
        vogel(bild, f)
        erstes(bild, f)
        zweites(bild, f)
        liste.append(bild)
    return liste
