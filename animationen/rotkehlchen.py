"""Rotkehlchen im Schnee: Ein verschneiter Zweig zieht sich quer durchs Bild, dahinter ein ruhiger
Winterhimmel am frühen Morgen mit blassem Mond und roten Beeren am Seitenzweig. Ein Rotkehlchen
sitzt darauf, plustert sich auf, singt (bunte Noten steigen auf), schüttelt sich, dass der Schnee
vom Zweig rieselt, hüpft ein Stück entlang, fliegt auf, zieht einen kleinen Bogen und landet wieder
an seinem Platz. Ein zweites Rotkehlchen kommt dazu, beide sitzen Schnabel an Schnabel, singen sich
an und plustern sich auf; zum Rundenende fliegt das zweite wieder fort. Anfang und Ende zeigen
dasselbe Bild – 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Himmel in waagerechten Streifen (gleiche Spalten), der
Zweig aus waagerechten Stücken mit wenigen Stufen (das dicke Ende links sieht aus wie die Gabel
rechts – gleiche Spalten), Beeren als Paare, kein Schneefall – nur ein paar Krümel, wenn sich der
Vogel schüttelt, hüpft oder landet. Die Brust ist mit Absicht leuchtend orange (ein Rotkehlchen
ist so), Rücken und Zweig dagegen sehr dunkel, damit sie auf den LEDs braun bleiben.
"""
from basis import B, GELB, HELLGRUEN, PINK, SCHWARZ, TUERKIS, Bild

NAME = "rotkehlchen"
TITEL = "Rotkehlchen im Schnee"

# früher Morgen: je Zeile eine Farbe, in deutlichen Stufen (gedämpft, damit die Brust leuchtet);
# ganz unten ein Hauch Morgenrot
HIMMEL = [(10, 22, 66)] * 4 + [(16, 34, 90)] * 5 + [(26, 48, 110)] * 5 + [(54, 50, 114)] * 2
MOND = (200, 195, 150)                         # blass, geht gerade unter
BEERE = (255, 0, 30)
KANTE = (215, 225, 250)                        # Schneeauflage
HOLZ = (66, 30, 4)                             # Oberseite des Zweigs
BORKE = (33, 11, 0)                            # Unterseite
KRUEMEL = (235, 240, 255)                      # rieselnder Schnee
RUECKEN = (62, 42, 8)                          # olivbraun, dunkel gehalten
FLUEGEL = (86, 56, 12)
BAUCH = (165, 155, 145)                        # gedämpft, sonst verschmilzt er mit dem Schnee
SCHNABEL = (200, 160, 60)
BEIN = (80, 45, 20)
VOGEL_1 = {"r": RUECKEN, "t": RUECKEN, "f": FLUEGEL, "o": (255, 85, 0), "a": SCHWARZ, "k": SCHNABEL,
           "w": BAUCH, "l": BEIN}
VOGEL_2 = {**VOGEL_1, "o": (255, 55, 0)}       # das zweite eine Spur röter
NOTEN = [GELB, PINK, TUERKIS, HELLGRUEN]

SCHNEE_Y = 11                                  # Schneeauflage im Bereich der Vögel; Holz in 12 und 13
FUSS = SCHNEE_Y - 1                            # Zeile der Beine
X0 = 19                                        # Stammplatz des ersten Rotkehlchens (linke Spalte der Figur)
X2 = X0 + 10                                   # Platz des zweiten, Schnabel an Schnabel

# Figuren (Blick nach rechts): r Rücken, t Schwanz, f Flügel, o Brust, a Auge, k Schnabel, w Bauch, l Bein
SITZT = ["...rrrr.",
         "..rroaok",
         ".rrrooo.",
         ".rrrooo.",
         "ttrrooo.",
         "..rwww..",
         "...l.l.."]
WIPPT = ["...rrrr.",                           # Schwanz zuckt hoch
         "..rroaok",
         ".rrrooo.",
         "ttrrooo.",
         ".rrrooo.",
         "..rwww..",
         "...l.l.."]
