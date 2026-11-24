"""Schwarzwälder Kirschtorte: Die Torte steht im Anschnitt auf der Tortenplatte (dunkle Böden, Sahne
mit Kirschen, oben Sahnetupfen mit Kirsche, außen Sahnemantel mit Raspeln). Ein Messer schneidet
ein Stück ab, der Tortenheber setzt es auf den Teller daneben, die Gabel holt Bissen um Bissen, bis
nur Krümel bleiben. Dann dreht sich die Tortenplatte, die Lücke wandert nach hinten, ein frischer
Teller kommt, die Torte glitzert – die Runde geht ohne Sprung in sich über. Links das Stubenfenster
mit Schnee und Tanne. 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum wiederholt sich die Torte alle vier Spalten (Lücke mit
Raspel, Tupfen mit Kirsche, je zwei Spalten breit), Teller und Tischdecke sind einfarbige Zeilen,
Messer, Heber und Gabel stehen senkrecht oder liegen waagerecht, die Wand bleibt dunkel.
"""
from basis import B, GELB, Bild

NAME = "kirschtorte"
TITEL = "Schwarzwälder Kirschtorte"

WAND = (0, 0, 0)
DECKE = (0, 75, 30)                            # Tischdecke (eine Zeile)
SCHOKO = (130, 55, 10)                         # Böden und Raspeln (gedämpft, große Fläche)
SAHNE = (255, 250, 235)
KIRSCHE = (255, 0, 20)
TELLER = (110, 128, 185)                       # Porzellan, bläulich und gedämpft (hebt sich von der Sahne ab)
GLANZ = (215, 228, 255)                        # Glanzlicht auf der Tortenplatte, wenn sie sich dreht
STAHL = (130, 180, 255)                        # Klinge, Heberblatt, Gabel
GRIFF = (230, 130, 20)
RAHMEN = (200, 105, 15)                        # Fensterrahmen, warmes Holz
NACHT = (0, 12, 62)
SCHNEE = (200, 210, 240)
TANNE = (0, 120, 40)
STAMM = (100, 50, 15)

X0 = 17                                        # linke Kante der Torte
BREIT = 24                                     # Spalten der ganzen Torte
SCHNITT = 17                                   # ab dieser Spalte ist es das Stück (7 breit)
OBEN = 2                                       # oberste Zeile der Torte (Kirschen); unterster Boden in Zeile 13
TX = 46                                        # Kuchenteller, 13 breit
SX = 49                                        # dort steht das Stück auf dem Teller

# Ablauf: Ruhe, Messer schneidet, Heber trägt hinüber, Gabel isst, Platte dreht sich (36 Bilder), Ruhe
MESSER_AB, HEBER_AB, ESSEN_AB, DREHEN_AB, GANZ_AB = 10, 38, 82, 210, 246
BISS = 20                                      # Bilder je Bissen
# Bissen: Spalten des Stücks, Zeilen, Höhe der Gabel – erst oben, dann unten, von rechts nach links
BISSEN = [((4, 6), (2, 8), 6), ((4, 6), (9, 13), 11), ((2, 3), (2, 8), 6), ((2, 3), (9, 13), 11),
          ((0, 1), (2, 8), 6), ((0, 1), (9, 13), 11)]
KRUEMEL = [(54, SCHOKO), (51, SAHNE), (49, SCHOKO)]              # bleiben nach dem 2., 4. und 6. Bissen
# Flocken im Fenster: Spalte, Versatz, Bilder je Zeile (17 Zeilen Umlauf → 85 und 51 Bilder, teilen 255)
FLOCKEN = [(2, 0, 5), (10, 31, 5), (4, 58, 3), (8, 20, 3)]
FUNKEN = [(X0 + 5, 1), (X0 + 21, 0), (X0 + 13, 1)]               # Glitzern über den Lücken zwischen den Kirschen


