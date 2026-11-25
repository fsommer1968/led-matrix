"""Schneepflug: nächtliche Dorfstraße mit Laternen, auf der Fahrbahn liegt Schnee. Ein oranges
Räumfahrzeug mit Rundum-Blinklicht und Scheinwerfer fährt von links nach rechts durch und schiebt
den Schnee mit dem gelben Pflugschild zur Seite: über dem Schild stiebt er auf, am vorderen Rand
türmt sich ein Wall, dahinter ist die Straße frei und dunkel. Im grünen Haus geht dabei ein
Fenster an. Danach schneit es leicht, die Fahrbahn wird wieder weiß, der Wall schneit ein, das
Fenster geht aus. Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert; gleiche Spalten und sich wiederholende Spaltenfolgen kosten
fast nichts. Darum wiederholt sich die Kulisse alle 16 Spalten (Laterne, dann ein Haus mit
gerader Dachkante), nur ein Haus ist anders (Farbe, Tür, Fenster), die Haufen im Wall haben
denselben Takt, das Fahrzeug hat viele gleiche Nachbarspalten, der Schneestaub bleibt in den
Spalten von Schild und Haufen, die Straße ist je Zustand einfarbig und schneit als Ganzes ein,
es gibt einen Stern und nur wenige Flocken.
"""
import math

from basis import B, GELB, NACHTBLAU, ORANGE, ROT, WEISS, Bild, dimmen, mischen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "schneepflug"
TITEL = "Schneepflug räumt nachts die Straße"

# ── Farben ─────────────────────────────────────────────────────────
KANTE = (215, 225, 250)                        # heller Schnee: hinterer Straßenrand, Wall, Aufgeschobenes
DECKE = (84, 96, 148)                          # Schneedecke auf der Fahrbahn, gedämpft (große Fläche)
ASPHALT = (14, 14, 24)                         # geräumte Fahrbahn
DACH = (150, 160, 205)                         # Schnee auf den Dächern (hinten, etwas matter)
HAUS = (33, 17, 14)
HAUS_GRUEN = (38, 76, 58)
FENSTER = (255, 185, 60)
DUNKEL = (30, 18, 22)                          # Fenster ohne Licht
TUER = (49, 31, 10)
PFOSTEN = (72, 72, 92)
LAMPE = (255, 225, 150)
HOF = (120, 88, 36)                            # Lichthof über der Lampe
STERN = (255, 240, 200)
STERN_X, STERN_Y, STERN_PERIODE = 46, 1, 51    # ein Stern; die Periode teilt 255: die Runde schließt
KASTEN = (185, 45, 0)                          # Streugutkasten hinter dem Fahrerhaus
SCHEIBE = (110, 200, 255)
RAD = (78, 78, 100)
NABE = (175, 175, 195)
ARM = (120, 120, 140)
LICHT = (255, 250, 200)                        # Scheinwerfer
KEGEL = [(4, (215, 200, 130)), (4, (140, 148, 160))]   # angeleuchtete Schneedecke: Spalten, Farbe
BLINK_AN, BLINK_AUS, BLINK_HOF = (255, 170, 0), (120, 50, 0), (150, 70, 0)
FLOCKE_NAH, FLOCKE_FERN = (225, 230, 255), (105, 115, 165)

# ── Aufbau ─────────────────────────────────────────────────────────
RAND_Y = 10                                    # hinterer Straßenrand (helle Schneekante)
STRASSE_Y = 11                                 # Fahrbahn: Zeilen 11 bis 14; Zeile 15 ist der vordere Rand
TAKT = 16                                      # Kulisse wiederholt sich: Laterne in der Lücke, dann ein Haus
LATERNE_X = 2
HAUS_X, HAUS_B, DACH_Y = 5, 11, 4
FENSTER_X = (7, 12)                            # zwei Fenster, je zwei Spalten breit
# Höhe des Walls über Zeile 15 je Spalte im Takt: ein Haufen unter der Laterne, ein flacher vor dem Haus
WALL_TAKT = (1, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0)
# Das dritte Haus ist das besondere (seine Spalten kosten ohnehin eigene Bytes): grün, Tür statt linkem
# Fenster, das rechte Fenster ist dunkel und geht an, wenn der Pflug kommt
BESONDERS, WACH_AN, WACH_AUS = 2, 84, 236

