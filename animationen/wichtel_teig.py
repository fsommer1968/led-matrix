"""Wichtel im Plätzchenteig: Weihnachtsbäckerei auf dem Küchentisch – große Teigschüssel mit
Kochlöffel, Nudelholz, zwei ausgestochene Plätzchen, im Fenster schneit es. Ein Wichtel (rote
Zipfelmütze, grünes Gewand) tippelt herbei, klettert am Schüsselrand hoch, balanciert, rutscht aus
und plumpst kopfüber in den Teig (Mehl staubt, die Beine strampeln noch). Kurz darauf taucht ein
goldgelber Lebkuchenmann mit Zuckerguss-Gesicht und der roten Zipfelmütze auf, springt heraus,
schaut verdutzt an sich herunter, zuckt mit den Schultern und hüpft davon. Am Ende ist der Tisch
wieder wie am Anfang – 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum schwarze Wand, Tisch und Schüssel aus waagerechten
Streifen (die Spalten der Schüsselmitte sind gleich), nur zwei Plätzchen, ein kleines Fenster mit
drei Flocken (kostet rund 11 KB), ein steiler Löffelstiel (rund 4 KB), Mehlstaub nur kurz.
"""
import math

from basis import B, GRUEN, HAUT, ROT, WEISS, Bild, dimmen

NAME = "wichtel_teig"
TITEL = "Wichtel im Plätzchenteig"

WAND = (0, 0, 0)
TISCH = (66, 30, 4)                            # Tischkante (Holz dunkel, sonst leuchtet es orange)
SCHUESSEL = (0, 40, 135)                       # große Flächen gedämpft
RAND = (95, 135, 225)
STREIFEN = (160, 175, 215)
FUSS = (0, 26, 90)
TEIG = (190, 145, 60)
TEIG_HELL = (228, 190, 110)
LEBKUCHEN = (255, 180, 0)                      # goldgelb statt braun (Braun wäre auf den LEDs kaum zu sehen)
ROLLE = (150, 121, 100)                        # Nudelholz: blasses Holz
ROLLE_DUNKEL = (100, 80, 66)
GRIFF = (150, 0, 20)
KEKS = (240, 195, 95)
HERZ = (255, 40, 110)
STIEFEL = (150, 0, 20)                         # rote Stiefel, helle Strümpfe (zu sehen, wenn er im Teig steckt)
STRUMPF = (220, 220, 235)
RAHMEN = (80, 36, 4)                           # Fensterrahmen
NACHT = (0, 0, 48)
FLOCKE = (150, 160, 200)
LOEFFEL = (170, 135, 110)                      # Kochlöffel: blasses Holz
AUGE = (50, 25, 10)
MEHL = (235, 235, 255)

SX, SB = 16, 22                                # Schüssel: linke Kante, Breite (Rand in Zeile 8)
TEIG_OBEN = 6                                  # oberste Zeile des Teigbergs in Ruhe
FUSS_Y = 14                                    # hier stehen die Füße auf dem Tisch (Tischkante Zeile 15)

# Wichtel (Blick nach rechts), 5 breit: w Bommel/Bart, r Mütze, h Gesicht, a Auge, g Gewand, b Stiefel
W_STEHT = ["w....", ".rr..", ".rrr.", ".hah.", ".gww.", ".ggg.", ".ggg.", ".b.b."]
W_GEHT = [".....", "wrr..", ".rrr.", ".hah.", ".gww.", ".ggg.", ".ggg.", "..b.."]     # Bommel wippt
W_GREIFT = ["w....", ".rr..", ".rrrg", ".hahg", ".gww.", ".ggg.", ".ggg.", ".b.b."]
W_ZIEHT = ["w....", ".rr..", ".rrr.", ".hahg", ".gwwg", ".ggg.", ".ggg.", "..b.."]
W_ARME = ["w....", ".rr..", ".rrr.", ".hah.", "ggwwg", ".ggg.", ".ggg.", ".b.b."]
W_LINKS = ["w....", ".rr..", ".rrr.", "ghah.", ".gww.", ".gggg", ".ggg.", ".b.b."]
W_RECHTS = ["w....", ".rr..", ".rrr.", ".hahg", ".gww.", "gggg.", ".ggg.", ".b.b."]
W_RUTSCHT = ["w....", ".rr.g", "grrr.", ".hah.", ".gww.", ".ggg.", ".gggb", ".b..."]
# steckt kopfüber im Teig: nur Gewandsaum und strampelnde Beine schauen heraus (4 Zeilen); s Strumpf
W_STECKT = ["b...b", ".s.s.", ".s.s.", ".ggg."]
W_ZAPPELT = [["b....", ".s.b.", ".s.s.", ".ggg."], ["....b", ".b.s.", ".s.s.", ".ggg."]]
W_SCHLAFF = [".....", ".b.b.", ".s.s.", ".ggg."]
W_FARBEN = {"w": WEISS, "r": ROT, "h": HAUT, "a": AUGE, "g": GRUEN, "b": STIEFEL, "s": STRUMPF}

