"""Wasserfall im Winter: In einer verschneiten Felsschlucht stürzt ein Schwarzwald-Wasserfall über
drei Felsstufen in die Tiefe, schäumt und spritzt unten im Becken und fließt als Bach nach rechts
ab; links und rechts stehen dunkle Tannen. In der Nacht funkeln zwei Sterne, an der Felskante
wachsen Eiszapfen langsam länger, und der Rand des Falls gefriert zu einem Eisvorhang. Dann färbt
das Morgenrot den Himmel, die Sonne schaut über die Felskante, das Eis glitzert, es tropft, die
Zapfen tauen zurück, und der Vorhang wird wieder Wasser. Auf einem verschneiten Stein am Bach
knickst und hüpft eine Wasseramsel – 255 Bilder, die Runde geht ohne Sprung in sich über.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum einfarbige Felsflächen und je Stufe nur zwei
Spaltenmuster im Wechsel (heller Streifen, ruhiges Wasser; alle weiteren Spalten sind Kopien) –
die Streifen einer Stufe laufen deshalb im Gleichtakt, versetzte kosten allein an der unteren
Stufe 2,4 KB mehr. Die Kanten der Felsstufen liegen genau an den Kanten des Falls, Sterne, Sonne
und Amsel stehen über Spalten, die ohnehin eigen sind, und die rechte Tanne steht auf einem
Schneehügel wie die linke (sie ist dann eine Kopie; der Bach verschwindet dahinter). Alle Takte
teilen 255.
"""
from basis import B, GELB, NACHTBLAU, WEISS, Bild, dimmen, mischen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "wasserfall"
TITEL = "Wasserfall im Winter"

FELS = (34, 38, 58)                            # Felswand hinten, gedämpft (große Fläche)
STUFE = (60, 64, 92)                           # Felsstufen und Stein davor, etwas heller
KANTE = (215, 225, 250)                        # Schnee auf den Kanten
BODEN = (105, 118, 165)                        # Schneeufer darunter, gedämpft
WASSER = (20, 100, 255)
STREIF = (190, 230, 255)                       # fallende helle Streifen
SCHAUM = (150, 205, 255)
BACH = (10, 70, 210)
GLANZ = (110, 180, 255)
EIS = (90, 220, 255)
TANNE = (0, 105, 40)
STAMM = (33, 19, 8)
AMSEL = (41, 21, 9)
BEIN = (210, 115, 20)
MORGEN_OBEN, MORGEN_UNTEN = (60, 18, 64), (180, 72, 40)              # Morgenrot: obere und untere Himmelszeile

OBEN = 2                                       # Zeile der obersten Schneekante
UFER = 14                                      # ab hier Schneeufer, Becken und Bach
STUFEN = [(20, 4, 2, 3), (26, 5, 5, 4), (33, 7, 9, 5)]               # x, Breite, Zeile der Kante, Fallhöhe
BECKEN_X, BACH_ENDE = 33, 52                   # unten Wasser von … bis; rechts davor ein Schneehügel
TAKT = 5                                       # Streifenabstand im Fall (teilt 255)
BACH_TAKT = 17                                 # Abstand der Glanzlichter im Bach (teilt 85)
ABSATZ = (14, 19)                              # Schnee auf der ersten Felsstufe, links vom Fall
STEIN = (44, 48, 11)                           # verschneiter Stein am Bach: von, bis, Zeile der Schneehaube
ZAPFEN = [(11, 3, 0), (13, 2, 30), (42, 3, 20), (46, 4, 0), (50, 3, 40)]         # x, größte Länge, wächst ab Bild
EISRAND = [(39, 2, 50), (38, 2, 80)]                                 # Eisvorhang: x, Stufe, gefriert ab Bild
TANNEN = (5, 58)
STERN = (255, 240, 200)
STERNE = [(13, 0, 51), (42, 30, 85)]           # x, Phase, Periode (teilt 255); über Eiszapfen
SONNE_X = 46                                   # die Morgensonne geht über dem Stein auf

