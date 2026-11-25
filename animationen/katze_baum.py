"""Katze spielt mit dem Christbaum: Neben den Geschenken steht der geschmückte Baum, links hängt
eine rote Kugel am Zweig. Eine grau getigerte Katze schleicht heran, duckt sich, wackelt mit dem
Hinterteil und schlägt mit der Pfote nach der Kugel – die pendelt. Dann springt die Katze in den
Baum, der Baum schwankt, die Kugel fällt und kullert davon; nur der Schwanz schaut noch heraus,
dann zwei gelbe Augen und der Kopf. Zum Schluss holt die Katze die Kugel, hängt sie wieder auf,
als wäre nichts gewesen, und trollt sich. Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum einfarbige Wand, der Baum in einer Farbe und aus
Spaltenpaaren (immer zwei gleiche Spalten nebeneinander, die Kugeln 2×2 genau auf einem Paar),
fünf Kugeln und sieben Lichter, die langsam in drei Gruppen wechseln (alle 1,7 s), Bänder der
Geschenke waagerecht oder zwei Spalten breit. Der schwankende Baum ist dasselbe Bild, nur je
Etage verschoben.
"""
import math

from basis import B, GELB, GOLD, ORANGE, PINK, ROT, TUERKIS, WEISS, Bild, dimmen, mischen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "katze_baum"
TITEL = "Katze spielt mit dem Christbaum"

WAND = (10, 6, 26)                             # Blau +1 (gleiche Nachbarbilder im GIF) zeigt die Matrix genauso
BODEN = (33, 17, 5)
TANNE = (0, 105, 28)
STAMM = (41, 21, 5)
LICHT = (255, 200, 80)
BLAU = (0, 90, 255)
BAND = (200, 210, 240)                         # Band und Schleife: nicht ganz weiß, sonst das Hellste im Bild
FELL = (165, 165, 180)
STREIFEN = (85, 85, 105)
NASE = (255, 80, 130)
GLANZ = mischen(ROT, WEISS, 0.55)
KATZE = {"k": FELL, "t": FELL, "d": STREIFEN, "a": GELB, "n": NASE}

M = 44                                         # linke der beiden mittleren Spalten des Baums
# Baum in Zeile y = 2…13 von M − 2n bis M + 1 + 2n: drei Etagen, immer zwei gleiche Spalten nebeneinander
STUFEN = [0, 0, 1, 2, 1, 2, 3, 4, 2, 3, 4, 5]
KUGELN = [(0, 4, GOLD), (-4, 7, BLAU), (4, 8, PINK), (0, 11, TUERKIS), (6, 12, ORANGE)]       # 2×2: x − M, y
LICHTER = [(1, 3, 0), (-2, 6, 1), (7, 9, 2), (3, 11, 0), (-3, 13, 2), (9, 13, 1), (-7, 13, 0)]  # x − M, y, Gruppe
HX, HY = M - 8, 10                             # hier hängt die rote Kugel (2×2) unter dem Zweig
LIEGT_X = 8                                    # bis hierhin kullert sie
DUCK_X, SITZ_X = 19, 26                        # Plätze der Katze vor dem Baum

# Ablauf (Bildnummern)
KOMMT, DUCKT_AB, SITZT_AB, HIEB1, HIEB2, DUCKT2 = 3, 43, 63, 67, 82, 90
SPRUNG_AB, IM_BAUM, FAELLT, AUGEN, KOPF_AB, KOPF_WEG = 98, 107, 112, 132, 138, 155
RUNTER, LANDET, NIMMT, DREHT, TRAEGT, HAENGT, FERTIG, WEG = 160, 169, 177, 180, 185, 195, 201, 211

# Katze (Blick nach rechts, Gesicht zum Betrachter): k Fell, t Schwanz, d Streifen, a Auge, n Nase
SCHLEICHT = [["..........k...k", "..........kkkkk", "tt........kakak", "..tkdkkdkkkknkk",
              "..kkdkkdkkkk...", "..k.k....k.k..."],
             ["..........k...k", "..........kkkkk", ".tt.......kakak", "...kdkkdkkkknkk",
              "..kkdkkdkkkk...", "...k.k..k.k...."]]
