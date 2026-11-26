"""Feuerzangenbowle: Ein Kupferkessel mit dunkelroter Bowle steht auf dem Rechaud, quer darüber liegt
die Feuerzange mit dem weißen Zuckerhut, links und rechts wartet je ein leeres Glas. Eine Kelle
gießt Rum auf den Zuckerhut, ein Streichholz zündet ihn an der Spitze an: Blaue Flammenzungen
laufen über den Zuckerhut und tanzen, Zucker tropft karamellfarben durch die Zange in den Kessel
(auf der Bowle brennt es kurz blau nach), der Zuckerhut wird Stufe um Stufe kleiner und schmilzt
weg. Dann wird die Zange abgehoben, die Schöpfkelle füllt beide Gläser, sie heben sich, stoßen über
dem Kessel zweimal an (Funken) und werden fortgetragen; zum Schluss senkt sich die Zange mit einem
neuen Zuckerhut auf den Kessel und zwei frische Gläser rücken heran. Die Runde geht ohne Sprung in
sich über – 255 Bilder.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum schwarzer Grund ohne Tischkante, ein aufgeschnittener Kessel mit
geraden Wänden (gleiche Nachbarspalten, links und rechts gleich), eine waagerechte Zange, ein
Zuckerhut in flachen Stufen, zwei gleiche Kelchgläser und Kellen mit geradem Stiel. Blau sind nur
die Flammen. Das Rechaud flackert im Takt 51, der in 255 aufgeht; alles andere hängt nur an der
Bildnummer, und die letzten Bilder zeigen schon wieder den Anfang.
"""
import math
import random

from basis import B, BLAU, DUNKELROT, GELB, GOLD, ORANGE, SCHWARZ, WEISS, Bild

NAME = "feuerzangenbowle"
TITEL = "Feuerzangenbowle"

RUNDE = 255

KUPFER = (185, 55, 12)
KUPFER_HELL = (255, 115, 45)                   # Rand und Glanz
MESSING = (190, 140, 20)                       # Griffe des Kessels
BOWLE = DUNKELROT
SPIEGEL = (235, 0, 40)                         # Oberfläche der Bowle
WELLE = (255, 90, 90)
METALL = (150, 150, 175)                       # Zange und Kellen
GESTELL = (90, 90, 100)                        # Beine des Rechauds
ZUCKER = (240, 240, 250)
GETRAENKT = (255, 220, 140)                    # vom Rum getränkt
SCHMELZ = (255, 185, 70)                       # unten schmilzt der Zucker
KARAMELL = (255, 140, 0)                       # Tropfen
RUM = (255, 170, 0)
KERN = (90, 220, 255)                          # heißer Kern der großen Flammenzungen
HELL = (0, 170, 255)
TIEF = (0, 25, 170)                            # Spitzen der Flammen
HOLZ = (72, 54, 28)                            # Streichholz: dunkel, sonst leuchtet Holz auf den LEDs orange
GLAS = (185, 190, 200)
FUNKE = (255, 245, 170)
DAMPF = (110, 110, 135)

MITTE = 32
ZANGE_Y = 8
RAND_Y, SPIEGEL_Y, RECHAUD_Y = 9, 11, 15
INNEN_L, INNEN_R = 24, 40                      # Bowle zwischen den Wänden
ZX = 26                                        # Zuckerhut: linke Spalte; er liegt in den drei Zeilen über der Zange

# Kessel im Schnitt (x ab 18): L Rand, C Kupfer, R Bowle, S Spiegel, h Griff
KESSEL = ["..LLLL.................LLLL..",
          ".hhCCC.................CCChh.",
          ".h.CCCSSSSSSSSSSSSSSSSSCCC.h.",
          ".hhCCCRRRRRRRRRRRRRRRRRCCChh.",
          "...CCCRRRRRRRRRRRRRRRRRCCC...",
          "....CCCCCCCCLLLLLCCCCCCCC...."]
KESSEL_FARBEN = {"L": KUPFER_HELL, "C": KUPFER, "R": BOWLE, "S": SPIEGEL, "h": MESSING}

