"""Neujahrsbrezel: Auf dem Holztisch liegt ein heller Teigstrang mit dickem, geflochtenem Bauch. Zwei
Hände fassen die Enden, heben sie an, legen erst das eine, dann das andere über Kreuz und drücken
sie auf dem Bauch fest – die Brezel ist geschlungen. Das Blech schiebt sich darunter, der Ofen
kommt ins Bild, das Fenster leuchtet auf: Die Brezel geht auf und bräunt in Stufen goldgelb, die
Uhr am Ofen läuft mit, zum Schluss zieht ein Lichtstreif über die Kruste. Zurück auf dem Tisch
streut eine Hand Hagelzucker darüber, die Körner blinken und blitzen. Dann wird die fertige Brezel
nach oben weggetragen und von unten kommt der nächste Teigstrang – die Runde geht ohne Sprung in
sich über. 255 Bilder.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum einfarbiger Tisch, das Blech als Band über die ganze Höhe,
senkrechte Arme, ein Ofen aus einfarbigen Spalten, Heizstäbe als durchgehende Zeilen und nur
wenige Zuckerkörner. Goldgelb statt Braun, weil Braun auf den LEDs orange leuchtet.
"""
import math
import random

from basis import B, BRAUN, HAUT, ROT, WEISS, Bild, mischen

NAME = "neujahrsbrezel"
TITEL = "Neujahrsbrezel"

TISCH = BRAUN
BLECH = (36, 40, 62)
# Teig: hell und blass, im Ofen in deutlichen Stufen goldgelb (kein Braun)
TEIG = [(255, 240, 190), (255, 232, 150), (255, 220, 100), (255, 205, 50), (255, 190, 0)]
SCHATTEN = [(165, 145, 100), (170, 148, 85), (175, 145, 55), (180, 138, 20), (185, 135, 0)]   # Kerben, Kreuzung
GLANZ = (255, 235, 140)                        # Lichtstreif, der über die goldgelbe Kruste zieht
AERMEL = (0, 60, 200)
OFEN = (30, 32, 50)
RAHMEN = (120, 125, 150)
DUNKEL = (8, 8, 14)                            # Ofenraum, kalt
GLUT = (110, 14, 0)                            # Ofenraum, heiß (große Fläche, gedämpft)
STAB = [(255, 100, 0), (255, 150, 20)]         # Heizstäbe, glühen langsam auf und ab
LAMPE_AUS = (70, 0, 0)
ZUCKER_MATT = (150, 150, 175)

MX = 31.5                                      # Mitte der Brezel
N = 121                                        # Punkte auf dem Strang
MITTE = N // 2                                 # … der mittlere ist die Bauchmitte
BAUCH = 22                                     # so viele Punkte links und rechts der Mitte sind Bauch
FERN = 20                                      # ab diesem Abstand auf dem Strang liegt ein Stück über dem anderen
ZOPF, ZOPF_WEIT = 6, 16                        # jeder sechste Punkt unten im Bauch trägt eine Kerbe
BLECH_X, BLECH_B = 16, 32                      # Blech: linke Spalte, Breite (über die ganze Höhe)
FENSTER_X, FENSTER_B = 14, 36                  # Ofenfenster, links und rechts je eine Spalte Rahmen
KNOPF_X, KNOPF_Y = 56, 2                       # Uhr am Ofen (3×3), darunter die Lampe
ZEIGER = [(1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0)]

# Ablauf
T_HAND, T_HEBEN, T_KREUZ, T_LOS, T_BLECH = 1, 7, 24, 56, 62
VERSATZ, KREUZ_DAUER = 13, 16                  # die rechte Hand folgt der linken
SCHWENK = 14                                   # so viele Bilder braucht der Ofen ins Bild und wieder hinaus
T_HIN, T_OFEN, T_HER, T_TISCH = 75, 89, 163, 177                     # Ofen kommt, steht, geht, ist fort
T_AUF = [99, 104, 109, 114]                    # die Brezel geht in vier Schritten auf
T_FARBE = [121, 129, 137, 145]                 # … und bräunt in vier Stufen
T_STREUEN, T_WEITER = 185, 239
STREU_DAUER, STREU_TEMPO, STREU_VORLAUF = 16, 2, 8                   # die Hand streut hin und zurück
T_FUNKELN = [207, 212, 217, 222, 226, 230, 234, 238, 242, 246, 250]  # je ein Korn blitzt auf
T_GLANZ, GLANZ_DAUER = (147, 228), 10          # fertig gebacken und fertig bestreut: ein Lichtstreif zieht darüber


