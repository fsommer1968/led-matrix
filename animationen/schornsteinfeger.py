"""Schornsteinfeger bringt Glück: mondhelle Nacht über verschneiten Dächern. Links klettert der
Schornsteinfeger über den First – schwarzer Zylinder, schwarze Kluft mit goldenen Knöpfen, weißes
Gesicht mit Rußfleck, die Leiter auf der Schulter, Kugel und Bürste am Seil in der Hand. Er stapft
zum Kamin, lässt Kugel und Bürste hinein und kehrt in drei Zügen; bei jedem stiebt oben Ruß heraus
und fällt im Bogen über das Dach. Dann zieht er das Gerät wieder hoch (eine Rußwolke quillt
hinterher), stellt es ab, winkt, lüftet den Zylinder und wirft sechs kleine grüne Glückskleeblätter,
die schaukelnd am Dach vorbei herabsegeln. Er nimmt sein Gerät, geht am Kamin vorbei, steigt aufs
tiefere Nachbardach hinunter und zieht vor dem Mond rechts aus dem Bild; eine Sternschnuppe fällt,
die Dächer liegen da wie am Anfang. Die Runde schließt ohne Sprung – 255 Bilder.

Schwarz ist auf der Matrix aus. Darum ist der Himmel nicht schwarz, sondern ein gedämpftes
Mondnacht-Blau: Zylinder und Kluft bleiben echte schwarze Schattenrisse davor (und vor Schnee und
Mond), Gesicht, Knöpfe, Leiter und Gerät leuchten. Auch der Ruß ist schwarz mit grauem Rand.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum waagerechte Firste (alle Dachspalten gleich), die
Kamine aus Rechtecken, die Leiter senkrecht (zwei gleiche Holme), vier Sterne, Ruß in wenigen
Flocken und Blöcken, sechs Kleeblätter, die einander nie überdecken. Die Sterne laufen in
Perioden, die 255 teilen (51, 85).
"""
import math

from basis import SCHWARZ, B, Bild, dimmen, mischen, sternschnuppe

NAME = "schornsteinfeger"
TITEL = "Schornsteinfeger bringt Glück"

HIMMEL = (0, 24, 96)                           # Mondnacht: gedämpftes Blau, davor steht die Kluft schwarz
KANTE = (215, 225, 250)                        # Schnee auf dem First
SCHNEE_MATT = (78, 90, 140)                    # darunter gedämpft (große Fläche)
DACH = (120, 28, 22)                           # Ziegel unter dem Schnee: nur die Traufe schaut heraus
GIEBEL = (40, 46, 80)                          # Kante am Ende des großen Dachs
KANTE_FERN = (170, 180, 215)                   # Schnee auf dem Nachbardach (etwas matter)
ZIEGEL = (165, 55, 28)
FUGE = (95, 32, 20)
RAND = (215, 120, 60)                          # Kranz oben am Kamin
MOND = (245, 205, 90)                          # gelber Mond: hebt sich vom weißen Gesicht ab
STERN = (255, 240, 200)
STERNE = [(4, 1, 0, 51), (20, 3, 20, 85), (41, 1, 40, 51), (62, 3, 10, 85)]   # x, y, Phase, Periode
KLUFT = SCHWARZ
GESICHT = (240, 220, 205)
AUGE = (50, 25, 10)
FLECK = (95, 90, 100)                          # Rußfleck auf der Wange
KNOPF = (255, 190, 0)
HOLZ = (95, 40, 0)                             # Leiter
SEIL = (170, 150, 100)
BUERSTE = (205, 205, 220)
KUGEL = (105, 110, 140)
GLANZ = (175, 180, 205)                        # Glanzpunkt auf der Kugel
RUSS = (105, 100, 110)
KLEE = (60, 255, 60)
KLEE_DUNKEL = (0, 140, 30)

FIRST = 12                                     # Zeile der Schneekante; der Feger steht darauf
HAUS_B = 46                                    # so breit ist das große Dach, rechts davon das Nachbardach
NACHBAR = 14                                   # … dessen First zwei Zeilen tiefer liegt
KAMIN_X, KAMIN_B = 30, 5                       # Schaft: links, Breite; Kranz je 1 breiter
KRANZ_Y = 7
MITTE = KAMIN_X + KAMIN_B // 2                 # 32
MOND_X, MOND_Y = 55, 4
NACHBAR_KAMIN = 58                             # kleiner Kamin auf dem Nachbardach: links, 3 breit, mit Schneehaube