GEHT = [["t.........k...k", "t.........kkkkk", "t.........kakak", ".tkdkkdkkkkknkk", "..kdkkdkkkkk...",
         "..k.k....k.k...", "..k.k....k.k..."],
        ["t.........k...k", "t.........kkkkk", ".t........kakak", ".tkdkkdkkkkknkk", "..kdkkdkkkkk...",
         "..k.k....k.k...", "...k.k..k.k...."]]
DUCKT = [["t..............", "t..kkk....k...k", ".tkkdkk...kkkkk", ".kkkdkkdk.kakak",
          ".kkkdkkdkkkknkk", ".kk.....kkk.kk."],
         ["..t............", ".t..kkk...k...k", "..tkkdkk..kkkkk", ".kkkdkkdk.kakak",
          ".kkkdkkdkkkknkk", ".kk.....kkk.kk."]]
SITZT = ["...k...k..", "...kkkkk..", "...kakak..", "...kknkk..", "..kkdkkk..", ".kkkdkkk..",
         "tkkkdkkk..", "ttkk.kk..."]
BLINZELT = SITZT[:2] + ["...kdkdk.."] + SITZT[3:]
PFOTE_HOCH = ["...k...k..", "...kkkkk.k", "...kakakk.", "...kknkk..", "..kkdkk...", ".kkkdkk...",
              "tkkkdkkk..", "ttkk.kk..."]
PFOTE_SCHLAG = ["...k...k..", "...kkkkk..", "...kakak..", "...kknkkkk", "..kkdkk...", ".kkkdkk...",
                "tkkkdkkk..", "ttkk.kk..."]
SPRUNG = ["...........k...k", "tt.........kkkkk", "..tkdkkdkkkkakak", "..kkdkkdkkkkknkk",
          ".kk.........kk.."]
KOPF = ["k....k", "kkkkkk", "kakkak", "kknnkk"]
KOPF_ZU = ["k....k", "kkkkkk", "kdkkdk", "kknnkk"]
# Sprung in den Baum: (x, y) der Figur je Bild; hinunter derselbe Bogen gespiegelt
HINEIN = [(19, 10), (21, 8), (24, 6), (27, 5), (30, 4), (33, 4), (36, 4), (38, 5), (40, 5)]
HERAUS = [(38, 5), (35, 5), (32, 5), (29, 6), (26, 7), (23, 8), (20, 9), (17, 10), (14, 10)]
# Schwanz, der links aus dem Baum schaut: drei Stellungen
SCHWANZ = [[(41, 6), (40, 6), (39, 5), (38, 4)], [(41, 6), (40, 6), (39, 6), (38, 6)],
           [(41, 6), (40, 6), (39, 7), (38, 7)]]
# Kugel fällt und hüpft einmal auf, danach kullert sie nach links
FALL = [(HX, 10), (HX, 11), (HX - 1, 13), (HX - 2, 12), (HX - 3, 11), (HX - 4, 12), (HX - 5, 13)]
ROLLT = 24


def versatz(y, dx):
    """Der Baum schwankt um den Fuß: unterste Etage fest, Mitte um dx, Spitze doppelt."""
    return 0 if y >= 10 else dx if y >= 6 else 2 * dx


