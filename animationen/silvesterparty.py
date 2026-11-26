"""Silvesterparty hinter dem Fenster: Von außen sieht man nachts eine Hauswand mit drei großen, warm
erleuchteten Fenstern. Dahinter feiern sechs Leute mit bunten Partyhütchen – sie wippen im Takt,
machen einen Schritt zur Seite und reißen die Arme hoch, unter der Decke glitzert die Discokugel und
schickt bunte Lichtpunkte durch den Raum, in den Fensterecken wiegen sich Luftschlangen. Rechts heben
zwei ihre Sektgläser, stoßen an (es blitzt) und trinken. Zweimal zieht draußen eine kleine Rakete am
Fenster vorbei; oben platzt sie, ihr Widerschein färbt kurz Wand und Schnee, und drinnen jubeln
alle. Am Ende wippen alle weiter wie am Anfang – die Runde geht ohne Sprung in sich über. 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum sind Wand, Fensterlicht und Fensterbank einfarbig, alle
Gäste haben dieselbe Form (fünf Spalten, spiegelgleich), je zwei teilen sich Hemd- und Hutfarbe,
gehobene Arme stehen senkrecht in den Schulterspalten (keine neue Spaltenform), die Gläser sind nur
beim Anstoßen zu sehen, die vier Luftschlangen sind Kopien voneinander, und nur sechs Lichtpunkte
wandern. Die Plätze der Gäste und die Bahnen der Punkte sind nach der Größe ausgesucht (schon eine
Spalte daneben kostet bis zu 800 Bytes mehr).
"""
from basis import B, GELB, HAUT, LILA, PINK, ROT, WEISS, Bild, mischen

NAME = "silvesterparty"
TITEL = "Silvesterparty hinter dem Fenster"

WAND = (18, 16, 38)                            # Hauswand bei Nacht
LICHT = (125, 78, 16)                          # warmes Licht im Zimmer (große Fläche, gedämpft)
SIMS = (125, 135, 175)                         # Fensterbank mit Schnee
BLAU = (0, 70, 255)
GRUEN = (0, 200, 40)
TUERKIS = (0, 230, 190)
KUGEL = (120, 130, 160)                        # Discokugel
SEKT = (255, 235, 150)
FUNKE = (255, 150, 0)
GLUT = (160, 50, 0)
AUGE = (0, 0, 0)                               # Augen: LED aus

FENSTER = (4, 24, 44)                          # linke Spalte der drei Fenster
FB = 16                                        # Fensterbreite
OBEN, UNTEN = 1, 13                            # Fenster: Zeilen 1 … 13, Fensterbank in Zeile 14

RUNDE = 255
TAKTE = 64                                     # halbe Takte je Runde (je etwa 4 Bilder)

# Tänzer: linke Spalte des Körpers (5 breit), Hut, Hemd, Taktversatz, kleiner (0/1), Armfolge je
# Abschnitt (8 halbe Takte): 0 unten, 1 im Takt hoch, 3 links/rechts im Wechsel; Seitschritt
# (Richtung, Versatz in halben Takten)
GAESTE = [(6, GELB, BLAU, 0, 0, (0, 1, 0, 3, 0, 1, 0, 3), (1, 2)),
          (13, LILA, PINK, 1, 1, (1, 0, 3, 0, 1, 0, 3, 0), (0, 0)),
          (24, ROT, GRUEN, 0, 0, (0, 3, 0, 1, 0, 3, 0, 1), (1, 6)),
          (34, GELB, PINK, 1, 1, (3, 0, 1, 0, 3, 0, 1, 0), (1, 6))]