HALB = ["...rrrr.",                            # halb aufgeplustert
        "..rroaok",
        ".rrroooo",
        ".rrroooo",
        "ttrroooo",
        "..rwwww.",
        "...l.l.."]
PLUSTER = ["..rrrrr.",                         # Federkugel, die Beine verschwinden
           ".rrroaok",
           "rrrroooo",
           "rrrroooo",
           "rrrroooo",
           "trrwwww.",
           "..rwww.."]
SINGT_ZU = ["...rrrr.",                        # gereckt
            "..rroaok",
            "..rrooo.",
            ".rrrooo.",
            ".rrrooo.",
            "ttrrooo.",
            "..rwww..",
            "...l.l.."]
SINGT_AUF = ["...rrrrk",                       # Schnabel weit offen
             "..rroao.",
             "..rroook",
             ".rrrooo.",
             ".rrrooo.",
             "ttrrooo.",
             "..rwww..",
             "...l.l.."]
FLUG_AUF = ["..ff.....",                        # Flügel oben
            "..fffrrr.",
            "ttrrroaok",
            ".rrroooo.",
            "..wwooo..",
            ".........",
            "........."]
FLUG_MITTE = [".........",                      # Flügel am Rücken
              ".....rrr.",
              "ttfffoaok",
              ".rrfoooo.",
              "..wwooo..",
              ".........",
              "........."]
FLUG_AB = [".........",                         # Flügel unten
           ".....rrr.",
           "ttrrroaok",
           ".rffoooo.",
           "..fffoo..",
           "..ff.....",
           "........."]
FLUEGELSCHLAG = [FLUG_AUF, FLUG_MITTE, FLUG_AB, FLUG_MITTE]
NOTE = [".n", ".n", "nn"]

# Ablauf (Bildnummern)
PLUSTERT, SINGT, SCHUETTELT, RUHT = 8, 28, 82, 102
STROPHE, GESANG = 27, 22                       # je Strophe 22 Bilder singen, 5 Luft holen
HUEPFER = (106, 115, 124)                      # drei Hüpfer nach rechts, je vier Spalten
FLUG_VON, FLUG_BIS = 134, 166                  # auf, kleiner Bogen, zurück auf den Stammplatz
DREHT = 174                                    # merkt das zweite und dreht sich ihm zu
KOMMT, DA, FORT, WEG = 170, 188, 236, 252      # das zweite Rotkehlchen
ZWEI_SINGT, EINS_ANTWORTET, KUSCHELN = (192, 204), (206, 218), (219, 233)

# Noten: Start, x, Farbe, Drift je Bild (setzt erst über den Köpfen ein)
NOTENPLAN = ([(s, X0 + 9, NOTEN[i % 4], 0.45) for i, s in enumerate((30, 38, 46, 57, 65, 73))]
             + [(193, X2 - 2, NOTEN[1], 0.4), (200, X2 - 2, NOTEN[2], 0.4),       # das zweite: nach rechts
                (207, X0 + 8, NOTEN[0], -0.4), (214, X0 + 8, NOTEN[3], -0.4)])     # die Antwort: nach links
# Schneekrümel: Start, Spalte
KRUEMELPLAN = ([(SCHUETTELT + s, X0 + dx) for s, dx in ((1, 1), (3, 6), (4, -3), (6, 10), (7, 3), (9, -1),
                                                        (11, 8), (12, 5), (14, -4), (15, 12), (17, 0),
                                                        (19, 7))]
               + [(h + 6, X0 + 4 * (i + 1) + 2) for i, h in enumerate(HUEPFER)]
               + [(FLUG_VON, X0 + 15), (FLUG_BIS, X0 + 2), (FLUG_BIS + 2, X0 + 5),
                  (DA, X2 + 3), (DA + 2, X2 + 6), (FORT, X2 + 2), (FORT + 2, X2 + 5)])


