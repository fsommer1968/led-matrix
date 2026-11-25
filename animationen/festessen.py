"""Weihnachtliches Festessen: Der Tisch ist von vorn zu sehen – rote Decke, zwei rote Kerzen mit
sanft flackernden Flammen, vorn in der Mitte ein Tannenzweig mit goldener Kugel. Die Gans steht
goldbraun und dampfend auf der Silberplatte, links die Schüssel mit Knödeln, rechts der Rotkohl.
Eine Hand führt das Messer und sägt Scheibe um Scheibe ab (zuerst die Keule mit der Manschette),
die Gabel hebt sie fort; nebenher holt ein Löffel Knödel und Rotkohl. Der Braten wird kleiner,
bis nur das Gerippe und ein Rest bleiben. Dann räumen zwei Hände ab: erst die Schüsseln, dann die
Platte. Sie tragen eine neue Platte herein und stellen sie ab, die Schüsseln kommen dazu, Dampf
steigt – die Runde geht ohne Sprung in sich über. 255 Bilder.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum sind Decke, Platte und Schüsselränder einfarbige
Zeilen, Arme, Messer, Gabel und Löffel stehen senkrecht, die Wand bleibt dunkel, das Gerippe
wiederholt sich alle drei Spalten, und an den Kerzen flackert nur die Flammenspitze.
"""
from basis import B, GELB, GOLD, HAUT, ROT, WEISS, Bild

NAME = "festessen"
TITEL = "Weihnachtliches Festessen"

WAND = (0, 0, 0)
KANTE = (235, 0, 20)                           # Tischkante: helle Zeile der Decke
DECKE = (130, 0, 12)                           # Überhang der Tischdecke (große Fläche, gedämpft)
FLAMME_AUSSEN = (255, 100, 0)
ZWEIG = (0, 150, 45)
KUGEL = (255, 190, 0)
PLATTE = (150, 165, 215)                       # Silberplatte
GANS = (220, 115, 10)                          # goldbraun
GANS_HELL = (255, 200, 70)                     # Glanz auf der Kruste
GANS_DUNKEL = (150, 60, 5)                     # Unterseite und Keule
FLEISCH = (255, 185, 110)                      # Anschnitt: helles Fleisch
KNOCHEN = (240, 240, 215)
SCHUESSEL_L = (0, 80, 235)                     # blaue Schüssel (Knödel)
SCHUESSEL_R = (215, 225, 255)                  # weiße Schüssel (Rotkohl)
KNOEDEL = (255, 225, 130)
ROTKOHL = (150, 0, 200)
AERMEL = (150, 155, 180)                       # heller Ärmel, gedämpft
STAHL = (130, 180, 255)
DAMPF = (190, 190, 215)
DAMPF_DUNKEL = (95, 95, 115)

KERZEN = (1, 60)                               # linke Spalte der beiden Kerzen (3 breit)
SL, SR = 7, 46                                 # linke Kante der Schüsseln (11 breit)
PX, PB = 21, 22                                # Platte: linke Kante, Breite
GX = 25                                        # linke Kante der Gans (14 breit)

# Gans von der Seite, Zeilen 4 … 10: G goldbraun, h Glanz, k Keule, d Unterseite, w Manschette
GANSBILD = ["............ww",
            "....GGGGG...kk",
            "..GGhhhGGG.kk.",
            ".GGhGGGGGGkkk.",
            "GGGGGGGGGGkkGG",
            "GGGGGGGGGGGGGG",
            ".dddddddddddd."]
GANSFARBEN = {"G": GANS, "h": GANS_HELL, "k": GANS_DUNKEL, "d": GANS_DUNKEL, "w": WEISS}
# Gerippe unter dem Fleisch: Rückgrat in Zeile 10, Rippen alle drei Spalten
GERIPPE = ["...w..w..w..w.",
           "...w..w..w..w.",
           "...wwwwwwwwwww"]
# Scheiben von rechts: erste und letzte Spalte; übrig bleiben die Spalten 0 … 2
SCHEIBEN = [(12, 13), (9, 11), (7, 8), (5, 6), (3, 4)]

