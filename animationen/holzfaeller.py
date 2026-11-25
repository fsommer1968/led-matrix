"""Holzfäller und Flößer: verschneiter Schwarzwaldhang mit dunklen Tannen, davor der Fluss. Der
Holzfäller in roter karierter Jacke schlägt im Takt an eine Tanne, Späne fliegen, Schnee rieselt von
den Zweigen, die Tanne neigt sich und fällt, Schnee stiebt auf. Der Stamm rutscht den Hang hinunter
in den Fluss, der Flößer bindet ihn ans Floß und stakt mit der langen Stange flussabwärts aus dem
Bild. Am Stumpf wächst eine junge Tanne nach, das nächste Floß treibt heran – 255 Bilder, die Runde
geht ohne Sprung in sich über.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum drei gleich geformte Tannen auf derselben Höhe (die
zweite und die nachgewachsene dritte sind Kopien der ersten), ein Hang in vier Stufen, Floß und
Stamm ohne Lücken, die Männer drei Spalten breit mit zwei gleichen, die Axt in Ruhe in einer Spalte,
Mondsichel statt Vollmond, zwei Sterne, zwei Wellen. Der Flößer auf dem nächsten Floß sitzt, damit
er vor dem Hang nichts verdeckt.
"""
import math
import random

from basis import B, HAUT, NACHTBLAU, ROT, Bild, dimmen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "holzfaeller"
TITEL = "Holzfäller und Flößer im Schwarzwald"

STERN = (255, 240, 200)
STERNE = [(30, 2, 0, 51), (50, 1, 20, 85)]                           # x, y, Phase, Periode (teilt 255)
SICHEL = ["XX.", ".XX", ".XX", ".XX", "XX."]                         # Mondsichel, drei Spalten
MOND = (240, 230, 170)
KANTE = (215, 225, 250)                        # Oberkante des Schnees
HANG = (78, 90, 140)                           # darunter gedämpft (große Fläche)
WASSER = (0, 40, 125)
WELLE = (40, 120, 230)
TANNE = (0, 105, 40)
STAMM = (33, 19, 8)
HOLZ = (66, 36, 10)
HOLZ_UNTEN = (41, 21, 5)
HOLZ_HELL = (82, 65, 35)                    # frischer Schnitt, Späne
MUETZE = (255, 170, 0)
KARO = (140, 0, 0)
HOSE = (41, 27, 15)
AUGE = (50, 25, 10)
STIEL = (66, 49, 26)
KLINGE = (200, 210, 230)
HUT = (240, 230, 170)
KITTEL = (0, 120, 255)
STANGE = (66, 55, 34)
SEIL = (255, 210, 0)

TANNEN_LINKS, TANNE_X = (2, 7), 21             # zwei Tannen bleiben stehen, die dritte wird gefällt
FAELLER_X = 11                                 # linke Spalte der Holzfäller-Figur
KUPPE = 23                                     # bis hierhin ist der Hang oben eben
FUSS = 8                                       # unterste Zeile über dem Schnee der Kuppe
UFER = 36                                      # ab hier nur noch Wasser
FLOSS_X, FLOSS_B, STAMM_B = 47, 14, 10         # Liegeplatz des Floßes, Länge von Floß und Stamm

# Ablauf
TAKT, SCHLAEGE = 13, 5                         # ein Schlag dauert 13 Bilder, Treffer im 7. Bild
NEIGT, FAELLT, LIEGT = 65, 72, 86              # Tanne neigt sich, fällt, liegt (Schnee stiebt auf)
STAMM_DA, RUTSCHT, IM_WASSER = 88, 94, 122     # der Stamm liegt, rutscht, schwimmt
BINDET, ZURUECK, ABFAHRT = 130, 142, 150       # Flößer kniet am Floßende und bindet, geht zurück, stakt los
WINKT_VON, WINKT_BIS = 154, 190                # der Holzfäller winkt dem Floß nach
SPROSS, WACHSEN = 146, 9                       # junge Tanne: alle neun Bilder eine Zeile höher
ANKUNFT = 250                                  # das nächste Floß liegt am Platz
GREIFT = 251                                   # der Holzfäller hebt die Axt wieder

