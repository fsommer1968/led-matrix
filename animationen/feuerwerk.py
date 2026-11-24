"""Feuerwerk über der Stadt: Raketen steigen mit Schweif, platzen als Kugeln, Ringe, Goldregen und
Herzen, die Stadt-Silhouette leuchtet in der Farbe des Feuerwerks auf; in der Mitte der Animation
steigen vier Raketen, deren Funken sich zu einer großen "2027" ordnen (Jahreszahl automatisch: basis.NEUES_JAHR) – 255 Bilder.

Feuerwerk() ist auch ein Baustein für andere Silvester-Animationen.
"""
import colorsys
import math
import random

from basis import NEUES_JAHR, B, BUNT, GELB, GOLD, ORANGE, PINK, ROT, WEISS, Bild, dimmen, mischen

NAME = "feuerwerk"
TITEL = "Feuerwerk über der Stadt"

HIMMEL = (0, 0, 14)
HAUS = (24, 22, 52)
KANTE = (46, 42, 88)
FENSTER = (255, 170, 40)
STUFEN = 8                                      # Helligkeitsstufen (hält die Palette klein)
MIN_STUFE = 2                                   # Funken unter 2/8 sind auf den LEDs praktisch aus


def _stufe(h):
    return max(0, min(STUFEN, round(h * STUFEN))) / STUFEN


def _funke(bild, x, y, farbe, h):
    """Setzt einen Funken in der Helligkeit h (0..1, auf Stufen gerundet). Funken unter MIN_STUFE
    fallen weg: auf den LEDs sind sie praktisch aus, im Speicher der Matrix (80 KB je Animation,
    jedes Bild einzeln komprimiert) kostet aber jeder einzelne Punkt 5 bis 8 Bytes."""
    s = _stufe(h)
    if s * STUFEN >= MIN_STUFE:
        bild.setze(x, y, dimmen(farbe, s))


def _matrixfarbe(r, g, b):
    """16-Bit-Farbe der Matrix, 7/4/5 Bit H/S/V (wie led/pi/matrix_spieler.hsv16)."""
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return (round(h * 127) & 0x7F) << 9 | round(s * 15) << 5 | round(v * 31)


def jedes_bild_anders(liste, grund):
    """Sorgt dafür, dass kein Bild seinem Vorgänger gleicht.

    Die Matrix spielt alle Bilder gleich lang (die Bilddauer wird nicht übertragen), und beim Speichern
    fasst das GIF gleiche Bilder hintereinander zu einem zusammen – ein Standbild über 20 Bilder wäre
    auf der Matrix nur ein Bild lang. Darum bekommt jedes Bild, das seinem Vorgänger gleicht, einen
    Hintergrundpixel in einer Nachbarfarbe, die die Matrix genauso darstellt (gleicher 16-Bit-Wert):
    im GIF verschieden, auf den LEDs unverändert."""
    ziel = _matrixfarbe(*grund)
    nachbarn = [(grund[0] + a, grund[1] + b, grund[2] + c)
                for c in (1, -1, 2, -2, 0) for b in (0, 1, -1) for a in (0, 1, -1)]
    ersatz = next((n for n in nachbarn if n != grund and min(n) >= 0 and max(n) <= 255
                   and _matrixfarbe(*n) == ziel), (grund[0], grund[1], grund[2] + 1))
    for i in range(1, len(liste)):
        if liste[i].px == liste[i - 1].px:
            ort = next(((x, y) for y in range(15, -1, -1) for x in range(B) if liste[i].px[y][x] == grund), None)
            if ort:
                liste[i].setze(*ort, ersatz)
    return liste