def spalte(o, dreh=0, mantel=True):
    """Farben der Tortenspalte o von Zeile OBEN bis 13 (None = leer). Innen wechseln Lücke (mit
    Raspel) und Tupfen mit Kirsche, je zwei Spalten breit; die Kirschen in den beiden Sahneschichten
    sitzen versetzt. `dreh` schiebt das Muster nach rechts (die Platte dreht sich)."""
    if o == 0 or (mantel and o == BREIT - 1):                        # Sahnemantel mit Raspeln
        return [None, None, None, SAHNE, SAHNE, SAHNE, SCHOKO, SAHNE, SAHNE, SCHOKO, SAHNE, SAHNE]
    i = (o - 1 - dreh) % 4
    if i < 2:
        return [None, None, SCHOKO if i == 0 else None, SAHNE, SCHOKO, SCHOKO, KIRSCHE, SCHOKO, SCHOKO,
                SAHNE, SCHOKO, SCHOKO]
    return [KIRSCHE, KIRSCHE, SAHNE, SAHNE, SCHOKO, SCHOKO, SAHNE, SCHOKO, SCHOKO, KIRSCHE, SCHOKO, SCHOKO]


def torte(bild, bis, dreh=0, mantel=True):
    """Torte von Spalte 0 bis `bis` (einschließlich); `mantel` = rechter Rand mit Sahnemantel."""
    for o in range(bis + 1):
        for k, farbe in enumerate(spalte(o, dreh, mantel)):
            bild.setze(X0 + o, OBEN + k, farbe)


def stueck(bild, x, dy=0, weg=()):
    """Das abgeschnittene Stück (Spalten SCHNITT … Ende) bei x; `weg` = gegessene Bissen."""
    for c in range(BREIT - SCHNITT):
        for k, farbe in enumerate(spalte(SCHNITT + c)):
            y = OBEN + k
            if not any(c0 <= c <= c1 and y0 <= y <= y1 for (c0, c1), (y0, y1), _ in weg):
                bild.setze(x + c, y + dy, farbe)