# Lebkuchenmann (von vorn), 9 breit: o Bommel, r Mütze, l Lebkuchen, w Zuckerguss, k Knopf
L_KOPF = [".....o...", "...rrr...", "..rrrrr.."]
L_BEINE = ["...lkl...", "..ll.ll..", "..ww.ww.."]
L_STEHT = L_KOPF + ["..lwlwl..", "..llwll..", ".wlllllw."] + L_BEINE
L_BLINZELT = L_KOPF + ["..lllll..", "..llwll..", ".wlllllw."] + L_BEINE
L_STAUNT = L_KOPF + ["..lwlwl..", "..lwwwl..", ".wlllllw."] + L_BEINE       # Mund offen
# Kopf gesenkt (Mütze eine Zeile tiefer): schaut an sich herunter, besieht erst die eine, dann die andere Hand
L_UNTEN = ["........."] + L_KOPF + ["..lwlwl..", ".wlllllw."] + L_BEINE
L_HAND_L = ["........."] + L_KOPF + [".wlwlwl..", "..lllllw."] + L_BEINE
L_HAND_R = ["........."] + L_KOPF + ["..lwlwlw.", ".wlllll.."] + L_BEINE
L_ZUCKT = L_KOPF + ["w.lwlwl.w", ".lllwlll.", "..lllll.."] + L_BEINE         # Schultern hoch, Hände offen
L_HUEPFT = L_KOPF + ["..lwlwl..", ".wllwllw.", "..lllll..", "...lkl...", "..ll.ll..", ".ww...ww."]
L_FARBEN = {"o": WEISS, "r": ROT, "l": LEBKUCHEN, "w": WEISS, "k": GRUEN}

STERN = ["...x...", "...x...", "xxxxxxx", ".xxxxx.", "..xxx..", ".xx.xx.", ".x...x."]
HERZFORM = [".x.x.", "xxxxx", ".xxx.", "..x.."]

# Ablauf
T_KOMMT, T_DA, T_KLETTERT, T_OBEN, T_RUTSCHT, T_FLUG, T_KOPF = 4, 30, 40, 67, 102, 108, 112
T_PLUMPS, T_SINKT, T_BLUBB, T_TAUCHT, T_SPRUNG, T_LANDET = 113, 134, 144, 154, 176, 187
T_SCHAUT, T_ZUCKT, T_HUEPFT = 191, 217, 231          # ab 248 ist er aus dem Bild, der Tisch wie am Anfang
FALL_X = 24                                    # hier taucht der Wichtel ein
MANN_X = 22                                    # hier taucht der Lebkuchenmann auf
MANN_TISCH = 38                                # hier landet er auf dem Tisch
AUFTAUCHEN = [5, 5, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0]      # y0 je Bild ab T_TAUCHT
# Klettern: x0 und Fußzeile je Schritt; einmal rutscht er ein Stück ab
STEIGEN = [(11, 14), (12, 13), (12, 12), (13, 11), (13, 10), (12, 12), (13, 11), (13, 10), (13, 9), (14, 8),
           (14, 7), (15, 7)]


def drehen(zeilen):
    """Dreht ein Sprite um 90° im Uhrzeigersinn (Kopf nach rechts)."""
    hoch, breit = len(zeilen), len(zeilen[0])
    return ["".join(zeilen[hoch - 1 - c][r] for c in range(hoch)) for r in range(breit)]


W_LIEGT = drehen(W_STEHT)
W_KOPFUEBER = drehen(W_LIEGT)


