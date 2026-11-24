"""Glücksschwein: Ein großes rosa Schwein mit Zylinder, Schlappohr, Ringelschwanz und einem
vierblättrigen Kleeblatt im Maul hüpft in fünf Sätzen von links nach rechts über die Matrix. Bei
jeder Landung springen goldene Taler auf, wenig Konfetti und drei Luftschlangen regnen herab, ein
Kleeblatt-Wirbel fliegt kurz durchs Bild. Rechts verbeugt es sich, dreht um und tanzt in kleinen
Hopsern (mit einer Pirouette in der Mitte) zurück; links dreht es wieder, lüftet den Hut und nimmt
Anlauf – die Runde geht ohne Sprung in sich über. 255 Bilder, kein Text.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum schwarzer Grund, ein Schwein mit vielen gleichen
Nachbarspalten, nur sieben Konfettistücke (senkrecht, eine Spalte breit), Luftschlangen über zwei
Spalten und Taler nur kurz nach jeder Landung. Alle Fallzeiten teilen 255, darum schließt die Runde.
"""
import math

from basis import B, BLAU, GELB, GOLD, HELLBLAU, LILA, ORANGE, PINK, ROT, TUERKIS, Bild

NAME = "gluecksschwein"
TITEL = "Glücksschwein tanzt im Konfetti"

ROSA = (255, 110, 160)
OHR = (225, 40, 110)                           # Schlappohr und Ringelschwanz
RUESSEL = (255, 170, 200)
NASE = (150, 20, 70)
AUGE = (25, 0, 20)
HUF = (200, 60, 110)
KLEE = (0, 200, 40)
KLEE_DUNKEL = (0, 110, 20)
FARBEN = {"p": ROSA, "e": OHR, "t": OHR, "n": RUESSEL, "o": NASE, "k": AUGE, "h": HUF, "d": HUF,
          "z": BLAU, "g": GOLD, "C": KLEE, "c": KLEE_DUNKEL}

BREITE = 24                                    # Schwein mit Schwanz und Kleeblatt, Blick nach rechts
RUMPF = [".....ppppppppeeppp......",          # acht Zeilen, darüber der Hut, darunter die Beine
         "....pppppppppeeeppp.....",
         "...ppppppppppeeepkpnnn..",
         "...pppppppppppeeppnnon..",
         "...pppppppppppppppnnnn..",
         "...ppppppppppppppppp....",
         "...pppppppppppppppp.....",
         "....pppppppppppppp......"]
HUT = ["zzzz", "gggg", "zzzzzz"]               # kleiner Zylinder mit goldenem Band; Krempe ab Spalte 13
SCHWANZ = [[".tt", "t..", ".tt"], ["tt.", "..t", ".tt"]]             # Ringelschwanz wackelt
KLEEBLATT = ["CC.CC", "CCcCC", ".ccc.", "CCcCC", "CC.CC"]            # hängt unter dem Rüssel
# Beine: (Spalte, Zeile, Zeilen) – die beiden vorderen Beine hell, die hinteren (d) dunkler daneben
BEINE = {"steht": ((4, 11, ["ppp.dd", "hhh.dd"]), (12, 11, ["ppp.dd", "hhh.dd"])),
         "sprung": ((2, 11, [".ppp..dd", "hhh....."]), (12, 11, ["ppp.dd", ".hhh.."])),
         "duckt": ((4, 12, ["hhh.dd"]), (12, 12, ["hhh.dd"])),
         "hinten": ((4, 11, ["hhh.dd", "....dd"]), (12, 11, ["ppp.dd", "hhh..."])),   # Bein hinten gehoben
         "vorn": ((4, 11, ["ppp.dd", "hhh..."]), (12, 11, ["hhh.dd", "....dd"])),     # Bein vorn gehoben
         "kniet": ((4, 11, ["ppp.dd", "hhh.dd"]), (12, 12, ["hhh.dd"]))}             # bei der Verbeugung
# von vorn (beim Umdrehen), 14 breit ab Spalte 5; von hinten dasselbe ohne Gesicht, mit Ringelschwanz
VORN = [".....zzzz.....",
        ".....gggg.....",
        "....zzzzzz....",
        ".eeppppppppee.",
        "eeeppppppppeee",
        "eeppkppppkppee",
        ".pppnnnnnnppp.",
        ".pppnonnonppp.",
        ".pppnnnnnnppp.",
        ".pppppppppppp.",
        "..pppppppppp..",
        "..ppp....ppp..",
        "..hhh....hhh.."]
HINTEN = [z.translate(str.maketrans("kno", "ppp")) for z in VORN]