class Feuerwerk:
    """Plant Raketen deterministisch; zeichnen(bild, f) malt den Stand zum Bild f.

    Die Raketen werden so verteilt, dass aufeinanderfolgende nicht an derselben Stelle platzen;
    jede Explosion hat eine klare Form (Strahlen, die zu Punkten werden, dann funkelnd verlöschen).
    """

    DAUER = {"kugel": 22, "ring": 20, "doppel": 22, "gold": 28, "herz": 24}

    def __init__(self, saat, abstand=(10, 22), x_bereich=(4, B - 4), y_bereich=(1, 6), start=0,
                 ende=10 ** 6, arten=("kugel", "ring", "gold", "doppel"), farben=BUNT, radius=(4.6, 6.8)):
        z = random.Random(saat)
        self.raketen = []
        t = start
        letzte = []
        while t < ende:
            kandidaten = [z.randrange(*x_bereich) for _ in range(6)]
            x = max(kandidaten, key=lambda k: min([abs(k - a) for a in letzte[-2:]] or [0]))
            letzte.append(x)
            ziel_y = z.randrange(*y_bereich)
            farbe = farben[z.randrange(len(farben))]
            farbe2 = farben[z.randrange(len(farben))]
            while farbe2 == farbe and len(farben) > 1:
                farbe2 = farben[z.randrange(len(farben))]
            art = z.choice(arten)
            groesse = z.uniform(*radius)
            dreh = z.uniform(0, 2 * math.pi)
            if art == "herz":
                farbe = z.choice((ROT, PINK))
            self.raketen.append((t, x, ziel_y, farbe, farbe2, art, self._funken(art, dreh, z), groesse))
            t += z.randrange(*abstand)

    @staticmethod
    def _funken(art, dreh, z):
        """Liste (winkel, weite, schicht): gleichmäßig verteilt, damit die Form klar bleibt."""
        if art == "ring":
            return [(dreh + i * 2 * math.pi / 16, 1.0, 0) for i in range(16)]
        if art == "gold":
            return [(dreh + i * 2 * math.pi / 11, z.uniform(0.75, 1.0), 0) for i in range(11)]
        if art == "herz":
            return [(i * 2 * math.pi / 20, 1.0, 0) for i in range(20)]
        aussen = [(dreh + i * 2 * math.pi / 12 + z.uniform(-0.08, 0.08), z.uniform(0.92, 1.0), 0)
                  for i in range(12)]
        n = 6 if art == "kugel" else 8
        innen = [(dreh + (i + 0.5) * 2 * math.pi / n, 0.5, 1) for i in range(n)]
        return aussen + innen

    @staticmethod
    def _steigzeit(ziel_y, boden):
        return max(4, round((boden - ziel_y) / 1.8))

    def blitz(self, f, boden=15):
        """(Stärke 0..1, Farbe) des hellsten frischen Platzers – für Widerschein auf der Stadt."""
        bester = (0.0, WEISS)
        for t0, x, ziel_y, farbe, farbe2, art, funken, radius in self.raketen:
            k = f - t0 - self._steigzeit(ziel_y, boden)
            if 0 <= k < 10:
                st = 1 - k / 10
                if st > bester[0]:
                    bester = (st, GOLD if art == "gold" else farbe)
        return bester

    def zeichnen(self, bild, f, boden=15, hell=1.0):
        for t0, x, ziel_y, farbe, farbe2, art, funken, radius in self.raketen:
            t = f - t0
            steig = self._steigzeit(ziel_y, boden)
            if t < 0 or t >= steig + self.DAUER[art]:
                continue
            if t < steig:
                self._aufstieg(bild, x, ziel_y, boden, t, steig, hell)
            else:
                self._platzen(bild, x, ziel_y, farbe, farbe2, art, funken, radius, t - steig, hell)

    @staticmethod
    def _aufstieg(bild, x, ziel_y, boden, t, steig, hell):
        def hoehe(tt):                                             # schnell los, oben langsamer
            s = max(0.0, min(1.0, tt / steig))
            return boden - (boden - ziel_y) * (1 - (1 - s) ** 2)
        y = round(hoehe(t))
        y1 = round(hoehe(t - 1))
        y2 = round(hoehe(t - 2.5))
        for yy in range(y + 1, y2 + 1):                            # Schweif
            if yy < boden:
                _funke(bild, x, yy, GOLD if yy <= y1 else ORANGE, (0.75 if yy <= y1 else 0.4) * hell)
        bild.setze(x, y, dimmen((255, 235, 170), _stufe(hell)))

    def _platzen(self, bild, x, ziel_y, farbe, farbe2, art, funken, radius, k, hell):
        dauer = self.DAUER[art]
        if k < 2:                                                  # Blitz
            c = dimmen(WEISS, _stufe(hell))
            bild.setze(x, ziel_y, c)
            for d in range(1, k + 2):
                for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
                    bild.setze(x + dx, ziel_y + dy, c)
            if k == 1:
                for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                    bild.setze(x + dx, ziel_y + dy, dimmen(mischen(farbe, WEISS, 0.5), _stufe(hell)))
            return

        def weite(kk):
            return radius * (1 - math.exp(-(max(kk, 0) + 0.5) / 3.2))

        fall = 0.022 if art == "gold" else 0.008
        halten = 8
        grund = 1.0 if k <= halten else 1 - (k - halten) / (dauer - halten)
        for i, (w, v, schicht) in enumerate(funken):
            def ort(kk):
                r = weite(kk) * v
                if art == "herz":
                    hx = math.sin(w) ** 3
                    hy = -(13 * math.cos(w) - 5 * math.cos(2 * w) - 2 * math.cos(3 * w) - math.cos(4 * w)) / 16
                    return x + r * hx, ziel_y + r * hy * 0.9 + fall * kk * kk
                return x + r * math.cos(w), ziel_y + r * math.sin(w) * 0.85 + fall * kk * kk

            if art == "gold":
                c = GELB if k < 7 else (GOLD if k < 16 else ORANGE)
            elif art == "doppel":
                c = farbe2 if schicht else farbe
            else:
                c = farbe
            h = grund
            if art != "gold" and k < 5:                            # frisch: noch weißglühend
                c = mischen(c, WEISS, (5 - k) / 6)
            if k >= 12:                                            # funkelnd verlöschen
                if (i * 5 + k) // 2 % 2:
                    h *= 0.45
                elif (i + k) % 5 == 0:
                    c = mischen(c, WEISS, 0.5)
            if schicht:
                h *= 0.8
            # Schweif: kurz nach dem Platzen Strahlen, beim Goldregen bis zum Schluss
            if art == "gold":
                for n, anteil in ((3.2, 0.25), (1.6, 0.5)):
                    if k - n >= 0:
                        _funke(bild, *ort(k - n), c, h * anteil * hell)
            elif art in ("kugel", "doppel") and not schicht and k <= 9:
                for n, anteil in ((2.4, 0.3), (1.2, 0.55)):
                    _funke(bild, *ort(k - n), c, h * anteil * hell)
            _funke(bild, *ort(k), c, h * hell)


