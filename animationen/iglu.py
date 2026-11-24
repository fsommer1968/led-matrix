"""Iglu: verschneite Ebene bei Nacht, Mond und drei Sterne. Ein Kind in bunter Winterjacke trägt
Schneeblock um Schneeblock heran und setzt Reihe auf Reihe, bis die Kuppel steht, hüpft vor Freude
und kriecht hinein. Drinnen geht das Licht an: Der Eingang leuchtet warm, die Fugen glimmen, aus dem
Loch im Dach steigt Rauch, eine Sternschnuppe fällt. Dann fängt es an zu schneien, das Kind schaut
kurz heraus, das Licht geht aus, das Iglu schneit zu und versinkt im Schnee. Die Ebene ist wieder
leer, die letzten Flocken fallen noch, wenn das Kind von vorn beginnt – die Runde geht ohne Sprung
in sich über, 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ebener Boden (alle Spalten gleich), Blöcke zwei Zeilen
hoch mit wenigen senkrechten Fugen statt eines Musters, das Kind drei Spalten breit, drei Sterne,
einzelne Flocken nur am Schluss, Rauch nur über dem Rauchloch.
"""
import math

from basis import B, GELB, HAUT, NACHTBLAU, WEISS, Bild, dimmen, mischen, sternschnuppe

NAME = "iglu"
TITEL = "Iglu wird gebaut, drinnen geht das Licht an"

KANTE = (190, 200, 235)                        # Oberkante der Schneedecke
BODEN = (88, 100, 150)                         # darunter gedämpft (große Fläche)
SPUR = (125, 138, 195)                         # Fußstapfen
BLOCK = (205, 216, 248)                        # Schneeblock, obere Zeile
BLOCK_UNTEN = (150, 165, 222)                  # untere Zeile dunkler: so sieht man die Reihen
FUGE = (85, 98, 165)                           # Fuge zwischen zwei Blöcken
HUEGEL = KANTE                                 # zugeschneit: ein Ton, wie die Schneedecke
MOND = (240, 230, 170)
STERN = (255, 240, 200)
STERNE = [(7, 2, 0, 51), (17, 0, 20, 85), (47, 1, 33, 51)]           # x, y, Phase, Periode (teilt 255)
LICHT = (255, 200, 50)                         # Eingang von innen beleuchtet
GLUT = (255, 125, 0)                           # Licht in den Fugen
SCHEIN = [(255, 215, 130), (205, 150, 85), (135, 110, 105)]          # Lichtschein im Schnee, drei Zeilen
RAUCH = (150, 150, 170)
FLOCKE = (190, 200, 235)
MUETZE = (0, 215, 190)
JACKE = (255, 25, 0)
HOSE = (0, 80, 255)
AUGE = (50, 25, 10)
FARBEN = {"p": GELB, "m": MUETZE, "h": HAUT, "a": AUGE, "j": JACKE, "b": HOSE}

# Kind (Blick nach rechts): p Bommel, m Mütze, h Gesicht, a Auge, j Jacke, b Hose
STEHT = [".p.", "mmm", "hha", "jjj", "jjj", "bbb", "bbb"]
GEHT = [".p.", "mmm", "hha", "jjj", "jjj", "bbb", "b.b"]
JUBEL = ["j.p.j", "jmmmj", ".aha.", ".jjj.", ".jjj.", ".bbb.", ".b.b."]
# von hinten vor der Tür: duckt sich und verschwindet im Eingang (wird kleiner)
KRIECHT = [[".p.", "mmm", "mmm", "jjj", "jjj", "bbb", "b.b"],
           [".p.", "mmm", "jjj", "jjj", "bbb"],
           ["mmm", "jjj", "bbb"],
           ["jjj", "bbb"],
           ["bbb"]]
GUCKT_AUS = ["mmm", "aha"]                     # Mütze und Augen im Eingang

# Kuppel 21 breit (x 22 bis 42), 8 hoch, vier Reihen zu je zwei Zeilen.
MITTE = 32
UMRISS = {12: 10, 11: 10, 10: 10, 9: 9, 8: 8, 7: 7, 6: 6, 5: 4}      # Zeile → Breite neben der Mittelspalte
# Blöcke in der Reihenfolge, in der gebaut wird: (y oben, x links, Breite, x der Fuge zum Nachbarn
# oder None, Blick des Kindes beim Setzen: 1 = es steht links davon, -1 = rechts)
BLOECKE = [(11, 22, 4, None, 1), (11, 26, 5, 26, 1), (11, 34, 4, None, 1), (11, 38, 5, 38, 1),   # Tür bleibt frei
           (9, 37, 6, None, -1), (9, 29, 8, 36, -1), (9, 22, 7, 28, -1),                          # Mitte: Türsturz
           (7, 24, 6, None, 1), (7, 30, 4, 30, 1), (7, 34, 7, 34, 1),
           (5, 33, 6, None, -1), (5, 26, 7, 32, -1)]
