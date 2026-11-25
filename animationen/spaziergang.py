"""Winterspaziergang zwischen den Jahren: verschneite Hügel am späten Nachmittag, die orangerote
Wintersonne sinkt langsam ins Tal, der Himmel geht dabei von Hellblau über Orange in Dämmerblau;
dunkle Tannen. Vater, Mutter und Kind stapfen mit bunten Mützen und Schals von links nach rechts
durch den Schnee, am Wegkreuz vorbei; der Hund tollt voraus, wälzt sich im Schnee und jagt einem
Schneeball nach. Hinter allen bleiben Spuren. Sind sie rechts hinaus, weht ein Windstoß die Spuren
zu, und es wird wieder hell – die Runde geht ohne Sprung in sich über, 255 Bilder.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum ein Himmel aus waagerechten Streifen (in jeder Spalte gleich; er
färbt sich Zeile für Zeile um, das kostet nichts), Hügel mit wenigen Stufen, die unter Tanne und
Kreuz liegen, vier gleiche Tannen im Vierertakt der Spuren (Kopien kosten fast nichts) und Leute,
die nur drei Spalten breit sind.
"""
from basis import B, GELB, PINK, ROT, SCHWARZ, TUERKIS, WEISS, Bild

NAME = "spaziergang"
TITEL = "Winterspaziergang zwischen den Jahren"

# ── Farben (deutlich verschiedene Stufen, große Flächen gedämpft) ──
# An der Matrix gemessen (25.11.2026): Braun und Hauttöne wirken orange. Darum ist alles Braune
# (Kreuz, Hosen, Fell) deutlich dunkler und weniger gesättigt, das Gesicht blasser, das Auge schwarz.
HIMMEL = (35, 115, 185)                        # hellblau
GLUT = (140, 70, 0)                            # oranger Streifen über den Hügeln
DAEMMER = (22, 28, 95)                         # Dämmerblau
SONNE = (255, 45, 0)
FERN = (70, 85, 140)                           # Hügel hinten, Schnee im Schatten
GRAT = (150, 165, 215)                         # ihr Grat, heller
KANTE = (215, 225, 250)                        # Oberkante des Schnees vorn
BODEN = (105, 118, 165)
SPUR = (40, 50, 105)                           # Fußstapfen
TANNE = (0, 95, 35)
HOLZ = (105, 68, 45)
HOSE = (80, 55, 42)
GESICHT = (255, 190, 145)
AUGE = SCHWARZ
FELL = (165, 100, 55)
FELL_DUNKEL = (70, 45, 32)

KANTE_Y = 11                                   # Zeile der Schneekante vorn, darunter der Weg
GRUND = 13                                     # in dieser Zeile stehen die Leute, hier liegen ihre Spuren
HUND_GRUND = 14                                # der Hund läuft eine Zeile weiter vorn
TAKT = 4                                       # Spuren alle vier Spalten
PFOTEN_VERSATZ, PFOTEN_Y = 2, 14               # Pfotenspuren: Versatz zu den Stiefeln, Zeile
FERN_STUFEN = [(0, 7), (12, 6), (25, 7)]       # ab x: oberste Zeile des Hügels (Stufen unter Tanne und Kreuz)
TANNE_OBEN = 2                                 # alle Tannen in denselben Zeilen, auch vor dem höheren Hügel
SONNE_X = 44
SATTEL = {41: 8, 42: 9, 43: 10, 44: 10, 45: 10, 46: 9, 47: 8}      # Tal, in dem die Sonne versinkt
TANNEN = [4, 12, 52, 60]                       # im Vierertakt der Spuren: so sind es Kopien
KREUZ_X = 22
KREUZ = ["..w..", ".wkw.", "w.k.w", ".kkk.", "..k..", "..k..", "..k.."]     # Wegkreuz mit Schneedach

# Himmel in Stufen: (Dämmerblau bis Zeile, Glut ab Zeile, Sonnenmitte) – je Stufe ändert sich
# eine Zeile oder die Sonne rückt ein Pixel
STUFEN = [(0, 7, 4), (0, 6, 4), (0, 6, 5), (0, 5, 5), (1, 5, 6), (2, 5, 6), (2, 4, 7), (3, 4, 7),
          (4, 4, 8), (5, 5, 8), (5, 5, 9), (6, 6, 9), (6, 6, 10), (7, 7, 10), (7, 7, 11)]
ABEND_AB, ABEND_TAKT = 8, 11                   # die Sonne sinkt: alle elf Bilder eine Stufe
MORGEN_AB, MORGEN_TAKT = 178, 5                # im Wind wird es wieder hell: alle fünf Bilder