# ── Stadt ──────────────────────────────────────────────────────────
# Die untersten neun Zeilen (y = 7 … 15): '=' Dachkante, '#' Hauswand, 'o' Fenster, '.' Himmel.
# Die Mitte bleibt niedrig, damit die "2027" darüber Platz hat.
# Die Matrix speichert nur 80 KB je Animation und komprimiert jedes Bild einzeln und spaltenweise:
# jede Spalte, die anders ist als ihre Nachbarin, kostet Bytes – in jedem der 255 Bilder. Darum sind
# gleiche Häuser Spalte für Spalte gleich gebaut und die Fenster stehen im festen Raster
# (Wand, Fenster, Wand, …): gleiche Spaltenfolgen kosten fast nichts (142 statt 199 Bytes je Bild).
STADT = ["......=................................................=........",
         "......#................................................#........",
         ".....=#=............................................===#===.....",
         ".....#o#...................=........................#o#o#o#.....",
         "..=..###......=======..=...#.....=====..=...........#######..=..",
         ".=#=.#o#=====.#o#o#o#.=#=.=#=====#o#o#.=#=.=====....#o#o#o#.=#=.",
         "=###=####o#o#.#######=###=###o#o######=###=#####.===#######=###=",
         "#o#o#########.#o#o#o##o#o#########o#o##o#o######.###########o#o#",
         "#############.##################################.###############"]


# Ab und zu geht ein Licht aus: Fenster (x, y) → Abschnitt (je 40 Bilder), in dem es dunkel ist.
# Immer nur eines zugleich und nur Fenster, die das Raster wenig stören (ein dunkles Fenster kostet
# je nach Platz 3 bis 13 Bytes in jedem Bild).
LICHT_AUS = {(29, 13): 0, (55, 12): 1, (36, 12): 2, (6, 10): 3, (41, 14): 4, (57, 10): 5, (34, 14): 6}


def _stadtplan():
    """Spaltenhöhen und Fensterplätze (x, y, phase) aus STADT; phase legt fest, wann das Licht aus ist."""
    oben = 16 - len(STADT)
    hoehen = [0] * B
    fenster = []
    for i, zeile in enumerate(STADT):
        for x, c in enumerate(zeile):
            if c != "." and not hoehen[x]:
                hoehen[x] = 16 - oben - i
            if c == "o":
                abschnitt = LICHT_AUS.get((x, oben + i))
                fenster.append((x, oben + i, 1 if abschnitt is None else (9 - abschnitt) % 9))
    return hoehen, fenster


HOEHEN, FENSTER_PLAETZE = _stadtplan()


