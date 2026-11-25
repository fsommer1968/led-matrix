"""Gemeinsame Bausteine für die Animationen der Matrix 64×16.

Jede Animation ist ein Modul mit NAME (Dateiname ohne _64x16.gif), TITEL und bilder() → Liste
von 255 Bild-Objekten. `erzeugen.py` schreibt daraus GIF und Vorschau nach led/.
"""
import colorsys
import math
import random

from PIL import Image

B, H = 64, 16
MAX_BILDER = 255

# ── Farben ─────────────────────────────────────────────────────────
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
GELB = (255, 210, 0)
GOLD = (255, 150, 0)
ROT = (255, 0, 0)
DUNKELROT = (150, 0, 20)
GRUEN = (0, 170, 0)
DUNKELGRUEN = (0, 90, 20)
HELLGRUEN = (60, 255, 60)
# Braun und Haut am 25.11.2026 an der Matrix ausgewählt (pi/farbtafel.py, Seite 6): die früheren
# Werte (110,50,10), (170,90,30) und (255,170,110) leuchteten auf den LEDs orange. Am Bildschirm
# wirkt das neue Braun fast schwarz, auf der Matrix ist es Holzbraun (Helligkeitsstufe 4 von 31).
BRAUN = (33, 11, 0)
HELLBRAUN = (49, 19, 0)
BLAU = (0, 60, 255)
HELLBLAU = (0, 200, 255)
NACHTBLAU = (0, 0, 22)
LILA = (170, 0, 255)
PINK = (255, 0, 160)
ORANGE = (255, 90, 0)
TUERKIS = (0, 255, 170)
SCHNEE = (140, 150, 190)
SCHNEEDECKE = (190, 200, 235)
GRAU = (90, 90, 100)
HAUT = (214, 173, 143)

BUNT = [ROT, GOLD, BLAU, PINK, LILA, ORANGE, HELLBLAU, TUERKIS, GELB]


def regenbogen(grad):
    """Farbton in 24 Stufen (begrenzt die Palette)."""
    stufe = int(grad % 360 / 15)
    r, g, b = colorsys.hsv_to_rgb(stufe / 24, 1, 1)
    return (round(r * 255), round(g * 255), round(b * 255))


def dimmen(farbe, f):
    return tuple(max(0, min(255, round(c * f))) for c in farbe)


def mischen(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def neues_jahr(heute=None):
    """Das Jahr, das an Silvester beginnt: ab Juli das folgende, sonst das laufende
    (MATRIX_JAHR setzt es fest). Für Jahreszahlen in den Silvester-Animationen."""
    import datetime
    import os
    if os.environ.get("MATRIX_JAHR"):
        return int(os.environ["MATRIX_JAHR"])
    heute = heute or datetime.date.today()
    return heute.year + 1 if heute.month >= 7 else heute.year


NEUES_JAHR = neues_jahr()


# ── Bild ───────────────────────────────────────────────────────────
class Bild:
    def __init__(self, grund=SCHWARZ):
        self.px = [[grund] * B for _ in range(H)]

    def setze(self, x, y, farbe):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < B and 0 <= y < H and farbe is not None:
            self.px[y][x] = farbe

    def hole(self, x, y):
        x, y = int(round(x)), int(round(y))
        return self.px[y][x] if 0 <= x < B and 0 <= y < H else None

    def rechteck(self, x0, y0, b, h, farbe):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + b):
                self.setze(x, y, farbe)

    def linie(self, x0, y0, x1, y1, farbe):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.setze(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, farbe)

    def kreis(self, cx, cy, r, farbe):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + r * 0.8:
                    self.setze(x, y, farbe)

    def figur(self, x0, y0, zeilen, farben, spiegeln=False):
        """Zeichnet ein Sprite aus Zeichen; '.' = durchsichtig, sonst farben[zeichen]."""
        breite = max(len(z) for z in zeilen)
        for dy, zeile in enumerate(zeilen):
            for dx, c in enumerate(zeile):
                if c != ".":
                    x = x0 + (breite - 1 - dx if spiegeln else dx)
                    self.setze(x, y0 + dy, farben[c])

    def text(self, x, y, text, farbe, hoch=1, breit=1):
        """5×7-Schrift (mit hoch/breit vergrößert); farbe ist eine Farbe oder f(index) → Farbe.
        Liefert die Breite."""
        start = x
        for i, z in enumerate(text):
            glyph = SCHRIFT.get(z, SCHRIFT[" "])
            f = farbe(i) if callable(farbe) else farbe
            for gy, zeile in enumerate(glyph):
                for gx, c in enumerate(zeile):
                    if c == "1":
                        for ky in range(hoch):
                            for kx in range(breit):
                                self.setze(x + gx * breit + kx, y + gy * hoch + ky, f)
            x += (len(glyph[0]) + 1) * breit
        return x - start - breit

    def image(self):
        im = Image.new("RGB", (B, H))
        im.putdata([p for zeile in self.px for p in zeile])
        return im


