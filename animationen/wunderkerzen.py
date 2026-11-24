"""Wunderkerzen: Dunkle Silvesternacht, drei erhobene Hände halten Wunderkerzen, die gold-weiß
sprühen. Eine nach der anderen schwenkt zur Seite und zeichnet mit der Spitze eine Leuchtspur in
die Luft – ein Herz, einen Stern, eine Spirale und zum Schluss ein Kleeblatt. Die Spur glüht an
der Spitze weiß-golden, bleibt in ihrer Farbe kurz stehen, glitzert und verglimmt dann in der
Reihenfolge, in der sie gezeichnet wurde. Die Kerzen werden dabei Stück für Stück kürzer; am Ende
zischen sie aus, die Hände sinken, neue Kerzen kommen hoch und werden mit einer kleinen Flamme
angezündet: Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum einfarbiger Himmel mit nur drei Sternen, senkrechte Stäbe und Arme
(gleiche Nachbarspalten), einfarbige Leuchtspuren und nur wenige Funken je Kerze. Die Figuren
stehen frei zwischen den Kerzen, damit sie auf den LEDs gut zu lesen sind.
"""
import math
import random

from basis import GELB, GOLD, HAUT, ORANGE, WEISS, Bild, dimmen

NAME = "wunderkerzen"
TITEL = "Wunderkerzen zeichnen in die Nacht"

RUNDE = 255
NACHT = (0, 0, 14)
DRAHT = (110, 110, 125)                        # Stab der Wunderkerze
GLUT = (255, 235, 150)                         # frische Spur und junge Funken
ROTGLUT = (170, 20, 0)                         # verlöschende Spitze
FLAMME_BLAU = (0, 60, 255)
STERN_FARBE = (110, 130, 255)
STERNE = [(2, 1, 0, 51), (62, 3, 20, 85), (34, 0, 40, 51)]          # x, y, Phase, Periode (teilt 255)

KERZEN_X = [10, 32, 54]                        # Spalte der drei Kerzen in Ruhe
AERMEL = [(0, 60, 220), (150, 0, 220), (210, 0, 30)]
HAND_Y = [12, 11, 12]                          # Ruhelage: Oberkante der Hand (die mittlere hält höher)
STAB = 6                                       # Länge einer frischen Kerze

ANLAUF = 10                                    # Bilder von der Ruhelage zum Anfang der Figur und zurück
STEHEN = 18                                    # so lange bleibt die fertige Figur stehen
GLIMMEN = 16                                   # dann verglimmt sie, vom Anfang des Strichs her
KOPF = 4                                       # so viele Pixel hinter der Spitze glüht die Spur noch hell
ENDE = 205                                     # ab hier brennen die Kerzen herunter (je Kerze 5 Bilder später)
NEU = 228                                      # ab hier kommen die neuen Kerzen (je Kerze 4 Bilder später)


