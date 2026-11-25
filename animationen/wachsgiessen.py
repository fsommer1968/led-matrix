"""Wachsgießen: der Silvesterbrauch (heute mit Wachs statt Blei). Links brennt eine Kerze, darüber
hält eine Hand einen Löffel. Ein buntes Wachsstück fällt hinein, schmilzt über der Flamme und wird
flüssig und glänzend. Die Hand hebt den Löffel an, schwenkt ihn nach rechts über die Schale mit
Wasser und kippt: Das Wachs zischt ins Wasser (Dampfwölkchen, Spritzer, Ringwellen) und erstarrt.
Eine zweite Hand greift von oben hinein, fischt die Figur heraus und hält sie hoch, daneben
glitzert es – erst ein Herz, dann ein Kleeblatt, dann ein Stern, jedes in seiner Farbe.
Währenddessen ist der Löffel schon wieder leer über der Kerze und das nächste Wachsstück fällt
hinein. Drei Durchgänge zu je 85 Bildern; die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum einfarbiger Grund, waagerechter Arm und Löffelstiel und eine
senkrechte zweite Hand (gleiche Nachbarspalten), eine eckige Schale mit einfarbigem Wasser,
einfarbige Figuren und nur wenige Wellen, Spritzer und Glitzerpunkte. Alles, was sich bewegt,
hängt nur vom Bild im Durchgang ab oder hat einen Takt, der in 255 aufgeht (Flamme 51, Wellen 15).
"""
from basis import B, GELB, GOLD, HAUT, ORANGE, WEISS, Bild, dimmen, mischen

NAME = "wachsgiessen"
TITEL = "Wachsgießen an Silvester"

RUNDE = 255
GANG = 85                                      # ein Durchgang (Herz, Kleeblatt, Stern)

NACHT = (0, 0, 14)
TISCH = (110, 50, 10)
KERZE = (235, 215, 170)
TELLER = (170, 100, 0)                         # Kerzenteller
KERN = (255, 245, 170)                         # heller Kern der Flamme
METALL = (150, 150, 175)                       # Löffel
AERMEL_L = (90, 0, 155)                        # Arm mit dem Löffel (kommt von links)
AERMEL_R = (0, 150, 110)                       # Hand, die die Figur herausfischt (kommt von oben)
WASSER = (0, 40, 170)
SPIEGEL = (0, 150, 255)                        # Wasseroberfläche
WELLE = (170, 230, 255)                        # kleine Wellen, Ringwellen und Spritzer
GLAS = (150, 165, 190)                         # Rand der Schale
DAMPF = (210, 215, 235)
STIEL = (0, 110, 20)                           # Stiel des Kleeblatts

KERZE_X = 16                                   # linke Spalte der Kerze (drei breit)
WEG = 26                                       # so weit schwenkt der Löffel nach rechts
SCHALE_L, SCHALE_R = 38, 60                    # Wände der Schale
SPIEGEL_Y = 11
GUSS_X = 47                                    # hier trifft das Wachs ins Wasser

# Zeitplan eines Durchgangs (Bild im Durchgang); die Figur wird bis in den nächsten hinein gezeigt
T_LANDET = 4                                   # das Wachsstück liegt im Löffel
T_WEICH, T_HALB, T_FLUESSIG = 12, 17, 22       # schmelzen in drei Stufen
T_HIN, T_KIPPT, T_GIESST, T_ZURUECK, T_DA = 32, 46, 49, 59, 73
T_TRIFFT = T_GIESST + 2                        # der Strahl erreicht das Wasser
T_GREIFT, T_UNTEN, T_HEBT, T_OBEN, T_GEHT, T_FORT = 64, 70, 72, 80, 108, 114

