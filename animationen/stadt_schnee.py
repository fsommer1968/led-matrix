"""Stadt im Schnee: es dämmert, Schnee fällt, Dächer, Kirchturm und Straße werden nach und nach
weiß, die Fenster gehen Stockwerk für Stockwerk an (warmes Licht, bunte Kirchenfenster, ein
Fernseher), Laternen leuchten, aus dem Schornstein steigt Rauch, zuletzt gehen die Lichter am
Tannenbaum auf dem Platz an – 255 Bilder.

Sparsam gezeichnet (23.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert; gleiche Spalten und sich wiederholende Spaltenfolgen kosten
fast nichts. Darum stehen die Häuser mit der Traufe zur Straße (gerade Dachkante statt Giebel),
die Fenster sitzen im festen Dreiertakt, der Schnee legt sich je Dach gleichmäßig (das Dach wird
in Stufen heller, dann wächst eine zweite Schicht), die Straße wird als Ganzes weiß, und es
fallen wenige Flocken.
"""
import random

from basis import B, GELB, ROT, Bild, Schnee, dimmen, mischen

NAME = "stadt_schnee"
TITEL = "Stadt wird weiß, Fenster gehen an"

ABEND = (22, 30, 78)
NACHT = (2, 3, 20)
WEISS_SCHNEE = (215, 225, 250)
STRASSE = (48, 48, 64)
ZIEGEL = (135, 45, 30)
SCHIEFER = (70, 72, 100)
KUPFER = (40, 120, 95)
KIRCHE = (80, 80, 98)
LICHT = [(255, 190, 70), (255, 160, 40), (255, 215, 110)]
TANNE = (0, 100, 40)
# Wenige Flocken an ausgesuchten Stellen (Spalte, Tempo, Phase): Eine Flocke vor dem ersten Fenstertakt
# eines Hauses kostet beim Komprimieren das Drei- bis Vierfache, darum fallen sie weiter rechts im Haus,
# vor Kirche und Platz; die fernen sind nur über den Dächern zu sehen.
SCHNEE_FERN = Schnee(anzahl=0, farbe=(105, 115, 160))               # hinter den Häusern
SCHNEE_FERN.flocken = [(13, 0.25, 6.0), (27, 0.34, 14.0), (44, 0.5, 2.0), (61, 0.34, 10.0), (35, 0.25, 18.0)]
SCHNEE_NAH = Schnee(anzahl=0, farbe=(225, 230, 255))                # davor
SCHNEE_NAH.flocken = [(8, 0.34, 3.0), (20, 0.25, 12.0), (33, 0.5, 8.0), (56, 0.34, 16.0)]

# Häuser, Traufe zur Straße: x, Breite (3n + 1), oberste Mauerzeile, Dachzeilen, Mauer, Dach,
# Fensterlicht, Schnee ab Bild. Das erste und das letzte Haus sind Zwillinge (gleiche Spalten:
# das zweite kostet fast nichts), auch Laterne und Schornstein stehen bei beiden gleich.
GRUEN = (45, 88, 72)
HAEUSER = [
    (0, 10, 9, 2, GRUEN, ZIEGEL, LICHT[2], 30),
    (10, 7, 6, 1, (56, 64, 110), SCHIEFER, LICHT[0], 70),
    (37, 10, 8, 2, (88, 52, 100), SCHIEFER, LICHT[1], 50),
    (47, 7, 10, 2, (118, 88, 40), ZIEGEL, LICHT[0], 90),
    (54, 10, 9, 2, GRUEN, ZIEGEL, LICHT[2], 30),
]
ZWILLING = {4: 0}                                # Haus 4 macht alles wie Haus 0, nur etwas später
ZWILLING_SPAETER = 8                             # Bilder
TURM_X, SCHIFF_X, SCHIFF_B = 17, 22, 7           # Kirche: Turm 5 breit, daneben das Schiff
KIRCHE_SCHNEE = 60
SCHORNSTEINE = [(6, 5, 2), (60, 5, 2)]           # x, oberste Zeile, Höhe; nur der erste raucht
LATERNEN = [(0, 28), (54, 28), (36, 40)]         # x, geht an bei Bild
BAUM_X = 32                                      # Tannenbaum auf dem Platz
BAUM_LICHTER = [(31, 11, ROT), (33, 12, GELB), (30, 13, (0, 200, 255)), (32, 10, (255, 0, 160)),
                (34, 13, ROT), (32, 13, GELB)]
