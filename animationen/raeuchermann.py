"""Räuchermännchen: eine gedrechselte Holzfigur aus dem Erzgebirge steht auf der Fensterbank – hoher
grüner Hut mit goldenem Band, weißer Bart, rote Jacke, runder Bauch, die Pfeife im Mundwinkel. Alle
fünf Sekunden glimmt die Räucherkerze im Bauch orange auf, der Pfeifenkopf glüht, der Mund geht auf,
und ein Rauchkringel steigt auf, der größer und blasser wird und nach rechts über die ganze Breite
wegzieht; immer drei sind unterwegs. Zweimal je Runde zwinkert das Männchen. Rechts steht ein
Gesteck: eine brennende Kerze in Tannenzweigen mit roten Beeren. Die Runde geht ohne Sprung in sich
über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum hat das Männchen paarweise gleiche Spalten (Arme zwei
breit, Sockel durchgehend) und einen spiegelgleichen Kopf – die Pfeife hängt am Bartrand, ein Stiel
quer durch den Bart kostet 10 Bytes je Bild mehr. Die Zweige wechseln nur zwischen zwei Höhen (ein
Zacken über vier Spalten kostet unter den Kringeln rund 2000 Bytes je Runde mehr), nur zwei Beeren
(jede rund 1000 Bytes je Runde), der Kerzenfuß ist so breit wie die Kerze. Die Kringel sind rund
mit gleichen Mittelspalten und einfarbig in sechs Grautönen (je Kringel 25 bis 40 Bytes je Bild).
"""
from basis import B, HAUT, NACHTBLAU, Bild

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "raeuchermann"
TITEL = "Räuchermännchen pafft Rauchkringel"

HUT = (0, 150, 50)
BAND = (255, 190, 30)
AUGE = (50, 25, 10)
NASE = (255, 90, 70)
LID = (181, 143, 121)                           # zugekniffenes Auge
BART = (235, 235, 245)
JACKE = (225, 15, 10)
ARM = (150, 0, 10)
HOSE = (30, 70, 200)
SOCKEL = (66, 36, 10)
PFEIFE = (49, 26, 8)
ASCHE = (70, 15, 0)                            # Räucherkerze im Bauch, wenn sie nicht glimmt
GLUT = [(140, 35, 0), (255, 90, 0), (255, 160, 20)]
BANK = (33, 18, 6)                            # Fensterbank (große Fläche, gedämpft)
ZWEIG = (0, 110, 40)
BEERE = (255, 30, 20)
KERZE = (215, 30, 20)
HALTER = (255, 190, 30)
FLAMME, FLAMME_FUSS = (255, 215, 60), (255, 120, 0)
RAUCH = [(235, 235, 245), (190, 190, 208), (150, 150, 172), (112, 112, 138), (78, 78, 105), (48, 48, 74)]

# Männchen, 11 Spalten breit: g Hut, y Band, s Haut, a/z Augen, n Nase, w Bart, o Mund, q Pfeifenstiel,
# p Pfeifenkopf, r Jacke, d Arm, h Hand, k Räucherkerze, b Hose, c Sockel
MANN = ["...ggggg...",
        "...ggggg...",
        "...yyyyy...",
        "..ggggggg..",
        "..ssaszss..",
        "..sssnsss..",
        "..wwwowwq..",
        "...wwwww.pp",
        "..rrrrrrr..",
        "ddrrrrrrrdd",
        "ddrrkkkrrdd",
        "ddrrkkkrrdd",
        "hhrrrrrrrhh",
        "..bbb.bbb..",
        "..bbb.bbb..",
        "ccccccccccc"]
X_MANN = 2

# Rauchkringel: Form und Grauton (Nummer in RAUCH) je Alter (ab diesem Bild)
R1 = ["#"]
R3 = [".#.", "#.#", ".#."]
R5 = [".###.", "#...#", "#...#", "#...#", ".###."]
R7 = ["..###..", ".#...#.", "#.....#", "#.....#", "#.....#", ".#...#.", "..###.."]
R9 = ["..#####..", ".#.....#.", "#.......#", "#.......#", "#.......#", ".#.....#.", "..#####.."]
STUFEN = [(0, R1, 0), (6, R3, 0), (16, R5, 1), (32, R5, 2), (48, R7, 2), (66, R7, 3), (84, R7, 4),
          (102, R9, 4), (128, R9, 5)]
