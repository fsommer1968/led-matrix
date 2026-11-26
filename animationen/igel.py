"""Igel im Winterschlaf: Am Waldrand liegt unter einer Hecke ein großer Laubhaufen in Rot, Orange und
Gelb. Darunter schläft ein Igel – der Haufen hebt und senkt sich langsam, Schlafbläschen steigen auf.
Ein letztes Blatt segelt herab, dann beginnt es zu schneien: der Schnee legt sich als weiße Haube auf
Laub, Hecke und Boden. Einmal schiebt der Igel Nase und Äuglein heraus, blinzelt, schnuppert, gähnt
und zieht sich wieder zurück. Zum Schluss fegt ein Windstoß den Schnee fort – Anfang und Ende zeigen
denselben Herbsthaufen, 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Himmel, Hecke und Boden als waagerechte Streifen (gleiche
Spalten), der Stamm ganz am linken Rand, das Laub aus nur sieben Spaltenmustern, die sich in Stücken
von drei, vier Spalten wiederholen (eine schon gezeigte Spalte kostet fast nichts), die Stufen des
Haufens und die Senken der Hecke an den Grenzen dieser Stücke, der Schnee auf Boden und Hecke als
durchgehende Zeile, wenige Flocken, höchstens zwei Bläschen.
Das Laub darf orange leuchten; Stamm und Stacheln sind sehr dunkel, damit sie braun bleiben.
"""
import math
import random

from basis import B, HAUT, SCHWARZ, Bild

NAME = "igel"
TITEL = "Igel im Winterschlaf"

HIMMEL = (10, 18, 62)
HECKE = (0, 55, 26)
HECKE_HELL = (0, 100, 30)                      # Kuppen der Hecke
BEERE = (255, 0, 40)
GRAS = (26, 50, 0)
ERDE = (14, 30, 0)
KANTE = (215, 225, 250)                        # Schnee oben
BODEN = (78, 90, 140)                          # Schnee darunter, gedämpft
FLOCKE = (150, 160, 200)
STAUB = (235, 240, 255)
BLASE = (110, 190, 255)
STAMM = (66, 30, 4)
BORKE = (33, 11, 0)
LAUB = {"r": (205, 18, 0), "o": (255, 90, 0), "g": (255, 185, 0), "d": (120, 24, 0)}
STACHEL = (66, 30, 4)
SPITZE = (150, 125, 95)
MAUL = (255, 60, 90)

RUNDE = 255
ATEMZUEGE = 6                                  # je Runde
BODEN_Y = 14                                   # Zeilen 14 und 15 sind Boden
X0 = 17                                        # linker Rand des Haufens, 32 Spalten breit
# Höhe je Spalte (ausgeatmet); die Stufen liegen, wo es geht, an den Grenzen der Laubflecken
BASIS = [2, 3, 4, 5, 5, 5, 5, 6, 6, 6] + [7] * 10 + [6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 3, 2]
# Laub: sieben Spaltenmuster (von oben nach unten), in Stücken von zwei bis vier Spalten gereiht
MUSTER = {"a": "oggorgr", "b": "gogrrod", "c": "grooggr", "d": "ogorror", "e": "oorggrd", "f": "googrrr",
          "g": "orgoorr"}
FOLGE = "dddaaaabbbgggcccceeefffaaaadddbb"
TEX = ["".join(MUSTER[m][r] for m in FOLGE) for r in range(7)]
# Hecke: Oberkante je Spalte (2 = Kuppe, 3 = Senke); über dem Haufen an den Grenzen der Laubflecken
SENKEN = [(9, 12), (20, 24), (40, 44), (51, 54), (59, 62)]
BEEREN = [(11, 7), (14, 10), (55, 6), (59, 9)]
STREU = [(9, "o"), (10, "g"), (53, "g"), (58, "r"), (59, "o")]      # einzelne Blätter im Gras

# Drehbuch
BLATT = 244                                    # das letzte Blatt löst sich (landet in der nächsten Runde)
SCHNEE_AN, SCHNEE_AUS = 18, 180                # in dieser Zeit starten Flocken
HAUBE_1, HAUBE_2 = 36, 88                      # ab hier wächst die erste, die zweite Lage der Haube
BODEN_1, BODEN_2, HECKE_1 = 46, 76, 60         # ab hier wird der Boden weiß, dick weiß, die Hecke weiß
WACH, RAUS, DRAUSSEN, REIN, WEG = 102, 108, 119, 177, 188            # rascheln, heraus, schauen, zurück, fort
WIND = 226                                     # der Windstoß setzt ein …
WIND_TEMPO = 4                                 # … und fegt mit vier Spalten je Bild nach rechts
KEIME_1 = (12, 30, 47, 59)                     # von hier breitet sich der Schnee am Boden aus
KEIME_2 = (4, 22, 39, 54)
KEIME_HECKE = (10, 26, 43, 57)