# Zuckerhut liegt auf der Zange, Spitze nach rechts; zehn Stufen, dann ist er weg
STUFEN = [[".XXXXX.......", "XXXXXXXXXX...", "XXXXXXXXXXXXX"],
          ["..XXXX.......", "XXXXXXXXX....", "XXXXXXXXXXXXX"],
          ["..XXX........", ".XXXXXXXX....", "XXXXXXXXXXXX."],
          [".............", ".XXXXXXX.....", ".XXXXXXXXXXX."],
          [".............", "..XXXXXX.....", ".XXXXXXXXXX.."],
          [".............", "..XXXXX......", "..XXXXXXXXX.."],
          [".............", "...XXX.......", "..XXXXXXXX..."],
          [".............", ".............", "...XXXXXXX..."],
          [".............", ".............", "...XXXXX....."],
          [".............", ".............", "....XXX......"]]

# Zeitplan (Bildnummern)
T_RUM_REIN, T_RUM_DA, T_RUM_KIPPT, T_RUM_ENDE, T_RUM_RAUS, T_RUM_FORT = 4, 12, 13, 27, 30, 38
T_HOLZ_REIN, T_ZUEND, T_HOLZ_RAUS, T_HOLZ_FORT = 32, 44, 46, 54
STUFE_AB = [0, 14, 24, 34, 43, 52, 61, 69, 77, 85, 92]       # Bilder nach dem Zünden, ab denen die Stufe gilt
BRENNT = 97                                    # so lange brennt es
T_AUS = T_ZUEND + BRENNT
T_ZANGE_HOCH = T_AUS + 2
T_KELLE = 150
T_HEBEN, T_STOSS1, T_STOSS2, T_GLAS_HOCH = 219, 229, 236, 241
T_ZANGE_KOMMT = 245
T_GLAS_NEU = 244                               # zwei frische Gläser rücken von den Seiten heran

GLAS_X, GLAS_Y = 6, 10                         # linkes Glas (linke obere Ecke), steht unten
STOSS_X, STOSS_Y = 25, 2                       # dort stößt es an
GLAS_FORM = ["G.....G", "G.....G", "G.....G", ".GGGGG.", "...G...", ".GGGGG."]   # Kelch mit Stiel und Fuß
KELLE_L, KELLE_M, KELLE_R = 10, 30, 49         # linke Spalte der Schöpfkelle: über dem linken Glas, im Kessel, rechts
KELLE_OBEN, KELLE_UNTEN = 5, 11                # obere Zeile des Bechers beim Tragen und beim Schöpfen

FLACKERN = [0, 1, 0, 2, 1, 0, 2, 0, 1, 2, 0, 1, 0, 2, 1, 2, 1]     # 17 Schritte zu je 3 Bildern
RECHAUD = [".OGGO.", "OGGGGO", "..GGO."]


def _sanft(a):
    a = max(0.0, min(1.0, a))
    return a * a * (3 - 2 * a)


