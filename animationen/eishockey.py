"""Eishockey auf dem Dorfteich: drei Kinder (zwei rote Jacken gegen eine grüne) jagen mit ihren
Schlägern einen schwarzen Puck über den zugefrorenen Teich. Anstoß in der Mitte, Pass durch die
Beine, Schuss ins rechte Tor zwischen den beiden Stiefeln, Jubel mit erhobenen Schlägern. Dann
holt sich Grün den Puck, zieht über das ganze Feld, ein Roter greift daneben, fällt hin und
rutscht auf dem Hosenboden, und der Schuss ins linke Tor gleicht aus. Zum Schluss liegt der Puck
wieder in der Mitte – 255 Bilder, die Runde geht ohne Sprung in sich über.

Die beiden Roten sehen gleich aus und tauschen über die Runde die Plätze: Wer am Ende den Puck
zur Mitte bringt, steht dort, wo am Anfang der andere stand. So schließt die Runde, ohne dass
jemand zurücklaufen muss.

Am Ufer stehen zwei Tannen und ein Haus mit Licht im Fenster, zwei Sterne funkeln. Der Puck zieht
bei Pass und Schuss einen hellen Strich, beim Abbremsen und beim Rutschen stäubt das Eis, hinter
dem Tor der Schnee. Wer vor dem Puck steht, verdeckt ihn (gezeichnet wird von hinten nach vorn).

Sparsam gezeichnet (Matrix speichert 80 KB, Ziel ≤ 76000 Bytes, siehe groesse.py): Himmel, Schnee
und Eis sind waagerechte Bänder (gleiche Nachbarspalten), die Tannen schlicht, das Haus ein Block
mit flachem Dach, die Stiefel eines Tors stehen in denselben Spalten, alle Kinder tragen die
gleiche Hose, keine Flocken, keine Kufenspuren. Zum Vergleich: jede Tanne kostet rund 5 KB, das
Haus 7 KB, ein Stern gut 1 KB.
"""
from basis import GELB, HAUT, PINK, ROT, WEISS, Bild, dimmen

NAME = "eishockey"
TITEL = "Eishockey auf dem Dorfteich"

HIMMEL = (3, 0, 26)
UFER = (190, 200, 235)                         # Schneerand hinten (Zeile 6) und vorn (Zeile 15)
UFER_SCHATTEN = (112, 126, 176)                # Zeile 7
EIS_HINTEN = (60, 86, 132)                     # Zeile 8–9
EIS = (74, 104, 154)                           # Zeile 10–14, hell genug für den schwarzen Puck
PUCK = (0, 0, 0)
TANNE = (0, 110, 40)
STAMM = (100, 55, 20)
STIEFEL = (215, 105, 15)
DACH = (150, 162, 205)                         # verschneites Dach des Hauses am Ufer
WAND = (95, 52, 28)
FENSTER = (255, 175, 40)
ZUG = (150, 185, 225)                          # heller Strich hinter dem schnellen Puck
HOLZ = (235, 175, 70)                          # Schläger
HOSE = (120, 75, 40)
AUGE = (50, 25, 10)
SPLITTER = (205, 230, 255)
STERN = (255, 240, 200)
STERNE = [(38, 0, 5, 51), (61, 2, 30, 85)]     # x, y, Phase, Periode (Teiler von 255): funkeln langsam

ROTE = {"m": GELB, "j": ROT}                   # Mütze, Jacke
GRUENE = {"m": PINK, "j": (0, 205, 60)}

HAUS = 18                                      # linke Spalte des Hauses (sieben breit)
TOR_L, TOR_R = 3, 58                           # linke Spalte der Stiefel (je drei breit)
MITTE = (31, 12)                               # Puck beim Anstoß (drei Spalten ab hier)
NETZ_L, NETZ_R = (0, 11), (61, 11)             # dort bleibt der Puck im Tor liegen

