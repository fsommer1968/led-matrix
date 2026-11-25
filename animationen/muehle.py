"""Schwarzwaldmühle im Winter: Eine alte Mühle mit tiefem, verschneitem Walmdach und einem warmen
Fenster steht am Bach vor dunklen Tannen. Daneben dreht sich das große hölzerne Wasserrad mit
Speichen und Schaufeln; das Wasser kommt über die Rinne, fällt oben auf das Rad, die Schaufeln
tragen es links hinunter in den Bach, auf dem ein paar Lichtpunkte glitzern. An Rinne und Dach
hängen Eiszapfen, ab und zu fällt ein Tropfen, und einmal landet ein Dompfaff auf dem First –
255 Bilder, die Runde geht ohne Sprung in sich über (eine Vierteldrehung des Rades dauert
17 Bilder, das sind 15 Vierteldrehungen je Runde; Wasser, Sterne und Lichtpunkte laufen in
Takten, die 255 teilen).

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Das Rad kostet in jedem Bild gut ein Drittel davon (jede
seiner 13 Spalten ist anders). Darum nur vier Speichen und vier Schaufeln, das Wasser am Rad sind
die Schaufeln selbst (links blau, rechts leer), ein glatter Bach über die ganze Breite, gleiche
schlanke Tannen im gleichen Abstand (die zweite ist eine Kopie der ersten), die rechte Dachseite
ist das Spiegelbild der linken.
"""
import math

from basis import B, NACHTBLAU, ROT, Bild, dimmen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "muehle"
TITEL = "Schwarzwaldmühle im Winter"

RUNDE = 255
VIERTEL = 17                                   # Bilder je Vierteldrehung (vier Speichen: 15 × 17 = 255)

STERN = (255, 240, 200)
STERNE = []                                    # Sterne und Bachlichter weggelassen: sonst 81,6 KB (24.11.2026)
KANTE = (215, 225, 250)                        # Schnee: Oberkante
DACH = (150, 162, 205)                         # verschneites Dach, gedämpft
WAND = (33, 17, 6)
FENSTER = (255, 185, 40)
HOLZ = (66, 36, 10)                          # Rad und Rinne
SCHAUFEL = (255, 190, 90)                      # leere Schaufeln: helles Holz
WASSER = (0, 170, 255)                         # fallendes Wasser, Rinne, volle Schaufeln
BACH = (0, 45, 150)                            # Bach, gedämpft (große Fläche)
GLITZER = (150, 220, 255)
EIS = (170, 225, 255)
TANNE = (0, 100, 40)
VOGEL_KOPF = (60, 60, 75)
VOGEL_RUECKEN = (120, 125, 150)
FELL = (74, 43, 15)
FELL_DUNKEL = (33, 18, 7)
NASE = (60, 30, 15)

CX, CY, R = 11, 9, 6                           # Rad: Mitte und Radius (Zeilen 3 bis 15)
SPEICHE = 5                                    # Länge der Speichen
RINNE_BIS = CX - 4                             # die Rinne endet über der linken Schulter des Rades
PFOSTEN = 2                                    # Stütze der Rinne am linken Rand, so breit
HAUS_X, HAUS_B = CX + 7, 19                    # Dach von HAUS_X an, so breit
WALM = [8, 6, 4]                               # oberste Dachzeile der äußeren Spalten (Walm)
FIRST = 3
FENSTER_X = HAUS_X + 9
TANNEN = (39, 45, 61)
ZAPFEN = [(3, 3), (5, 2)]                      # Eiszapfen an der Rinne: x, Länge
DACHZAPFEN = 2                                 # Eiszapfen an den Dachecken: Länge
TROPFEN = [(3, 5, 40), (3, 5, 142), (HAUS_X, 12, 96), (HAUS_X + HAUS_B - 1, 12, 210)]  # x, ab Zeile, Start
LICHTER = ()                                   # (früher drei Lichtpunkte im Bach)
VOGEL_X, VOGEL_KOMMT, VOGEL_DA, VOGEL_WEG = HAUS_X + 11, 14, 24, 74   # Platz auf dem First; Anflug, sitzt, Abflug
REH_X = 48                                     # hier trinkt das Reh
REH_KOMMT, REH_DA, REH_TRINKT, REH_HEBT, REH_GEHT_AB, REH_WEG = 108, 130, 138, 176, 184, 208
REH_TEMPO = 0.8