# Feger von der Seite (Blick nach rechts), 5 breit, 10 hoch: z Zylinder, h Gesicht, a Auge,
# r Rußfleck, k Kluft, g Knopf
ZYLINDER = [".zzz.", ".zzz.", "zzzzz"]
RUMPF = [".hha.", ".rhh.", ".kgk.", ".kkk.", ".kgk."]
BEINE = [[".k.k.", ".k.k."], [".kkk.", "..k.."]]
FARBEN = {"z": KLUFT, "k": KLUFT, "h": GESICHT, "a": AUGE, "r": FLECK, "g": KNOPF}
LEITER = ["l.l", "lll"]                        # im Wechsel, 9 Zeilen, hinter dem Rücken
GERAET = ["bbbbb", "..o..", ".oGo.", "..o.."]  # Bürste, darunter die Kugel
OBEN_Y = FIRST - 10                            # oberste Zeile des Zylinders, wenn er steht

# ── Ablauf ─────────────────────────────────────────────────────────
X_AUF, X_VOR, X_KAMIN = 8, 20, 24              # linke Kante: Aufstieg, vor dem Kamin, am Kamin
X_STUFE, X_FORT = HAUS_B - 3, B + 3            # Tritt hinunter aufs Nachbardach; aus dem Bild
T_AUF = 4                                      # klettert herauf: Sprosse für Sprosse
T_OBEN = T_AUF + 24                            # 28: steht auf dem First
T_LOS = T_OBEN + 4                             # 32: stapft los
T_VOR = T_LOS + (X_VOR - X_AUF) * 2            # 56: vor dem Kamin
T_HEBT = T_VOR + 2                             # 58: hebt das Gerät
T_TRITT = T_HEBT + 6                           # 64: tritt an den Kamin
T_SENKT = T_TRITT + 8                          # 72: lässt das Gerät hinab
T_KEHRT = T_SENKT + 10                         # 82: drei Züge, je 8 Bilder
T_ZIEHT = T_KEHRT + 24                         # 106: zieht hoch
T_ZURUECK = T_ZIEHT + 8                        # 114: tritt zurück
T_STELLT = T_ZURUECK + 8                       # 122: stellt das Gerät ab
T_WINKT = T_STELLT + 6                         # 128: winkt
T_GRUSS = T_WINKT + 12                         # 140: lüftet den Zylinder
T_WIRFT = T_GRUSS + 8                          # 148: drei Würfe, je 8 Bilder
T_NIMMT = T_WIRFT + 24                         # 172: nimmt das Gerät wieder
T_WEITER = T_NIMMT + 2                         # 174: geht weiter
T_FORT = T_WEITER + 72                         # 246: rechts aus dem Bild
T_SCHNUPPE = 243                               # zum Schluss eine Sternschnuppe über dem leeren Dach (bis 252)
HEBEN = [(6, 5), (7, 4), (7, 3), (8, 2), (8, 1), (8, 0)]             # Hand (dx, dy) vom Tragen bis über den Kamin
ZUG = [1, 0, 0, 1, 2, 2, 2, 2]                 # Hand beim Kehren: hoch, halten, wieder hinab
WINKEN = [(6, 3), (5, 1), (5, 1), (7, 2), (7, 2), (7, 2), (5, 1), (5, 1), (5, 1), (7, 2), (7, 2), (6, 2)]
GRUSS = [1, 2, 2, 2, 2, 2, 1, 0]               # so hoch lüftet er den Zylinder
WERFEN = [(5, 6), (6, 5), (7, 3), (7, 1), (7, 1), (7, 1), (7, 3), (6, 5)]   # ausholen, oben loslassen (3 und 5)
# Kleeblätter: losgelassen (Bild nach T_WIRFT), Weite (Spalten), Sinktempo, Schaukelphase
KLEEBLAETTER = [(3, 14, 0.30, 4.5), (5, -14, 0.26, 0.2), (11, 2, 0.26, 3.3), (13, -6, 0.28, 4.2),
                (19, 21, 0.29, 3.2), (21, 11, 0.30, 2.3)]
# Rußflocken je Zug: Tempo nach rechts und nach oben (je Bild); sie fliegen im Bogen und fallen vor dem Dach hinab
FLOCKEN = [(-0.8, -1.3), (-0.3, -1.8), (0.45, -1.6), (0.9, -1.2)]
FALL = 0.16                                    # so viel schneller fällt eine Flocke je Bild