# Figuren (Blick nach rechts), dazu die Spalte, in der der Rumpf beginnt (er ist drei breit).
# m Mütze, h Gesicht, a Auge, j Jacke, b Hose, s Schläger
POSEN = {
    "gleiten": (1, [".mmm...", ".mmm...", ".hha...", ".jjj...", ".jjjs..", ".jjj.s.", ".bbb.s.", ".bbb.ss"]),
    "schritt": (1, [".mmm...", ".mmm...", ".hha...", ".jjj...", ".jjjs..", ".jjj.s.", ".bbb.s.", "b..b.ss"]),
    "tipp": (1, [".mmm...", ".mmm...", ".hha...", ".jjj...", ".jjjs..", ".jjj.s.", ".bbb.ss", ".bbb..."]),
    "ausholen": (1, [".mmm...", "smmm...", "shha...", ".sjj...", ".jjj...", ".jjj...", ".bbb...", ".b.b..."]),
    "schuss": (1, [".mmm...", ".mmm...", ".hha..s", ".jjj.s.", ".jjjs..", ".jjj...", ".bbb...", "b..b..."]),
    "jubel": (1, ["....s..", "....s..", ".mmms..", ".mmmj..", ".hhaj..", ".jjj...", ".jjj...", ".jjj...",
                  ".bbb...", ".bbb..."]),
    "sprung": (1, ["....s..", "....s..", ".mmms..", ".mmmj..", ".hhaj..", ".jjj...", ".jjj...", ".jjj...",
                   ".b.b...", "......."]),
    "wackeln": (1, [".....s.", ".mmm.s.", ".mmm...", ".hha...", "jjjjj..", ".jjj...", ".bbb...", "..b.b.."]),
    "hocke": (1, [".mmm...", ".mmm...", ".hha.s.", ".jjjjs.", ".bbbbs."]),
    "sitzen": (5, [".....mmm....", ".....mmm....", ".....hha....", ".....jjj...b", "ssss.jjjbbbb"]),
}

TAKT = 1.25                                    # der Ablauf ist in Schritten geplant, 1 Schritt = 1,25 Bilder
ENDE = 204                                     # Schritt 204 = Bild 255 = wieder Bild 0


def z(schritt):
    """Schritt des Ablaufplans → Bildnummer."""
    return round(schritt * TAKT)


# Wege: (Schritt, x des Rumpfs, Zeile der Kufen); dazwischen wird weich gegleitet.
# Rollen: (ab Schritt, Pose, Blick nach rechts?)
ROT_A = {   # steht beim Anstoß, passt, greift später daneben und rutscht auf dem Hosenboden
    "farben": ROTE,
    "weg": [(0, 25, 12), (16, 25, 12), (40, 33, 13), (78, 33, 13), (84, 37, 13), (88, 40, 13),
            (114, 50, 13), (132, 50, 13), (150, 44, 10), (ENDE, 44, 10)],
    "rolle": [(0, "lauf", True), (1, "tipp", True), (3, "lauf", True), (8, "schuss", True),
              (13, "lauf", True), (45, "jubeln", True),
              (72, "lauf", True), (84, "wackeln", True), (88, "sitzen", True), (128, "hocke", True),
              (132, "lauf", True)],
}
ROT_B = {   # lauert vorn, schießt das erste Tor, verteidigt zu spät, bringt den Puck zur Mitte
    "farben": ROTE,
    "weg": [(0, 44, 10), (16, 44, 10), (34, 45, 11), (66, 45, 11), (96, 12, 10), (110, 12, 10),
            (118, 13, 11), (126, 13, 11), (138, 6, 11), (144, 6, 11), (196, 25, 12), (ENDE, 25, 12)],
    "rolle": [(0, "lauf", True), (34, "ausholen", True), (38, "schuss", True), (44, "jubeln", True),
              (66, "lauf", False), (96, "lauf", True), (126, "lauf", False), (141, "lauf", True),
              (197, "tipp", True), (199, "lauf", True)],
}
GRUEN = {   # verliert den Anstoß, holt den Puck aus dem Tor und gleicht aus
    "farben": GRUENE,
    "weg": [(0, 37, 12), (12, 37, 12), (36, 40, 13), (46, 40, 13), (62, 55, 11), (68, 55, 11),
            (84, 45, 10), (108, 27, 12), (152, 27, 12), (190, 37, 12), (ENDE, 37, 12)],
    "rolle": [(0, "lauf", False), (5, "tipp", False), (7, "lauf", False), (12, "lauf", True),
              (65, "lauf", False), (108, "ausholen", False),
              (112, "schuss", False), (118, "jubeln", False), (152, "lauf", False), (201, "tipp", False),
              (203, "lauf", False)],
}
KINDER = [ROT_A, ROT_B, GRUEN]

