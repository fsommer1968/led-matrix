"""Weihnachtsmann steckt im Schornstein fest: verschneites Dach bei Nacht mit Mond, links parkt der
Schlitten mit dem Geschenksack, rechts wartet das Rentier. Der Weihnachtsmann steigt aus, springt in
den Schornstein und bleibt mit dem dicken Bauch stecken. Er zappelt und stemmt sich, das Rentier
stupst ihn zweimal mit der Nase, nimmt Anlauf – und mit einem Ruck flutscht er hinein; die Mütze
schwebt noch einen Augenblick und fällt hinterher. Eine Rußwolke pufft dem Rentier ins Gesicht (es
schüttelt sich), dann steigt warmer Rauch auf, und in den Dachfenstern blinkt es bunt: Bescherung.
Am Ende taucht der Weihnachtsmann rußig wieder auf (das Rentier hüpft vor Vergnügen), springt
heraus, stapft zum Schlitten, setzt sich und schüttelt den Ruß ab; die Fenster werden wieder matt.
Die Runde schließt ohne Sprung – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ein waagerechter First (alle Dachspalten gleich),
Schornstein und Schlitten aus Rechtecken, das Rentier mit gleichen Rumpfspalten, Vollmond,
drei Sterne, zwei gleiche Dachfenster, Ruß und Rauch als Blöcke statt einzelner Flocken.
Sterne und Nasenglimmen laufen in Perioden, die 255 teilen (51, 85, 15).
"""
from basis import HAUT, NACHTBLAU, ROT, WEISS, B, Bild, dimmen, mischen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "weihnachtsmann_kamin"
TITEL = "Weihnachtsmann steckt im Schornstein fest"

KANTE = (215, 225, 250)                        # Schnee auf dem First
SCHNEE_MATT = (78, 90, 140)                    # darunter gedämpft (große Fläche)
DACH = (120, 28, 22)                           # Ziegel unter dem Schnee
ZIEGEL = (165, 55, 28)
FUGE = (95, 32, 20)
RAND = (215, 120, 60)                          # Kranz oben am Schornstein
MOND = (240, 230, 170)
STERN = (255, 240, 200)
STERNE = [(17, 1, 0, 51), (24, 5, 20, 85), (46, 0, 40, 51)]          # x, y, Phase, Periode (teilt 255)
FELL = (66, 36, 12)
FELL_DUNKEL = (33, 18, 7)
GEWEIH = (220, 175, 105)
AUGE = (50, 25, 10)
NASE_MATT = (255, 80, 50)                      # die rote Nase glimmt im Wechsel
KUFE = (255, 190, 0)
SCHLITTEN = (0, 150, 60)
SACK = (49, 31, 11)
STIEFEL = (75, 75, 95)
RUSS = (105, 100, 110)                         # Rußwolke
RUSS_ROT = (150, 34, 28)                       # rußiger Mantel
RUSS_WEISS = (125, 125, 138)                   # rußiger Bart
RUSS_FELL = (90, 80, 80)                       # rußiger Rentierkopf
FENSTER_MATT = (120, 75, 15)                   # Dachfenster: Nachtlicht
FENSTER_AN = (255, 190, 50)                    # … und hell nach der Bescherung
BESCHERUNG = ((255, 0, 160), (0, 255, 170))    # dazwischen blinkt es bunt (Baumlichter)
FENSTER = (21, 44)                             # linke Kanten der beiden Dachfenster, je 4 breit
RAUCH = ((230, 130, 50), (200, 130, 80), (165, 130, 110), (135, 125, 125), (105, 100, 110),
         (80, 78, 90), (55, 55, 68))           # warmer Rauch kühlt beim Aufsteigen ab

FIRST = 12                                     # Zeile der Schneekante; die Figuren stehen darauf
KAMIN_X, KAMIN_B = 30, 9                       # Schornstein: links, Breite; Kranz je 1 breiter
KRANZ_Y = 7                                    # Zeile des Kranzes, Schaft darunter bis zum First
MITTE = KAMIN_X + KAMIN_B // 2                 # 34

