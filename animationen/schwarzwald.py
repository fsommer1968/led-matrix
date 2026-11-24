"""Winter im Schwarzwald: Vor dem dunklen Tannenwald steht zwischen zwei verschneiten Tannen ein
Schwarzwaldhof mit tief heruntergezogenem Walmdach unter Schnee. Ein Mädchen mit Bollenhut und
Laterne stapft durch den Schnee heim, die Tür leuchtet auf, die Fenster gehen nacheinander an.
Darüber erscheint Buchstabe für Buchstabe SCHWARZWALD in Bollenhut-Rot, Schnee legt sich als weiße
Haube auf die Buchstaben, es glitzert, ein weißer Glanz läuft durch das Wort; dann verlischt die
Schrift, eine Sternschnuppe fällt, die Fenster gehen aus – 255 Bilder, die Runde geht ohne Sprung
in sich über.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Unter der Schrift kostet jede Spalte, die anders ist als ihre
Nachbarn, doppelt. Darum ein glatter Waldsaum statt gezackter Hänge, Haus und Tannen nur in der
Mitte, und die beiden Tannen stehen genau unter den beiden W (24 Spalten Abstand): Das zweite
„WA“ samt Tanne ist dann eine Kopie des ersten. Das Mädchen ist im Haus, bevor die Schrift kommt.
Drei gleiche Fenster (das linke ist die Tür), drei Sterne und drei Flocken, beide nur dort, wo
kein Buchstabe steht. Die Schrift füllt die ganze Breite: elf Buchstaben der 5×7-Schrift, das L
eine Spalte schmaler.
"""
import math

from basis import B, GELB, HAUT, NACHTBLAU, ROT, SCHRIFT, WEISS, Bild, dimmen, sternschnuppe

NAME = "schwarzwald"
TITEL = "Winter im Schwarzwald"

WORT = "SCHWARZWALD"
STERN = (255, 240, 200)
STERNE = [(9, 2, 0, 51), (33, 4, 20, 85), (56, 1, 40, 51)]           # x, y, Phase, Periode (teilt 255)
KANTE = (215, 225, 250)
BODEN = (105, 118, 165)
WALD = (0, 50, 26)                             # Waldsaum hinten, dunkel
WIPFEL = (0, 30, 22)                           # seine oberste Zeile, noch dunkler
TANNE = (0, 120, 45)
STAMM = (95, 55, 22)
DACH = (150, 162, 205)                         # verschneites Dach, gedämpft
BALKEN = (130, 65, 20)
WAND = (80, 42, 14)
FENSTER_AUS = (26, 20, 34)
FENSTER_AN = (255, 185, 40)
FLOCKE = (150, 160, 200)
KLEID = (70, 60, 170)
STIEFEL = (120, 70, 30)
AUGE = (50, 25, 10)

HAUS_X = 25                                    # Haus: 15 Spalten unter A, R und Z
FENSTER = [2, 6, 10]                           # drei Fenster (je drei Spalten) ab HAUS_X; das linke ist die Tür
TANNEN = (20, 44)                              # zwei gleiche Tannen genau unter den beiden W
FLOCKEN = [(7, 0, 3), (51, 6, 5), (60, 11, 4)]                       # x, Phase, Tempo in 1/15 je Bild

# Mädchen mit Bollenhut (Blick nach rechts), Laterne voraus: r Bollen, w Hut/Ärmel, h Haut, a Auge,
# k Kleid, b Stiefel, l Laterne
MAEDCHEN = [["r.r.r.", "wwwww.", ".hha..", "wkkkw.", ".kkk.l", ".b.b.."],
            ["r.r.r.", "wwwww.", ".hha..", "wkkkw.", ".kkk.l", "..bb.."]]
MAEDCHEN_FARBEN = {"r": ROT, "w": WEISS, "h": HAUT, "a": AUGE, "k": KLEID, "b": STIEFEL, "l": GELB}

# Ablauf
TUER_X = 25                                    # hier steht das Mädchen vor der Tür
HEIM = 50                                      # ab hier ist es im Haus
FENSTER_AN_AB = [47, 55, 60]                   # Tür leuchtet auf, dann gehen die Fenster an
SCHRIFT_AB, TAKT = 62, 5                       # ein Buchstabe alle fünf Bilder
HAUBE_AB = 122                                 # Schnee legt sich auf die Buchstaben
HAUBEN = [3, 7, 0, 9, 5, 1, 10, 4, 8, 2, 6]    # in dieser Reihenfolge
FUNKEN_TAKT = 8                                # alle acht Bilder blitzt ein Pixel der Schrift weiß auf
GLANZ_AB = 186                                 # ein weißer Glanz läuft durch das Wort, zwei Bilder je Buchstabe
SCHRIFT_WEG = 214                              # Schrift verlischt von links nach rechts
SCHNUPPE = 236                                 # Sternschnuppe, wenn die Schrift fort ist
FENSTER_WEG = 242                              # Fenster gehen aus


