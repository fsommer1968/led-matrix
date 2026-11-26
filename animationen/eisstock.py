"""Eisstockschießen auf dem zugefrorenen Teich: Zwei Spieler in dicken Jacken (Rot und Blau) schießen
nacheinander ihren Eisstock zur gelben Daube am rechten Ende der Bahn. Rot holt aus, pendelt den
Stock nach hinten und lässt ihn mit einem Ausfallschritt los: Er gleitet mit kleiner Schneespur
immer langsamer und bleibt dicht vor der Daube liegen, Rot jubelt. Dann tritt Blau an, sein Stock
kommt schneller, stößt den roten weg (Funken beim Anstoß) und schiebt sich selbst an die Daube:
Blau jubelt, Rot rauft sich die Haare, schüttelt den Kopf und sinkt in die Knie. Zum Schluss
gehen beide zu ihren Stöcken, schieben sie am Griff übers Eis zurück, und alles steht wieder
bereit – 255 Bilder, die Runde geht ohne Sprung in sich über.

Am verschneiten Ufer stehen drei Tannen und eine Laterne, zwei Sterne funkeln langsam. Gezeichnet
wird von hinten nach vorn; wer einen Stock führt, hat ihn vor sich.

Sparsam gezeichnet (Matrix speichert 80 KB, Ziel ≤ 76000 Bytes, siehe groesse.py): Himmel, Schnee
und Eis sind waagerechte Bänder (gleiche Nachbarspalten), die drei Tannen sind Kopien voneinander
(die erste kostet rund 9 KB, jede weitere unter 1 KB), keine Flocken; die Schneespur besteht aus
drei Punkten hinter dem gleitenden Stock. Die Kulisse allein braucht rund 35 KB, ein Spieler mit
Stock rund 17 KB.
"""
from basis import BLAU, GELB, HAUT, ROT, Bild, dimmen

NAME = "eisstock"
TITEL = "Eisstockschießen"

HIMMEL = (3, 0, 26)
UFER = (190, 200, 235)                         # Schneerand hinten (Zeile 6) und vorn (Zeile 15)
UFER_SCHATTEN = (112, 126, 176)                # Zeile 7
EIS_HINTEN = (54, 70, 100)                     # Zeile 8–9: gedämpftes Blaugrau, damit Rot und Blau leuchten
EIS = (70, 90, 126)                            # Zeile 10–14
TANNE = (0, 110, 40)
STAMM = (33, 18, 7)
PFAHL = (70, 70, 85)                           # Laternenpfahl
LICHT = (255, 190, 50)
LICHT_HELL = (255, 235, 150)
SCHEIN = (255, 225, 160)                       # Laternenlicht auf dem Schnee
DAUBE = GELB
GRIFF = (255, 235, 170)                        # Griff der Stöcke
HOSE = (41, 26, 14)
AUGE = (50, 25, 10)
SPUR = (205, 225, 255)                         # Schneespur hinter dem gleitenden Stock
FUNKE = (255, 240, 120)
STERN = (255, 240, 200)
STERNE = [(10, 1, 5, 51), (61, 2, 30, 85)]     # x, y, Phase, Periode (Teiler von 255): funkeln langsam

TANNEN = (31, 38, 52)                          # Spalte der Spitze
LATERNE = 45
BAHN = 13                                      # auf dieser Zeile liegen Stöcke und Daube
DAUBE_X = 57                                   # zwei Spalten breit
START = 15                                     # hier steht, wer schießt (Spalte des Rumpfs)
VORN, NAH, STOSS_X = 19, 50, 45                # linke Spalte des Stocks: losgelassen, vor der Daube, Blau trifft