# Ablauf: Ruhe, schneiden (5 Scheiben), Rest, Schüsseln fort, Platte fort, leerer Tisch,
# neue Platte, neue Schüsseln, Ruhe bis zum Ende der Runde
SCHNEIDEN_AB, TAKT = 6, 24
SCHEIBE_HOCH = [0] * 15 + [-1, -2, -3, -4, -6, -8, -10, -12, -14]   # Versatz der Scheibe je Bild im Takt
REST_AB = SCHNEIDEN_AB + TAKT * len(SCHEIBEN)                    # 126
FORT_S, FORT_P, LEER_AB, NEU_P, NEU_S, RUHE_AB = 134, 152, 170, 176, 202, 228
HEBEN = [0, 0, -1, -2, -3, -4, -5, -7, -9, -11, -13, -15]       # greifen, dann hinauf (12 Bilder)
# Versatz beim Hereintragen: erst eine Zeile je Bild, zum Absetzen hin halb so schnell (20 Bilder)
SENKEN = [-11, -10, -9, -8, -7, -6, -5, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 0, 0]
# Flackern: Zustand der Flamme je Bild (0 ruhig, 1 hoch, 2 klein); 17 und 15 teilen 255
FLACKERN = ("00011000002200000", "002200000110000")
DAMPF_X = (GX + 6, GX + 3, GX + 9)                               # Dampfwölkchen über der Gans
MESSER_AB = [2, 4, 5, 7, 6, 8, 7, 9, 10]                         # Messerspitze je Bild: sägt sich hinunter
# Löffel während der 2. bis 5. Scheibe: Mitte, Zeile des Löffelblatts beim Aufnehmen, Farbe, Höhe des Happens
LOEFFEL = [(SL + 5, 7, KNOEDEL, 2), (SR + 5, 8, ROTKOHL, 1), (SL + 7, 9, KNOEDEL, 2), (SR + 7, 9, ROTKOHL, 1)]
LOEFFEL_HOCH = [0, 0, 1, 2, 3, 5, 7, 9, 11, 13]                  # ab dem Aufnehmen


def tisch(bild, f):
    """Decke, Kerzen und der Tannenzweig mit Kugel vorn am Überhang."""
    bild.rechteck(0, 12, B, 1, KANTE)
    bild.rechteck(0, 13, B, 3, DECKE)
    for k, x in enumerate(KERZEN):
        bild.rechteck(x - 1, 11, 5, 1, GOLD)                         # Leuchter
        bild.rechteck(x, 6, 3, 5, ROT)
        bild.rechteck(x, 4, 3, 2, FLAMME_AUSSEN)                     # Flamme: außen orange, innen gelb
        bild.rechteck(x + 1, 3, 1, 3, GELB)
        zustand = FLACKERN[k][f % len(FLACKERN[k])]
        if zustand == "1":                                           # Spitze züngelt hoch
            bild.setze(x + 1, 2, FLAMME_AUSSEN)
        elif zustand == "2":                                         # Flamme duckt sich
            bild.setze(x + 1, 3, FLAMME_AUSSEN)
    bild.rechteck(22, 13, 20, 1, ZWEIG)                              # Zweig
    bild.rechteck(24, 14, 5, 1, ZWEIG)
    bild.rechteck(35, 14, 5, 1, ZWEIG)
    bild.rechteck(30, 14, 4, 1, KUGEL)                               # Kugel
    bild.rechteck(31, 13, 2, 3, KUGEL)
    if f % 51 < 4:                                                   # Glanzlicht blitzt kurz auf
        bild.setze(31, 14, WEISS)


def platte(bild, dy, bis, gerippe_ab, anschnitt):
    """Platte mit Gans: Spalten 0 … bis-1 der Gans stehen noch, ab `gerippe_ab` liegt das Gerippe frei."""
    bild.rechteck(PX, 11 + dy, PB, 1, PLATTE)
    for k, zeile in enumerate(GERIPPE):
        for c, z in enumerate(zeile):
            if z != "." and c >= gerippe_ab:
                bild.setze(GX + c, 8 + k + dy, KNOCHEN)
    scheibe(bild, 0, bis - 1, 0, dy, anschnitt)


def scheibe(bild, c0, c1, dx, dy, anschnitt=False):
    """Die Spalten c0 … c1 der Gans, um dx und dy versetzt; `anschnitt`: die rechte Spalte ist eine
    Schnittfläche und zeigt helles Fleisch."""
    for k, zeile in enumerate(GANSBILD):
        for c in range(c0, c1 + 1):
            if zeile[c] != ".":
                farbe = FLEISCH if anschnitt and c == c1 and zeile[c] in "Ghk" else GANSFARBEN[zeile[c]]
                bild.setze(GX + c + dx, 4 + k + dy, farbe)


