"""Hundeschlitten: Vier Huskys (grau-weiß, rotes Geschirr, Ringelrute) ziehen im Galopp den Schlitten
durch die verschneite Nacht; hinten steht eine Person in dicker roter Jacke und gelber Mütze auf den
Kufen, hinter dem Schlitten stäubt der Schnee. Das Gespann bleibt im Bild, die Landschaft zieht vorbei:
nahe Tannen schnell, eine ferne Tanne am Horizont langsam (Parallaxe); links ein ferner Berg, rechts
der Mond. Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum sind die vier Hunde gleich, laufen im Gleichschritt und
stehen genau zehn Spalten auseinander vor einfarbigem Grund – der zweite bis vierte sind Kopien des
ersten und kosten fast nichts. Alles, was hinter den Hunden von Spalte zu Spalte anders ist, macht
sie wieder teuer: Deshalb ist der Horizont dort flach, der Berg steht fest links hinter dem
Schlitten, und es ziehen nur zwei nahe Tannen und eine ferne vorbei. Zwei Sterne über Schlitten und
erstem Hund (dort sind die Spalten ohnehin einzeln), kein Schneefall.
"""
from basis import B, GELB, HAUT, NACHTBLAU, ROT, WEISS, Bild, dimmen

NAME = "hundeschlitten"
TITEL = "Huskygespann zieht den Schlitten durch den Schnee"

KANTE = (215, 225, 250)                        # Oberkante der Spur, Schnee auf den Tannen
BODEN = (78, 90, 140)                          # darunter gedämpft
KAMM = (120, 135, 190)                         # Horizont und Kamm des Berges
FERN = (20, 27, 58)                            # Ebene und Berg dahinter, dunkel (große Fläche)
FELL = (96, 104, 130)
LEINE = (190, 150, 70)
JACKE = (255, 50, 0)
HOSE = (0, 110, 255)
HOLZ = (210, 120, 30)
KUFE = (140, 140, 165)
SACK = (0, 170, 60)
TANNE = (0, 95, 35)
STAMM = (90, 50, 20)
MOND = (240, 230, 170)
STERN = (255, 240, 200)
STERNE = [(9, 0, 0, 51), (23, 2, 20, 85)]      # x, y, Phase, Periode

FUSS = 13                                      # unterste Zeile der Figuren; darunter die Spur
HORIZONT = 5                                   # Kammzeile der Ebene
BERG = [(3, 3), (10, 2), (12, 3), (15, 4)]     # links: bis Spalte … diese Kammzeile, danach HORIZONT
SCHLITTEN_X = 5
HUND_X = SCHLITTEN_X + 12                      # erster Hund, die anderen je ABSTAND weiter
ABSTAND = 10
SCHRITTE = 84                                  # Beinstellungen je Runde: 21 Galoppsprünge, je drei Bilder

# Die Runde schließt, weil alle Takte in 255 Bildern aufgehen: nahe Tannen 255 Spalten, ferne Tanne
# 85 Spalten (eine Spalte alle drei Bilder), 84 Beinstellungen, Staub alle 3, Sterne 51 und 85.
TANNEN = [(40, 12), (168, 11)]                 # nah: Ort in der 255 Spalten langen Welt, Höhe
FERNE_TANNE = (40, 4)                          # fern: Ort in der 85 Spalten langen Welt, Höhe; sie fehlt
#                                                im Bild nur, während die zweite nahe Tanne durchzieht

# Husky (Blick nach rechts), 10 breit: Die Spalten 0 und 1 tragen die Zugleine, die weiße
# Rutenspitze kommt je Beinstellung dazu. g Fell, e Ohren, T Rute, w weiß, r Geschirr, l Leine
HUND = ["......e.e.",
        ".T....ggg.",
        "..ggggggww",
        "..gggrgww.",
        "llwwwrww.."]
BEINE = [["..w....w..", ".w......w."],            # gestreckt
         ["..w...w...", ".w....w..."],            # vorn aufgesetzt
         ["...w..w...", "....ww...."],            # untergezogen
         ["...w...w..", "...w....w."]]            # hinten abgedrückt
RUTE = [1, 1, 2, 2]                            # Spalte der Rutenspitze: steht hoch, ringelt sich nach vorn
HUND_FARBEN = {"g": FELL, "e": FELL, "T": FELL, "w": WEISS, "r": ROT, "l": LEINE}

