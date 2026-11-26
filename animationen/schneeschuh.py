"""Schneeschuhwanderung: Ein verschneiter Berghang steigt von links nach rechts an, oben steht ein
kleines Gipfelkreuz. Später Nachmittag – der Himmel ist oben noch blau und zum Horizont hin rötlich,
die Sonne sinkt rot in den Sattel hinter dem Nachbargipfel, dessen Grat auf der Sonnenseite glüht.
Ein Wanderer mit dicker roter Jacke, gelber Mütze, Stöcken und breiten Schneeschuhen stapft durch
den tiefen Schnee hinauf, sinkt bei jedem Schritt ein Stück ein (Schnee stäubt) und lässt eine Spur
aus Abdrücken zurück. Oben reckt er die Arme mit den Stöcken, dreht sich um und schaut einem Vogel
nach, der über dem Tal kreist; dann steigt er am Kreuz vorbei auf der anderen Seite ab. Zum Schluss
fegt der Wind über den Hang und verweht die Spur – der Hang ist wieder glatt, Anfang und Ende
zeigen dasselbe Bild. 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Himmel in waagerechten Streifen (gleiche Spalten), der
Hang in gleich breiten Stufen, der Nachbargipfel im selben Takt gestuft, das Kreuz so breit wie die
Kuppe, die Abdrücke je drei Spalten im Takt der Stufen (rechts abwechselnd eine Stufe mit, eine
ohne), die Sonne ein Block aus drei Zeilen; kein Schneefall – nur ein paar Körner Schneestaub am
Schuh und kurze Schneefahnen im Wind.
"""
import math

from basis import B, GELB, HAUT, ROT, SCHWARZ, Bild

NAME = "schneeschuh"
TITEL = "Schneeschuhwanderung zum Gipfel"

# Himmel am späten Nachmittag: je Zeile eine Farbe, in deutlichen Stufen (große Fläche, gedämpft)
HIMMEL = [(28, 62, 135)] * 3 + [(75, 65, 130)] * 2 + [(125, 70, 100)] * 2 + [(150, 88, 38)] * 9
SONNENROT = (255, 64, 0)
FERN = (40, 34, 82)                            # Nachbargipfel im Gegenlicht
FERN_SCHNEE = (112, 108, 160)                  # sein Grat im Schatten
FERN_GLUT = (230, 125, 105)                    # … und auf der Sonnenseite (Alpenglühen)
KANTE = (215, 225, 250)                        # Oberkante des Hangs
HANG = (78, 90, 140)                           # darunter gedämpft (große Fläche)
ABDRUCK = (98, 110, 165)                       # Schneeschuh-Abdruck in der Kante
VERWEHT = (165, 176, 215)                      # Abdruck, halb zugeweht
STAUB = (235, 240, 255)
KREUZ = (60, 26, 2)                            # Holz, dunkel gehalten (sonst leuchtet es orange)
HOSE = (0, 70, 255)
SCHUH = (255, 115, 0)
STOCK = (225, 225, 240)
AUGE = (50, 25, 10)
FARBEN = {"m": GELB, "h": HAUT, "a": AUGE, "j": ROT, "b": HOSE, "s": SCHUH, "p": STOCK}

# Hang: (erste Spalte, Zeile der Oberkante) – links flach, sechs Stufen hinauf, Kuppe, rechts steil ab
STUFEN = [(0, 14), (6, 13), (12, 12), (18, 11), (24, 10), (30, 9), (36, 8), (44, 7),
          (47, 8), (50, 9), (53, 10), (56, 11), (59, 12), (62, 13)]
FERN_SPITZE = 12                               # ab hier fällt der Nachbargipfel zur Sonne hin ab
KREUZ_X = 45                                   # das Kreuz ist so breit wie die Kuppe (gleiche Spaltenwechsel)
SONNE = [(7, 20, 23), (8, 19, 24), (9, 19, 24)]                      # Zeile, von Spalte, bis Spalte

# Wanderer (Blick nach rechts), 7 breit: m Mütze, h Gesicht, a Auge, j Jacke, b Hose, s Schneeschuh, p Stock
SCHRITT_A = ["..mmm..",                        # Ausfallschritt, vorderer Stock eingesetzt
             "..hha..",
             ".jjjj.p",
             "pjjjjjp",
             "p.bbb.p",
             "..b.b.p",
             ".ss.sss"]
SCHRITT_B = ["..mmm..",                        # Füße beisammen (eingesunken), hinterer Stock stößt ab
             "..hha..",
             ".jjjj..",
             "pjjjjjp",
             "p.bbb.p",
             "p..bb..",
             "..ssss."]