def _sanft(a):
    a = max(0.0, min(1.0, a))
    return a * a * (3 - 2 * a)


# ── Strang ─────────────────────────────────────────────────────────
def _glatt(punkte, mal=2):
    """Ecken abrunden (Chaikin), die Enden bleiben."""
    for _ in range(mal):
        neu = [punkte[0]]
        for (x0, y0), (x1, y1) in zip(punkte, punkte[1:]):
            neu.append((x0 * 0.75 + x1 * 0.25, y0 * 0.75 + y1 * 0.25))
            neu.append((x0 * 0.25 + x1 * 0.75, y0 * 0.25 + y1 * 0.75))
        neu.append(punkte[-1])
        punkte = neu
    return punkte


def _weg(halb):
    """Linke Hälfte (vom Ende bis zur Bauchmitte) → ganzer Strang aus N Punkten in gleichem
    Abstand, die rechte Hälfte ist das Spiegelbild."""
    punkte = _glatt(halb)
    strecke = [0.0]
    for (x0, y0), (x1, y1) in zip(punkte, punkte[1:]):
        strecke.append(strecke[-1] + math.hypot(x1 - x0, y1 - y0))
    links, k = [], 0
    for i in range(MITTE + 1):
        s = strecke[-1] * i / MITTE
        while k < len(punkte) - 2 and strecke[k + 1] < s:
            k += 1
        a = (s - strecke[k]) / ((strecke[k + 1] - strecke[k]) or 1)
        links.append((punkte[k][0] + (punkte[k + 1][0] - punkte[k][0]) * a,
                      punkte[k][1] + (punkte[k + 1][1] - punkte[k][1]) * a))
    return links + [(2 * MX - x, y) for x, y in reversed(links[:-1])]


GERADE = _weg([(4, 13), (MX, 13)])
BOGEN = _weg([(5, 3), (19, 11.5), (25, 13.5), (MX, 13.5)])
# geschlungen: zwei runde Schlaufen, in der Mitte der Knoten, die Enden gespreizt auf dem Bauch
BREZEL = _weg([(38, 12), (35, 10.5), (32.5, 9), (MX, 7.5), (30.5, 6), (29.5, 4), (27.5, 2.5), (24.5, 2),
               (21.5, 3), (19.5, 6), (20, 9.5), (23, 12.5), (27, 14), (MX, 14)])
# aufgegangen: etwas größer, die Arme dicker, die Löcher bleiben offen
GROSS = _weg([(38.5, 11.5), (35, 10), (32.5, 8.5), (MX, 7), (30.5, 5.5), (29.5, 4), (27.5, 2.5), (24.5, 2),
              (21, 3), (19, 6), (19.5, 9.5), (22.5, 12.5), (27, 14), (MX, 14)])
PINSEL = {2: ["XX", "XX"], 3: [".X.", "XXX", ".X."]}


def _strang(bild, punkte, stufe=0, arme=2, dy=0, glanz=None):
    """Zeichnet den Strang: der Bauch drei, die Arme zwei oder (aufgegangen) drei Pixel dick, erst
    der linke Arm vom Bauch bis zum Ende, dann der rechte darüber. Wo ein Stück über einem anderen
    liegt, bekommt das untere einen Schattenrand; mitten im Bauch sitzen die Kerben des Zopfs. Die
    rechte Hälfte wird gespiegelt gerundet, damit die Brezel genau symmetrisch wird. `glanz` ist
    die Lage eines schrägen, zwei Pixel breiten Lichtstreifs (x + y)."""
    besitzer, dunkel, kerben = {}, set(), []
    for i in list(range(MITTE, -1, -1)) + list(range(MITTE + 1, N)):
        x, y = punkte[i]
        rechts = i > MITTE
        if rechts:
            x = 2 * MX - x
        maske = PINSEL[3 if abs(i - MITTE) <= BAUCH else arme]
        d = len(maske)
        x0, y0 = math.floor(x - (d - 1) / 2 + 0.5), math.floor(y - (d - 1) / 2 + 0.5)
        stempel = {(B - 1 - x0 - ax if rechts else x0 + ax, y0 + ay)
                   for ay, zeile in enumerate(maske) for ax, c in enumerate(zeile) if c == "X"}
        for px, py in stempel:
            for nachbar in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                if nachbar not in stempel and abs(besitzer.get(nachbar, i) - i) > FERN:
                    dunkel.add(nachbar)
        for p in stempel:
            besitzer[p] = i
            dunkel.discard(p)
        if abs(i - MITTE) % ZOPF == 2 and abs(i - MITTE) <= ZOPF_WEIT:           # Zopf: Kerbe mitten im Bauch
            kerben.append((B - 2 - x0 if rechts else x0 + 1, y0 + 1))
    dunkel.update(p for p in kerben if abs(besitzer[p] - MITTE) <= BAUCH)       # nicht, wo ein Arm darüber liegt
    for (px, py) in besitzer:
        farbe = SCHATTEN[stufe] if (px, py) in dunkel else TEIG[stufe]
        if glanz is not None and 0 <= px + py - glanz < 2 and (px, py) not in dunkel:
            farbe = GLANZ
        bild.setze(px, py + dy, farbe)


