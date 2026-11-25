"""Bescherung: Zwei Kinder im gestreiften Schlafanzug (eins mit Zipfelmütze) stehen im dunklen Flur
vor der geschlossenen Wohnzimmertür, treten von einem Fuß auf den anderen, und das kleine späht
durchs Schlüsselloch (Licht im Schlüsselloch und unter der Tür). Das goldene Glöckchen über der
Tür klingelt, die Tür schwingt auf, das Licht breitet sich aus, und rechts strahlt der Christbaum
mit brennenden Kerzen und Kugeln neben einem Berg Geschenke. Die Kinder hüpfen jubelnd hinein,
das kleine reißt ein Geschenk auf (Papierfetzen fliegen, ein Teddy kommt zum Vorschein) und hält
ihn hoch. Dann laufen sie zurück, das Zimmer verschwindet, die Tür geht langsam wieder zu, und
die Kinder warten wieder davor. Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum einfarbige Wände, der Baum in einer Farbe und aus
Spaltenpaaren (immer zwei gleiche Spalten nebeneinander), Kerzen und Kugeln zwei Spalten breit,
Geschenke mit waagerechtem Band, Streifen der Schlafanzüge waagerecht, neun Papierfetzen. Die
Flammen wechseln zwischen zwei deutlich verschiedenen Farben (die Matrix kennt nur 32
Helligkeitsstufen), in drei Gruppen.
"""
import random

from basis import B, GELB, GOLD, HAUT, PINK, ROT, WEISS, Bild

NAME = "bescherung"
TITEL = "Bescherung"

FLUR = (6, 8, 40)                              # Wand im dunklen Flur
ZIMMER = (70, 20, 6)                           # Wand im Wohnzimmer, warm
BODEN = (95, 48, 15)
RAHMEN = (165, 90, 30)
TUER = (105, 48, 10)
LICHT = (240, 160, 40)                         # Lichtschein in der offenen Tür
TANNE = (0, 120, 30)
STAMM = (120, 60, 15)
FLAMME_HELL = (255, 255, 150)
GLOCKE_GOLD = (255, 200, 0)
BLAU = (0, 90, 255)
LILA = (170, 0, 255)
BAND = (200, 210, 240)
FELL = (215, 125, 40)
AUGE = (50, 25, 10)

# Tür: Rahmen x = 14 und 23, Blatt x = 15…22 (Angel rechts), Zeile 4 Rahmen oben, Blatt 5…14
TX, TB, TY = 15, 8, 5
KNAUF, LOCH = (16, 10), (16, 12)
GLOCKE_X = 15                                  # Glöckchen über der Tür, 7 Spalten breit
GLOCKE = {0: ["..ggg..", "..ggg..", ".ggggg.", "...w..."],
          -1: ["..ggg..", ".ggg...", "ggggg..", ".w....."],
          1: ["..ggg..", "...ggg.", "..ggggg", ".....w."]}
SCHWUNG = [-1, -1, -1, 0, 1, 1, 1, 0]          # acht Bilder je Hin und Her
ZX = 24                                        # ab hier das Wohnzimmer

# Baum: in Zeile y = 2…13 von M − 2n bis M + 1 + 2n, immer zwei gleiche Spalten nebeneinander
M = 54
STUFEN = [0, 0, 1, 1, 2, 1, 2, 2, 3, 2, 3, 3]
KERZEN = [(-2, 5, 0), (2, 5, 1), (0, 7, 2), (-3, 9, 1), (3, 9, 0), (-1, 11, 2), (1, 11, 0)]   # Paar, y Flamme, Gruppe
KUGELN = [(-1, 9, PINK), (1, 9, BLAU)]                           # Paar, y, Farbe (2×1)

# Geschenke: (x, y oben, Breite, Höhe, Papier, Band, Zeile des Bands)
GA = (36, 10, 6, 5, ROT, GELB, 12)             # dieses wird aufgerissen
GESCHENKE = [(42, 11, 6, 4, BLAU, BAND, 12), (43, 8, 4, 3, LILA, GELB, 9)]
TEDDY = ["b...b", "bbbbb", "bkhkb", ".rrr.", "bbbbb", "bb.bb"]
TEDDY_FARBEN = {"b": FELL, "k": AUGE, "h": (255, 200, 130), "r": ROT}
TEDDY_PLATZ = (36, 9)

