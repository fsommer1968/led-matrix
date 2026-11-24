"""Eislaufen: zwei Läufer mit Mütze und wehendem Schal ziehen ihre Runden auf dem zugefrorenen
See, die Kufen hinterlassen helle Spuren, vorn in der Mitte springt jeder einmal; zwei Laternen
spiegeln sich im Eis, Tannen am Ufer, Lichterkette über dem See – 255 Bilder, nahtlos im Kreis.

Sparsam gezeichnet, weil die Matrix je Animation nur 80 KB speichert (Ziel ≤ 76000 Bytes,
siehe groesse.py): Jedes Bild wird einzeln und spaltenweise gepackt, darum kosten Einzelpunkte
und jede senkrechte Kante in allen 255 Bildern. Deshalb einfarbige, gleiche Tannen, neun
Lichter (abwechselnd an, aus = dunkel), kurze Kufenspuren in zwei Stufen, wenige Sterne und
Flocken, beide Laternen flackern gemeinsam.
"""
import math

from basis import (B, BUNT, GELB, GOLD, PINK, ROT, WEISS, Bild, Schnee, Sterne, dimmen, mischen)

NAME = "eislaufen"
TITEL = "Eisläufer auf dem See"

HIMMEL = (3, 0, 26)
EIS = [(50, 95, 165), (26, 58, 125)] + [(20, 48, 110)] * 4     # Zeile 10–15
SPUR = (170, 215, 255)
TANNE = (0, 135, 35)
MAST = (75, 75, 95)
LATERNEN = (12, 51)
# Lichterkette: zwei Lichter sitzen auf den Laternen (beide im gleichen Blinktakt, dann sind die
# Laternenspalten gleich), zwei in den Lücken zwischen den Tannen
LICHTER = (5, 12, 19, 25, 32, 38, 44, 51, 58)
STERNE = Sterne(anzahl=2, saat=61, y_max=3)
SCHNEE = Schnee(anzahl=3, saat=62, farbe=(110, 120, 170))

LAEUFER = [  # schaut nach rechts, 6 breit, 9 hoch
    [   # Abstoß: hinteres Bein gestreckt
        "..mm..",
        "..mmm.",
        "..hh..",
        "ssjjj.",
        "..jj.j",
        "..jj..",
        "..bb..",
        ".b..b.",
        "b...bb",
    ],
    [   # Gleiten: Beine zusammen
        "..mm..",
        "..mmm.",
        "..hh..",
        ".sjjj.",
        "s.jjj.",
        "..jj..",
        "..bb..",
        "..bb..",
        "..bbb.",
    ],
    [   # Sprung: Arme hoch, Beine angezogen
        "..mm..",
        "j.mmmj",
        "j.hh.j",
        ".jjjj.",
        "s.jj..",
        "s.jj..",
        ".bbbb.",
        ".b..b.",
        "......",
    ],
]
PAARE = (  # Mütze, Jacke, Schal, Hose
    (ROT, (0, 110, 255), GELB, (120, 90, 200)),
    (PINK, (0, 200, 90), WEISS, (200, 110, 40)),
)


def kette_y(x):
    """Lichterkette hängt in drei Bögen zwischen Bildrand und Laternen."""
    for a, b, tief in ((-9, LATERNEN[0], 2), (LATERNEN[0], LATERNEN[1], 3), (LATERNEN[1], B + 8, 2)):
        if a <= x <= b:
            u = (x - a) / (b - a)
            return round(tief * 4 * u * (1 - u))
    return 0


def kulisse(bild, f):
    STERNE.zeichnen(bild, f)
    for tx, hoch in ((2, 5), (8, 5), (55, 5), (61, 5)):               # Tannen am Ufer, alle gleich
        for k in range(hoch):
            halb = (k + 1) // 2
            bild.rechteck(tx - halb, 10 - hoch + k, 2 * halb + 1, 1, TANNE)
    SCHNEE.zeichnen(bild, f)
    for zeile, farbe in enumerate(EIS):                               # See
        bild.rechteck(0, 10 + zeile, B, 1, farbe)
    for lx in LATERNEN:                                               # Laternen mit Schein
        bild.rechteck(lx, 4, 1, 6, MAST)
        flacker = 1.0 if (f // 9) % 7 else 0.8                         # beide gemeinsam
        bild.rechteck(lx - 1, 2, 3, 2, dimmen(GOLD, 0.75 * flacker))
        bild.setze(lx, 2, dimmen((255, 240, 150), flacker))
        bild.setze(lx, 3, dimmen((255, 240, 150), flacker))
        bild.setze(lx, 1, MAST)
        for k, y in enumerate((10, 11, 12, 13)):                      # Spiegelung im Eis, schimmert
            if k < 3 + (f // 6) % 2:
                bild.setze(lx, y, mischen(EIS[y - 10], GOLD, 0.55 - k * 0.12))
    for i, x in enumerate(LICHTER):                                   # Lichterkette
        an = (i + f // 12) % 2 != 0
        farbe = GELB if x in LATERNEN else BUNT[(i * 2) % len(BUNT)]
        bild.setze(x, kette_y(x), farbe if an else None)


def bilder():
    liste = []
    spuren = {}
    # Vorlauf, damit die Spuren am Anfang schon liegen (nahtloser Kreis)
    for f in list(range(255 - 60, 255)) + list(range(255)):
        bild = Bild(HIMMEL)
        kulisse(bild, f)
        for (x, y), alter in list(spuren.items()):                    # Kufenspuren verblassen
            if 10 <= y <= 15:
                bild.setze(x, y, mischen(SPUR, EIS[y - 10], (0.0 if alter < 7 else 0.5)))
            spuren[(x, y)] = alter + 1
            if alter > 13:
                del spuren[(x, y)]
        figuren = []
        for i, (muetze, jacke, schal, hose) in enumerate(PAARE):
            w = 2 * math.pi * 2 * f / 255 + i * 0.75 * math.pi
            x = 29 + round(21 * math.cos(w))
            fuss = 13 + round(1.6 * math.sin(w))                      # Zeile der Kufen
            rechts = math.sin(w) < 0
            vorn = (w / (2 * math.pi) - 0.25) % 1                     # 0 = vorn in der Mitte
            t = vorn * 127.5 if vorn < 0.5 else (vorn - 1) * 127.5    # Bilder vor/nach der Mitte
            hoch = 0
            if -6 <= t <= 6:                                          # Sprung
                hoch = round(3 * math.cos(t / 6 * math.pi / 2))
                figur = LAEUFER[2]
            else:
                figur = LAEUFER[0] if (f // 7 + i) % 2 == 0 else LAEUFER[1]
                spuren[(x + (2 if rechts else 3), fuss)] = 0
            figuren.append((fuss, x, hoch, figur, rechts, t,
                            {"m": muetze, "h": (255, 190, 140), "j": jacke, "s": schal, "b": hose}))
        for fuss, x, hoch, figur, rechts, t, farben in sorted(figuren, key=lambda z: z[0]):
            bild.figur(x, fuss - 8 - hoch, figur, farben, spiegeln=not rechts)
            if -6 <= t <= 8:                                          # Glitzer beim Sprung
                for k in range(3):
                    if (f + k) % 3 != 0:
                        bild.setze(x + (-2, 7, 2)[k] + (f + k) % 2, fuss - 3 + k - (f + k) % 3, WEISS)
        liste.append(bild)
    return liste[60:]