# Räumfahrzeug (Blick nach rechts), 21 breit, Zeilen 6 bis 14: k Kasten, o orange, f Scheibe,
# l Scheinwerfer, t Rücklicht, w Rad, n Nabe, g Arm, y Schild. Viele Nachbarspalten sind gleich
# (Kasten, Radmitte unter dem Blinklicht, Haube); die Nabe springt zwischen oben und unten: das Rad dreht sich.
PFLUG = ["........ooooo........",
         "kkkkkkkkoffff........",
         "kkkkkkkkoffff........",
         "ooooooooooooooool....",
         "toooooooooooooooo..yy",
         "oowwoooooowwooooogyy.",
         ".wNNw....wNNw....gyy.",
         ".wnnw....wnnw.....yy.",
         "..ww......ww.......yy"]
PFLUG_B = len(PFLUG[0])
PFLUG_Y = 6
BLINK_X = 10                                   # Blinklicht: zwei Spalten über dem Fahrerhaus

START = 24                                     # ab hier schiebt sich das Schild ins Bild (ein Pixel je zwei Bilder)
HAUFEN = (3, 2, 1)                             # aufgeschobener Schnee vor dem Schild (Höhe je Spalte)
# Schneestaub über Schild und Haufen (Spalte ab Schildspitze, Zeile), zwei Phasen im Wechsel
STAUB = (((1, 8), (2, 9), (3, 7), (0, 7), (2, 6)), ((1, 6), (2, 8), (3, 9), (0, 9), (3, 6)))
# Einschneien: ab WEISS_AB wird die geräumte Fahrbahn in STUFEN Schritten wieder weiß
WEISS_AB, STUFEN, STUFE_DAUER = 184, 7, 9
# Flocken: Spalte, Start, Tempo, nah (hell, fällt bis auf die Straße) oder fern (matt, nur vor dem Himmel)
FLOCKEN = [(9, 150, 0.34, 1), (44, 154, 0.25, 0), (27, 160, 0.5, 1), (60, 165, 0.25, 0), (3, 170, 0.34, 0),
           (36, 174, 0.34, 1), (19, 179, 0.25, 1), (51, 184, 0.5, 1), (12, 189, 0.34, 0), (41, 193, 0.34, 1),
           (58, 198, 0.34, 0), (24, 202, 0.5, 1), (5, 206, 0.34, 1), (33, 210, 0.5, 0), (47, 214, 0.5, 1),
           (16, 217, 0.5, 1), (55, 220, 0.5, 0), (29, 222, 0.5, 1)]


def schild_x(f):
    """Vorderste Spalte des Pflugschilds."""
    return (f - START) // 2


def kulisse(bild, f):
    """Himmel mit Stern, Häuser mit Laternen dazwischen und der hintere Straßenrand."""
    bild.setze(STERN_X, STERN_Y, dimmen(STERN, 1.0 if f % STERN_PERIODE < STERN_PERIODE * 0.6 else 0.5))
    for nr, x0 in enumerate(range(0, B, TAKT)):
        bild.rechteck(x0 + LATERNE_X, 5, 1, 5, PFOSTEN)              # Laterne mit Lichthof darüber
        bild.setze(x0 + LATERNE_X, 4, LAMPE)
        bild.setze(x0 + LATERNE_X, 3, HOF)
        # Haus: Schnee auf dem Dach (oben schmaler: von Fenster zu Fenster), zwei Fenster
        bild.rechteck(x0 + FENSTER_X[0], DACH_Y - 1, FENSTER_X[1] + 2 - FENSTER_X[0], 1, DACH)
        bild.rechteck(x0 + HAUS_X, DACH_Y, HAUS_B, 1, DACH)
        if nr != BESONDERS:
            bild.rechteck(x0 + HAUS_X, DACH_Y + 1, HAUS_B, RAND_Y - DACH_Y - 1, HAUS)
            for wx in FENSTER_X:
                bild.rechteck(x0 + wx, DACH_Y + 2, 2, 2, FENSTER)
        else:
            bild.rechteck(x0 + HAUS_X, DACH_Y + 1, HAUS_B, RAND_Y - DACH_Y - 1, HAUS_GRUEN)
            bild.rechteck(x0 + FENSTER_X[0], DACH_Y + 3, 2, 3, TUER)
            bild.rechteck(x0 + FENSTER_X[1], DACH_Y + 2, 2, 2, FENSTER if WACH_AN <= f < WACH_AUS else DUNKEL)
    bild.rechteck(0, RAND_Y, B, 1, KANTE)


