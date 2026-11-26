"""Schneesturm: Ein Schwarzwaldhaus mit tief heruntergezogenem Walmdach und warm leuchtenden Fenstern
steht zwischen dunklen Tannen. Unter einer schweren Wolkendecke treibt der Sturm den Schnee in
schrägen Streifen von links nach rechts, die Tannen biegen sich im Takt der Böen, ein Fensterladen
klappert auf und zu, vom First weht eine Schneefahne, links am Haus türmt sich die Schneewehe. Dann
legt sich der Sturm: Die Streifen werden kürzer und steiler, die Wolken ziehen ab, ein paar Flocken
sinken senkrecht, der Mond kommt durch und lässt Dach und Schnee aufleuchten, auf den Tannen bleibt
Schnee liegen. Zum Schluss schiebt sich eine neue Wolkenfront vor den Mond, es frischt wieder auf,
die erste Böe schüttelt die Tannen frei und fegt die lockere Wehe ab – 255 Bilder, die Runde geht
ohne Sprung in sich über.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum wenige, kräftige Schneestreifen statt dichtem Gestöber
(im Sturm fast waagerecht: je Zeile drei gleiche Nachbarspalten, ein langer Streifen kostet kaum
mehr als ein kurzer), eine glatte Wolkendecke über die ganze Breite, einfarbiges Dach mit nur vier
Walmspalten je Seite, drei gleiche Fenster unter dem First, vier gleiche schlanke Tannen (die
anderen drei sind Kopien der ersten, auch wenn sie sich biegen), drei Sterne, die Wehe nur links
vom Haus. Das Mondlicht ist ein reiner Farbwechsel und kostet nichts. Der Schnee ist ein kleines
Teilchenspiel ohne Zufall, das nur vom Bild in der Runde abhängt: Zwei Runden laufen vor, die
dritte ist dann in sich geschlossen.
"""
import math

from basis import B, NACHTBLAU, WEISS, Bild, dimmen

NAME = "schneesturm"
TITEL = "Schwarzwaldhaus im Schneesturm"

RUNDE = 255
WOLKE = (40, 42, 60)                           # Wolkendecke: dunkles Grau, deutlich über dem Nachthimmel
# Schnee in drei deutlichen Stufen: unter Wolken, Mond halb frei, Mondlicht – (Kante, Boden, Dach)
SCHNEE = [((160, 170, 200), (80, 90, 128), (112, 122, 160)),
          ((188, 198, 225), (92, 104, 146), (131, 142, 182)),
          ((215, 225, 250), (105, 118, 165), (150, 162, 205))]
WAND = (49, 19, 0)                             # Holzwand, auf den LEDs dunkles Braun
FENSTER = (255, 185, 40)
LADEN = (0, 170, 40)                           # grüner Fensterladen
LADEN_KANTE = (60, 255, 60)                    # … von der Seite gesehen, im Schwung
TANNE = (0, 95, 35)
STAMM = (33, 18, 7)
MOND = (240, 230, 170)
STERN = (255, 240, 200)
FLOCKE = (200, 210, 240)

# Haus: Dach Zeilen 4 bis 10 (First 15 Spalten, Traufe 23), Wand Zeilen 11 bis 13
HAUS_X, HAUS_B = 21, 23                        # linke Ecke der Traufe, Breite
WALM = (10, 9, 7, 5)                           # Walm: oberste Dachzeile je Spalte von außen, unten ausgestellt
WAND_X, WAND_B = 23, 19
FENSTER_X = (25, 30, 35)                       # drei Fenster, je drei Spalten; am rechten hängt der Laden
LADEN_X = 38                                   # offen: rechts neben dem rechten Fenster
TANNEN = (3, 10, 51, 58)                       # vier gleiche Tannen, Mitte x (zwei Paare im selben Abstand)
HOEHE = 10
ASTWERK = (0, 0, 1, 1, 2, 1, 2, 2, 1, 2)       # halbe Breite je Zeile von oben: zwei Kerben, nie breiter als fünf Spalten
FAHNE_X = HAUS_X + HAUS_B - len(WALM)          # hier reißt die Böe den Schnee vom First
MOND_X = 44
STERNE = [(17, 1, 0, 51), (33, 1, 20, 85), (55, 2, 40, 51)]          # x, y, Phase, Periode (teilt 255)