def _zwischen(a, b, t):
    return [(xa + (xb - xa) * t, ya + (yb - ya) * t) for (xa, ya), (xb, yb) in zip(a, b)]


def _form(f):
    """Der Strang, während die Hände ihn schlingen: erst beide Enden anheben, dann legt die linke
    Hand ihr Ende über Kreuz auf den Bauch, die rechte folgt."""
    a = _sanft((f - T_HEBEN) / (T_KREUZ - T_HEBEN - 3))
    punkte = []
    for i in range(N):
        w = max(0.0, min(1.0, (i - 50) / 20))
        b = _sanft((f - T_KREUZ - w * VERSATZ) / KREUZ_DAUER)
        x = GERADE[i][0] + (BOGEN[i][0] - GERADE[i][0]) * a
        y = GERADE[i][1] + (BOGEN[i][1] - GERADE[i][1]) * a
        punkte.append((x + (BREZEL[i][0] - x) * b, y + (BREZEL[i][1] - y) * b))
    return punkte


def _hand(bild, x, y, daumen):
    """Hand am Strangende mit Daumen zur Mitte hin, der Arm kommt von unten."""
    x0, y0 = math.floor(x) - 1, math.floor(y) - 1
    bild.rechteck(x0, y0, 3, 3, HAUT)
    bild.setze(x0 + 1 + 2 * daumen, y0 + 1, HAUT)
    bild.rechteck(x0, y0 + 3, 3, 16, AERMEL)


# ── Ofen ───────────────────────────────────────────────────────────
def _ofen(bild, ox, hitze, uhr):
    """Ofen von vorn, um ox nach rechts verschoben: Griff, Fenster, Uhr und Lampe; hitze 0–3."""
    bild.rechteck(ox, 0, B, 16, OFEN)
    bild.rechteck(ox + FENSTER_X - 1, 0, FENSTER_B + 2, 16, RAHMEN)
    bild.rechteck(ox + FENSTER_X, 0, FENSTER_B, 16, mischen(DUNKEL, GLUT, hitze / 3))
    bild.rechteck(ox + 5, 3, 2, 10, RAHMEN)                          # Griff
    bild.rechteck(ox + KNOPF_X, KNOPF_Y, 3, 3, RAHMEN)               # Uhr mit Zeiger
    bild.setze(ox + KNOPF_X + ZEIGER[uhr % 8][0], KNOPF_Y + ZEIGER[uhr % 8][1], ROT)
    bild.rechteck(ox + KNOPF_X, 10, 3, 2, ROT if hitze else LAMPE_AUS)