def glyph(z):
    """5×7-Zeichen; das L eine Spalte schmaler, damit das Wort in 64 Spalten passt."""
    return [zeile[:4] for zeile in SCHRIFT[z]] if z == "L" else SCHRIFT[z]


def tanne(bild, x):
    """Tanne: Stufen aus je drei Zeilen, Schnee auf Spitze und Astenden, Stamm."""
    for k in range(6):
        halb = k // 3 + k % 3
        bild.rechteck(x - halb, 8 + k, 2 * halb + 1, 1, TANNE)
        if k % 3 == 2:
            bild.setze(x - halb, 8 + k, KANTE)
            bild.setze(x + halb, 8 + k, KANTE)
    bild.setze(x, 8, KANTE)
    bild.setze(x, 14, STAMM)


def haus(bild, f):
    """Schwarzwaldhof: Walmdach unter Schnee, fünf Zeilen hoch und bis fast zum Boden gezogen,
    darunter die Holzwand mit Tür und zwei Fenstern."""
    x = HAUS_X
    for k in range(5):                                               # Dach: Zeilen 8 bis 12
        bild.rechteck(x + 4 - k, 8 + k, 7 + 2 * k, 1, KANTE if k == 0 else DACH)
    bild.rechteck(x, 13, 15, 1, BALKEN)                              # Traufe
    bild.rechteck(x + 1, 13, 13, 2, WAND)
    for i, fx in enumerate(FENSTER):
        an = FENSTER_AN_AB[i] <= f < FENSTER_WEG + i * 4
        bild.rechteck(x + fx, 13, 3, 2, FENSTER_AN if an else FENSTER_AUS)


def schrift(bild, f):
    """Zeichnet die Schrift und liefert die Spalten, in denen gerade ein Buchstabe steht."""
    belegt = set()
    x = 0
    for i, z in enumerate(WORT):
        g = glyph(z)
        alter = f - (SCHRIFT_AB + i * TAKT)
        rest = SCHRIFT_WEG + i * 2 - f                               # verlischt von links nach rechts
        if alter >= 0 and rest > 0:
            belegt.update(range(x - 1, x + len(g[0]) + 1))
            bild.rechteck(x - 1, 0, len(g[0]) + 2, 7, NACHTBLAU)     # kein Stern im Buchstaben
            farbe = WEISS if alter < 2 or 0 <= f - GLANZ_AB - i * 2 < 2 else ROT
            if rest <= 2:
                farbe = dimmen(ROT, 0.4)
            haube = rest > 2 and f >= HAUBE_AB + HAUBEN.index(i) * 4
            pixel = []
            for gx in range(len(g[0])):
                oben = True
                for gy in range(7):
                    if g[gy][gx] == "1":
                        schnee = oben and gy < 2 and haube           # Schnee liegt obenauf
                        bild.setze(x + gx, gy, KANTE if schnee else farbe)
                        if not schnee:
                            pixel.append((x + gx, gy))
                        oben = False
            funke = f // FUNKEN_TAKT
            if alter >= TAKT and rest > 2 and f % FUNKEN_TAKT < 2 and funke * 4 % 11 == i:
                bild.setze(*pixel[funke * 7 % len(pixel)], WEISS)    # Glitzern
        x += len(g[0]) + 1
    return belegt


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        sternschnuppe(bild, f, SCHNUPPE, 62, 0, laenge=8)
        bild.rechteck(0, 10, B, 1, WIPFEL)                           # Waldsaum hinten
        bild.rechteck(0, 11, B, 3, WALD)
        bild.rechteck(0, 14, B, 1, KANTE)
        bild.rechteck(0, 15, B, 1, BODEN)
        haus(bild, f)
        for x in TANNEN:
            tanne(bild, x)
        if f < HEIM:                                                 # Mädchen stapft heim bis zur Tür:
            x = min(TUER_X, -6 + 2 * f // 3)                         # alle drei Bilder ein Schritt von zwei Pixeln
            bild.figur(x, 9, MAEDCHEN[(f // 3) % 2 if x < TUER_X else 0], MAEDCHEN_FARBEN)
        belegt = schrift(bild, f)
        for x, phase, tempo in FLOCKEN:                              # wenige Flocken, nur vor Himmel und Wald
            y = (phase + f * tempo / 15) % 17 - 1
            x += round(math.sin(2 * math.pi * (f * 5 / 255 + phase / 17)))    # trudeln, fünfmal je Runde
            if bild.hole(x, y) in (NACHTBLAU, WALD, WIPFEL) and not (y < 7 and x in belegt):
                bild.setze(x, y, FLOCKE)
        liste.append(bild)
    return liste