# Figuren (Blick nach rechts), dazu die Spalte, in der der Rumpf beginnt (er ist drei breit).
# m Mütze, h Gesicht, a Auge, j Jacke (mit Ärmeln fünf breit), b Hose
POSEN = {
    "steht": (1, [".mmm.", ".mmm.", ".hha.", "jjjjj", "jjjjj", ".jjj.", ".bbb.", ".bbb."]),
    "schritt": (1, [".mmm.", ".mmm.", ".hha.", "jjjjj", "jjjjj", ".jjj.", ".bbb.", ".b.b."]),
    "aus_tief": (3, ["...mmm.", "...mmm.", "...hha.", ".jjjjj.", "j..jjj.", "...jjj.", "...bbb.", "...bbb."]),
    "aus_hoch": (4, ["....mmm.", "....mmm.", "jjj.hha.", "...jjjj.", "....jjj.", "....jjj.", "....bbb.",
                     "...b..b."]),
    "wurf": (1, ["..mmm...", "..mmm...", "..hha...", ".jjjj...", ".jjjjjj.", ".bbbb...", "bb.bb..."]),
    "bueckt": (1, ["..mmm..", "..mmm..", ".jhha..", ".jjjj..", ".jjj.j.", ".bbb...", ".bbb..."]),
    "jubel": (1, ["j...j", "jmmmj", ".mmm.", ".hha.", ".jjj.", ".jjj.", ".jjj.", ".bbb.", ".bbb."]),
    "sprung": (1, ["j...j", "jmmmj", ".mmm.", ".hha.", ".jjj.", ".jjj.", ".jjj.", ".b.b.", "....."]),
    "haare": (1, ["jmmmj", "jmmmj", "jhhaj", ".jjj.", ".jjj.", ".jjj.", ".bbb.", ".bbb."]),
    "haare2": (1, ["jmmmj", "jmmmj", "jahhj", ".jjj.", ".jjj.", ".jjj.", ".bbb.", ".bbb."]),      # schüttelt den Kopf
    "knie": (1, ["jmmmj", "jmmmj", "jhhaj", ".jjj.", ".jjj.", "bbbb."]),
    "knie2": (1, ["jmmmj", "jmmmj", "jahhj", ".jjj.", ".jjj.", "bbbb."]),
}
STOCK = ["..g..", ".ccc.", "ccccc"]            # Griff oben, runder Körper in der Teamfarbe (fünf breit)
# Wo der Stock zur Pose ist: Spalten ab dem Rumpf (Blick nach rechts), Zeilen über den Füßen.
# Wer geht, schiebt den Stock am Griff neben sich übers Eis; beim Umdrehen ist er kurz vor den Füßen.
GRIFFWEITE = {"bereit": (3, 0), "bueckt": (3, 0), "hebt": (2, -1), "neben": (-1, -1), "aus_tief": (-6, -1),
              "aus_hoch": (-7, -3), "wurf": (4, 0), "haelt": (2, 0), "schiebt": (2, 0), "dreht": (-1, 0)}

# Ablauf (Bildnummern)
R_AUSHOLEN, R_WURF, R_LOS, R_LIEGT = 6, 16, 18, 56
R_JUBEL, R_WEG, R_SCHAUT = 57, 68, 78
B_KOMMT, B_DA, B_BEREIT, B_AUSHOLEN, B_WURF, B_LOS = 66, 80, 82, 84, 94, 96
STOSS = 112                                    # der blaue Stock trifft den roten
B_LIEGT, R_LIEGT_2 = 124, 134
HOLEN = 144                                    # beide gehen zu ihren Stöcken
B_DORT, B_ZURUECK, B_VORN, B_PLATZ = 180, 186, 222, 236         # am Stock, kehrt um, wieder am Start, am Platz
R_DORT, R_ZURUECK, R_VORN, R_PLATZ, R_STELLT = 182, 188, 222, 236, 240


def schwung(ab, wurf):
    """Rollen für einen Schuss: Stock anheben, nach hinten pendeln, vor und mit Ausfallschritt loslassen."""
    return [(ab, "hebt", True), (ab + 2, "neben", True), (ab + 3, "aus_tief", True), (ab + 5, "aus_hoch", True),
            (wurf - 2, "aus_tief", True), (wurf - 1, "neben", True), (wurf, "wurf", True), (wurf + 8, "steht", True)]