# ── Kessel, Zange, Zuckerhut ───────────────────────────────────────
def _kessel(bild, f):
    bild.figur(18, RAND_Y, KESSEL, KESSEL_FARBEN)
    bild.setze(INNEN_L - 1, RECHAUD_Y, GESTELL)                     # Rechaud: zwei Beine, dazwischen die Flamme
    bild.setze(INNEN_R + 1, RECHAUD_Y, GESTELL)
    bild.figur(MITTE - 3, RECHAUD_Y, [RECHAUD[FLACKERN[(f // 3) % 17]]], {"G": GELB, "O": ORANGE})


def _zange_y(f):
    """Zeile der Zange; None, solange sie abgehoben ist."""
    if f < T_ZANGE_HOCH:
        return ZANGE_Y
    if f < T_ZANGE_KOMMT:
        y = ZANGE_Y - (f - T_ZANGE_HOCH + 1)
        return y if y >= 0 else None
    return min(ZANGE_Y, f - T_ZANGE_KOMMT)


def _stufe(f):
    """Stufe des Zuckerhuts (0 voll … 9 Rest, 10 weg)."""
    u = f - T_ZUEND
    if u < 0 or f >= T_ZANGE_KOMMT:
        return 0
    return max(s for s, ab in enumerate(STUFE_AB) if u >= ab)


def _zange(bild, f):
    y = _zange_y(f)
    if y is None:
        return
    bild.rechteck(MITTE - 16, y, 33, 1, METALL)
    stufe = _stufe(f)
    if stufe >= len(STUFEN):
        return
    u = f - T_ZUEND
    for dy, zeile in enumerate(STUFEN[stufe]):
        for dx, c in enumerate(zeile):
            if c == ".":
                continue
            x = ZX + dx
            farbe = ZUCKER
            if T_RUM_KIPPT + 2 <= f < T_ZANGE_KOMMT:
                if u < (12 - dx) * 0.7:                             # getränkt, bis die Flamme da ist
                    if abs(x - MITTE) <= (f - T_RUM_KIPPT - 2) * 0.8:
                        farbe = GETRAENKT
                elif dy == 2:                                       # unten schmilzt er
                    farbe = SCHMELZ
            bild.setze(x, y - 3 + dy, farbe)


# ── Flammen und Tropfen ────────────────────────────────────────────
def _flammen(bild, f):
    """Blaue Flammenzungen über dem Zuckerhut: Jede Zunge schwankt hin und her und schlägt mal höher,
    mal niedriger, dazwischen züngelt es flach; ab und zu löst sich oben ein Flämmchen. Fuß hell,
    Spitze dunkelblau – nichts Weißes, damit sich die Flammen vom Zucker abheben."""
    u = f - T_ZUEND
    if u < 0 or u >= BRENNT:
        return
    stufe = _stufe(f)
    weg = stufe >= len(STUFEN)
    form = STUFEN[min(stufe, len(STUFEN) - 1)]
    spalten = [dx for dx, c in enumerate(form[2]) if c != "."]
    links, rechts = spalten[0], spalten[-1]
    breite = rechts - links + 1
    anzahl = 3 if breite >= 9 else (2 if breite >= 6 else 1)
    grund = (0.45 if weg else 0.62 + 0.38 * breite / 13) * min(1.0, (BRENNT - u) / 5)
    zungen = []
    for i in range(anzahl):
        mitte = links + (i + 0.5) * breite / anzahl + 1.3 * math.sin(0.31 * f + 2.4 * i)
        gipfel = grund * (5.0 + 1.3 * math.sin(0.47 * f + 1.9 * i) + 0.8 * math.sin(0.83 * f + 4.1 * i))
        zungen.append((mitte, gipfel))
    spitze = {}
    for dx in range(links - 3, rechts + 4):
        an = u - (12 - dx) * 0.7                                    # die Flamme läuft von der Spitze nach links
        if an < 0:
            continue
        aussen = not links <= dx <= rechts
        oben = ZANGE_Y
        if not aussen and not weg:
            oben = ZANGE_Y - 3 + min(k for k in range(3) if form[k][dx] != ".")
        if aussen:                                                  # neben dem Zucker brennt Rum auf der Zange
            nah = dx in (links - 1, rechts + 1)
            h = ((f // 2 + 2 * dx) % 4 == 0) + (nah and (f // 3 + dx) % 3 != 0)
        else:
            h = 1 + ((f // 2 + dx) % 3 == 0)
        kern = False
        for mitte, gipfel in zungen:
            gipfel *= 1 + 0.3 * max(0.0, 1 - an / 12)               # Stichflamme beim Zünden
            h = max(h, gipfel - 0.8 * (dx - mitte) ** 2)            # runde Zunge mit schmaler Spitze
            kern = kern or abs(dx - mitte) < 0.75
        h *= min(1.0, (an + 1) / 3)
        if h > oben - 1:                                            # unter dem oberen Rand staucht sie sich
            h = oben - 1 + (h - oben + 1) * 0.4
        h = min(oben, round(h))
        spitze[dx] = oben - h
        for k in range(h):
            if k == h - 1 and h >= 3:
                farbe = TIEF
            elif k == 0:
                farbe = HELL
            elif kern and k == 1 and h >= 4:
                farbe = KERN
            elif k < h * 0.45:
                farbe = HELL
            else:
                farbe = BLAU
            bild.setze(ZX + dx, oben - 1 - k, farbe)
    for i, (mitte, gipfel) in enumerate(zungen):                    # Flämmchen lösen sich von den Spitzen
        dx, takt = round(mitte), (f + 3 * i) % 8
        if gipfel >= 3.6 and takt < 2 and dx in spitze and spitze[dx] - 2 - takt >= 0:
            bild.setze(ZX + dx, spitze[dx] - 2 - takt, TIEF if takt else BLAU)


def _tropfen_liste():
    """(Bild nach dem Zünden, Spalte): alle paar Bilder ein Tropfen unter dem Zuckerhut."""
    z = random.Random(11)
    liste, u = [], 10
    while u < BRENNT - 8:
        stufe = max(s for s, ab in enumerate(STUFE_AB) if u >= ab)
        spalten = [dx for dx, c in enumerate(STUFEN[min(stufe, len(STUFEN) - 1)][2]) if c != "."]
        liste.append((u, ZX + z.choice(spalten)))
        u += z.choice([5, 6, 7, 8])
    return liste


TROPFEN = _tropfen_liste()


def _tropfen(bild, f):
    """Karamell tropft durch die Zange in die Bowle; auf dem Spiegel flackert es kurz blau."""
    u = f - T_ZUEND
    for nr, (start, x) in enumerate(TROPFEN):
        t = u - start
        if not 0 <= t < 10:
            continue
        if t < 2:
            bild.setze(x, ZANGE_Y, KARAMELL)                        # hängt an der Zange
        elif t < 5:                                                 # fällt und zieht sich dabei lang
            bild.setze(x, ZANGE_Y + 1 + (t == 4), KARAMELL)
            if t == 3:
                bild.setze(x, ZANGE_Y + 2, KARAMELL)
        else:
            bild.setze(x, SPIEGEL_Y, WELLE)
            if t >= 7:
                bild.setze(x - 1, SPIEGEL_Y, WELLE)
                bild.setze(x + 1, SPIEGEL_Y, WELLE)
            if t < 9:                                               # der Rum brennt auf dem Spiegel kurz nach
                bild.setze(x, SPIEGEL_Y - 1, HELL if t % 2 else BLAU)
                if nr % 2 == 0 and t in (6, 7):
                    bild.setze(x, SPIEGEL_Y - 2, BLAU)


# ── Rumkelle und Streichholz ───────────────────────────────────────
def _rumkelle(bild, f):
    if not T_RUM_REIN <= f < T_RUM_FORT:
        return
    if f < T_RUM_DA:
        x0 = round(-6 + 33 * _sanft((f - T_RUM_REIN + 1) / (T_RUM_DA - T_RUM_REIN)))
    elif f < T_RUM_RAUS:
        x0 = 27
    else:
        x0 = round(27 - 33 * _sanft((f - T_RUM_RAUS + 1) / (T_RUM_FORT - T_RUM_RAUS)))
    bild.rechteck(0, 0, x0 + 1, 1, METALL)                          # Stiel von links
    if T_RUM_KIPPT <= f < T_RUM_ENDE + 2:                           # gekippt: der Rum läuft über die Lippe
        bild.rechteck(x0 + 1, 1, 2, 1, METALL)
        bild.rechteck(x0 + 3, 2, 2, 1, METALL)
        if f < T_RUM_ENDE:
            if f < T_RUM_ENDE - 5:
                bild.rechteck(x0 + 3, 1, 2, 1, RUM)
            bild.rechteck(x0 + 5, 2, 1, 4, RUM)
    else:                                                           # waagerecht: drei Zeilen tiefer Becher
        bild.setze(x0 + 4, 0, METALL)
        bild.setze(x0, 1, METALL)
        bild.setze(x0 + 4, 1, METALL)
        bild.rechteck(x0 + 1, 2, 3, 1, METALL)
        if f < T_RUM_KIPPT:
            bild.rechteck(x0 + 1, 1, 3, 1, RUM)


def _streichholz(bild, f):
    if not T_HOLZ_REIN <= f < T_HOLZ_FORT:
        return
    if f < T_ZUEND:
        a = _sanft((f - T_HOLZ_REIN + 1) / (T_ZUEND - T_HOLZ_REIN))
    elif f < T_HOLZ_RAUS:
        a = 1
    else:
        a = 1 - _sanft((f - T_HOLZ_RAUS + 1) / (T_HOLZ_FORT - T_HOLZ_RAUS))
    x, y = round(51 - 12 * a), round(-3 + 9 * a)
    for k in range(1, 6):
        bild.setze(x + k, y - k + 1, HOLZ)
    bild.setze(x, y, GELB)
    bild.setze(x, y - 1, GELB)
    bild.setze(x - (f % 2), y - 2 + (f % 2), ORANGE)


# ── Gläser und Schöpfkelle ─────────────────────────────────────────
def _glas(bild, x, y, stand):
    """Kelchglas; stand = Zeilen Bowle (0–2)."""
    bild.figur(x, y, GLAS_FORM, {"G": GLAS})
    for k in range(stand):
        bild.rechteck(x + 1, y + 2 - k, 5, 1, SPIEGEL if k == stand - 1 else BOWLE)


# Schöpfkelle: (Dauer, Spalte von, Spalte bis, Zeile von, Zeile bis, gefüllt, gießt)
KELLE_WEG = [(7, KELLE_M, KELLE_M, -3, KELLE_UNTEN, False, False),          # taucht ein
             (2, KELLE_M, KELLE_M, KELLE_UNTEN, KELLE_UNTEN, True, False),
             (4, KELLE_M, KELLE_M, KELLE_UNTEN, KELLE_OBEN, True, False),
             (10, KELLE_M, KELLE_L, KELLE_OBEN, KELLE_OBEN, True, False),    # zum linken Glas
             (9, KELLE_L, KELLE_L, KELLE_OBEN, KELLE_OBEN, True, True),
             (10, KELLE_L, KELLE_M, KELLE_OBEN, KELLE_OBEN, False, False),
             (3, KELLE_M, KELLE_M, KELLE_OBEN, KELLE_UNTEN, False, False),
             (2, KELLE_M, KELLE_M, KELLE_UNTEN, KELLE_UNTEN, True, False),
             (3, KELLE_M, KELLE_M, KELLE_UNTEN, KELLE_OBEN, True, False),
             (10, KELLE_M, KELLE_R, KELLE_OBEN, KELLE_OBEN, True, False),    # zum rechten Glas
             (9, KELLE_R, KELLE_R, KELLE_OBEN, KELLE_OBEN, True, True),
             (5, KELLE_R, KELLE_R, KELLE_OBEN, -4, False, False)]            # nach oben weg


def _kelle_lage(f):
    """Schöpfkelle: (linke Spalte, obere Zeile des Bechers, gefüllt, gießt seit n Bildern oder None)."""
    t = f - T_KELLE
    if t < 0:
        return None
    for dauer, x0, x1, y0, y1, voll, giesst in KELLE_WEG:
        if t < dauer:
            a = (t + 1) / dauer
            if x0 != x1:
                a = _sanft(a)
            if giesst:
                return x0, y0, t < 6, t
            return round(x0 + (x1 - x0) * a), round(y0 + (y1 - y0) * a), voll, None
        t -= dauer
    return None


def _giesst_ab(rechts):
    """Bildnummer, ab der ins linke oder rechte Glas gegossen wird."""
    n = 0
    for nr, schritt in enumerate(KELLE_WEG):
        if schritt[6] and (nr > 5) == rechts:
            return T_KELLE + n
        n += schritt[0]


def _glas_stand(f, rechts):
    t = f - _giesst_ab(rechts)
    return 0 if t < 3 else (1 if t < 6 else 2)


def _kelle(bild, f):
    lage = _kelle_lage(f)
    if lage is None:
        return
    x, y, voll, giesst = lage
    bild.rechteck(x + 2, 0, 1, y + 1, METALL)                       # Stiel von oben
    bild.setze(x, y, METALL)
    bild.setze(x + 4, y, METALL)
    bild.setze(x, y + 1, METALL)
    bild.setze(x + 4, y + 1, METALL)
    bild.rechteck(x + 1, y + 2, 3, 1, METALL)
    if voll:
        bild.rechteck(x + 1, y + 1, 3, 1, SPIEGEL)
    if giesst is not None and giesst < 8:                           # Strahl über die Lippe ins Glas
        sx = x - 1 if x < MITTE else x + 5
        oben = y + 1 + max(0, giesst - 5) * 3
        unten = min(GLAS_Y + 2, y + 2 + giesst * 3)
        bild.rechteck(sx, oben, 1, unten - oben + 1, SPIEGEL)


def _glaeser(bild, f):
    """Zwei Gläser stehen leer neben dem Kessel, werden gefüllt, heben sich (erst hoch, dann zur
    Mitte, so bleiben sie über dem Kesselrand), stoßen zweimal an und werden nach oben fortgetragen;
    zum Schluss rücken zwei frische Gläser von den Seiten heran."""
    if f >= T_GLAS_NEU:
        x = round(-9 + (GLAS_X + 9) * _sanft((f - T_GLAS_NEU + 1) / (RUNDE - 1 - T_GLAS_NEU)))
        _glas(bild, x, GLAS_Y, 0)
        _glas(bild, B - 7 - x, GLAS_Y, 0)
        return
    if f < T_HEBEN:
        x, y = GLAS_X, GLAS_Y
    elif f < T_GLAS_HOCH:
        a = (f - T_HEBEN) / (T_STOSS1 - T_HEBEN)
        auf = (0, 1, 2, 2, 2, 2, 1, 0)[f - T_STOSS1] if T_STOSS1 <= f <= T_STOSS2 else 0
        x = round(GLAS_X + (STOSS_X - GLAS_X) * _sanft(a)) - auf
        y = round(GLAS_Y + (STOSS_Y - GLAS_Y) * _sanft(a * 2))
    else:
        x, y = STOSS_X, STOSS_Y - 2 * (f - T_GLAS_HOCH + 1)
        if y < -6:
            return
    _glas(bild, x, y, _glas_stand(f, False))
    _glas(bild, B - 7 - x, y, _glas_stand(f, True))
    if _giesst_ab(False) + 12 <= f < T_HEBEN:                       # das volle Glas dampft, sobald die Kelle weg ist
        for k in (0, 5):
            t = (f + k) % 10
            if t < 6:
                bild.setze(GLAS_X + 2 + (k > 0) * 2 + (t // 2) % 2, GLAS_Y - 2 - t // 2, DAMPF)
    for stoss in (T_STOSS1, T_STOSS2):                              # Funken über der Stelle, an der sie sich treffen
        t = f - stoss
        if t == 0:
            bild.rechteck(MITTE - 1, y - 1, 2, 1, WEISS)
        elif t == 1:
            bild.rechteck(MITTE - 1, y - 2, 2, 1, FUNKE)
            bild.setze(MITTE - 3, y - 1, GELB)
            bild.setze(MITTE + 2, y - 1, GELB)
        elif t == 2:
            for dx, dy in ((-2, -3), (1, -3), (-4, -2), (3, -2)):
                bild.setze(MITTE + dx, y + dy, GOLD)


def bilder():
    liste = []
    for f in range(RUNDE):
        bild = Bild(SCHWARZ)
        _kessel(bild, f)
        _tropfen(bild, f)
        _zange(bild, f)
        _flammen(bild, f)
        _rumkelle(bild, f)
        _streichholz(bild, f)
        _kelle(bild, f)
        _glaeser(bild, f)
        liste.append(bild)
    return liste