# Kinder (Blick nach rechts), fünf Spalten breit, der Körper in den mittleren drei
K1 = {"m": ROT, "w": WEISS, "s": HAUT, "a": AUGE, "p": (0, 140, 255), "q": BAND, "f": HAUT}
K2 = {"h": (255, 200, 40), "s": HAUT, "a": AUGE, "p": (255, 0, 160), "q": (255, 170, 220), "f": HAUT}
KOPF1 = [".mmm.", "mssa.", "wsss.", ".qqq.", ".ppp.", ".qqq."]
KOPF2 = [".hhh.", "hhsa.", ".ppp.", ".qqq.", ".ppp."]
BEINE = [".p.p.", ".f.f."]
TRITT = [[".f.p.", "...f."], [".p.f.", ".f..."]]
STEHT1, STEHT2 = KOPF1 + BEINE, KOPF2 + BEINE
TRITT1 = [KOPF1 + t for t in TRITT]
TRITT2 = [KOPF2 + t for t in TRITT]
JUBEL1 = ["smmms", "pssap", "wsss.", ".qqq.", ".ppp.", ".qqq."] + BEINE
JUBEL2 = ["shhhs", "phsap", ".ppp.", ".qqq.", ".ppp."] + BEINE
SPAEHT2 = [[".ppp...", ".qqqhhh", ".pppssa"] + t for t in ([".p.p...", ".f.f..."], [".p.f...", ".f....."])]
REISST2 = [[".hhh..", "hhsa..", ".pppps", ".qqq..", ".ppp..", ".p.p..", ".f.f.."],
           [".hhh..", "hhsa.s", ".pppp.", ".qqq..", ".ppp..", ".p.p..", ".f.f.."]]

# Ablauf (Bildnummern)
WARTET = 234                                   # ab hier stehen beide wieder vor der Tür (bis GLOCKE_AB)
TRITT_AB = 8                                   # so viele Bilder danach beginnt das Treten
SPAEHT_AB, SPAEHT_BIS = 8, 28
GLOCKE_AB, GLOCKE_BIS = 34, 64
TUER_AUF, LICHT_AB = 56, 62
REIN2, REIN1, DRIN2, DRIN1 = 66, 70, 98, 102
JUBEL_BIS, REISST_AB, FREI = 128, 132, 158
HEBT_AB, HOCH, SENKT_AB, UNTEN = 160, 166, 196, 202
RAUS1, RAUS2 = 202, 204
DUNKEL_AB, TUER_ZU = 214, 234
X1_FLUR, X2_FLUR, X1_ZIMMER, X2_ZIMMER = 1, 7, 25, 30


def fetzen_plan():
    z = random.Random(12)
    plan = []
    for k in range(9):
        plan.append((REISST_AB + 2 + k * 3, z.choice([-1, 1]) * z.uniform(0.25, 0.8), -z.uniform(0.8, 1.3),
                     GELB if k % 3 == 2 else ROT))
    return plan


FETZEN = fetzen_plan()


def teddy(bild, x, y):
    bild.figur(round(x), round(y), TEDDY, TEDDY_FARBEN)