STEHT = ["..mmm..",
         "..hha..",
         ".jjjj..",
         "pjjjjjp",
         "p.bbb.p",
         "p.b.b.p",
         ".ss.ss."]
JUBEL_A = ["p.....p",                          # Arme und Stöcke hoch (acht Zeilen)
           "p.mmm.p",
           "j.hha.j",
           ".jjjjj.",
           "..jjj..",
           "..bbb..",
           "..b.b..",
           ".ss.ss."]
JUBEL_B = [".......",
           "p.mmm.p",
           "p.hha.p",
           "jjjjjjj",
           "..jjj..",
           "..bbb..",
           "..b.b..",
           ".ss.ss."]
BLICK = ["..mmm..",                            # Hand über den Augen, schaut in die Ferne
         "..hhaj.",
         ".jjjjj.",
         "pjjjj..",
         "p.bbb..",
         "p.b.b..",
         ".ss.ss."]

# Vogel (schwarz vor dem hellen Himmel): Flügel oben, gleitet, Flügel unten, in der Kehre von vorn
VOGEL_AUF = ["x...x", ".x.x.", "..x.."]
VOGEL_GLEITET = [".....", "xx.xx", "..x.."]
VOGEL_AB = [".....", ".xxx.", "x...x"]
VOGEL_SCHMAL = [".....", ".x.x.", "..x.."]
SCHLAG = [VOGEL_AUF, VOGEL_GLEITET, VOGEL_AB, VOGEL_GLEITET]         # Flügelschlag

KOMMT, OBEN, AB, WEG = 2, 114, 164, 212        # Wanderer: kommt, ist oben, steigt ab, ist fort
X_START, X_OBEN, X_ENDE = -6, 36, 65           # linke Spalte der Figur
SCHRITT, SCHRITT_AB = 8, 6                     # Bilder je Schritt hinauf (drei Spalten weit) und hinunter
WIND, WIND_ENDE = 215, 249                     # der Wind verweht die Spur von links nach rechts
WIND_TEMPO = 2.3                               # Spalten je Bild
WEHEN = [(2, 1), (-3, 2), (-8, 1), (-13, 2)]   # Schneefahnen: Spalte zur Windfront, Zeilen über dem Hang
VOGEL_DA, VOGEL_KREIST, VOGEL_FORT, VOGEL_WEG = 108, 120, 192, 208
VOGEL_MITTE, VOGEL_RADIUS, VOGEL_UMLAUF = (28, 3), (5, 2), 36        # zwei Umläufe über dem Tal


def hang_y(x):
    """Zeile der Oberkante des Hangs in Spalte x."""
    y = STUFEN[0][1]
    for x0, zeile in STUFEN:
        if x >= x0:
            y = zeile
    return y


def abdruck(x):
    """Liegt in Spalte x ein Abdruck? Drei Spalten Abdruck, drei Spalten glatt – im Takt der Stufen,
    damit sich die Spalten wiederholen; unter dem Kreuz keiner."""
    if x < KREUZ_X - 1:
        return x % 6 >= 3
    return x > KREUZ_X + 1 and (x - KREUZ_X - 2) % 6 < 3


def fern_y(x):
    """Oberkante des Nachbargipfels (Spitze bei 9 bis 11), Stufen im Takt des Hangs; 99 = keiner."""
    if x < 9:
        return 8 if x < 6 else 7
    if x < 24:
        return 6 + (x - 9) // 3
    return 99