def fenster(bild, f):
    """Stubenfenster: warmer Holzrahmen, draußen Nacht, Schnee, eine Tanne mit Schneehaube."""
    bild.rechteck(1, 0, 11, 12, RAHMEN)
    bild.rechteck(2, 1, 9, 10, NACHT)
    bild.rechteck(2, 10, 9, 1, SCHNEE)                               # Schnee draußen
    for x, phase, tempo in FLOCKEN:                                  # Flocken fallen langsam
        y = ((f + phase) // tempo) % 17 - 3
        if 1 <= y <= 9:
            bild.setze(x, y, SCHNEE)
    for k, halb in enumerate((0, 0, 1, 1, 2, 2)):                    # Tanne: alle zwei Zeilen eine Stufe breiter
        bild.rechteck(6 - halb, 3 + k, 2 * halb + 1, 1, TANNE)
    bild.setze(6, 2, SCHNEE)
    bild.setze(6, 9, STAMM)
    bild.rechteck(0, 12, 13, 1, RAHMEN)                              # Fensterbank


def messer(bild, x, spitze):
    """Senkrechtes Messer, Spitze bei Zeile `spitze`, Griff oben."""
    bild.rechteck(x, spitze - 9, 1, 10, STAHL)
    bild.rechteck(x - 1, spitze - 14, 3, 5, GRIFF)


def heber(bild, x, y):
    """Tortenheber von der Seite: Blatt 9 breit ab x in Zeile y, Griff nach rechts."""
    bild.rechteck(x, y, 9, 1, STAHL)
    bild.rechteck(x + 9, y - 1, 12, 1, GRIFF)


def gabel(bild, x, y, happen=None):
    """Gabel von rechts: Zinken ab x, Stiel bis zum Rand; `happen` = Farben des Bissens (drei Zeilen)."""
    bild.rechteck(x + 2, y, B, 1, STAHL)
    bild.rechteck(x, y - 1, 3, 1, STAHL)
    bild.rechteck(x, y + 1, 3, 1, STAHL)
    for k, farbe in enumerate(happen or ()):
        bild.rechteck(x - 1, y - 1 + k, 3, 1, farbe)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(WAND)
        fenster(bild, f)
        bild.rechteck(0, 15, B, 1, DECKE)
        bild.rechteck(X0 - 2, 14, BREIT + 4, 1, TELLER)              # Tortenplatte

        # ── Torte: ganz, angeschnitten oder beim Drehen ──
        if f < MESSER_AB or f >= GANZ_AB:
            torte(bild, BREIT - 1)
        elif f < DREHEN_AB:
            torte(bild, SCHNITT - 1, mantel=False)
        else:                                                        # Platte dreht sich, die Lücke schließt sich
            t = f - DREHEN_AB
            rand = min(BREIT - 1, SCHNITT - 1 + (t + 3) // 5)
            torte(bild, rand, dreh=(t + 1) // 3, mantel=rand == BREIT - 1)
            for x in range(X0 - 4 + t, X0 - 1 + t):                  # Glanzlicht läuft einmal über die Platte
                if X0 - 2 <= x < X0 + BREIT + 2:
                    bild.setze(x, 14, GLANZ)
        funke = (f - GANZ_AB) % 255                                  # die Torte ist wieder ganz: Glitzern
        if funke < 18:                                               # (läuft über die Naht 254 → 0 weiter)
            bild.setze(*FUNKEN[funke // 3 % 3], GELB)

        # ── Kuchenteller (wird beim Drehen gegen einen frischen getauscht) ──
        tdx = 0
        if DREHEN_AB <= f < DREHEN_AB + 21:
            t = f - DREHEN_AB
            tdx = 2 * (t + 1) if t < 9 else 2 * (20 - t)
        bild.rechteck(TX + tdx, 14, 13, 1, TELLER)

        if MESSER_AB <= f < HEBER_AB:
            # ── Messer schneidet von oben, schiebt das Stück eine Spalte ab und geht wieder ──
            t = f - MESSER_AB
            stueck(bild, X0 + SCHNITT + (1 if t >= 17 else 0))
            messer(bild, X0 + SCHNITT, min(13, t) if t < 20 else 13 - 2 * (t - 19))
        elif HEBER_AB <= f < ESSEN_AB:
            # ── Tortenheber schiebt sich darunter, hebt an, trägt hinüber, setzt ab ──
            t = f - HEBER_AB
            start = X0 + SCHNITT + 1
            if t < 12:                                               # von rechts unter das Stück
                dx, dy, hx = 0, 0, max(start - 1, 64 - 3 * (t + 1))
            elif t < 16:                                             # anheben
                dx, dy, hx = 0, -1 - (t - 12) // 2, start - 1
            elif t < 30:                                             # hinüber
                dx, dy = t - 15, -2
                hx = start - 1 + dx
            elif t < 35:                                             # absetzen
                dx, dy = SX - start, -1 if t < 32 else 0
                hx = start - 1 + dx
            else:                                                    # Heber zieht sich zurück
                dx, dy, hx = SX - start, 0, SX - 1 + 3 * (t - 34)
            stueck(bild, start + dx, dy)
            heber(bild, hx, 14 + dy)
        elif ESSEN_AB <= f < DREHEN_AB:
            # ── Gabel isst das Stück: hin, einstechen, Bissen mitnehmen, nach rechts oben hinaus ──
            t = f - ESSEN_AB
            nr, tb = t // BISS, t % BISS
            fertig = min(nr, len(BISSEN)) + (1 if nr < len(BISSEN) and tb >= 10 else 0)
            stueck(bild, SX, weg=BISSEN[:fertig])
            for k, (x, farbe) in enumerate(KRUEMEL):
                if fertig >= 2 * k + 2:
                    bild.setze(x, 13, farbe)
            if nr < len(BISSEN):
                (_, c1), _, gy = BISSEN[nr]
                ziel = SX + c1 + 1
                if tb < 8:
                    gabel(bild, max(ziel, 64 - 2 * tb), gy)
                elif tb < 10:
                    gabel(bild, ziel - 1, gy)
                else:
                    fort = max(0, tb - 11)
                    gabel(bild, ziel + 2 * fort, gy - fort // 2, [KIRSCHE if nr == 2 else SAHNE, SCHOKO, SAHNE])
        elif tdx and f < DREHEN_AB + 9:                              # Krümel fahren mit dem Teller hinaus
            for x, farbe in KRUEMEL:
                bild.setze(x + tdx, 13, farbe)
        liste.append(bild)
    return liste