def _heizung(bild, hitze, f):
    """Heizstäbe oben und unten im Fenster, daneben je eine Zeile Widerschein."""
    stab = mischen(GLUT, STAB[(f // 8) % 2], hitze / 3)
    for y, anteil in ((0, 1.0), (15, 1.0), (1, 0.35), (14, 0.35)):
        bild.rechteck(FENSTER_X, y, FENSTER_B, 1, mischen(mischen(DUNKEL, GLUT, hitze / 3), stab, anteil))


def bilder():
    # Zuckerkörner: Plätze auf der fertigen Brezel, nicht nebeneinander
    probe = Bild()
    _strang(probe, GROSS, 4, 3)
    plaetze = [(x, y) for x in range(B) for y in range(1, 16) if probe.px[y][x] == TEIG[4]]
    z = random.Random(2027)
    z.shuffle(plaetze)
    koerner = []
    for x, y in plaetze:
        if all(abs(x - kx) + abs(y - ky) > 3 for kx, ky, _, _ in koerner) and len(koerner) < 22:
            weg = (x - BLECH_X) / STREU_TEMPO                        # fällt, wenn die Hand darüber ist:
            start = weg if len(koerner) % 2 == 0 else 2 * STREU_DAUER - weg         # … hin oder zurück
            koerner.append((x, y, start, z.randrange(16)))
    funkeln, frei = [], list(koerner)                                # blitzen darf nur, was schon liegt
    for t in T_FUNKELN:
        korn = next(k for k in frei if T_STREUEN + k[2] + k[1] / 2 < t)
        frei.remove(korn)
        funkeln.append((t, korn[0], korn[1]))

    liste = []
    for f in range(255):
        bild = Bild(TISCH)
        hoch = max(0, min(16, f - T_WEITER + 1))                     # am Ende wird die Brezel nach oben weggetragen
        # Ofen: kommt von rechts ins Bild und geht wieder
        hitze = max(0, min(3, (f - T_OFEN) // 2, (T_HER - 1 - f) // 2))
        if T_HIN <= f < T_TISCH:
            ox = round(B * (1 - _sanft(min(f - T_HIN + 1, T_TISCH - 1 - f) / SCHWENK)))
            _ofen(bild, ox, hitze, max(0, min(8, (f - T_OFEN - 4) // 8)))
        # Blech: schiebt sich von links unter die Brezel
        if f >= T_BLECH:
            bx = BLECH_X - round((BLECH_X + BLECH_B) * (1 - _sanft((f - T_BLECH + 1) / 10)))
            bild.rechteck(bx, -hoch, BLECH_B, 16, mischen(BLECH, GLUT, hitze / 3))
        if hitze:
            _heizung(bild, hitze, f)
        # Strang und Brezel
        if f < T_BLECH:
            _strang(bild, _form(f))
        else:
            stufe = sum(1 for t in T_FARBE if f >= t)
            auf = sum(1 for t in T_AUF if f >= t)
            glanz = next((BLECH_X + (f - t) * 5 for t in T_GLANZ if t <= f < t + GLANZ_DAUER), None)
            _strang(bild, _zwischen(BREZEL, GROSS, auf / 4), stufe, 3 if auf >= 2 else 2, -hoch, glanz)
        if hoch > 12:                                                # der nächste Strang kommt von unten
            _strang(bild, GERADE, dy=16 - hoch)
        # Hände beim Schlingen
        if T_HAND <= f < T_BLECH:
            punkte = _form(f)
            tief = max(0, T_HEBEN - 1 - f) + max(0, f - T_LOS) * 2
            _hand(bild, punkte[0][0], punkte[0][1] + tief, 1)
            _hand(bild, punkte[-1][0], punkte[-1][1] + tief, -1)
        # Hagelzucker
        if f >= T_STREUEN - STREU_VORLAUF:
            g = f - T_STREUEN
            for x, y, start, phase in koerner:
                if g < start:
                    continue
                fy = 2 + (g - start) * 2                             # fällt zwei Zeilen je Bild
                if fy < y:
                    bild.setze(x, fy, WEISS)
                else:                                                # liegt und blinkt ab und zu matt
                    bild.setze(x, y - hoch, ZUCKER_MATT if (f + phase) % 16 < 2 else WEISS)
            if g < 2 * STREU_DAUER + STREU_VORLAUF:                  # die Hand: von links herein, hin und zurück
                hx = BLECH_X - 5 + min(g, 2 * STREU_DAUER - g) * STREU_TEMPO
                bild.rechteck(hx - 2, 0, 3, 1, AERMEL)
                bild.rechteck(hx + 1, 0, 3, 1, HAUT)
                bild.rechteck(hx + 2, 1, 3, 1, HAUT)
            for start, x, y in funkeln:                              # Glitzern: ein Korn blitzt als Kreuz auf
                if start <= f < start + 4:
                    for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        bild.setze(x + ax, y + ay - hoch, WEISS if f - start in (1, 2) else ZUCKER_MATT)
                    bild.setze(x, y - hoch, WEISS)
        liste.append(bild)
    return liste