def schuesseln(bild, dy, knoedel=3, kohl=2):
    """Links Knödel in der blauen, rechts Rotkohl in der weißen Schüssel; `knoedel` (3 … 1) und
    `kohl` (2 … 0) sagen, wie viel noch da ist."""
    for x, farbe in ((SL, SCHUESSEL_L), (SR, SCHUESSEL_R)):
        bild.rechteck(x, 9 + dy, 11, 1, farbe)
        bild.rechteck(x + 1, 10 + dy, 9, 1, farbe)
        bild.rechteck(x + 2, 11 + dy, 7, 1, farbe)
    bild.rechteck(SL + 2, 7 + dy, 3, 2, KNOEDEL)                     # drei Knödel als Pyramide
    if knoedel >= 2:
        bild.rechteck(SL + 6, 7 + dy, 3, 2, KNOEDEL)
    if knoedel >= 3:
        bild.rechteck(SL + 4, 5 + dy, 3, 2, KNOEDEL)
    bild.rechteck(SR + 2, 8 + dy, 7 if kohl else 4, 1, ROTKOHL)      # Rotkohl als Haufen
    if kohl >= 2:
        bild.rechteck(SR + 3, 7 + dy, 5, 1, ROTKOHL)


def arm(bild, x, y):
    """Arm von oben: Hand (3 breit, 2 hoch) mit der Unterkante in Zeile y, darüber der Ärmel."""
    bild.rechteck(x, 0, 3, max(0, y - 1), AERMEL)
    bild.rechteck(x, y - 1, 3, 2, HAUT)


def messer(bild, x, spitze):
    """Senkrechtes Messer, Spitze in Zeile `spitze`; oben die Hand, die es führt, mit Ärmel."""
    bild.rechteck(x, spitze - 6, 1, 7, STAHL)
    bild.rechteck(x - 1, spitze - 9, 3, 3, HAUT)
    bild.rechteck(x - 1, 0, 3, max(0, spitze - 9), AERMEL)


def gabel(bild, x, y):
    """Senkrechte Gabel: zwei Zinken bis Zeile y, Stiel bis zum oberen Rand."""
    bild.rechteck(x, 0, 1, max(0, y - 2), STAHL)
    bild.rechteck(x - 1, y - 2, 3, 1, STAHL)
    bild.rechteck(x - 1, y - 1, 1, 2, STAHL)
    bild.rechteck(x + 1, y - 1, 1, 2, STAHL)


def loeffel(bild, x, y, farbe=None, hoch=0):
    """Senkrechter Löffel: Blatt (3 breit) in Zeile y, Stiel bis zum oberen Rand, darauf der Happen."""
    bild.rechteck(x, 0, 1, max(0, y - hoch), STAHL)
    bild.rechteck(x - 1, y - hoch, 3, hoch, farbe)
    bild.rechteck(x - 1, y, 3, 1, STAHL)