# ── Familie: (Abstand zum Schluss, Kopf und Rumpf, Farben, Schritt-Takt, Versatz) ──
# m Mütze, o Bommel, h Gesicht, a Auge, s Schal, j Jacke, b Beine
GROSS = ["mmm", "mmm", "hha", "sss", "jjj", "jjj", "jjj"]
MITTEL = [".o.", "mmm", "hha", "sss", "jjj", "jjj", "jjj"]
KLEIN = [".o.", "mmm", "hha", "sss", "jjj"]
# Schritt in vier Teilen: vorderer Fuß gehoben, eingesunken, hinterer Fuß gehoben, eingesunken
BEINE = [["b.b", "b.."], ["b.b"], ["b.b", "..b"], ["b.b"]]
FAMILIE = [
    (0, MITTEL, {"m": GELB, "o": WEISS, "s": TUERKIS, "j": (190, 0, 255)}, 4, 0),      # Mutter
    (5, GROSS, {"m": ROT, "s": GELB, "j": (0, 70, 255)}, 4, 2),                        # Vater
    (11, KLEIN, {"m": PINK, "o": WEISS, "s": ROT, "j": (40, 230, 60)}, 3, 1),          # Kind vorneweg
]
FAMILIE_BREIT = 14
FAMILIE_AB = 6                                 # ab hier kommt die Familie ins Bild, ein Pixel je zwei Bilder

# ── Hund (Blick nach rechts): b Fell, c rotes Halstuch, t Rute, e Ohr, h Kopf, n Nase, l Läufe ──
HUND_STEHT = ["....e.", "t..hhn", ".bbbc.", ".l..l."]
HUND_WEDELT = ["t...e.", "...hhn", ".bbbc.", ".l..l."]
HUND_LAUF = [["....e.", "t..hhn", ".bbbc.", "l....l"], ["....e.", "t..hhn", ".bbbc.", "..ll.."]]
HUND_WAELZT = [[".l.l..", "tbbbch", ".bbbbe"], ["..l.l.", ".bbbch", "tbbbbe"]]
HUND_GRAEBT = [["t.....", ".bbb..", ".bbbce", ".l..hn"], [".t....", ".bbb..", ".bbbce", ".l.lhn"]]
HUND_FARBEN = {"b": FELL, "c": ROT, "h": FELL, "t": FELL_DUNKEL, "e": FELL_DUNKEL, "n": AUGE,
               "l": FELL_DUNKEL}

# Weg des Hundes: (Bild, x) – dazwischen gleichmäßig
HUND_WEG = [(1, -7), (26, 35), (69, 35), (84, 54), (116, 54), (128, 66)]
WAELZT_AB, WAELZT_BIS = 30, 62                 # wälzt sich im Schnee
WURF, LANDUNG = 66, 84                         # das Kind wirft den Schneeball, der Hund jagt ihm nach
SATZ = [1, 2, 2, 1]                            # … und springt zuletzt danach (Pixel über dem Boden)
BALL_ZIEL = 60
GRAEBT_BIS = 108                               # wühlt dort im Schnee, schaut sich dann um und läuft voraus

WIND_AB, WIND_BIS = 172, 250                   # der Windstoß weht die Spuren zu
WIND_TEMPO = 1.25
BOEEN = [(10, 0, 3), (13, -9, 2), (14, -20, 3), (12, -31, 2)]        # Zeile, Versatz, Länge


def fern_y(x):
    """Oberste Zeile der Hügel hinten in Spalte x."""
    if x in SATTEL:
        return SATTEL[x]
    y = FERN_STUFEN[0][1]
    for ab, oben in FERN_STUFEN:
        if x >= ab:
            y = oben
    return y


