"""Schwarzwälder Glasbläser: In der Glashütte steht links der gemauerte Ofen mit glühender Öffnung.
Der Glasbläser (rote Mütze, blaue Schürze) schiebt die lange Pfeife hinein, dreht sie in der
Schmelze und zieht einen glühenden Tropfen heraus (Funken steigen auf), schwenkt ihn herum, dreht
ihn und bläst ihn am Mund zu einer Kugel auf, die Stufe um Stufe größer wird; zwischendurch holt
er Luft. Die Kugel kühlt ab (glühend orange, rot, dunkelrot, dann durchsichtig hellblau), die Farbe
steigt von unten auf und sie glänzt bunt – erst rot, dann gold, dann grün. Die fertige Kugel löst
sich, schwebt nach rechts und hängt sich an den kleinen Christbaum; der Glasbläser holt schon den
nächsten Tropfen. Hängen alle drei, funkeln Stern und Kugeln, der geschmückte Baum rollt hinaus und
ein frischer kommt herein. Drei Durchgänge zu je 85 Bildern; die Runde geht ohne Sprung in sich
über – 255 Bilder.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum schwarze Wand ohne Boden (alles steht auf der
Unterkante), ein Ofen aus gleichen Spalten, Glut und Baum spiegelgleich (rechte Hälfte = linke),
die Pfeife immer waagerecht, der Glasbläser drei Spalten breit mit zwei fast gleichen, einfarbige
Kugeln, kein Flimmern. Alles, was sich bewegt, hängt nur vom Bild im Durchgang ab oder hat einen
Takt, der in 85 aufgeht (Glut: 17 Schritte zu je 5 Bildern).
"""
import math

from basis import GELB, HAUT, HELLBLAU, ORANGE, ROT, WEISS, Bild, mischen

NAME = "glasblaeser"
TITEL = "Schwarzwälder Glasbläser"

RUNDE = 255
GANG = 85                                      # ein Durchgang (rote, goldene, grüne Kugel)

OFEN = (62, 64, 80)                            # gemauerter Ofen, gedämpft (große Fläche)
OFEN_HELL = (120, 122, 140)                    # Oberkante der Kuppel
KERN = (255, 245, 170)                         # hellste Glut
GLUT_ROT = (235, 45, 0)                        # Glas, das schon abkühlt
DUNKELGLUT = (140, 12, 0)                      # … und nur noch schwach glimmt
GLAS = HELLBLAU                                # Rand der abgekühlten, noch klaren Kugel
GLAS_INNEN = (0, 30, 55)                       # ihr durchsichtiges Inneres
ROHR = (150, 150, 175)                         # Glasmacherpfeife
MUETZE = ROT
HEMD = (210, 210, 225)
SCHUERZE = (0, 70, 255)
HOSE = (90, 90, 100)
AUGE = (50, 25, 10)
TANNE = (0, 95, 35)
KAPPE = (190, 210, 255)                        # silberner Aufhänger der fertigen Kugel
KUGELFARBEN = [ROT, (255, 170, 0), (0, 255, 60)]                    # rot, gold, grün

OFEN_B = 15                                    # Ofen: Spalten 0 bis 14, Kuppel ab Zeile 3
GLUT_X, GLUT_Y = 5, 7                          # Öffnung: sieben Spalten, sieben Zeilen
MANN_X, MANN_Y = 19, 5                         # linke Spalte und oberste Zeile des Glasbläsers
HAND, MUND = 10, 8                             # Zeile des Rohrs in den Händen und am Mund
KUGEL_L, KUGEL_Y = 39, MUND                    # die Kugel wächst vom Rohrende nach rechts
BAUM_X = 57
# halbe Breite je Zeile: drei Etagen
BAUM = {4: 0, 5: 1, 6: 2, 7: 3, 8: 1, 9: 2, 10: 3, 11: 4, 12: 2, 13: 3, 14: 4, 15: 5}
PLAETZE = [(52, 11), (59, 11), (56, 7)]        # hier hängen die drei Kugeln (linke obere Ecke)
BAUM_WEG = 12                                  # so weit rollt der Baum hinaus

# Zeitplan eines Durchgangs (Bild im Durchgang)
T_REIN, T_HOLT, T_RAUS = 5, 12, 17             # Pfeife im Ofen, Tropfen gefasst, Tropfen heraus
T_SCHWENK, T_DREHT, T_BLAS = 25, 33, 35        # herumgeschwenkt, gedreht, an den Mund gehoben
STUFE = 4                                      # alle vier Bilder eine Kugelgröße mehr (sechs Größen)
ATEM = 8                                       # alle acht Bilder holt er Luft (Kopf kurz vom Rohr)
T_ORANGE, T_ROT, T_DUNKEL, T_KLAR, T_BUNT, T_LOS = 59, 62, 65, 68, 73, 77
FLUG = 18                                      # so lange schwebt die Kugel zum Baum
# Baumwechsel (Bild in der Runde): die dritte Kugel hängt ab Bild VOLL
VOLL = 2 * GANG + T_LOS + FLUG - RUNDE
FUNKELN_BIS, HINAUS, FORT, HEREIN, DA = 34, 36, 46, 48, 58

