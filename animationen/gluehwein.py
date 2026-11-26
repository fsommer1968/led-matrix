"""Glühweinstand: Abend auf dem Weihnachtsmarkt. Eine kleine Holzhütte mit verschneitem Dach und
bunter Lichterkette am Dachrand, auf dem Tresen ein großer Kessel, aus dem es dampft. Die
Verkäuferin schöpft mit der Kelle roten Glühwein und gießt ihn in die Tasse am Tresenende. Zwei
Besucher mit Mütze und Schal kommen von rechts: Der vordere nimmt die erste dampfende Tasse und
reicht sie nach hinten weiter, holt die zweite, dann stoßen beide zweimal an (kleines Funkeln),
trinken und gehen mit ihren Tassen nach links am Stand vorbei weiter. Die Verkäuferin stellt eine
frische Tasse hin und rührt im Kessel; zum Rundenende kommen die nächsten Besucher von rechts.
Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum eine Hütte aus gleichen Spalten (gerades Dach, glatte Wand, glatter
Tresen mit durchgehender Girlande), ein Kessel mit geraden Wänden, Figuren nur drei Spalten breit,
nur sieben Lämpchen (jedes kostet in jedem Bild rund sechs Bytes), ein einziger Stern rechts (links
der Hütte wäre er doppelt so teuer) und kein Schneefall. Kesseldampf (Takt 17), Lichterkette
(Takt 85) und Stern (Takt 51) laufen in Takten, die in 255 aufgehen; alles andere hängt nur an der
Zeit seit dem Auftritt der Besucher, und die Runde beginnt mitten in deren Anmarsch.
"""
from basis import (B, GELB, GOLD, HAUT, HELLBLAU, HELLGRUEN, NACHTBLAU, ORANGE, PINK, ROT, TUERKIS,
                   WEISS, Bild, dimmen)

NAME = "gluehwein"
TITEL = "Glühweinstand"

RUNDE = 255
VORLAUF = 22                                   # Bild 0 zeigt die Besucher schon auf dem Weg zum Stand

# Farben (Holz sehr dunkel, sonst leuchtet es auf den LEDs orange)
DACHSCHNEE = (190, 200, 235)
BODEN = (120, 130, 175)
BALKEN = (66, 34, 8)                           # Dachrand und Pfosten
WAND = (33, 11, 0)                             # Rückwand der Hütte
TRESEN = (90, 46, 10)                          # Tresenplatte
FRONT = (49, 19, 0)                            # Tresenfront
GIRLANDE = (0, 100, 30)
KETTE = [ROT, GELB, HELLGRUEN, HELLBLAU, PINK]
KESSEL = (85, 90, 115)
KESSEL_RAND = (170, 175, 205)
KESSEL_WULST = (120, 126, 160)
WEIN = (235, 0, 40)
METALL = (150, 150, 175)
LEER = (70, 70, 85)                            # leere Kelle von innen
TASSE = (235, 235, 245)
DAMPF = [(215, 220, 250), (125, 130, 160), (70, 73, 95)]            # hell, mittel, dunkel
HAAR = (255, 200, 40)
PULLI = (0, 150, 60)
AUGE = (50, 25, 10)
HOSE = (70, 80, 125)
STERN = (255, 240, 200)
FUNKE = (255, 245, 170)
STERN_X, STERN_Y = 58, 1                       # ein einziger Stern (jeder kostet in jedem Bild Bytes)

# Hütte: Dach von HX bis HX+32, Pfosten bei HX+1 und HX+31, Tresenplatte in Zeile 11
HX = 9
KESSEL_X = HX + 3                              # Kessel zehn Spalten breit, Rand in Zeile 7
# Dampf: Spalte im Kessel und wohin die Fahne pendelt; zwei beginnen unter einem Lämpchen (die Spalte
# ist ohnehin eine eigene, dort kostet der Dampf am wenigsten)
FAHNEN = [(3, 1), (6, -1), (8, -1)]
FRAU_KESSEL, FRAU_TASSE = HX + 15, HX + 23     # linke Spalte der Verkäuferin am Kessel / beim Eingießen
TASSE_X, TASSE_Y = HX + 29, 9                  # Tasse auf dem Tresen (zwei Spalten, zwei Zeilen)
A_X, B_X = HX + 33, HX + 42                    # hier stehen die beiden Besucher
STOSS_X = A_X + 5                              # zwischen dieser und der nächsten Spalte treffen sich die Tassen

# Besucher: Mütze, Schal, Mantel
A_FARBEN = {"p": WEISS, "m": ROT, "s": GELB, "j": (0, 110, 255)}
B_FARBEN = {"p": WEISS, "m": ORANGE, "s": TUERKIS, "j": (170, 0, 255)}