def dampf(bild, f, dy, anzahl):
    """Dampfwölkchen über der Gans: steigen in 15 Bildern von Zeile 3 hinaus und pendeln dabei."""
    for k, x in enumerate(DAMPF_X[:anzahl]):
        stufe = (f // 3 + k * 2) % 5                                 # 3 Bilder je Zeile
        y = 3 - stufe + dy
        farbe = DAMPF if stufe < 3 else DAMPF_DUNKEL
        bild.setze(x + stufe % 2, y, farbe)
        if stufe:
            bild.setze(x + (stufe + 1) % 2, y + 1, farbe)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(WAND)
        tisch(bild, f)
        platte_dy, s_dy, bis, gerippe_ab, dampf_n = 0, 0, 14, 14, 3  # Zustand in Ruhe: alles steht
        knoedel, kohl, anschnitt = 3, 2, False
        arme, vorn, hinten = [], [], []

        if SCHNEIDEN_AB <= f < REST_AB:
            # ── schneiden: Messer hinunter, Scheibe rückt ab, Gabel sticht ein und hebt sie fort ──
            nr, t = divmod(f - SCHNEIDEN_AB, TAKT)
            c0, c1 = SCHEIBEN[nr]
            dampf_n = max(0, 3 - nr)
            bis, gerippe_ab = c0, c1 + 1 if t < 9 else c0
            oben = min(k for k, zeile in enumerate(GANSBILD) if zeile[c0:c1 + 1].strip(".")) + 4
            dx = 1 if t >= 9 else 0                                  # durchgeschnitten: die Scheibe rückt ab
            anschnitt = t >= 9
            sy = SCHEIBE_HOCH[t]                                     # die Gabel hebt die Scheibe fort
            vorn.append((scheibe, c0, c1, dx, sy, nr >= 1))
            if t < 14:                                               # Messer sägt hinunter und hält
                vorn.append((messer, GX + c0, MESSER_AB[min(t, 8)]))
            elif t < 18:                                             # und zieht sich zurück
                vorn.append((messer, GX + c0, 10 - 3 * (t - 13)))
            if t >= 10:                                              # Gabel sticht in die abgerückte Scheibe
                vorn.append((gabel, GX + c1 + 1 - (c1 - c0) // 2, min(oben + 2, 2 * (t - 10)) + sy))
            # nebenher holt ein Löffel Knödel und Rotkohl (ab der zweiten Scheibe, abwechselnd)
            genommen = nr - 1 + (1 if t >= 10 else 0)                # so viele Happen sind schon fort
            knoedel, kohl = 3 - (genommen + 1) // 2, 2 - genommen // 2
            if nr >= 1:
                lx, ly, farbe, hoch = LOEFFEL[nr - 1]
                if t < 10:
                    hinten.append((lx, ly - (9 - t)))
                elif t < 10 + len(LOEFFEL_HOCH):
                    vorn.append((loeffel, lx, ly - LOEFFEL_HOCH[t - 10], farbe, hoch))
        elif REST_AB <= f < FORT_S:
            bis, gerippe_ab, dampf_n, knoedel, kohl, anschnitt = 3, 3, 0, 1, 0, True
        elif FORT_S <= f < FORT_P:
            # ── Schüsseln fort: Hände kommen, greifen, heben ──
            bis, gerippe_ab, dampf_n, knoedel, kohl, anschnitt = 3, 3, 0, 1, 0, True
            t = f - FORT_S
            if t < 6:
                hy = 2 * t - 1
            else:
                s_dy = HEBEN[t - 6]
                hy = 9 + s_dy
            arme = [(SL + 9, hy), (SR - 1, hy)]
        elif FORT_P <= f < LEER_AB:
            # ── Platte mit dem Gerippe fort ──
            bis, gerippe_ab, dampf_n, s_dy, anschnitt = 3, 3, 0, None, True
            t = f - FORT_P
            if t < 6:
                hy = 2 * t + 1
            else:
                platte_dy = HEBEN[t - 6]
                hy = 11 + platte_dy
            arme = [(PX - 2, hy), (PX + PB - 1, hy)]
        elif LEER_AB <= f < NEU_P:
            platte_dy = s_dy = None                                  # leerer Tisch
        elif NEU_P <= f < NEU_S:
            # ── neue Platte: herein, absetzen, Hände hinauf ──
            s_dy = None
            t = f - NEU_P
            platte_dy = SENKEN[min(t, len(SENKEN) - 1)]
            hy = 11 + platte_dy if t < len(SENKEN) else 11 - 2 * (t - len(SENKEN) + 1)
            arme = [(PX - 2, hy), (PX + PB - 1, hy)]
        elif NEU_S <= f < RUHE_AB:
            # ── neue Schüsseln ──
            t = f - NEU_S
            s_dy = SENKEN[min(t, len(SENKEN) - 1)]
            hy = 9 + s_dy if t < len(SENKEN) else 9 - 2 * (t - len(SENKEN) + 1)
            arme = [(SL + 9, hy), (SR - 1, hy)]

        if platte_dy is not None:
            if dampf_n:
                dampf(bild, f, platte_dy, dampf_n)
            platte(bild, platte_dy, bis, gerippe_ab, anschnitt)
        for x, y in hinten:                                          # leerer Löffel taucht hinter den Haufen
            loeffel(bild, x, y)
        if s_dy is not None:
            schuesseln(bild, s_dy, knoedel, kohl)
        for x, y in arme:
            arm(bild, x, y)
        for zeichne, *werte in vorn:                                 # Scheibe, Messer, Gabel, voller Löffel
            zeichne(bild, *werte)
        liste.append(bild)
    return liste