# Glasbläser (Blick nach rechts): m Mütze, h Haut, a Auge, j Hemd, s Schürze, b Hose
HAELT = [".mmm.", ".mmmm", ".hha.", ".hhh.", "jsssj", "jsssj", ".sss.", ".sss.", ".bbb.", ".bbb.", ".bbb."]
BLAEST = [".mmm..", ".mmmm.", ".hha..", ".hhh..", "jsssjj", "jsss..", "hsss..", ".sss..", ".bbb..",
          ".bbb..", ".bbb.."]
VORN = [".mmm.", ".mmm.", ".aha.", ".hhh."] + HAELT[4:]            # im Schwenk: Blick zum Betrachter
KOPF = 4                                       # so viele Zeilen gehören zum Kopf
MANN = {"m": MUETZE, "h": HAUT, "a": AUGE, "j": HEMD, "s": SCHUERZE, "b": HOSE}

# Glut in der Ofenöffnung, von oben nach unten: o orange, y gelb, k helle Schmelze. Die drei
# mittleren Spalten sind gleich, die daneben eine Zeile tiefer, die am Rand orange – ruhig,
# gedämpft, hell
GLUT = ["ooyyykk", "oooyyyk", "oyyykkk"]
FLACKERN = [0, 1, 0, 2, 1, 0, 2, 0, 1, 2, 0, 1, 0, 2, 1, 2, 1]     # 17 Schritte zu je 5 Bildern
HEISS = {"o": ORANGE, "y": GELB, "k": KERN}