# rechts die beiden mit den Gläsern: Körper, Hut, Hemd, Seite zur Mitte
PAAR = [(46, LILA, GRUEN, 1), (53, ROT, BLAU, -1)]
ANSTOSSEN = (96, 204)                          # Beginn der beiden Male
# Ablauf des Anstoßens: (bis Bild, Haltung)
ABLAUF = [(3, "brust"), (7, "hoch"), (16, "stoss"), (19, "hoch"), (33, "trinken"), (36, "brust")]
BLITZ = (7, 12)                                # in diesen Bildern blitzt es über den Gläsern
# Raketen: Start, Spalte unten, Richtung, Farbe des Sterns
RAKETEN = [(36, 17, 1, PINK), (150, 46, -1, TUERKIS)]
FLUG = 24                                      # so viele Bilder ist die Rakete zu sehen
JUBEL = 14                                     # danach reißen alle die Arme hoch
SCHEIN = (0.32, 0.32, 0.24, 0.24, 0.24, 0.16, 0.16, 0.16, 0.08, 0.08, 0.08)   # Widerschein je Bild
# Luftschlangen (Zickzack, zwei Spalten): Spalte, Länge, Farbe – alle gleich, das kostet fast nichts
LUFTSCHLANGEN = [(4, 5, TUERKIS), (18, 5, TUERKIS), (44, 5, TUERKIS), (58, 5, TUERKIS)]
KUGEL_X = 30                                   # Discokugel: Spalten 30 … 33, Zeilen 1 … 4
# Lichtpunkte der Discokugel: Zeile, Startspalte, Farbe, Umläufe je Runde (Vorzeichen = Richtung).
# Türkis läuft unterhalb der Luftschlangen, sonst sähe der Punkt wie ein Stück davon aus.
PUNKTE = [(2, 2, PINK, 1), (3, 8, GRUEN, -1), (5, 34, BLAU, 2), (7, 52, TUERKIS, -2), (8, 57, WEISS, 1),
          (4, 8, WEISS, -1)]


