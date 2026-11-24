"""Nussknacker: Ein Nussknacker aus dem Erzgebirge (hohe blaue Mütze, rote Uniform, weißer Bart)
steht auf dem Tisch, daneben ein Häufchen Walnüsse. Dreimal hüpft eine Nuss vom Haufen über den
Tisch in seinen Mund: Der Hebel hinten geht hoch, der Unterkiefer klappt auf, die Nuss landet,
der Hebel fährt herunter, der Kiefer schnappt zu, die Schale springt in Stücken weg und der Kern
fällt neben ihn auf den Tisch. Nach jeder Nuss zwinkert er. Zum Schluss wischt eine Hand (roter
Ärmel, weißer Rand) die drei Kerne zusammen und nimmt sie mit, und aus dem Säckchen rechts springen
drei neue Nüsse auf den Haufen – die Runde geht ohne Sprung in sich über. Kein Text – 255 Bilder.

Je Nuss 60 Bilder (0, 60, 120), darin:
4–7     Hebel hoch, Kiefer auf
8–35    die Nuss hüpft vom Haufen auf den Tisch und von dort in den Mund
36–40   sie liegt im Mund
41–42   Hebel herunter, Kiefer zu (er kneift die Augen zu): knack
42–57   Schalenstücke fliegen, der Kern fällt auf seinen Platz
50–54   er zwinkert
180–203 die Hand kommt von oben, wischt die Kerne zusammen und hebt sie weg
209–246 drei neue Nüsse springen aus dem Säckchen auf den Haufen

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum Wand und Tisch als waagerechte Bänder (alle Spalten gleich), der
Nussknacker von vorn und spiegelgleich (linke und rechte Hälfte haben gleiche Spalten), alle
Nüsse gleich geformt, der Arm aus gleichen Spalten, das Säckchen bis auf den Flicken spiegelgleich;
nichts flackert (keine Kerze, kein Schnee). Eine Kerze passte nicht mehr unter die 76000 Bytes.
"""
from basis import GELB, HAUT, ROT, WEISS, Bild

NAME = "nussknacker"
TITEL = "Nussknacker knackt Nüsse"

WAND = (0, 26, 16)                             # dunkle Wand (große Fläche)
TISCH_KANTE = (150, 85, 30)                    # Tischplatte: helle Kante …
TISCH = (80, 42, 12)                           # … und gedämpfte Front
MUETZE = (20, 70, 255)
GOLD = (255, 170, 0)
BART = (170, 180, 215)                         # Haar und Bart, etwas dunkler als die Zähne
AUGE = (0, 0, 0)
NASE = (255, 95, 60)
SCHNURRBART = (40, 20, 10)
RACHEN = (55, 0, 5)
SOCKEL = (0, 140, 50)
HEBEL = (210, 130, 30)
NUSS = (200, 120, 40)
NUSS_DUNKEL = (140, 78, 22)                   # Ecken der Nuss: wirkt rund
KERN = (250, 220, 150)
AERMEL = (200, 0, 20)                          # roter Ärmel mit weißem Rand
SACK = (160, 120, 65)                          # Jute, gedämpft
SACK_RAND = (220, 180, 110)                    # umgekrempelter Rand
FLICKEN = (200, 0, 20)                         # roter Flicken

# Nussknacker von vorn, 9 breit, 16 hoch (Mund zu); b Mütze, g Gold, w Bart, h Haut, a Auge,
# n Nase, m Schnurrbart, t Zähne, r Uniform, p Hose, s Sockel
FIGUR = ["..bbbbb..", "..bbgbb..", "..bbbbb..", ".ggggggg.", ".whahahw.", ".whahahw.", ".wmmnmmw.",
         ".wtttttw.", ".wwwwwww.", "grrwwwrrg", "rrrrgrrrr", "rrrrgrrrr", "h.pp.pp.h", "..pp.pp..",
         "sssssssss", "sssssssss"]
FARBEN = {"b": MUETZE, "g": GOLD, "w": BART, "h": HAUT, "a": AUGE, "n": NASE, "m": SCHNURRBART,
          "t": WEISS, "r": ROT, "p": MUETZE, "s": SOCKEL, "N": NUSS, "d": NUSS_DUNKEL, "k": KERN,
          "A": AERMEL, "S": SACK, "L": SACK_RAND, "W": WEISS, "F": FLICKEN}