# Schlitten, 12 breit: m Mütze, h Gesicht, j Jacke, p Hose, b Lenkbügel, s Sack, w Ladefläche,
# r Kufe, l Zugleine; die beiden mittleren Spalten der Person und drei der Ladefläche sind gleich
SCHLITTEN = [".mm.........",
             ".mmh........",
             "jjjj........",
             "jjjjb.......",
             "jjjjbss.....",
             ".pp.bss.....",
             ".pp.bwwwwwwl",
             ".pp.b.....w.",
             "rrrrrrrrrrr."]
SCHLITTEN_FARBEN = {"m": GELB, "h": HAUT, "j": JACKE, "p": HOSE, "b": HOLZ, "s": SACK, "w": HOLZ,
                    "r": KUFE, "l": LEINE}
# Schnee stäubt hinter den Kufen: zwei Wölkchen (je zwei gleiche Spalten), Ort und Helligkeit je Bild
STAUB = [[(-1, 0, 1.0), (-4, -2, 0.5)], [(-2, -1, 0.85), (-5, -1, 0.4)], [(-3, -2, 0.7), (-1, 0, 0.6)]]


def kamm(x):
    """Kammzeile: links der ferne Berg, sonst der flache Horizont."""
    for bis, zeile in BERG:
        if x < bis:
            return zeile
    return HORIZONT


def tanne(bild, x, hoehe):
    """Nahe Tanne hinter dem Gespann: Spitze, drei Spalten, unten fünf; Schneehaube und Schnee auf
    einem Ast (über den Hunden, damit er nicht mit ihrem Weiß verschwimmt), Stamm."""
    oben = FUSS + 1 - hoehe
    bild.rechteck(x, oben, 1, hoehe - 1, TANNE)
    bild.rechteck(x - 1, oben + 2, 3, hoehe - 3, TANNE)
    bild.rechteck(x - 2, oben + 5, 5, hoehe - 6, TANNE)
    bild.setze(x, FUSS, STAMM)
    bild.setze(x, oben, KANTE)
    bild.setze(x - 1, oben + 2, KANTE)


def ferne_tanne(bild, x, hoehe):
    """Kleine Tanne auf dem Horizont: steht ganz über den Hunden, drei Spalten breit."""
    bild.rechteck(x, HORIZONT - hoehe, 1, hoehe, TANNE)
    bild.rechteck(x - 1, HORIZONT - hoehe + 2, 3, hoehe - 2, TANNE)
    bild.setze(x, HORIZONT - hoehe, KANTE)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # zwei Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        bild.kreis(60, 2, 2.2, MOND)                                 # sitzt auf dem Horizont auf
        for x in range(B):                                           # Ebene und Berg, darüber der helle Kamm
            y0 = kamm(x)
            bild.setze(x, y0, KAMM)
            bild.rechteck(x, y0 + 1, 1, FUSS - y0, FERN)
        wx, hoehe = FERNE_TANNE                                      # fern: eine Spalte alle drei Bilder
        ferne_tanne(bild, (wx - f // 3) % 85 - 8, hoehe)
        for wx, hoehe in TANNEN:                                     # nah: eine Spalte je Bild
            tanne(bild, (wx - f) % 255 - 8, hoehe)
        bild.rechteck(0, FUSS + 1, B, 1, KANTE)                      # die Spur
        bild.rechteck(0, FUSS + 2, B, 1, BODEN)
        bild.figur(SCHLITTEN_X, FUSS - 8, SCHLITTEN, SCHLITTEN_FARBEN)
        for dx, dy, hell in STAUB[f % 3]:
            bild.rechteck(SCHLITTEN_X + dx - 1, FUSS + dy, 2, 1, dimmen(WEISS, hell))
        schritt = f * SCHRITTE // 255 % 4
        for n in range(4):                                           # vier gleiche Hunde im Gleichschritt
            x = HUND_X + n * ABSTAND
            bild.figur(x, FUSS - 6, HUND + BEINE[schritt], HUND_FARBEN)
            bild.setze(x + RUTE[schritt], FUSS - 6, WEISS)
        liste.append(bild)
    return liste
