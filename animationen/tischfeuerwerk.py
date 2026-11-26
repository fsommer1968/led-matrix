"""Tischfeuerwerk: festlich gedeckter Silvestertisch (dunkle Decke mit Goldsaum, zwei Sektgläser,
eine Kerze), in der Mitte eine bunt gestreifte Tischbombe. Eine Hand hält ein Streichholz an die
Lunte, Funken laufen sie entlang, dann – Puff – platzt die Bombe auf: Konfetti und Luftschlangen
fliegen hoch und regnen herab, Hufeisen, Kleeblatt und Glücksschwein purzeln auf den Tisch, Glitzer
funkelt. Zum Schluss fegt eine Hand alles vom Tisch und schiebt eine neue Tischbombe hin –
255 Bilder, die Runde schließt ohne Sprung.

Sparsam gezeichnet: Jedes Bild wird einzeln und spaltenweise komprimiert. Darum einfarbiger
Grund, Decke und Saum über die ganze Breite gleich, die Bombe quer gestreift (alle Spalten gleich),
beide Gläser gleich, waagerechte Arme (gleiche Spalten) und nur so viel Konfetti, wie der Speicher
hergibt.
"""
import math
import random

from basis import (B, BLAU, GELB, GOLD, HAUT, HELLBLAU, HELLGRUEN, NACHTBLAU, ORANGE, PINK, ROT, TUERKIS,
                   WEISS, Bild)

NAME = "tischfeuerwerk"
TITEL = "Tischfeuerwerk"

DECKE = (105, 0, 30)                           # dunkle Tischdecke (Zeilen 13 und 14)
SAUM = (190, 112, 0)                           # Goldsaum (Zeile 15)
GLAS = (150, 190, 255)
SEKT = (255, 200, 40)
WACHS = (230, 220, 190)
LUNTE_FARBE = (130, 130, 120)
HOLZ = (170, 150, 110)                         # Streichholz
AERMEL = (0, 25, 105)                          # Ärmel: große Fläche, darum gedämpft
SCHWEIN = (255, 70, 140)
RUESSEL = (255, 160, 190)
KLEE = (0, 220, 40)
KLEE_MITTE = (0, 110, 25)
EISEN = (255, 190, 0)
GLITZER = (120, 120, 140)
LILA = (170, 0, 255)

BODEN = 12                                     # unterste Zeile über dem Tisch
BOMBE_X = 29                                   # linke Kante der Tischbombe (7 breit, Zeilen 6 bis 12)
GLAESER = (5, 13)                              # linke Kanten der beiden Gläser (5 breit)
KERZE_X = 58                                   # linke Kante der Kerze (3 breit)

# Ablauf (Bildnummern)
HAND_KOMMT, HAND_DA, HAND_GEHT, HAND_WEG = 8, 30, 40, 52
LUNTE_AB, PUFF = 36, 82
FEGEN_AB, FEGEN_BIS, ARM_WEG = 188, 216, 228
NEU_AB, NEU_STEHT, NEU_WEG = 220, 244, 252

BOMBE = [".ggggg.", "rrrrrrr", "yyyyyyy", "bbbbbbb", "nnnnnnn", "ppppppp", "ggggggg"]
GEPLATZT = ["g.....g", "r.r.r.r", "yyyyyyy", "bbbbbbb", "nnnnnnn", "ppppppp", "ggggggg"]
BOMBE_FARBEN = {"g": GOLD, "r": ROT, "y": GELB, "b": BLAU, "n": HELLGRUEN, "p": PINK}
# Lunte vom Deckel bis zur Spitze (bezogen auf die linke Kante der Bombe)
LUNTE = [(3, 5), (3, 4), (4, 3), (5, 2), (6, 2), (7, 2), (8, 3)]

GLAS_FORM = ["G...G", "GsssG", "GsssG", "GsssG", ".GsG.", "..G..", "..G..", ".GGG."]

HUFEISEN = [".xxx.", "x...x", "x...x", "x...x", "xx.xx"]
KLEEBLATT = ["xx.xx", "xxdxx", ".ddd.", "xxdxx", "xx.xx"]
SCHWEINCHEN = ["..e....", ".ppppp.", "nappppt", "nppppp.", ".p..p.."]
# Glücksbringer: Form, Farben, Ruheplatz (linke Kante), Flugdauer
BRINGER = [(HUFEISEN, {"x": EISEN}, 22, 24),
           (KLEEBLATT, {"x": KLEE, "d": KLEE_MITTE}, 39, 29),
           (SCHWEINCHEN, {"p": SCHWEIN, "e": SCHWEIN, "t": SCHWEIN, "n": RUESSEL, "a": (20, 0, 10)}, 47, 34)]

