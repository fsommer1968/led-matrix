"""Bunt: Tannen, Regenbogen-Schrift, Geschenke, Lichterkette – 255 Bilder (23.11.2026).

Szenen: 1. drei Tannen wachsen, Stern funkelt, Kugeln blinken, Lichterkette im Regenbogen (75)
        2. "FROHE WEIHNACHTEN" als Regenbogen-Welle (90)
        3. bunte Geschenke fallen und stapeln sich (50)
        4. Lichterkette: Lauflicht, Blinken, Farbwechsel, ausblenden (40)
Durch alle Szenen fällt leise Schnee.
"""
import math

from basis import (B, BLAU, BRAUN, BUNT, DUNKELGRUEN, GELB, GOLD, GRUEN, HELLBLAU, HELLGRUEN,
                   LILA, ORANGE, PINK, ROT, SCHRIFT, TUERKIS, WEISS, Bild, Schnee, dimmen,
                   regenbogen)

NAME = "weihnacht_bunt"
TITEL = "Bunt: Tannen, Schrift, Geschenke, Lichterkette"
DRAHT = (40, 90, 40)

SCHNEE_FALL = Schnee()


def schnee(bild, f):
    SCHNEE_FALL.zeichnen(bild, f)


# ── Szene 1: Tannen ────────────────────────────────────────────────
TANNEN = [9, 32, 54]