def wanderer(f):
    """Linke Spalte, Figur, gespiegelt?, tief – oder None, wenn er nicht im Bild ist.
    tief: 0 = steht oben auf dem Schnee, sonst das wievielte Bild er schon eingesunken ist."""
    if KOMMT <= f < OBEN:                                            # stapft hinauf
        t = f - KOMMT
        tief = max(0, t % SCHRITT - SCHRITT // 2 + 1)
        return X_START + t * 3 // SCHRITT, SCHRITT_B if tief else SCHRITT_A, False, tief
    if OBEN <= f < AB:                                               # auf dem Gipfel
        u = f - OBEN
        if u < 4 or u >= 47:
            return X_OBEN, STEHT, False, 0
        if u < 22:                                                   # reckt die Arme
            return X_OBEN, JUBEL_B if (u - 4) // 6 == 1 else JUBEL_A, False, 0
        if u < 25:
            return X_OBEN, STEHT, False, 0
        if u < 28 or u >= 45:                                        # dreht sich zum Tal
            return X_OBEN, STEHT, True, 0
        return X_OBEN, BLICK, True, 0
    if AB <= f < WEG:                                                # steigt rechts ab
        t = f - AB
        tief = max(0, t % SCHRITT_AB - SCHRITT_AB // 2 + 1)
        x = X_OBEN + round((X_ENDE - X_OBEN) * t / (WEG - AB))
        return x, SCHRITT_B if tief else SCHRITT_A, False, tief
    return None


def spur_bis(f):
    """Bis zu dieser Spalte liegen Abdrücke (hinter der Ferse des Wanderers)."""
    w = wanderer(f)
    if w:
        return w[0] + 1
    return -1 if f < KOMMT else B


def vogel(f):
    """Ort und Figur des Vogels – oder None."""
    if not VOGEL_DA <= f < VOGEL_WEG:
        return None
    (mx, my), (rx, ry) = VOGEL_MITTE, VOGEL_RADIUS
    x0, y0 = mx - rx, my                                             # Einstieg links am Kreis
    schlag = SCHLAG[f // 2 % 4]
    if f < VOGEL_KREIST:                                             # kommt von links oben
        a = 1 - (f - VOGEL_DA) / (VOGEL_KREIST - VOGEL_DA)
        return x0 - 10 * a, y0 - 5 * a, schlag
    if f < VOGEL_FORT:                                               # kreist (ganze Umläufe), gleitet
        w = math.pi + 2 * math.pi * (f - VOGEL_KREIST) / VOGEL_UMLAUF
        figur = VOGEL_SCHMAL if abs(math.sin(w)) < 0.4 else VOGEL_GLEITET        # in der Kehre von vorn
        return mx + rx * math.cos(w), my - ry * math.sin(w), figur
    a = (f - VOGEL_FORT) / (VOGEL_WEG - VOGEL_FORT)                  # zieht nach links oben davon
    return x0 - 24 * a, y0 - 6 * a * a, schlag


def bilder():
    liste = []
    for f in range(255):
        bild = Bild()
        for y in range(16):                                          # Himmel in Streifen
            bild.rechteck(0, y, B, 1, HIMMEL[y])
        for y, von, bis in SONNE:                                    # Sonne im Sattel
            bild.rechteck(von, y, bis - von + 1, 1, SONNENROT)
        for x in range(B):                                           # Nachbargipfel davor
            y0 = fern_y(x)
            for y in range(y0, 16):
                bild.setze(x, y, FERN if y > y0 else FERN_GLUT if x >= FERN_SPITZE else FERN_SCHNEE)
        v = vogel(f)
        if v:
            bild.figur(round(v[0]) - 2, round(v[1]) - 2, v[2], {"x": SCHWARZ})
        bild.rechteck(KREUZ_X, 2, 1, 5, KREUZ)                       # Gipfelkreuz mit Schneehaube
        bild.rechteck(KREUZ_X - 1, 3, 3, 1, KREUZ)
        bild.setze(KREUZ_X, 1, KANTE)
        wind_x = (f - WIND) * WIND_TEMPO - 3 if WIND <= f < WIND_ENDE else None     # Spalte der Windfront
        bis = spur_bis(f)
        for x in range(B):                                           # Hang mit Spur
            y0 = hang_y(x)
            farbe = KANTE
            if x < bis and abdruck(x) and f < WIND_ENDE:
                farbe = ABDRUCK
                if wind_x is not None and x < wind_x:                # hinter der Front erst halb, dann ganz zu
                    farbe = VERWEHT if x >= wind_x - 6 else KANTE
            bild.setze(x, y0, farbe)
            for y in range(y0 + 1, 16):
                bild.setze(x, y, HANG)
        if wind_x is not None:                                       # Schneestaub im Wind
            for dx, dy in WEHEN:                                     # kurze Fahnen dicht über dem Hang
                x = round(wind_x) + dx
                if 0 <= x < B:
                    bild.rechteck(x - 1, hang_y(x) - dy, 2, 1, STAUB)
        w = wanderer(f)
        if w:
            x, figur, gespiegelt, tief = w
            boden = hang_y(x + 3) + (1 if tief else 0)               # sinkt bei jedem Schritt ein
            bild.figur(x, boden - len(figur), figur, FARBEN, spiegeln=gespiegelt)
            if 1 <= tief <= 2:                                       # Schnee stäubt vor und hinter dem Schuh
                bild.setze(x - 1 - tief, boden - 1 - tief, STAUB)
                bild.setze(x + 7 + tief, boden - 1 - tief, STAUB)
        liste.append(bild)
    return liste