HERZ = [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."]
KLEE = [".XX.XX.", "XXX.XXX", "XXXXXXX", "..XXX..", "XXXXXXX", "XXXSXXX", ".XXSXX.", "....S.."]
STERN = ["...X...", "..XXX..", "XXXXXXX", ".XXXXX.", "..XXX..", ".XX.XX.", "XX...XX"]
FORMEN = [(HERZ, (255, 0, 70)), (KLEE, (40, 255, 40)), (STERN, GELB)]

# Flamme: unter dem Löffel geduckt, sonst eine Zeile höher
FLAMMEN = [[".G.", "GGG", "GKG", ".O."],
           ["...", ".GG", "GKG", ".O."],
           ["G..", "GG.", "GKG", ".O."]]
FLAMMEN_FREI = [[".G.", ".G.", "GGG", "GKG", ".O."],
                ["...", ".GG", "GGG", "GKG", ".O."],
                ["G..", "GG.", "GGG", "GKG", ".O."]]
FLACKERN = [0, 1, 0, 2, 1, 0, 2, 0, 1, 2, 0, 1, 0, 2, 1, 2, 1]     # 17 Schritte zu je 3 Bildern


def _sanft(a):
    a = max(0.0, min(1.0, a))
    return a * a * (3 - 2 * a)


# ── Kerze und Schale ───────────────────────────────────────────────
def _kerze(bild, f, frei):
    bild.rechteck(KERZE_X - 1, 14, 5, 1, TELLER)
    bild.rechteck(KERZE_X, 11, 3, 3, KERZE)
    flamme = (FLAMMEN_FREI if frei else FLAMMEN)[FLACKERN[(f // 3) % 17]]
    bild.figur(KERZE_X, 11 - len(flamme), flamme, {"G": GELB, "K": KERN, "O": ORANGE})


def _schale(bild, f):
    bild.rechteck(SCHALE_L, 10, 1, 4, GLAS)
    bild.rechteck(SCHALE_R, 10, 1, 4, GLAS)
    bild.setze(SCHALE_L + 1, 14, GLAS)
    bild.setze(SCHALE_R - 1, 14, GLAS)
    bild.rechteck(SCHALE_L + 1, SPIEGEL_Y, SCHALE_R - SCHALE_L - 1, 1, SPIEGEL)
    bild.rechteck(SCHALE_L + 1, SPIEGEL_Y + 1, SCHALE_R - SCHALE_L - 1, 2, WASSER)
    bild.rechteck(SCHALE_L + 2, 14, SCHALE_R - SCHALE_L - 3, 1, WASSER)
    for x in range(SCHALE_L + 1, SCHALE_R):                         # kleine Wellen wandern nach rechts
        if (x - 2 * ((f // 5) % 3)) % 6 == 0:
            bild.setze(x, SPIEGEL_Y, WELLE)


def _ringe(bild, t):
    """Ringwellen laufen von der Gussstelle zu den Wänden: zweimal beim Guss, dann wenn die Hand
    eintaucht und wenn die Figur das Wasser verlässt."""
    for start, r0 in ((T_TRIFFT, 1), (T_TRIFFT + 5, 1), (T_UNTEN, 2), (T_HEBT + 2, 4)):
        if t >= start:
            for x in (GUSS_X - r0 - (t - start), GUSS_X + r0 + (t - start)):
                if SCHALE_L < x < SCHALE_R:
                    bild.setze(x, SPIEGEL_Y, WEISS)


# ── Löffel ─────────────────────────────────────────────────────────
def _lage(t):
    """Löffel im Durchgang: (Versatz nach rechts, Hub nach oben, Kippstufe 0–2). Vor dem Schwenk
    hebt die Hand den Löffel zwei Zeilen an, so bleibt der Ärmel über der Flamme."""
    hub = 2 if T_HIN <= t < T_DA - 1 else (1 if t in (T_HIN - 1, T_DA - 1) else 0)
    if t < T_HIN:
        return 0, hub, 0
    if t < T_KIPPT:
        return round(WEG * _sanft((t - T_HIN + 1) / (T_KIPPT - T_HIN))), hub, 0
    if t < T_KIPPT + 2:
        return WEG, hub, 1
    if t < T_ZURUECK - 2:
        return WEG, hub, 2
    if t < T_ZURUECK:
        return WEG, hub, 1
    if t < T_DA:
        return round(WEG * (1 - _sanft((t - T_ZURUECK + 1) / (T_DA - T_ZURUECK)))), hub, 0
    return 0, hub, 0


def _loeffel(bild, t, farbe):
    dx, hub, kipp = _lage(t)
    y = 5 - hub                                                     # Zeile des Stiels
    fest, hell = dimmen(farbe, 0.7), mischen(farbe, WEISS, 0.45)   # festes Stück matter, Glanz heller
    bild.rechteck(0, y - 1, 4 + dx, 3, AERMEL_L)                    # Arm von links, Faust
    bild.rechteck(4 + dx, y - 1, 3, 3, HAUT)
    if kipp < 2:
        bild.rechteck(7 + dx, y, 8, 1, METALL)                      # Stiel
        bild.rechteck(15 + dx, y + 1, 5, 1, METALL)                 # Schale des Löffels
        bild.setze(20 + dx, y + kipp, METALL)
    else:                                                           # gekippt: die Spitze hängt tiefer
        bild.rechteck(7 + dx, y, 7, 1, METALL)
        bild.rechteck(14 + dx, y + 1, 4, 1, METALL)
        bild.rechteck(18 + dx, y + 2, 3, 1, METALL)
    # Wachs im Löffel
    a = t - T_GIESST
    if t < 1:
        pass
    elif t < T_LANDET:                                              # das Stück fällt von oben hinein
        bild.rechteck(16, 2 * t - 3, 3, 2, fest)
    elif t < T_WEICH:
        bild.rechteck(16, 4, 3, 2, fest)
    elif t < T_HALB:                                                # unten läuft es schon breit
        bild.rechteck(16, 4, 3, 1, fest)
        bild.rechteck(15, 5, 5, 1, farbe)
    elif t < T_FLUESSIG:
        bild.setze(17, 4, farbe)
        bild.rechteck(15, 5, 5, 1, farbe)
    elif kipp < 2 and a < 0:                                        # flüssig, ein Glanzpunkt wandert
        bild.rechteck(15 + dx, y, 5, 1, farbe)
        bild.setze(15 + dx + (0, 1, 2, 3, 4, 3, 2, 1)[(t // 2) % 8], y, hell)
    elif a < 5:                                                     # läuft über die Spitze aus
        rest = 3 if a < 1 else (2 if a < 3 else 1)
        bild.rechteck(21 + dx - rest, y + 1, rest, 1, farbe)
    # Strahl ins Wasser
    oben, unten = y + 2 + 2 * max(0, a - 4), min(10, y + 3 + 2 * a)
    if a >= 0 and oben <= unten:
        bild.rechteck(GUSS_X, oben, 1, unten - oben + 1, hell)


# ── im Wasser ──────────────────────────────────────────────────────
WOLKEN = [["XX", "XX"], [".XX", "XXX"], ["X.X", ".X."]]              # Dampf: jung, weit, zerfließend


def _guss(bild, t, farbe):
    """Spritzer, Dampf und der Klumpen, der im Wasser erstarrt."""
    a = t - T_TRIFFT                                                # Bilder seit dem ersten Tropfen
    if a < 0:
        return
    for vx, vy, start in ((-1.1, 1.5, 0), (1.2, 1.8, 1), (-0.6, 2.0, 3), (0.7, 1.4, 4)):   # Spritzer
        b = a - start
        if 0 <= b < 7:
            y = 10 - vy * b + 0.3 * b * b
            if y <= 10:
                bild.setze(GUSS_X + vx * b, y, WELLE)
    for start, x0, drift in ((1, 49, 0.2), (4, 50, -0.1), (8, 49, 0.3)):                   # Dampf
        b = a - start
        if 0 <= b < 14:
            stufe = 0 if b < 4 else (1 if b < 9 else 2)
            bild.figur(round(x0 + drift * b), round(8 - b * 0.5), WOLKEN[stufe],
                       {"X": dimmen(DAMPF, (1, 0.6, 0.3)[stufe])})
    if t < T_HEBT:                                                  # Klumpen: erst glühend hell, dann fest
        c = mischen(farbe, WEISS, 0.45) if a < 8 else farbe
        bild.rechteck(GUSS_X - 1, 12, 3, 1, c)
        if a >= 2:
            bild.rechteck(GUSS_X - 1, 13, 3, 1, c)
        if a >= 6:
            bild.rechteck(GUSS_X - 2, 13, 5, 1, c)


def _fischen(bild, t, form, farbe):
    """Die zweite Hand greift von oben ins Wasser, hebt die Figur heraus und hält sie hoch."""
    if t < T_GREIFT or t >= T_FORT:
        return
    if t < T_UNTEN:
        yb = round(-1 + 12 * _sanft((t - T_GREIFT + 1) / (T_UNTEN - T_GREIFT)))
    elif t < T_HEBT:
        yb = 11
    elif t < T_OBEN:
        yb = round(11 - 10 * _sanft((t - T_HEBT + 1) / (T_OBEN - T_HEBT)))
    elif t < T_GEHT:
        yb = 1
    else:
        yb = round(1 - 10 * _sanft((t - T_GEHT + 1) / (T_FORT - T_GEHT)))
    if t >= T_HEBT:                                                 # Figur hängt an den Fingern
        for dy, zeile in enumerate(form):
            y = yb + 1 + dy
            if t < T_OBEN and y >= SPIEGEL_Y:                       # der Rest steckt noch im Wasser
                break
            for dx, c in enumerate(zeile):
                if c != ".":
                    bild.setze(GUSS_X - 3 + dx, y, STIEL if c == "S" else farbe)
        tropfen = t - T_HEBT - 5                                    # ein Tropfen fällt zurück
        if 0 <= tropfen < 6:
            y = yb + len(form) + 1 + tropfen
            if y < SPIEGEL_Y:
                bild.setze(GUSS_X, y, WELLE)
    bild.rechteck(GUSS_X - 1, 0, 3, yb - 2, AERMEL_R)
    bild.rechteck(GUSS_X - 1, yb - 2, 3, 3, HAUT)
    if T_OBEN + 2 <= t < T_GEHT - 2:                                # Glitzern links und rechts der Figur
        for k, (x, y) in enumerate(((41, 3), (53, 5), (41, 8), (53, 1))):
            s = (t + k * 3) % 12
            if s < 2 or 4 <= s < 6:                                 # Punkt, Kreuz, Punkt, Pause
                bild.setze(x, y, WEISS if s < 2 else GOLD)
            elif s < 4:
                for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    bild.setze(x + ddx, y + ddy, KERN)
                bild.setze(x, y, WEISS)


def bilder():
    liste = []
    for f in range(RUNDE):
        gang, t = divmod(f, GANG)
        form, farbe = FORMEN[gang]
        vor_form, vor_farbe = FORMEN[gang - 1]                      # Figur aus dem Durchgang davor
        dx, hub, _ = _lage(t)
        bild = Bild(NACHT)
        bild.rechteck(0, 15, B, 1, TISCH)
        _kerze(bild, f, frei=dx > 2 or hub > 0)
        _schale(bild, f)
        _ringe(bild, t)
        _guss(bild, t, farbe)
        _loeffel(bild, t, farbe)
        _fischen(bild, t, form, farbe)
        _fischen(bild, t + GANG, vor_form, vor_farbe)
        liste.append(bild)
    return liste
