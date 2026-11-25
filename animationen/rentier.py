"""Rentier mit roter Nase: großes Rentier galoppiert von links herein und bleibt stehen, die rote
Nase beginnt zu leuchten und zu strahlen, die Lichter im Geweih gehen an; am Ende galoppiert es
mit Glitzerspur nach rechts davon – 255 Bilder.

Ohne Namensschriftzug (25.11.2026): Die bekannte rotnasige Rentierfigur ist markenrechtlich geschützt;
für die Veröffentlichung bleibt das Rentier namenlos. TEXT leer lassen.

Sparsam gezeichnet, weil die Matrix je Animation nur 80 KB speichert (Ziel ≤ 76000 Bytes,
siehe groesse.py): einfarbige Tannen, wenige Sterne, die zwischendurch ganz ausgehen, die
Schrift einfarbig und so hoch, dass sie die Tannen verdeckt (Schrift über Tannen kostete
je Spalte doppelt), äußerer Nasenschein nur beim hellsten Puls, dünnere Glitzerspur.

0–23    galoppiert herein
23–50   steht, Nase glimmt auf, Geweih-Lichter gehen an
50–92   (früher Schriftzug, jetzt ohne)
92–210  Nase strahlt, Schweif wedelt, ein Freudensprung
210–255 galoppiert davon
"""
import math
import random

from basis import (B, BUNT, GOLD, NACHTBLAU, ROT, SCHNEEDECKE, WEISS, Bild, Schnee, dimmen,
                   mischen)

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "rentier"
TITEL = "Rentier mit leuchtender Nase"

FELL = (58, 30, 10)
FELL_DUNKEL = (33, 16, 5)
BAUCH = (225, 175, 110)
GEWEIH = (225, 190, 130)
HUF = (95, 75, 95)
NASE = (255, 20, 10)
TANNE = (0, 120, 32)
BODEN = (150, 160, 200)
KOERPER = [  # schaut nach rechts, 22 breit; Beine (4 Zeilen) kommen darunter
    "...........a.a..a.a...",
    "...........a.a..a.a...",
    "...........aaa..aaa...",
    "............a....a....",
    "..........ohhhhhh.....",
    "...........hhhehhhh...",
    "...........hhhhhhhh...",
    "...t........hhhhh.....",
    "...tbbbbbbbbccc.......",
    "....bbbbbbbbbwwg......",
    "....bbwwwwwwbb........",
]
BEINE = {
    "stehen": ["....ll.....ll.........", "....l.d....l.d........", "....l.d....l.d........",
               "....k.k....k.k........"],
    "strecken": ["....ll.....ll.........", "...l.d......l.d.......", "..l.d........l.d......",
                 "..k.k.........k.k....."],
    "sammeln": ["....ll.....ll.........", ".....ll...ll..........", "......ld.dl...........",
                "......k...k..........."],
    "scharren": ["....ll.....ll.........", "....l.d....l..d.......", "....l.d....l...d......",
                 "....k.k....k.........."],
}
FARBEN = {"a": GEWEIH, "h": FELL, "o": FELL_DUNKEL, "e": (15, 8, 30), "t": WEISS, "b": FELL,
          "w": BAUCH, "c": ROT, "g": GOLD, "l": FELL, "d": FELL_DUNKEL, "k": HUF}
LICHTER = ((11, 0), (13, 0), (16, 0), (18, 0))
NASE_DX, NASE_DY = 19, 5                                         # Nase 2×2 in der Figur
# Sterne von Hand verteilt (x, y, Phase, Periode): zwei links über dem Rücken (immer zu sehen),
# vier rechts (hinter der Schrift verdeckt). Jeder sichtbare Stern kostet je Bild etwa 9 Bytes.
STERNE = [(2, 1, 0, 32), (7, 4, 17, 40), (30, 2, 9, 24), (42, 5, 30, 32), (54, 1, 5, 40),
          (61, 6, 22, 24)]
SCHNEE = Schnee(anzahl=3, saat=89, farbe=(120, 130, 175))
TEXT = ""                                                        # kein Name (Markenrecht)
TEXT_X = 23
TANNEN = [(30, 5), (44, 5), (58, 5)]                               # Mitte, Höhe (alle gleich)


def sterne(bild, f):
    """Funkeln wie basis.Sterne, aber im dunklen Teil der Periode ist der Stern ganz aus."""
    for x, y, phase, periode in STERNE:
        h = 0.5 + 0.5 * math.cos(2 * math.pi * ((f + phase) % periode) / periode)
        if h >= 0.3:
            bild.setze(x, y, dimmen((255, 240, 200), round(h * 4) / 4))


def wald(bild):
    for tx, hoch in TANNEN:
        for k in range(hoch):
            halb = (k + 1) // 2
            bild.rechteck(tx - halb, 15 - hoch + k, 2 * halb + 1, 1, TANNE)
        bild.setze(tx, 14 - hoch, SCHNEEDECKE)
    bild.rechteck(0, 15, B, 1, BODEN)


