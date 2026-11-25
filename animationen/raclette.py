"""Raclette-Abend: Das Raclette-Gerät steht von vorn über die ganze Breite da – oben die dunkle
Grillplatte mit Würstchen, Champignon und Paprika (es dampft), darunter der glühende Heizstab,
unten vier bunte Pfännchen (rot, blau, grün, gelb). Die blasse Käsescheibe in den Pfännchen wird
gelb, wirft Blasen und bräunt vom Rand her. Reihum zieht eine Hand ein Pfännchen heraus, der Käse
gleitet auf die Kartoffel auf dem Teller daneben, beim Wegziehen spannt sich ein Faden und reißt,
und das Pfännchen kommt mit einer frischen Scheibe wieder ins Fach. Die vier Pfännchen laufen
versetzt, die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ist das Gerät in allen Spalten gleich (Platte, Heizstab
und Boden als durchgehende Zeilen), der Heizstab atmet über die ganze Breite in fünf Stufen.
Alles andere hält sich an das Spaltenraster der Pfännchen (Rand, drei Käsespalten, drei
Griffspalten, drei Käsespalten, Rand, Lücke): Die Scheibe füllt das Pfännchen ganz, Grillgut sitzt
genau über Griff oder Lücke, die Kartoffel steht in der Lücke, die Bräune liegt auf den Randspalten
und den äußeren Dritteln. Jedes Stück Grillgut und jedes Dampfwölkchen kostet rund 2 KB bzw. 0,4 KB.
"""
import math

from basis import B, Bild, dimmen

NAME = "raclette"
TITEL = "Raclette-Abend"

GERAET = (72, 80, 118)                         # Grillplatte, Seitenwände, Boden (dunkel, große Fläche)
# Heizstab in fünf deutlich verschiedenen Stufen von hell nach dunkel
GLUT = [(255, 100, 0), (255, 70, 0), (240, 42, 0), (205, 24, 0), (165, 14, 0)]
FRISCH = (255, 244, 170)                       # frische Käsescheibe, blass
HALBGELB = (255, 232, 100)                     # wird warm
KAESE = (255, 222, 30)                         # geschmolzen, kräftig gelb (zitroniger als das gelbe Pfännchen)
# An der Matrix gemessen (25.11.2026): Braun und Hauttöne wirken orange, darum Braun deutlich
# dunkler und weniger gesättigt, Haut und Kartoffel blass.
GOLDBRAUN = (135, 82, 42)                      # überbacken
KRUSTE = (85, 50, 30)                          # dunkel angebackener Rand
KARTOFFEL = (170, 140, 90)
HAND = (255, 205, 170)
TELLER = (110, 128, 185)                       # Porzellan, bläulich und gedämpft
PILZ = (225, 205, 170)
STIEL = (160, 135, 100)
WURST = (130, 70, 45)                          # Würstchen oben, darunter dunkler
WURST_UNTEN = (85, 45, 28)
PAPRIKA_ROT = (255, 0, 30)
PAPRIKA_GRUEN = (0, 190, 30)
DAMPF = (125, 130, 150)
DAMPF_DUENN = (62, 65, 78)

Y_GRILL, Y_PLATTE, Y_GLUT, Y_BODEN = 1, 3, 4, 9    # Zeilen: Grillgut (zwei), Platte, Heizstab, Boden
Y_DRIN, Y_DRAUSSEN = 8, 12                     # Bodenzeile des Pfännchens im Fach und herausgezogen
PULS = 51                                      # Bilder je Atemzug des Heizstabs (teilt 255)
DAMPF_RUNDE = 85                               # Bilder, bis ein Dampfwölkchen wiederkommt (teilt 255)

# Pfännchen (elf breit): linke Spalte, Farbe, Start im Umlauf, Seite der Kartoffel (+1 rechts, -1 links).
# Zwischen 1 und 2 sowie 3 und 4 ist die Lücke fünf Spalten breit (dort steht der Teller), in der
# Mitte vier. Das gelbe Pfännchen ist dottergelb, damit sich der Käse darin abhebt.
PFANNEN = [(3, (255, 0, 40), 0, 1), (19, (0, 70, 255), 128, -1),
           (34, (0, 185, 0), 64, 1), (50, (255, 165, 0), 191, -1)]