def klettern(k):
    """Zeilen, die er nach k Bildern geschafft hat: je Sprosse zwei Zeilen in zwei Bildern, dann zwei Bilder Halt."""
    return 2 * (k // 4) + min(k % 4, 2)


def flocke(vx, vy, k):
    """Wo eine Rußflocke k Bilder nach dem Zug ist: Spalten und Zeilen ab der Kaminöffnung (Wurfbogen)."""
    return round(vx * k), round(vy * k + FALL * k * k)


def feger(bild, x, y, schritt, hand, hut=0):
    """Feger mit linker Kante x und Zylinder-Oberkante y; hand = (dx, dy) der vorderen Hand,
    hut = so viele Zeilen ist der Zylinder gelüftet."""
    for k in range(9):                                               # Leiter auf der Schulter
        bild.figur(x - 3, y - 1 + k, [LEITER[k % 2]], {"l": HOLZ})
    bild.figur(x, y - hut, ZYLINDER, FARBEN)
    bild.figur(x, y + 3, RUMPF + BEINE[schritt], FARBEN)
    bild.setze(x, y + 5, KLUFT)                                      # hinterer Arm hält die Leiter
    bild.linie(x + 4, y + 5, x + hand[0], y + hand[1], KLUFT)
    bild.setze(x + hand[0], y + hand[1], GESICHT)


def geraet(bild, cx, y):
    """Bürste (Zeile y) und Kugel darunter, Mitte cx."""
    bild.figur(cx - 2, y, GERAET, {"b": BUERSTE, "o": KUGEL, "G": GLANZ})


def dach(bild):
    """Großes Dach mit dickem Schnee, rechts das tiefere Nachbardach."""
    bild.rechteck(0, FIRST, HAUS_B, 1, KANTE)
    bild.rechteck(0, FIRST + 1, HAUS_B, 2, SCHNEE_MATT)
    bild.rechteck(0, FIRST + 3, HAUS_B, 1, DACH)
    bild.rechteck(HAUS_B - 1, FIRST + 1, 1, 3, GIEBEL)
    bild.rechteck(NACHBAR_KAMIN, NACHBAR - 3, 3, 3, ZIEGEL)
    bild.rechteck(NACHBAR_KAMIN - 1, NACHBAR - 4, 5, 1, KANTE_FERN)   # Schneehaube
    bild.rechteck(HAUS_B, NACHBAR, B - HAUS_B, 1, KANTE_FERN)
    bild.rechteck(HAUS_B, NACHBAR + 1, B - HAUS_B, 1, SCHNEE_MATT)


def wolke(bild, cx, y, farbe, kern):
    """Rußwolke 5×3: Rand in farbe, Kern dunkel."""
    bild.rechteck(cx - 1, y, 3, 3, farbe)
    bild.rechteck(cx - 2, y + 1, 5, 1, farbe)
    bild.rechteck(cx - 1, y + 1, 3, 1, kern)


def kleeblatt(bild, x, y, quer):
    x, y = round(x), round(y)
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)) if quer else ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        bild.setze(x + dx, y + dy, KLEE)
    bild.setze(x, y, KLEE_DUNKEL)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        sternschnuppe(bild, f, T_SCHNUPPE, 30, 0)
        bild.kreis(MOND_X, MOND_Y, 3, MOND)

        # Wo steht der Feger, was macht die vordere Hand, wo ist das Gerät?
        x, y, schritt, hand, hut, da = X_AUF, OBEN_Y, 0, HEBEN[0], 0, T_AUF <= f < T_FORT
        seil = None                                                  # Seillänge, sobald das Gerät über dem Kamin hängt
        steht = None                                                 # Gerät abgestellt: Mitte
        if f < T_OBEN:                                               # klettert über den First
            y = OBEN_Y + 12 - klettern(f - T_AUF)
        elif f < T_LOS:
            pass
        elif f < T_VOR:                                              # stapft zum Kamin
            x = X_AUF + (f - T_LOS + 1) // 2
            schritt = ((f - T_LOS) // 4) % 2
        elif f < T_HEBT:
            x = X_VOR
        elif f < T_TRITT:                                            # hebt das Gerät hoch
            x, hand = X_VOR, HEBEN[f - T_HEBT]
        elif f < T_SENKT:                                            # tritt an den Kamin
            x = min(X_KAMIN, X_VOR + (f - T_TRITT + 1) // 2)
            schritt, hand = ((f - T_TRITT) // 4) % 2, HEBEN[-1]
        elif f < T_KEHRT:                                            # lässt Kugel und Bürste hinab
            k = f - T_SENKT
            x, hand, seil = X_KAMIN, (8, max(0, k - 7)), min(k // 2 + 1, 4)
        elif f < T_ZIEHT:                                            # kehrt: drei Züge auf und ab
            x, hand, seil = X_KAMIN, (8, ZUG[(f - T_KEHRT) % 8]), 4
        elif f < T_ZURUECK:                                          # zieht das Gerät hoch
            k = f - T_ZIEHT
            x, hand, seil = X_KAMIN, (8, (1, 0, 0, 0, 0, 0, 0, 0)[k]), (4, 4, 3, 3, 2, 2, 1, 0)[k]
        elif f < T_STELLT:                                           # tritt zurück
            x = max(X_VOR, X_KAMIN - (f - T_ZURUECK + 1) // 2)
            schritt, hand = ((f - T_ZURUECK) // 4) % 2, HEBEN[-1]
        elif f < T_WINKT:                                            # stellt das Gerät ab
            x, hand = X_VOR, HEBEN[max(0, 4 - (f - T_STELLT))]
        elif f < T_GRUSS:                                            # winkt
            x, hand, steht = X_VOR, WINKEN[f - T_WINKT], X_VOR + 6
        elif f < T_WIRFT:                                            # lüftet den Zylinder
            hut = GRUSS[f - T_GRUSS]
            x, hand, steht = X_VOR, (5, 2 - hut), X_VOR + 6
        elif f < T_NIMMT:                                            # wirft Kleeblätter
            x, hand, steht = X_VOR, WERFEN[(f - T_WIRFT) % 8], X_VOR + 6
        elif f < T_WEITER:
            x = X_VOR
        else:                                                        # geht am Kamin vorbei, steigt aufs Nachbardach
            x = X_VOR + round((f - T_WEITER + 1) * (X_FORT - X_VOR) / (T_FORT - T_WEITER))
            y = OBEN_Y + max(0, min(NACHBAR - FIRST, x - X_STUFE))
            schritt = ((f - T_WEITER) // 4) % 2

        hx, hy = x + hand[0], y + hand[1]                            # vordere Hand
        im_kamin = seil is not None
        if da and im_kamin:                                          # Seil und Gerät verschwinden im Kamin
            bild.rechteck(hx, hy + 1, 1, KRANZ_Y - hy - 1, SEIL)
            if seil < 4:
                geraet(bild, hx, OBEN_Y + 1 + seil)

        # Kamin
        bild.rechteck(KAMIN_X, KRANZ_Y + 1, KAMIN_B, FIRST - KRANZ_Y - 1, ZIEGEL)
        bild.rechteck(KAMIN_X, KRANZ_Y + 3, KAMIN_B, 1, FUGE)
        bild.rechteck(KAMIN_X - 1, KRANZ_Y, KAMIN_B + 2, 1, RAND)

        for vorn in (False, True):                                   # beim Heraufklettern hinter dem First
            if da and vorn == (f >= T_OBEN):
                feger(bild, x, y, schritt, hand, hut)
                if steht is not None:
                    geraet(bild, steht, FIRST - 4)
                elif not im_kamin:
                    geraet(bild, hx, hy + 1)
            if not vorn:
                dach(bild)

        # Ruß stiebt bei jedem Zug aus dem Kamin: Flocken fliegen im Bogen und fallen vor dem Dach hinab
        for zug in range(3):
            k = f - (T_KEHRT + zug * 8)
            if 0 <= k < 3:
                bild.rechteck(MITTE - 1, KRANZ_Y - 1, 3, 1, SCHWARZ)
            seite = -1 if zug == 1 else 1
            for vx, vy in FLOCKEN:
                for alter, farbe in ((1, RUSS), (0, SCHWARZ)):       # grauer Schweif, davor die schwarze Flocke
                    if k - alter >= 1:
                        dx, dy = flocke(vx, vy, k - alter)
                        bild.setze(MITTE + seite * dx, KRANZ_Y - 1 + dy, farbe)
        # Rußwolke, wenn die Bürste wieder herauskommt: steigt, zieht nach rechts und verweht
        k = f - (T_ZIEHT + 2)
        if 0 <= k < 4:
            bild.rechteck(MITTE - 1, KRANZ_Y - 2, 3, 2, RUSS)
            bild.rechteck(MITTE - 1, KRANZ_Y - 1, 3, 1, SCHWARZ)
        elif 4 <= k < 20:
            stufe = k // 4                                           # 1 … 4
            wolke(bild, MITTE + stufe - 1, KRANZ_Y - 2 - 2 * stufe,
                  mischen(RUSS, HIMMEL, (stufe - 1) * 0.25), SCHWARZ if stufe < 3 else HIMMEL)

        # Kleeblätter: fliegen im Bogen aus der Hand und segeln schaukelnd herab
        for los, weite, sink, phase in KLEEBLAETTER:
            t = f - T_WIRFT - los
            if t < 0:
                continue
            u = min(t, 12) / 12
            kx = X_VOR + 7 + weite * u * (2 - u) + 2 * math.sin(t / 5 + phase) * min(1, t / 12)
            ky = OBEN_Y + 1 - 2 * math.sin(min(t, 8) / 8 * math.pi / 2) + sink * max(0, t - 8)
            if ky < 17:
                kleeblatt(bild, kx, ky, (t // 6) % 2)
        liste.append(bild)
    return liste