# Luftschlangen: Farbe, Gipfel des Flugs, Dauer des Herabsinkens, Ruheform (von oben nach unten),
# Zahl der Punkte, die als Haken über dem Glasrand bzw. Bombenrand liegen
SCHLANGEN = [(PINK, (23, 0), 34, [(16, 4), (17, 4), (18, 5), (18, 6), (19, 7), (18, 8), (18, 9), (19, 10)], 2),
             (TUERKIS, (8, 0), 44, [(6, 4), (5, 4), (4, 5), (4, 6), (3, 7), (4, 8), (4, 9), (3, 10)], 2),
             (LILA, (41, 0), 26, [(35, 5), (36, 6), (36, 7), (37, 8), (36, 9), (36, 10), (37, 11)], 1)]
STEIGT = 9                                     # so viele Bilder schießt eine Luftschlange hoch

KONFETTI_FARBEN = [ROT, GELB, HELLBLAU, PINK, HELLGRUEN, ORANGE, TUERKIS, LILA]
KONFETTI = 32


def weich(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def gedreht(zeilen, viertel):
    """Dreht eine Form um Vierteldrehungen (für das Purzeln)."""
    for _ in range(viertel % 4):
        zeilen = ["".join(zeilen[len(zeilen) - 1 - y][x] for y in range(len(zeilen)))
                  for x in range(len(zeilen[0]))]
    return zeilen


def belegt(x):
    """Spalten, in denen etwas auf dem Tisch steht oder liegen wird (dort bleibt kein Konfetti liegen)."""
    if any(g <= x < g + 5 for g in GLAESER) or BOMBE_X <= x < BOMBE_X + 7 or KERZE_X - 1 <= x < KERZE_X + 4:
        return True
    return any(x0 <= x < x0 + len(form[0]) for form, _, x0, _ in BRINGER)


def konfetti_bahnen():
    """Bahn jedes Konfettis: schneller Stoß nach oben, dann langsames Herabtrudeln (Luftwiderstand).
    Liefert je Stück (Farbe, {Bild: (x, y)}, Landebild oder None, Lande-x)."""
    z = random.Random(12)
    liste = []
    faecher = list(range(KONFETTI))
    z.shuffle(faecher)                                               # gleichmäßig über die Breite gestreut
    for i in range(KONFETTI):
        start = PUFF + 1 + z.randrange(5)
        x, y = BOMBE_X + 3.0, 5.0
        vx = -4.3 + 8.6 * (faecher[i] + z.random()) / KONFETTI
        vy = z.uniform(-2.3, -0.5)
        g = z.uniform(0.032, 0.05)
        phase = z.randrange(40)
        bahn, landung, lx = {}, None, None
        for f in range(start, FEGEN_AB):
            x, y = x + vx, y + vy
            vx, vy = vx * 0.85, vy * 0.85 + g
            xi = round(x + (math.sin((f + phase) / 5.0) if vy > 0 else 0))
            if y >= BODEN:
                landung, lx = f, xi
                break
            bahn[f] = (xi, round(y))
        if lx is not None and (belegt(lx) or not 0 <= lx < B):
            lx = None                                                # fällt hinter Glas, Bombe oder Figur
        liste.append((KONFETTI_FARBEN[i % len(KONFETTI_FARBEN)], bahn, landung, lx))
    return liste


def glas(bild, x, f, versatz):
    bild.figur(x, 5, GLAS_FORM, {"G": GLAS, "s": SEKT})
    stufe = ((f + versatz) // 5) % 3                                 # eine Perle steigt auf
    bild.setze(x + 2, 8 - stufe, WEISS)


def kerze(bild, f):
    bild.rechteck(KERZE_X - 1, 12, 5, 1, GOLD)
    bild.rechteck(KERZE_X, 9, 3, 3, WACHS)
    neigung = (0, 0, 1, 0, -1)[(f // 3) % 5]
    bild.setze(KERZE_X + 1, 8, GELB)
    bild.setze(KERZE_X + 1 + neigung, 7, ORANGE)


def bombe(bild, x, geplatzt=False, lunte_bis=len(LUNTE)):
    bild.figur(x, 6, GEPLATZT if geplatzt else BOMBE, BOMBE_FARBEN)
    if not geplatzt:
        for dx, y in LUNTE[:lunte_bis]:
            bild.setze(x + dx, y, LUNTE_FARBE)


def luftschlange(f, farbe, gipfel, sinkt, form, haken, schub):
    """Punkte einer Luftschlange im Bild f: erst als Strich hochgeschossen, dann sinkt sie
    zappelnd herab und bleibt mit dem Haken über dem Rand hängen."""
    t = f - (PUFF + 1)
    if t < 0:
        return []
    sx, sy = BOMBE_X + 3, 5
    if t < STEIGT:                                                   # schießt hoch
        punkte = []
        for k in range(4):
            a = 1 - (1 - max(0, t - k) / STEIGT) ** 2
            punkte.append((round(sx + (gipfel[0] - sx) * a), round(sy + (gipfel[1] - sy) * a)))
        return punkte
    haengt = form[haken:]
    u = (t - STEIGT) / sinkt
    if u >= 1:
        return [(x + schub, y) for x, y in form]
    dx = (gipfel[0] - haengt[0][0]) * (1 - weich(u))
    dy = (gipfel[1] - haengt[0][1]) * (1 - u)
    achse = min(x for x, _ in haengt)
    zappelt = (t // 4) % 2
    laenge = min(len(haengt), 3 + (t - STEIGT) // 3)                 # rollt sich ab
    return [(round((2 * achse + 1 - x if zappelt else x) + dx), round(y + dy)) for x, y in haengt[:laenge]]


def bilder():
    bahnen = konfetti_bahnen()
    z = random.Random(5)
    funken_zufall = [(z.choice([-1, 1, 2, -2]), z.choice([-1, -2, 0]), z.choice([-1, 0, 1]), z.choice([-2, -1]))
                     for _ in range(255)]
    glitzer = [(3 + (k * 23) % 58, 1 + (k * 5) % 7, PUFF + 12 + k * 8) for k in range(11)]
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        bild.rechteck(0, 13, B, 2, DECKE)
        bild.rechteck(0, 15, B, 1, SAUM)
        kerze(bild, f)
        for i, x in enumerate(GLAESER):
            glas(bild, x, f, i * 7)

        # ── Fegen: Front der Hand, davor das Konfettihäufchen, davor alles Geschobene ──
        fegt = FEGEN_AB <= f < ARM_WEG
        if f < FEGEN_AB:
            front = -99
        elif f < FEGEN_BIS:
            front = round(-3 + (f - FEGEN_AB) * 72 / (FEGEN_BIS - FEGEN_AB))
        else:
            front = 99
        kette = front + 3                                            # rechts vom Häufchen

        def geschoben(x0, breite):
            nonlocal kette
            if x0 < kette:
                x0 = kette
                kette = x0 + breite
            return x0

        # ── Tischbombe und Glücksbringer, von links nach rechts (Reihenfolge der Kette) ──
        t = f - (PUFF + 1)
        stuecke = []                                                 # (x, y, Form, Farben)
        bomben_schub = 0
        dinge = [BRINGER[0], None, BRINGER[1], BRINGER[2]]           # None = die Bombe
        for ding in dinge:
            if ding is None:
                if PUFF <= f < FEGEN_BIS:
                    bomben_schub = geschoben(BOMBE_X, 9) - BOMBE_X    # samt Luftschlange
                    bombe(bild, BOMBE_X + bomben_schub, geplatzt=f > PUFF, lunte_bis=0)
                continue
            form, farben, ziel, dauer = ding
            if t < 0 or f >= FEGEN_BIS:
                continue
            if t < dauer:                                            # Flug im Bogen, purzelnd
                g = 46 / dauer ** 2                                  # Gipfel knapp am oberen Bildrand
                vy = (8 - 3) / dauer - g * dauer / 2
                x = BOMBE_X + 1 + (ziel - BOMBE_X - 1) * t / dauer
                stuecke.append((round(x), round(3 + vy * t + g * t * t / 2), gedreht(form, t // 4), farben))
            elif t < dauer + 8:                                      # hüpft einmal auf
                stuecke.append((ziel, 8 - round(2 * math.sin(math.pi * (t - dauer) / 8)), form, farben))
            else:
                stuecke.append((geschoben(ziel, len(form[0])), 8, form, farben))
        if f < PUFF:
            brennt = 0
            if f >= LUNTE_AB:
                brennt = min(len(LUNTE) - 1, (f - LUNTE_AB) * len(LUNTE) // (PUFF - LUNTE_AB))
            rest = len(LUNTE) - brennt
            bombe(bild, BOMBE_X, lunte_bis=rest)
            if f >= LUNTE_AB:                                        # Funken an der Brennstelle
                dx, y = LUNTE[rest - 1]
                x = BOMBE_X + dx
                a, b, c, d = funken_zufall[f]
                bild.setze(x, y, WEISS if f % 2 else GELB)
                bild.setze(x + a, y + b, ORANGE)
                if f % 3:
                    bild.setze(x + c, y + d, GELB)
        if f >= NEU_AB:                                              # neue Bombe wird hingeschoben
            x_neu = BOMBE_X + round(36 * (1 - weich((f - NEU_AB) / (NEU_STEHT - NEU_AB))))
            bombe(bild, x_neu)

        # ── Luftschlangen ──
        if f < FEGEN_BIS:
            for i, (farbe, gipfel, sinkt, form, haken) in enumerate(SCHLANGEN):
                an_bombe = i == 2
                if not an_bombe and min(x for x, _ in form) < kette:  # weggefegt
                    continue
                for x, y in luftschlange(f, farbe, gipfel, sinkt, form, haken, bomben_schub if an_bombe else 0):
                    bild.setze(x, y, farbe)

        for x, y, form, farben in stuecke:
            bild.figur(x, y, form, farben)

        # ── Puff ──
        u = f - PUFF
        mx, my = BOMBE_X + 3, 5
        if u == 0:
            bild.kreis(mx, my, 1.5, WEISS)
        elif u == 1:
            bild.kreis(mx, my, 3, GELB)
            bild.kreis(mx, my, 1.5, WEISS)
        elif u in (2, 3):
            r = 3 + u
            for k in range(8):
                w = k * math.pi / 4 + 0.4
                bild.setze(mx + r * math.cos(w), my - abs(r * 0.8 * math.sin(w)), ORANGE if u == 3 else GELB)

        # ── Konfetti ──
        haufen = []
        for farbe, bahn, landung, lx in bahnen:
            if f in bahn:
                bild.setze(bahn[f][0], bahn[f][1], farbe)
            elif landung is not None and f >= landung and lx is not None:
                if lx < kette:
                    haufen.append(farbe)
                else:
                    bild.setze(lx, BODEN, farbe)
        if FEGEN_AB <= f < FEGEN_BIS:
            plaetze = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
            for (dx, dy), farbe in zip(plaetze, haufen):
                bild.setze(front + dx, BODEN - dy, farbe)

        # ── Glitzer: blitzt kurz als Kreuz auf ──
        for x, y, start in glitzer:
            u = f - start
            if 0 <= u < 6 and f < FEGEN_AB:
                if u in (2, 3):
                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        bild.setze(x + dx, y + dy, GLITZER)
                bild.setze(x, y, WEISS if 1 <= u < 5 else GLITZER)

        # ── Hand mit Streichholz (von rechts) ──
        if HAND_KOMMT <= f < HAND_WEG:
            if f < HAND_DA:
                weg = 1 - weich((f - HAND_KOMMT) / (HAND_DA - HAND_KOMMT))
            elif f < HAND_GEHT:
                weg = 0
            else:
                weg = weich((f - HAND_GEHT) / (HAND_WEG - HAND_GEHT))
            hx = BOMBE_X + 13 + round(weg * 26)
            bild.rechteck(hx, 2, 4, 3, HAUT)
            bild.rechteck(hx + 4, 2, 1, 3, WEISS)
            bild.rechteck(hx + 5, 2, B, 3, AERMEL)
            bild.rechteck(hx - 3, 3, 3, 1, HOLZ)
            bild.setze(hx - 4, 3, GELB)
            bild.setze(hx - 4, 2, ORANGE if f % 2 else GELB)

        # ── Hand fegt den Tisch ab (von links) ──
        if fegt:
            if f < FEGEN_BIS:
                hand = front
            else:
                hand = round(67 - (f - FEGEN_BIS) * 75 / (ARM_WEG - FEGEN_BIS))
            bild.rechteck(hand - 3, 8, 2, 1, HAUT)                   # flache Hand, Fingerspitzen oben
            bild.rechteck(hand - 3, 9, 3, 4, HAUT)
            bild.rechteck(hand - 4, 9, 1, 3, WEISS)
            bild.rechteck(hand - 4 - B, 9, B, 3, AERMEL)

        # ── Hand schiebt die neue Bombe hin (von rechts) ──
        if f >= NEU_AB:
            if f < NEU_STEHT:
                hx = x_neu + 7
            else:
                hx = BOMBE_X + 7 + round(30 * weich((f - NEU_STEHT) / (NEU_WEG - NEU_STEHT)))
            bild.rechteck(hx, 8, 3, 4, HAUT)
            bild.rechteck(hx + 3, 9, 1, 3, WEISS)
            bild.rechteck(hx + 4, 9, B, 3, AERMEL)
        liste.append(bild)
    return liste