def stufe(f):
    """Wie weit die geräumte Fahrbahn wieder eingeschneit ist: 0 (frei) … 1 (weiß)."""
    return max(0, min(STUFEN, (f - WEISS_AB) // STUFE_DAUER + 1)) / STUFEN


def strasse(bild, f):
    """Fahrbahn: Schneedecke vor dem Schild, dahinter frei und dunkel mit Wall am vorderen Rand;
    später schneit alles in Stufen wieder ein."""
    vorn = schild_x(f)
    a = stufe(f)
    for x in range(B):
        if f < START or x >= vorn - 1:                               # noch nicht geräumt
            bild.rechteck(x, STRASSE_Y, 1, 5, DECKE)
            continue
        bild.rechteck(x, STRASSE_Y, 1, 4, mischen(ASPHALT, DECKE, a))
        hoch = WALL_TAKT[x % TAKT] if x <= vorn - PFLUG_B else 0     # der Wall türmt sich erst hinter dem Wagen
        bild.rechteck(x, 15 - hoch, 1, 1 + hoch, mischen(KANTE, DECKE, a))


def pflug(bild, f):
    """Räumfahrzeug mit Blinklicht, Scheinwerferkegel, aufgeschobenem Schnee und Schneestaub."""
    vorn = schild_x(f)
    x0 = vorn - PFLUG_B + 1
    if vorn + len(HAUFEN) + sum(n for n, _ in KEGEL) < 0 or x0 >= B:
        return
    # aufgeschobener Schnee vor dem Schild, Schneestaub darüber
    bild.rechteck(vorn - 1, 15, 2, 1, KANTE)                         # der Wall beginnt unter dem Schild
    for k, hoch in enumerate(HAUFEN):
        bild.rechteck(vorn + 1 + k, 15 - hoch, 1, hoch + 1, KANTE)
    for dx, y in STAUB[((f + 1) // 2) % 2]:                          # wechselt zwischen zwei Schritten des Wagens
        bild.setze(vorn + dx, y, WEISS)
    # Scheinwerfer leuchtet die Schneedecke davor an (nah heller, fern matter)
    x = vorn + 1 + len(HAUFEN)
    for breit, farbe in KEGEL:
        bild.rechteck(x, STRASSE_Y, breit, 5, farbe)
        x += breit
    oben = (f // 2) % 2                                              # Nabe oben oder unten
    farben = {"k": KASTEN, "o": ORANGE, "f": SCHEIBE, "l": LICHT, "t": ROT, "w": RAD, "g": ARM, "y": GELB,
              "N": NABE if oben else RAD, "n": RAD if oben else NABE}
    bild.figur(x0, PFLUG_Y, PFLUG, farben)
    # Rundum-Blinklicht: vier Bilder hell mit Hof, vier Bilder dunkel
    bx = x0 + BLINK_X
    if (f // 4) % 2:
        bild.rechteck(bx, PFLUG_Y - 1, 2, 1, BLINK_AUS)
    else:
        bild.rechteck(bx, PFLUG_Y - 2, 2, 2, BLINK_AN)
        bild.rechteck(bx, PFLUG_Y - 3, 2, 1, BLINK_HOF)
        bild.setze(bx - 1, PFLUG_Y - 2, BLINK_HOF)
        bild.setze(bx + 2, PFLUG_Y - 2, BLINK_HOF)


def flocken(bild, f):
    """Leichter Schneefall, während die Fahrbahn wieder weiß wird."""
    for x, start, tempo, nah in FLOCKEN:
        y = (f - start) * tempo - 1
        if f < start or y > (14 if nah else RAND_Y - 1):
            continue
        x += round(math.sin((f + start) / 9))
        if nah or bild.hole(x, y) == NACHTBLAU:
            bild.setze(x, y, FLOCKE_NAH if nah else FLOCKE_FERN)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        kulisse(bild, f)
        strasse(bild, f)
        pflug(bild, f)
        flocken(bild, f)
        liste.append(bild)
    return liste
