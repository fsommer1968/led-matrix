"""Weihnachtszug: Dampflok (rotes Führerhaus, grüner Kessel, Treibräder mit Kuppelstange) mit drei
bunt beleuchteten Wagen (Tannenbaum, Geschenke, Schneemann) fährt durch die verschneite Nacht –
255 Bilder.

0–90    Zug fährt von links herein, pfeift "TUUT" (vor der Lok ist der Himmel noch frei)
90–187  Zug bleibt in der Bildmitte, die Landschaft zieht vorbei (Tannen, Haus)
187–255 Zug fährt rechts hinaus, "TUUT" zum Abschied hinter dem letzten Wagen

Sparsam gezeichnet, weil die Matrix je Animation nur 80 KB speichert (Ziel ≤ 76000 Bytes,
siehe groesse.py): Jedes Bild wird einzeln und spaltenweise gepackt. Waagerechte Kanten und
gleiche Nachbarspalten kosten nichts, jede senkrechte Kante und jeder Einzelpunkt kostet in
allen 255 Bildern. Darum sind Lok, Wagen und Ladung aus waagerechten Streifen und
spiegelgleichen Hälften gebaut, alle Wagen haben dieselbe Farbe, die Wagenlichter sitzen über
den Rädern, das Gleis hat keine Schwellen, das Land ist flach, und Sterne, Schnee und
Landschaft sind dünn besetzt. Der volle Zug in der Bildmitte ist am teuersten, deshalb steht
er etwas kürzer dort als früher (97 statt 125 Bilder).
"""
import math

from basis import (B, BUNT, GELB, GOLD, NACHTBLAU, PINK, ROT, BLAU, TUERKIS, WEISS, Bild, Schnee,
                   dimmen)

NAME = "zug"
TITEL = "Weihnachtszug mit Tannenbaum, Geschenken und Schneemann"

SCHIENE = (120, 120, 135)
RAD = (115, 115, 140)
RAD_HELL = (255, 255, 255)
HUEGEL = (20, 26, 62)
HUEGEL_KANTE = (55, 65, 105)
TANNE_FERN = (0, 62, 20)
HAUS = (85, 50, 30)
KESSEL = (0, 165, 55)
SCHLOT = (130, 130, 150)
LAMPE = (255, 245, 170)
SCHNEEWEISS = (235, 240, 255)
ZWEIG = (190, 110, 40)
STERNE = ((8, 1, 0, 32), (50, 2, 13, 40))                       # x, y, Phase, Periode
SCHNEE = Schnee(anzahl=2, saat=18, farbe=(120, 130, 175))

LOK = [  # fährt nach rechts, 19 breit, Zeile 4–11; Räder und Schienenräumer kommen dazu
    "............kk.....",
    "rrrrrr......kk.....",
    "rrrrrr......kk.....",
    "rwwrrrgggggggggggl.",
    "rwwrrrggggggggggg..",
    "rrrrrryyyyyyyyyyy..",
    "rrrrrrggggggggggg..",
    "rrrrrrrrrrrrrrrrrr.",
]
LOK_FARBEN = {"k": SCHLOT, "r": ROT, "w": GELB, "g": KESSEL, "y": GOLD, "l": LAMPE}
LOK_BREITE = 19
WAGEN = (0, 90, 220)                            # alle Wagen gleich: gleiche Spalten kosten nichts
ZUG_LAENGE = LOK_BREITE + 3 * 13
EIN, AB = 90, 187                               # Zug steht ab EIN in der Mitte, fährt ab AB hinaus
STANGE = (0, 1, 1, 1, 0, -1, -1, -1)             # Höhe der Kuppelstange je Radstellung

BAUM = [  # 8 breit, spiegelgleich; a/b/c sind Kugeln
    "...**...",
    "...gg...",
    "..gggg..",
    "..agga..",
    ".gggggg.",
    ".gbccbg.",
    "gggggggg",
]
GESCHENKE = [  # 8 breit: rotes Paket mit Band und Schleife, daneben zwei gestapelte
    ".oo.....",
    ".oo.yyyy",
    "roorbbbb",
    "rooryyyy",
    "roortttt",
    "roorpppp",
    "roortttt",
]
SCHNEEMANN = [  # 7 breit, schaut nach vorn; der Zweig rechts winkt
    "..hhh..",
    ".hhhhh.",
    "..www..",
    "..wow..",
    ".rrrrr.",
    ".wwwwwt",
    ".wwwww.",
]


def sterne(bild, f):
    """Funkeln wie basis.Sterne, aber im dunklen Teil der Periode ist der Stern ganz aus."""
    for x, y, phase, periode in STERNE:
        h = 0.5 + 0.5 * math.cos(2 * math.pi * ((f + phase) % periode) / periode)
        if h >= 0.3:
            bild.setze(x, y, dimmen((255, 240, 200), round(h * 4) / 4))