def takt(f, versatz=0):
    """Nummer des halben Takts; 64 je Runde, damit die Runde aufgeht."""
    return (f * TAKTE // RUNDE + versatz) % TAKTE


def gast(bild, x, y, hut, hemd, links=False, rechts=False, glas=None, seite=1):
    """Gast von vorn: Spitzhut, Gesicht mit zwei Augen, Hemd bis zur Fensterbank; y = Hutspitze.
    Gehobene Arme stehen in den Schulterspalten neben dem Kopf, die Hand neben der Hutspitze.
    glas: Haltung des Arms mit dem Sektglas auf der Seite zur Mitte."""
    bild.rechteck(x + 2, y, 1, 2, hut)
    bild.rechteck(x + 1, y + 2, 3, 1, hut)
    bild.rechteck(x + 1, y + 3, 3, 3, HAUT)
    bild.setze(x + 1, y + 4, AUGE)
    bild.setze(x + 3, y + 4, AUGE)
    bild.rechteck(x, y + 6, 5, UNTEN + 1 - (y + 6), hemd)
    for oben, spalte in ((links, x), (rechts, x + 4)):
        if oben:
            bild.rechteck(spalte, y + 1, 1, 5, hemd)
            bild.setze(spalte, y, HAUT)
    s = x + 4 if seite > 0 else x                                    # Schulterspalte zur Mitte hin
    if glas == "brust":                                              # Glas kommt vor der Brust hoch
        bild.rechteck(s, y + 6, 1, 2, SEKT)
    elif glas == "hoch":                                             # erhoben: Glas über der Hand
        bild.rechteck(s, y + 1, 1, 5, hemd)
        bild.setze(s, y, HAUT)
        bild.rechteck(s, y - 2, 1, 2, SEKT)
    elif glas == "stoss":                                            # Arm zur Mitte: die Gläser berühren sich
        bild.rechteck(s, y + 4, 1, 2, hemd)
        bild.rechteck(s + seite, y + 2, 1, 2, hemd)
        bild.setze(s + seite, y + 1, HAUT)
        bild.rechteck(s + seite, y - 1, 1, 2, SEKT)
    elif glas == "trinken":                                          # Glas am Mund
        bild.rechteck(s, y + 3, 1, 2, SEKT)
        bild.setze(s, y + 5, HAUT)


def bilder():
    liste = []
    for f in range(RUNDE):
        # Rakete oben geplatzt: Widerschein auf Wand und Schnee, drinnen Jubel
        wand, sims, jubel = WAND, SIMS, False
        for start, _, _, farbe in RAKETEN:
            t = f - start - FLUG
            if 0 <= t < len(SCHEIN):
                wand = mischen(WAND, farbe, SCHEIN[t])
                sims = mischen(SIMS, farbe, SCHEIN[t] * 1.5)         # der Schnee wirft das Licht stärker zurück
            jubel = jubel or 0 <= t < JUBEL
        bild = Bild(wand)
        for fx in FENSTER:
            bild.rechteck(fx, OBEN, FB, UNTEN - OBEN + 1, LICHT)
            bild.rechteck(fx, UNTEN + 1, FB, 1, sims)
        wiegen = takt(f) // 4 % 2                                    # Luftschlangen wiegen sich langsam
        for x, laenge, farbe in LUFTSCHLANGEN:
            for k in range(laenge):
                bild.setze(x + (k + wiegen) % 2, OBEN + k, farbe)
        # wandernde Lichtpunkte, nur auf der Zimmerwand (hinter den Gästen)
        for y, x0, farbe, umlaeufe in PUNKTE:
            x = (x0 + f * B * umlaeufe // RUNDE) % B
            if bild.hole(x, y) == LICHT:
                bild.setze(x, y, farbe)
        # Discokugel im mittleren Fenster, der Glanzpunkt läuft herum
        bild.rechteck(KUGEL_X + 1, OBEN, 2, 4, KUGEL)
        bild.rechteck(KUGEL_X, OBEN + 1, 4, 2, KUGEL)
        glanz = takt(f) % 4
        bild.setze(KUGEL_X + glanz, OBEN + 1 + glanz % 2, WEISS)
        # Tänzer
        for x, hut, hemd, versatz, kleiner, folge, (seit, wann) in GAESTE:
            n = takt(f, versatz)
            hoch = n % 2
            art = folge[n // 8]
            links = rechts = False
            if jubel:
                links = rechts = True
            elif art == 1:
                links = rechts = bool(hoch)
            elif art == 3:
                links, rechts = n // 2 % 2 == 0, n // 2 % 2 == 1
            x += seit * ((n + wann) // 4 % 2)                        # Schritt zur Seite und zurück
            gast(bild, x, 3 + kleiner - hoch, hut, hemd, links, rechts)
        # das Paar mit den Gläsern: wiegt sich im halben Tempo, hebt die Gläser, stößt an, trinkt
        u = min([f - s for s in ANSTOSSEN if f >= s] or [99])
        haltung = next((h for bis, h in ABLAUF if u < bis), None)
        for x, hut, hemd, seite in PAAR:
            if haltung:
                gast(bild, x, 3, hut, hemd, glas=haltung, seite=seite)
            else:
                gast(bild, x, 3 - takt(f) // 2 % 2, hut, hemd, jubel, jubel)
        if haltung == "stoss" and BLITZ[0] <= u < BLITZ[1]:
            mitte = PAAR[0][0] + 5
            if u - BLITZ[0] < 3:                                     # erst über den Gläsern …
                bild.rechteck(mitte, 1, 2, 1, WEISS)
            else:                                                    # … dann springt der Blitz zur Seite
                bild.setze(mitte - 1, 1, WEISS)
                bild.setze(mitte + 2, 1, WEISS)
        # draußen vor der Wand: die Rakete steigt schräg auf, der Schweif flackert
        for start, x0, richtung, farbe in RAKETEN:
            t = f - start
            if 0 <= t < FLUG:
                schweif = (FUNKE, GELB, None, GLUT) if f % 2 else (GELB, FUNKE, GLUT, None)
                for k, teil in enumerate((WEISS, ROT, ROT) + schweif):
                    if teil:
                        bild.setze(x0 + richtung * ((t - k) // 2), 16 - (t - k), teil)
        liste.append(bild)
    return liste