# Ablauf eines Pfännchens (t = Bilder seit seinem Start):
HAND_DA = 6                                    # Hand ist von unten am Griff, der Teller steht
ZIEHEN_AB = 8                                  # herausziehen (vier Zeilen, alle zwei Bilder eine)
SCHIEBEN_AB = 18                               # Käse gleitet auf die Kartoffel (zehn Spalten)
LIEGT_AB = 38                                  # Käse liegt als Haube auf der Kartoffel
FORT_AB = 41                                   # leeres Pfännchen schräg nach unten hinaus, der Faden spannt sich
NEU_AB = 58                                    # mit frischer Scheibe wieder hinauf ins Fach
DRIN_AB = 68                                   # steht im Fach, die Hand geht
TELLER_FORT = 62                               # Teller mit Kartoffel sinkt nach unten weg
# Schmelzen (Bilder nach DRIN_AB): wird wärmer, dann gelb, wirft Blasen, Kruste über dem Rand,
# zuletzt die äußeren Drittel goldbraun
HALB, WEICH, BLASEN, BRAUN, BRAUN_2 = 22, 40, 64, 112, 146
# Blasen, je drei Bilder lang: Spalte im Pfännchen und Breite (1 = Blase, 3 = Beule über einem Drittel)
BLASEN_FOLGE = [(3, 1), (7, 3), (5, 1), (1, 3), (9, 1), (4, 3), (1, 1), (7, 3), (6, 1), (1, 3), (7, 1), (4, 3)]
FADEN = [0, 0, 1, 2, 3, 3, 2, 1]               # Länge des Fadens je Schritt beim Wegziehen (reißt nach Schritt 5)

# Grillgut auf der Platte, genau über Lücke (mit Randspalten) oder Griff: Spalte, Zeilen, Farben
ROT_STUECK = (["rrr", "rrr"], {"r": PAPRIKA_ROT})
GRUEN_STREIFEN = (["...", "ggg"], {"g": PAPRIKA_GRUEN})
WUERSTCHEN = (["wwwwwww", "vvvvvvv"], {"w": WURST, "v": WURST_UNTEN})
CHAMPIGNON = (["pppppp", ".ssss."], {"p": PILZ, "s": STIEL})
GRILLGUT = [(7, ROT_STUECK), (13, WUERSTCHEN), (23, GRUEN_STREIFEN), (29, CHAMPIGNON),
            (38, ROT_STUECK), (44, WUERSTCHEN), (54, GRUEN_STREIFEN)]
# Dampfwölkchen: Spalte, Zeile (1 = über einem flachen Streifen, 0 = über einem hohen Stück),
# Drift (+1 rechts, -1 links), Versatz im Umlauf
DAMPF_ORTE = [(24, 1, 1, 0), (47, 0, 1, 17), (16, 0, -1, 34), (55, 1, -1, 51), (32, 0, -1, 68)]


def geraet(bild, f):
    """Gehäuse von vorn: Grillplatte, Heizstab (atmet in fünf Stufen), Boden, Seitenwände."""
    glut = GLUT[round(2 - 2 * math.cos(2 * math.pi * (f % PULS) / PULS))]
    bild.rechteck(0, Y_PLATTE, B, 1, GERAET)
    bild.rechteck(2, Y_GLUT, B - 4, 1, glut)
    bild.rechteck(0, Y_BODEN, B, 1, GERAET)
    bild.rechteck(0, Y_PLATTE, 2, Y_BODEN - Y_PLATTE + 1, GERAET)
    bild.rechteck(B - 2, Y_PLATTE, 2, Y_BODEN - Y_PLATTE + 1, GERAET)
    for x, (zeilen, farben) in GRILLGUT:
        bild.figur(x, Y_GRILL, zeilen, farben)
    for x, y, drift, versatz in DAMPF_ORTE:                          # steigt auf, wird breiter, dünner, vergeht
        stufe = (f + versatz) % DAMPF_RUNDE // 6                     # je sechs Bilder
        if stufe < 3:
            breit = 2 if stufe > y else 1
            bild.rechteck(min(x, x + drift * (breit - 1)), max(0, y - stufe), breit, 1,
                          DAMPF_DUENN if stufe == 2 else DAMPF)