def stadt(bild, f, licht=0.0, lichtfarbe=WEISS):
    """Silhouette mit Dachkante und warmen Fenstern; licht (0..1) färbt sie im Schein des Feuerwerks."""
    licht = round(licht * 4) / 4
    haus = mischen(HAUS, dimmen(lichtfarbe, 0.3), licht * 0.6)
    kante = mischen(KANTE, dimmen(lichtfarbe, 0.6), licht * 0.7)
    for x, h in enumerate(HOEHEN):
        for y in range(16 - h, 16):
            bild.setze(x, y, kante if y == 16 - h else haus)
    for wx, wy, phase in FENSTER_PLAETZE:
        an = (f // 40 + phase) % 9 != 0                            # ab und zu geht ein Licht aus
        bild.setze(wx, wy, FENSTER if an else dimmen(FENSTER, 0.3))


# ── "2027" aus Funken ──────────────────────────────────────────────
ZIFFERN_FETT = {
    "2": [".XXXXX.", "XX...XX", ".....XX", "....XX.", "...XX..", "..XX...", ".XX....", "XX.....", "XXXXXXX"],
    "0": [".XXXXX.", "XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX", ".XXXXX."],
    "7": ["XXXXXXX", ".....XX", ".....XX", "....XX.", "...XX..", "...XX..", "..XX...", "..XX...", "..XX..."],
}
JAHR_START = 136                                # erste der vier Raketen startet
JAHR_ENDE = 208


def jahr_aus_funken(bild, f, boden=11):
    """Vier Raketen steigen, platzen, und ihre Funken fliegen auf die Plätze der Ziffern."""
    z = random.Random(2027)
    x0, y0 = 15, 1
    for d, ziffer in enumerate(str(NEUES_JAHR)):
        cx, cy = x0 + d * 9 + 3, y0 + 4
        start = JAHR_START + d * 4
        steig = 5
        t = f - start
        punkte = [(x0 + d * 9 + gx, y0 + gy, z.randrange(10), z.uniform(0.25, 0.5))
                  for gy, zeile in enumerate(ZIFFERN_FETT[ziffer]) for gx, c in enumerate(zeile) if c == "X"]
        if t < 0:
            continue
        if t < steig:                                              # Rakete
            y = round(boden - (boden - cy) * (1 - (1 - t / steig) ** 2))
            bild.setze(cx, y, (255, 235, 170))
            bild.setze(cx, y + 1, dimmen(GOLD, 0.75))
            if y + 2 < boden:
                bild.setze(cx, y + 2, dimmen(ORANGE, 0.4))
            continue
        k = t - steig
        ende = JAHR_ENDE - 22 + d * 2                              # ab hier rieseln die Funken herab
        for tx, ty, phase, tempo in punkte:
            if f < ende:
                s = min(1.0, k / 7)
                e = 1 - (1 - s) ** 3
                px, py = cx + (tx - cx) * e, cy + (ty - cy) * e
                if k < 2:
                    c = WEISS
                elif (phase + f // 3) % 10 == 0:                   # Glitzern
                    c = WEISS
                elif (tx + ty - f // 2) % 6 == 0:                  # wandernder Schimmer
                    c = GOLD
                else:
                    c = GELB
                bild.setze(px, py, c)
            else:
                kk = f - ende - phase * 0.6                        # jeder Funke löst sich etwas später
                if kk < 0:
                    bild.setze(tx, ty, GOLD)
                    continue
                h = 1 - kk / 12
                if h > 0:
                    _funke(bild, tx, ty + tempo * kk + 0.03 * kk * kk, GOLD if h > 0.5 else ORANGE, h)


def bilder():
    arten = ("kugel", "ring", "gold", "doppel", "kugel", "herz")
    vorher = Feuerwerk(saat=2027, abstand=(7, 13), y_bereich=(3, 7), start=2, ende=118, arten=arten)
    nachher = Feuerwerk(saat=27, abstand=(7, 12), y_bereich=(3, 7), start=JAHR_ENDE - 6, ende=231, arten=arten)
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        licht, farbe = 0.0, WEISS
        for fw in (vorher, nachher):
            fw.zeichnen(bild, f, boden=11)
            st, c = fw.blitz(f, boden=11)
            if st > licht:
                licht, farbe = st, c
        if JAHR_START + 5 <= f < JAHR_ENDE - 8:                    # goldener Schein der Jahreszahl
            an = min(1.0, (f - JAHR_START - 5) / 8, (JAHR_ENDE - 8 - f) / 8)
            if an * 0.75 > licht:
                licht, farbe = an * 0.75, GOLD
        if JAHR_START <= f < JAHR_ENDE:                            # hinter den Dächern
            jahr_aus_funken(bild, f)
        stadt(bild, f, licht, farbe)
        liste.append(bild)
    return jedes_bild_anders(liste, HIMMEL)