X_LINKS, X_RECHTS = 0, B - BREITE - 3          # linke Kante des Schweins; rechts Platz für die Verbeugung
HUEPFER, JE_HUEPFER, FLUG = 5, 20, 12          # hin: fünf große Hüpfer
HOPSER, JE_HOPSER, HOPS_FLUG = 8, 10, 6        # zurück: acht kleine Hopser, in der Mitte eine Pirouette
RECHTS_AN = HUEPFER * JE_HUEPFER               # 100: steht rechts, verbeugt sich, dreht um
ZURUECK = 128                                  # tanzt zurück
PIROUETTE = ZURUECK + 4 * JE_HOPSER            # 168: 20 Bilder Drehsprung
LINKS_AN = ZURUECK + (HOPSER + 2) * JE_HOPSER  # 228: steht links, dreht um

# Konfetti und Luftschlangen: Spalte, Fallzeit (teilt 255), Versatz, Farbe
KONFETTI = [(5, 85, 0, ROT), (13, 51, 30, HELLBLAU), (22, 85, 50, GELB), (31, 51, 44, TUERKIS),
            (40, 85, 22, PINK), (49, 51, 10, GELB), (59, 85, 70, HELLBLAU)]
SCHLANGEN = [(9, 85, 48, TUERKIS), (27, 85, 20, ORANGE), (53, 85, 76, LILA)]
WIRBEL = [(28, -1), (184, 1)]                  # Start, Richtung des Kleeblatt-Wirbels
WIRBEL_DAUER = 38


def stand(f):
    """Wo das Schwein im Bild f ist: x, Höhe über dem Boden, Blick (r, l, v = von vorn,
    h = von hinten), Beine, Neigung bei der Verbeugung (0–2), Hut hebt ab (0/1)."""
    if f < RECHTS_AN:                                              # große Hüpfer nach rechts
        k, t = divmod(f, JE_HUEPFER)
        weg = (X_RECHTS - X_LINKS) / HUEPFER
        if t <= FLUG:
            hoch = round(3.4 * math.sin(math.pi * t / FLUG))
            return (X_LINKS + round(weg * (k + t / FLUG)), hoch, "r", "sprung" if hoch else "steht", 0,
                    1 if t in (9, 10, 11) else 0)                  # im Fallen hebt der Hut kurz ab
        beine = "duckt" if t in (FLUG + 1, FLUG + 2, JE_HUEPFER - 1) else "steht"
        return X_LINKS + round(weg * (k + 1)), 0, "r", beine, 0, 0
    if f < ZURUECK:                                                # rechts: Verbeugung, dann umdrehen
        t = f - RECHTS_AN
        neigung = 0 if t < 3 or t >= 17 else (1 if t < 5 or t >= 15 else 2)
        if 20 <= t <= 22:                                          # dreht sich im kleinen Hüpfer
            return X_RECHTS, (1, 2, 1)[t - 20], "v", "steht", 0, 0
        return X_RECHTS, 0, "r" if t < 20 else "l", "duckt" if t in (19, 23, 27) else "steht", neigung, 0
    if f < LINKS_AN:                                               # kleine Hopser nach links
        k, t = divmod(f - ZURUECK, JE_HOPSER)
        weg = (X_RECHTS - X_LINKS) / HOPSER
        if PIROUETTE <= f < PIROUETTE + 2 * JE_HOPSER:             # Drehsprung auf der Stelle
            t = f - PIROUETTE
            x = X_RECHTS - round(weg * 4)
            if 2 <= t < 14:
                hoch = round(3.4 * math.sin(math.pi * (t - 2) / 12))
                return x, hoch, "lllvvvrrrhhh"[t - 2], "sprung" if hoch else "steht", 0, 0
            return x, 0, "l", "duckt" if t in (0, 1, 15, 16, 19) else "steht", 0, 0
        if k >= 4:
            k -= 2
        if t <= HOPS_FLUG:
            hoch = round(2.3 * math.sin(math.pi * t / HOPS_FLUG))
            beine = ("hinten", "vorn")[k % 2] if hoch else "steht"
            return X_RECHTS - round(weg * (k + t / HOPS_FLUG)), hoch, "l", beine, 0, 1 if t in (4, 5) else 0
        return X_RECHTS - round(weg * (k + 1)), 0, "l", "steht", 0, 0
    t = f - LINKS_AN                                               # links: umdrehen, Anlauf nehmen
    if 9 <= t <= 11:
        return X_LINKS, (1, 2, 1)[t - 9], "v", "steht", 0, 0
    hut = (1, 2, 2, 2, 1)[t - 16] if 16 <= t <= 20 else 0           # lüftet den Hut, dann Anlauf
    return X_LINKS, 0, "l" if t < 9 else "r", "duckt" if t in (8, 12, 25, 26) else "steht", 0, hut