def tanne_zeilen(cx):
    """{y: (x_links, x_rechts)} für Nadeln (y 2..13), dazu Stamm y 14..15."""
    z = {}
    for y in range(2, 14):
        r = y - 2
        w = r % 4 + (r // 4) * 2
        z[y] = (cx - w, cx + w)
    return z


HELL_NADEL = (30, 210, 40)
#          dx, y   (wenige, klar gesetzte Kugeln je Tanne; die Lichterkette sitzt auf y 5, 9, 13)
KUGEL_PLATZ = [(0, 4), (-1, 7), (2, 8), (-3, 11), (1, 11), (4, 12), (-1, 12)]
KUGELN = {cx: [(cx + dx, y, (n * 2 + i * 3) % len(BUNT), (n * 5 + i * 7) % 24)
               for n, (dx, y) in enumerate(KUGEL_PLATZ)]
          for i, cx in enumerate(TANNEN)}


def stern(bild, cx, g):
    """Stern auf der Spitze: Kreuz 3×3, pulsiert, ab und zu Strahlen."""
    puls = (g // 4) % 2
    for dx, dy in ((0, 0), (-1, 1), (1, 1), (0, 2)):
        bild.setze(cx + dx, dy, GELB if puls else GOLD)
    bild.setze(cx, 1, WEISS if puls else GELB)
    if g % 16 < 4:                                     # Strahlen (alle Sterne im Gleichtakt)
        for dx, dy in ((-2, 1), (2, 1), (-1, 0), (1, 0)):
            bild.setze(cx + dx, dy, dimmen(GELB, 0.6))


def szene_tannen(f):
    bild = Bild()
    schnee(bild, f)
    sichtbar_ab = max(0, 15 - f)                     # wachsen von unten (f 0..15)
    for cx in TANNEN:
        z = tanne_zeilen(cx)
        for y in (14, 15):
            if y >= sichtbar_ab:
                bild.rechteck(cx - 1, y, 3, 1, BRAUN)
        for y, (l, r) in z.items():
            if y < sichtbar_ab:
                continue
            w = r - cx
            for x in range(l, r + 1):                # links Licht, rechts Schatten
                d = x - cx
                bild.setze(x, y, HELL_NADEL if d < -w * 0.45 and w > 1 else
                           DUNKELGRUEN if d > w * 0.4 and w > 1 else GRUEN)
        if f < 16:
            continue
        g = f - 16
        # Lichterkette auf der Unterkante jeder Stufe: geht Stufe für Stufe an, Regenbogen läuft;
        # die Farben zählen ab der Baummitte – drei gleiche Ketten brauchen im Speicher der Matrix
        # (80 KB je Animation, jedes Bild einzeln gepackt) kaum mehr als eine
        for n, y in enumerate((13, 9, 5)):
            if g < n * 4:
                continue
            l, r = z[y]
            for x in range(l, r + 1):
                if (x - l) % 2 == 0:
                    bild.setze(x, y, regenbogen((x - cx) * 20 + y * 40 - g * 15))
                else:
                    bild.setze(x, y, DUNKELGRUEN)
        # Kugeln: erscheinen nacheinander, wechseln langsam die Farbe, blitzen ab und zu weiß
        for n, (x, y, farbe, phase) in enumerate(KUGELN[cx]):
            if g < 12 + n * 3:
                continue
            blitz = (g + phase) % 24 < 2
            bild.setze(x, y, WEISS if blitz else BUNT[(farbe + (g + phase) // 24) % len(BUNT)])
        stern(bild, cx, g)
    return bild


# ── Szene 2: Schrift ───────────────────────────────────────────────
TEXT = "FROHE WEIHNACHTEN"


def szene_text(f):
    bild = Bild()
    schnee(bild, f + 75)
    start = B - 2 * f                                # 2 Pixel je Bild
    # Schatten nur nach unten statt schräg: die Spalten bleiben einfach, das spart Speicher
    for schatten in (True, False):                   # erst die Schatten, dann die Buchstaben
        x = start
        for i, z in enumerate(TEXT):
            glyph = SCHRIFT[z]
            y0 = 4 + round(2.4 * math.sin((x + f * 3) / 7))
            farbe = regenbogen(i * 22 + f * 12)
            if schatten:
                farbe = dimmen(farbe, 0.28)
            for gy, zeile in enumerate(glyph):
                for gx, c in enumerate(zeile):
                    if c == "1":
                        bild.setze(x + gx, y0 + gy + schatten, farbe)
            x += len(glyph[0]) + 1
    return bild


# ── Szene 3: Geschenke ─────────────────────────────────────────────
#            x, Breite, Höhe, Paket, Band, Start, Ziel-y (Unterkante)
GESCHENKE = [(3, 8, 6, ROT, GOLD, 0, 15),
             (13, 7, 5, BLAU, PINK, 4, 15),
             (22, 9, 7, LILA, GELB, 8, 15),
             (33, 6, 5, TUERKIS, ROT, 12, 15),
             (41, 8, 6, ORANGE, BLAU, 16, 15),
             (51, 9, 7, PINK, HELLGRUEN, 20, 15),
             (23, 6, 4, GRUEN, ROT, 24, 8),           # auf dem lila Paket
             (4, 6, 4, GOLD, LILA, 28, 9),            # auf dem roten
             (52, 6, 4, HELLBLAU, GOLD, 32, 8)]       # auf dem pinken


def geschenk(bild, x, unten, b, h, paket, band, glanz):
    oben = unten - h + 1
    bild.rechteck(x, oben, b, h, paket)
    dunkel = dimmen(paket, 0.6)
    for y in range(oben, unten + 1):                 # Schattenkante rechts und unten
        bild.setze(x + b - 1, y, dunkel)
    for xx in range(x, x + b):
        bild.setze(xx, unten, dunkel)
    mx = x + b // 2
    for y in range(oben, unten + 1):
        bild.setze(mx, y, band)
    my = oben + (h - 1) // 2
    for xx in range(x, x + b):
        bild.setze(xx, my, band)
    for dx, dy in ((-2, -2), (-1, -1), (1, -1), (2, -2)):   # Schleife
        bild.setze(mx + dx, oben + dy, band)
    bild.setze(mx, oben - 1, WEISS if glanz else band)


def szene_geschenke(f):
    bild = Bild()
    schnee(bild, f + 165)
    for i, (x, b, h, paket, band, start, ziel) in enumerate(GESCHENKE):
        if f < start:
            continue
        unten = min(ziel, -2 + (f - start) * 2)       # fällt 2 Pixel je Bild
        gelandet = unten == ziel
        seit = f - start - (ziel + 2) // 2            # Bilder seit der Landung
        gestaucht = gelandet and seit < 2             # Aufprall: kurz flacher
        glanz = gelandet and (f + i * 3) % 12 < 3
        geschenk(bild, x, unten, b, h - gestaucht, paket, band, glanz)
        if gelandet and seit < 3:                     # Aufprall: Schnee stiebt zur Seite
            bild.setze(x - 1 - seit, unten - seit, WEISS)
            bild.setze(x + b + seit, unten - seit, WEISS)
    return bild


# ── Szene 4: Lichterkette ──────────────────────────────────────────
def draht_y(x):
    return 1 + 8 * math.sin(math.pi * (x % 32) / 32)


BIRNEN = [(x, round(draht_y(x)) + 2, BUNT[i % len(BUNT)]) for i, x in enumerate(range(3, B, 5))]


def szene_kette(f):
    bild = Bild()
    schnee(bild, f + 215)
    hell = 1.0 if f < 34 else (39 - f) / 6           # letzte Bilder ausblenden
    for x in range(B):
        bild.setze(x, draht_y(x), dimmen(DRAHT, hell))
    n = len(BIRNEN)
    for i, (x, y, farbe) in enumerate(BIRNEN):
        if f < 14:                                    # Lauflicht
            an = i <= f * n // 13
        elif f < 24:                                  # abwechselnd blinken
            an = (i + f // 2) % 2 == 0
        else:                                         # alle an, Farben wandern
            an = True
            farbe = BUNT[(i + (f - 24) // 2) % len(BUNT)]
        bild.setze(x, y - 1, dimmen(DRAHT, hell))     # Fassung
        birne = farbe if an else dimmen(farbe, 0.15)  # aus: nur ein Hauch Farbe
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            bild.setze(x + dx, y + dy, dimmen(birne, hell))
        if an and hell == 1.0 and f >= 24 and (i + f) % 4 == 0:
            bild.setze(x, y + 2, WEISS)                   # Funkeln
    return bild


def bilder():
    liste = [szene_tannen(f) for f in range(75)]
    liste += [szene_text(f) for f in range(90)]
    liste += [szene_geschenke(f) for f in range(50)]
    liste += [szene_kette(f) for f in range(40)]
    return liste