STUFEN = 4                                       # Schnee wird in so vielen Stufen heller
STUFE_DAUER = 9                                  # Bilder je Stufe
ZWEITE_SCHICHT = 80                              # so viele Bilder später wächst die zweite Schicht


def _stadt():
    """Feste Kulisse: Pixel der Gebäude, Fenster je Stockwerk, Schneekanten je Gebäude."""
    px = {}
    stockwerke = []                              # (Hausnummer, [(x, y, breit, hoch)], Lichtfarbe)
    schnee = []                                  # (ab Bild, [(x, oberste Zeile)])

    def rechteck(x0, y0, b, h, farbe):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + b):
                if 0 <= x < B and 0 <= y < 15:
                    px[(x, y)] = farbe

    def kanten(x0, b, ab):
        schnee.append((ab, [(x, min(y for (xx, y) in px if xx == x)) for x in range(x0, x0 + b)]))

    for nr, (x, b, top, dach, mauer, dachfarbe, licht, ab) in enumerate(HAEUSER):
        rechteck(x, top, b, 15 - top, mauer)
        rechteck(x, top - dach, b, dach, dachfarbe)
        kanten(x, b, ab)
        for wy in range(top + 1, 14, 3):
            stockwerke.append((nr, [(wx, wy, 2, 2) for wx in range(x + 1, x + b - 2, 3)], licht))
    # Kirche: Turm mit spitzem Kupferhelm, Schiff mit Schieferdach
    rechteck(TURM_X, 5, 5, 10, KIRCHE)
    rechteck(TURM_X, 4, 5, 1, KUPFER)
    rechteck(TURM_X + 1, 2, 3, 2, KUPFER)
    rechteck(TURM_X + 2, 0, 1, 2, KUPFER)
    rechteck(SCHIFF_X, 10, SCHIFF_B, 5, KIRCHE)
    rechteck(SCHIFF_X, 8, SCHIFF_B, 2, SCHIEFER)
    kanten(TURM_X, 5 + SCHIFF_B, KIRCHE_SCHNEE)
    for x, top, h in SCHORNSTEINE:
        rechteck(x, top, 1, h, (95, 50, 40))
    return px, stockwerke, schnee


STADT, STOCKWERKE, SCHNEEKANTEN = _stadt()


def _zeiten():
    """Wann welches Fenster angeht: die Stockwerke in gewürfelter Reihenfolge, die Fenster eines
    Stockwerks kurz nacheinander (so gleichen sich die Fensterspalten bald wieder). Das
    Zwillingshaus folgt seinem Vorbild Fenster für Fenster mit kleinem Abstand."""
    z = random.Random(982)
    folge = [i for i, st in enumerate(STOCKWERKE) if st[0] not in ZWILLING]
    z.shuffle(folge)
    an = {}
    for k, i in enumerate(folge):
        fenster = STOCKWERKE[i][1]
        reihe = fenster if z.random() < 0.5 else fenster[::-1]
        for j, fe in enumerate(reihe):
            an[fe] = 14 + k * 20 + j * 5
    for nr, fenster, _ in STOCKWERKE:
        if nr in ZWILLING:
            dx = HAEUSER[nr][0] - HAEUSER[ZWILLING[nr]][0]
            for wx, wy, b, h in fenster:
                an[(wx, wy, b, h)] = an[(wx - dx, wy, b, h)] + ZWILLING_SPAETER
    fernseher = next(st for st in STOCKWERKE if st[0] == 1)[1][1]    # im blauen Haus oben rechts
    flimmern = [z.choice(((90, 140, 255), (60, 100, 220), (130, 180, 255))) for _ in range(90)]
    return an, fernseher, flimmern


AN, FERNSEHER, FLIMMERN = _zeiten()
KIRCHENFENSTER = [(SCHIFF_X + 2, 11, 120), (SCHIFF_X + 4, 11, 128)]  # x, y, geht an bei Bild
TURMFENSTER = (TURM_X + 2, 7, 176)
BUNT_GLAS = ((255, 60, 40), (255, 190, 40), (60, 120, 255))