STURZ = 6                                      # ab so vielen Blöcken ist die Tür überdeckt
TUER = [(31, 11), (32, 11), (33, 11), (31, 12), (32, 12), (33, 12), (32, 10)]
BODEN_Y = 13
TRAGEN_Y = 9                                   # Block vor der Jacke
START_X = -7                                   # im ersten Bild ragt nur eine Spalte des Blocks herein


def _bauplan():
    """Je Bild der Bauzeit: (x, Blick, Schritt, y des Blocks in der Hand oder None, gesetzte Blöcke)."""
    plan, x = [], START_X
    for n, (y, bx, breite, _, blick) in enumerate(BLOECKE):
        ziel = bx - 3 if blick > 0 else bx + breite
        while x != ziel:                                             # mit dem Block hinlaufen, 1 Pixel je Bild
            richtung = 1 if ziel > x else -1
            x += richtung
            plan.append((x, richtung, x % 4 < 2, TRAGEN_Y, n))
        for k in (1, 2):                                             # an seinen Platz heben oder senken
            plan.append((x, blick, False, round(TRAGEN_Y + (y - TRAGEN_Y) * k / 2), n))
        plan.append((x, blick, False, None, n + 1))                  # sitzt
    return plan


BAUPLAN = _bauplan()
FERTIG = len(BAUPLAN)                          # Kuppel steht (132)
ZUR_TUER = FERTIG + 8                          # zweimal hüpfen, dann zwei Schritte vor die Tür
HINEIN = ZUR_TUER + 2
DRIN = HINEIN + 2 * len(KRIECHT)
LICHT_AN = DRIN + 2
RAUCH_AB, RAUCH_ENDE = LICHT_AN + 8, 204
SCHNUPPE = 186
GUCKT, GUCKT_ENDE = 203, 215                   # es fängt an zu schneien: das Kind schaut heraus
LICHT_AUS, ZU, SINKT = 218, 222, 230
# Flocken: (x, Startbild), erst einzelne, beim Zuschneien mehr; jede fällt 28 Bilder lang, die
# letzten noch in die nächste Runde hinein (das Kind kommt im ausklingenden Schneefall). Gerade und
# ungerade Startbilder im Wechsel: so rückt in jedem Bild etwa die Hälfte der Flocken eine Zeile weiter.
FLOCKEN = [(50, 194), (13, 199), (37, 202), (5, 207), (27, 210), (60, 215), (44, 216), (18, 219),
           (33, 220), (2, 223), (51, 224), (24, 227), (40, 228), (10, 231), (62, 232), (30, 235),
           (47, 236), (15, 239), (53, 240), (4, 244), (22, 246)]


def kuppel(bild, anzahl, licht=0.0, zu=0.0, tief=0):
    """Die ersten `anzahl` Blöcke; licht 0…1 von innen beleuchtet, zu 0…1 zugeschneit, tief = versunken."""
    def punkt(x, y, farbe):
        if abs(x - MITTE) <= UMRISS[y] and y + tief < BODEN_Y:
            bild.setze(x, y + tief, mischen(farbe, HUEGEL, zu))

    for y, x, breite, fuge, _ in BLOECKE[:anzahl]:
        for yy, farbe in ((y, BLOCK), (y + 1, BLOCK_UNTEN)):
            for xx in range(x, x + breite):
                punkt(xx, yy, farbe)
            if fuge is not None:                                     # Fuge: dunkel, von innen beleuchtet glimmt sie
                punkt(fuge, yy, mischen(FUGE, GLUT, licht))
    if anzahl >= STURZ:                                              # Eingang: dunkel, später hell
        for x, y in TUER:
            punkt(x, y, mischen(NACHTBLAU, LICHT, licht))
    if licht > 0:
        punkt(MITTE, 5, mischen(FUGE, LICHT, licht))                 # Rauchloch oben in der Mittelfuge
        for k, schein in enumerate(SCHEIN):                          # Schein auf dem Schnee vor der Tür
            for x in range(MITTE - 1 - k, MITTE + 2 + k):
                bild.setze(x, BODEN_Y + k, mischen(bild.hole(x, BODEN_Y + k), schein, licht))