# Ablauf: Wind 0 (still) bis 1 (Sturm)
STURM_VOLL, STURM_ENDE, STILL_AB, STILL_BIS = 30, 100, 136, 212
WIND_START = 0.6                               # so stark weht es am Rundenanfang (und am Ende wieder)
BOEEN = 10                                     # Böen je Runde
AUFKLAREN, FRONT = 128, 208                    # Wolken ziehen nach rechts ab, neue Front kommt von links
FRANSEN = (3, 1, 0, 2)                         # ausgefranster Wolkenrand je Zeile
RATE_STURM, RATE_STILL, FALL = 0.52, 0.10, 0.32     # neue Streifen je Bild im Sturm, Flocken in der Stille; Fallen in Pixel je Bild
SAAT = 5                                       # Anfang in der Folge der Startplätze (so gewählt, dass die Runde klein bleibt)
HAUBE_AB = (124, 132)                          # Schnee bleibt liegen: erst auf den Wipfeln, dann auf den Ästen
# Schneewehe: Höhe in halben Stufen – wächst im Sturm, sackt in der Stille, wird am Ende abgefegt
WEHE = ((0, 1.0), (14, 1.5), (28, 2.0), (42, 2.5), (56, 3.0), (70, 3.5), (84, 4.0),
        (150, 3.5), (186, 3.0), (220, 2.5), (230, 2.0), (240, 1.5), (249, 1.0))


def wind(f):
    """Windstärke 0…1 über die Runde; am Ende wieder so wie am Anfang."""
    f %= RUNDE
    if f < STURM_VOLL:
        return WIND_START + (1 - WIND_START) * f / STURM_VOLL
    if f < STURM_ENDE:
        return 1.0
    if f < STILL_AB:
        return 0.5 + 0.5 * math.cos(math.pi * (f - STURM_ENDE) / (STILL_AB - STURM_ENDE))
    if f < STILL_BIS:
        return 0.0
    return WIND_START * (f - STILL_BIS) / (RUNDE - STILL_BIS)


def boe(f):
    """Böe 0…1, zehnmal je Runde."""
    return max(0.0, math.sin(2 * math.pi * f * BOEEN / RUNDE))


def biegung(f):
    """So viele Pixel neigen sich die Wipfel nach rechts (0 bis 3)."""
    return round(wind(f) * (1 + 2 * boe(f)))


HAUBE_WEG = min(f for f in range(STILL_BIS, RUNDE) if biegung(f))   # die erste Böe schüttelt die Tannen frei


def bewoelkt(x, y, f):
    """Liegt die Wolkendecke (Zeilen 0 bis 3) über diesem Pixel?"""
    if y > 3:
        return False
    if f < AUFKLAREN:
        return True
    if x >= (f - AUFKLAREN) * 1.4 + FRANSEN[y]:                      # alte Decke zieht nach rechts ab
        return True
    return f >= FRONT and x <= (f - FRONT) * 1.5 - FRANSEN[y]        # neue Front von links


def mondlicht(f):
    """0 = Wolkendecke, 1 = Mond halb frei, 2 = klar."""
    frei = sum(not bewoelkt(MOND_X + x, y, f) for x in range(4) for y in range(4))
    return 0 if frei == 0 else 1 if frei < 16 else 2


def tanne(bild, x, f, schnee):
    """Schlanke dunkle Tanne (fünf Spalten, zwei Kerben); der Wipfel biegt sich in den Böen nach
    rechts, die Mitte halb so weit, der Fuß bleibt stehen. In der Stille liegt Schnee auf."""
    b = biegung(f)
    haube = sum(f >= ab for ab in HAUBE_AB) if f < HAUBE_WEG else 0
    for k in range(HOEHE):
        halb = ASTWERK[k]
        y = 13 - HOEHE + k
        dx = round(b * ((HOEHE - 1 - k) / (HOEHE - 1)) ** 1.6)
        bild.rechteck(x - halb + dx, y, 2 * halb + 1, 1, TANNE)
        if haube and k == 0:
            bild.setze(x, y, schnee)
        if haube > 1 and k == 4:
            bild.setze(x - halb, y, schnee)
            bild.setze(x + halb, y, schnee)
    bild.setze(x, 13, STAMM)
    t = f - HAUBE_WEG
    if 0 <= t < 4:                                                   # der abgeschüttelte Schnee stiebt davon
        for px, py in ((x + 2 + 2 * t, 3 + t), (x + 3 + 2 * t, 3 + t), (x + 3 + 2 * t, 7 + t)):
            if bild.hole(px, py) in (NACHTBLAU, WOLKE):
                bild.setze(px, py, schnee)


