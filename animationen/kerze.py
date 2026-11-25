"""Kerzenlicht: eine dicke rote Kerze brennt ruhig auf einem Tannenkranz – 255 Bilder.

Die Flamme wiegt sich sanft und atmet (mal höher, mal niedriger); ihr warmer Schein auf der Wand,
auf dem Kranz und an den Fensterrahmen atmet mit. Zweimal in der Runde zuckt die Flamme, wird
klein, und ein dünner Rauchfaden steigt auf; zweimal läuft ein Wachstropfen an der Kerze herab
und erstarrt. Links und rechts ein dunkles Fenster, hinter dem Schnee fällt. Kein Text.
Die Kerze wird nicht kürzer, alle Bewegungen gehen in 255 Bildern auf, Zucken und Tropfen liegen
ganz innerhalb der Runde – sie schließt ohne Sprung.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild
wird einzeln und spaltenweise komprimiert; eine Spalte, die einer früheren gleicht, kostet fast
nichts, jede neue etwa 10 Bytes. Darum: Kerze aus gleichen Spalten, der Kranz vor der Kerze flach,
Tannengrün als Kachel aus drei Spalten und spiegelgleich zur Kerzenmitte, Beeren im Raster der
Kachel, der Kranz überall gleich hell, der Schein in wenigen festen Stufen, eine kleine Flamme,
wenige Flocken (Zapfen und ein Lichtfleck auf dem Kranz waren zu teuer).
"""
import math

from basis import Bild, dimmen, mischen

NAME = "kerze"
TITEL = "Kerzenlicht"

RUNDE = 255
WAND = (10, 4, 3)                              # warmes Dunkel
CX = 32                                        # Mitte der Kerze (Docht)
KX, KB = 28, 9                                 # linke Kante und Breite der Kerze
OBEN = 5                                       # oberste Zeile der Kerze

# Kerze
ROT_K = (190, 0, 25)
RAND_K = (120, 0, 18)                          # Rundung: dunklere Kanten
SAUM = (255, 120, 40)                          # geschmolzener Rand, leuchtet vom Feuer
WARM_K, WARM_K2 = (235, 40, 25), (212, 14, 25)  # zwei Zeilen darunter, noch angestrahlt
LICHT_K = [0.45, 0.7, 0.88, 0.94, 1.0]         # wie stark Saum und Zeilen leuchten, je Flammenhöhe 0…4
TROPF_HELL, TROPF = (255, 170, 120), (255, 80, 60)

# Flamme
KERN, GELB_F, ORANGE_F, SPITZE = (255, 250, 200), (255, 215, 50), (255, 125, 0), (235, 60, 0)
RAUCH = (130, 130, 150)

# Schein auf der Wand: zwei Ringe um die Flamme, Radien (waagerecht, senkrecht) je Flammenhöhe 0…4
SCHEIN_INNEN, SCHEIN_AUSSEN = (84, 34, 8), (42, 17, 4)
SCHEIN_TIEF = 14                               # senkrechter Radius des äußeren Rings unterhalb der Flamme
RADIEN = [((2.6, 1.6), (4.6, 2.8)), ((3.6, 2.4), (6.2, 3.8)), ((4.6, 3.0), (7.6, 4.6)),
          ((5.0, 3.3), (8.3, 5.0)), ((5.6, 3.6), (9.0, 5.4))]

# Kranz: Tannengrün als Kachel aus drei Spalten (A B C B), Zeilen 11–15, spiegelgleich zur Kerzenmitte
KRANZ_HALB = 17                                # so viele Spalten links und rechts der Mitte
SPALTE = {"A": "mlmdd", "B": ".mdld", "C": "..lmd"}
KACHEL = "ABCB"
ENDE = ("...md", "..lmd")                      # runde Enden
VORN = "...md"                                 # vor der Kerze: flach, alle Spalten gleich
NADEL = {"d": (0, 60, 14), "m": (0, 120, 22), "l": (20, 180, 40)}
BEEREN = [20, 24, 40, 44]                      # rote Beeren 2×2, im Raster der Kachel (gleiche Spaltenfolge)
BEERE = (255, 0, 0)

# Fenster: Rahmen, Kreuz, Nachtblau, Schnee auf dem Sims
FENSTER = [2, 52]                              # linke Kante, 11 breit
RAHMEN, RAHMEN_HELL = (80, 40, 14), (170, 85, 28)
NACHT = (0, 8, 46)
FLOCKE = (200, 210, 240)
SIMS_SCHNEE = (140, 150, 190)
# Flocken je Fenster: Spalte im Fenster, Startzeile, Durchläufe je Runde (ganze Zahl: schließt ohne Sprung)
FLOCKEN = [[(2, 0, 5), (8, 3, 6), (4, 7, 8)], [(7, 2, 5), (1, 5, 6), (3, 9, 8)]]
FALLHOEHE = 10                                 # Zeilen 1–10: hinter Rahmen, Kreuz und Sims verdeckt

