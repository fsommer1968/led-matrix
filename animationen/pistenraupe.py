"""Pistenraupe: nächtlicher Skihang, der sanft nach rechts ansteigt, dunkle Tannen an beiden
Rändern, Mond und Sterne. Eine rote Pistenraupe mit Kettenlaufwerk, warm erleuchteter Kabine,
gelbem Rundumlicht (es dreht sich) und zwei Scheinwerfern schiebt sich langsam von links nach
rechts den Hang hinauf: zuerst wandert nur der Lichtfleck der Scheinwerfer ins Bild, dann das
Räumschild mit einer kleinen Schneewalze, die Raupe mit umlaufender Kette und hinten die Fräse
mit Finisher, hinter der die geriffelte Cordspur als feines Streifenmuster zurückbleibt. Danach
schneit es leicht, die Spur schneit in feinen Stufen zu, bis der Hang wieder glatt ist. Die
Runde geht ohne Sprung in sich über – 255 Bilder.

Anders als der Schneepflug (Dorfstraße, Häuser, Laternen, oranger Lastwagen): hier ein freier
Hang mit Gefälle, ein Kettenfahrzeug und eine Spur, die als Muster liegen bleibt.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert; gleiche Nachbarspalten kosten fast nichts. Darum steigt
der Hang in wenigen Stufen, die Cordspur besteht aus waagerechten Streifen (alle Spalten einer
Stufe sind gleich), der Lichtfleck ist einfarbig, die Raupe hat viele gleiche Nachbarspalten,
ihr starrer Aufbau bleibt auch über einer Stufe gerade, es gibt nur vier Tannen, drei Sterne
und wenige Flocken. Die Kulisse allein kostet etwa 180 Bytes je Bild (Mond 30, jede Tanne
rund 20, jeder Stern rund 9), die Raupe samt Lichtfleck bis zu 200.
"""
import math

from basis import B, GELB, NACHTBLAU, Bild, dimmen, mischen

NAME = "pistenraupe"
TITEL = "Pistenraupe präpariert nachts den Hang"

# ── Farben ─────────────────────────────────────────────────────────
KANTE = (215, 225, 250)                        # Oberkante des Hangs, Schneewalze vor dem Schild
HANG = (78, 90, 140)                           # unberührter Schnee, gedämpft (große Fläche)
CORD_HELL = (180, 190, 230)                    # Cordspur: helle Rippen …
CORD_DUNKEL = (40, 50, 96)                     # … und dunkle Rillen
ROT = (235, 20, 15)                            # Raupe
FENSTER = (255, 185, 60)                       # warmes Licht in der Kabine
KETTE = (26, 26, 40)
GLIED = (150, 150, 172)                        # helle Kettenglieder, sie laufen um
FRAESE = (120, 120, 142)                       # Fräse am Heck, Schildarm
FINISHER = (255, 150, 0)                       # Glättmatte hinter der Fräse
LICHT = (255, 250, 200)                        # Scheinwerfer
KEGEL = (225, 208, 135)                        # angeleuchteter Schnee, einfarbig
BLINK_AUS, BLINK_HOF = (120, 80, 0), (150, 110, 0)
TANNE = (0, 92, 36)
MOND = (240, 230, 170)
STERN = (255, 240, 200)
STERNE = [(10, 1, 0, 51), (30, 1, 30, 85), (45, 0, 9, 51)]   # x, y, Phase, Periode (teilt 255: die Runde schließt)
FLOCKE_NAH, FLOCKE_FERN = (225, 230, 255), (105, 115, 165)

# ── Aufbau ─────────────────────────────────────────────────────────
MOND_X = 18
TANNEN = [(2, 8), (8, 5), (55, 4), (61, 6)]    # Spalte der Spitze, Höhe
STUFE_B = 13                                   # alle 13 Spalten steigt der Hang um eine Zeile
BAND = 4                                       # Spurbreite: vier Zeilen unter der Kante
KEGEL_FORM = (2, 4, 4, 4, 4, 4, 4, 2)          # Lichtfleck vor dem Schild: Höhe je Spalte, Enden gerundet
KEGEL_B = len(KEGEL_FORM)