# Reh (Blick nach links): f Fell, d hintere Läufe, w Spiegel, e Lauscher, a Auge, k Nase
REH_STEHT = [".e.e.......", "kfaf.......", "..ff.......", "..ffffffffw", "..ffffffffw",
             "..f.d..d.f.", "..f.d..d.f."]
REH_SCHRITT = [".e.e.......", "kfaf.......", "..ff.......", "..ffffffffw", "..ffffffffw",
               "..f.d..d.f.", "...fd..df.."]
REH_TRINKEN = ["...........", "...........", "...........", "..ffffffffw", ".effffffffw",
               ".ff.d..d.f.", ".af.d..d.f.", ".k........."]
REH_FARBEN = {"f": FELL, "d": FELL_DUNKEL, "w": KANTE, "e": FELL, "a": NASE, "k": NASE}

# Felge: alle Bildpunkte im Abstand R von der Mitte, mit ihrem Winkel
FELGE = [(math.atan2(-dy, dx) % (2 * math.pi), dx, dy)
         for dx in range(-R, R + 1) for dy in range(-R, R + 1) if 31 <= dx * dx + dy * dy <= 42]
VOLL_VON, VOLL_BIS = math.radians(118), math.radians(262)           # hier tragen die Schaufeln Wasser


def runden(v):
    """Rundet von der Null weg (hält die Speichen punktsymmetrisch)."""
    return int(v + 0.5) if v >= 0 else -int(-v + 0.5)