NUSS_BILD = ["dNd", "NNN", "dNd"]
KERN_BILD = [".k.", "kkk"]
HAND = ["WWWW", "hhhh", "hhhh", ".hh."]         # Hand von oben, darüber der Ärmel
# offenes, bauchiges Säckchen voller Nüsse, 9 breit, steht auf dem Tisch (Zeilen 6 bis 13)
SACK_BILD = ["..dNdNd..", ".LLLLLLL.", "..SSSSS..", ".SSSSSSS.", "SSSSSFFSS", "SSSSSFFSS", "SSSSSSSSS",
             ".SSSSSSS."]
SACK_X = 55

X0 = 9                                         # linke Spalte des Nussknackers
MUND_X, MUND_Y = X0 + 3, 7                     # Nuss im Mund (linke obere Ecke)
HAUFEN_X = 43                                  # linke Spalte des Haufens
# Nüsse im Haufen (linke obere Ecke): unten drei, darauf zwei, oben eine
HAUFEN = [(0, 11), (4, 11), (8, 11), (2, 9), (6, 9), (4, 7)]
REIHENFOLGE = [5, 4, 3]                        # diese Nüsse werden geknackt (oben zuerst)
NACHFUELLEN = [3, 4, 5]                        # so kommen sie wieder
KERN_X = [30, 26, 22]                          # Plätze der Kerne (der erste am weitesten weg)
AUFSETZER_X = 37                               # hier setzt die Nuss auf dem Tisch auf

Z = 60                                         # Bilder je Nuss
T_AUF, T_AB, T_TISCH, T_MUND, T_DRUCK, T_KNACK = 4, 8, 20, 36, 41, 42
KERN_DAUER = 10
HAND_AB, HAND_UNTEN, HAND_LINKS, HAND_WEG = 180, 187, 198, 206
HAND_X0, HAND_X1 = 31, 21
HUPF = [(209, 221), (222, 234), (235, 247)]    # je Nuss: springt aus dem Säckchen, liegt auf dem Haufen
# Schalenstücke: Tempo x, y und Breite
SPLITTER = [(-1.3, -1.5, 2), (1.1, -1.7, 2), (2.0, -0.9, 2), (-0.5, -2.0, 2), (0.5, -2.2, 1), (-2.0, -0.8, 1)]


def kiefer(t):
    """Öffnung des Mundes in Zeilen (0 zu, 2 offen) und Stellung des Hebels (0 unten, 2 oben)."""
    if t < T_AUF or t >= T_KNACK:
        return 0, 0
    if t < T_AUF + 2 or t == T_DRUCK:
        return 1, 1
    return 2, 2