def haus(bild, f, kante, dach):
    """Schwarzwaldhaus: Walmdach unter Schnee bis fast zum Boden, Holzwand, drei helle Fenster."""
    for i, oben in enumerate(WALM):                                  # Walm links und rechts gleich
        for x in (HAUS_X + i, HAUS_X + HAUS_B - 1 - i):
            bild.rechteck(x, oben, 1, 11 - oben, dach)
    bild.rechteck(HAUS_X + len(WALM), 4, HAUS_B - 2 * len(WALM), 1, kante)       # First unter Schnee
    bild.rechteck(HAUS_X + len(WALM), 5, HAUS_B - 2 * len(WALM), 6, dach)
    bild.rechteck(WAND_X, 11, WAND_B, 3, WAND)
    for x in FENSTER_X:
        bild.rechteck(x, 11, 3, 2, FENSTER)
    # Fensterladen: im Sturm schlägt er bei jeder Böe zweimal zu
    takt = f * BOEEN / RUNDE % 1
    zu = wind(f) > 0.25 and (0.14 <= takt < 0.30 or 0.42 <= takt < 0.52)
    schwung = wind(f) > 0.25 and (0.10 <= takt < 0.34 or 0.38 <= takt < 0.56) and not zu
    if zu:
        bild.rechteck(FENSTER_X[2], 11, 3, 2, LADEN)
    elif schwung:
        bild.rechteck(LADEN_X, 11, 1, 2, LADEN_KANTE)
    else:
        bild.rechteck(LADEN_X, 11, 3, 2, LADEN)


def wehe(bild, f, kante):
    """Schneewehe an der Wetterseite: Keil links vom Haus, unter der Traufe bis an die Wand."""
    d = [stufe for ab, stufe in WEHE if f >= ab][-1]
    for x in range(8, WAND_X):
        h = math.floor(d - (HAUS_X - 1 - x) / 2) if x < HAUS_X else min(math.floor(d), 3)
        if h > 0:
            bild.rechteck(x, 14 - h, 1, h, kante)


def schnee():
    """Teilchenspiel: je Bild die Liste (x, y, Länge, Steigung) der Streifen und Flocken. Die
    Startplätze folgen dem goldenen Schnitt (gleichmäßig verteilt, keine Klumpen, kein Zufall).
    Zwei Runden Vorlauf, damit die Runde in sich geschlossen ist."""
    teilchen, je_bild = [], []
    for lauf in range(3 * RUNDE):
        f = lauf % RUNDE
        if f == 0:
            konto, nummer = 0.0, SAAT
        w = wind(f) * (0.85 + 0.15 * boe(f))
        konto += RATE_STILL + RATE_STURM * w * (1 + 0.7 * boe(f))    # in den Böen mehr
        while konto >= 1:
            konto -= 1
            nummer += 1
            links = -46 * w - 2                                      # im Sturm kommt der Schnee auch von der Seite
            teilchen.append([links + (B - 1 - links) * (nummer * 0.618034 % 1), -1.0,
                             0.8 + 0.4 * (nummer * 0.754878 % 1)])
        vx, vy = 4.4 * w, 1.15 * w                                   # im Sturm fast waagerecht (drei Spalten je Zeile)
        for t in teilchen:
            t[0] += vx
            t[1] += vy + FALL * t[2]
        teilchen = [t for t in teilchen if t[1] < 15 and t[0] < B + 8]
        if lauf >= 2 * RUNDE:
            laenge = 1 if w < 0.2 else 2 + round(6 * w)
            je_bild.append([(t[0], t[1], laenge, (vy + FALL) / vx if vx else 0) for t in teilchen])
    return je_bild


def bilder():
    liste = []
    flug = schnee()
    for f in range(RUNDE):
        bild = Bild(NACHTBLAU)
        kante, boden, dach = SCHNEE[mondlicht(f)]
        bild.figur(MOND_X, 0, [".mm.", "mmmm", "mmmm", ".mm."], {"m": MOND})
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        for y in range(4):                                           # Wolkendecke davor
            for x in range(B):
                if bewoelkt(x, y, f):
                    bild.setze(x, y, WOLKE)
        for x in TANNEN:
            tanne(bild, x, f, kante)
        bild.rechteck(0, 14, B, 1, kante)
        bild.rechteck(0, 15, B, 1, boden)
        haus(bild, f, kante, dach)
        wehe(bild, f, kante)
        fahne = round(4 * wind(f) * boe(f)) + (f % 2 if boe(f) > 0.5 else 0)    # Schneefahne am First, flattert
        for i in range(fahne if wind(f) > 0.4 else 0):
            bild.setze(FAHNE_X + i, 4 + i // 3, WEISS if i < 3 else kante)
        for x, y, laenge, steigung in flug[f]:                       # Schnee vor Himmel, Wolken, Tannen und Dach
            for i in range(laenge):
                px, py = round(x) - i, round(y - i * steigung)
                if bild.hole(px, py) in (NACHTBLAU, WOLKE, TANNE, dach):
                    bild.setze(px, py, WEISS if laenge > 1 else FLOCKE)
        liste.append(bild)
    return liste