def textbreite(text, breit=1):
    return (sum(len(SCHRIFT.get(z, SCHRIFT[" "])[0]) + 1 for z in text) - 1) * breit


SCHRIFT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    "Ü": ["01010", "00000", "10001", "10001", "10001", "10001", "01110"],
    "!": ["1", "1", "1", "1", "1", "0", "1"],
    ".": ["0", "0", "0", "0", "0", "0", "1"],
    " ": ["000"] * 7,
}


# kleine Ziffern 3×5 (z. B. für Türchen)
KLEIN = {
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
}


def klein_text(bild, x, y, text, farbe):
    for z in text:
        for gy, zeile in enumerate(KLEIN[z]):
            for gx, c in enumerate(zeile):
                if c == "1":
                    bild.setze(x + gx, y + gy, farbe)
        x += 4


# ── Schnee und Sterne ──────────────────────────────────────────────
class Schnee:
    def __init__(self, anzahl=14, saat=2026, farbe=SCHNEE):
        z = random.Random(saat)
        self.flocken = [(z.randrange(B), z.choice([0.25, 0.34, 0.5]), z.uniform(0, 20))
                        for _ in range(anzahl)]
        self.farbe = farbe

    def zeichnen(self, bild, f, nur_auf=None):
        for x, tempo, phase in self.flocken:
            y = (phase + f * tempo) % 20 - 2
            dx = round(math.sin((f + phase * 7) / 9))
            if nur_auf is None or bild.hole(x + dx, y) in nur_auf:
                bild.setze(x + dx, y, self.farbe)


class Sterne:
    def __init__(self, anzahl=22, saat=7, y_max=9):
        z = random.Random(saat)
        self.sterne = [(z.randrange(B), z.randrange(y_max), z.randrange(40), z.choice([24, 32, 40]))
                       for _ in range(anzahl)]

    def zeichnen(self, bild, f):
        for x, y, phase, periode in self.sterne:
            t = (f + phase) % periode / periode
            h = 0.25 + 0.75 * (0.5 + 0.5 * math.cos(2 * math.pi * t))
            bild.setze(x, y, dimmen((255, 240, 200), round(h * 4) / 4))


def sternschnuppe(bild, f, start, x0, y0, laenge=10):
    """Schnuppe von (x0, y0) nach links unten, 10 Bilder lang."""
    t = f - start
    if 0 <= t < laenge:
        for k in range(4):
            bild.setze(x0 - (t - k) * 2, y0 + (t - k), dimmen(WEISS, 1 - k * 0.25) if t >= k else None)


# ── Speichern ──────────────────────────────────────────────────────
def _jedes_bild_anders(bilder):
    """Pillow legt gleiche Nachbarbilder im GIF zusammen; die Matrix spielt aber in festem Takt,
    Standbilder würden dann zu kurz. Gleicht ein Bild seinem Vorgänger, bekommt ein Pixel einen
    um 1 anderen Blauwert (auf den LEDs nicht zu sehen)."""
    neu = []
    for im in bilder:
        if neu and im.tobytes() == neu[-1].tobytes():
            im = im.copy()
            r, g, b = im.getpixel((0, 0))
            im.putpixel((0, 0), (r, g, b + 1 if b < 255 else b - 1))
        neu.append(im)
    return neu


def speichern(bilder, pfad, faktor=1, dauer=100):
    """Liste von PIL-RGB-Bildern als GIF mit einer gemeinsamen Palette (≤ 256 Farben)."""
    bilder = _jedes_bild_anders(bilder)
    farben = sorted({c for im in bilder for c in im.get_flattened_data()})
    if len(farben) <= 256:
        index = {c: i for i, c in enumerate(farben)}
        palette = [v for c in farben for v in c] + [0] * 3 * (256 - len(farben))
        p_bilder = []
        for im in bilder:
            p = Image.new("P", im.size)
            p.putpalette(palette)
            p.putdata([index[c] for c in im.get_flattened_data()])
            p_bilder.append(p)
    else:                                       # zu viele Farben: gemeinsam auf 256 reduzieren
        streifen = Image.new("RGB", (B, H * len(bilder)))
        for i, im in enumerate(bilder):
            streifen.paste(im, (0, i * H))
        pal = streifen.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        p_bilder = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in bilder]
    if faktor > 1:
        p_bilder = [p.resize((B * faktor, H * faktor), Image.NEAREST) for p in p_bilder]
    p_bilder[0].save(pfad, save_all=True, append_images=p_bilder[1:], duration=dauer, loop=0,
                     optimize=False, disposal=1)
    return min(len(farben), 256)
