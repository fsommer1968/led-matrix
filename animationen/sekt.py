"""Sekt: die Flasche wird geschüttelt und schräg gehalten, der Korken knallt und fliegt quer durchs
Bild, Schaum spritzt; dann schenkt die Flasche zwei Gläser ein, die Gläser heben sich, stoßen
dreimal an (Funken, Perlen steigen), die Szene rückt nach links und groß erscheint "PROST" –
255 Bilder.
"""
import math
import random

from basis import B, GELB, GOLD, SCHRIFT, WEISS, Bild, dimmen, mischen
from feuerwerk import jedes_bild_anders

NAME = "sekt"
TITEL = "Sektkorken knallt, Gläser stoßen an"

HINTERGRUND = (10, 0, 20)
SEKT = (255, 200, 40)
SCHAUM = (255, 245, 210)
GLAS = (150, 190, 255)
KORK = (230, 150, 70)

# Flasche 7×13 (oben zwei Zeilen für den Korken); f Glas, h Glanz, g Goldfolie, e Etikett, r Banderole
FLASCHE = ["..ccc..", "..ccc..", "..ggg..", "..ggg..", "..fff..", "..hff..", ".fhfff.", "fhfffff", "fheeeef",
           "fhrrrrf", "fheeeef", "fhfffff", "fffffff"]
FLASCHE_FARBEN = {"f": (0, 150, 50), "h": (110, 240, 130), "g": GOLD, "e": (255, 240, 200), "r": (230, 0, 40),
                  "c": KORK}
GLAS_FORM = ["G.....G", "G.....G", "G.....G", "G.....G", ".G...G.", "..GGG..", "...G...", "...G...", "...G...",
             ".GGGGG."]

# Ablauf (Bildnummern)
ZIELEN = 34                                     # Flasche neigt sich zum Schuss
KNALL = 46
WEG1, GIESST1, WEG2, GIESST2, ZURUECK, STEHT = 62, 74, 92, 99, 117, 130
HEBEN = 134
STOESSE = (146, 164, 182, 222, 242)             # Bilder, in denen die Gläser sich treffen
RUECKEN = (194, 208)                            # Szene rückt nach links
SCHRIFT_AB = 206
VERSATZ = 28

FLASCHE_X, FLASCHE_Y = 17.5, 9.5                # Mitte der stehenden Flasche
GLAS_X = (38, 46)                               # linke Kante = x - 3


def flasche(bild, cx, cy, winkel, offen, ox=0):
    """Dreht das Flaschenbild um seine Mitte (cx, cy); winkel in Grad im Uhrzeigersinn.
    Je Pixel neun Proben, die Mehrheit entscheidet – das hält die Kanten beim Drehen ruhig."""
    w = math.radians(winkel)
    co, si = math.cos(w), math.sin(w)
    for y in range(int(cy) - 8, int(cy) + 9):
        for x in range(int(cx) - 8, int(cx) + 9):
            treffer = {}
            for py in (0.17, 0.5, 0.83):
                for px in (0.17, 0.5, 0.83):
                    dx, dy = x + px - cx, y + py - cy
                    sx = math.floor(dx * co + dy * si + 3.5)
                    sy = math.floor(-dx * si + dy * co + 6.5)
                    if 0 <= sx < 7 and 0 <= sy < 13:
                        c = FLASCHE[sy][sx]
                        if c != "." and not (c == "c" and offen):
                            treffer[c] = treffer.get(c, 0) + 1
            if sum(treffer.values()) >= 5:
                bild.setze(x - ox, y, FLASCHE_FARBEN[max(treffer, key=treffer.get)])


def muendung(cx, cy, winkel, abstand=4.5):
    w = math.radians(winkel)
    return cx + abstand * math.sin(w), cy - abstand * math.cos(w)


