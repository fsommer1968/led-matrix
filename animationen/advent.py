"""Adventskranz: vier Kerzen werden nacheinander angezündet und flackern – 255 Bilder.

Kranz aus Tannengrün mit roten Beeren, goldenen Kugeln und roter Schleife; dicke rote Kerzen
mit tropfenförmiger Flamme und warmem Hof; mit jeder brennenden Kerze wird der Kranz heller.

Größe (23.11.2026): Die Matrix speichert je Animation nur 80 KB und komprimiert jedes Bild
einzeln, spaltenweise. Deshalb wiederholt sich das Tannengrün alle 5 Spalten, Beeren und Kugeln
sitzen im selben Raster wie die Kerzen (15 Spalten), der Kranz ist überall gleich hell, der
Flammenhof hat eine Farbe, und es funkeln nur acht Sterne – so bleiben advent1–4 unter 76000 Bytes
(vorher 146000–174000).

VARIANTEN advent1 … advent4 (23.11.2026): für die n-te Adventswoche brennen n Kerzen –
die Kerzen fallen nacheinander auf den Kranz, die der vergangenen Sonntage zündet ein Streichholz
zügig im Vorbeiziehen an, die neue wird feierlich entzündet (Streichholz reißt an, nähert sich
langsam, die Flamme wächst, goldene Funken); ohne Text, die Kerzen erklären sich selbst
(23.11.2026). Ohne n (klassisch): vier Kerzen nacheinander, am Ende "ADVENT".
"""
import math
import random

from basis import B, GOLD, WEISS, Bild, dimmen, mischen, textbreite

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "advent"
TITEL = "Adventskranz mit vier Kerzen"
VARIANTEN = [(f"advent{n}", f"Adventskranz {n}. Advent ({n} Kerze{'n' if n > 1 else ''}, ohne Text)", {"n": n})
             for n in range(1, 5)]

KERZENROT = (200, 0, 30)
KERZEN = [(7, KERZENROT), (22, KERZENROT), (37, KERZENROT), (52, KERZENROT)]   # linke Kante, 5 breit
KB = 5                                      # Kerzenbreite
OBEN, UNTEN = 6, 12                         # Kerze von Zeile OBEN bis UNTEN (unten im Kranz)
ZUEND = [15, 60, 105, 150]
HINTERGRUND = (6, 2, 14)
WARM = (255, 120, 0)
STERNE = [(1, 1, 0), (15, 0, 9), (18, 3, 20), (31, 1, 5), (34, 3, 27), (46, 0, 14), (48, 2, 31),
          (61, 1, 18)]                      # (Spalte, Zeile, Phase) – zwischen den Flammen


def sterne(bild, f):
    """Wenige Sterne in zwei Helligkeiten, zeitweise aus (jeder Stern kostet in jedem Bild Platz)."""
    for x, y, phase in STERNE:
        t = (f + phase) % 36
        if t < 26:
            bild.setze(x, y, (255, 240, 200) if 8 <= t < 18 else (128, 120, 100))


# Kranz: Tannengrün als Kachel, die sich alle 5 Spalten wiederholt, aus nur drei verschiedenen
# Spalten (A B A C B). Die Matrix komprimiert jedes Bild einzeln und spaltenweise: gleiche Spalten
# kosten fast nichts, ein unregelmäßiges Nadelmuster dagegen in jedem der 255 Bilder (Größengrenze
# 76000 Bytes je Animation, 23.11.2026). Zeilen 11–15: d dunkel, m mittel, l hell, . frei.
SPALTE = {"A": "mlmdd", "B": ".mdld", "C": "..lmd"}
KACHEL = "ABACB"
ENDE = ("...md", "..lmd")                   # runde Enden: äußerste und zweite Spalte, beidseits gleich
NADEL = {"d": (0, 60, 14), "m": (0, 120, 22), "l": (20, 180, 40)}
BEEREN = [3, 13, 43, 58]                    # je zwei rote Beeren in Zeile 13
KUGELN = [17, 47]                           # goldene Kugeln 2×2
SCHLEIFE = ["rr..rr", "rrkkrr", "rr..rr"]