# Ereignisse
ZUCKEN = [48, 150]                             # hier zuckt die Flamme (am Ende eines Ausatmens), danach Rauch
ZUCK = [(2, -1), (1, 1), (1, -1), (0, 0), (1, 0), (1, 0), (1, 1), (1, 0), (1, 0), (2, 0),
        (2, -1), (3, 0), (4, 0), (3, 0)]       # (Höhe, Neigung), je zwei Bilder
TROPFEN = [(92, 30), (194, 34)]                # Start, Spalte
TROPF_WEG = [8, 13, 18, 24, 31, 39]            # ab diesem Bild eine Zeile tiefer
TROPF_DAUER = 56


def _flammenfolge():
    """(Höhe 0…4, Neigung −1…1) der Flamme für jedes Bild: Sie atmet (fünf Atemzüge je Runde) und
    wiegt sich; ganze Schwingungen je Runde, darum ohne Sprung. Neigungen, die nur ein oder zwei
    Bilder dauern würden, entfallen (kein Zittern). Bei ZUCKEN liegt die feste Folge ZUCK darüber
    (sie beginnt und endet auf der Höhe, die der Atem dort gerade hat)."""
    hoehen, neigungen = [], []
    for f in range(RUNDE):
        atem = math.sin(2 * math.pi * 5 * f / RUNDE)
        wiegen = math.sin(2 * math.pi * 7 * f / RUNDE) + 0.5 * math.sin(2 * math.pi * 16 * f / RUNDE + 1)
        hoehen.append(4 if atem > 0.4 else 3 if atem > -0.4 else 2)
        neigungen.append(-1 if wiegen < -0.8 else 1 if wiegen > 0.8 else 0)
    for f in range(RUNDE):                                           # Ausschläge unter drei Bildern glätten
        if neigungen[f] != neigungen[f - 1] and len({neigungen[(f + k) % RUNDE] for k in range(3)}) > 1:
            neigungen[f] = neigungen[f - 1]
    folge = list(zip(hoehen, neigungen))
    for start in ZUCKEN:
        for k, zustand in enumerate(ZUCK):
            folge[start + 2 * k] = folge[start + 2 * k + 1] = zustand
    return folge


def schein(bild, hoehe):
    """Warmer Hof um die Flamme, nur auf der Wand; wächst und schrumpft mit der Flamme.
    Der äußere Ring ist nach unten lang gezogen und reicht neben der Kerze bis hinter den Kranz:
    die Tannenspitzen stehen dort vor warmem Licht (kostet nicht mehr als ein runder Hof)."""
    (ix, iy), (ax, ay) = RADIEN[hoehe]
    for y in range(0, 14):
        for x in range(CX - 10, CX + 11):
            if bild.hole(x, y) != WAND:
                continue
            dx, dy = x - CX, y - 3
            if (dx / ix) ** 2 + (dy / iy) ** 2 <= 1:
                bild.setze(x, y, SCHEIN_INNEN)
            elif (dx / ax) ** 2 + (dy / (ay if dy < 0 else SCHEIN_TIEF)) ** 2 <= 1:
                bild.setze(x, y, SCHEIN_AUSSEN)


def flamme(bild, hoehe, neigung):
    """Tropfenförmige Flamme über dem Docht; unterste Zeile mit weißem Kern."""
    y = OBEN - 1
    if hoehe == 0:                                                   # fast aus
        bild.setze(CX, y, GELB_F)
        return
    bild.setze(CX - 1, y, ORANGE_F)
    bild.setze(CX, y, KERN)
    bild.setze(CX + 1, y, ORANGE_F)
    if hoehe == 1:                                                   # klein
        bild.setze(CX + neigung, y - 1, ORANGE_F)
        return
    bild.setze(CX, y - 1, GELB_F)
    if hoehe == 2:                                                   # schlank
        bild.setze(CX + neigung, y - 2, ORANGE_F)
        return
    bild.setze(CX - 1, y - 1, ORANGE_F)
    bild.setze(CX + 1, y - 1, ORANGE_F)
    if hoehe == 3:                                                   # voll
        bild.setze(CX + neigung, y - 2, ORANGE_F)
        return
    bild.setze(CX, y - 2, GELB_F)                                    # hoch
    bild.setze(CX + neigung, y - 3, SPITZE)