# ── Figuren als Pixelketten (13 Spalten breit, Ursprung links oben) ──
def _zug(*ecken):
    """Pixelkette in Strichrichtung durch die Eckpunkte; jedes Stück läuft waagerecht, senkrecht
    oder genau schräg (so bleibt die Linie überall ein Pixel dünn)."""
    kette = [ecken[0]]
    for (x0, y0), (x1, y1) in zip(ecken, ecken[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        assert abs(x1 - x0) in (0, n) and abs(y1 - y0) in (0, n), (x0, y0, x1, y1)
        for i in range(1, n + 1):
            kette.append((x0 + (x1 - x0) * i // n, y0 + (y1 - y0) * i // n))
    return kette


# von der Kerbe oben über die rechte Rundung zur Spitze und links wieder hinauf
HERZ = _zug((6, 2), (8, 0), (10, 0), (12, 2), (12, 5), (6, 11), (0, 5), (0, 2), (2, 0), (4, 0), (6, 2))
# fünf Zacken, von der oberen Zacke im Uhrzeigersinn
STERN = _zug((6, 0), (7, 1), (7, 2), (8, 3), (8, 4), (12, 4), (9, 7), (9, 8), (10, 9), (10, 10),
             (11, 11), (11, 12), (10, 12), (9, 11), (8, 11), (6, 9), (4, 11), (3, 11), (2, 12),
             (1, 12), (1, 11), (2, 10), (2, 9), (3, 8), (3, 7), (0, 4), (4, 4), (4, 3), (5, 2),
             (5, 1), (6, 0))
# von der Mitte nach außen, zwei Windungen mit je zwei Pixeln Abstand
SPIRALE = _zug((6, 6), (8, 6), (9, 7), (9, 8), (8, 9), (4, 9), (3, 8), (3, 4), (4, 3), (10, 3),
               (12, 5), (12, 9), (9, 12), (3, 12), (0, 9), (0, 3), (3, 0), (9, 0), (10, 1))
# vier Blätter in einem Zug (unten links beginnend), dann der Stiel
KLEE = _zug((6, 9), (5, 10), (5, 11), (4, 12), (2, 12), (0, 10), (0, 8), (1, 7), (2, 7), (3, 6),
            (2, 5), (1, 5), (0, 4), (0, 2), (2, 0), (4, 0), (5, 1), (5, 2), (6, 3), (7, 2), (7, 1),
            (8, 0), (10, 0), (12, 2), (12, 4), (11, 5), (10, 5), (9, 6), (10, 7), (11, 7), (12, 8),
            (12, 10), (10, 12), (8, 12), (7, 11), (7, 10), (6, 9), (6, 13), (7, 14))

# Figur: Pixelkette, Farbe der Spur, oberste Zeile, Pixel je Bild beim Zeichnen
FIGUREN = {"herz": (HERZ, (255, 0, 70), 2, 1.1),
           "stern": (STERN, GELB, 1, 1.2),
           "spirale": (SPIRALE, (0, 200, 255), 1, 1.3),
           "klee": (KLEE, (40, 255, 40), 0, 1.2)}
# wer wann was wo zeichnet: Kerze, erstes Bild, Figur, mittlere Spalte (zwischen den Kerzen)
AUFTRAEGE = [(0, 10, "herz", 21), (2, 48, "stern", 43), (1, 94, "spirale", 21), (1, 148, "klee", 43)]


def _dauer(form):
    return round((len(FIGUREN[form][0]) - 1) / FIGUREN[form][3])


def _stelle(form, t):
    """Index in der Pixelkette nach t Bildern Zeichnen."""
    n = len(FIGUREN[form][0]) - 1
    return max(0, min(n, round(t * n / _dauer(form))))


def _punkt(form, mitte, i):
    kette, _, oben, _ = FIGUREN[form]
    return mitte - 6 + kette[i][0], oben + kette[i][1]


# ── Kerzen ─────────────────────────────────────────────────────────
def _laenge(f):
    """Die Kerzen brennen langsam herunter: alle 41 Bilder ein Pixel kürzer."""
    return STAB - min(4, f // 41)


def _ruhe(k, f, lang):
    """Ruhelage der Spitze; die Hand wiegt ganz langsam um eine Spalte hin und her."""
    wiegen = round(1.2 * math.sin(2 * math.pi * (f / 85 + k / 3)))
    return KERZEN_X[k] + wiegen, HAND_Y[k] - 1 - lang


def _gleiten(a, b, t):
    t = t * t * (3 - 2 * t)                                         # sanft anfahren und abbremsen
    return round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t)


def _bahnen():
    """Ort der Spitze je Kerze und Bild, solange sie brennt: Ruhelage, Anlauf, Zeichnen, Rückweg.
    Folgen zwei Aufträge einer Kerze dicht aufeinander, schwenkt sie direkt zur nächsten Figur."""
    bahnen = []
    for k in range(3):
        bahn = [None] * RUNDE
        for kk, start, form, mitte in AUFTRAEGE:
            if kk == k:
                for t in range(_dauer(form) + 1):
                    bahn[start + t] = _punkt(form, mitte, _stelle(form, t))
        f = 0
        while f < RUNDE:
            if bahn[f] is not None:
                f += 1
                continue
            g = f
            while g < RUNDE and bahn[g] is None:
                g += 1
            vorher = bahn[f - 1] if f > 0 else None                 # Lücke f … g-1
            nachher = bahn[g] if g < RUNDE else None
            for i in range(f, g):
                ruhe = _ruhe(k, i, _laenge(i))
                if vorher and nachher and g - f <= 2 * ANLAUF:
                    bahn[i] = _gleiten(vorher, nachher, (i - f + 1) / (g - f + 1))
                elif vorher and i - f < ANLAUF:
                    bahn[i] = _gleiten(vorher, ruhe, (i - f + 1) / ANLAUF)
                elif nachher and g - i <= ANLAUF:
                    bahn[i] = _gleiten(ruhe, nachher, 1 - (g - i) / ANLAUF)
                else:
                    bahn[i] = ruhe
            f = g
        bahnen.append(bahn)
    return bahnen


BAHNEN = _bahnen()


def _kerze(k, f):
    """Zustand der Kerze k im Bild f: (x, y der Spitze, Stablänge, Zustand).
    Zustände: brennt, zischt (fast herunter), glimmt, glut, weg, neu, zuenden, faengt (Feuer), blitz."""
    aus = ENDE + 5 * k
    neu = NEU + 4 * k
    if f >= neu:                                                    # neue Kerze steigt auf und wird angezündet
        x, y = _ruhe(k, f, STAB)
        y += max(0, (neu + 6 - f) * 2)
        if f < neu + 6:
            return x, y, STAB, "neu"
        if f < neu + 11:
            return x, y, STAB, "zuenden"
        if f < neu + 13:
            return x, y, STAB, "faengt"
        if f < neu + 15:
            return x, y, STAB, "blitz"
        return x, y, STAB, "brennt"
    if f >= aus:                                                    # heruntergebrannt
        x, y = _ruhe(k, f, 1)
        if f < aus + 6:
            return x, y, 1, "zischt"
        if f < aus + 8:
            return x, y, 1, "glimmt"
        if f < aus + 10:
            return x, y, 1, "glut"
        if f < aus + 16:                                            # die Hand sinkt
            return x, y + f - aus - 9, 1, "glut"
        return x, 99, 1, "weg"
    return BAHNEN[k][f][0], BAHNEN[k][f][1], _laenge(f), "brennt"


def _hand_und_stab(bild, k, x, y, lang, zustand):
    """Stab unter der Spitze, Faust, darunter der Ärmel – beim Schwenken schräg zurück zur Schulter."""
    if zustand == "weg":
        return
    for yy in range(y + 1, y + 1 + lang):
        bild.setze(x, yy, DRAHT)
    hand = y + lang + 1
    bild.rechteck(x - 1, hand, 3, 2, HAUT)
    schraeg = max(-1.0, min(1.0, (KERZEN_X[k] - x) / max(1, 20 - hand)))
    for yy in range(hand + 2, 16):
        bild.rechteck(x - 1 + round((yy - hand - 1) * schraeg), yy, 3, 1, AERMEL[k])


def _spitze(bild, k, f, x, y, zustand):
    if zustand == "brennt":                                         # flackert zwischen + und ×
        # (255 Bilder sind ungerade: der Takt wechselt in der dunklen Pause, damit er über die Naht passt)
        if (f + k + (f >= NEU)) % 2 == 0:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                bild.setze(x + dx, y + dy, GELB)
        else:
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                bild.setze(x + dx, y + dy, GOLD)
        bild.setze(x, y, WEISS)
    elif zustand == "zischt":
        bild.setze(x, y, WEISS if f % 2 else GELB)
    elif zustand == "glimmt":
        bild.setze(x, y, ORANGE)
    elif zustand == "glut":
        bild.setze(x, y, ROTGLUT)
    elif zustand == "neu":
        bild.setze(x, y, DRAHT)
    elif zustand in ("zuenden", "faengt"):                          # kleine Flamme neben der Spitze
        bild.setze(x, y, DRAHT if zustand == "zuenden" else ORANGE)
        bild.setze(x - 1, y + 1, FLAMME_BLAU)
        bild.setze(x - 1, y, ORANGE)
        if f % 2:
            bild.setze(x - 1, y - 1, GELB)
    elif zustand == "blitz":
        for d in (1, 2):
            for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
                bild.setze(x + dx, y + dy, WEISS if d == 1 else GELB)
        bild.setze(x, y, WEISS)


def _zeichnet(k, f):
    return any(kk == k and start <= f <= start + _dauer(form) for kk, start, form, _ in AUFTRAEGE)


def _funken(bild, k, f):
    """Funken fliegen in kurzen Strahlen von der Spitze weg: frisch ein Strich aus zwei Pixeln,
    dann ein Punkt, der verglimmt. Jeder lebt drei Bilder und geht von dem Ort aus, an dem die
    Spitze bei seiner Geburt war. Die Kerze, die gerade zeichnet, sprüht doppelt."""
    for alter in (2, 1, 0):
        g = (f - alter) % RUNDE
        x, y, lang, zustand = _kerze(k, g)
        if zustand not in ("brennt", "zischt") or (zustand == "zischt" and g % 2):
            continue
        z = random.Random(g * 31 + k * 977)
        for _ in range(2 if _zeichnet(k, g) else 1):
            w = z.uniform(2.2, 7.2)                                 # nicht nach unten auf Stab und Hand
            tempo = z.uniform(0.9, 1.3)
            for r, farbe in (((2.0, GLUT), (3.0, GELB)), ((3.2 + tempo, GOLD),),
                             ((3.4 + 2 * tempo, dimmen(ORANGE, 0.6)),))[alter]:
                bild.setze(x + r * math.cos(w), y + r * math.sin(w) + 0.15 * alter * alter, farbe)


def _spuren(bild, f):
    for k, start, form, mitte in AUFTRAEGE:
        kette, farbe, oben, _ = FIGUREN[form]
        dauer = _dauer(form)
        t = f - start
        if t < 0 or t >= dauer + STEHEN + GLIMMEN:
            continue
        ende = _stelle(form, min(t, dauer))
        # verglimmen: die Spur erlischt in der Reihenfolge, in der sie gezeichnet wurde
        rand = (t - dauer - STEHEN + 1) / GLIMMEN * (len(kette) + 12) - 12 if t >= dauer + STEHEN else -99
        for j in range(ende + 1):
            if j <= rand:
                continue
            if j <= rand + 12:
                c = dimmen(farbe, 0.3 if j <= rand + 6 else 0.6)
            elif t <= dauer and j > ende - KOPF:
                c = GLUT
            elif (j * 5 + f // 3 * 7) % 19 == 0:                    # Glitzern: wenige Punkte, alle drei Bilder andere
                c = WEISS
            else:
                c = farbe
            bild.setze(*_punkt(form, mitte, j), c)


def bilder():
    liste = []
    for f in range(RUNDE):
        bild = Bild(NACHT)
        for x, y, phase, periode in STERNE:                         # drei Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN_FARBE, 1.0 if (f + phase) % periode < periode * 0.7 else 0.5))
        kerzen = [_kerze(k, f) for k in range(3)]
        for k, (x, y, lang, zustand) in enumerate(kerzen):
            _hand_und_stab(bild, k, x, y, lang, zustand)
        _spuren(bild, f)
        for k, (x, y, lang, zustand) in enumerate(kerzen):
            _funken(bild, k, f)
            _spitze(bild, k, f, x, y, zustand)
        liste.append(bild)
    return liste