def schwanken(f):
    if IM_BAUM <= f < IM_BAUM + 16:                                  # kräftig
        return 1 if ((f - IM_BAUM) // 2) % 2 == 0 else -1
    if IM_BAUM + 16 <= f < IM_BAUM + 28:                             # klingt ab
        return (1, 0, -1, 0)[((f - IM_BAUM - 16) // 3) % 4]
    if KOPF_WEG + 1 <= f < RUNTER:                                   # die Katze dreht sich im Baum um
        return (1, -1)[((f - KOPF_WEG - 1) // 2) % 2]
    return 0


def linke_kante(y):
    """Linker Rand des Baums in Zeile y; über und unter dem Baum keiner."""
    return M - 2 * STUFEN[y - 2] if 2 <= y <= 13 else B


def baum(bild, f, dx):
    for r, n in enumerate(STUFEN):
        bild.rechteck(M - 2 * n + versatz(2 + r, dx), 2 + r, 2 + 4 * n, 1, TANNE)
    bild.rechteck(M, 14, 2, 1, STAMM)
    sx = M + versatz(0, dx)                                          # Stern auf der Spitze
    bild.rechteck(sx - 1, 1, 4, 1, GOLD)
    bild.rechteck(sx, 0, 2, 2, WEISS if (f // 17) % 3 == 0 else GELB)
    for x, y, farbe in KUGELN:
        bild.rechteck(M + x + versatz(y, dx), y, 2, 2, farbe)
    for x, y, gruppe in LICHTER:                                     # Lichterkette: eine Gruppe ruht
        bild.setze(M + x + versatz(y, dx), y, dimmen(LICHT, 0.4) if (f // 17) % 3 == gruppe else LICHT)


def geschenke(bild):
    bild.rechteck(58, 9, 6, 6, BLAU)                                 # groß: Band senkrecht, Schleife
    bild.rechteck(60, 8, 2, 7, BAND)
    bild.rechteck(54, 12, 4, 3, PINK)                                # klein: Band waagerecht
    bild.rechteck(54, 13, 4, 1, GELB)


def katze(bild, x0, y0, zeilen, spiegeln=False, im_baum=False):
    """Zeichnet die Katze; im_baum: nur, was links vom Baum noch zu sehen ist."""
    breite = max(len(z) for z in zeilen)
    for dy, zeile in enumerate(zeilen):
        for dx, c in enumerate(zeile):
            x, y = x0 + (breite - 1 - dx if spiegeln else dx), y0 + dy
            if c != "." and (not im_baum or x < linke_kante(y)):
                bild.setze(x, y, KATZE[c])


def sitzt(bild, x0, figur, f):
    """Sitzende Katze; die Schwanzspitze zuckt ab und zu (liegt dann flach am Boden)."""
    katze(bild, x0, 7, figur)
    if f % 12 < 4:
        bild.setze(x0, 13, WAND)
        bild.setze(x0 - 1, 14, FELL)


def pendel(f):
    """Auslenkung der hängenden Kugel in Spalten (nach einem Pfotenhieb, klingt ab)."""
    for start, weite, dauer, periode in ((HIEB1 + 4, 2, 14, 8), (HIEB2 + 4, 3, 24, 10), (HAENGT + 2, 1, 8, 8)):
        t = f - start
        if 0 <= t < dauer:
            return round(weite * (1 - t / dauer) * math.sin(2 * math.pi * t / periode))
    return 0


def kugel(bild, x, y, glanz=0):
    bild.rechteck(x, y, 2, 2, ROT)
    gx, gy = ((0, 0), (0, 1), (1, 1), (1, 0))[glanz % 4]             # Glanzlicht wandert beim Kullern
    bild.setze(x + gx, y + gy, GLANZ)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(WAND)
        bild.rechteck(0, 15, B, 1, BODEN)
        dx = schwanken(f)
        if SPRUNG_AB <= f < IM_BAUM:                                 # Sprung: verschwindet im Baum
            x, y = HINEIN[f - SPRUNG_AB]
            katze(bild, x, y, SPRUNG, im_baum=True)
        elif RUNTER <= f < LANDET:                                   # … und kommt wieder heraus
            x, y = HERAUS[f - RUNTER]
            katze(bild, x, y, SPRUNG, spiegeln=True, im_baum=True)
        baum(bild, f, dx)
        geschenke(bild)

        # Katze vor dem Baum
        kx = None                                                    # Maul beim Tragen
        if KOMMT <= f < DUCKT_AB:                                    # schleicht heran
            x = round(-15 + (f - KOMMT) * (DUCK_X + 15) / (DUCKT_AB - KOMMT))
            katze(bild, x, 9, SCHLEICHT[(f // 3) % 2])
        elif DUCKT_AB <= f < SITZT_AB:                               # duckt sich, wackelt mit dem Hinterteil
            katze(bild, DUCK_X, 9, DUCKT[((f - DUCKT_AB) // 2) % 2 if f >= DUCKT_AB + 4 else 0])
        elif SITZT_AB <= f < DUCKT2:                                 # setzt sich auf, zwei Pfotenhiebe
            figur = SITZT
            for hieb in (HIEB1, HIEB2):
                if hieb <= f < hieb + 4:
                    figur = PFOTE_HOCH
                elif hieb + 4 <= f < hieb + 7:
                    figur = PFOTE_SCHLAG
            sitzt(bild, SITZ_X, figur, f)
        elif DUCKT2 <= f < SPRUNG_AB:                                # duckt sich zum Sprung
            katze(bild, DUCK_X, 9, DUCKT[((f - DUCKT2) // 2) % 2])
        elif IM_BAUM <= f < RUNTER:                                  # im Baum
            if f <= KOPF_WEG:                                        # Schwanz schaut heraus und pendelt
                vx = versatz(6, dx)
                for x, y in SCHWANZ[(1, 0, 1, 2)[(f // 3) % 4]]:
                    bild.setze(x + vx, y, FELL)
            if AUGEN <= f < KOPF_AB and f != AUGEN + 3:              # zwei Augen im Grünen
                bild.setze(M - 1, 8, GELB)
                bild.setze(M + 2, 8, GELB)
            elif KOPF_AB <= f < KOPF_WEG:                            # der Kopf schaut heraus
                katze(bild, M - 2, 6, KOPF_ZU if f in (KOPF_AB + 9, KOPF_AB + 10) else KOPF)
        elif LANDET <= f < DREHT:                                    # läuft zur Kugel, nimmt sie ins Maul
            x = max(LIEGT_X + 2, 14 - (f - LANDET))
            katze(bild, x, 8, GEHT[(f // 3) % 2 if x > LIEGT_X + 2 else 0], spiegeln=True)
            kx = x - 2
        elif DREHT <= f < TRAEGT:                                    # dreht sich um: sitzt, Kugel im Maul
            sitzt(bild, LIEGT_X + 4, SITZT, f)
            kx = LIEGT_X + 9
        elif TRAEGT <= f < HAENGT:                                   # trägt sie zum Baum zurück
            x = min(DUCK_X, LIEGT_X + 2 + f - TRAEGT)
            katze(bild, x, 8, GEHT[(f // 3) % 2])
            kx = x + 15
        elif HAENGT <= f < WEG:                                      # hängt sie auf, sitzt unschuldig da
            figur = PFOTE_SCHLAG if f < HAENGT + 2 else PFOTE_HOCH if f < FERTIG else SITZT
            if f in (FERTIG + 5, FERTIG + 6):
                figur = BLINZELT
            sitzt(bild, SITZ_X, figur, f)
        elif f >= WEG:                                               # trollt sich nach links
            katze(bild, round(DUCK_X - (f - WEG) * 0.8), 8, GEHT[(f // 3) % 2], spiegeln=True)

        # die rote Kugel
        if f < FAELLT or f >= HAENGT + 2:                            # hängt (und pendelt)
            p = pendel(f) + versatz(9, dx)
            kugel(bild, HX + p, HY - (abs(p) >= 2))
        elif f < NIMMT:                                              # fällt, hüpft, kullert, liegt
            t = f - FAELLT
            if t < len(FALL):
                x, y = FALL[t]
            else:
                u = min(1.0, (t - len(FALL)) / ROLLT)
                x, y = round(FALL[-1][0] - (FALL[-1][0] - LIEGT_X) * (1 - (1 - u) ** 2)), 13
            kugel(bild, x, y, (HX - x) // 2)
        elif f < HAENGT:                                             # im Maul der Katze
            kugel(bild, kx, 11)
        else:                                                        # die Pfote hebt sie an den Zweig
            kugel(bild, HX, HY + 1)
        liste.append(bild)
    return liste
