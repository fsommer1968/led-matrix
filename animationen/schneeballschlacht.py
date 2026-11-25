"""Schneeballschlacht: zwei Kinder mit bunten Mützen neben ihren Schneewällen werfen hin und her
(ausholen, werfen, ducken, jubeln), Treffer stäuben; am Ende lassen sich beide in den Schnee fallen
und machen Schneeengel (Blick von oben), die Engel bleiben im Schnee zurück – 255 Bilder.
"""
import math
import random

from basis import B, H, HAUT, PINK, ROT, WEISS, Bild, Schnee, dimmen, mischen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "schneeballschlacht"
TITEL = "Schneeballschlacht und Schneeengel"

HIMMEL = (4, 12, 40)
KANTE = (215, 225, 250)                        # Oberkante der Schneedecke
BODEN = (105, 118, 165)
WALL = (235, 240, 255)
WALL_SCHATTEN = (150, 165, 215)
TANNE = (0, 70, 30)
HOSE = (41, 27, 15)
AUGE = (50, 25, 10)
FELD = (38, 48, 88)                            # Schneefläche von oben (nachts, gedämpft)
ABDRUCK = (185, 198, 240)
ABDRUCK_TIEF = (125, 140, 195)                # wo Kopf und Rumpf lagen
SCHNEE = Schnee(anzahl=8, saat=931, farbe=(120, 130, 175))
SCHNEE.flocken += [(24, 1.0, 0.0), (39, 1.0, 10.0)]   # zwei nahe Flocken: jedes Bild bewegt sich etwas
GLITZER = [(random.Random(933 + i).randrange(B), random.Random(977 + i).randrange(H)) for i in range(256)]

KIND_A = {"m": ROT, "j": (0, 90, 255), "g": (255, 200, 0)}          # Mütze, Jacke, Handschuh
KIND_B = {"m": PINK, "j": (0, 190, 70), "g": (255, 120, 0)}

# Figuren (Blick nach rechts), 10 breit; p Bommel, m Mütze, h Gesicht, a Auge, j Jacke,
# g Handschuh, b Hose, o Schneeball, W Schnee im Gesicht
POSEN = {
    "steh": ["....pp....", "...mmmm...", "...mmmm...", "...hhah...", "...hhhh...",
             "...jjjj...", "...jjjjg..", "...jjjj...", "...bbbb...", "...b..b..."],
    "ausholen": ["....pp....", "oo.mmmm...", "g..mmmm...", ".j.hhah...", "..jhhhh...",
                 "...jjjj...", "...jjjjg..", "...jjjj...", "...bbbb...", "...b..b..."],
    "wurf": ["....pp....", "...mmmm...", "...mmmm...", "...hhah.g.", "...hhhhj..",
             "...jjjjj..", "..gjjjj...", "...jjjj...", "...bbbb...", "..b...b..."],
    "jubel": ["....pp....", ".g.mmmm.g.", ".j.mmmm.j.", "..jhhahj..", "...hhhh...",
              "...jjjj...", "...jjjj...", "...jjjj...", "...bbbb...", "...b..b..."],
    "getroffen": ["...pp.....", "..mmmm....", "..mmmm.W..", "..hhWWW...", ".ghhWW..g.",
                  "..jjjjjj..", "...jjjj...", "...jjjj...", "...bbbb...", "...b..b..."],
    "duck": ["..........", "..........", "..........", "..........", "....pp....",
             "...mmmm...", "...mmmm...", "...hhah...", "..jjjjjg..", "..bbbbbb.."],
    "liegen": ["..........", "..........", "..........", "..........", "..........",
               "..........", "..........", "..........", ".mmhhjjjj.b", "pmmhhjjjjbbb"],
}

A_X, B_X, KIND_Y = 3, 51, 3                    # linke obere Ecke der Figuren
FLUG = {"treffer": 17, "umfallen": 17, "wall": 13, "drueber": 22}
ZIEL = {"treffer": (54, 7), "umfallen": (54, 7), "wall": (41, 10), "drueber": (67, 6)}
WUERFE_A = [(12, "wall"), (62, "treffer"), (112, "drueber"), (162, "umfallen")]
WUERFE_B = [(37, "treffer"), (87, "drueber"), (137, "treffer")]
SEITENSICHT = 194                              # bis hierhin Schlacht, danach Überblendung
ENGEL = 200                                    # ab hier Blick von oben
AUFSTEHEN = 238                                # Kinder weg, die Engel bleiben
PERIODE = 14                                   # Bilder je Armschwung