def glas(bild, x, y, fuell, neigung=0, perle=None, ox=0):
    """Sektkelch, linke obere Ecke (x, y); fuell 0..4 Zeilen; neigung schert den Kelch (± Pixel am Rand)."""
    for r, zeile in enumerate(GLAS_FORM):
        v = round(neigung * (9 - r) / 9)
        if 1 <= r <= 4 and r > 4 - fuell:
            for c in range(1, 6):
                if zeile[c] == "." and (r < 4 or 2 <= c <= 4):
                    oben = r == 5 - fuell
                    bild.setze(x + c + v - ox, y + r, SCHAUM if oben and fuell < 4 else SEKT)
        for c, p in enumerate(zeile):
            if p == "G":
                bild.setze(x + c + v - ox, y + r, GLAS)
    if perle is not None and fuell >= 4:                           # eine Perle steigt auf
        r = 4 - perle[1]
        v = round(neigung * (9 - r) / 9)
        bild.setze(x + perle[0] + v - ox, y + r, WEISS)


def weich(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def zwischen(a, b, t):
    return tuple(p + (q - p) * weich(t) for p, q in zip(a, b))


def flaschenlage(f):
    """(cx, cy, winkel) der Flasche im Bild f."""
    steht = (FLASCHE_X, FLASCHE_Y, 0)
    schuss = (FLASCHE_X, 8.5, 45)
    giessen = [(GLAS_X[i] + 0.5 - 4.5, 3.5, 90) for i in (0, 1)]
    if f < ZIELEN:                                                 # schütteln, zweimal
        for von, bis in ((4, 15), (19, 31)):
            if von <= f < bis:
                staerke = math.sin(math.pi * (f - von) / (bis - von))
                return (FLASCHE_X + 1.2 * staerke * math.sin(f * 2.1), FLASCHE_Y - staerke,
                        16 * staerke * math.sin(f * 2.1))
        return steht
    if f < WEG1:
        return zwischen(steht, schuss, (f - ZIELEN) / 8)
    if f < GIESST1:
        return zwischen(schuss, giessen[0], (f - WEG1) / (GIESST1 - WEG1 - 2))
    if f < WEG2:
        return giessen[0]
    if f < GIESST2:
        return zwischen(giessen[0], giessen[1], (f - WEG2) / (GIESST2 - WEG2 - 1))
    if f < ZURUECK:
        return giessen[1]
    return zwischen(giessen[1], steht, (f - ZURUECK) / (STEHT - ZURUECK))


def fett_text(bild, x, y, text, farbe):
    """5×7-Schrift doppelt hoch und einen Pixel fetter (6 breit, 1 Abstand)."""
    for i, z in enumerate(text):
        c = farbe(i) if callable(farbe) else farbe
        if c is None:
            continue
        for gy, zeile in enumerate(SCHRIFT[z]):
            for gx, p in enumerate(zeile):
                if p == "1":
                    bild.rechteck(x + i * 7 + gx, y + gy * 2, 2, 2, c)


def stern(bild, x, y, k):
    """Klirr-Funken am Treffpunkt der Gläser, k = Bilder seit dem Stoß."""
    if k == 0:
        bild.setze(x, y, WEISS)
    for d, (dx, dy) in enumerate(((0, -1), (1, -1), (-1, -1), (2, 0), (-2, 0), (1, 1), (-1, 1))):
        r = 1 + k
        if k < 5:
            bild.setze(x + dx * r, y + dy * r * 0.8, dimmen(WEISS if (d + k) % 2 else GELB, 1 - k * 0.18))


def bilder():
    z = random.Random(31)
    schaum = []
    korken = None
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        ox = round(VERSATZ * weich((f - RUECKEN[0]) / (RUECKEN[1] - RUECKEN[0])))

        # ── Gläser ──
        fuell = [0, 0]
        for i, start in enumerate((GIESST1, GIESST2)):
            fuell[i] = max(0, min(4, (f - start - 3) // 3))
        heben = weich((f - HEBEN) / 8)
        neigung = 0.0
        for s in STOESSE:
            k = f - s
            if -5 <= k < 0:
                neigung = max(neigung, weich((k + 5) / 4))
            elif 0 <= k < 3:
                neigung = 1.0
            elif 3 <= k < 9:
                neigung = max(neigung, 1 - weich((k - 3) / 6))
        for i in (0, 1):
            seite = -1 if i == 0 else 1
            gx = GLAS_X[i] - 3 + round(seite * (2 if i == 0 else 1) * heben)
            gy = 6 - round(2 * heben)
            perle = ((f // 3 + i * 2) % 3 + 2, (f // 2 + i * 3) % 5) if f >= HEBEN else None
            glas(bild, gx, gy, fuell[i], neigung=-seite * 2 * neigung, perle=perle, ox=ox)
        for s in STOESSE:
            if 0 <= f - s < 5:
                stern(bild, 42 - ox, 3, f - s)

        # ── Flasche, Strahl, Schaum, Korken ──
        cx, cy, winkel = flaschenlage(f)
        offen = f >= KNALL
        if KNALL - 6 <= f < KNALL:                                 # der Korken drückt heraus
            cx += (f % 2) * 0.6
        for i, (start, ende) in enumerate(((GIESST1, WEG2), (GIESST2, ZURUECK))):
            if start <= f < ende - 2:                              # Sektstrahl ins Glas
                oben = 6
                unten = min(10 - fuell[i], oben + (f - start) * 2)
                for y in range(oben, unten + 1):
                    bild.setze(GLAS_X[i] - ox, y, SEKT if (y + f) % 3 else SCHAUM)
        flasche(bild, cx, cy, winkel, offen, ox=ox)
        mx, my = muendung(cx, cy, winkel)
        w = math.radians(winkel)
        if f == KNALL:
            korken = [mx + 1.0 * math.sin(w), my - 1.0 * math.cos(w), 2.0, -0.6]     # flache Bahn, bleibt im Bild
        if KNALL <= f < KNALL + 5:                                 # Knall: Strahlenkranz an der Mündung
            k = f - KNALL
            for a in range(-2, 3):
                ww = w + a * 0.55
                for r in (2 + k, 3 + k):
                    bild.setze(mx + r * math.sin(ww) - ox, my - r * math.cos(ww),
                               dimmen(WEISS if (a + k) % 2 else GELB, 1 - k * 0.15))
        if KNALL <= f < KNALL + 24:                                # Schaum spritzt, lässt nach
            for _ in range(3 if f < KNALL + 12 else 1):
                ww = w + z.uniform(-0.45, 0.45)
                tempo = z.uniform(0.6, 1.5) * (1 if f < KNALL + 12 else 0.6)
                schaum.append([mx, my, tempo * math.sin(ww), -tempo * math.cos(ww), 11])
        for s in schaum:
            bild.setze(s[0] - ox, s[1], dimmen(SCHAUM, min(1, s[4] / 7)))
            s[0] += s[2]
            s[1] += s[3]
            s[3] += 0.1
            s[4] -= 1
        schaum = [s for s in schaum if s[4] > 0 and s[1] < 16]
        if korken:
            bild.rechteck(round(korken[0]) - 1 - ox, round(korken[1]) - 1, 3, 2, KORK)
            bild.setze(round(korken[0]) - ox, round(korken[1]) - 1, mischen(KORK, WEISS, 0.4))
            korken[0] += korken[2]
            korken[1] += korken[3]
            korken[3] += 0.07
            if korken[1] > 18 or korken[0] > B + 2:
                korken = None

        # ── PROST ──
        if f >= SCHRIFT_AB:
            def farbe(i):
                t = f - SCHRIFT_AB - i * 3
                if t < 0:
                    return None
                if t < 2:
                    return WEISS
                return mischen(GOLD, GELB, round(2 + 2 * math.sin(f / 3.5 - i * 1.2)) / 4)
            fett_text(bild, 30, 1, "PROST", farbe)
        liste.append(bild)
    return jedes_bild_anders(liste, HINTERGRUND)