def nussknacker(bild, auf, hebel, augen):
    """auf: Mundöffnung in Zeilen; hebel 0 unten, 1 waagerecht, 2 oben; augen 0 offen,
    1 zwinkert (rechtes Auge zu), 2 beide zugekniffen."""
    bild.figur(X0, 0, FIGUR, FARBEN)
    if auf:                                                          # Unterkiefer klappt herunter
        bild.rechteck(X0 + 2, 7, 5, auf, RACHEN)
        bild.rechteck(X0 + 2, 7 + auf, 5, 1, WEISS)                  # Zähne
        bild.rechteck(X0 + 2, 8 + auf, 5, 1, BART)                   # Kinn mit Bartspitze
        bild.rechteck(X0 + 3, 9 + auf, 3, 1, BART)
    if augen:                                                        # zu: aus dem Balken wird ein Strich
        bild.setze(X0 + 5, 4, HAUT)
        bild.setze(X0 + 6, 5, AUGE)
    if augen == 2:
        bild.setze(X0 + 3, 4, HAUT)
        bild.setze(X0 + 2, 5, AUGE)
    for k in range(1, 5):                                            # Hebel hinten, zwei Zeilen dick
        y = 8 + k * (1 - hebel)
        bild.setze(X0 - k, y, HEBEL)
        bild.setze(X0 - k, y + 1, HEBEL)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(WAND)
        bild.rechteck(0, 14, 64, 1, TISCH_KANTE)
        bild.rechteck(0, 15, 64, 1, TISCH)
        runde, t = (f // Z, f % Z) if f < 3 * Z else (3, 0)
        auf, hebel = kiefer(t) if runde < 3 else (0, 0)
        augen = 1 if (runde < 3 and 50 <= t < 55) or 249 <= f < 253 else 0
        if runde < 3 and T_DRUCK <= t < T_KNACK + 2:                 # beim Knacken kneift er die Augen zu
            augen = 2

        # Haufen: was schon unterwegs war, fehlt, bis das Säckchen nachfüllt
        da = set(range(6))
        for k, nr in enumerate(REIHENFOLGE):
            if f >= k * Z + T_AB:
                da.discard(nr)
        for nr, (_, liegt) in zip(NACHFUELLEN, HUPF):
            if f >= liegt:
                da.add(nr)
        for nr in sorted(da):
            bild.figur(HAUFEN_X + HAUFEN[nr][0], HAUFEN[nr][1], NUSS_BILD, FARBEN)

        # Kerne auf dem Tisch, bis die Hand sie holt
        hand_x = HAND_X0 if f < HAND_UNTEN else max(HAND_X1, HAND_X0 - (f - HAND_UNTEN))
        for k, x in enumerate(KERN_X):
            if f >= k * Z + T_KNACK + KERN_DAUER and not (f >= HAND_UNTEN and hand_x <= x + 1):
                bild.figur(x, 12, KERN_BILD, FARBEN)

        # die Schale springt in Stücken weg (hinter dem Kopf hervor, das Gesicht bleibt frei)
        if runde < 3 and T_KNACK < t < T_KNACK + 16:
            u = t - T_KNACK
            for vx, vy, breit in SPLITTER:
                x = MUND_X + 1 + vx * u
                y = 7 + vy * u + 0.18 * u * u
                if y < 13:
                    bild.rechteck(round(x), round(y), breit, 1, NUSS)

        nussknacker(bild, auf, hebel, augen)

        if runde < 3:
            sx, sy = HAUFEN[REIHENFOLGE[runde]]
            sx += HAUFEN_X
            if T_AB <= t < T_TISCH:                                  # erster Hüpfer: vom Haufen auf den Tisch
                u = (t - T_AB) / (T_TISCH - T_AB)
                x = sx + (AUFSETZER_X - sx) * u
                y = sy + (11 - sy) * u - 3 * 4 * u * (1 - u)
                bild.figur(round(x), round(y), NUSS_BILD, FARBEN)
            elif T_TISCH <= t < T_MUND:                              # zweiter Hüpfer: in den Mund
                u = (t - T_TISCH) / (T_MUND - T_TISCH)
                x = AUFSETZER_X + (MUND_X - AUFSETZER_X) * u
                y = 11 + (MUND_Y - 11) * u - 4 * 4 * u * (1 - u)
                bild.figur(round(x), round(y), NUSS_BILD, FARBEN)
            elif T_MUND <= t < T_DRUCK:                              # liegt im Mund
                bild.figur(MUND_X, MUND_Y, ["NNN", "dNd"], FARBEN)
            elif t == T_DRUCK:
                bild.rechteck(MUND_X, MUND_Y, 3, 1, NUSS)
            if t == T_KNACK:                                         # knack: es blitzt zwischen den Zähnen
                bild.rechteck(X0 + 2, 7, 5, 1, GELB)
            if T_KNACK < t < T_KNACK + KERN_DAUER:                   # Kern fällt auf seinen Platz
                u = (t - T_KNACK) / KERN_DAUER
                x = MUND_X + (KERN_X[runde] - MUND_X) * u
                y = 7 + 5 * u - 3 * 4 * u * (1 - u)
                bild.figur(round(x), round(y), KERN_BILD, FARBEN)

        # Hand wischt die Kerne zusammen
        if HAND_AB <= f < HAND_WEG:
            if f < HAND_UNTEN:
                unten = -1 + (f - HAND_AB + 1) * 2                   # unterste Zeile der Hand
            elif f < HAND_LINKS:
                unten = 13
            else:
                unten = 13 - (f - HAND_LINKS + 1) * 2
            bild.rechteck(hand_x, 0, 4, max(0, unten - 3), AERMEL)
            bild.figur(hand_x, unten - 3, HAND, FARBEN)

        # Säckchen: drei neue Nüsse springen heraus und auf den Haufen
        bild.figur(SACK_X, 6, SACK_BILD, FARBEN)
        for nr, (los, liegt) in zip(NACHFUELLEN, HUPF):
            if los <= f < liegt:
                u = (f - los) / (liegt - los)
                zx, zy = HAUFEN_X + HAUFEN[nr][0], HAUFEN[nr][1]
                x = SACK_X + 3 + (zx - SACK_X - 3) * u
                y = 5 + (zy - 5) * u - 4 * 4 * u * (1 - u)
                bild.figur(round(x), round(y), NUSS_BILD, FARBEN)
        liste.append(bild)
    return liste