# Holzfäller (Blick nach rechts), zehn Spalten, Zeilen 0 bis 8: m Mütze, j/d Karo, k Klinge, w Stiel
HOLT_AUS = ["kkwwww....", "k.mmmj....", "..mmmj....", "..hha.....", "..jjd.....", "..ddj.....",
            "..jjd.....", "..bbb.....", "..bbb....."]
SCHWUNG = ["..........", "..mmm..kk.", "..mmm.wk..", "..hhaw....", "..jjdj....", "..ddj.....",
           "..jjd.....", "..bbb.....", "..bbb....."]
SCHLAG = ["..........", "..mmm.....", "..mmm.....", "..hha.....", "..jjd.....", "..ddj....k",
          "..jjdjwwwk", "..bbb.....", "..bbb....."]
RUHT = ["..........", "..mmm.....", "..mmm.....", "..hha.....", "..jjd.....", "..ddjj....",
        "..jjdw....", "..bbbk....", "..bbbk...."]                    # Axt steht neben dem Bein
WINKT = [RUHT[:1] + ["..mmm.j...", "..mmmj...."] + RUHT[3:],
         RUHT[:1] + ["..mmm.....", "..mmmjj..."] + RUHT[3:]]
FAELLER = {"m": MUETZE, "h": HAUT, "a": AUGE, "j": ROT, "d": KARO, "b": HOSE, "w": STIEL, "k": KLINGE}
FOLGE = [HOLT_AUS] * 5 + [SCHWUNG] + [SCHLAG] * 4 + [SCHWUNG] + [HOLT_AUS] * 2

# Flößer (Blick nach rechts), fünf Spalten mit Hutkrempe
STEHT = [".ggg.", "ggggg", ".hha.", ".fff.", ".fff.", ".bbb.", ".bbb."]
GEHT = STEHT[:6] + [".b.b."]
SITZT = [".ggg.", "ggggg", ".hha.", ".fff."]
FLOESSER = {"g": HUT, "h": HAUT, "a": AUGE, "f": KITTEL, "b": HOSE}

# Tanne: (Spalte neben der Mitte, Höhe über dem Fuß); Schnee auf Astenden und Spitze
SCHNEE_ORTE = [(-2, 4), (2, 4), (-1, 6), (1, 6), (0, 8)]
HALB = {3: 2, 4: 2, 5: 1, 6: 1, 7: 0, 8: 0}    # Höhe → halbe Breite der Krone
# Wege, auf denen der Schnee nach einem Schlag herunterrieselt (Spalte neben der Mitte, Zeile)
RIESELN = [[(-2, 5), (-3, 6), (-3, 7), (-3, 8)], [(2, 5), (3, 6), (3, 7), (3, 8)],
           [(-2, 3), (-3, 4), (-3, 6), (-3, 8)], [(2, 3), (3, 4), (3, 6), (3, 8)],
           [(1, 1), (2, 2), (3, 4), (3, 6)]]
SPAENE = [[(-1, 5), (-2, 4), (-3, 4), (-4, 5)], [(-1, 6), (-2, 5), (-3, 5), (-3, 7)]]


def hang_y(x):
    """Oberkante des Schnees: links die Kuppe, dann alle drei Spalten eine Stufe hinunter zum Fluss."""
    if x <= KUPPE:
        return FUSS + 1
    if x < UFER:
        return FUSS + 2 + (x - KUPPE - 1) // 3
    return 14                                                        # Wasser


def tanne(bild, mitte, fuss, schnee=(0, 1, 2, 3, 4), winkel=0.0, ruck=0, kerbe=False):
    """Tanne mit drei Zeilen Stamm und sechs Zeilen Krone; winkel dreht sie um den Fuß nach rechts,
    dabei hebt sich der Fuß um zwei Zeilen, damit sie am Ende auf dem Schnee liegt. Was unter dem
    Schnee läge, bleibt weg (so wächst auch die junge Tanne aus dem Boden)."""
    zellen = {(0, h): STAMM for h in range(3)}
    if kerbe:
        zellen[(0, 2)] = HOLZ_HELL
    for h, halb in HALB.items():
        for dx in range(-halb, halb + 1):
            zellen[(dx + ruck, h)] = TANNE
    for i in schnee:
        dx, h = SCHNEE_ORTE[i]
        zellen[(dx + ruck, h)] = KANTE
    c, s = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))
    fuss -= round(2 * min(1.0, winkel / 90))
    for y in range(16):
        for x in range(mitte - 4, mitte + 13):
            if 0 <= x < B and y < hang_y(x):
                u, v = x - mitte, fuss - y
                farbe = zellen.get((round(u * c - v * s), round(u * s + v * c)))
                if farbe:
                    bild.setze(x, y, farbe)


