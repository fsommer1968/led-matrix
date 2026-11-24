"""Schwibbogen: Im dunklen Fenster steht ein Schwibbogen aus dem Erzgebirge. Die sieben Kerzen auf
dem Bogen gehen nacheinander von außen nach innen an, dahinter wird der Scherenschnitt warm
erleuchtet (zwei Bergleute neben Schlägel und Eisen, Tannen, Häuschen mit hellem Fenster), eine
Weile brennt alles ruhig, dann gehen die Lichter von innen nach außen wieder aus, ein Rauchfaden
steigt auf; draußen fällt leichter Schnee. Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ist alles spiegelgleich zur Mitte (die rechte Hälfte
kostet als Kopie der linken wenig), der Bogen fällt in Stufen, deren Kanten möglichst mit den
Kerzen zusammenfallen, Tanne und Bergmann stehen jeweils ganz unter einer Stufe und sind in sich
spiegelgleich, die Kerzen sind zwei gleiche Spalten breit, nur die Flammenspitze (ein Pixel)
wandert langsam hin und her, und ohne Licht ist das Innere so schwarz wie die Figuren. Sterne
gibt es keine, nur sechs Flocken.
"""
from basis import B, NACHTBLAU, SCHWARZ, Bild, dimmen, mischen

NAME = "schwibbogen"
TITEL = "Schwibbogen im Fenster, die Lichter gehen an"

LICHT = (190, 110, 10)                         # warmes Licht hinter der Szene (große Fläche, gedämpft)
HOLZ_DUNKEL, HOLZ = (40, 18, 6), (150, 62, 10)                       # Bogen und Sockel: ohne/mit Licht
WACHS_DUNKEL, WACHS = (70, 0, 0), (235, 0, 0)                        # rote Kerzen
BANK_DUNKEL, BANK = (26, 26, 44), (84, 60, 40)                       # Fensterbank
FLAMME = (255, 205, 40)
SPITZE = (255, 110, 0)                         # Flammenspitze, ein Pixel
GLUT = (150, 30, 0)                            # Docht glimmt nach
RAUCH = (95, 95, 110)
FLOCKE = (150, 160, 200)

MITTE = 31.5
# Bogen: Oberkante je Abstand zur Mitte (bis einschließlich d, Zeile); ganz außen senkrecht
STUFEN = [(9, 4), (15, 5), (19, 6), (22, 7), (24, 8), (26, 9), (27, 10), (28, 11), (29, 12)]
BODEN = 13                                     # unterste Zeile im Bogen; 14 Sockel, 15 Fensterbank
# Kerzen: linke Spalte (zwei Spalten breit), in der Reihenfolge des Anzündens: außen → innen
KERZEN = [7, 55, 14, 48, 22, 40, 31]
AN, AN_TAKT = 14, 9                            # erste Kerze, Abstand der nächsten
AUS, AUS_TAKT = 196, 6                         # die mittlere geht zuerst aus, dann nach außen

# Scherenschnitt, linke Hälfte (rechts gespiegelt); steht auf Zeile 13
HAUS = ["..##..", ".####.", "######", "##..##", "######"]            # mit erleuchtetem Fenster
TANNE = ["..#..", "..#..", ".###.", ".###.", "#####", "#####"]
BERGMANN = [".##.", ".##.", "####", "####", ".##.", ".##.", "#..#"]
KREUZ = ["#..", ".#.", "..#", "..#", ".#.", "#.."]                   # halbes Kreuz aus Schlägel und Eisen
SZENE = [(10, HAUS), (17, TANNE), (24, BERGMANN), (29, KREUZ)]

# Schnee vor dem Fenster: Spalte, Tempo n (17 Zeilen Fallstrecke in 255/n Bildern), Phase
FLOCKEN = [(0, 3, 2), (5, 5, 9), (18, 3, 13), (36, 5, 4), (59, 3, 7), (63, 5, 15)]


def abstand(x):
    return int(abs(x - MITTE))


def bogen_oben(d):
    for bis, y in STUFEN:
        if d <= bis:
            return y
    return None


def an_aus(i):
    """Bild, in dem Kerze i (Reihenfolge des Anzündens) angeht und in dem sie verlischt."""
    return AN + i * AN_TAKT, AUS + (len(KERZEN) - 1 - i) * AUS_TAKT


def brennt(i, f):
    """Wie weit Kerze i brennt: 0 aus … 1 voll (wächst beim Anzünden, fällt beim Löschen)."""
    an, aus = an_aus(i)
    return max(0.0, min(1.0, (f - an) / 6, (aus + 5 - f) / 5))


def zucken(f):
    """Das Licht hinter der Szene zuckt ab und zu ganz leicht (kostet nichts: Die Fläche bleibt
    einfarbig)."""
    if f % 37 in (5, 6, 7):
        return (0.96, 0.92, 0.96)[f % 37 - 5]
    return 0.95 if f % 61 in (30, 31) else 1


def flamme(bild, x, y, i, f, g):
    """Flamme der Kerze i (y = untere Zeile der Flamme); g = wie weit die Kerze brennt."""
    if g >= 0.5:                                                     # brennt: Die Spitze neigt sich langsam
        bild.rechteck(x, y, 2, 1, FLAMME)                            # mal nach links, mal nach rechts
        bild.setze(x + (1 if (f + i * 5) % 17 < 6 else 0), y - 1, SPITZE)
    elif g > 0:                                                      # zündet gerade oder glimmt nach
        bild.rechteck(x, y, 2, 1, SPITZE if f < AUS else GLUT)
    else:                                                            # eben aus: Ein Rauchfaden steigt auf
        t = f - (an_aus(i)[1] + 5)
        if 0 <= t < 9:
            bild.setze(x + (t // 3) % 2, y - t // 3, dimmen(RAUCH, 1 - t // 3 * 0.3))


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        glut = [brennt(i, f) for i in range(len(KERZEN))]
        hell = round((sum(glut) / len(KERZEN)) ** 0.7 * 20) / 20    # Licht hinter der Szene in 20 Stufen
        licht = dimmen(LICHT, hell * zucken(f))
        holz = mischen(HOLZ_DUNKEL, HOLZ, hell)
        for x, n, phase in FLOCKEN:                                  # leichter Schneefall vor dem Fenster
            bild.setze(x, (phase + f * n / 15) % 17 - 1, FLOCKE)
        for x in range(B):
            d = abstand(x)
            oben = bogen_oben(d)
            if oben is not None:
                bild.rechteck(x, oben, 1, BODEN + 1 - oben, licht)   # Licht (überdeckt den Schnee)
                bild.setze(x, oben, holz)
                if d == 29:
                    bild.setze(x, oben + 1, holz)
            if d <= 30:
                bild.setze(x, 14, holz)
            bild.setze(x, 15, mischen(BANK_DUNKEL, BANK, hell))
        for x0, zeilen in SZENE:                                     # Scherenschnitt, spiegelgleich
            y0 = BODEN + 1 - len(zeilen)
            bild.figur(x0, y0, zeilen, {"#": SCHWARZ})
            bild.figur(B - x0 - len(zeilen[0]), y0, zeilen, {"#": SCHWARZ}, spiegeln=True)
        for i, x in enumerate(KERZEN):
            oben = bogen_oben(abstand(x))
            bild.rechteck(x, oben - 2, 2, 2, mischen(WACHS_DUNKEL, WACHS, glut[i]))
            flamme(bild, x, oben - 3, i, f, glut[i])
        liste.append(bild)
    return liste