def zimmer(f):
    """Das ganze Wohnzimmer als Bild (die Tür und das Licht geben davon frei, was zu sehen ist)."""
    bild = Bild(ZIMMER)
    for r, n in enumerate(STUFEN):
        bild.rechteck(M - 2 * n, 2 + r, 2 + 4 * n, 1, TANNE)
    bild.rechteck(M, 14, 2, 1, STAMM)
    bild.rechteck(M, 0, 2, 2, WEISS if (f // 6) % 2 else GELB)     # Stern auf der Spitze
    for k, y, gruppe in KERZEN:                                    # Kerzen flackern in drei Gruppen
        hell = (f // 4 + gruppe) % 3 == 0
        bild.rechteck(M + 2 * k, y, 2, 1, FLAMME_HELL if hell else GELB)
        bild.rechteck(M + 2 * k, y + 1, 2, 1, ROT)
    for k, y, farbe in KUGELN:
        bild.rechteck(M + 2 * k, y, 2, 1, farbe)
    for x, y, b, h, papier, band, by in GESCHENKE:
        bild.rechteck(x, y, b, h, papier)
        bild.rechteck(x, by, b, 1, band)
    x, y, b, h, papier, band, by = GA
    stufe = 0 if f < REISST_AB + 8 else min(3, 1 + (f - REISST_AB - 8) // 8)
    liegt = not (HEBT_AB <= f < UNTEN)
    if stufe and liegt:
        teddy(bild, *TEDDY_PLATZ)
    if stufe == 0:
        bild.rechteck(x, y, b, h, papier)
        bild.rechteck(x, by, b, 1, band)
        bild.rechteck(x + 2, y - 1, 2, 1, band)                    # Schleife
    elif stufe == 1:
        bild.rechteck(x, by, b, y + h - by, papier)
        bild.rechteck(x, by, b, 1, band)
    elif stufe == 2:
        bild.rechteck(x, 14, b, 1, papier)
    else:                                                          # Papierreste am Boden
        bild.setze(x - 1, 14, papier)
        bild.setze(x + b - 1, 14, papier)
    for start, vx, vy, farbe in FETZEN:                            # Papierfetzen fliegen im Bogen
        t = f - start
        if 0 <= t < 18:
            fy = 10 + vy * t + 0.06 * t * t
            if fy <= 14:
                bild.setze(38 + vx * t, fy, farbe)
    bild.rechteck(0, 15, B, 1, BODEN)
    return bild


def tuer(bild, f):
    """Rahmen, Blatt (Angel rechts, wird beim Öffnen schmal) und Glöckchen."""
    if f < TUER_AUF or f >= TUER_ZU + 18:
        w = TB
    elif f < TUER_ZU:
        w = max(2, TB - (f - TUER_AUF) // 2)
    else:
        w = min(TB, 2 + (f - TUER_ZU) // 3)
    bild.rechteck(TX - 1, TY - 1, TB + 2, 11, RAHMEN)
    bild.rechteck(TX, TY, TB - w, 10, LICHT)
    bild.rechteck(TX + TB - w, TY, w, 10, TUER)
    if w == TB:                                                    # zu: Licht im Schlüsselloch und unter der Tür
        bild.setze(*KNAUF, GOLD)
        bild.setze(*LOCH, GELB)
        bild.rechteck(TX, TY + 9, TB, 1, GELB)
    else:
        bild.setze(TX + TB - w, KNAUF[1], GOLD)
    s = SCHWUNG[(f - GLOCKE_AB) % 8] if GLOCKE_AB <= f < GLOCKE_BIS else 0
    bild.figur(GLOCKE_X, 0, GLOCKE[s], {"g": GLOCKE_GOLD, "w": WEISS})
    if s:                                                          # Klangstriche auf der Seite des Ausschlags
        x = GLOCKE_X - 3 if s < 0 else GLOCKE_X + 8
        bild.rechteck(x, 0, 2, 1, FLAMME_HELL)
        bild.rechteck(x + s, 2, 2, 1, FLAMME_HELL)


def huepfer(t, hoch=2):
    return [0, 1, hoch, hoch, hoch, 1, 0, 0][t % 8]


def kind1(f):
    """Liefert (x, hoch, Zeilen, gespiegelt)."""
    if f >= WARTET - 4 or f < GLOCKE_AB:
        u = (f - WARTET + 4) % 255
        if u < TRITT_AB + 4:                                       # eben angekommen: dreht sich zur Tür
            return X1_FLUR, 0, STEHT1, False
        k = (u // 5) % 2
        return X1_FLUR + k, 0, TRITT1[k], False
    if f < GLOCKE_AB + 6:                                          # horcht auf
        return X1_FLUR, 0, STEHT1, False
    if f < REIN1:
        t = f - GLOCKE_AB - 6
        return X1_FLUR, huepfer(t), JUBEL1 if huepfer(t) else STEHT1, False
    if f < DRIN1:
        t = f - REIN1
        x = X1_FLUR + (X1_ZIMMER - X1_FLUR) * t / (DRIN1 - REIN1)
        return round(x), huepfer(t), JUBEL1 if huepfer(t) else STEHT1, False
    if f < JUBEL_BIS or HOCH <= f < SENKT_AB:
        t = f - DRIN1
        return X1_ZIMMER, huepfer(t), JUBEL1 if huepfer(t) else STEHT1, False
    if REISST_AB <= f < HEBT_AB:                                   # schaut zu und zappelt
        k = (f // 5) % 2
        return X1_ZIMMER + k, 0, TRITT1[k], False
    if f < RAUS1:
        return X1_ZIMMER, 0, STEHT1, False
    t = f - RAUS1
    x = X1_ZIMMER + (X1_FLUR - X1_ZIMMER) * t / (WARTET - 4 - RAUS1)
    return round(x), huepfer(t, 1), STEHT1, True


def kind2(f):
    if f >= WARTET or f < GLOCKE_AB:
        u = (f - WARTET) % 255
        if SPAEHT_AB <= f < SPAEHT_BIS:                            # bückt sich zum Schlüsselloch, zappelt
            return X2_FLUR, 0, SPAEHT2[(f // 4) % 2], False
        if u < TRITT_AB:
            return X2_FLUR, 0, STEHT2, False
        k = ((u + 2) // 5) % 2
        return X2_FLUR + k, 0, TRITT2[k], False
    if f < GLOCKE_AB + 2:                                          # horcht auf
        return X2_FLUR, 0, STEHT2, False
    if f < REIN2:
        t = f - GLOCKE_AB - 2
        return X2_FLUR, huepfer(t), JUBEL2 if huepfer(t) else STEHT2, False
    if f < DRIN2:
        t = f - REIN2
        x = X2_FLUR + (X2_ZIMMER - X2_FLUR) * t / (DRIN2 - REIN2)
        return round(x), huepfer(t), JUBEL2 if huepfer(t) else STEHT2, False
    if f < JUBEL_BIS:
        t = f - DRIN2
        return X2_ZIMMER, huepfer(t), JUBEL2 if huepfer(t) else STEHT2, False
    if f < REISST_AB:
        return X2_ZIMMER + 1, 0, STEHT2, False
    if f < FREI:
        return X2_ZIMMER + 1, 0, REISST2[(f // 3) % 2], False
    if f < HEBT_AB:
        return X2_ZIMMER + 1, 0, REISST2[0], False
    if f < UNTEN:
        t = f - HOCH
        hoch = huepfer(t, 1) if HOCH <= f < SENKT_AB else 0
        return X2_ZIMMER + 1, hoch, JUBEL2, False
    if f < RAUS2:
        return X2_ZIMMER + 1, 0, STEHT2, False
    t = f - RAUS2
    x = X2_ZIMMER + 1 + (X2_FLUR - X2_ZIMMER - 1) * t / (WARTET - RAUS2)
    return round(x), huepfer(t, 1), STEHT2, True


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(FLUR)
        bild.rechteck(0, 15, B, 1, BODEN)
        # Wohnzimmer: das Licht breitet sich von der Tür nach rechts aus und zieht sich zurück
        if LICHT_AB <= f < DUNKEL_AB:
            grenze = ZX + (f - LICHT_AB) * 3
        elif DUNKEL_AB <= f:
            grenze = B - (f - DUNKEL_AB) * 2
        else:
            grenze = ZX
        if grenze > ZX:
            raum = zimmer(f)
            for x in range(ZX, min(B, grenze)):
                for y in range(15):
                    bild.px[y][x] = raum.px[y][x]
            if f < DUNKEL_AB and grenze < B:                       # heller Saum vorn am Licht
                bild.rechteck(grenze, 0, 2, 15, LICHT)
        tuer(bild, f)
        x, hoch, zeilen, gespiegelt = kind1(f)
        bild.figur(x, 15 - len(zeilen) - hoch, zeilen, K1, spiegeln=gespiegelt)
        x, hoch, zeilen, gespiegelt = kind2(f)
        y = 15 - len(zeilen) - hoch
        bild.figur(x, y, zeilen, K2, spiegeln=gespiegelt)
        if HEBT_AB <= f < UNTEN:                                   # Teddy hochheben, zeigen, absetzen
            a = min(1.0, (f - HEBT_AB) / (HOCH - HEBT_AB), (UNTEN - f) / (UNTEN - SENKT_AB))
            tx = TEDDY_PLATZ[0] + (x - TEDDY_PLATZ[0]) * a
            ty = TEDDY_PLATZ[1] + (y - 6 - TEDDY_PLATZ[1]) * a
            teddy(bild, tx, ty)
        liste.append(bild)
    return liste