# Besucher (Blick nach links): p Bommel, m Mütze, a Auge, h Haut, s Schal (das Ende hängt über den
# Rücken), j Mantel, b Hose
BESUCHER = [".pp", "mmm", "mmm", "ahh", "hhh", "sss", "jjs", "jjs", "jjj"]
BEINE = [["bbb", "bbb"], ["bbb", "b.."], ["bbb", ".bb"]]            # steht, Schritt vorn, Schritt hinten
# Verkäuferin (Blick nach rechts): H Haar, h Haut, a Auge, g Pulli
FRAU = ["HHH", "Hha", "Hhh", "Hgg", "ggg", "ggg", "ggg"]
FRAU_FARBEN = {"H": HAAR, "h": HAUT, "a": AUGE, "g": PULLI}

# Zeitplan in Bildern seit dem Auftritt der Besucher (u)
U_DA = 33                                      # beide stehen am Stand
# Gänge der Verkäuferin: Beginn, Bilder am Tresenende, mit Wein. Jeder Gang: Kelle heben (4 Bilder),
# zum Tresenende gehen (8), dort stehen, zurückgehen (8), Kelle eintauchen (6); sonst rührt sie.
GAENGE = [(10, 19, True), (55, 16, True), (212, 6, False)]         # erste Tasse, zweite Tasse, frische Tasse
U_GIESST1, U_GIESST2, U_FRISCH = (beginn + 12 for beginn, _, _ in GAENGE)
U_NIMMT1, U_REICHT, U_NIMMT2 = 34, 39, 76                           # Besucher A
U_STOSS1, U_STOSS2 = 90, 99                                         # die Tassen berühren sich
U_TRINKT1, U_TRINKT2 = 107, 130
U_WEITER = 152                                                      # beide gehen nach links weiter