def stufe(f):
    """Stand des Abends: steigt während des Spaziergangs, fällt am Schluss zügig wieder auf null."""
    hoch = len(STUFEN) - 1
    if f < MORGEN_AB:
        return max(0, min(hoch, (f - ABEND_AB) // ABEND_TAKT + 1))
    return max(0, hoch - (f - MORGEN_AB) // MORGEN_TAKT - 1)


def tanne(bild, x):
    """Dunkle Tanne vor dem Hügel: sechs Zeilen, alle zwei Zeilen eine Stufe breiter."""
    for k in range(6):
        halb = k // 2
        bild.rechteck(x - halb, TANNE_OBEN + k, 2 * halb + 1, 1, TANNE)


def hund_x(f):
    """Linke Spalte des Hundes, None außerhalb seines Weges."""
    for (f0, x0), (f1, x1) in zip(HUND_WEG, HUND_WEG[1:]):
        if f0 <= f <= f1:
            return x0 + (x1 - x0) * (f - f0) / (f1 - f0)
    return None


def familie_x(f):
    """Linke Spalte der Mutter (sie geht am Schluss)."""
    return -FAMILIE_BREIT - 2 + (f - FAMILIE_AB) // 2


def bilder():
    liste = []
    hund_spur = -1                                                   # so weit ist der Hund schon gelaufen
    for f in range(255):
        dunkel_bis, glut_ab, sonne_y = STUFEN[stufe(f)]
        bild = Bild(HIMMEL)
        bild.rechteck(0, 0, B, dunkel_bis, DAEMMER)
        bild.rechteck(0, glut_ab, B, 16 - glut_ab, GLUT)
        bild.kreis(SONNE_X, sonne_y, 2.2, SONNE)
        for x in range(B):                                           # Hügel hinten
            bild.rechteck(x, fern_y(x), 1, KANTE_Y - fern_y(x), FERN)
            bild.setze(x, fern_y(x), GRAT)
        for x in TANNEN:
            tanne(bild, x)
        bild.rechteck(0, KANTE_Y, B, 1, KANTE)                       # Schnee vorn
        bild.rechteck(0, KANTE_Y + 1, B, 4, BODEN)
        bild.figur(KREUZ_X, KANTE_Y + 1 - len(KREUZ), KREUZ, {"k": HOLZ, "w": KANTE})

        # Spuren: bleiben liegen, bis der Wind sie von links her zuweht. Stiefel und Pfoten im
        # selben Vierertakt, um zwei Spalten versetzt: vor der Familie eine Reihe, hinter ihr zwei.
        fx = familie_x(f)
        hx = hund_x(f)
        if hx is not None:
            hund_spur = max(hund_spur, round(hx))
        geweht = (f - WIND_AB) * WIND_TEMPO if f >= WIND_AB else -1
        for x in range(0, B, TAKT):
            if geweht < x < fx + FAMILIE[-1][0]:                   # bis hinter das Kind
                bild.setze(x, GRUND, SPUR)
            if geweht < x + PFOTEN_VERSATZ < hund_spur:
                bild.setze(x + PFOTEN_VERSATZ, PFOTEN_Y, SPUR)

        # Familie
        for ab, rumpf, farben, takt, versatz in FAMILIE:
            x = fx + ab
            if not -4 < x < B + 1:
                continue
            zeilen = rumpf + BEINE[((f + versatz) // takt) % 4]
            oben = GRUND + 1 - len(zeilen)
            bild.figur(x, oben, zeilen, {"h": GESICHT, "a": AUGE, "b": HOSE, **farben})
            schal = oben + rumpf.index("sss")
            bild.setze(x - 1, schal + ((f + versatz) // 3) % 2, farben["s"])        # Schal flattert
            if rumpf is KLEIN and WURF - 5 <= f < WURF + 2:                          # holt aus und wirft
                bild.setze(x + 3, schal - (1 if f < WURF else -1), farben["j"])

        # Schneeball: das Kind wirft ihn in hohem Bogen voraus
        if WURF <= f < LANDUNG:
            t = (f - WURF) / (LANDUNG - WURF)
            start = familie_x(WURF) + 15
            bild.setze(start + (BALL_ZIEL - start) * t, 9 - 26 * t * (1 - t) + 4 * t, WEISS)

        # Hund
        if hx is not None:
            x = round(hx)
            if WAELZT_AB <= f < WAELZT_BIS:
                k = (f // 3) % 2
                bild.figur(x, HUND_GRUND - 2, HUND_WAELZT[k], HUND_FARBEN)
                bild.setze(x - 2 + 9 * k, HUND_GRUND - 1 - (f % 3), WEISS)          # Schnee stiebt
            elif LANDUNG - 3 <= f < LANDUNG + 1:                                     # Satz nach dem Ball
                bild.figur(x, HUND_GRUND - 3 - SATZ[f - LANDUNG + 3], HUND_LAUF[0], HUND_FARBEN)
            elif LANDUNG + 1 <= f < GRAEBT_BIS:
                k = (f // 2) % 2
                bild.figur(x, HUND_GRUND - 3, HUND_GRAEBT[k], HUND_FARBEN)
                bild.setze(x + 6 + (f % 3), HUND_GRUND - 1 - (f % 3), WEISS)
            else:
                vor = hund_x(max(1, f - 1))
                if hx == vor:                                        # steht und wedelt
                    zeilen = HUND_WEDELT if (f // 2) % 2 else HUND_STEHT
                    bild.figur(x, HUND_GRUND - 3, zeilen, HUND_FARBEN, spiegeln=f >= GRAEBT_BIS)
                else:
                    bild.figur(x, HUND_GRUND - 3, HUND_LAUF[(f // 2) % 2], HUND_FARBEN)

        # Windstoß: Schneefahnen fegen über den Weg
        if WIND_AB <= f < WIND_BIS:
            for zeile, versatz, lang in BOEEN:
                kopf = round(geweht + versatz)
                for k in range(lang):
                    if 0 <= kopf - k < B:
                        bild.setze(kopf - k, zeile, WEISS)
        liste.append(bild)
    return liste