TAKT, LEBEN = 51, 153                          # alle 51 Bilder ein Kringel (fünf je Runde), so lange lebt er
X_RAUCH, ZIEHT = 12, 3                         # Start über der Pfeife; alle drei Bilder eine Spalte nach rechts
ZWINKERN = (25, 180)                           # Beginn, je sieben Bilder
X_KERZE = 53
ZWEIG_VON, ZWEIG_BIS, BEEREN = 45, 62, (48, 59)     # Gesteck um die Kerze
FLACKERN = [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]      # 17 Bilder, 15-mal je Runde


def kringel(bild, alter, versatz=0):
    """Ein Kringel: steigt von der Pfeife auf, zieht nach rechts, wächst und verblasst mit dem Alter."""
    form, ton = R1, 0
    for ab, f, t in STUFEN:
        if alter >= ab:
            form, ton = f, t
    cx = X_RAUCH + (alter + versatz) // ZIEHT                        # versetzt: nicht alle rücken im selben Bild
    cy = 5 if alter < 3 else 4 if alter < 9 else 3
    x0, y0 = cx - len(form[0]) // 2, cy - len(form) // 2
    for dy, zeile in enumerate(form):
        for dx, c in enumerate(zeile):
            if c == "#":
                bild.setze(x0 + dx, y0 + dy, RAUCH[ton])


def kulisse(bild, f):
    """Fensterbank und Gesteck: Tannenzweige mit Beeren, Kerze mit flackernder Flamme."""
    bild.rechteck(0, 15, B, 1, BANK)
    for x in range(ZWEIG_VON, ZWEIG_BIS + 1):                        # Tannenzweige: gleichmäßig gezackt
        hoch = 2 + x % 2
        bild.rechteck(x, 15 - hoch, 1, hoch, ZWEIG)
    for x in BEEREN:
        bild.setze(x, 13, BEERE)
    bild.rechteck(X_KERZE, 15, 3, 1, HALTER)
    bild.rechteck(X_KERZE, 10, 3, 5, KERZE)
    bild.setze(X_KERZE + 1, 9, FLAMME_FUSS)
    bild.setze(X_KERZE + 1, 8, FLAMME)
    if FLACKERN[f % 17]:
        bild.setze(X_KERZE + 1, 7, FLAMME)


def mann(bild, f):
    """Das Männchen: Glut im Bauch und im Pfeifenkopf vor dem Paffen, Mund auf beim Paffen, Zwinkern."""
    t = f % TAKT
    glut = ASCHE
    if t >= TAKT - 10:                                               # vor dem Paffen glimmt die Räucherkerze auf
        glut = GLUT[min(2, (t - (TAKT - 10)) // 3)]
    elif t < 6:
        glut = GLUT[max(0, 1 - t // 3)]
    zieht = t >= TAKT - 4                                            # zieht an der Pfeife: der Kopf glüht
    pafft = t < 6                                                    # Mund auf, der Rauch kommt
    zu = any(z <= f < z + 7 for z in ZWINKERN)
    farben = {"g": HUT, "y": BAND, "s": HAUT, "a": AUGE, "z": LID if zu else AUGE, "n": NASE,
              "w": BART, "o": AUGE if pafft else BART, "q": PFEIFE, "p": GLUT[1] if zieht else PFEIFE,
              "r": JACKE, "d": ARM, "h": HAUT, "k": glut, "b": HOSE, "c": SOCKEL}
    bild.figur(X_MANN, 0, MANN, farben)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        kulisse(bild, f)
        mann(bild, f)
        for k in range(255 // TAKT):                                 # Rauchkringel
            alter = (f - k * TAKT) % 255
            if alter < LEBEN:
                kringel(bild, alter, k % ZIEHT)
        liste.append(bild)
    return liste