# Weihnachtsmann von der Seite (Blick nach rechts), 6 breit; der Pelzsaum kostet keine eigene Spalte
OBEN = ["wrrr..", ".rrrr.", ".hhah.", ".wwww.", "rrrrrr", "rrrrrr", "wwwwww"]
SITZT = OBEN
GEHT = [OBEN + [".bb.bb", ".bb.bb"], OBEN + ["..bb..", "..bb.."]]
# von vorn im Schornstein, 11 breit: der Bauch quillt über den Schaft; g Handschuhe
HOCH = ["....rrrw...", "...rrrrr...", "g..wwwww..g", "r..hahah..r", ".r.wwwww.r.", "..rrwwwrr..",
        ".rrrrrrrrr."]
TIEF = ["....rrrw...", "...rrrrr...", "...wwwww...", "...hahah...", "...wwwww...", ".rrrwwwrrr.",
        "grrrrrrrrrg"]
LINKS = ["....rrrw...", "...rrrrr...", "g..wwwww...", "r..hahah...", ".r.wwwww...", "..rrwwwrrr.",
         ".rrrrrrrrrg"]
RECHTS = [z[::-1] for z in LINKS]              # gespiegelt: auch der Zipfel kippt auf die andere Seite
# rutscht hinein: Arme senkrecht nach oben, ohne Mütze (die schwebt noch)
RUTSCHT = [".g.......g.", ".r..hhh..r.", ".r.hhhhh.r.", ".r.hahah.r.", ".r.wwwww.r.", ".rrrwwwrrr.",
           ".rrrrrrrrr."]
MUETZE = ["....rrrw...", "...rrrrr...", "...wwwww..."]
# taucht auf: Arme noch im Schaft
TAUCHT = ["....rrrw...", "...rrrrr...", "...wwwww...", "...hahah...", "...wwwww...", "..rrwwwrr..",
          ".rrrrrrrrr."]

# Rentier (Blick nach links), 12 breit: die Rumpfspalten zwischen den Läufen sind gleich; k Kopf
RENTIER = ["g.g.........", ".gg.........", ".kkk........", "nkak........", ".fffffffffff",
           "...ffffffff.", "...ffffffff.", "...f.d..d.f.", "...f.d..d.f."]
RENTIER_GEHT = RENTIER[:7] + ["...f.d..d.f.", "....d....d.."]

# ── Ablauf ─────────────────────────────────────────────────────────
X_SITZ, X_KAMIN = 6, 22                        # linke Kante des Weihnachtsmanns: im Schlitten, am Schornstein
T_AUF, T_LOS = 8, 11                           # steigt aus, geht los
T_DA = T_LOS + X_KAMIN - X_SITZ                # 27: steht vor dem Schornstein
T_SPRUNG, T_STECKT = 31, 41                    # springt, steckt fest
T_KOMMT, T_STUPS1, T_STUPS2 = 68, 86, 96       # Rentier kommt näher, stupst zweimal
T_ANLAUF, T_RUCK = 102, 117                    # Rentier nimmt Anlauf, Ruck
T_MUETZE = T_RUCK + 7                          # die Mütze fällt hinterher
T_WEG = T_MUETZE + 3                           # 127: alles im Schornstein, Rußwolke
T_SCHEUT, T_RENTIER_SCHUETTELT = 129, 142      # Rentier weicht zurück, schüttelt den Ruß ab
T_RAUCH, T_RAUCH_LETZTER = 142, 166            # warmer Rauch: erstes und letztes Wölkchen
T_BESCHERUNG = 150                             # im Haus gehen die Lichter an
T_HERAUS, T_OBEN, T_ABSPRUNG = 190, 197, 207   # taucht rußig auf, zappelt und stemmt sich, springt
T_UNTEN = T_ABSPRUNG + 10                      # 217: steht wieder auf dem Dach
T_ZURUECK = T_UNTEN + X_KAMIN - X_SITZ         # 233: am Schlitten
T_SITZT, T_SCHUETTELN, T_SAUBER = 237, 239, 245
RENTIER_RUHE, RENTIER_NAH = 45, 41             # linke Kante des Rentiers


