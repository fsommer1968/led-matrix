"""Winterwald: Lichtung zwischen verschneiten Tannen unter Mond und Sternen. Ein Reh tritt heraus und
äst, ein Fuchs schnürt von rechts heran, das Reh merkt auf und springt in großen Sätzen davon, der
Fuchs schnuppert an der Stelle und zieht weiter; die Spuren bleiben im Schnee – 255 Bilder.

Sparsam gezeichnet (23.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum hinten ein durchgehender dunkler Waldsaum mit vier
gleich geformten Fichten statt einer Wand aus zehn Tannen, vorn zwei gleiche Tannen im selben
Abstand zu allem (die zweite ist eine Kopie der ersten), drei Sterne, kein Schneefall, Spuren
im festen Vierertakt nur auf der Lichtung.
"""
import math

from basis import B, NACHTBLAU, WEISS, Bild, dimmen, sternschnuppe

NAME = "winterwald"
TITEL = "Reh und Fuchs im Winterwald"

STERN = (255, 240, 200)
STERNE = [(13, 1, 0, 32), (27, 3, 11, 40), (61, 1, 23, 24)]          # x, y, Phase, Periode
SAUM_OBEN = 10                                 # Waldsaum hinten: Zeilen 10 bis 12, durchgehend
FICHTEN = [(18, 4), (27, 3), (34, 4), (45, 3)]                       # hinten: Mitte x, Höhe über dem Saum
VORN = (5, 53)                                 # vorn: zwei gleiche Tannen (die zweite kostet fast nichts)
SPUR_VON, SPUR_BIS = 11, 48                    # Spuren nur zwischen den Tannen, alle vier Spalten
KANTE = (215, 225, 250)
BODEN = (105, 118, 165)
SPUR = (120, 132, 185)
TANNE_HINTEN = (0, 52, 26)
TANNE_VORN = (0, 115, 45)
STAMM = (95, 55, 22)
MOND = (240, 230, 175)
FELL = (205, 120, 45)
FELL_DUNKEL = (105, 58, 22)
FUCHS = (255, 105, 0)
FUCHS_DUNKEL = (160, 60, 0)
NASE = (60, 30, 15)

# Reh (Blick nach rechts): f Fell, d hintere Läufe, w Spiegel, e Lauscher, a Auge, k Nase
REH_STEHT = ["........e.e.", "........fff.", "........fafk", "........ff..", "wffffffff...",
             "wffffffff...", ".f.d..d.f...", ".f.d..d.f...", ".f.d..d.f..."]
REH_GEHT = ["........e.e.", "........fff.", "........fafk", "........ff..", "wffffffff...",
            "wffffffff...", ".f.d..d.f...", "..fd..df....", "..df..fd...."]
REH_AEST = ["............", ".............", ".............", ".............", "wffffffff....",
            "wffffffff.e..", ".f.d..d.fffe.", ".f.d..d.f.faf", ".f.d..d.f..fk"]
REH_WACH = ["........e.e.", "w.......fff.", "w.......fafk", "w.......ff..", "wffffffff...",
            "wffffffff...", ".f.d..d.f...", ".f.d..d.f...", ".f.d..d.f..."]
REH_SATZ = ["...........e.e.", "...........fff.", "w.........ffafk", "wwfffffffff....",
            ".fffffffffffff.", "f.d........d..f"]
REH_LANDET = ["..........e.e..", "..........fff..", "w........ffafk.", "wffffffffff....",
              ".fffffffffff...", "..ffd....dff...", "...fd....df...."]
# Fuchs (Blick nach rechts): f Fell, t Rute, w weiß, d dunkle Läufe
FUCHS_A = ["............e.e.", "...........ffff.", "wtt........fafwk", "wttttffffffffww.", ".ttttffffffff...",
           ".....d.d..d.d...", "....d..d..d..d.."]
FUCHS_B = ["............e.e.", "...........ffff.", ".wtt.......fafwk", "wttttffffffffww.", ".ttttffffffff...",
           ".....d.d..d.d...", ".....d.d..d.d..."]
FUCHS_SCHNUPPERT = ["................", "wtt.........e.e.", "wtttt......ffff.", ".ttttfffffffafw.", "....fffffffffwwk",
                    ".....d.d..d.d...", ".....d.d..d.d..."]

REH_FARBEN = {"f": FELL, "d": FELL_DUNKEL, "w": WEISS, "e": FELL, "a": NASE, "k": NASE}
FUCHS_FARBEN = {"f": FUCHS, "t": FUCHS, "w": WEISS, "d": FUCHS_DUNKEL, "e": FUCHS, "a": NASE, "k": NASE}

REH_X = 22                                     # hier äst das Reh
REH_KOMMT, REH_DA, REH_MERKT, REH_FLIEHT = 8, 52, 138, 148
FUCHS_KOMMT, FUCHS_HALT, FUCHS_WEITER = 118, 170, 184
FUCHS_TEMPO = 0.75