def _stufe(f, ab):
    """Anteil Schnee 0 … 1 in STUFEN Schritten, beginnend bei Bild ab."""
    return max(0, min(STUFEN, (f - ab) // STUFE_DAUER + 1)) / STUFEN


def bilder():
    liste = []
    for f in range(255):
        himmel = mischen(ABEND, NACHT, min(12, f // 10) / 12)        # dämmert in 12 Stufen
        bild = Bild(himmel)
        SCHNEE_FERN.zeichnen(bild, f)
        x, top, h = SCHORNSTEINE[0]                                  # Rauch: ein Wölkchen steigt auf
        t = f % 24
        bild.setze(x + t // 5 + (1 if (t // 3) % 2 else 0), top - 1 - t // 4,
                   (95, 95, 115) if t < 12 else (60, 60, 80))
        for (x, y), farbe in STADT.items():
            bild.setze(x, y, farbe)
        # Tannenbaum auf dem Platz
        for k, halb in enumerate((0, 1, 1, 2, 2)):
            bild.rechteck(BAUM_X - halb, 9 + k, 2 * halb + 1, 1, TANNE)
        bild.setze(BAUM_X, 14, (95, 55, 22))
        if f > 90:                                                   # Schnee auf den Zweigen
            bild.setze(BAUM_X - 2, 12, WEISS_SCHNEE)
            bild.setze(BAUM_X + 2, 12, WEISS_SCHNEE)
        if f > 60:
            bild.setze(BAUM_X, 8, WEISS_SCHNEE)
        for i, (lx, ly, farbe) in enumerate(BAUM_LICHTER):
            if f >= 200 + i * 5:
                blinkt = f >= 236 and (f // 4 + i) % 3 == 0
                bild.setze(lx, ly, dimmen(farbe, 0.45) if blinkt else farbe)
        if f >= 232:
            bild.setze(BAUM_X, 8, GELB if (f // 3) % 2 else (255, 240, 160))   # Stern auf der Spitze
        # Fenster
        for nr, fenster, licht in STOCKWERKE:
            dunkel = dimmen(HAEUSER[nr][4], 0.35)
            for fe in fenster:
                wx, wy, b, h = fe
                farbe = dunkel if f < AN[fe] else FLIMMERN[f // 3] if fe == FERNSEHER else licht
                bild.rechteck(wx, wy, b, h, farbe)
        for wx, wy, ab in KIRCHENFENSTER:                            # dunkel nicht zu sehen (spart Bytes)
            if f >= ab:
                for k, c in enumerate(BUNT_GLAS):
                    bild.setze(wx, wy + k, c)
        wx, wy, ab = TURMFENSTER
        if f >= ab:
            bild.rechteck(wx, wy, 1, 2, LICHT[0])
        # Schnee legt sich auf Dächer und Straße: je Gebäude gleichmäßig, in Stufen heller
        for ab, kanten in SCHNEEKANTEN:
            a1, a2 = _stufe(f, ab), _stufe(f, ab + ZWEITE_SCHICHT)
            for x, y in kanten:
                if a1:
                    bild.setze(x, y, mischen(STADT[(x, y)], WEISS_SCHNEE, a1))
                if a2 and y > 0 and (x, y - 1) not in STADT:
                    bild.setze(x, y - 1, mischen(himmel, WEISS_SCHNEE, a2))
        bild.rechteck(0, 15, B, 1, mischen(STRASSE, WEISS_SCHNEE, _stufe(f, 40)))
        for lx, ab in LATERNEN:                                      # Laternen mit Lichthof darüber
            bild.rechteck(lx, 11, 1, 4, (75, 75, 90))
            if f >= ab:
                bild.setze(lx, 10, (255, 225, 150))
                bild.setze(lx, 9, mischen(bild.hole(lx, 9), (255, 190, 90), 0.45))
            else:
                bild.setze(lx, 10, (80, 80, 90))
        SCHNEE_NAH.zeichnen(bild, f)
        liste.append(bild)
    return liste