def kaese(bild, x0, y, tm, blasen=True):
    """Käse im Pfännchen (Boden in Zeile y) nach tm Bildern unter dem Heizstab."""
    farbe = FRISCH if tm < HALB else HALBGELB if tm < WEICH else KAESE
    bild.rechteck(x0 + 1, y - 2, 9, 2, farbe)                        # Scheibe: blass, wärmer, gelb geschmolzen
    if tm >= BRAUN_2:                                                # überbacken: die äußeren Drittel goldbraun
        bild.rechteck(x0 + 1, y - 2, 3, 1, GOLDBRAUN)
        bild.rechteck(x0 + 7, y - 2, 3, 1, GOLDBRAUN)
    if blasen and tm >= BLASEN:                                      # abwechselnd eine kleine Blase und eine
        ort, breit = BLASEN_FOLGE[(tm - BLASEN) // 3 % len(BLASEN_FOLGE)]   # Beule über einem Drittel
        bild.rechteck(x0 + ort, y - 3, breit, 1, KAESE)


def pfanne(bild, x0, y, farbe, kruste=False):
    """Pfännchen von vorn: Boden elf breit in Zeile y, Rand eine Zeile hoch, Griff darunter;
    `kruste` = über dem Rand ist Käse angebacken."""
    bild.rechteck(x0, y, 11, 1, farbe)
    bild.rechteck(x0 + 4, y + 1, 3, 2, farbe)
    for x in (x0, x0 + 10):
        bild.setze(x, y - 1, farbe)
        if kruste:
            bild.setze(x, y - 2, KRUSTE)


def hand(bild, x0, oben, farbe):
    """Hand von unten am Griff: fünf breit, darunter der Ärmel."""
    bild.rechteck(x0 + 3, oben, 5, 2, HAND)
    bild.rechteck(x0 + 3, oben + 2, 5, 16, dimmen(farbe, 0.4))


def stelle(x0, seite, u):
    """Spalte u in Schieberichtung: 0–8 Käse im Pfännchen, 9 sein Rand, 10–14 Lücke mit der
    Kartoffel, 15 der Rand des Nachbarn."""
    return x0 + 1 + u if seite > 0 else x0 + 9 - u


def teller(bild, x0, seite, dy):
    """Teller mit Kartoffel in der Lücke neben dem Pfännchen (dy = noch so viele Zeilen zu tief)."""
    links = min(stelle(x0, seite, 9), stelle(x0, seite, 15))
    bild.rechteck(links, 15 + dy, 7, 1, TELLER)
    bild.rechteck(links + 1, 12 + dy, 5, 3, KARTOFFEL)
    bild.rechteck(links, 13 + dy, 7, 1, KARTOFFEL)


def haube(bild, x0, seite, dy, nah):
    """Käse auf der Kartoffel: zwei Zeilen dick, an den Seiten läuft er herunter."""
    bild.rechteck(min(stelle(x0, seite, 10), stelle(x0, seite, 14)), 10 + dy, 5, 2, KAESE)
    bild.rechteck(stelle(x0, seite, 15), 11 + dy, 1, 2, KAESE)
    if nah:
        bild.rechteck(stelle(x0, seite, 9), 11 + dy, 1, 2, KAESE)


def bild_nr(f):
    """Das Bild f der Runde; alles hängt nur von f modulo 255, 85 und 51 ab."""
    bild = Bild()
    geraet(bild, f)
    for x0, farbe, start, seite in PFANNEN:
        t = (f - start) % 255
        if t >= DRIN_AB:                                             # im Fach, der Käse schmilzt
            pfanne(bild, x0, Y_DRIN, farbe, kruste=t - DRIN_AB >= BRAUN)
            kaese(bild, x0, Y_DRIN, t - DRIN_AB)
            if t < DRIN_AB + 8:                                      # die Hand zieht sich zurück
                hand(bild, x0, Y_DRIN + 2 + (t - DRIN_AB), farbe)
            continue
        # ── Teller mit Kartoffel: steigt auf, bekommt den Käse, sinkt wieder ──
        if 2 <= t < TELLER_FORT + 5:
            dy = max(0, HAND_DA - t) if t < TELLER_FORT else t - TELLER_FORT + 1
            teller(bild, x0, seite, dy)
            if t >= LIEGT_AB:
                haube(bild, x0, seite, dy, nah=t >= FORT_AB)
        x, y = x0, Y_DRIN
        if t < ZIEHEN_AB:                                            # Hand kommt von unten an den Griff
            oben = max(Y_DRIN + 2, 16 - t)
        elif t < FORT_AB:                                            # herausziehen und halten
            y += min(4, (t - ZIEHEN_AB + 1) // 2)
            oben = y + 2
        elif t < NEU_AB:                                             # leer schräg nach unten hinaus, von der
            schritt = (t - FORT_AB + 1) // 2                         # Kartoffel weg; der Faden spannt sich
            x, y = x0 - seite * schritt, Y_DRAUSSEN + schritt
            oben = y + 2
            for k in range(FADEN[schritt] if schritt < len(FADEN) else 0):   # schräg von der Haube zum Rand
                bild.setze(stelle(x0, seite, 8 - k), 13 + k, KAESE)
        else:                                                        # frisch belegt wieder hinauf
            y += DRIN_AB - t
            oben = y + 2
        pfanne(bild, x, y, farbe, kruste=t < NEU_AB and y < 16)
        hand(bild, x, oben, farbe)
        if t < SCHIEBEN_AB:                                          # überbackener Käse, blubbert nur im Fach
            kaese(bild, x, y, 255 - DRIN_AB + t, blasen=t < ZIEHEN_AB)
        elif t < LIEGT_AB:                                           # Käse gleitet zur Seite auf die Kartoffel,
            s = (t - SCHIEBEN_AB + 1) // 2                           # über ihr zerfließt die gebräunte Haut
            for u in range(s, min(8 + s, 14) + 1):
                braun = u < 9 and not 3 <= u - s <= 5
                bild.setze(stelle(x0, seite, u), y - 2, GOLDBRAUN if braun else KAESE)
                bild.setze(stelle(x0, seite, u), y - 1, KAESE)
            if s >= 7:
                bild.rechteck(stelle(x0, seite, 15), 11, 1, 2, KAESE)
        elif t >= NEU_AB:
            kaese(bild, x, y, 0)
    return bild


def bilder():
    return [bild_nr(f) for f in range(255)]
