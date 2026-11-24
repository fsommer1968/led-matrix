"""Skifahrer: verschneiter Hang bei Nacht unter der Mondsichel. Zwei Skifahrer wedeln nacheinander
im Slalom um rote und blaue Torstangen ins Tal (vor der roten vorbei, hinter der blauen), gehen in
jedem Schwung in die Hocke, setzen den Stock ein und wirbeln Schnee auf; die rote Stange federt nach.
Hinten fährt der Sessellift das Seil hinauf und bringt beide mit baumelnden Ski wieder nach oben.
Tal- und Bergstation liegen außerhalb des Bildes, darum geht die Runde ohne Sprung in sich über –
255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum fällt der Hang in nur fünf Stufen, das Seil läuft
gleich gestuft darüber, die Tore sind schlanke Stangen (eine Spalte) im Takt der Stufen, die
Figuren haben gleiche Nachbarspalten, drei Sterne, eine schmale Mondsichel, kein Schneefall.
"""
import math

from basis import B, BLAU, GELB, HAUT, LILA, NACHTBLAU, PINK, TUERKIS, WEISS, Bild, dimmen

NAME = "skifahrer"
TITEL = "Skifahrer im Slalom, Sessellift fährt hinauf"

KANTE = (215, 225, 250)                        # Oberkante des Hangs
HANG = (78, 90, 140)                           # darunter gedämpft (große Fläche)
SEIL = (70, 70, 92)
STUETZE = (100, 100, 122)
SESSEL = (150, 160, 195)
TOR_ROT = (255, 0, 0)
TOR_BLAU = (0, 90, 255)
SKI = (255, 150, 0)
STOCK = (235, 235, 245)
AUGE = (50, 25, 10)
STERN = (255, 240, 200)
MOND = (240, 230, 170)
STERNE = [(21, 0, 0, 51), (39, 1, 30, 85), (50, 0, 20, 51)]          # x, y, Phase, Periode (teilt 255)

RUNDE = 255
STUFE = 12                                     # alle zwölf Spalten fällt der Hang um eine Zeile
SEIL_UEBER = 9                                 # das Seil läuft so viele Zeilen über der Hangkante
TORE = [8, 20, 32, 44, 56]                     # im Takt der Stufen, abwechselnd rot und blau
STUETZEN = [14, 50]
ABSTAND, JE_RUNDE = 32, 4                      # Sessel alle 32 Spalten, vier kommen je Runde vorbei
LIFT_X0 = 120                                  # legt fest, wann ein Sessel ins Bild kommt
AB = 96                                        # Bilder für die Abfahrt (drei Spalten in vier Bildern)

# Skifahrer: Mütze, Jacke, Hose, Start im Umlauf, Nummer des Sessels
FAHRER = [(GELB, (0, 220, 70), BLAU, 0, 0), (TUERKIS, PINK, LILA, 128, 2)]

# Abfahrt (Blick nach rechts), 7 breit: aufrecht zwischen den Toren (Stock nach hinten), in der
# Hocke im Schwung (Stock vorn eingesetzt)
HOCH = ["..mmm..", "..hha..", "..jjj..", ".pjjj..", "p.bbb..", ".ssssss"]
TIEF = [".......", "...mmm.", "...hha.", "..jjjp.", "..bbbbp", ".ssssss"]
# Sessel (fährt nach links hinauf), Gehänge hinten; mit Fahrgast baumeln die Ski
SESSEL_LEER = ["....g", "....g", "....g", "....c", ".cccc"]
SESSEL_VOLL = [".mmmg", ".ahhg", ".jjjg", ".bbjc", ".bccc"]
BAUMELN = ["ssss.", ".ssss"]
# Schneewolke hinter den Skienden, je zwei Spalten Fahrt eine Stufe: (dx, dy) und Helligkeit
STAUB = [([(0, 0), (-1, 0), (-1, -1)], 1.0),
         ([(0, -1), (-1, 0), (-1, -1), (-1, -2), (-2, 0), (-2, -1)], 1.0),
         ([(-1, -2), (-2, -1), (-2, -2), (-3, -2), (-3, -3)], 0.75),
         ([(-2, -3), (-4, -2)], 0.5)]