def _posen(eigene, fremde, legt_sich=None):
    """Haltung je Bild: Standard stehen; Ducken, Treffer, Jubel und Würfe nach Plan."""
    p = ["steh"] * SEITENSICHT

    def fuelle(von, bis, pose):
        for f in range(max(0, von), min(SEITENSICHT, bis + 1)):
            p[f] = pose

    for t, ergebnis in fremde:
        lande = t + FLUG[ergebnis]
        if ergebnis in ("wall", "drueber"):
            fuelle(t + 4, lande + (3 if ergebnis == "wall" else -3), "duck")
        elif ergebnis == "treffer":
            fuelle(lande, lande + 4, "getroffen")
        else:
            fuelle(lande, lande + 3, "getroffen")
            fuelle(lande + 4, lande + 6, "duck")
            fuelle(lande + 7, SEITENSICHT, "liegen")
    for t, ergebnis in eigene:
        if ergebnis in ("treffer", "umfallen"):
            fuelle(t + FLUG[ergebnis] + 1, t + FLUG[ergebnis] + 8, "jubel")
        fuelle(t - 5, t - 1, "ausholen")
        fuelle(t, t + 3, "wurf")
    if legt_sich is not None:                                        # lässt sich selbst fallen
        fuelle(legt_sich, legt_sich + 2, "duck")
        fuelle(legt_sich + 3, SEITENSICHT, "liegen")
    return p


POSE_A = _posen(WUERFE_A, WUERFE_B, legt_sich=188)
POSE_B = _posen(WUERFE_B, WUERFE_A)


