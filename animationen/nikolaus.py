"""Nikolaus (6. Dezember): Bischof mit Mitra und goldenem Stab stapft mit dem Sack durch den
Schnee herein, winkt, wirft Äpfel, Nüsse und Mandarinen in drei Stiefel, winkt zum Abschied –
255 Bilder. Ohne Text, er ist an Mitra und Stab zu erkennen (23.11.2026).
"""
import colorsys
import math

from basis import B, GELB, GOLD, NACHTBLAU, ROT, SCHNEEDECKE, WEISS, Bild, dimmen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "nikolaus"
TITEL = "Nikolaus winkt und füllt die Stiefel"

HAUT = (214, 171, 143)
BART = (240, 240, 250)
DUNKEL = (60, 35, 25)
STAB = (58, 37, 14)
MANTEL = (200, 0, 20)
SACK = (49, 31, 12)
SACK_DUNKEL = (33, 19, 6)
# Die Matrix speichert nur 80 KB je Animation, jedes Bild einzeln komprimiert: Jeder einzelne
# Punkt am Himmel kostet in jedem Bild rund 5 Bytes. Darum blinken die Sterne reihum auf (jeder
# ist nur einen Teil der Zeit an), und es fallen wenige Flocken (23.11.2026).
STERN = (255, 240, 200)
STERN_AN = 0.33                               # Anteil der Zeit, in der ein Stern leuchtet
# (x, y, Periode in Bildern, Phase 0…1) – Perioden teilen 255, die Schleife läuft nahtlos
STERNE = [(28, 1, 85, 0.00), (39, 5, 51, 0.30), (50, 3, 85, 0.55), (22, 4, 51, 0.80),
          (56, 5, 85, 0.20), (33, 5, 51, 0.05), (20, 1, 85, 0.70), (45, 1, 51, 0.55),
          (61, 2, 85, 0.90), (25, 6, 85, 0.40), (36, 2, 51, 0.65), (58, 0, 51, 0.15),
          (47, 6, 85, 0.35), (42, 3, 85, 0.82)]
FLOCKE = (150, 165, 215)
# (x, Runden je Durchlauf, Startzeile 0…20)
FLOCKEN = [(35, 3, 15.8), (58, 4, 9.4), (48, 4, 2.7), (23, 6, 5.5), (54, 5, 18.0), (40, 6, 12.9),
           (18, 5, 11.0), (62, 3, 0.5), (30, 4, 16.0), (45, 3, 6.0)]
ANZAHL_FLOCKEN = 5

NIKOLAUS = [   # Stab links (s, Krümme g), Mitra (m, Kreuz und Band g), Gesicht, Bart, Mantel
    ".gg.........",
    "g..g..m.....",
    "g....mgm....",
    "g...mgggm...",
    "s...mmgmm...",
    "s...mmmmm...",
    "s...ggggg...",
    "s...heheh...",
    "s..bbbbbbb..",
    "shmbbbbbbbm.",
    "s.mmbbbbbmm.",
    "s.mmmbbbmmm.",
    "s.mmmmbmmmm.",
    "s.mmmmgmmmm.",
    "s.mmmmgmmmm.",
    "s..dd...dd..",
]
FARBEN = {"g": GOLD, "s": STAB, "m": MANTEL, "w": WEISS, "h": HAUT, "e": (0, 0, 40),
          "b": BART, "d": DUNKEL, "k": SACK, "K": SACK_DUNKEL}