def hang_y(x):
    """Oberkante des Hangs: von links oben in fünf Stufen hinunter."""
    return 9 + max(0, min(5, (x + 8) // STUFE))


def lift_x(nummer, f):
    """Spalte des Gehänges von Sessel nummer im Bild f (ganzzahlig gerechnet, damit Sessel und
    Fahrgast nach einer Runde genau wieder aufeinanderliegen)."""
    return LIFT_X0 + ABSTAND * nummer - (f * ABSTAND * JE_RUNDE + RUNDE // 2) // RUNDE


def sessel(bild, x, zeilen, farben):
    """Hängt den Sessel mit dem Gehänge (rechte Spalte) in Spalte x ans Seil."""
    bild.figur(x - 4, hang_y(x) - SEIL_UEBER + 1, zeilen, farben)


def bilder():
    liste = []
    for f in range(RUNDE):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        bild.rechteck(59, 0, 2, 4, MOND)                             # Mondsichel
        bild.rechteck(58, 1, 1, 2, MOND)
        bild.rechteck(60, 1, 1, 2, NACHTBLAU)
        for x in range(B):                                           # Seil und Hang
            y0 = hang_y(x)
            bild.setze(x, y0 - SEIL_UEBER, SEIL)
            bild.setze(x, y0, KANTE)
            for y in range(y0 + 1, 16):
                bild.setze(x, y, HANG)
        for x in STUETZEN:                                           # Stützen mit Querträger
            oben = hang_y(x) - SEIL_UEBER
            bild.rechteck(x, oben, 1, SEIL_UEBER, STUETZE)
            bild.rechteck(x - 1, oben, 3, 1, STUETZE)
        farben_lift = {"g": STUETZE, "c": SESSEL}
        for nummer in range(-8, 9):                                  # leere Sessel
            x = lift_x(nummer, f)
            if -1 <= x <= B + 4:
                sessel(bild, x, SESSEL_LEER, farben_lift)
        hinten, vorn, staub, federt = [], [], [], {}
        for muetze, jacke, hose, start, nummer in FAHRER:
            t = (f - start) % RUNDE
            farben = {"m": muetze, "h": HAUT, "a": AUGE, "j": jacke, "b": hose, "s": SKI,
                      "p": STOCK, **farben_lift}
            if t >= AB:                                              # im Sessel hinauf
                x = lift_x(nummer, start + t)
                sessel(bild, x, SESSEL_VOLL + [BAUMELN[x // 6 % 2]], farben)
                continue
            x = t * 3 // 4 - 7                                       # Abfahrt
            mitte = x + 3
            schwung = (mitte - TORE[0]) / STUFE                      # ganze Zahl = genau am Tor
            w = 1.5 + 1.5 * math.cos(math.pi * schwung)              # 3 vor dem roten Tor … 0 hinter dem blauen
            grund = max(9.0, min(14.0, 8.5 + (mitte + 8) / STUFE))   # Hangkante ohne Stufen
            y = min(15, round(grund - 1 + w))                        # Zeile der Ski
            tor = (mitte - TORE[0] + 3) // STUFE
            nach = mitte - TORE[0] - tor * STUFE                     # Spalten hinter dem Tor (-3 … 8)
            if 0 <= tor < len(TORE) and 0 <= nach < 8:               # Schnee stiebt im Schwung auf
                punkte, hell = STAUB[nach // 2]
                ay = min(15, hang_y(TORE[tor]) - 1 + (0 if tor % 2 else 3))
                staub += [(TORE[tor] - 3 + dx, ay + dy, dimmen(WEISS, hell)) for dx, dy in punkte]
                federt[tor] = tor % 2 == 0 and 2 <= nach <= 5        # … und die rote Stange federt nach
            (vorn if w > 1.5 else hinten).append((x, y - 5, TIEF if nach < 3 else HOCH, farben))
        for x, y, zeilen, farben in hinten:
            bild.figur(x, y, zeilen, farben)
        for k, x in enumerate(TORE):                                 # Torstangen
            farbe = TOR_BLAU if k % 2 else TOR_ROT
            y0 = hang_y(x)
            bild.rechteck(x + (1 if federt.get(k) else 0), y0 - 3, 1, 2, farbe)
            bild.rechteck(x, y0 - 1, 1, 2, farbe)
        for x, y, zeilen, farben in vorn:
            bild.figur(x, y, zeilen, farben)
        for x, y, farbe in staub:
            bild.setze(x, y, farbe)
        liste.append(bild)
    return liste