# Raupe (Blick nach rechts), 22 breit: H Hof, B und C Rundumlicht (linke und rechte Hälfte), r rot,
# f Fenster, l Scheinwerfer, a Schildarm, y Finisher, t Fräse, k Kette, w Kettenglied, s Schild,
# p Schneewalze vor dem Schild.
# Viele Nachbarspalten sind gleich. Der Aufbau (die oberen sieben Zeilen) ist starr und richtet sich
# nach dem Hang unter der Kabine, Fräse und Kette folgen spaltenweise dem Gelände, das Schild dem
# Hang an der Schildspitze.
RAUPE = ["...........HH.........",
         "...........BC.........",
         ".........rrrrrr.......",
         ".........rffffrl......",
         ".........rfffffr......",
         "...rrrrrrrrrrrrrl..s..",
         "...rrrrrrrrrrrrraas...",
         ".ttkkkkkkkkkkkkk..s...",
         "yttkwwkkwwkkwwkk..ssp.",
         "yttkkkkkkkkkkkk...sspp"]
RAUPE_B, RAUPE_H = len(RAUPE[0]), len(RAUPE)
MITTE = 9                                      # Spalte, nach der sich der starre Aufbau richtet
SCHILD = 19                                    # Spalte der Schildspitze in der Figur
KETTE_AB = RAUPE_H - 3                         # ab dieser Zeile: Laufwerk (folgt dem Gelände)

# Einschneien: ab WEISS_AB verblasst die Spur in STUFEN Schritten
WEISS_AB, STUFEN, STUFE_DAUER = 192, 14, 4
# Flocken: Spalte, Start, Tempo, nah (hell, fällt bis auf den Hang) oder fern (matt, nur vor dem Himmel)
FLOCKEN = [(9, 150, 0.34, 1), (44, 154, 0.25, 0), (30, 160, 0.5, 1), (60, 165, 0.25, 0), (40, 167, 0.34, 1),
           (3, 170, 0.34, 0), (36, 174, 0.34, 1), (23, 179, 0.25, 1), (51, 184, 0.5, 1), (26, 186, 0.34, 0),
           (14, 189, 0.34, 0), (41, 193, 0.34, 1), (8, 196, 0.5, 1), (57, 198, 0.34, 0), (24, 202, 0.5, 1),
           (52, 205, 0.34, 1), (5, 206, 0.34, 1), (33, 210, 0.5, 0), (47, 214, 0.5, 1), (12, 217, 0.5, 1),
           (55, 220, 0.5, 0), (29, 222, 0.5, 1)]


def hang_y(x):
    """Oberkante des Hangs: steigt nach rechts in Stufen an."""
    return 11 - max(0, min(B - 1, x)) // STUFE_B


def schild_x(f):
    """Spalte der Schildspitze: ein Pixel je zwei Bilder; zuerst erscheint nur der Lichtkegel."""
    return f // 2 - KEGEL_B - 3