def teig(bild, f):
    """Teigberg über dem Schüsselrand; wackelt nach dem Plumps und nach dem Sprung, blubbert vor
    dem Auftauchen."""
    x0, breit = SX + 4, SB - 8                                       # oberste Zeile
    wackelt = T_PLUMPS <= f < T_SINKT + 6 or T_SPRUNG <= f < T_SPRUNG + 10
    if wackelt and (f // 2) % 2:
        x0, breit = SX + 5, SB - 10
    bild.rechteck(SX + 2, TEIG_OBEN + 1, SB - 4, 1, TEIG)
    bild.rechteck(x0, TEIG_OBEN, breit, 1, TEIG_HELL)
    if T_BLUBB <= f < T_TAUCHT + 2:                                  # Blasen wölben sich und platzen
        k, u = divmod(f - T_BLUBB, 4)
        if k < 2 and u < 3:
            bild.rechteck(SX + (5, 12)[k], TEIG_OBEN - 1, 2, 1, TEIG_HELL)
        elif k >= 2:                                                 # … dann hebt sich die Mitte
            bild.rechteck(MANN_X + 3, TEIG_OBEN - 1, 4, 1, TEIG_HELL)


def fenster(bild, f):
    """Kleines Küchenfenster links oben: Nacht, drei Flocken fallen langsam (die Runde geht auf)."""
    bild.rechteck(1, 0, 9, 6, RAHMEN)
    bild.rechteck(2, 1, 3, 4, NACHT)
    bild.rechteck(6, 1, 3, 4, NACHT)
    for x, phase, runden in ((3, 0, 9), (6, 2.5, 12), (8, 4.5, 8)):
        y = (phase + f * runden * 6 / 255) % 6                       # 6 Zeilen Weg, davon 4 sichtbar
        if y < 4:
            bild.setze(x, 1 + int(y), FLOCKE)


def loeffel(bild, f):
    """Kochlöffel steckt rechts im Teig (steiler Stiel, je Spalte zwei Zeilen); zittert beim Plumps."""
    dx = 1 if T_PLUMPS <= f < T_PLUMPS + 8 and (f - T_PLUMPS) % 4 < 2 else 0
    for k in range(3):
        bild.rechteck(32 + k + (dx if k else 0), 4 - 2 * k, 1, 2, LOEFFEL)


def schuessel(bild):
    bild.rechteck(SX, 8, SB, 1, RAND)
    bild.rechteck(SX, 9, SB, 1, SCHUESSEL)
    bild.rechteck(SX, 10, SB, 1, STREIFEN)
    bild.rechteck(SX + 1, 11, SB - 2, 2, SCHUESSEL)
    bild.rechteck(SX + 2, 13, SB - 4, 1, SCHUESSEL)
    bild.rechteck(SX + 4, 14, SB - 8, 1, FUSS)


def tischzeug(bild):
    bild.rechteck(3, 12, 8, 2, ROLLE)                                # Nudelholz liegt links
    bild.rechteck(3, 14, 8, 1, ROLLE_DUNKEL)
    bild.rechteck(1, 13, 2, 1, GRIFF)
    bild.rechteck(11, 13, 2, 1, GRIFF)
    bild.figur(49, 8, STERN, {"x": KEKS})                            # Plätzchen rechts
    bild.figur(58, 11, HERZFORM, {"x": HERZ})


def mehl(bild, f):
    """Mehlstaub beim Plumps: erst eine Wolke um den Wichtel, dann fliegen Körnchen im Bogen
    auseinander und verblassen."""
    t = f - T_PLUMPS
    if not 0 <= t < 16:
        return
    if t < 3:                                                        # Wolke links und rechts
        for dx in (-1 - t, 5 + t):
            bild.rechteck(FALL_X + dx, TEIG_OBEN - 1 - (t > 0), 1, 1 + (t > 0), MEHL)
    for k, vx in enumerate((-1.3, -0.8, -0.35, 0.45, 0.9, 1.4)):
        vy = -1.1 - 0.25 * (k % 3)
        x = FALL_X + (0 if vx < 0 else 4) + vx * t
        y = TEIG_OBEN - 1 + vy * t + 0.09 * t * t
        if t > 1 and (y < TEIG_OBEN or abs(vx) * t > 7):
            bild.setze(x, y, dimmen(MEHL, 1.0 if t < 6 else (0.6 if t < 11 else 0.35)))


def staub(bild, x, t):
    """Mehlwölkchen neben den Füßen des Lebkuchenmanns, wenn er aufsetzt (t = Bilder seit dem Aufsetzen)."""
    if t == 0:
        bild.setze(x, FUSS_Y, MEHL)
        bild.setze(x + 8, FUSS_Y, MEHL)
    elif t == 1:
        bild.setze(x - 1, FUSS_Y - 1, dimmen(MEHL, 0.5))
        bild.setze(x + 9, FUSS_Y - 1, dimmen(MEHL, 0.5))


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(WAND)
        hinten, vorn, wolke = None, None, None                       # (x0, y0, Zeilen, Farben)
        if T_KOMMT <= f < T_DA:                                      # Wichtel tippelt herbei
            x = round(-5 + (f - T_KOMMT) * 16 / (T_DA - T_KOMMT))
            vorn = (x, FUSS_Y - 7, W_GEHT if (f // 3) % 2 else W_STEHT, W_FARBEN)
        elif T_DA <= f < T_KLETTERT:                                 # staunt die Schüssel an, hüpft neugierig
            u = f - T_DA
            hopst = 1 if u in (3, 4, 7, 8) else 0
            vorn = (11, FUSS_Y - 7 - hopst, W_GREIFT if u >= 2 else W_STEHT, W_FARBEN)
        elif T_KLETTERT <= f < T_OBEN:                               # klettert an der Schüssel hoch
            u = f - T_KLETTERT
            k = u * len(STEIGEN) // (T_OBEN - T_KLETTERT)
            x, fuss = STEIGEN[k]
            vorn = (x, fuss - 7, W_ZIEHT if k % 2 else W_GREIFT, W_FARBEN)
        elif T_OBEN <= f < T_RUTSCHT:                                # balanciert auf dem Rand
            u = f - T_OBEN
            x = 15 + min(6, u // 4)
            takt = 4 if u < 25 else 2                                # zum Schluss rudert er heftig
            pose = (W_ARME, W_LINKS, W_ARME, W_RECHTS)[(u // takt) % 4]
            vorn = (x, 0, pose, W_FARBEN)
        elif T_RUTSCHT <= f < T_FLUG:                                # rutscht aus
            vorn = (21, 0 if f < T_RUTSCHT + 3 else -1, W_RUTSCHT, W_FARBEN)
        elif T_FLUG <= f < T_KOPF:                                   # liegt quer in der Luft
            vorn = (20 + (f - T_FLUG), 1, W_LIEGT, W_FARBEN)
        elif T_KOPF <= f < T_SINKT + 6:                              # kopfüber in den Teig
            u = f - T_KOPF
            if u < 5:                                                # taucht ein (Zipfel zuerst)
                hinten = (FALL_X, -2 + u, W_KOPFUEBER, W_FARBEN)
            elif u < 8:                                              # steckt fest, Beine in die Luft
                hinten = (FALL_X, TEIG_OBEN - 4, W_STECKT, W_FARBEN)
            elif f < T_SINKT - 3:                                    # … und strampelt
                hinten = (FALL_X, TEIG_OBEN - 4, W_ZAPPELT[(f // 2) % 2], W_FARBEN)
            else:                                                    # gibt auf und versinkt langsam
                hinten = (FALL_X, TEIG_OBEN - 4 + max(0, (f - T_SINKT + 2) // 2), W_SCHLAFF, W_FARBEN)
        elif T_TAUCHT <= f < T_SPRUNG:                               # Lebkuchenmann taucht auf
            u = f - T_TAUCHT                                         # erst die Mütze, dann lugen die Augen heraus
            y = AUFTAUCHEN[min(u, len(AUFTAUCHEN) - 1)]
            zeilen = L_BLINZELT if u in (11, 12, 15, 16) else L_STEHT
            hinten = (MANN_X, y, zeilen, L_FARBEN)
        elif T_SPRUNG <= f < T_LANDET:                               # springt im Bogen auf den Tisch
            s = (f - T_SPRUNG) / (T_LANDET - T_SPRUNG)
            x = round(MANN_X + (MANN_TISCH - MANN_X) * s)
            y = round((FUSS_Y - 8) * s - 3 * math.sin(math.pi * s))
            vorn = (x, y, L_HUEPFT, L_FARBEN)
        elif T_LANDET <= f < T_HUEPFT:
            wolke = (MANN_TISCH, f - T_LANDET)
            if f < T_SCHAUT:
                zeilen = L_HUEPFT if f == T_LANDET else L_STEHT
            elif f < T_ZUCKT:                                        # schaut an sich herunter, besieht die Hände,
                u = f - T_SCHAUT                                     # … und staunt mit offenem Mund
                zeilen = (L_UNTEN if u < 5 else L_HAND_L if u < 10 else L_HAND_R if u < 15
                          else L_UNTEN if u < 18 else L_BLINZELT if u in (23, 24) else L_STAUNT)
            else:                                                    # zuckt zweimal mit den Schultern
                u = f - T_ZUCKT
                zeilen = L_ZUCKT if u < 5 or 8 <= u < 12 else L_STEHT
            vorn = (MANN_TISCH, FUSS_Y - 8, zeilen, L_FARBEN)
        elif f >= T_HUEPFT:                                          # hüpft davon
            u = f - T_HUEPFT
            x = round(MANN_TISCH + u * 1.5)
            hoch = round(3 * abs(math.sin(math.pi * u / 8)))
            if x < B:
                vorn = (x, FUSS_Y - 8 - hoch, L_HUEPFT if hoch else L_STEHT, L_FARBEN)
                if u and u % 8 < 2:
                    wolke = (x - u % 8, u % 8)                       # Mehl stäubt bei jedem Aufsetzen
        fenster(bild, f)
        loeffel(bild, f)
        if hinten:
            bild.figur(*hinten)
        bild.rechteck(0, FUSS_Y + 1, B, 1, TISCH)
        teig(bild, f)
        schuessel(bild)
        tischzeug(bild)
        if vorn:
            bild.figur(*vorn)
        if wolke:
            staub(bild, *wolke)
        mehl(bild, f)
        liste.append(bild)
    return liste