def tanne(bild, x, hoehe=10, fuss=13):
    """Schlanke Tanne: alle drei Zeilen eine Stufe breiter, Schnee auf der Spitze."""
    for k in range(hoehe):
        halb = min(2, k // 3)
        bild.rechteck(x - halb, fuss - hoehe + k, 2 * halb + 1, 1, TANNE)
    bild.setze(x, fuss - 1 - hoehe, KANTE)


def haus(bild):
    """Mühle: Walmdach unter Schnee, darunter die Holzwand mit einem warmen Fenster; an den
    Dachecken je ein Eiszapfen."""
    for k in range(HAUS_B):
        aussen = min(k, HAUS_B - 1 - k)
        oben = WALM[aussen] if aussen < len(WALM) else FIRST
        bild.rechteck(HAUS_X + k, oben, 1, 10 - oben, DACH)
        if oben == FIRST:
            bild.setze(HAUS_X + k, FIRST, KANTE)                     # First: frischer Schnee
        if aussen == 0:
            bild.rechteck(HAUS_X + k, 10, 1, DACHZAPFEN, EIS)
        else:
            bild.rechteck(HAUS_X + k, 10, 1, 3, WAND)
    bild.rechteck(FENSTER_X, 10, 3, 2, FENSTER)


def rad(bild, f):
    """Wasserrad: Felge, vier Speichen, dazwischen vier Schaufeln; dreht links herum. Auf der
    linken Seite (abwärts) sind die Schaufeln voll Wasser, rechts leer."""
    a = 2 * math.pi * f / (4 * VIERTEL)
    for _, dx, dy in FELGE:
        bild.setze(CX + dx, CY + dy, HOLZ)
    for k in range(2):                         # zwei Durchmesser = vier Speichen
        c, s = math.cos(a + k * math.pi / 2), math.sin(a + k * math.pi / 2)
        if abs(c) >= abs(s):
            for i in range(-round(SPEICHE * abs(c)), round(SPEICHE * abs(c)) + 1):
                bild.setze(CX + i, CY + runden(-i * s / c), HOLZ)
        else:
            for i in range(-round(SPEICHE * abs(s)), round(SPEICHE * abs(s)) + 1):
                bild.setze(CX + runden(-i * c / s), CY + i, HOLZ)
    for k in range(4):                         # Schaufeln: der Felgenpunkt, der dem Winkel am nächsten liegt
        w = (a + math.pi / 4 + k * math.pi / 2) % (2 * math.pi)
        _, dx, dy = min(FELGE, key=lambda p: min(abs(p[0] - w), 2 * math.pi - abs(p[0] - w)))
        bild.setze(CX + dx, CY + dy, WASSER if VOLL_VON <= w <= VOLL_BIS else SCHAUFEL)


def vogel(bild, f):
    """Dompfaff (rote Brust, grauer Rücken): fliegt von rechts oben heran, sitzt auf dem First,
    wippt ab und zu mit dem Schwanz, fliegt nach links oben davon."""
    if VOGEL_KOMMT <= f < VOGEL_DA:                                  # Anflug
        t = VOGEL_DA - f
        x, y = VOGEL_X + t * 3, FIRST - 1 - min(2, (t + 1) // 2)
    elif VOGEL_DA <= f < VOGEL_WEG:                                  # sitzt
        x, y = VOGEL_X, FIRST - 1
    elif VOGEL_WEG <= f < VOGEL_WEG + 9:                             # Abflug
        t = f - VOGEL_WEG + 1
        x, y = VOGEL_X - t * 3, FIRST - 1 - min(2, (t + 1) // 2)
    else:
        return
    sitzt = VOGEL_DA <= f < VOGEL_WEG
    wippt = sitzt and (f - VOGEL_DA) % 17 in (11, 12)
    bild.setze(x, y, ROT)
    bild.setze(x + 1, y - 1 if wippt or (not sitzt and f % 2) else y, VOGEL_RUECKEN)   # Schwanz oder Flügel


def reh(bild, f):
    """Reh: kommt von rechts aus dem Wald, trinkt am Bach, hebt den Kopf, dreht um und geht."""
    if REH_KOMMT <= f < REH_DA:                                      # kommt
        x = REH_X + round((REH_DA - f) * REH_TEMPO)
        bild.figur(x, 6, REH_SCHRITT if (f // 3) % 2 else REH_STEHT, REH_FARBEN)
    elif REH_DA <= f < REH_TRINKT or REH_HEBT <= f < REH_GEHT_AB:    # steht und schaut
        bild.figur(REH_X, 6, REH_STEHT, REH_FARBEN)
    elif REH_TRINKT <= f < REH_HEBT:                                 # trinkt
        bild.figur(REH_X, 6, REH_TRINKEN, REH_FARBEN)
    elif REH_GEHT_AB <= f < REH_WEG:                                 # dreht um und geht
        x = REH_X + round((f - REH_GEHT_AB) * REH_TEMPO)
        bild.figur(x, 6, REH_SCHRITT if (f // 3) % 2 else REH_STEHT, REH_FARBEN, spiegeln=True)


def szene(f):
    """Ein Bild der Runde."""
    bild = Bild(NACHTBLAU)
    for x, y, phase, periode in STERNE:                              # wenige Sterne, funkeln langsam
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    for x in TANNEN:
        tanne(bild, x)
    bild.rechteck(0, 2, PFOSTEN, 11, WAND)                           # Stütze der Rinne
    bild.rechteck(0, 13, B, 1, KANTE)                                # Ufer
    bild.rechteck(0, 14, B, 2, BACH)                                 # Bach
    for x, y, phase in LICHTER:                                      # Lichtpunkte ziehen mit dem Bach
        t = (f + phase) % 51
        if t < 18:
            bild.setze(x + t // 3, y, GLITZER)
    haus(bild)
    # Rinne: unten Holz, darin das Wasser; am Ende fällt es auf das Rad; Eiszapfen
    bild.rechteck(0, 1, RINNE_BIS, 1, HOLZ)
    bild.rechteck(0, 0, RINNE_BIS, 1, WASSER)
    for x, n in ZAPFEN:
        bild.rechteck(x, 2, 1, n, EIS)
    for x, y0, start in TROPFEN:                                     # ab und zu fällt ein Tropfen
        t = f - start
        if 0 <= t < 14:
            y = y0 + (t * t) // 10 if t >= 6 else y0 - 1             # hängt erst, fällt dann schneller
            if y < 13:
                bild.setze(x, y, EIS if t >= 6 else GLITZER)
    rad(bild, f)
    for y in range(CY - 5):                                          # Wasserfall: Lücken laufen mit hinunter
        if (y - f) % 5 != 0:
            bild.setze(RINNE_BIS, y, WASSER)
    vogel(bild, f)
    reh(bild, f)
    return bild


def bilder():
    return [szene(f) for f in range(RUNDE)]
