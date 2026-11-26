"""Schneehasen im Mondschein: Waldlichtung bei Nacht, großer Mond, drei Sterne, dunkle Tannen am
Rand. Zwei Schneehasen (weiß, dunkle Ohrspitzen, dunkles Auge) hoppeln von links und rechts auf die
Lichtung. Der eine macht Männchen und spitzt die Ohren, der andere knabbert an einem Zweig; dann
jagen sie sich im Kreis, einer gräbt eine Mulde in den Schnee und kuschelt sich hinein, der andere
knabbert auch am Zweig und legt sich daneben – eine Sternschnuppe fällt, während sie dösen. Die
Hoppelspuren bleiben im Schnee. Zum Schluss hoppeln beide davon, ein Windstoß verweht die Spuren,
füllt die Mulde und pudert den Zweig neu – Anfang und Ende zeigen dieselbe leere Lichtung, 255 Bilder.

Vor dem dunklen Himmel sind die Hasen weiß; wo sie an Schnee grenzen, bekommen sie einen grauen
Schatten-Umriss, und unter jedem liegt sein Schatten auf dem Schnee.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum einfarbiger Himmel und Schnee, vier gleiche Tannen im
Achtertakt, drei Sterne, kein Schneefall; die Spuren liegen im selben Achtertakt (ein Hopser = acht
Spalten, gleiche Spalten wiederholen sich), die Hasen haben einen geraden Rücken (gleiche
Nachbarspalten).
"""
import math

from basis import B, H, NACHTBLAU, SCHWARZ, WEISS, Bild, dimmen, sternschnuppe

NAME = "schneehase"
TITEL = "Schneehasen im Mondschein"

KANTE_Y = 11                                   # Oberkante des Schnees; darunter vier Zeilen Schnee
KANTE = (215, 225, 250)
BODEN = (78, 90, 140)                          # große Fläche gedämpft
SCHATTEN = (36, 44, 84)                        # Schatten-Umriss der Hasen auf dem Schnee
SPUR = (26, 32, 66)                            # Hoppelspuren: deutlich dunkler als der Schnee
TANNE = (0, 60, 28)
STAMM = (33, 19, 8)
MOND = (240, 230, 170)
STERN = (255, 240, 200)
STERNE = [(19, 2, 0, 51), (39, 1, 30, 85), (47, 1, 50, 51)]         # x, y, Phase, Periode (teilen 255)
TANNEN = (4, 12, 52, 60)                       # vier gleiche im Achtertakt (die Kopien kosten fast nichts)
OHRSPITZE = (50, 50, 60)                       # vor dem Himmel noch als dunkles Grau zu sehen
AUGE = SCHWARZ
ZWEIG = (60, 26, 4)
FARBEN = {"w": WEISS, "e": OHRSPITZE, "a": AUGE}
SCHNEE_FARBEN = (KANTE, BODEN, SPUR)

# Hasen (Blick nach rechts): w Fell, e Ohrspitze, a Auge
HOCKT = ["....e...",
         "....we..",
         "....ww..",
         "....www.",
         "....waww",
         ".wwwwww.",
         "wwwwwww.",
         "wwwwwww."]
GESTRECKT = ["......e...",
             "......we..",
             "......www.",
             ".wwwwwwaww",
             "wwwwwwwww.",
             "ww.....ww."]
SATZ = ["....eww....",                       # im vollen Lauf: Ohren zurückgelegt, Läufe gestreckt
        ".......www.",
        ".wwwwwwwaww",
        "wwwwwwwwww.",
        "w.w.....w.w"]
SATZ_2 = ["....eww....",                     # … und die Läufe unter dem Bauch
          ".......www.",
          "..wwwwwwaww",
          ".wwwwwwwww.",
          "...ww.ww..."]
AUFRICHTEN = ["...e.e.",
              "...w.w.",
              "...www.",
              "...waww",
              "..www..",
              ".wwwww.",
              "wwwww..",
              "wwwww.."]
MAENNCHEN = ["..e.e.",
             "..w.w.",
             "..w.w.",
             "..www.",
             "..waww",
             "..www.",
             ".wwwww",
             ".www..",
             ".www..",
             "wwwww."]