def rauch(bild, f):
    """Dünner Rauchfaden über der klein gewordenen Flamme: steigt, biegt ab und verblasst."""
    for start in ZUCKEN:
        t = f - start - 7
        for k in range(3):
            a = t - k * 3
            if 0 <= a < 9:
                y = 2 - a // 3
                bild.setze(CX + (0, 1, 0)[y] - (1 if k == 2 else 0), y, dimmen(RAUCH, (1.0, 0.7, 0.45)[2 - y]))


def kerze(bild, f, hoehe):
    """Dicke Kerze: alle inneren Spalten gleich; oben der leuchtende Saum und zwei angestrahlte
    Zeilen, die mit der Flamme heller und dunkler werden. Ab und zu läuft ein Tropfen herab."""
    licht = LICHT_K[hoehe]
    bild.rechteck(KX, OBEN, KB, 16 - OBEN, ROT_K)
    bild.rechteck(KX, OBEN, 1, 16 - OBEN, RAND_K)
    bild.rechteck(KX + KB - 1, OBEN, 1, 16 - OBEN, RAND_K)
    for k, farbe in enumerate((SAUM, WARM_K, WARM_K2)):
        bild.rechteck(KX + 1, OBEN + k, KB - 2, 1, mischen(ROT_K, farbe, licht))
    for start, x in TROPFEN:                                         # sammelt sich am Saum, läuft, erstarrt
        t = f - start
        if 0 <= t < TROPF_DAUER:
            y = OBEN + sum(1 for w in TROPF_WEG if t >= w)
            kalt = round(min(1.0, max(0, t - 40) / 16) * 4) / 4      # unten wird er in vier Stufen kerzenrot
            bild.setze(x, y, mischen(TROPF_HELL, ROT_K, kalt))
            if y > OBEN:
                bild.setze(x, y - 1, mischen(TROPF, ROT_K, kalt))


def kranz(bild, hell):
    """Tannenkranz, überall gleich hell (hell = 0…1 mit dem Atem der Flamme): ein Lichtfleck
    nur nahe der Kerze würde die Spalten ungleich machen und zu viel Speicher kosten.
    Vor der Kerze liegt der vordere Bogen des Kranzes flach (zwei Zeilen, alle Spalten gleich)."""
    f = 0.7 + 0.35 * hell
    for d in range(KRANZ_HALB + 1):
        rand = KRANZ_HALB - d
        spalte = ENDE[rand] if rand < 2 else VORN if d < KB // 2 else SPALTE[KACHEL[d % 4]]
        for dy, c in enumerate(spalte):
            if c != ".":
                farbe = dimmen(NADEL[c], f)
                farbe = mischen(farbe, (255, 120, 0), 0.12) if dy < 2 else farbe
                bild.setze(CX - d, 11 + dy, farbe)
                bild.setze(CX + d, 11 + dy, farbe)
    for x in BEEREN:
        bild.rechteck(x, 13, 2, 2, BEERE)


def fenster(bild, x0, f, flocken, kerze_rechts, hell):
    """Dunkles Fenster mit Kreuz, 11 breit, Zeilen 1–11; draußen fällt Schnee. Die Rahmenkante
    zur Kerze hin fängt deren Licht (hell = 0…1)."""
    bild.rechteck(x0, 1, 11, 11, RAHMEN)
    for dx in (1, 6):
        bild.rechteck(x0 + dx, 2, 4, 4, NACHT)
        bild.rechteck(x0 + dx, 7, 4, 4, NACHT)
    bild.rechteck(x0 + 10 if kerze_rechts else x0, 1, 1, 11, dimmen(RAHMEN_HELL, 0.6 + 0.4 * hell))
    for dx, start, runden in flocken:
        y = 1 + (start * RUNDE + f * runden * FALLHOEHE) // RUNDE % FALLHOEHE
        if bild.hole(x0 + dx, y) == NACHT:
            bild.setze(x0 + dx, y, FLOCKE)
    for dx in (1, 2, 3, 4, 6, 7, 8, 9):                              # Schnee liegt auf dem Sims
        bild.setze(x0 + dx, 10, SIMS_SCHNEE)


def bilder():
    liste = []
    folge = _flammenfolge()
    for f in range(RUNDE):
        bild = Bild(WAND)
        hoehe, neigung = folge[f]
        fenster(bild, FENSTER[0], f, FLOCKEN[0], True, hoehe / 4)
        fenster(bild, FENSTER[1], f, FLOCKEN[1], False, hoehe / 4)
        kerze(bild, f, hoehe)
        kranz(bild, hoehe / 4)
        schein(bild, hoehe)
        flamme(bild, hoehe, neigung)
        rauch(bild, f)
        liste.append(bild)
    return liste
