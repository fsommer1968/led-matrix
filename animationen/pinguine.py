"""Pinguine: zwei Pinguine mit Zipfelmützen auf dem Eis – einer watschelt hin und her, der andere
wirft ihm einen Schneeball an den Kopf; ein dritter rutscht auf dem Bauch quer durch, die beiden
hüpfen über ihn. Mond, Eisberge, Lichterkette – 255 Bilder, läuft nahtlos im Kreis.

Der Hintergrund ist sparsam gezeichnet, weil die Matrix je Animation nur 80 KB speichert (Ziel
≤ 76000 Bytes, siehe groesse.py): Jedes Bild wird einzeln und spaltenweise gepackt, darum
kosten Einzelpunkte und senkrechte Kanten in allen 255 Bildern. Deshalb Eisberge als Stufen,
acht Lichter (aus = dunkel), ein Glanzlicht, wenig Schnee, Mond ohne Krater.
"""
import math

from basis import (B, BLAU, BUNT, GOLD, ROT, WEISS, Bild, Schnee, dimmen)

NAME = "pinguine"
TITEL = "Pinguine auf dem Eis"

HIMMEL = (0, 8, 36)
EIS = (120, 185, 240)
EIS_MITTE = (35, 85, 170)
EIS_TIEF = (20, 50, 120)
EISBERG = (22, 44, 100)
EISBERG_KANTE = (55, 95, 165)
FRACK = (45, 65, 150)                     # „schwarz“ wäre auf der Matrix aus – darum Blau
MOND = (235, 230, 190)
SCHNEE = Schnee(anzahl=3, saat=55, farbe=(110, 120, 170))
RUNDE = 127.5                             # zwei Runden je Durchlauf

STEHEN = [  # schaut nach rechts, 8 breit, 10 hoch
    "...p....",
    "..mmm...",
    ".mmmmm..",
    ".bbbbb..",
    ".sssss..",
    ".sswksoo",
    ".swwws..",
    "sswwwss.",
    ".swwws..",
    ".ff.ff..",
]
SCHRITT = STEHEN[:7] + ["sswwws..", ".swwwss.", "..ff.ff."]
AUSHOLEN = STEHEN[:5] + ["ssswksoo", "sswwws..", ".swwwss.", ".swwws..", ".ff.ff.."]
JUBEL = STEHEN[:5] + ["ssswksoo", "sswwwss.", ".swwws.s", ".swwws..", ".ff.ff.."]
RUTSCHEN = [  # Kopf rechts, 12 breit, 4 hoch
    ".......pmm..",
    "..ssssssbmm.",
    "ffssssssskoo",
    ".fwwwwwwww..",
]


def farben(muetze):
    return {"m": muetze, "p": WEISS, "b": WEISS, "s": FRACK, "w": WEISS, "k": (10, 10, 40),
            "o": GOLD, "f": (255, 110, 0)}


# Eisberge als Stufen (x von, x bis, oberste Zeile) – jede senkrechte Kante kostet in jedem Bild
# Platz, waagerechte Kanten nicht; die Matrix speichert nur 80 KB je Animation.
EISBERGE = ((0, 6, 10), (27, 34, 8), (35, 41, 10))
LICHTER = range(3, B, 8)                  # Lichterkette oben, acht Lichter