# Wasseramsel (Blick nach links): d dunkelbraun, w weiße Brust, b Bein
AMSEL_STEHT = ["dd..", "wddd", ".b.."]
AMSEL_KNICKS = ["....", "dd.d", "wdd."]
AMSEL_FARBEN = {"d": AMSEL, "w": WEISS, "b": BEIN}
KNICKSE = (18, 22, 70, 74, 131, 135, 178, 182, 236, 240)             # hier duckt sie sich zwei Bilder lang
HUEPFER = (100, 208)                           # hier hüpft sie und dreht sich um


def rampe(f, von, bis):
    """0 vor »von«, 1 nach »bis«, dazwischen gleichmäßig."""
    return min(1.0, max(0.0, (f - von) / (bis - von)))


def tanne(bild, x):
    """Tanne im Vordergrund: gestuftes Dreieck, Schneespitze, Stamm."""
    for k in range(11):
        halb = min(4, (k + 1) // 2)
        bild.rechteck(x - halb, 2 + k, 2 * halb + 1, 1, TANNE)
    bild.setze(x, 1, KANTE)
    bild.setze(x, 13, STAMM)


def zapfen_laenge(f, lang, ab):
    """Wächst in der Nacht von 1 auf »lang« und taut am Morgen zurück."""
    return 1 + round((lang - 1) * (rampe(f, ab, ab + 90) - rampe(f, 196 + ab // 4, 240 + ab // 4)))


def eisrand(f, ab, hoehe):
    """Zeilen (von, bis) der Randspalte, die gefroren sind: friert von oben her zu, taut von oben her auf."""
    return round(hoehe * rampe(f, 204 + ab // 6, 228 + ab // 6)), round(hoehe * rampe(f, ab, ab + 24))


def bilder():
    liste = []
    for f in range(255):
        rot = round(8 * (rampe(f, 118, 158) - rampe(f, 204, 244))) / 8           # Morgenrot kommt und geht
        bild = Bild(mischen(NACHTBLAU, MORGEN_OBEN, rot))
        bild.rechteck(0, 1, B, 1, mischen(NACHTBLAU, MORGEN_UNTEN, rot))
        if rot < 0.3:                                                # nachts zwei Sterne, funkeln langsam
            for x, phase, periode in STERNE:
                bild.setze(x, 0, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        if 140 <= f < 226:                                           # die Sonne schaut über die Felskante
            ganz = 152 <= f < 214
            sonne = mischen(MORGEN_UNTEN, GELB, min(4, f - 139, 226 - f) / 4)
            bild.rechteck(SONNE_X - 1 - ganz, 1, 3 + 2 * ganz, 1, sonne)
            if ganz:
                bild.rechteck(SONNE_X - 1, 0, 3, 1, sonne)
        bild.rechteck(0, OBEN, B, 1, KANTE)                          # Felswand mit Schneekante
        bild.rechteck(0, OBEN + 1, B, UFER - OBEN - 1, FELS)
        bild.rechteck(0, UFER, B, 1, KANTE)                          # Schneeufer
        bild.rechteck(0, UFER + 1, B, 1, BODEN)
        bild.rechteck(BECKEN_X, UFER, BACH_ENDE - BECKEN_X + 1, 2, BACH)         # Becken und Bach
        # Felsstufen vor der Wand: jede reicht bis unter die Kante des nächsten Falls
        for (_, _, y0, _), von, bis in ((STUFEN[1], ABSATZ[0], STUFEN[1][0]), (STUFEN[2], STUFEN[1][0], STUFEN[2][0])):
            bild.rechteck(von, y0 + 1, bis - von, UFER - y0 - 1, STUFE)
        bild.rechteck(ABSATZ[0], STUFEN[1][2], ABSATZ[1] - ABSATZ[0] + 1, 1, KANTE)
        bild.rechteck(STEIN[0], STEIN[2] + 1, STEIN[1] - STEIN[0] + 1, UFER - STEIN[2] - 1, STUFE)
        bild.rechteck(STEIN[0], STEIN[2], STEIN[1] - STEIN[0] + 1, 1, KANTE)
        # der Fall: je Stufe nur zwei Spaltenmuster im Wechsel – helle Streifen mit Lücken, die ein
        # Pixel je Bild nach unten wandern, dazwischen ruhiges Wasser
        for i, (x0, breite, y0, fall) in enumerate(STUFEN):
            if i:                                                    # Wasser läuft über die Stufe zur Kante
                vx = STUFEN[i - 1][0]
                bild.rechteck(vx, y0, x0 - vx, 1, WASSER)
            for j in range(breite):
                for k in range(fall + 1):
                    hell = j % 2 == 0 and (f - k + i * 2) % TAKT < 3
                    if k < fall:
                        farbe = STREIF if hell else WASSER
                    else:                                            # unten schäumt es
                        farbe = WEISS if hell else SCHAUM
                    bild.setze(x0 + j, y0 + k, farbe)
        if f % TAKT < 2:                                             # Gischt spritzt am Becken auf, im Takt des Falls
            bild.setze(STUFEN[2][0] + STUFEN[2][1], UFER - 1 - f % TAKT, WEISS)
        # Eisvorhang am Rand des Falls
        for x, i, ab in EISRAND:
            von, bis = eisrand(f, ab, STUFEN[i][3])
            for k in range(von, bis):
                bild.setze(x, STUFEN[i][2] + k, EIS)
        # Bach: Glanzlichter ziehen nach rechts
        for x in range(BECKEN_X, BACH_ENDE + 1):
            lage = (x - f // 3) % BACH_TAKT
            if lage < 2 and x > STUFEN[2][0] + STUFEN[2][1]:
                bild.setze(x, UFER, GLANZ)
            elif 8 <= lage < 10:
                bild.setze(x, UFER + 1, GLANZ)
        # Eiszapfen wachsen in der Nacht und tauen am Morgen; beim Tauen fällt je ein Tropfen
        for x, lang, ab in ZAPFEN:
            n = zapfen_laenge(f, lang, ab)
            bild.rechteck(x, OBEN + 1, 1, n, EIS)
            grund = OBEN + 1 + n                                     # hier endet der freie Fels unter dem Zapfen
            while bild.hole(x, grund) == FELS:
                grund += 1
            for t in range(max(1, f - 12), f + 1):
                if zapfen_laenge(t, lang, ab) < zapfen_laenge(t - 1, lang, ab):
                    y = OBEN + 1 + zapfen_laenge(t, lang, ab) + (f - t)
                    if y < grund:
                        bild.setze(x, y, EIS)
        # Glitzern in der Morgensonne: zwei Stücke Eis blitzen weiß auf, alle zwei Bilder andere
        if 152 <= f < 214:
            eis = [(x, y) for x in range(B) for y in range(OBEN + 1, UFER) if bild.px[y][x] == EIS]
            for k in range(2 if eis else 0):
                bild.setze(*eis[(f // 2 * 7 + k * len(eis) // 2) % len(eis)], WEISS)
        for x in TANNEN:
            tanne(bild, x)
        # Wasseramsel auf dem Stein
        links = not HUEPFER[0] + 2 <= f < HUEPFER[1] + 2
        hoch = 0
        for h in HUEPFER:
            if 0 <= f - h < 5:
                hoch = (1, 2, 2, 1, 0)[f - h]
        figur = AMSEL_KNICKS if any(0 <= f - k < 2 for k in KNICKSE) else AMSEL_STEHT
        bild.figur(STEIN[0] + 1, STEIN[2] - 3 - hoch, figur, AMSEL_FARBEN, spiegeln=not links)
        liste.append(bild)
    return liste