MAENNCHEN_OHR = ["..e...",
                 "..w.e.",
                 "..w.w.",
                 "..www.",
                 "..waww",
                 "..www.",
                 ".wwwww",
                 ".www..",
                 ".www..",
                 "wwwww."]
KNABBERT = ["....e.e.",
            "....w.w.",
            "....www.",
            "....waww",
            "...www..",
            ".wwwww..",
            "wwwww...",
            "wwwww..."]
KNABBERT_2 = ["....e.e.",
              "....w.w.",
              "....www.",
              "....waw.",
              "...wwww.",
              ".wwwww..",
              "wwwww...",
              "wwwww..."]
GRAEBT = ["......e...",                    # Hinterteil hoch, Kopf tief, die Pfoten scharren im Loch
          ".www..we..",
          "wwwwwwwww.",
          "wwwwwwwwaw",
          "ww..wwwww.",
          ".......ww."]
GRAEBT_2 = ["......e...",
            "..ww..we..",
            "wwwwwwwww.",
            "wwwwwwwwaw",
            "ww..wwwww.",
            ".....ww..."]
KUSCHELT = ["......e...",
            "......we..",
            "......www.",
            "..wwwwwaww",
            "wwwwwwwwww"]
SCHLAEFT = ["...ewwww..",                   # in der Mulde, Ohren angelegt
            ".wwwwwwaww",
            "wwwwwwwwww"]
SCHLAEFT_2 = ["..wewwww..",                 # … atmet
              ".wwwwwwaww",
              "wwwwwwwwww"]
DUCKT = ["...ewwww.",                       # flach hingelegt
         ".wwwwwwaw",
         "wwwwwwww."]
DUCKT_2 = ["..wewwww.",
           ".wwwwwwaw",
           "wwwwwwww."]
ZWEIG_X, ZWEIG_Y = 41, 5                       # kahler Zweig mit Schneehäubchen auf beiden Ästen

# Drehbuch
HUPF = 2                                       # Höhe eines Hopsers
SPUR_BREIT = 2                                 # zwei Pfoten nebeneinander
TAKT = 8                                       # Spuren nur in den Spalten 0, 8, 16, … (ein Hopser)
A_KOMMT, A_VON, A_SITZ = 3, -8, 24             # Hase A von links
B_KOMMT, B_VON, B_SITZ = 14, 72, 48            # Hase B von rechts zum Zweig
LUFT, SITZ = 4, 3
A_DA = A_KOMMT + 4 * (LUFT + SITZ)
B_DA = B_KOMMT + 3 * (LUFT + SITZ)
A_HOCH, A_RUNTER = 36, 68                      # Männchen
B_KNABBERT, B_SATT = 42, 74
JAGD = 76                                      # im Kreis: Mitte, Halbachsen, Winkel in Grad
KREIS_X, KREIS_Y, KREIS_RX, KREIS_RY = 32, 11.5, 14, 1.5
# B rennt zuerst los (hinten herum nach links) und endet hinten bei x = 24; A setzt vorn links
# (x = 25) nach und endet hinten bei x = 37 – unterwegs liegen sie sich im Kreis fast gegenüber
A_START, A_WINKEL, A_BOGEN, A_DAUER = JAGD + 3, 240, 549, 70
B_START, B_WINKEL, B_BOGEN, B_DAUER = JAGD, 0, 485, 62
KREIS_SPUREN = [(16, 13), (48, 13), (24, 11), (32, 11), (40, 11), (24, 14), (32, 14), (40, 14)]
RAMPE = 6
A_JAGD_ENDE, B_JAGD_ENDE = A_START + A_DAUER, B_START + B_DAUER
A_RUHE_X, A_LIEGE_X, B_MULDE_X = 37, 36, 24
A_KNABBERT, A_SATT, A_LIEGT = 153, 174, 181
GRABEN, GRABEN_ENDE = 142, 166
KUSCHELN, SCHLAF, B_WACH = 171, 180, 211
SCHNUPPE, A_WACH = 192, 211
A_GEHT, B_GEHT = 214, 217
A_WEG = (40, 48, 56, 64, 72)                   # Landungen beim Davonhoppeln
B_WEG = (32, 40, 48, 56, 64, 72)
WIND, WIND_TEMPO = 231, 3.5