def stamm(bild, x0, laenge=STAMM_B):
    """Stamm, zwei Zeilen dick: liegt auf dem Hang auf, ab dem Ufer schwimmt er."""
    for x in range(x0, x0 + laenge):
        unten = hang_y(x) if x < UFER else 15
        bild.setze(x, unten - 2, HOLZ_HELL if x == x0 else HOLZ)
        bild.setze(x, unten - 1, HOLZ_UNTEN)


def floss(bild, x0, laenge=FLOSS_B):
    bild.rechteck(x0, 13, laenge, 1, HOLZ)
    bild.rechteck(x0, 14, laenge, 1, HOLZ_UNTEN)


def weg(t):
    """Weich anfahren: Strecke nach t Bildern bei 0,75 Spalten je Bild."""
    return 0.75 * t * t / (t + 8) if t > 0 else 0


def bilder():
    z = random.Random(11)
    wolke = [(TANNE_X + 1 + z.randrange(12), z.uniform(0.6, 1.3), z.randrange(3)) for _ in range(14)]
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        bild.figur(39, 1, SICHEL, {"X": MOND})
        for x in TANNEN_LINKS:
            tanne(bild, x, FUSS)
        for x in range(B):                                           # Hang und Fluss
            y0 = hang_y(x)
            if x < UFER:
                bild.setze(x, y0, KANTE)
                for y in range(y0 + 1, 14):
                    bild.setze(x, y, HANG)
            bild.setze(x, 14, WASSER)
            bild.setze(x, 15, WASSER)
        bild.rechteck(UFER, 13, B - UFER, 1, HANG)                   # anderes Ufer
        for k in range(2):                                           # Wellen ziehen flussabwärts
            x = (k * 32 + f * 64 // 255) % 64
            bild.setze(x, 15, WELLE)
            bild.setze((x + 1) % 64, 15, WELLE)

        # die Tanne, die gefällt wird
        schlag, c = f // TAKT, f % TAKT
        if f < NEIGT:
            treffer = schlag + (1 if c >= 6 else 0)                  # so viele Schläge sitzen schon
            tanne(bild, TANNE_X, FUSS, schnee=range(min(treffer, 5), 5) if treffer < 5 else (),
                  ruck=1 if c in (6, 7) else 0, kerbe=treffer > 0)
            if 6 <= c < 10:                                          # Späne fliegen
                for bahn in SPAENE:
                    dx, y = bahn[c - 6]
                    bild.setze(TANNE_X + dx, y, HOLZ_HELL)
            if 6 <= c < 6 + 2 * 4:                                   # Schnee rieselt von den Zweigen
                k = (c - 6) // 2
                for dx, y in RIESELN[schlag][max(0, k - 1):k + 1]:
                    bild.setze(TANNE_X + dx, y, KANTE)
        elif f < STAMM_DA:
            if f < FAELLT:
                winkel = f - NEIGT + 1.0
            else:
                winkel = 7 + 111 * min(1.0, (f - FAELLT + 1) / (LIEGT - FAELLT)) ** 2
            tanne(bild, TANNE_X, FUSS, schnee=(), winkel=winkel, kerbe=True)
        if LIEGT - 1 <= f < SPROSS:
            bild.setze(TANNE_X, FUSS, HOLZ_HELL)                     # Stumpf
        if f >= SPROSS:                                              # junge Tanne wächst nach
            groesse = min(9, 1 + (f - SPROSS) // WACHSEN)
            tanne(bild, TANNE_X, FUSS + 9 - groesse)

        # Stamm: liegt, rutscht, schwimmt, hängt am Floß
        floss_x = FLOSS_X + round(weg(f - ABFAHRT))
        if f >= STAMM_DA:
            t = min(1.0, max(0.0, (f - RUTSCHT) / (IM_WASSER - RUTSCHT)))
            x0 = TANNE_X + 2 + round((FLOSS_X - STAMM_B - TANNE_X - 2) * t ** 1.6)
            x0 += floss_x - FLOSS_X
            stamm(bild, x0)
            if RUTSCHT + 4 < f < IM_WASSER and x0 <= UFER:           # Schnee stäubt hinter dem Stamm
                bild.setze(x0 - 1, hang_y(x0 - 1) - 1 - f % 2, KANTE)
            if f < IM_WASSER and 0 <= x0 + STAMM_B - UFER < 6:       # es spritzt
                for k in range(2):
                    bild.setze(x0 + STAMM_B + k * 2, 12 - (f + k) % 2, WELLE)
            if f >= BINDET + 4:
                bild.setze(floss_x - 1, 13, SEIL)

        # Floß mit Flößer: wartet, bindet den Stamm an, stakt davon
        floss(bild, floss_x)
        if f < ABFAHRT:
            bild.linie(floss_x + 11, 4, floss_x + 11, 14, STANGE)    # Stange steckt im Grund
            if f < IM_WASSER:
                bild.figur(floss_x + 6, 6, STEHT, FLOESSER)
            elif f < BINDET:                                         # geht ans Floßende
                x = floss_x + 6 - round(6 * (f - IM_WASSER + 1) / (BINDET - IM_WASSER))
                bild.figur(x, 6, GEHT if f % 4 < 2 else STEHT, FLOESSER, spiegeln=True)
            elif f < ZURUECK:                                        # kniet und bindet
                bild.figur(floss_x, 9, SITZT, FLOESSER, spiegeln=True)
                if (f // 3) % 2:
                    bild.setze(floss_x, 12, KITTEL)
            else:
                x = floss_x + round(6 * (f - ZURUECK + 1) / (ABFAHRT - ZURUECK))
                bild.figur(x, 6, GEHT if f % 4 < 2 else STEHT, FLOESSER)
        else:
            if ((f - ABFAHRT) // 7) % 2 == 0:                        # stößt sich ab …
                bild.linie(floss_x + 11, 5, floss_x + 14, 14, STANGE)
            else:                                                    # … und setzt die Stange neu
                bild.linie(floss_x + 11, 2, floss_x + 11, 11, STANGE)
            bild.figur(floss_x + 6, 6, STEHT, FLOESSER)
        # das nächste Floß treibt von links heran, der Flößer sitzt und steht am Liegeplatz auf
        if f > ABFAHRT:
            neu_x = FLOSS_X - round(weg(ANKUNFT - f))
            floss(bild, neu_x)
            if f < ANKUNFT - 2:
                bild.figur(neu_x + 6, 9, SITZT, FLOESSER)
                bild.linie(neu_x + 11, 7, neu_x + 11, 12, STANGE)
            else:
                bild.figur(neu_x + 6, 6, STEHT, FLOESSER)
                bild.linie(neu_x + 11, 4, neu_x + 11, 14, STANGE)

        # Schnee stiebt auf, wo die Tanne aufschlägt
        if LIEGT - 1 <= f < LIEGT + 10:
            t = f - LIEGT + 1
            for x, tempo, spaet in wolke:
                if t >= spaet:
                    y = hang_y(x) - 1 - (t - spaet) * tempo + 0.08 * (t - spaet) ** 2
                    if y < hang_y(x):
                        bild.setze(x + (t - spaet) // 4, y, dimmen(KANTE, min(1.0, 1.6 - t * 0.12)))

        # Holzfäller
        if f < SCHLAEGE * TAKT - 2:
            pose = FOLGE[c]
        elif WINKT_VON <= f < WINKT_BIS:
            pose = WINKT[(f // 5) % 2]
        elif f >= GREIFT:
            pose = SCHWUNG
        else:
            pose = RUHT
        # tritt zwei Schritte zurück, wenn die Tanne sich neigt, und wieder vor, wenn die junge steht
        abstand = 0 if f <= NEIGT else 1 if f < NEIGT + 4 else 2 if f < 243 else 1 if f < 247 else 0
        bild.figur(FAELLER_X - abstand, 0, pose, FAELLER)
        liste.append(bild)
    return liste