def sprung(t, x0, x1, y0, y1, hoch=3):
    """Bogen von (x0, y0) nach (x1, y1), t von 0 bis 1."""
    return round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t - hoch * 4 * t * (1 - t))


def rentier_x(f):
    """Linke Kante des Rentiers und ob es gerade läuft."""
    if f < T_KOMMT:
        return RENTIER_RUHE, False
    if f < T_KOMMT + 10:                                             # kommt neugierig näher
        return RENTIER_RUHE - (f - T_KOMMT + 1) // 2, True
    if f < T_ANLAUF:                                                 # stupst zweimal
        stups = T_STUPS1 <= f < T_STUPS1 + 3 or T_STUPS2 <= f < T_STUPS2 + 3
        return RENTIER_NAH - 2 * stups, False
    if f < T_ANLAUF + 8:                                             # nimmt Anlauf: zurück …
        return RENTIER_NAH + (f - T_ANLAUF + 1) // 2, True
    if f < T_RUCK - 3:
        return RENTIER_RUHE, False
    if f < T_RUCK:                                                   # … und los
        return RENTIER_RUHE - (f - (T_RUCK - 3) + 1) * 2, True
    if f < T_SCHEUT:
        return RENTIER_NAH - 2 if f < T_RUCK + 2 else RENTIER_NAH, False
    if f < T_SCHEUT + 10:                                            # weicht vor dem Ruß zurück
        return min(RENTIER_RUHE, RENTIER_NAH + (f - T_SCHEUT + 1) // 2), True
    if T_RENTIER_SCHUETTELT <= f < T_RENTIER_SCHUETTELT + 8:         # schüttelt den Ruß ab
        return RENTIER_RUHE + (f - T_RENTIER_SCHUETTELT) // 2 % 2, False
    return RENTIER_RUHE, False


def steckt(f):
    """Haltung, dx, dy des feststeckenden Weihnachtsmanns."""
    u = f - T_STECKT
    if u < 6:                                                        # verdutzt
        return HOCH, 0, 0
    if u < 30:                                                       # zappelt
        return (LINKS if (u // 3) % 2 else RECHTS), 0, 0
    if u < 44:                                                       # stemmt sich hoch – vergeblich
        return TIEF, 0, -1 if 34 <= u < 40 else 0
    for start in (T_STUPS1, T_STUPS2):                               # wird gestupst
        if start <= f < start + 3:
            return LINKS, -1, 0
    if f >= T_RUCK - 3:                                              # das Rentier kommt angerannt!
        return HOCH, 0, 0
    if f >= T_STUPS2 + 3:                                            # ergibt sich
        return TIEF, 0, 0
    return (HOCH if (u // 4) % 2 else TIEF), 0, 0                    # winkt das Rentier heran


def fenster(f):
    """Farbe der Dachfenster: Nachtlicht, zur Bescherung bunt blinkend, dann hell, am Ende wieder matt."""
    if f < T_BESCHERUNG or f >= T_SAUBER:
        return FENSTER_MATT
    if f >= T_SITZT:                                                 # das Haus geht schlafen
        return mischen(FENSTER_AN, FENSTER_MATT, 0.5)
    k = f - T_BESCHERUNG
    if k < 36 and k // 4 % 2:                                        # Baumlichter blinken bunt
        return BESCHERUNG[k // 8 % 2]
    return FENSTER_AN


def wolke(bild, cx, y, halb, h, farbe):
    """Block mit abgeschnittenen Ecken, 2·halb+1 breit, h hoch."""
    bild.rechteck(cx - halb, y, 2 * halb + 1, h, farbe)
    for x in (cx - halb, cx + halb):
        bild.setze(x, y, NACHTBLAU)
        bild.setze(x, y + h - 1, NACHTBLAU)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        bild.kreis(58, 3, 2.2, MOND)
        russig = T_RUCK <= f < T_SAUBER
        farben = {"r": RUSS_ROT if russig else ROT, "w": RUSS_WEISS if russig else WEISS,
                  "g": RUSS_WEISS if russig else WEISS, "h": dimmen(HAUT, 0.75) if russig else HAUT,
                  "a": AUGE, "b": STIEFEL}
        sauber = {"r": ROT, "w": WEISS, "g": WEISS, "h": HAUT, "a": AUGE}

        # hinter dem Schornstein: Sprung hinein, Feststecken, Hineinrutschen, Auftauchen, Sprung heraus
        if T_SPRUNG <= f < T_STECKT:
            x, y = sprung((f - T_SPRUNG + 1) / (T_STECKT - T_SPRUNG), X_KAMIN, MITTE - 3, 3, 1)
            bild.figur(x, y, GEHT[0], farben)
        elif T_STECKT <= f < T_RUCK:
            figur, dx, dy = steckt(f)
            bild.figur(MITTE - 5 + dx, dy, figur, farben)
        elif T_RUCK <= f < T_WEG:                                    # flutscht hinein, die Mütze hinterher
            bild.figur(MITTE - 5, (f - T_RUCK + 1) * 2, RUTSCHT, sauber)
            bild.figur(MITTE - 5, max(0, f - T_MUETZE + 1) * 3, MUETZE, sauber)
        elif T_HERAUS <= f < T_OBEN:                                 # taucht wieder auf
            bild.figur(MITTE - 5, T_OBEN - f, TAUCHT, farben)
        elif T_OBEN <= f < T_ABSPRUNG - 4:                           # steckt schon wieder: zappelt kurz
            bild.figur(MITTE - 5, 0, LINKS if (f - T_OBEN) // 3 % 2 else RECHTS, farben)
        elif T_ABSPRUNG - 4 <= f < T_ABSPRUNG:                       # … und stemmt sich heraus
            bild.figur(MITTE - 5, -1 if f >= T_ABSPRUNG - 2 else 0, TIEF, farben)
        elif T_ABSPRUNG <= f < T_UNTEN:
            x, y = sprung((f - T_ABSPRUNG + 1) / (T_UNTEN - T_ABSPRUNG), MITTE - 3, X_KAMIN, 1, 3)
            bild.figur(x, y, GEHT[0], farben, spiegeln=True)

        # Dach und Schornstein
        bild.rechteck(0, FIRST, B, 1, KANTE)
        bild.rechteck(0, FIRST + 1, B, 1, SCHNEE_MATT)
        bild.rechteck(0, FIRST + 2, B, 2, DACH)
        for x in FENSTER:
            bild.rechteck(x, FIRST + 2, 4, 2, fenster(f))
        bild.rechteck(KAMIN_X, KRANZ_Y + 1, KAMIN_B, FIRST - KRANZ_Y - 1, ZIEGEL)
        bild.rechteck(KAMIN_X, KRANZ_Y + 3, KAMIN_B, 1, FUGE)
        bild.rechteck(KAMIN_X - 1, KRANZ_Y, KAMIN_B + 2, 1, RAND)

        # Schlitten mit Sack, der Weihnachtsmann sitzt darin
        if f < T_AUF or f >= T_SITZT:
            wackeln = (f - T_SCHUETTELN) // 2 % 2 if T_SCHUETTELN <= f < T_SAUBER else 0
            bild.figur(X_SITZ + wackeln, 2, SITZT, farben)
        bild.rechteck(2, 6, 3, 3, SACK)
        bild.setze(3, 5, SACK)
        bild.rechteck(1, 6, 1, 3, SCHLITTEN)                         # Lehne
        bild.rechteck(1, 9, 12, 2, SCHLITTEN)
        bild.rechteck(0, 11, 14, 1, KUFE)
        bild.rechteck(13, 9, 1, 2, KUFE)                             # Kufe vorn hochgebogen

        # Rentier: bekommt die Rußwolke ab und schüttelt sie am Platz wieder aus dem Fell
        rx, laeuft = rentier_x(f)
        kopf = RUSS_FELL if T_WEG + 2 <= f < T_RENTIER_SCHUETTELT + 5 else FELL
        kichert = f - T_OBEN in (1, 2, 5, 6)                         # hüpft, als der Rußmann auftaucht
        bild.figur(rx, 3 - kichert, RENTIER_GEHT if laeuft and (f // 2) % 2 else RENTIER,
                   {"g": GEWEIH, "f": FELL, "k": kopf, "d": FELL_DUNKEL, "a": AUGE,
                    "n": ROT if f % 15 < 8 else NASE_MATT})
        if not laeuft and not kichert and f % 51 in (30, 31, 32, 36, 37, 38):   # wedelt ab und zu
            bild.setze(rx + 11, 7, NACHTBLAU)
            bild.setze(rx + 11, 6, FELL)
        k = f - T_RENTIER_SCHUETTELT
        if 1 <= k < 9:
            for dx, dy in ((-1, 1), (4, 0)):
                bild.setze(RENTIER_RUHE + dx + (dx > 0) * k // 2 - (dx < 0) * k // 2, 4 + dy - k // 3, RUSS)

        # Weihnachtsmann zu Fuß
        if T_AUF <= f < T_SPRUNG:
            x = min(X_KAMIN, X_SITZ + max(0, f - T_LOS + 1))
            bild.figur(x, 3, GEHT[(f // 3) % 2 if T_LOS <= f < T_DA else 0], farben)
        elif T_UNTEN <= f < T_SITZT:
            x = max(X_SITZ, X_KAMIN - (f - T_UNTEN + 1))
            bild.figur(x, 3, GEHT[(f // 3) % 2 if f < T_ZURUECK else 0], farben, spiegeln=f < T_ZURUECK + 2)

        # Schnee stiebt vom Kranz, wenn er aufsetzt, gestupst wird oder herausspringt
        for start in (T_STECKT, T_STUPS1, T_STUPS2, T_RUCK, T_ABSPRUNG):
            k = f - start
            if 0 <= k < 4:
                for seite in (-1, 1):
                    bild.setze(MITTE + seite * (7 + k), KRANZ_Y - 1 - k + k // 3, dimmen(WEISS, 1 - k * 0.2))
        # Rußwolke nach dem Hineinrutschen: quillt heraus und zieht dem Rentier ins Gesicht
        k = f - T_WEG
        if 0 <= k < 4:
            wolke(bild, MITTE, 4, 3, 3, RUSS)
        elif 4 <= k < 8:
            wolke(bild, MITTE + 1, 2, 4, 4, RUSS)
        elif 8 <= k < 12:
            wolke(bild, MITTE + 2, 0, 4, 4, dimmen(RUSS, 0.75))
        elif 12 <= k < 16:
            wolke(bild, MITTE + 3, -1, 3, 3, dimmen(RUSS, 0.5))
        # warmer Rauch: Wölkchen steigen auf, werden größer, kühlen ab und ziehen nach rechts
        for start in range(T_RAUCH, T_RAUCH_LETZTER + 1, 12):
            k = f - start
            if 0 <= k < 28:
                stufe = k // 4                                       # 0 … 6
                bild.rechteck(MITTE - 1 + stufe // 2, 5 - stufe, 3 + stufe // 3, 2, RAUCH[stufe])
        # Ruß fliegt beim Schütteln davon
        k = f - T_SCHUETTELN
        if 0 <= k < 9:
            for dx, dy in ((-2, 0), (7, 1), (2, -3)):
                bild.setze(X_SITZ + dx + (dx > 0) * k // 2 - (dx < 0) * k // 2, 3 + dy - k // 3 + (k % 2), RUSS)
        liste.append(bild)
    return liste