def kulisse(bild):
    for y in range(16):
        bild.rechteck(0, y, B, 1, HIMMEL[y])
    bild.rechteck(5, 1, 2, 4, MOND)                                  # kleiner Mond: zwei gleiche Spalten …
    bild.rechteck(4, 2, 4, 2, MOND)                                  # … und zwei gleiche Ränder
    # Hauptast: Schnee, Holz, Borke; rechts ab Spalte 46 nur noch ein dünner Zweig eine Zeile tiefer
    bild.rechteck(0, SCHNEE_Y, 46, 1, KANTE)
    bild.rechteck(0, SCHNEE_Y + 1, 46, 1, HOLZ)
    bild.rechteck(46, SCHNEE_Y + 1, B - 46, 1, KANTE)
    bild.rechteck(0, SCHNEE_Y + 2, B, 1, BORKE)
    # links das dicke Ende (kommt vom Stamm) mit dickerem Schnee
    bild.rechteck(0, SCHNEE_Y, 10, 1, HOLZ)
    bild.rechteck(0, SCHNEE_Y - 1, 10, 1, KANTE)
    bild.rechteck(0, SCHNEE_Y - 2, 5, 1, KANTE)
    # rechts die Gabel: der obere Zweig steigt in drei Stufen, jede mit Schneeauflage
    bild.rechteck(38, SCHNEE_Y - 1, 3, 1, KANTE)                     # Schneepolster in der Gabel
    bild.rechteck(12, SCHNEE_Y - 1, 3, 1, KANTE)                     # … und eins links vom Stammplatz
    for x0, x1, y in ((41, 47, 11), (48, 54, 10), (55, 60, 9)):
        bild.rechteck(x0, y, x1 - x0 + 1, 1, HOLZ)
        bild.rechteck(x0, y - 1, x1 - x0 + 1, 1, KANTE)
    # rote Beeren hängen am oberen Zweig, paarweise (gleiche Nachbarspalten)
    bild.rechteck(57, 10, 2, 2, BEERE)
    bild.rechteck(50, 11, 2, 1, BEERE)


def bezier(p0, p1, p2, p3, a):
    b = 1 - a
    return tuple(b ** 3 * p0[i] + 3 * b * b * a * p1[i] + 3 * b * a * a * p2[i] + a ** 3 * p3[i]
                 for i in (0, 1))


def vogel(bild, x, fuss, pose, links, farben):
    """Zeichnet die Figur so, dass ihre unterste Zeile in der Zeile `fuss` liegt."""
    bild.figur(round(x), round(fuss) - len(pose) + 1, pose, farben, spiegeln=links)


def ruht(f, versatz=0):
    """Sitzen mit gelegentlichem Schwanzzucken."""
    return WIPPT if (f + versatz) % 23 in (3, 4) else SITZT