def hintergrund(bild, f):
    for x0, x1, oben in EISBERGE:
        bild.rechteck(x0, oben, x1 - x0 + 1, 13 - oben, EISBERG)
        bild.rechteck(x0, oben, x1 - x0 + 1, 1, EISBERG_KANTE)
    SCHNEE.zeichnen(bild, f)
    bild.kreis(56, 5, 2, MOND)
    for i, x in enumerate(LICHTER):                                    # zwei von drei leuchten
        if (i + f // 10) % 3 != 0:
            bild.setze(x, i % 2, BUNT[(i * 4 + f // 30) % len(BUNT)])
    bild.rechteck(0, 13, B, 1, EIS)                                    # Eisfläche
    bild.rechteck(0, 14, B, 1, EIS_MITTE)
    bild.rechteck(0, 15, B, 1, EIS_TIEF)
    for dx in range(4):                                                # ein Glanzlicht wandert
        x = (f // 3 + dx) % B
        bild.setze(x, 14, EIS)
        bild.setze(x, 15, EIS_MITTE)


def sprung(mitte, rutscher_mitte):
    """Hüpfhöhe, solange der Rutscher unter dem Pinguin durchkommt."""
    d = abs(mitte - rutscher_mitte)
    return round(4.4 * math.cos(d / 9 * math.pi / 2)) if d < 9 else 0


def bilder():
    liste = []
    spritzer = []
    ball = None
    for f in range(255):
        bild = Bild(HIMMEL)
        hintergrund(bild, f)
        # Rutscher: zweimal je Durchlauf von rechts nach links
        t3 = (f - 95) % RUNDE
        x3 = round(B + 2 - t3 * 1.0) if t3 < 82 else None
        mitte3 = x3 + 6 if x3 is not None else 999
        # Pinguin 1 (rot) watschelt hin und her
        w1 = 2 * math.pi * f / RUNDE
        x1 = 4 + round(18 * (0.5 - 0.5 * math.cos(w1)))
        rechts1 = math.sin(w1) >= 0
        # Pinguin 2 (blau) steht rechts und wirft
        x2 = 43
        tw = (f - 30) % RUNDE                                          # 0–10 ausholen, 10 Wurf
        if 10 <= tw < 11 and ball is None:
            ziel_f = f + 18
            zx = 4 + 18 * (0.5 - 0.5 * math.cos(2 * math.pi * ziel_f / RUNDE)) + 5
            ball = {"t": 0, "x0": x2 + 6.0, "y0": 4.0, "x1": zx, "y1": 6.0}
        treffer = (f - 58) % RUNDE                                     # 0 = Ball kommt an
        h1 = sprung(x1 + 3.5, mitte3)
        if treffer < 8:
            h1 = max(h1, (1, 2, 3, 3, 2, 2, 1, 0)[int(treffer)])
        h2 = sprung(x2 + 3.5, mitte3)
        if 30 <= tw < 54:                                              # freut sich
            h2 = max(h2, 2 if (tw // 4) % 2 == 0 else 0)
        if 0 <= tw < 10:
            figur2 = AUSHOLEN
        elif 30 <= tw < 54:
            figur2 = JUBEL if (tw // 4) % 2 == 0 else STEHEN
        else:
            figur2 = STEHEN
        steht1 = treffer < 14
        figur1 = STEHEN if steht1 or h1 else (STEHEN, SCHRITT)[(f // 5) % 2]
        bild.figur(x1, 3 - h1, figur1, farben(ROT), spiegeln=not rechts1)
        bild.figur(x2, 3 - h2, figur2, farben(BLAU), spiegeln=True)
        if 0 <= tw < 10:                                               # Schneeball in der Flosse
            bild.rechteck(x2 + 6, 5 - h2, 2, 2, WEISS)
        if x3 is not None:
            muetze = ((0, 220, 90), (255, 0, 160))[int((f - 95) // RUNDE) % 2]
            bild.figur(x3, 9, RUTSCHEN, farben(muetze), spiegeln=True)
            for k in range(2):                                         # Schneestaub dahinter
                if (f + k) % 3 != 2:
                    bild.setze(x3 + 13 + k * 2 + f % 2, 12 - (k + f) % 2, dimmen(WEISS, 0.9 - k * 0.25))
        if ball:
            u = ball["t"] / 18
            bx = ball["x0"] + (ball["x1"] - ball["x0"]) * u
            by = ball["y0"] + (ball["y1"] - ball["y0"]) * u - 6.5 * 4 * u * (1 - u) * 0.5
            bild.rechteck(round(bx), round(by), 2, 2, WEISS)
            bild.setze(round(bx) + 2, round(by) + (0 if u < 0.5 else -1), dimmen(WEISS, 0.45))
            ball["t"] += 1
            if ball["t"] > 18:
                for k in range(7):
                    w = math.pi * (0.15 + 0.7 * k / 6)
                    spritzer.append([ball["x1"], ball["y1"], 1.3 * math.cos(w) - 0.3,
                                     -1.2 * math.sin(w), 0])
                ball = None
        for s in spritzer:
            bild.setze(s[0], s[1], dimmen(WEISS, 1 - s[4] / 10))
            s[0] += s[2]
            s[1] += s[3]
            s[3] += 0.18
            s[4] += 1
        spritzer = [s for s in spritzer if s[4] < 9]
        liste.append(bild)
    return liste