def stufen(wert, n):
    """Rundet auf n Stufen je 1,0 – hält die Zahl der Farben klein (GIF-Palette 256)."""
    return round(wert * n) / n


def kerzenlicht(brennend):
    """Helligkeit 0…1 des ganzen Kranzes: jede brennende Kerze macht ihn heller (die erste am
    meisten); brennend = [(mitte, stärke)]. Der Kranz ist in einem Bild überall gleich hell –
    ein Lichtfleck je Kerze würde jede Spalte anders machen und zu viel Speicher kosten."""
    return stufen((sum(min(1.0, stufen(s, 4)) for _, s in brennend) / 4) ** 0.6, 16)


def kranz(bild, f, brennend=()):
    licht = kerzenlicht(brennend)
    hell = 0.55 + 0.6 * licht
    gruen = {c: dimmen(farbe, hell) for c, farbe in NADEL.items()}
    oben = {c: mischen(farbe, WARM, 0.12 * licht) for c, farbe in gruen.items()}   # warm angestrahlt
    for x in range(1, B - 1):
        rand = min(x - 1, B - 2 - x)
        spalte = ENDE[rand] if rand < 2 else SPALTE[KACHEL[(x + 2) % 5]]
        for dy, c in enumerate(spalte):
            if c != ".":
                bild.setze(x, 11 + dy, (oben if dy < 2 else gruen)[c])
    hell = 0.7 + 0.3 * licht
    for x in BEEREN:
        bild.rechteck(x, 13, 2, 1, dimmen((255, 0, 0), hell))
    for i, x in enumerate(KUGELN):
        bild.rechteck(x, 13, 2, 2, dimmen(GOLD, hell))
        bild.setze(x, 13, WEISS if (f // 8 + i * 3) % 6 == 0 else dimmen((255, 210, 80), hell))
    bild.figur(29, 13, SCHLEIFE, {"r": dimmen((255, 0, 20), hell), "k": dimmen((150, 0, 10), hell)})


def flamme(bild, cx, alter, z, langsam=False):
    """Tropfenförmige Flamme über der Kerzenmitte cx; alter = Bilder seit dem Zünden."""
    stufe = alter // (7 if langsam else 3)                         # 0 Funke, 1, 2 klein, ab 3 voll
    if stufe == 0:
        bild.setze(cx + z.choice((-1, 0, 1)), 5 - alter % 2, (255, 255, 180))
        bild.setze(cx, 5, (255, 200, 60))
        return 0.3
    bild.setze(cx, 5, (255, 220, 60))
    if stufe == 1:
        bild.setze(cx, 4, (255, 140, 0))
        return 0.5
    form = z.choice((0, 0, 0, 1, 2, 3)) if stufe >= 3 else 0       # 0 ruhig, 1 hoch, 2/3 geneigt
    neigung = {2: -1, 3: 1}.get(form, 0)
    orange, gelb = (255, 130, 0), (255, 220, 60)
    bild.setze(cx, 4, (255, 250, 200))
    bild.setze(cx - 1, 4, orange)
    bild.setze(cx + 1, 4, orange)
    bild.setze(cx, 3, gelb)
    if stufe == 2:
        return 0.75
    bild.setze(cx - 1, 3, orange if neigung <= 0 else None)
    bild.setze(cx + 1, 3, orange if neigung >= 0 else None)
    bild.setze(cx + neigung, 2, orange)
    if form == 1:
        bild.setze(cx, 2, gelb)
        bild.setze(cx, 1, (230, 60, 0))
    return z.choice((0.9, 1.0))


SCHEIN = (52, 22, 8)                        # warmer Hof um die Flamme: eine Farbe, feste Form
HOF = ((-2, 3), (-2, 4), (-1, 2), (-1, 3), (-1, 4), (-1, 5), (0, 1), (0, 2),
       (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4))
HOF_KLEIN = ((-1, 4), (-1, 5), (0, 3), (1, 4), (1, 5))             # solange die Flamme noch wächst


def kerze(bild, x, farbe, brennt_seit, z, f, dy=0, langsam=False):
    """Kerze mit linker Kante x; liefert die Stärke ihres Scheins (0 = aus).

    Wenige Farben und immer dieselbe Form: so gleichen sich die Spalten der vier Kerzen, und die
    Matrix speichert die zweite bis vierte fast umsonst (früher: weicher Schein in 32 Stufen und
    drei Wärmestufen am Kerzenkopf)."""
    an = brennt_seit is not None
    licht, schatten = mischen(dimmen(farbe, 1.3), (255, 170, 90), 0.15), dimmen(farbe, 0.6)
    bild.rechteck(x, OBEN + dy, KB, UNTEN - OBEN + 1, farbe)
    bild.rechteck(x, OBEN + dy, 1, UNTEN - OBEN + 1, licht)                 # Licht links
    bild.rechteck(x + KB - 1, OBEN + dy, 1, UNTEN - OBEN + 1, schatten)     # Schatten rechts
    bild.rechteck(x + 1, OBEN + dy, KB - 2, 1, (255, 150, 70) if an else dimmen(farbe, 1.15))
    cx = x + KB // 2
    if not an:
        bild.setze(cx, OBEN - 1 + dy, (110, 85, 60))               # Docht
        return 0.0
    bild.rechteck(x + 1, OBEN + 1 + dy, KB - 2, 1, mischen(farbe, (255, 130, 40), 0.3))  # vom Feuer erhellt
    staerke = flamme(bild, cx, brennt_seit, z, langsam)
    for dx, yy in HOF if staerke >= 0.75 else HOF_KLEIN if staerke >= 0.5 else ():
        if bild.hole(cx + dx, yy) == HINTERGRUND:
            bild.setze(cx + dx, yy, SCHEIN)
    return staerke


def zuendzeiten(n):
    """Wann jede Kerze angeht (None = bleibt aus): frühere zügig, die neue feierlich."""
    if n is None:
        return list(ZUEND)
    zeiten = [55 + k * 8 for k in range(n - 1)] + [NEU]
    return zeiten + [None] * (4 - n)


EINLAUF = [4, 14, 24, 34]                   # Kerzen fallen nacheinander auf den Kranz (Varianten)
FALL = 10                                   # Bilder je Fall
NEU = 100                                   # die Kerze der Woche wird hier entzündet


def einlauf_versatz(f, start):
    """Versatz nach oben während des Falls (None = noch nicht da), mit kleinem Aufprall."""
    t = f - start
    if t < 0:
        return None
    if t < FALL:
        return -round(14 * (1 - (t / FALL) ** 2))
    return -1 if t == FALL else 0


HOLZ = (66, 50, 31)


def streichholz(bild, kx, ky, brennt=True, f=0):
    """Streichholz mit Kopf bei (kx, ky), Stiel nach rechts oben, Flämmchen darüber."""
    kx, ky = round(kx), round(ky)
    for k in range(1, 6):
        bild.setze(kx + k, ky - k, HOLZ if k > 1 else (150, 90, 40))
    if brennt:
        bild.setze(kx, ky, (255, 240, 170))
        bild.setze(kx, ky - 1, (255, 200, 40))
        bild.setze(kx + (f // 2) % 2 - (f // 3) % 2, ky - 2, (255, 120, 0))
    else:
        bild.setze(kx, ky, (90, 40, 20))


def rauch(bild, x, y, t):
    """Rauchfähnchen nach dem Ausblasen, t = Bilder seit dem Erlöschen."""
    for k in range(3):
        a = t - k * 2
        if 0 <= a < 9:
            bild.setze(x + round(math.sin((a + k) / 1.5)), y - a // 2 - k,
                       dimmen((150, 150, 170), stufen(1 - a / 10, 4)))


def zuegig(bild, f, n):
    """Ein Streichholz zieht von links über die Kerzen der vergangenen Sonntage."""
    if n < 2:
        return
    ende = 55 + (n - 2) * 8                                        # letzte frühere Kerze
    x = KERZEN[0][0] + 2 + (f - 55) * 15 / 8
    if 47 <= f <= ende + 3:
        streichholz(bild, x, 4, f=f)
    elif ende + 3 < f <= ende + 8:
        xe = KERZEN[0][0] + 2 + (ende + 3 - 55) * 15 / 8 + (f - ende - 3)
        streichholz(bild, xe, 4 - (f - ende - 3), brennt=False)
        rauch(bild, round(xe), 3 - (f - ende - 3), f - ende - 3)


def feierlich(bild, f, cx):
    """Das Streichholz für die neue Kerze: anreißen, langsam nähern, halten, wegnehmen, ausblasen."""
    t = f - NEU
    if -19 <= t < -15:                                             # anreißen: heller Blitz
        k = t + 19
        mx, my = cx + 7, 2
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)) + (((2, 0), (-2, 0)) if k in (1, 2) else ()):
            bild.setze(mx + dx, my + dy, (255, 255, 200) if dx == dy == 0 or k in (1, 2) else (255, 180, 60))
    elif -15 <= t < 0:                                             # nähert sich langsam dem Docht
        a = min(1.0, (t + 15) / 11)
        streichholz(bild, cx + 7 - 6 * a, 2 + 2.6 * a, f=f)
    elif 0 <= t < 6:                                               # hält am Docht
        streichholz(bild, cx + 1, 5, f=f)
    elif 6 <= t < 14:                                              # zieht sich zurück
        streichholz(bild, cx + 1 + (t - 6), 5 - (t - 6) * 0.6, f=f)
    elif 14 <= t < 24:                                             # ausgeblasen, Rauch steigt
        streichholz(bild, cx + 9, 0, brennt=False)
        rauch(bild, cx + 9, 0, t - 14)
    if 24 <= t < 48:                                               # goldene Funken um die neue Flamme
        r = 3 + (t - 24) / 4
        for k in range(8):
            w = k * math.pi / 4 + t / 9
            x, y = cx + r * 1.5 * math.cos(w), 3.5 + r * 0.7 * math.sin(w)
            if bild.hole(x, y) == HINTERGRUND or (bild.hole(x, y) or (99,))[0] < 90 and y < 6:
                bild.setze(x, y, dimmen((255, 210, 90), max(0.25, stufen(1 - (t - 24) / 26, 5))))


def staub(bild, x, t):
    """Aufprall: Nadeln spritzen links und rechts hoch (t = Bilder seit dem Aufsetzen)."""
    if 0 <= t < 5:
        hoch = (0, 1, 2, 2, 1)[t]
        for sx, r in ((x - 1 - t, -1), (x + KB + t, 1)):
            bild.setze(sx, 11 - hoch, (120, 255, 120) if t < 3 else (40, 150, 50))
            if t < 3:
                bild.setze(sx + r, 12 - hoch, (40, 150, 50))


def bilder(n=None):
    zeiten = zuendzeiten(n)
    text = "ADVENT" if n is None else None
    text_ab = 185
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        if f >= (160 if n is None else NEU + 50):
            sterne(bild, f)
        brennend = []
        for i, ((x, farbe), zuend) in enumerate(zip(KERZEN, zeiten)):
            z = random.Random((f // 2) * 31 + i * 7)               # Flackern alle zwei Bilder
            an = zuend is not None and f >= zuend
            dy = 0 if n is None else einlauf_versatz(f, EINLAUF[i])
            if dy is None:
                continue
            neu = n is not None and zuend == NEU
            s = kerze(bild, x, farbe, f - zuend if an else None, z, f, dy, langsam=neu)
            if s:
                brennend.append((x + 2, s))
            if n is not None:
                staub(bild, x, f - EINLAUF[i] - FALL)
        kranz(bild, f, brennend)
        if n is not None:
            zuegig(bild, f, n)
            feierlich(bild, f, KERZEN[n - 1][0] + 2)
        if text and f >= text_ab:                                   # Schrift vor den Kerzen
            k = min(len(text), (f - text_ab) // 4 + 1)
            x0 = (B - textbreite(text)) // 2 + 1
            bild.rechteck(x0 - 2, 0, textbreite(text[:k]) + 4, 10, HINTERGRUND)   # ruhiger Grund
            bild.text(x0, 2, text[:k],
                      lambda i: mischen(GOLD, (255, 240, 160), stufen(0.5 + 0.5 * math.sin(f / 5 + i), 2)))
        liste.append(bild)
    return liste