# Tropfen am Rohrende (nach rechts gezeichnet, Zeile des Rohrs = zweite Angabe): frisch, sackt, steigt
TROPFEN = [(["yy", "yo"], 0), (["yy", "yy", ".o"], 0), ([".o", "yy", "yy"], -1)]
DREHEN = [0, 1, 0, 2]
# Kugelgrößen beim Aufblasen, die Mitte liegt in der Zeile des Rohrs
FORMEN = [[".X.", "XXX", ".X."],
          ["XXX", "XXX", "XXX"],
          [".XX.", "XXXX", "XXXX", "XXXX", ".XX."],
          [".XXX.", "XXXXX", "XXXXX", "XXXXX", ".XXX."],
          ["..XX..", ".XXXX.", "XXXXXX", "XXXXXX", "XXXXXX", ".XXXX.", "..XX.."],
          ["..XXX..", ".XXXXX.", "XXXXXXX", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX.."]]
GROSS, MITTEL = FORMEN[5], FORMEN[3]
KLEIN = [".XX.", "XXXX", "XXXX", ".XX."]       # so hängt sie am Baum

# Schwenk vom Ofen zum Baum in vier Schritten zu je zwei Bildern: (Blick, Zeile, Rohr von, bis);
# von = None: das Rohr zeigt gerade zum Betrachter
SCHWENK = [(-1, HAND, 16, 26), (0, HAND, None, None), (1, HAND, 19, 29), (1, HAND, 19, 34)]
# … und nach dem Loslassen der Kugel zurück (je ein Bild)
ZURUECK = [(1, HAND - 1, 21, 36), (1, HAND, 19, 34), (1, HAND, 19, 29), (1, HAND, 19, 29),
           (0, HAND, None, None), (0, HAND, None, None), (-1, HAND, 16, 26), (-1, HAND, 13, 28)]
# Funken, wenn der Tropfen aus dem Ofen kommt: (Bild im Durchgang, Spalte, Drift je Bild)
FUNKEN = [(12, 9, 0.5), (14, 11, 0.8), (16, 8, -0.3)]


def _sanft(a):
    a = max(0.0, min(1.0, a))
    return a * a * (3 - 2 * a)


# ── Ofen ───────────────────────────────────────────────────────────
def _ofen(bild, f, t):
    bild.rechteck(2, 0, 3, 3, OFEN)                                 # Abzug
    for x in range(OFEN_B):                                         # Kuppel mit heller Oberkante
        oben = 3 + max(0, 2 - x, x - OFEN_B + 3)
        bild.setze(x, oben, OFEN_HELL)
        bild.rechteck(x, oben + 1, 1, 15 - oben, OFEN)
    stufe = 2 if T_REIN <= t < T_HOLT else FLACKERN[(f // 5) % 17]  # mit der Pfeife darin lodert es hell
    bild.rechteck(GLUT_X, GLUT_Y + 1, 7, 6, ORANGE)                 # Öffnung mit gerundeten Ecken
    for dx in range(1, 6):                                          # Glut: in der Mitte eine Zeile höher
        zeilen = GLUT[stufe] if 1 < dx < 5 else "o" + GLUT[stufe][:6]
        for dy, c in enumerate(zeilen):
            bild.setze(GLUT_X + dx, GLUT_Y + dy, HEISS[c])


# ── Glasbläser, Pfeife und Glas ────────────────────────────────────
def _haltung(t):
    """Pfeife im Durchgang: (Blick, Zeile, von, bis) – Blick -1 zum Ofen, 0 nach vorn, +1 zum Baum."""
    if t <= T_REIN:                                                 # schiebt die Pfeife in den Ofen
        return -1, HAND, 13 - t, 28 - t
    if t < T_HOLT:                                                  # dreht sie in der Schmelze hin und her
        s = (t - T_REIN) // 2 % 2
        return -1, HAND, 8 - s, 23 - s
    if t < T_RAUS:                                                  # zieht sie mit dem Tropfen heraus
        s = t - T_HOLT + 1
        return -1, HAND, 8 + s, 23 + s
    if t < T_SCHWENK:                                               # schwenkt zum Baum herum
        return SCHWENK[(t - T_RAUS) // 2]
    if t < T_DREHT:
        return 1, HAND, 19, 34
    if t == T_DREHT:                                                # hebt sie an den Mund
        return 1, HAND - 1, 21, 36
    if t < T_LOS:
        return 1, MUND, 23, 38
    return ZURUECK[t - T_LOS]


def _kugel(bild, x0, cy, form, rand, innen=None, glanz=None, farbe=None, ab=99):
    """Kugel mit linker Spalte x0 und Mitte in Zeile cy; innen = Farbe der Felder, die ringsum
    Nachbarn haben (sonst wie der Rand); glanz = Farbe des Glanzpunkts oben links; ab der Zeile
    `ab` der Form ist die Kugel schon in `farbe` gefärbt."""
    h, b = len(form), len(form[0])
    y0 = cy - h // 2
    for dy, zeile in enumerate(form):
        for dx, c in enumerate(zeile):
            if c == ".":
                continue
            mitten = (0 < dy < h - 1 and 0 < dx < b - 1 and form[dy - 1][dx] != "." and form[dy + 1][dx] != "."
                      and zeile[dx - 1] != "." and zeile[dx + 1] != ".")
            bild.setze(x0 + dx, y0 + dy, farbe if dy >= ab else (innen if (mitten and innen) else rand))
    if glanz:
        bild.setze(x0 + (b - 1) // 3, y0 + (h - 1) // 3, glanz)


def _blitz(bild, x, y):
    """Weißes Kreuz: ein Glanzpunkt blitzt auf."""
    bild.rechteck(x - 1, y, 3, 1, WEISS)
    bild.rechteck(x, y - 1, 1, 3, WEISS)


def _blaeser(bild, t, farbe):
    blick, zeile, von, bis = _haltung(t)
    am_mund = zeile == MUND
    figur = BLAEST if am_mund else (HAELT if blick else VORN)
    atmet = T_BLAS <= t < T_ORANGE and (t - T_BLAS) % ATEM >= ATEM - 2          # holt Luft: Kopf zurück
    bild.figur(MANN_X - (1 if atmet else 0), MANN_Y, figur[:KOPF], MANN, spiegeln=blick < 0)
    bild.figur(MANN_X, MANN_Y + KOPF, figur[KOPF:], MANN, spiegeln=blick < 0)
    if von is None:                                                 # Rohr zeigt zum Betrachter
        bild.rechteck(MANN_X, HAND, 5, 1, ROHR)
    else:
        bild.rechteck(von, zeile, bis - von + 1, 1, ROHR)
    if am_mund:
        bild.setze(MANN_X + 6, MUND, HAUT)                          # Hand am Rohr
    else:                                                           # beide Hände am Rohr; beim Heben nur die vordere
        bild.setze(MANN_X, HAND, HAUT)
        bild.setze(MANN_X + 4, zeile, HAUT)
    for start, x0, drift in FUNKEN:                                 # Funken steigen aus der Öffnung
        b = t - start
        if 0 <= b < 6:
            bild.setze(x0 + drift * b, GLUT_Y - 1 - b, GELB if b < 3 else ORANGE)
    # Glas am Rohrende
    if t < T_HOLT or t >= T_LOS:
        return
    if von is None:                                                 # glühendes Ende von vorn
        bild.rechteck(MANN_X + 1, HAND, 3, 2, GELB)
        bild.setze(MANN_X + 2, HAND, KERN)
    elif t < T_BLAS:                                                # Tropfen, beim Drehen sackt und steigt er
        form, dy = TROPFEN[DREHEN[((t - T_SCHWENK) // 2) % 4] if T_SCHWENK <= t < T_DREHT else 0]
        x = bis + 1 if blick > 0 else von - 2
        bild.figur(x, zeile + dy, form, HEISS, spiegeln=blick < 0)
    elif t < T_ORANGE:                                              # wird aufgeblasen
        stufe = min(5, (t - T_BLAS) // STUFE)
        _kugel(bild, KUGEL_L, KUGEL_Y, FORMEN[stufe], GELB if stufe < 2 else ORANGE, GELB,
               KERN if stufe < 2 else None)
    elif t < T_KLAR:                                                # kühlt ab: orange, rot, dunkelrot
        _kugel(bild, KUGEL_L, KUGEL_Y, GROSS, ORANGE if t < T_ROT else (GLUT_ROT if t < T_DUNKEL else DUNKELGLUT))
    else:                                                           # klar; dann steigt die Farbe von unten auf
        _kugel(bild, KUGEL_L, KUGEL_Y, GROSS, GLAS, GLAS_INNEN, WEISS, farbe, 7 - 2.5 * max(0, t - T_BUNT + 1))
        if t < T_BUNT:
            bild.setze(KUGEL_L + 4, KUGEL_Y + 1, GLAS)              # Lichtreflex im klaren Glas
        elif t >= T_LOS - 2:
            _blitz(bild, KUGEL_L + 2, KUGEL_Y - 1)                  # fertig: der Glanzpunkt blitzt auf


# ── Kugel unterwegs und Christbaum ─────────────────────────────────
def _baum_versatz(f):
    """Der geschmückte Baum rollt nach rechts hinaus, ein frischer kommt herein (None = keiner da)."""
    if f < HINAUS or f >= DA:
        return 0
    if f < FORT:
        return round(BAUM_WEG * _sanft((f - HINAUS + 1) / (FORT - HINAUS)))
    if f < HEREIN:
        return None
    return round(BAUM_WEG * (1 - _sanft((f - HEREIN + 1) / (DA - HEREIN))))


def _baum(bild, f, dx):
    cx = BAUM_X + dx
    for y, halb in BAUM.items():
        bild.rechteck(cx - halb, y, 2 * halb + 1, 1, TANNE)
    hell = VOLL <= f < FUNKELN_BIS and (f // 3) % 2                  # alle drei Kugeln hängen: der Stern funkelt
    bild.rechteck(cx - 1, 2, 3, 1, WEISS if hell else GELB)
    bild.rechteck(cx, 1, 1, 3, WEISS if hell else GELB)


def _kugeln(bild, f, dx):
    """Die drei Kugeln der Runde: im Flug zum Baum oder schon am Baum (bis er hinausrollt)."""
    for nr, farbe in enumerate(KUGELFARBEN):
        los = nr * GANG + T_LOS
        zx, zy = PLAETZE[nr]
        for u in (f - los, f + RUNDE - los):                        # diese Runde oder noch die davor
            if 0 <= u < FLUG:
                a = (u + 1) / FLUG
                a = (a + _sanft(a)) / 2                             # sanft los, zügig ans Ziel
                form = GROSS if u < 6 else (MITTEL if u < 12 else KLEIN)
                halb = len(form) / 2                                # die Mitte wandert, die Kugel wird kleiner
                x0 = round(KUGEL_L + 3.5 + (zx + 2 - KUGEL_L - 3.5) * a - halb)
                y0 = round(KUGEL_Y + 0.5 + (zy + 2 - KUGEL_Y - 0.5) * a - 2 * math.sin(math.pi * a) - halb)
                _kugel(bild, x0, y0 + len(form) // 2, form, farbe, glanz=WEISS)
                if form is not KLEIN:                               # Aufhänger obenauf
                    bild.setze(x0 + len(form) // 2, y0 - 1, KAPPE)
            elif FLUG <= u < RUNDE + FORT - los and dx is not None:
                hell = u < FLUG + 2                                 # blitzt beim Aufhängen
                _kugel(bild, zx + dx, zy + 2, KLEIN, mischen(farbe, WEISS, 0.6) if hell else farbe,
                       glanz=WEISS)
                if VOLL + 2 <= f < FUNKELN_BIS and (f - VOLL) // 2 % 4 == nr + 1:   # reihum ein Blitzen
                    _blitz(bild, zx + 1, zy + 1)


def bilder():
    liste = []
    for f in range(RUNDE):
        gang, t = divmod(f, GANG)
        bild = Bild()
        _ofen(bild, f, t)
        dx = _baum_versatz(f)
        if dx is not None:
            _baum(bild, f, dx)
        _blaeser(bild, t, KUGELFARBEN[gang])
        _kugeln(bild, f, dx)
        liste.append(bild)
    return liste