def tanne(bild, x, hoehe, farbe, schnee):
    """Tanne aus Stufen (je drei Zeilen), Schnee auf Spitze und Astenden."""
    fuss = 13
    for k in range(hoehe):
        halb = k // 3 + k % 3
        y = fuss - 1 - hoehe + k
        bild.rechteck(x - halb, y, 2 * halb + 1, 1, farbe)
        if schnee and k % 3 == 2:
            bild.setze(x - halb, y, schnee)
            bild.setze(x + halb, y, schnee)
    bild.setze(x, fuss - 1, STAMM if schnee else farbe)
    if schnee:
        bild.setze(x, fuss - 1 - hoehe, schnee)
        bild.setze(x, fuss - 2 - hoehe, schnee)


def fuchs_x(f):
    if f < FUCHS_HALT:
        return B - (f - FUCHS_KOMMT) * FUCHS_TEMPO
    halt = B - (FUCHS_HALT - FUCHS_KOMMT) * FUCHS_TEMPO
    return halt - max(0, f - FUCHS_WEITER) * FUCHS_TEMPO


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        sternschnuppe(bild, f, 28, 52, 0)
        sternschnuppe(bild, f, 240, 30, 0)
        bild.kreis(41, 3, 2.2, MOND)
        bild.rechteck(0, SAUM_OBEN, B, 13 - SAUM_OBEN, TANNE_HINTEN)    # hinten: dunkler Waldsaum
        for x, h in FICHTEN:                                         # … aus dem einzelne Fichten ragen
            for k in range(h):
                bild.rechteck(x - k, SAUM_OBEN - h + k, 2 * k + 1, 1, TANNE_HINTEN)
        for x in VORN:                                               # vorn: rahmen die Lichtung
            tanne(bild, x, 11, TANNE_VORN, KANTE)
        bild.rechteck(0, 13, B, 1, KANTE)
        bild.rechteck(0, 14, B, 2, BODEN)
        # Spuren im Schnee: bleiben liegen, wo die Tiere gelaufen sind
        reh_von = -13 + (min(f, REH_DA) - REH_KOMMT) * 0.8 if f > REH_KOMMT else -99
        for x in range(SPUR_VON, SPUR_BIS):                          # nur auf der Lichtung
            if x % 4 == 1 and (x < reh_von + 2 or (f > REH_FLIEHT and x % 8 == 1 and x < REH_X + 8
                                                    and x > REH_X + 8 - (f - REH_FLIEHT) * 1.7)):
                bild.setze(x, 13, SPUR)
            if f >= FUCHS_KOMMT and x % 4 == 1 and x > fuchs_x(f) + 14:
                bild.setze(x, 14, dimmen(KANTE, 0.8))
        # Reh
        if REH_KOMMT <= f < REH_DA:                                  # tritt heraus
            x = round(-13 + (f - REH_KOMMT) * 0.8)
            bild.figur(x, 4, REH_GEHT if (f // 4) % 2 else REH_STEHT, REH_FARBEN)
        elif REH_DA <= f < REH_MERKT:                                # äst, hebt zwischendurch den Kopf
            u = f - REH_DA
            oben = u < 8 or 32 <= u < 42 or 68 <= u < 76
            bild.figur(REH_X, 4, REH_STEHT if oben else REH_AEST, REH_FARBEN)
            if not oben and (f // 5) % 2:                            # rupft: Kopf nickt
                bild.setze(REH_X + 12, 12, KANTE)
        elif REH_MERKT <= f < REH_FLIEHT:                            # merkt auf: Spiegel leuchtet
            bild.figur(REH_X, 4, REH_WACH if (f // 2) % 2 else REH_STEHT, REH_FARBEN)
        elif f >= REH_FLIEHT:                                        # springt in Sätzen nach links davon
            t = f - REH_FLIEHT
            x = round(REH_X - 3 - t * 1.7)
            hoch = 4.5 * abs(math.sin(t / 9 * math.pi))
            if x > -16:
                if hoch > 1.5:
                    bild.figur(x, round(7 - hoch), REH_SATZ, REH_FARBEN, spiegeln=True)
                else:
                    bild.figur(x, round(6 - hoch), REH_LANDET, REH_FARBEN, spiegeln=True)
                    if t > 3:
                        for k in range(3):                           # Schnee stiebt beim Aufsetzen
                            bild.setze(x + 12 + k * 2, 12 - (k + f) % 2, dimmen(WEISS, 0.7))
        # Fuchs schnürt von rechts nach links
        if f >= FUCHS_KOMMT:
            x = round(fuchs_x(f))
            if x > -17:
                if FUCHS_HALT + 2 <= f < FUCHS_WEITER - 1:           # schnuppert an der Rehspur
                    figur = FUCHS_SCHNUPPERT
                elif FUCHS_HALT <= f < FUCHS_WEITER:
                    figur = FUCHS_B
                else:
                    figur = FUCHS_A if (f // 3) % 2 else FUCHS_B
                bild.figur(x, 6, figur, FUCHS_FARBEN, spiegeln=True)
        liste.append(bild)
    return liste