# ── Hütte und Kessel ───────────────────────────────────────────────
def _huette(bild, f):
    bild.rechteck(HX + 4, 0, 25, 1, DACHSCHNEE)                    # Schneehaube, oben schmaler
    bild.rechteck(HX, 1, 33, 1, DACHSCHNEE)
    bild.rechteck(HX, 2, 33, 1, BALKEN)
    for k in range(7):                                              # Lichterkette: die Farben wandern
        bild.setze(HX + 1 + 5 * k, 2, KETTE[(k - f // 17) % len(KETTE)])
    bild.rechteck(HX + 2, 3, 29, 8, WAND)
    bild.rechteck(HX + 1, 3, 1, 12, BALKEN)
    bild.rechteck(HX + 31, 3, 1, 12, BALKEN)
    bild.rechteck(HX + 2, 11, 29, 1, TRESEN)
    bild.rechteck(HX + 2, 12, 29, 1, GIRLANDE)                     # Tannengirlande unter der Tresenplatte
    bild.rechteck(HX + 2, 13, 29, 2, FRONT)


def _kessel(bild, f):
    x = KESSEL_X
    bild.rechteck(x, 8, 10, 1, KESSEL_WULST)                        # heller Wulst unter dem Rand
    bild.rechteck(x, 9, 10, 1, KESSEL)
    bild.rechteck(x + 1, 10, 8, 1, KESSEL)                          # unten gerundet
    bild.rechteck(x + 1, 7, 8, 1, WEIN)
    bild.setze(x, 7, KESSEL_RAND)
    bild.setze(x + 9, 7, KESSEL_RAND)
    for k, (spalte, seite) in enumerate(FAHNEN):                    # drei Dampffahnen, Takt 17
        stufe = (f + k * 6) % 17 // 3
        if stufe < 4:
            sx, sy = x + spalte + seite * (stufe % 2), 6 - stufe
            bild.setze(sx, sy, DAMPF[stufe // 2])
            if 0 < stufe < 3:
                bild.setze(sx, sy + 1, DAMPF[stufe // 2 + 1])


# ── Verkäuferin mit Kelle ──────────────────────────────────────────
def _frau_lage(u):
    """(linke Spalte, Blick, Kelle: Zeilen tiefer als ganz oben (0–2), voll,
    steht seit n Bildern am Tresenende oder None)."""
    for beginn, steht, wein in GAENGE:
        t = u - beginn
        if 0 <= t < 4:                                              # hebt die Kelle aus dem Kessel
            return FRAU_KESSEL, -1, max(0, 2 - (t + 1) // 2), wein, None
        if 4 <= t < 12:                                             # trägt sie zum Tresenende
            return FRAU_KESSEL + t - 3, 1, 0, wein, None
        if 12 <= t < 12 + steht:                                    # gießt ein und wartet
            return FRAU_TASSE, 1, 0, wein and t < 17, t - 12
        t -= 12 + steht
        if 0 <= t < 8:                                              # geht zum Kessel zurück
            return FRAU_TASSE - t - 1, -1, 0, False, None
        if 8 <= t < 14:                                             # taucht die Kelle wieder ein
            return FRAU_KESSEL, -1, min(2, (t - 7) // 2), False, None
    return FRAU_KESSEL, -1, 2, False, None                          # rührt im Kessel


def _wein_gang(u):
    """Wahr, solange die Verkäuferin Wein zur Tasse bringt (nicht beim Gang mit der frischen Tasse)."""
    return any(wein and beginn <= u < beginn + 12 + steht for beginn, steht, wein in GAENGE)


def _frau(bild, u):
    x0, blick, tief, voll, giesst = _frau_lage(u)
    bild.figur(x0, 4, FRAU, FRAU_FARBEN, spiegeln=blick < 0)
    e = x0 + 3 if blick > 0 else x0 - 1                             # erste Spalte vor dem Körper
    y = 5 + tief
    ruehrt = tief == 2 and not voll and (u // 5) % 2
    bild.setze(e, y + 1, PULLI)                                     # Arm
    bild.setze(e + blick, y - ruehrt, METALL)                       # Stiel
    bild.setze(e + 2 * blick, y - ruehrt, METALL)
    for k in (3, 4):                                                # Schöpfer: oben der Wein, unten Metall
        bild.setze(e + k * blick, y, WEIN if voll else LEER)
        bild.setze(e + k * blick, y + 1, METALL)
    if _wein_gang(u) and giesst is not None and 1 <= giesst < 7:    # Strahl in die Tasse
        bild.rechteck(TASSE_X + 1, 7, 1, 1 if giesst == 1 else 2, WEIN)


def _tasse(bild, x, y, voll):
    bild.rechteck(x, y, 2, 2, TASSE)
    if voll:
        bild.rechteck(x, y, 2, 1, WEIN)


def _tassendampf(bild, u, x, y, phase=0):
    """Eine Dampffahne über der Tasse (linke Spalte x, obere Zeile y)."""
    stufe = (u + phase) % 15 // 3
    if stufe < 3:
        bild.setze(x + (stufe + phase) % 2, y - 1 - stufe, DAMPF[stufe])


def _tresen_tasse(bild, u):
    """Die Tasse auf dem Tresen: leer, gefüllt, genommen; die Verkäuferin stellt eine frische hin."""
    if U_NIMMT1 + 2 <= u < U_NIMMT1 + 5 or U_NIMMT2 + 2 <= u < U_FRISCH:
        return                                                      # gerade genommen
    if u in (U_NIMMT1 + 5, U_NIMMT1 + 6, U_FRISCH, U_FRISCH + 1):   # die frische taucht hinter dem Tresen auf
        bild.rechteck(TASSE_X, TASSE_Y + 1, 2, 1, TASSE)
        return
    for giesst, nimmt in ((U_GIESST1, U_NIMMT1), (U_GIESST2, U_NIMMT2)):
        if giesst + 3 <= u < nimmt + 2:
            _tasse(bild, TASSE_X, TASSE_Y, True)
            if u >= giesst + 7:
                _tassendampf(bild, u, TASSE_X, TASSE_Y)
            return
    _tasse(bild, TASSE_X, TASSE_Y, False)


# ── Besucher ───────────────────────────────────────────────────────
def _besucher(bild, u, x, blick, farben, pose, geht=False, phase=0):
    """pose: None (keine Tasse), 'greift', 'streckt', 'haelt', 'hebt', 'trinkt'."""
    farben = {**farben, "h": HAUT, "a": AUGE, "b": HOSE}
    spiegeln = blick > 0
    kopf = -blick if pose == "trinkt" else 0                        # legt den Kopf zurück
    bild.figur(x + kopf, 4, BESUCHER[:3], farben, spiegeln)
    bild.figur(x, 7, BESUCHER[3:], farben, spiegeln)
    bild.figur(x, 13, BEINE[1 + (u // 3) % 2 if geht else 0], farben, spiegeln)
    v = x - 1 if blick < 0 else x + 3                               # erste Spalte vor dem Körper
    if pose == "greift":
        bild.setze(v, 10, farben["j"])
        bild.setze(v + blick, 10, farben["j"])
        return
    if pose is None:
        return
    tx, ty = v, 9
    if pose == "streckt":
        bild.setze(v, 10, farben["j"])
        tx = v + blick
    elif pose == "hebt":
        ty = 8
    elif pose == "trinkt":
        ty = 7
    links = min(tx, tx + blick)
    _tasse(bild, links, ty, True)
    if pose != "trinkt":
        _tassendampf(bild, u, links, ty, phase)


def _weg(u, platz, abstand):
    """Spalte eines Besuchers und ob er geht: von rechts herein (zwei Spalten in drei Bildern, im Takt
    der Schritte), stehen, nach links hinaus (eine Spalte je Bild); None = fort."""
    if u < U_DA:
        x = max(platz, B + abstand - u * 2 // 3)
        return x, x > platz
    if u < U_WEITER + 2:
        return platz, False
    x = platz - (u - U_WEITER - 2)
    return (x, True) if x > -4 else (None, False)


def _anstoss(u):
    for stoss in (U_STOSS1, U_STOSS2):
        if stoss - 2 <= u < stoss + 3:
            return "streckt"
    return None


def _trinkpose(u, start):
    """Tasse heben, trinken, senken."""
    t = u - start
    if 0 <= t < 2 or 14 <= t < 16:
        return "hebt"
    if 2 <= t < 14:
        return "trinkt"
    return None


def _a(bild, u):
    """Der vordere Besucher: holt beide Tassen am Tresen, die erste reicht er weiter."""
    x, geht = _weg(u, A_X, 0)
    if x is None:
        return
    blick, pose = -1, None
    if u >= U_WEITER:
        pose = "haelt"
    elif u >= U_DA:
        for nimmt in (U_NIMMT1, U_NIMMT2):
            if nimmt <= u < nimmt + 2:
                pose = "greift"
            elif nimmt + 2 <= u < nimmt + 4:
                pose = "streckt"
            elif nimmt + 4 <= u:
                pose = "haelt"
        if U_REICHT <= u < U_NIMMT2:                                # dreht sich um und reicht die Tasse weiter
            blick, pose = 1, "haelt"
            if u >= U_REICHT + 2:
                pose = "streckt"
            if u >= U_REICHT + 5:
                pose = None
            if u >= U_REICHT + 8:
                blick = -1
        if u >= U_NIMMT2 + 6:                                       # dreht sich zum Anstoßen um
            blick = 1
            pose = _anstoss(u) or _trinkpose(u, U_TRINKT1) or _trinkpose(u, U_TRINKT2) or "haelt"
    _besucher(bild, u, x, blick, A_FARBEN, pose, geht)


def _b(bild, u):
    """Der hintere Besucher: bekommt die erste Tasse gereicht."""
    x, geht = _weg(u, B_X, 9)
    if x is None:
        return
    pose = None
    if U_REICHT + 3 <= u < U_REICHT + 5:
        pose = "greift"
    elif U_REICHT + 5 <= u < U_REICHT + 7:
        pose = "streckt"
    elif u >= U_REICHT + 7:
        pose = _anstoss(u) or _trinkpose(u, U_TRINKT1 + 2) or _trinkpose(u, U_TRINKT2 + 2) or "haelt"
    _besucher(bild, u, x, -1, B_FARBEN, pose, geht, phase=7)


def _funkeln(bild, u):
    """Kleines Funkeln über den Tassen, wenn sie sich berühren."""
    x = STOSS_X
    for stoss in (U_STOSS1, U_STOSS2):
        t = u - stoss
        if t in (0, 1):
            bild.rechteck(x, 8, 2, 1, WEISS)
        if t == 1:
            bild.rechteck(x, 7, 2, 1, FUNKE)
            bild.setze(x - 1, 8, GELB)
            bild.setze(x + 2, 8, GELB)
        elif t == 2:
            bild.rechteck(x, 6, 2, 1, GELB)
            bild.setze(x - 2, 7, GOLD)
            bild.setze(x + 3, 7, GOLD)
        elif t == 3:
            bild.setze(x - 2, 5, GOLD)
            bild.setze(x + 3, 5, GOLD)


def bilder():
    liste = []
    for f in range(RUNDE):
        u = (f + VORLAUF) % RUNDE
        bild = Bild(NACHTBLAU)
        bild.setze(STERN_X, STERN_Y, dimmen(STERN, 1.0 if f % 51 < 34 else 0.5))   # funkelt langsam
        bild.rechteck(0, 15, B, 1, BODEN)
        _huette(bild, f)
        _frau(bild, u)
        _kessel(bild, f)
        _tresen_tasse(bild, u)
        _a(bild, u)
        _b(bild, u)
        _funkeln(bild, u)
        liste.append(bild)
    return liste