def kind(bild, x, blick, schritt, block_y=None, breite=4):
    """Das Kind von der Seite; block_y = Oberkante des Blocks, den es vor sich hält."""
    bild.figur(x, 6, GEHT if schritt else STEHT, FARBEN, spiegeln=blick < 0)
    if block_y is None:
        return
    bild.rechteck(x + 3 if blick > 0 else x - breite, block_y, breite, 2, WEISS)
    hand = x + 3 if blick > 0 else x - 1
    if block_y + 2 <= 9:                                             # Arm streckt sich nach oben
        for y in range(block_y + 2, 10):
            bild.setze(hand, y, JACKE)
    elif block_y > 10:                                               # … oder nach unten
        bild.setze(hand, 10, JACKE)


def rauch(bild, f):
    """Rauchfahne aus dem Loch: schlängelt sich nach oben und wird blasser; wächst an, reißt unten ab."""
    for hoehe in range(5):                                           # 0 = direkt über dem Loch
        if f - RAUCH_AB < hoehe * 3 or f - RAUCH_ENDE >= hoehe * 3:
            continue
        x = MITTE + 0.5 + (0.5 + 0.3 * hoehe) * math.sin(f * 0.3 - hoehe * 1.2) + 0.25 * hoehe
        bild.setze(math.floor(x), 4 - hoehe, dimmen(RAUCH, 1 - 0.14 * hoehe))


def bilder():
    liste = []
    spur_bis = -1
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        sternschnuppe(bild, f, SCHNUPPE, 24, 0)
        bild.kreis(56, 3, 2.2, MOND)
        bild.rechteck(0, BODEN_Y, B, 1, KANTE)
        bild.rechteck(0, BODEN_Y + 1, B, 2, BODEN)
        zu = min(1.0, max(0, f - ZU + 2) // 2 * 0.25)                # schneit zu …
        tief = max(0, f - SINKT + 3) // 3                            # … und versinkt, alle drei Bilder eine Zeile
        if f < FERTIG:
            spur_bis = max(spur_bis, BAUPLAN[f][0] - 1)
        for x in range(1, spur_bis + 1, 4):                          # Fußstapfen, bis der Schnee sie deckt
            bild.setze(x, BODEN_Y, mischen(SPUR, KANTE, zu))

        if f < FERTIG:                                               # bauen
            x, blick, schritt, block_y, anzahl = BAUPLAN[f]
            kuppel(bild, anzahl)
            kind(bild, x, blick, schritt, block_y, min(5, BLOECKE[min(anzahl, len(BLOECKE) - 1)][2]))
        elif f < ZUR_TUER:                                           # fertig: zweimal hüpfen
            kuppel(bild, len(BLOECKE))
            if (f - FERTIG) % 4 < 2:
                bild.figur(BAUPLAN[-1][0] - 1, 5, JUBEL, FARBEN)
            else:
                kind(bild, BAUPLAN[-1][0], -1, False)
        elif f < HINEIN:                                             # zwei Schritte vor die Tür
            kuppel(bild, len(BLOECKE))
            kind(bild, BAUPLAN[-1][0] - 1 - (f - ZUR_TUER), -1, f == ZUR_TUER)
        elif f < DRIN:                                               # duckt sich und kriecht hinein
            kuppel(bild, len(BLOECKE))
            stufe = (f - HINEIN) // 2
            farben = {k: dimmen(v, 1 - 0.2 * max(0, stufe - 1)) for k, v in FARBEN.items()}
            bild.figur(MITTE - 1, BODEN_Y - len(KRIECHT[stufe]), KRIECHT[stufe], farben)
        elif tief < 8:
            if f < LICHT_AN:
                licht = 0.0
            elif f < LICHT_AUS:                                      # geht an, flackert dann sacht
                licht = min(1.0, (f - LICHT_AN + 2) // 2 * 0.25)
                if licht == 1.0 and (f // 6) % 4 == 0:
                    licht = 0.85
            else:                                                    # geht aus
                licht = max(0.0, 1 - (f - LICHT_AUS + 2) // 2 * 0.25)
            kuppel(bild, len(BLOECKE), licht, zu, tief)
            rauch(bild, f)
            if GUCKT <= f < GUCKT_ENDE:                              # taucht im Eingang auf und wieder ab
                k = min(f - GUCKT, GUCKT_ENDE - 1 - f, 2) // 2
                bild.figur(MITTE - 1, 12 - k, GUCKT_AUS[:k + 1], FARBEN)

        for x, start in FLOCKEN:                                     # einzelne Flocken, nur vor dem Himmel
            t = (f - start) % 255
            if t < 28 and bild.hole(x, t // 2 - 1) == NACHTBLAU:
                bild.setze(x, t // 2 - 1, FLOCKE)
        liste.append(bild)
    return liste