# Wege: (Bild, x des Rumpfs, Zeile der Füße); dazwischen gleichmäßig
ROTER = {
    "farben": {"m": (0, 190, 60), "j": ROT},
    "weg": [(0, START, 13), (R_WEG, START, 13), (R_SCHAUT, 23, 9), (HOLEN, 23, 9), (R_DORT, 56, 10),
            (R_ZURUECK, 56, 10), (R_VORN, 26, 10), (R_PLATZ, START, 13), (255, START, 13)],
    # (ab Bild, Pose, Blick nach rechts?)
    "rolle": [(0, "bereit", True), *schwung(R_AUSHOLEN, R_WURF), (R_JUBEL, "jubeln", True),
              (R_WEG, "geht", True), (R_SCHAUT, "steht", True), (STOSS + 2, "rauft", True),
              (HOLEN, "geht", True), (R_DORT, "bueckt", True), (R_ZURUECK - 2, "dreht", False),
              (R_ZURUECK, "schiebt", False), (R_PLATZ, "dreht", True), (R_PLATZ + 2, "haelt", True),
              (R_STELLT, "bereit", True)],
}
BLAUER = {
    "farben": {"m": (255, 110, 0), "j": BLAU},
    "weg": [(0, 1, 10), (B_KOMMT, 1, 10), (B_DA, START, 13), (HOLEN, START, 13), (B_DORT, 48, 13),
            (B_ZURUECK, 48, 13), (B_VORN, START, 13), (B_PLATZ, 1, 10), (255, 1, 10)],
    "rolle": [(0, "haelt", True), (B_KOMMT, "schiebt", True), (B_DA, "haelt", True), (B_BEREIT, "bereit", True),
              *schwung(B_AUSHOLEN, B_WURF), (STOSS + 2, "jubeln", True), (HOLEN, "geht", True),
              (B_DORT, "bueckt", True), (B_ZURUECK - 2, "dreht", False), (B_ZURUECK, "schiebt", False),
              (B_PLATZ, "dreht", True), (B_PLATZ + 2, "haelt", True)],
}

# Funken beim Anstoß (zwischen den beiden Stöcken, eine Zeile über dem Eis), je Bild eine Stufe
FUNKEN = [[(-1, 0), (0, 0)], [(-1, -1), (0, -1), (-2, -2), (1, -2)], [(-3, -3), (2, -3), (-1, -3)],
          [(-4, -3), (3, -3)], [(-5, -4), (4, -4)]]


def aus(t):
    """Ausgleiten: schnell los, sanft zum Stehen."""
    return 1 - (1 - t) ** 2


def ort(sp, f):
    """Ort des Spielers im Bild f: x des Rumpfs, Zeile der Füße."""
    weg = sp["weg"]
    for (f0, x0, y0), (f1, x1, y1) in zip(weg, weg[1:]):
        if f0 <= f < f1:
            t = (f - f0) / (f1 - f0)
            return round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
    return weg[-1][1], weg[-1][2]


def rolle(sp, f):
    """Pose und Blickrichtung des Spielers im Bild f."""
    pose, rechts = "steht", True
    for ab, p, r in sp["rolle"]:
        if ab <= f:
            pose, rechts = p, r
    return pose, rechts


def in_der_hand(sp, f):
    """Linke Spalte und unterste Zeile des Stocks, solange der Spieler ihn führt."""
    x, fuss = ort(sp, f)
    pose, rechts = rolle(sp, f)
    dx, dy = GRIFFWEITE[pose]
    return (x + dx if rechts else x - 2 - dx), fuss + dy


def stock_rot(f):
    """Ort des roten Stocks und wie viele Punkte Schnee hinter ihm stäuben (0, solange er ruht)."""
    if f < R_LOS or f >= R_DORT:
        return in_der_hand(ROTER, f), 0
    if f < R_LIEGT:                                                  # gleitet bis kurz vor die Daube
        t = (f - R_LOS) / (R_LIEGT - R_LOS)
        return (round(VORN + (NAH - VORN) * aus(t)), BAHN), 3 if t < 0.7 else 0
    if f < STOSS:
        return (NAH, BAHN), 0
    t = min(1, (f - STOSS) / (R_LIEGT_2 - STOSS))                    # weggestoßen: schräg nach hinten
    weit = 1 - (1 - t) ** 3                                          # springt mit einem Ruck los
    return (round(NAH + 9 * weit), round(BAHN - 3 * weit)), 1 if 0.1 < t < 0.5 else 0


def stock_blau(f):
    """Ort des blauen Stocks und die Punkte seiner Schneespur."""
    if f < B_LOS or f >= B_DORT:
        return in_der_hand(BLAUER, f), 0
    if f < STOSS:                                                    # schneller Schuss, trifft noch mit Schwung
        t = f - B_LOS
        dauer = STOSS - B_LOS
        v0 = 2 * (STOSS_X - VORN) / dauer - 1.25                     # kommt mit 1,25 Spalten je Bild an
        return (round(VORN + v0 * t - (v0 - 1.25) / (2 * dauer) * t * t), BAHN), 3
    t = min(1, (f - STOSS) / (B_LIEGT - STOSS))                      # schiebt sich noch an die Daube
    return (round(STOSS_X + 6 * aus(t)), BAHN), 0