def kind(bild, x, f, pose, farben, spiegeln):
    palette = {"p": WEISS, "h": HAUT, "a": AUGE, "b": HOSE, "o": WEISS, "W": WEISS, **farben}
    y = KIND_Y - (1 if pose == "jubel" and (f // 2) % 2 else 0)      # hüpft beim Jubeln
    zeilen = POSEN[pose]
    if pose == "liegen":                                             # Kopf nach außen
        x += -3 if not spiegeln else 1
    bild.figur(x, y, zeilen, palette, spiegeln=spiegeln)


def wall(bild, x):
    for dy, (einzug, farbe) in enumerate(((2, WALL), (1, WALL_SCHATTEN), (0, WALL_SCHATTEN), (0, WALL_SCHATTEN))):
        bild.rechteck(x + einzug, 9 + dy, 9 - 2 * einzug, 1, farbe)
    bild.rechteck(x + 1, 10, 7, 1, WALL)                             # helle Kuppe
    bild.setze(x + 1, 10, WALL_SCHATTEN)
    bild.setze(x + 7, 10, WALL_SCHATTEN)


def tanne(bild, x, hoehe):
    for k in range(hoehe):
        for dx in range(-(k // 2), k // 2 + 1):
            bild.setze(x + dx, 13 - hoehe + k, TANNE)
    bild.setze(x, 12 - hoehe, dimmen(KANTE, 0.6))


def ballpunkt(wurf, t, nach_rechts):
    """Ort des Balls t Bilder nach dem Abwurf (Bogen), für die linke Werferin gerechnet."""
    n = FLUG[wurf]
    zx, zy = ZIEL[wurf]
    a = t / n
    x = 13 + (zx - 13) * a
    y = 5 + (zy - 5) * a - 4 * 4.2 * a * (1 - a)
    return (x if nach_rechts else B - 1 - x), y


def seitensicht(f, stauben, z):
    bild = Bild(HIMMEL)
    for x, h in ((27, 5), (32, 7), (37, 4)):
        tanne(bild, x, h)
    SCHNEE.zeichnen(bild, f)
    bild.rechteck(0, 13, B, 1, KANTE)
    bild.rechteck(0, 14, B, 2, BODEN)
    wall(bild, 14)
    wall(bild, 41)
    g = min(f, SEITENSICHT - 1)
    kind(bild, A_X, f, POSE_A[g], KIND_A, False)
    kind(bild, B_X, f, POSE_B[g], KIND_B, True)
    for wuerfe, nach_rechts in ((WUERFE_A, True), (WUERFE_B, False)):
        for t0, ergebnis in wuerfe:
            t = f - t0
            n = FLUG[ergebnis]
            if 0 <= t < n:
                for k, hell in ((2, 0.25), (1, 0.5)):                # Schweif
                    if t - k >= 0:
                        sx, sy = ballpunkt(ergebnis, t - k, nach_rechts)
                        bild.setze(sx, sy, dimmen(WEISS, hell))
                x, y = ballpunkt(ergebnis, t, nach_rechts)
                bild.rechteck(round(x), round(y), 2, 2, WEISS)
            elif t == n and ergebnis != "drueber":                   # Treffer: stauben
                x, y = ballpunkt(ergebnis, n, nach_rechts)
                for _ in range(12):
                    stauben.append([x + 0.5, y, z.uniform(-1.1, 1.1), z.uniform(-1.3, 0.1), 9])
    for s in stauben:
        bild.setze(s[0], s[1], dimmen(WEISS, 0.35 + 0.65 * s[4] / 9))
        s[0] += s[2]
        s[1] += s[3]
        s[3] += 0.16
        s[4] -= 1
    stauben[:] = [s for s in stauben if s[4] > 0 and s[1] < 13]
    return bild


# ── Schneeengel von oben ───────────────────────────────────────────
ENGEL_KOERPER = ["..p..", ".mmm.", "mmmmm", "hahah", "hhhhh", "jjjjj", "jjjjj", "jjjjj", "jjjjj", ".bbb."]


def _strahl(bild, x, y, grad, laenge, farbe, seite, spitze=None):
    """Linie ab (x, y) nach außen; grad 0 = waagerecht, positiv = nach oben."""
    for k in range(laenge):
        px = x + seite * k * math.cos(math.radians(grad))
        py = y - k * math.sin(math.radians(grad))
        bild.setze(px, py, spitze if spitze and k == laenge - 1 else farbe)


def engel(bild, cx, f, farben):
    """Kind liegt im Schnee (Blick von oben) und schwingt Arme und Beine; liefert, wie viel vom
    Kind noch zu sehen ist (1 … 0)."""
    t = f - ENGEL
    palette = {"p": WEISS, "h": HAUT, "a": AUGE, "b": HOSE, **farben}
    schwung = -math.cos(t / PERIODE * 2 * math.pi)                   # −1 Arme unten … +1 oben
    weit = schwung if t < PERIODE / 2 else 1.0                       # so weit ist schon überstrichen
    arm = 12 + 48 * schwung
    bein = -70 + 20 * schwung                                        # −90 = gerade nach unten
    for seite in (-1, 1):                                            # Abdruck: Flügel und Rock
        grad = -36.0
        while grad <= 12 + 48 * weit:
            _strahl(bild, cx + seite * 2, 6, grad, 8, ABDRUCK, seite)
            grad += 4
        grad = -90.0
        while grad <= -70 + 20 * weit:
            _strahl(bild, cx + seite * 1, 9, grad, 7, ABDRUCK, seite)
            grad += 3
    if f >= AUFSTEHEN:                                               # Kind ist aufgestanden: Engel bleibt
        bild.rechteck(cx - 1, 0, 3, 5, ABDRUCK_TIEF)                 # Kopf
        bild.rechteck(cx - 2, 1, 5, 3, ABDRUCK_TIEF)
        bild.rechteck(cx - 2, 5, 5, 5, ABDRUCK_TIEF)                 # Rumpf
        for y in range(10, 16):                                      # Rock
            halb = 1 + (y - 9) * 3 // 4
            bild.rechteck(cx - halb, y, 2 * halb + 1, 1, ABDRUCK)
        return max(0.0, 1 - ((f - AUFSTEHEN) // 2 + 1) / 3)          # Kind blendet in zwei Stufen aus
    for seite in (-1, 1):
        _strahl(bild, cx + seite * 1, 10, bein, 5, HOSE, seite, spitze=(90, 55, 30))
        _strahl(bild, cx + seite * 3, 6, arm, 5, farben["j"], seite, spitze=farben["g"])
    bild.figur(cx - 2, 0, ENGEL_KOERPER, palette)
    return 1


def draufsicht(f):
    grund = Bild(FELD)
    for k in range(3):                                               # Glitzern im Schnee wandert
        grund.setze(*GLITZER[(f - k) % 256], (110, 125, 175) if k else (150, 165, 215))
    bild = Bild()
    bild.px = [zeile[:] for zeile in grund.px]
    rest = 1
    for cx, farben in ((18, KIND_A), (45, KIND_B)):
        rest = engel(bild, cx, f, farben)
    if 0 < rest < 1:                                                 # Kinder verschwinden weich
        ohne = Bild()
        ohne.px = [zeile[:] for zeile in grund.px]
        for cx, farben in ((18, KIND_A), (45, KIND_B)):
            engel(ohne, cx, AUFSTEHEN + 10, farben)
        mit = Bild()
        mit.px = [zeile[:] for zeile in grund.px]
        for cx, farben in ((18, KIND_A), (45, KIND_B)):
            engel(mit, cx, AUFSTEHEN - 1, farben)
        for y in range(H):
            for x in range(B):
                bild.px[y][x] = mischen(ohne.px[y][x], mit.px[y][x], rest)
    return bild


def bilder():
    z = random.Random(932)
    stauben = []
    liste = []
    for f in range(255):
        if f < ENGEL:
            bild = seitensicht(f, stauben, z)
            if f >= SEITENSICHT:                                     # Überblenden zum Blick von oben
                oben = draufsicht(ENGEL)
                a = ((f - SEITENSICHT) // 2 + 1) / 4                 # drei Stufen
                for y in range(H):
                    for x in range(B):
                        bild.px[y][x] = mischen(bild.px[y][x], oben.px[y][x], a)
        else:
            bild = draufsicht(f)
        liste.append(bild)
    return liste