def gerundet(x):
    return int(math.floor(x + 0.5))


def tanne(bild, x, hoehe=8):
    """Tanne aus Stufen (je drei Zeilen), Schnee auf der Spitze."""
    fuss = KANTE_Y
    for k in range(hoehe):
        halb = k // 3 + k % 3
        bild.rechteck(x - halb, fuss - 1 - hoehe + k, 2 * halb + 1, 1, TANNE)
    bild.setze(x, fuss - 1, STAMM)
    bild.setze(x, fuss - 1 - hoehe, KANTE)


def hoppeln(t, orte, luft=LUFT, sitz=SITZ):
    """Hopser von Ort zu Ort (orte[0] = Start), je Hopser luft Bilder in der Luft und sitz am Boden.
    t Bilder seit Beginn → (Mitte, Höhe, in der Luft)."""
    k, u = divmod(t, luft + sitz)
    if k >= len(orte) - 1:
        return orte[-1], 0, False
    a = (u + 1) / (luft + 1) if u < luft else 1.0
    x = orte[k] + (orte[k + 1] - orte[k]) * a
    return x, (gerundet(HUPF * math.sin(math.pi * a)) if u < luft else 0), u < luft


def landungen(start, orte, luft=LUFT, sitz=SITZ):
    """Spuren der Hopser: (ab Bild, x, y)."""
    return [(start + k * (luft + sitz) + luft, x, KANTE_Y) for k, x in enumerate(orte[1:])]


def reihe(von, nach):
    schritt = TAKT if nach > von else -TAKT
    return list(range(von, nach + schritt, schritt))


def anteil(t, dauer, rampe=RAMPE):
    """Weganteil 0..1 mit sanftem Anlauf und Auslauf."""
    t = max(0, min(dauer, t))
    v = 1 / (dauer - rampe)
    if t < rampe:
        return v * t * t / (2 * rampe)
    if t > dauer - rampe:
        return 1 - v * (dauer - t) ** 2 / (2 * rampe)
    return v * (t - rampe / 2)


def kreis_ort(winkel):
    w = math.radians(winkel)
    return KREIS_X + KREIS_RX * math.cos(w), KREIS_Y - KREIS_RY * math.sin(w)


def jagd(t, winkel0, bogen, dauer, sitz_x):
    """Im Kreis: hinten nach links, vorn nach rechts. → (Mitte, Boden, Höhe, Figur, Blick links)."""
    winkel = winkel0 + bogen * anteil(t, dauer)
    x, y = kreis_ort(winkel)
    w = min(1, t / 5)                                                # vom Sitzplatz auf die Bahn
    x, y = sitz_x + (x - sitz_x) * w, 10 + (y - 10) * w
    links = math.sin(math.radians(winkel)) > 0
    schritt = t % 4
    return x, gerundet(y), (0, 1, 1, 0)[schritt], SATZ if schritt in (1, 2) else SATZ_2, links