def zeichne(bild, x, fuss, pose, farben, rechts):
    """Figur mit dem Rumpf ab Spalte x, die unterste Zeile auf der Zeile fuss; nach links gespiegelt
    bleibt der Rumpf in denselben Spalten."""
    versatz, zeilen = POSEN[pose]
    oben = fuss - len(zeilen) + 1
    for dy, zeile in enumerate(zeilen):
        for dx, c in enumerate(zeile):
            if c != ".":
                rel = dx - versatz
                bild.setze(x + rel if rechts else x + 2 - rel, oben + dy, farben[c])


def kulisse(bild, f):
    """Sterne, Ufer, Eis, Tannen, Laterne und Daube."""
    for x, y, phase, periode in STERNE:
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    bild.rechteck(0, 6, 64, 1, UFER)                                 # Ufer, Eis und vorderer Schneerand
    bild.rechteck(0, 7, 64, 1, UFER_SCHATTEN)
    bild.rechteck(0, 8, 64, 2, EIS_HINTEN)
    bild.rechteck(0, 10, 64, 5, EIS)
    bild.rechteck(0, 15, 64, 1, UFER)
    for tx in TANNEN:                                                # Tannen am Ufer
        for k, halb in enumerate((0, 1, 1, 2, 2)):
            bild.rechteck(tx - halb, 1 + k, 2 * halb + 1, 1, TANNE)
        bild.setze(tx, 1, UFER)                                      # Schnee auf Spitze und Astenden
        bild.setze(tx - 2, 4, UFER)
        bild.setze(tx + 2, 4, UFER)
        bild.setze(tx, 6, STAMM)
    bild.rechteck(LATERNE, 2, 1, 5, PFAHL)                           # Laterne: Pfahl, Dach, Licht, Schein im Schnee
    bild.rechteck(LATERNE - 1, 0, 3, 1, PFAHL)
    bild.rechteck(LATERNE - 1, 1, 3, 1, LICHT)
    bild.setze(LATERNE, 1, LICHT_HELL)
    bild.rechteck(LATERNE - 2, 6, 2, 1, SCHEIN)
    bild.rechteck(LATERNE + 1, 6, 2, 1, SCHEIN)
    bild.rechteck(DAUBE_X, BAHN, 2, 1, DAUBE)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        kulisse(bild, f)
        dinge = []                                                   # von hinten nach vorn zeichnen
        for sp, stock, farbe in ((ROTER, stock_rot, ROT), (BLAUER, stock_blau, BLAU)):
            x, fuss = ort(sp, f)
            pose, rechts = rolle(sp, f)
            if pose in ("geht", "schiebt"):
                pose = "schritt" if (f // 3) % 2 else "steht"
            elif pose == "jubeln":
                pose = "sprung" if (f // 5) % 2 else "jubel"
            elif pose == "rauft":
                pose = ("knie" if f >= STOSS + 14 else "haare") + ("2" if (f // 4) % 2 else "")
            elif pose in ("bereit", "haelt", "dreht", "hebt", "neben"):
                pose = "steht"
            dinge.append((fuss, "spieler", (x, fuss, pose, {**sp["farben"], "h": HAUT, "a": AUGE, "b": HOSE},
                                            rechts)))
            (sx, sy), spur = stock(f)
            vor = fuss + 0.1 if rolle(sp, f)[0] in GRIFFWEITE else 0     # in der Hand: vor dem Spieler
            dinge.append((max(sy + 0.5, vor), "stock", (sx, sy, farbe)))
            for k, (dx, hell) in enumerate(((-1 - f % 2, 1), (-4 + f % 2, 0.7), (-6 - f % 2, 0.7))):
                if k < spur and sx + dx >= VORN:                     # kleine Schneespur (unter allem anderen)
                    bild.setze(sx + dx, sy, dimmen(SPUR, hell))
        for _, art, daten in sorted(dinge, key=lambda e: e[0]):
            if art == "stock":
                sx, sy, farbe = daten
                bild.figur(sx, sy - 2, STOCK, {"g": GRIFF, "c": farbe})
            else:
                zeichne(bild, *daten)
        k = f - STOSS                                                # Funken beim Anstoß
        if 0 <= k < len(FUNKEN):
            for dx, dy in FUNKEN[k]:
                bild.setze(NAH + dx, BAHN - 1 + dy, FUNKE if k < 3 else dimmen(FUNKE, 0.5))
        liste.append(bild)
    return liste