# Puck: (Schritt, Ort, Art) – Ort ist ein Punkt oder das Kind, an dessen Schläger er liegt.
# Art bis zum nächsten Eintrag: "haftet" am Schläger, "gleitet" geradlinig zum nächsten Ort,
# "saust" ebenso, aber mit hellem Strich dahinter (Pass und Schuss).
PUCK_WEG = [(0, MITTE, "gleitet"), (8, MITTE, "saust"), (16, ROT_B, "haftet"), (38, ROT_B, "saust"),
            (42, NETZ_R, "gleitet"), (62, GRUEN, "gleitet"), (68, GRUEN, "haftet"), (112, GRUEN, "saust"),
            (118, NETZ_L, "gleitet"), (138, ROT_B, "gleitet"), (144, ROT_B, "haftet"), (ENDE, ROT_B, "haftet")]

# Eissplitter beim Abbremsen: (Schritt, x, Zeile, Richtung); der Fächer wächst über sieben Bilder
BREMSEN = [(36, 44, 13, 1), (116, 16, 11, 1), (188, 40, 12, 1)]
FAECHER = [[(0, 0), (1, -1)], [(1, 0), (2, -1), (1, -2)], [(2, -1), (3, -2), (1, -3)], [(3, -1), (4, -2), (2, -3)],
           [(4, -1), (5, -2)], [(5, -1), (6, -1)], [(6, 0)]]
# Tor: Schnee stäubt hinter den Stiefeln auf: (Schritt, x, Zeile)
TORE = [(42, 62, 10), (118, 1, 10)]
STAUB = [[(0, 0)], [(-1, -1), (1, 0)], [(-1, -1), (1, -1), (0, -2)], [(-1, -2), (1, -2)], [(0, -3)]]


def weich(t):
    """Sanft anfahren und ausgleiten."""
    return t * t * (3 - 2 * t)


def ort(kind, f):
    """Ort des Kindes im Bild f (ungerundet): x des Rumpfs, Zeile der Kufen."""
    weg = kind["weg"]
    for (s0, x0, y0), (s1, x1, y1) in zip(weg, weg[1:]):
        f0, f1 = z(s0), z(s1)
        if f0 <= f < f1:
            t = weich((f - f0) / (f1 - f0))
            return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
    return weg[-1][1], weg[-1][2]


def rolle(kind, f):
    """Pose und Blickrichtung des Kindes im Bild f."""
    pose, rechts = "lauf", True
    for s, p, r in kind["rolle"]:
        if z(s) <= f:
            pose, rechts = p, r
    return pose, rechts


def am_schlaeger(kind, f):
    """Wo der Puck liegt, wenn das Kind ihn führt: vor der Kelle."""
    x, y = ort(kind, f)
    return (round(x) + 6 if rolle(kind, f)[1] else round(x) - 6), round(y)