SACK_BILD = [".KK..", "kkkk.", "kkkk.", "kkkk.", "kkkk."]
# rechter Arm je Haltung: Liste von (dx, dy, Zeichen)
ARM = {
    "unten": [(11, 9, "m"), (11, 10, "m"), (11, 11, "m"), (11, 12, "w")],
    "hoch1": [(11, 9, "m"), (11, 8, "m"), (12, 9, "m"), (12, 8, "m"), (12, 7, "m"), (13, 7, "m"),
              (12, 6, "m"), (13, 6, "m"), (12, 5, "w"), (13, 5, "w"), (12, 4, "w"), (13, 4, "w")],
    "hoch2": [(11, 9, "m"), (11, 8, "m"), (12, 9, "m"), (12, 8, "m"), (13, 8, "m"), (13, 7, "m"),
              (14, 7, "m"), (14, 6, "m"), (15, 6, "w"), (15, 5, "w"), (16, 6, "w"), (16, 5, "w")],
    "sack": [(11, 9, "m"), (11, 10, "m"), (12, 10, "m"), (12, 11, "m"), (13, 11, "w"), (13, 10, "w")],
}
STIEFEL = ["wwwww..", "wwwww..", ".ccc...", ".ccc...", ".ccc...", ".cccccc", ".cccccc"]
STIEFEL_X = [29, 41, 53]
STIEFEL_FARBE = [ROT, ROT, ROT]               # alle gleich: der 2. und 3. sind dann fast gratis
APFEL, MANDARINE, NUSS, GRUEN = (255, 30, 0), (255, 120, 0), GELB, (90, 230, 0)
GABEN = [[MANDARINE, NUSS, GRUEN], [APFEL, NUSS, MANDARINE], [NUSS, APFEL, MANDARINE]]
PLATZ = [(0, 7), (3, 7), (1, 5)]              # wo die drei Gaben aus dem Stiefel schauen
FLUG = 16                                     # Bilder je Wurf
WUERFE = [(98 + k * 9, k % 3, k // 3) for k in range(9)]   # (Start, Stiefel, wievielte Gabe)
X_STAND = 3


def nikolaus(bild, x, f, arm, geht, sack_getragen):
    figur = list(NIKOLAUS)
    if geht and (f // 4) % 2:
        figur[-1] = "s...dddd...."
        figur[-2] = "s..mmmgmmm.."
    bild.figur(x, 0, figur, FARBEN)
    if sack_getragen:                                             # Sack hängt an der rechten Hand
        bild.figur(x + 11, 10 - (geht and (f // 4) % 2), SACK_BILD, FARBEN)
        arm = "unten"
    for dx, dy, c in ARM[arm]:
        bild.setze(x + dx, dy, FARBEN[c])


def sterne(bild, f):
    for x, y, periode, phase in STERNE:
        t = abs((f / periode + phase) % 1 - 0.5) / STERN_AN       # 0 = Mitte des Aufleuchtens
        if t < 0.5:
            bild.setze(x, y, STERN if t < 0.25 else dimmen(STERN, 0.5))


def schnee(bild, f):
    for i, (x, runden, start) in enumerate(FLOCKEN[:ANZAHL_FLOCKEN]):
        y = (start + f * runden * 20 / 255) % 20 - 2
        dx = round(math.sin(2 * math.pi * (f * 5 / 255 + i * 0.37)))
        bild.setze(x + dx, y, FLOCKE)


def gabe(bild, x, y, farbe):
    bild.rechteck(int(round(x)), int(round(y)), 2, 2, farbe)


def _matrixfarbe(c):
    """Farbe, wie die Matrix sie zeigt (7/4/5 Bit H/S/V, wie hsv16 in led/pi/matrix_spieler.py)."""
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return round(h * 127) & 0x7F, round(s * 15), round(v * 31)


def _jedes_bild_anders(liste):
    """Gleiche Nachbarbilder legt PIL im GIF zu einem zusammen – dann fehlen Bilder, und die
    Matrix (fester Takt) läuft an ruhigen Stellen schneller. Ein Bild, das seinem Vorgänger
    gleicht, bekommt darum an einem Pixel einen um 1 anderen Farbwert, den die Matrix genauso
    zeigt: im GIF verschieden, auf den LEDs unsichtbar."""
    for vor, bild in zip(liste, liste[1:]):
        if bild.px != vor.px:
            continue
        stellen = ((y, x, k, d) for y in range(16) for x in range(64) for k in range(3)
                   for d in (1, -1))
        for y, x, k, d in stellen:
            c = bild.px[y][x]
            n = tuple(w + d if i == k else w for i, w in enumerate(c))
            if 0 <= n[k] <= 255 and _matrixfarbe(n) == _matrixfarbe(c):
                bild.px[y] = bild.px[y][:x] + [n] + bild.px[y][x + 1:]
                break
    return liste


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        sterne(bild, f)
        schnee(bild, f)
        bild.rechteck(0, 15, B, 1, SCHNEEDECKE)
        for i, sx in enumerate(STIEFEL_X):                         # Stiefel vor der Tür
            for start, ziel, k in WUERFE:                          # Gaben, die schon drin sind
                if ziel == i and f >= start + FLUG:
                    gabe(bild, sx + PLATZ[k][0], PLATZ[k][1], GABEN[i][k])
                    if k == 2:                                     # die dritte liegt obenauf
                        bild.rechteck(sx + 1, 5, 3, 2, GABEN[i][k])
                        bild.rechteck(sx + 2, 7, 1, 2, GABEN[i][k])
            bild.figur(sx, 9, STIEFEL, {"w": WEISS, "c": STIEFEL_FARBE[i]})
        # Ablauf: 0–36 kommt herein, 36–96 winkt, 96–190 füllt Stiefel, 190–228 winkt, 228+ geht
        winken = "hoch1" if (f // 5) % 2 else "hoch2"
        if f < 36:
            x, arm, geht = X_STAND - 19 + round(19 * f / 36), "unten", True
        elif f < 96:
            x, arm, geht = X_STAND, winken, False
        elif f < 190:
            x, geht = X_STAND, False
            t = (f - 98) % 9 if 98 <= f < 98 + 9 * 9 else 5
            arm = "sack" if t >= 6 else "hoch2" if t < 3 else "unten"
        elif f < 228:
            x, arm, geht = X_STAND, winken, False
        else:
            x, arm, geht = X_STAND - round((f - 228) * 0.75), "unten", True
        if not geht:                                               # Sack steht neben ihm
            bild.figur(x + 12, 10, SACK_BILD, FARBEN)
        nikolaus(bild, x, f, arm, geht, geht)
        for start, ziel, k in WUERFE:                              # Gaben fliegen im Bogen
            t = f - start
            if 0 <= t < FLUG:
                x0, y0 = X_STAND + 16, 4
                x1, y1 = STIEFEL_X[ziel] + PLATZ[k][0], PLATZ[k][1]
                gx = x0 + (x1 - x0) * t / FLUG
                gy = y0 + (y1 - y0) * t / FLUG - 4 * 4 * (t / FLUG) * (1 - t / FLUG)
                gabe(bild, gx, gy, GABEN[ziel][k])
        liste.append(bild)
    return _jedes_bild_anders(liste)