def hase_a(f):
    """→ (Mitte, Boden, Höhe, Figur, Blick links) oder None."""
    if f < A_KOMMT:
        return None
    if f < A_DA:
        x, hoch, luft = hoppeln(f - A_KOMMT, reihe(A_VON, A_SITZ))
        return x, 10, hoch, GESTRECKT if luft else HOCKT, False
    if f < A_START:
        if A_HOCH + 2 <= f < A_RUNTER:                               # Männchen, die Ohren spielen
            t = f - A_HOCH - 2
            ohr = t in (5, 6, 11, 12, 25, 26)
            return A_SITZ, 10, 0, MAENNCHEN_OHR if ohr else MAENNCHEN, 15 <= t < 23
        if A_HOCH <= f < A_RUNTER + 2:
            return A_SITZ, 10, 0, AUFRICHTEN, False
        return A_SITZ, 10, 0, HOCKT, False
    if f < A_JAGD_ENDE:
        return jagd(f - A_START, A_WINKEL, A_BOGEN, A_DAUER, A_SITZ)
    if f < A_GEHT:
        if A_KNABBERT <= f < A_SATT:
            return A_RUHE_X, 10, 0, KNABBERT if (f // 2) % 2 else KNABBERT_2, False
        if f < A_LIEGT or f >= A_WACH:
            return A_RUHE_X, 10, 0, HOCKT, False
        return A_LIEGE_X, 10, 0, DUCKT_2 if (f + 8) % 16 < 6 else DUCKT, True      # liegt neben der Mulde, atmet
    x, hoch, luft = hoppeln(f - A_GEHT, (A_RUHE_X,) + A_WEG, 3, 1)
    if x > B + 6:
        return None
    return x, 10, hoch, GESTRECKT if luft else HOCKT, False


def hase_b(f):
    if f < B_KOMMT:
        return None
    if f < B_DA:
        x, hoch, luft = hoppeln(f - B_KOMMT, reihe(B_VON, B_SITZ))
        return x, 10, hoch, GESTRECKT if luft else HOCKT, True
    if f < B_START:
        if B_KNABBERT <= f < B_SATT:
            return B_SITZ, 10, 0, KNABBERT if (f // 2) % 2 else KNABBERT_2, True
        return B_SITZ, 10, 0, HOCKT, True
    if f < B_JAGD_ENDE:
        return jagd(f - B_START, B_WINKEL, B_BOGEN, B_DAUER, B_SITZ)
    if f < GRABEN:
        return B_MULDE_X, 10, 0, HOCKT, True
    if f < GRABEN_ENDE:
        return B_MULDE_X, 11, 0, GRAEBT if (f // 2) % 2 else GRAEBT_2, True
    if f < KUSCHELN:
        return B_MULDE_X, 10, 0, HOCKT, f < GRABEN_ENDE + 2
    if f < B_GEHT:
        if SCHLAF <= f < B_WACH:
            return B_MULDE_X, 11, 0, SCHLAEFT_2 if f % 16 < 6 else SCHLAEFT, False
        return B_MULDE_X, 11, 0, KUSCHELT, False
    x, hoch, luft = hoppeln(f - B_GEHT, (B_MULDE_X,) + B_WEG, 3, 1)
    if x > B + 6:
        return None
    return x, 10, hoch, GESTRECKT if luft else HOCKT, False


def spuren_liste():
    """Alle Spuren als (ab Bild, x, y): Landungen beim Hoppeln und Tupfen auf der Kreisbahn –
    alle in Spalten im Achtertakt, damit sich die Spalten wiederholen."""
    liste = landungen(A_KOMMT, reihe(A_VON, A_SITZ)) + landungen(B_KOMMT, reihe(B_VON, B_SITZ))
    liste += landungen(A_GEHT, (A_RUHE_X,) + A_WEG, 3, 1) + landungen(B_GEHT, (B_MULDE_X,) + B_WEG, 3, 1)
    for x, y in KREIS_SPUREN:                                        # Kreisbahn: sobald ein Hase vorbeikommt
        winkel = math.degrees(math.acos(max(-1, min(1, (x - KREIS_X) / KREIS_RX))))
        if y > 13:                                                   # vorn
            winkel = 360 - winkel
        ab = None
        for f in range(JAGD, A_JAGD_ENDE):
            for start, winkel0, bogen, dauer in ((A_START, A_WINKEL, A_BOGEN, A_DAUER),
                                                 (B_START, B_WINKEL, B_BOGEN, B_DAUER)):
                if f >= start and ab is None:
                    weit = winkel0 + bogen * anteil(f - start, dauer)
                    if any(winkel0 < winkel + 360 * n <= weit for n in range(3)):
                        ab = f
        liste.append((ab, x, y))
    return liste


SPUREN = spuren_liste()


def hase(bild, mitte, boden, hoch, figur, links):
    """Weißer Hase; wo er an Schnee grenzt, ein grauer Schatten-Umriss, darunter sein Schatten."""
    breite = len(figur[0])
    x0 = gerundet(mitte - breite / 2)
    y0 = boden - hoch - len(figur) + 1
    punkte = {}
    for dy, zeile in enumerate(figur):
        for dx, c in enumerate(zeile):
            if c != ".":
                punkte[(x0 + (breite - 1 - dx if links else dx), y0 + dy)] = FARBEN[c]
    for x in range(x0 + 1, x0 + breite - 1):                         # Schatten auf dem Schnee
        if bild.hole(x, boden + 1) in SCHNEE_FARBEN:
            bild.setze(x, boden + 1, SCHATTEN)
    for x, y in punkte:
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) not in punkte and bild.hole(nx, ny) in SCHNEE_FARBEN:
                bild.setze(nx, ny, SCHATTEN)
    for (x, y), farbe in punkte.items():
        bild.setze(x, y, farbe)


def zweig(bild, f, wind_x):
    """Kahler Zweig; das Schneehäubchen fällt, wenn ein Hase knabbert, der Wind pudert ihn neu."""
    bild.rechteck(ZWEIG_X + 1, ZWEIG_Y + 3, 1, 3, ZWEIG)
    for dx, oben, knabbert, satt in ((2, ZWEIG_Y, B_KNABBERT, B_SATT), (0, ZWEIG_Y + 1, A_KNABBERT, A_SATT)):
        zupft = knabbert <= f < satt and (f // 2) % 4 == 0           # der Ast wird kurz heruntergezogen
        bild.rechteck(ZWEIG_X + dx, oben + zupft, 1, ZWEIG_Y + 3 - oben - zupft, ZWEIG)
        if f < knabbert + 6 or wind_x > ZWEIG_X + dx:
            bild.setze(ZWEIG_X + dx, oben - 1 + zupft, KANTE)
        elif f < knabbert + 9:                                       # das Häubchen fällt in die Astgabel
            bild.setze(ZWEIG_X + 1, ZWEIG_Y + f - knabbert - 6, KANTE)


def landschaft(bild, f):
    for x, y, phase, periode in STERNE:                              # wenige Sterne, funkeln langsam
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    sternschnuppe(bild, f, SCHNUPPE, 27, 0)                          # während die Hasen dösen
    bild.kreis(32, 3, 3, MOND)
    for x in TANNEN:
        tanne(bild, x)
    bild.rechteck(0, KANTE_Y, B, 1, KANTE)
    bild.rechteck(0, KANTE_Y + 1, B, H - KANTE_Y - 1, BODEN)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        landschaft(bild, f)
        wind_x = (f - WIND) * WIND_TEMPO if f >= WIND else -1
        # Mulde: dunkle Lücke in der Schneekante, rechts und links ein Häufchen
        stufe = 0 if f < GRABEN + 4 else min(3, 1 + (f - GRABEN - 4) // 6)
        if stufe and B_MULDE_X + 4 > wind_x:
            halb = (0, 2, 3, 4)[stufe]
            bild.rechteck(B_MULDE_X - halb, KANTE_Y, 2 * halb + 1, 1, SCHATTEN)
            if stufe >= 2:                                           # Aushub rechts, dann auch links
                bild.rechteck(B_MULDE_X + halb + 1, KANTE_Y - 1, 2, 1, KANTE)
            if stufe >= 3:
                bild.rechteck(B_MULDE_X - halb - 2, KANTE_Y - 1, 2, 1, KANTE)
        # Spuren
        for ab, x, y in SPUREN:
            if ab is not None and f >= ab and x > wind_x:
                for dx in range(SPUR_BREIT):
                    if bild.hole(x + dx, y) in SCHNEE_FARBEN:
                        bild.setze(x + dx, y, SPUR)
        hasen = [h for h in (hase_a(f), hase_b(f)) if h]
        hasen.sort(key=lambda h: h[1])
        for h in hasen:
            if h[1] <= 10:
                hase(bild, *h)
        zweig(bild, f, wind_x)
        for h in hasen:
            if h[1] > 10:
                hase(bild, *h)
        if GRABEN <= f < GRABEN_ENDE:                                # Schnee fliegt nach hinten
            for k in range(2):
                u = (f + 2 * k) % 4
                bild.setze(B_MULDE_X + 5 + 2 * u, 9 - (1, 2, 2, 1)[u], KANTE)
        if 0 <= wind_x < B + 8:                                      # Windstoß: Schneestaub
            for k, (dx, dy) in enumerate(((0, 0), (-2, -1), (-5, 0), (-7, -2))):
                bild.setze(wind_x + dx, KANTE_Y - 1 + dy - (f + k) % 2, KANTE)
        liste.append(bild)
    return liste