def puck_ort(f):
    """Ort des Pucks im Bild f und – solange er schnell übers Eis gleitet – wo er zwei Bilder
    vorher war (für den Strich dahinter), sonst None."""
    def punkt(wo, bild_nr):
        return am_schlaeger(wo, bild_nr) if isinstance(wo, dict) else wo
    for (s0, wo0, art), (s1, wo1, _) in zip(PUCK_WEG, PUCK_WEG[1:]):
        f0, f1 = z(s0), z(s1)
        if f0 <= f < f1:
            if art == "haftet":
                return punkt(wo0, f), None
            (x0, y0), (x1, y1) = punkt(wo0, f0), punkt(wo1, f1)

            def flug(t):
                return round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
            davor = flug(max(0, f - 2 - f0) / (f1 - f0)) if art == "saust" and f > f0 else None
            return flug((f - f0) / (f1 - f0)), davor
    return punkt(PUCK_WEG[-1][1], f), None


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
    for x, y, phase, periode in STERNE:
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    bild.rechteck(0, 6, 64, 1, UFER)                                 # Ufer, Eis und vorderer Schneerand
    bild.rechteck(0, 7, 64, 1, UFER_SCHATTEN)
    bild.rechteck(0, 8, 64, 2, EIS_HINTEN)
    bild.rechteck(0, 10, 64, 5, EIS)
    bild.rechteck(0, 15, 64, 1, UFER)
    for tx in (10, 54):                                              # zwei Tannen am Ufer
        for k, halb in enumerate((0, 1, 1, 2, 2)):
            bild.rechteck(tx - halb, 1 + k, 2 * halb + 1, 1, TANNE)
        bild.setze(tx, 1, UFER)                                      # Schneespitze
        bild.setze(tx, 6, STAMM)
    bild.rechteck(HAUS, 2, 7, 1, DACH)                               # Haus mit Licht im Fenster
    bild.rechteck(HAUS, 3, 7, 3, WAND)
    bild.rechteck(HAUS + 2, 3, 2, 2, FENSTER)
    for x0, spiegeln in ((TOR_L, False), (TOR_R, True)):             # Tore: je zwei Stiefel
        for oben in (7, 12):
            bild.figur(x0, oben, ["bb.", "bb.", "bbb"], {"b": STIEFEL}, spiegeln=spiegeln)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        kulisse(bild, f)
        (px, py), davor = puck_ort(f)
        dinge = [(py + 0.5, "puck", None)]                           # von hinten nach vorn zeichnen
        for kind in KINDER:
            xf, yf = ort(kind, f)
            x, fuss = round(xf), round(yf)
            pose, rechts = rolle(kind, f)
            faehrt = abs(ort(kind, f + 1)[0] - xf) > 0.08
            hoch = 0
            if pose == "lauf":
                pose = "schritt" if faehrt and (f // 5) % 2 else "gleiten"
            elif pose == "jubeln":
                pose = "sprung" if (f // 5) % 2 else "jubel"
                hoch = 1 if pose == "sprung" else 0
            dinge.append((fuss, "kind", (x, fuss, hoch, pose, rechts, kind["farben"], faehrt)))
        for _, art, daten in sorted(dinge, key=lambda e: e[0]):
            if art == "puck":
                if davor:                                            # Strich hinter dem schnellen Puck
                    bild.linie(davor[0] + 1, davor[1], px + 1, py, ZUG)
                bild.rechteck(px, py, 3, 1, PUCK)
                continue
            x, fuss, hoch, pose, rechts, farben, faehrt = daten
            zeichne(bild, x, fuss - hoch, pose, {**farben, "h": HAUT, "a": AUGE, "b": HOSE, "s": HOLZ}, rechts)
            if pose == "sitzen" and faehrt:                          # Eis stäubt vor den Füßen
                vorn = x + 7 if rechts else x - 5
                r = 1 if rechts else -1
                bild.setze(vorn + r, fuss - f % 2, SPLITTER)
                bild.setze(vorn + 2 * r, fuss - 1 - f % 3 // 2, WEISS)
        for s, sx, sy, r in BREMSEN:                                 # Eissplitter beim Abbremsen
            k = f - z(s)
            if 0 <= k < len(FAECHER):
                for dx, dy in FAECHER[k]:
                    bild.setze(sx + r * dx, sy + dy, WEISS if k < 4 else SPLITTER)
        for s, sx, sy in TORE:                                       # Tor: Schnee stäubt auf
            k = (f - z(s)) // 2
            if 0 <= k < len(STAUB):
                for dx, dy in STAUB[k]:
                    bild.setze(sx + dx, sy + dy, WEISS if k < 3 else SPLITTER)
        liste.append(bild)
    return liste