# Igelkopf (Blick nach rechts): s Stacheln, h helle Stachelspitzen, f Gesicht, a Auge, k Nase, m Maul
KOPF = ["..hsh......",
        ".shssff....",
        "hsshffaff..",
        "sshsffffffk",
        ".sssffff..."]
KOPF_ZU = KOPF[:2] + ["hsshfffff.."] + KOPF[3:]
KOPF_SCHNUPPERT = KOPF[:2] + ["hsshffafffk", "sshsfffff..", ".sssffff..."]
KOPF_GAEHNT = ["..hsh......",
               ".shssffffk.",
               "hsshfffff..",
               "sshsfmmm...",
               ".sssffffff."]
KOPF_FARBEN = {"s": STACHEL, "h": SPITZE, "f": HAUT, "a": SCHWARZ, "k": SCHWARZ, "m": MAUL}
KOPF_X, KOPF_Y = X0 + 13, 9                    # Platz des Kopfes, wenn er ganz heraus ist
KOPF_B = 11                                    # Breite; links von KOPF_X bleibt er im Laub verborgen


def atem(f):
    """0 (ausgeatmet) bis 1 (eingeatmet), sechs ruhige Atemzüge je Runde."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * f * ATEMZUEGE / RUNDE)


def hub(c, f):
    """Um wie viele Zeilen die Spalte c des Haufens gehoben ist: beim Einatmen wölbt sich erst die
    Kuppe, dann die ganze Mitte; kurz vor dem Aufwachen raschelt es über dem Igel."""
    a = atem(f)
    hoch = 0
    if a >= 0.75 and 13 <= c <= 16:
        hoch = 2
    elif a >= 0.45 and 9 <= c <= 20 or a >= 0.2 and 13 <= c <= 16:
        hoch = 1
    if WACH <= f < RAUS and (f - WACH) // 2 % 2 == 0 and 13 <= c <= 22:
        hoch = min(2, hoch + 1)
    return hoch


def windfront(f):
    """Spalte, bis zu der der Windstoß am Ende schon gefegt hat."""
    return -4 + (f - WIND) * WIND_TEMPO if f >= WIND else -99


def bedeckt(f, ab, keime, x):
    """Schnee breitet sich ab Bild `ab` von den Keimen nach beiden Seiten aus."""
    return f >= ab and min(abs(x - k) for k in keime) <= (f - ab) / 2 and x >= windfront(f)


def haube(c, f):
    """Dicke der Schneehaube über Spalte c: wächst von der Kuppe nach außen, der Wind trägt sie ab."""
    front = windfront(f)
    x = X0 + c
    d = abs(c - 14.5)
    dick = 0
    if f >= HAUBE_1 and d <= min(12, (f - HAUBE_1) / 4 + 0.5):
        dick = 1
    if f >= HAUBE_2 and d <= min(3, (f - HAUBE_2) / 6 + 0.5):
        dick = 2
    if x < front - 5:
        return 0
    if x < front:
        return min(dick, 1)
    return dick


def oberkante(c, f):
    """Oberste Zeile des Haufens samt Haube in Spalte c."""
    return BODEN_Y - BASIS[c] - hub(c, f) - haube(c, f)


def hecke_y(x):
    return 3 if any(von <= x < bis for von, bis in SENKEN) else 2


def landschaft(bild, f):
    streu = dict(STREU)
    for x in range(B):
        y0 = hecke_y(x)
        for y in range(BODEN_Y):
            bild.setze(x, y, HIMMEL if y < y0 else HECKE_HELL if y == 2 else HECKE)
        if bedeckt(f, HECKE_1, KEIME_HECKE, x):
            bild.setze(x, y0 - 1, KANTE)
        gras = LAUB[streu[x]] if x in streu else GRAS                # der Schnee deckt auch die Blätter zu
        bild.setze(x, BODEN_Y, KANTE if bedeckt(f, BODEN_1, KEIME_1, x) else gras)
        bild.setze(x, BODEN_Y + 1, BODEN if bedeckt(f, BODEN_2, KEIME_2, x) else ERDE)
    for x, y in BEEREN:
        bild.setze(x, y, BEERE)
    bild.rechteck(0, 0, 5, BODEN_Y, STAMM)                           # Stamm am Waldrand
    bild.rechteck(0, 0, 1, BODEN_Y, BORKE)


def haufen(bild, f):
    """Laubhaufen mit Atem und Schneehaube: die unteren zwei Zeilen liegen fest, darüber hebt sich alles."""
    for c in range(32):
        x = X0 + c
        hoch = hub(c, f)
        y0 = BODEN_Y - BASIS[c] - hoch
        for y in range(y0, BODEN_Y):
            r = y - 7 + hoch if y < 12 else y - 7
            bild.setze(x, y, LAUB[TEX[r][c]])
        for k in range(haube(c, f)):
            bild.setze(x, y0 - 1 - k, KANTE)


def igel(bild, f):
    """Der Kopf schiebt sich nach rechts aus dem Laub: blinzeln, schnuppern, gähnen, zurück."""
    if not WACH <= f < WEG:
        return
    if f < RAUS:                                                     # es raschelt: nur die Nase
        heraus = 1 + (f - WACH) // 3
    elif f < DRAUSSEN:
        heraus = min(KOPF_B, 2 + f - RAUS)
    elif f < REIN:
        heraus = KOPF_B
    else:
        heraus = max(0, KOPF_B - (f - REIN))
    t = f - DRAUSSEN
    figur = KOPF
    if 4 <= t < 6 or 9 <= t < 11 or 53 <= t < 55:                    # blinzelt
        figur = KOPF_ZU
    elif 14 <= t < 32 and (t - 14) // 3 % 2 == 0:                    # schnuppert
        figur = KOPF_SCHNUPPERT
    elif 36 <= t < 50:                                               # gähnt
        figur = KOPF_GAEHNT
    x = KOPF_X - (KOPF_B - heraus)
    for dy, zeile in enumerate(figur):
        for dx, z in enumerate(zeile):
            if z != "." and x + dx >= KOPF_X:
                bild.setze(x + dx, KOPF_Y + dy, KOPF_FARBEN[z])


def blasen(bild, f):
    """Schlafbläschen statt „z“: je Atemzug zwei, steigen schräg nach rechts oben und werden größer.
    Die Runde ist dafür ein Kreis – das letzte Bläschen steigt in der nächsten Runde weiter."""
    c0 = 18                                                          # hier, über dem Igel, lösen sie sich
    for zug in range(ATEMZUEGE):
        aus = round((zug + 0.5) * RUNDE / ATEMZUEGE)                 # hier beginnt das Ausatmen
        if WACH - 30 < aus < WEG:                                    # der Igel ist wach
            continue
        for k in range(2):
            start = aus + k * 12
            t = (f - start) % RUNDE
            schritt = t // 5
            y = oberkante(c0, start % RUNDE) - 1 - schritt
            if t >= 30 or y < 0:
                continue
            x = X0 + c0 + schritt + schritt % 2
            bild.setze(x, y, BLASE)
            if t >= 12:
                bild.setze(x + 1, y, BLASE)
                bild.setze(x, y - 1, BLASE)
                bild.setze(x + 1, y - 1, BLASE)


def blatt(bild, f):
    """Das letzte Blatt: löst sich am Ende der Runde und segelt am Anfang der nächsten auf den Haufen."""
    t = (f - BLATT) % RUNDE
    y = t // 3
    x = 48 - t // 6 + (0, 1, 2, 1)[t // 3 % 4]
    c = x - X0
    if y < (oberkante(c, f) if 0 <= c < 32 else BODEN_Y):
        bild.setze(x, y, LAUB["g" if t // 3 % 2 else "o"])


def flocken_liste():
    """Start, Spalte, Tempo und Pendelphase der Flocken – gleichmäßig über die Schneezeit verteilt."""
    z = random.Random(5)
    liste = []
    n = 30
    for k in range(n):
        start = SCHNEE_AN + round(k * (SCHNEE_AUS - SCHNEE_AN) / (n - 1))
        liste.append((start, z.randrange(8, B - 1), z.choice([0.34, 0.5]), z.randrange(20)))
    return liste


FLOCKEN = flocken_liste()
# Schneefahne: Abstand vor der Windfront, Höhe über Haufen oder Boden (abwechselnd zwei Muster)
FAHNE = [[(0, 1), (2, 2), (4, 1), (6, 3), (7, 1), (9, 2), (12, 4), (15, 2)],
         [(1, 1), (3, 2), (5, 2), (8, 3), (10, 1), (11, 3), (13, 3), (16, 1)]]
LUFT = (HIMMEL, HECKE, HECKE_HELL)


def flocken(bild, f):
    """Wenige Flocken; sie fallen nur vor Himmel und Hecke und enden auf Laub, Schnee oder Boden."""
    for start, x, tempo, phase in FLOCKEN:
        t = f - start
        if t < 0:
            continue
        y = int(t * tempo)
        x += round(math.sin((t + phase) / 8))
        c = x - X0
        if y < (oberkante(c, f) if 0 <= c < 32 else BODEN_Y) and bild.hole(x, y) in LUFT:
            bild.setze(x, y, FLOCKE)


def wind(bild, f):
    """Schneefahne vor dem Windstoß."""
    if not WIND <= f < WIND + 20:
        return
    front = windfront(f)
    for dx, dy in FAHNE[f % 2]:
        x = front + dx
        c = x - X0
        y = (oberkante(c, f) if 0 <= c < 32 else BODEN_Y) - dy
        if 0 <= x < B and bild.hole(x, y) in LUFT:
            bild.setze(x, y, STAUB)


def bilder():
    liste = []
    for f in range(RUNDE):
        bild = Bild()
        landschaft(bild, f)
        haufen(bild, f)
        igel(bild, f)
        blasen(bild, f)
        blatt(bild, f)
        flocken(bild, f)
        wind(bild, f)
        liste.append(bild)
    return liste