def nasenschein(bild, nx, ny, staerke, strahlen, f):
    """Roter Schein um die 2×2-Nase (linke obere Ecke nx, ny); staerke 0…1 in Stufen."""
    if staerke <= 0:
        return
    for dy in range(-3, 5):
        for dx in range(-3, 5):
            d = math.hypot(dx - 0.5, dy - 0.5)
            if d < 1.0:
                continue
            anteil = 0.55 if d < 2.0 else 0.28 if d < 2.9 and staerke >= 1 else 0
            if anteil:
                bild.setze(nx + dx, ny + dy, mischen(NACHTBLAU, NASE, anteil * staerke))
    if strahlen:
        gerade = (f // 5) % 2 == 0
        for k in range(8):
            if (k % 2 == 0) != gerade:
                continue
            w = k * math.pi / 4
            for r in (3.6, 4.6):
                bild.setze(nx + 0.5 + r * math.cos(w), ny + 0.5 + r * math.sin(w),
                           dimmen(NASE, 0.75 if r < 4 else 0.4))


def rentier(bild, x, y, f, beine, nase, lichter, blinzeln, wedeln):
    farben = dict(FARBEN)
    if blinzeln:
        farben["e"] = FELL
    bild.figur(x, y, KOERPER, farben)
    bild.figur(x, y + 11, BEINE[beine], farben)
    if wedeln:                                                       # Schweif hoch
        bild.setze(x + 3, y + 7, NACHTBLAU)
        bild.setze(x + 2, y + 7, WEISS)
        bild.setze(x + 2, y + 6, WEISS)
    kern = mischen((110, 0, 0), NASE, nase)
    bild.rechteck(x + NASE_DX, y + NASE_DY, 2, 2, kern)
    if nase > 0.8:
        bild.setze(x + NASE_DX, y + NASE_DY, (255, 120, 90))         # Glanzpunkt
    for k, (dx, dy) in enumerate(LICHTER[:lichter]):                 # Geweih-Lichter
        an = (k + f // 7) % 4 != 0
        farbe = BUNT[(k * 2 + f // 28) % len(BUNT)]
        bild.setze(x + dx, y + dy, farbe if an else dimmen(farbe, 0.35))


def ohne_doppelte(liste):
    """Pillow legt gleiche Nachbarbilder im GIF zusammen – dann wären es weniger als 255 Bilder.
    Ist ein Bild gleich seinem Vorgänger, ändert ein Punkt unsichtbar die Farbe (Blau um 1)."""
    for i in range(1, len(liste)):
        if liste[i].px == liste[i - 1].px:
            r, g, b = liste[i].px[1][1]
            liste[i].px[1][1] = (r, g, b + 1 if b < 255 else b - 1)
    return liste


def bilder():
    z = random.Random(12)
    liste = []
    spur = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        sterne(bild, f)
        SCHNEE.zeichnen(bild, f)
        wald(bild)
        hoch = 0
        if f < 23:                                                   # galoppiert herein
            x, galopp = -24 + f, True
        elif f < 210:
            x, galopp = -1, False
        else:
            x, galopp = -1 + (f - 210) * 2, True
        if galopp:
            gestreckt = (f // 3) % 2 == 0
            beine = "strecken" if gestreckt else "sammeln"
            hoch = 1 if gestreckt else 0
        elif 140 <= f < 164:                                         # Freudensprung (zweimal)
            t = (f - 140) % 12
            hoch = (0, 1, 2, 3, 3, 3, 2, 1, 0, 0, 0, 0)[t]
            beine = "sammeln" if hoch >= 2 else "stehen"
        elif 100 <= f < 124 and (f // 6) % 2 == 0:                   # scharrt mit dem Huf
            beine = "scharren"
        else:
            beine = "stehen"
        # Nase: glimmt auf (23–50), pulsiert, strahlt ab 92 im Wechsel
        if f < 23:
            nase, strahlen = 0.4, False
        elif f < 50:
            nase, strahlen = 0.4 + 0.6 * round((f - 23) / 27 * 4) / 4, False
        elif f < 210:
            nase = (1.0, 0.8, 0.6, 0.8)[(f // 5) % 4]
            strahlen = f >= 92 and (f // 20) % 2 == 0
        else:
            nase, strahlen = 1.0, False
        lichter = 0 if f < 30 else min(4, (f - 30) // 5 + 1)
        nasenschein(bild, x + NASE_DX, NASE_DY - hoch, nase if f >= 23 else 0.5, strahlen, f)
        # Schriftzug (leer): erschiene ab 50; beim Davongaloppieren nimmt die Nase die Buchstaben mit
        if f >= 50:
            n = min(len(TEXT), (f - 50) // 6 + 1)
            for i in range(n):
                bx = TEXT_X + i * 6
                if galopp and f >= 210 and bx < x + NASE_DX + 2:
                    continue
                neu = f - (50 + i * 6)
                farbe = WEISS if neu < 3 else (GOLD if (f // 8) % 4 == 0 else ROT)   # ganzes Wort
                bild.rechteck(bx - 1, 0, 7, 15, NACHTBLAU)            # Sterne/Schnee/Tannen dahinter weg
                bild.text(bx, 1, TEXT[i], farbe, hoch=2)
        if galopp and f >= 210:                                      # Glitzerspur, ein Funke je Bild
            spur.append([x + z.randrange(1, 5), 5 + z.randrange(0, 9), z.randrange(len(BUNT)), 0])
        for s in spur:
            if s[3] < 12:
                bild.setze(s[0], s[1], dimmen(BUNT[s[2]] if s[3] % 4 < 3 else WEISS, 1 - s[3] / 14))
            s[1] += 0.25
            s[3] += 1
        spur = [s for s in spur if s[3] < 12]
        blinzeln = not galopp and f % 47 in (0, 1, 2)
        wedeln = not galopp and 60 <= f and (f // 4) % 6 == 0
        rentier(bild, x, 0 - hoch, f, beine, nase, lichter, blinzeln, wedeln)
        liste.append(bild)
    return ohne_doppelte(liste)