def schwein(bild, f):
    x0, hoch, blick, beine, neigung, hut = stand(f)
    duckt = 1 if beine == "duckt" else 0
    pixel = {}

    def teil(zeilen, dx, dy, kippt=False):
        for j, zeile in enumerate(zeilen):
            for i, c in enumerate(zeile):
                if c != ".":
                    # Verbeugung: der Kopf sinkt in zwei Stufen
                    senke = min(neigung, 0 if dx + i < 8 else (1 if dx + i < 12 else 2)) if kippt else 0
                    pixel[(dx + i, dy + j + senke)] = FARBEN[c]

    if blick in "vh":                                              # von vorn oder von hinten
        teil(VORN if blick == "v" else HINTEN, 5, 0)
        if blick == "v":
            teil(KLEEBLATT, 10, 8)
        else:
            teil(SCHWANZ[0], 10, 6)
    else:
        teil(RUMPF, 0, 3 + duckt, True)
        teil(SCHWANZ[(f // 5) % 2], 0, 4 + duckt)
        teil(HUT[:2], 14 + neigung // 2, duckt - hut + neigung)
        teil(HUT[2:], 13 + neigung // 2, 2 + duckt - hut + neigung)
        teil(KLEEBLATT, 19 + (0, 2, 3)[neigung], 8 + duckt)
        for spalte, zeile, zeilen in BEINE["kniet" if neigung == 2 else beine]:
            teil(zeilen, spalte, zeile)
        if f % 60 in (40, 41):                                     # blinzelt
            pixel[(17, 5 + duckt)] = ROSA
    for (i, j), farbe in pixel.items():
        bild.setze(x0 + (BREITE - 1 - i if blick == "l" else i), 3 - hoch + j, farbe)


def landungen():
    """Für jede Landung: Bild, linke Kante des Schweins, Seiten (-1 links, 1 rechts), Zahl der Taler."""
    for k in range(HUEPFER):
        f = k * JE_HUEPFER + FLUG
        yield f, stand(f)[0], (-1,), 2
    for k in range(HOPSER):
        f = ZURUECK + (k + (2 if k >= 4 else 0)) * JE_HOPSER + HOPS_FLUG
        yield f, stand(f)[0], (1,), 1
    yield PIROUETTE + 14, stand(PIROUETTE)[0], (-1, 1), 2


def taler(bild, f):
    """Bei jeder Landung springen hinter dem Schwein Taler auf und drehen sich im Flug."""
    for start, x0, seiten, anzahl in landungen():
        for seite in seiten:
            for n in range(anzahl):
                weite, hoehe = ((0.5, 9), (1.0, 6))[(n + start // 10) % 2]
                t = f - start - 2 * n                              # der zweite Taler kommt etwas später
                if not 0 <= t <= 14:
                    continue
                dx = 2 + weite * t
                x = round(x0 + BREITE + dx) if seite > 0 else round(x0 - 1 - dx)
                y = round(15 - hoehe * math.sin(math.pi * t / 14))   # aus dem Boden und wieder hinein
                if (t // 3) % 2:                                   # Kante: nur ein Strich
                    bild.rechteck(x, y - 1, 1, 3, GOLD)
                else:
                    bild.rechteck(x - 1, y - 1, 3, 3, GOLD)
                    bild.setze(x, y, GELB)


def konfetti(bild, f):
    for x, zeit, versatz, farbe in KONFETTI:
        t = (f + versatz) % zeit
        y = round(t * 19 / zeit) - 2
        dx = (0, 1, 0, -1)[(t // 8) % 4]                           # trudelt
        bild.rechteck(x + dx, y, 1, 2 if (t // 5) % 2 else 1, farbe)
    for x, zeit, versatz, farbe in SCHLANGEN:                      # Luftschlange: geschwungenes Band
        t = (f + versatz) % zeit
        y = round(t * 26 / zeit) - 9
        for k in range(8):
            bild.setze(x + ((k + t // 5) // 2) % 2, y + k, farbe)


def wirbel(bild, f):
    """Vier kleine Kleeblätter kreisen umeinander und ziehen einmal quer durchs Bild."""
    for start, richtung in WIRBEL:
        t = f - start
        if not 0 <= t < WIRBEL_DAUER:
            continue
        mitte = -6 + (B + 12) * t / (WIRBEL_DAUER - 1)
        if richtung < 0:
            mitte = B - 1 - mitte
        for k in range(4):
            w = t * 0.42 * richtung + k * math.pi / 2
            x, y = round(mitte + 5 * math.cos(w)), round(7.5 + 5 * math.sin(w))
            if (t // 3 + k) % 2:
                for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                    bild.setze(x + dx, y + dy, KLEE)
            else:
                for dx, dy in ((0, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)):
                    bild.setze(x + dx, y + dy, KLEE)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild()
        konfetti(bild, f)
        wirbel(bild, f)
        taler(bild, f)
        schwein(bild, f)
        liste.append(bild)
    return liste