def singt(f, start):
    return SINGT_AUF if ((f - start) // 3) % 2 == 0 else SINGT_ZU


# Flug des ersten: vom Ende der Hüpfer auf, herum und zurück auf den Stammplatz
BOGEN = ((X0 + 12, FUSS), (X0 + 28, 4), (X0 + 1, 2), (X0, FUSS))


def erstes(f):
    """Das erste Rotkehlchen: (x, Fußzeile, Figur, Blick nach links)."""
    if f < PLUSTERT or f >= WEG:
        return X0, FUSS, ruht(f), False
    if f < SINGT:                                                    # plustert sich auf
        return X0, FUSS, HALB if f < PLUSTERT + 2 or f >= SINGT - 2 else PLUSTER, False
    if f < SCHUETTELT:                                               # singt zwei Strophen
        u = (f - SINGT) % STROPHE
        return X0, FUSS, singt(u, 0) if u < GESANG else SITZT, False
    if f < RUHT:                                                     # schüttelt sich
        return X0 + (0, 1, 0, -1)[(f - SCHUETTELT) % 4], FUSS, PLUSTER, False
    if f < FLUG_VON:                                                 # hüpft den Zweig entlang
        x = X0
        for h in HUEPFER:
            if f >= h + 6:
                x += 4
            elif f >= h:
                k = f - h
                return x + round(4 * (k + 1) / 6), FUSS - (1, 2, 2, 2, 1, 0)[k], SITZT, False
        return x, FUSS, SITZT, False
    if f < FLUG_BIS:                                                 # fliegt auf, Bogen, landet
        a = (f - FLUG_VON) / (FLUG_BIS - FLUG_VON)
        x, y = bezier(*BOGEN, a)
        return x, y, FLUEGELSCHLAG[f % 4], bezier(*BOGEN, a + 0.03)[0] < x
    if f < DREHT:
        return X0, FUSS, SITZT, True
    if EINS_ANTWORTET[0] <= f < EINS_ANTWORTET[1]:
        return X0, FUSS, singt(f, EINS_ANTWORTET[0]), False
    if KUSCHELN[0] <= f < KUSCHELN[1]:
        return X0, FUSS, HALB if f < KUSCHELN[0] + 2 or f >= KUSCHELN[1] - 2 else PLUSTER, False
    return X0, FUSS - (f in (DA + 1, DA + 2)), ruht(f), False        # kleiner Hüpfer zur Begrüßung


def zweites(f):
    """Das zweite Rotkehlchen (sitzt mit Blick nach links) oder None."""
    if f < KOMMT or f >= WEG:
        return None
    if f < DA:                                                       # fliegt von rechts oben an, bremst
        a = 1 - (1 - (f - KOMMT) / (DA - KOMMT)) ** 1.6
        x, y = bezier((68, 3), (52, 3), (X2 + 8, 5), (X2, FUSS), a)
        return x, y, FLUEGELSCHLAG[f % 4], True
    if f >= FORT:                                                    # fliegt nach rechts oben davon
        a = ((f - FORT) / (WEG - FORT)) ** 1.5
        x, y = bezier((X2, FUSS), (X2 + 4, 5), (50, 4), (70, 2), a)
        return x, y, FLUEGELSCHLAG[f % 4], False
    if ZWEI_SINGT[0] <= f < ZWEI_SINGT[1]:
        return X2, FUSS, singt(f, ZWEI_SINGT[0]), True
    if KUSCHELN[0] <= f < KUSCHELN[1]:
        return X2, FUSS, HALB if f < KUSCHELN[0] + 2 or f >= KUSCHELN[1] - 2 else PLUSTER, True
    return X2, FUSS, ruht(f, 21), f < FORT - 2                       # dreht sich vor dem Abflug um


def bilder():
    liste = []
    for f in range(255):
        bild = Bild()
        kulisse(bild)
        for start, x, farbe, drift in NOTENPLAN:                     # Noten steigen auf
            t = f - start
            if 0 <= t < 21:                                          # erst rasch hoch, dann gemächlich zur Seite
                y = 2 - t // 3 if t < 6 else -(t - 6) // 5
                bild.figur(round(x + drift * max(0, t - 4)), y, NOTE, {"n": farbe})
        for start, x in KRUEMELPLAN:                                 # Schnee rieselt vom Zweig
            t = f - start
            if 0 <= t < 12:
                bild.setze(x, SCHNEE_Y + 1 + t // 3, KRUEMEL)
        if SCHUETTELT <= f < RUHT:                                   # Schnee stiebt links und rechts auf
            k = f % 2
            bild.setze(X0 - 2 + k, FUSS - k, KRUEMEL)
            bild.setze(X0 + 10 - k, FUSS - 1 + k, KRUEMEL)
        zwei = zweites(f)
        if zwei:
            vogel(bild, *zwei, VOGEL_2)
        vogel(bild, *erstes(f), VOGEL_1)
        liste.append(bild)
    return liste