def rad_klein(bild, x, y, phase):
    """2×2-Rad; der helle Streifen wechselt zwischen oben und unten (beide Spalten gleich)."""
    oben = (phase // 2) % 2 == 0
    bild.rechteck(x, y, 2, 1, RAD_HELL if oben else RAD)
    bild.rechteck(x, y + 1, 2, 1, RAD if oben else RAD_HELL)


def lok(bild, x, phase):
    bild.figur(x, 4, LOK, LOK_FARBEN)
    bild.rechteck(x + 16, 13, 1, 2, GOLD)                        # Schienenräumer
    bild.setze(x + 17, 14, GOLD)
    rad_klein(bild, x + 12, 13, phase)
    for rx in (x, x + 6):                                        # Treibräder 3×3
        bild.rechteck(rx, 12, 3, 3, RAD)
    bild.rechteck(x, 13 + STANGE[phase % 8], 9, 1, GOLD)         # Kuppelstange geht auf und ab


def wagen(bild, x, ladung, f, phase):
    bild.rechteck(x, 11, 12, 2, WAGEN)
    licht = BUNT[(f // 12) % len(BUNT)]                          # je ein Licht über den Rädern
    for rx in (x, x + 10):
        bild.rechteck(rx, 11, 2, 1, licht)
        rad_klein(bild, rx, 13, phase)
    if ladung == "baum":
        blink = (f // 6) % 3
        bild.figur(x + 2, 4, BAUM, {
            "g": (0, 190, 40), "*": GELB if (f // 5) % 2 else WEISS,
            "a": ROT if blink != 0 else GOLD, "b": GOLD if blink != 1 else TUERKIS,
            "c": (0, 110, 255) if blink != 2 else PINK})
    elif ladung == "geschenke":
        bild.figur(x + 2, 4, GESCHENKE, {"r": ROT, "o": GOLD, "y": GELB, "b": BLAU, "t": TUERKIS,
                                         "p": PINK})
    elif ladung == "schneemann":
        wink = (f // 8) % 2                                      # winkt mit dem Zweig
        bild.figur(x + 2, 4, SCHNEEMANN, {"h": (70, 80, 200), "w": SCHNEEWEISS, "o": (255, 100, 0),
                                          "r": ROT, "t": None if wink else ZWEIG})
        if wink:
            bild.setze(x + 8, 8, ZWEIG)


def landschaft(bild, versatz):
    bild.rechteck(0, 12, B, 3, HUEGEL)                           # flaches Land mit heller Kante
    bild.rechteck(0, 12, B, 1, HUEGEL_KANTE)
    for i in range(2):                                           # Tannen ziehen vorbei
        tx = round((i * 52 - versatz * 0.7) % 105) - 10
        bild.rechteck(tx, 8, 1, 5, TANNE_FERN)
        bild.rechteck(tx - 1, 10, 3, 3, TANNE_FERN)
        bild.setze(tx, 7, HUEGEL_KANTE)
    hx = round((20 - versatz * 0.5) % (B + 30)) - 15             # Häuschen mit Licht
    bild.rechteck(hx, 10, 6, 3, HAUS)
    bild.rechteck(hx, 9, 6, 1, HUEGEL_KANTE)
    bild.rechteck(hx + 1, 8, 4, 1, HUEGEL_KANTE)
    bild.rechteck(hx + 1, 11, 4, 1, GELB)


def wolke(bild, x, y, groesse, farbe):
    """Dampfwölkchen in vier Größen, unten breiter als oben."""
    if groesse == 0:
        bild.setze(x, y, farbe)
    elif groesse == 1:
        bild.rechteck(x - 1, y, 2, 1, farbe)
        bild.setze(x, y - 1, farbe)
    elif groesse == 2:
        bild.rechteck(x - 1, y, 3, 1, farbe)
        bild.rechteck(x - 1, y - 1, 2, 1, farbe)
    else:
        bild.rechteck(x - 2, y, 4, 1, farbe)
        bild.rechteck(x - 1, y - 1, 2, 1, farbe)


def tuut(bild, x, t, dauer):
    """Buchstaben kommen nacheinander, stehen, verschwinden zusammen."""
    if 0 <= t < dauer:
        n = min(4, t // 3 + 1)
        hell = (t // 5) % 2                                      # T und T gleich, U und U gleich
        bild.text(x, 0, "TUUT"[:n], lambda i: GELB if (i in (1, 2)) == bool(hell) else GOLD)


def bilder():
    dampf = []
    liste = []
    versatz = 0
    phase = 0
    mitte = B // 2 + ZUG_LAENGE // 2 + 1                          # Spitze der Lok in der Mitte
    for f in range(255):
        bild = Bild(NACHTBLAU)
        sterne(bild, f)
        bild.kreis(31, 2, 1.5, (240, 235, 190))
        if EIN <= f < AB:
            versatz += 1
        landschaft(bild, versatz)
        SCHNEE.zeichnen(bild, f)
        bild.rechteck(0, 15, B, 1, SCHIENE)                      # Gleis
        if f < EIN:
            kopf = round(mitte * (f / EIN))
            tempo = 0.8
        elif f < AB:
            kopf, tempo = mitte, 0.0
        else:
            kopf, tempo = mitte + (f - AB) * 2, 2.0
        phase += 2 if f >= AB else 1
        lok_x = kopf - LOK_BREITE
        # Dampf: Wölkchen wachsen und verblassen, bleiben hinter dem Zug zurück
        if f % 7 == 0 and -4 <= lok_x + 12 < B + 2:
            dampf.append([lok_x + 12.0, 3.0, 0])
        for d in dampf:
            alter = d[2]
            c = dimmen((230, 230, 240), (1.0, 0.8, 0.6, 0.45, 0.3)[min(4, alter // 4)])
            wolke(bild, round(d[0]), round(d[1]), min(3, alter // 3), c)
            d[0] -= 1.0 - tempo * 0.6 if tempo < 2 else 0.2
            d[1] -= 0.2 if d[1] > 1.2 else 0
            d[2] += 1
        dampf = [d for d in dampf if d[2] < 18]
        lok(bild, lok_x, phase)
        for nr, ladung in enumerate(("baum", "geschenke", "schneemann")):
            wagen(bild, lok_x - 13 * (nr + 1), ladung, f, phase)
        tuut(bild, 39, f - 20, 30)                               # vor der einfahrenden Lok
        tuut(bild, 3, f - (AB + 16), 30)                         # hinter dem ausfahrenden Zug
        liste.append(bild)
    return liste