def verblasst(f):
    """Wie weit die Spur wieder zugeschneit ist: 0 (frisch) … 1 (glatt)."""
    return max(0, min(STUFEN, (f - WEISS_AB) // STUFE_DAUER + 1)) / STUFEN


def tanne(bild, x, hoehe):
    """Dunkle Tanne auf der Hangkante: alle zwei Zeilen eine Stufe breiter (höchstens fünf Spalten)."""
    fuss = hang_y(x)
    for k in range(hoehe):
        halb = min(2, k // 2)
        bild.rechteck(x - halb, fuss - hoehe + k, 2 * halb + 1, 1, TANNE)


def kulisse(bild, f):
    """Himmel mit Sternen und Mond, Tannen an den Rändern."""
    for x, y, phase, periode in STERNE:
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    bild.kreis(MOND_X, 2, 2.2, MOND)
    for x, hoehe in TANNEN:
        tanne(bild, x, hoehe)


def hang(bild, f):
    """Hang mit heller Kante; hinter der Raupe die Cordspur, die später zuschneit."""
    heck = schild_x(f) - SCHILD                                      # hinterste Spalte der Raupe
    a = verblasst(f)
    hell, dunkel = mischen(CORD_HELL, HANG, a), mischen(CORD_DUNKEL, HANG, a)
    for x in range(B):
        y0 = hang_y(x)
        bild.setze(x, y0, KANTE)
        bild.rechteck(x, y0 + 1, 1, 15 - y0, HANG)
        if x < heck:                                                 # Cord: dunkle Rille, helle Rippe im Wechsel
            for k in range(BAND):
                bild.setze(x, y0 + 1 + k, hell if k % 2 else dunkel)


def raupe(bild, f):
    """Pistenraupe mit Rundumlicht, Lichtkegel und laufender Kette."""
    vorn = schild_x(f)
    x0 = vorn - SCHILD
    if x0 > B:
        return
    for k, hoch in enumerate(KEGEL_FORM):                            # Lichtfleck auf dem Schnee vor dem Schild
        x = vorn + 3 + k
        bild.rechteck(x, hang_y(x) + 1 + (BAND - hoch) // 2, 1, hoch, KEGEL)
    # Rundumlicht dreht sich: links hell, beide hell mit Hof, rechts hell, beide dunkel (je zwei Bilder,
    # um ein Bild gegen den Schritt der Raupe versetzt: so ändert sich in jedem Bild etwas)
    links, rechts = ((1, 0), (1, 1), (0, 1), (0, 0))[((f + 1) // 2) % 4]
    farben = {"r": ROT, "f": FENSTER, "l": LICHT, "t": FRAESE, "a": FRAESE, "s": ROT, "k": KETTE,
              "w": GLIED, "p": KANTE, "y": FINISHER, "B": GELB if links else BLINK_AUS,
              "C": GELB if rechts else BLINK_AUS, "H": BLINK_HOF if links and rechts else None}
    schritt = (f // 2) % 4                                           # die Kettenglieder laufen mit jedem Schritt
    aufbau = hang_y(x0 + MITTE) + BAND                               # Unterkante für den starren Aufbau
    schild = hang_y(vorn) + BAND                                     # … und für das Schild
    for dx in range(RAUPE_B):
        x = x0 + dx
        if not 0 <= x < B:
            continue
        boden = hang_y(x) + BAND
        for dy, zeile in enumerate(RAUPE):
            c = zeile[dx]
            if c == ".":
                continue
            if c in "sp":
                unten = schild
            elif dy < KETTE_AB:
                unten = aufbau
            else:
                unten = boden
                if c in "kw" and dy == RAUPE_H - 2 and dx < 15:      # Muster läuft nach hinten
                    c = "w" if (dx + schritt) % 4 < 2 else "k"
            bild.setze(x, unten - RAUPE_H + 1 + dy, farben[c])
        if boden > aufbau and RAUPE[KETTE_AB][dx] == "k":            # Kette hängt eine Zeile tiefer: Lücke schließen
            bild.setze(x, aufbau - 2, KETTE)
    if (f // 2) % 2:                                                 # jeden zweiten Schritt: die Walze vor dem
        bild.setze(vorn + 2, schild - 1, KANTE)                      # Schild rollt, hinter der Fräse stäubt es
        if x0 >= 1:
            bild.setze(x0 - 1, hang_y(x0 - 1) + BAND - 2, KANTE)


def flocken(bild, f):
    """Leichter Schneefall, während die Spur zuschneit."""
    for x, start, tempo, nah in FLOCKEN:
        y = (f - start) * tempo - 1
        if f < start or y > (hang_y(x) + BAND if nah else hang_y(x) - 1):
            continue
        x += round(math.sin((f + start) / 9))
        if nah or bild.hole(x, y) == NACHTBLAU:
            bild.setze(x, y, FLOCKE_NAH if nah else FLOCKE_FERN)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        kulisse(bild, f)
        hang(bild, f)
        raupe(bild, f)
        flocken(bild, f)
        liste.append(bild)
    return liste
