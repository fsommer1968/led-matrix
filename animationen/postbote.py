"""Der Postbote bringt Weihnachtspost: verschneite Straße, links ein Lattenzaun mit rotem Briefkasten,
rechts das Haus mit grüner Tür und hellem Fenster. Der Postbote (gelbe Jacke, blaue Mütze, große
Tasche) zieht seinen gelben Paketwagen heran, auf dem ein Turm aus drei Paketen schwankt. Am
Briefkasten stopft er Brief um Brief hinein, bis die Umschläge oben herausquellen; der letzte springt
heraus und fällt in den Schnee. Dann zieht er weiter vor die Tür und wuchtet die Pakete über den Kopf
zu einem Stapel: Karton, rotes Geschenk, obenauf das kleine blaue. Der Stapel wackelt, das kleine
rutscht herunter, er fängt es auf, stellt es daneben ab, wischt sich die Stirn und zieht mit dem
leeren Wagen rechts aus dem Bild. Die Tür geht auf: Die Mutter holt den Stapel herein, das Kind rennt
zum Briefkasten, hüpft nach den Briefen, hebt den aus dem Schnee auf und nimmt auf dem Rückweg das
kleine Paket mit. Die Tür geht zu, der Briefkasten ist wieder leer, eine Sternschnuppe fällt. Die
Runde schließt ohne Sprung – 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ein Zaun im festen Vierertakt, Haus, Dach, Tür und
Wagen aus Rechtecken (gleiche Nachbarspalten), die Klappe am Briefkasten über die ganze Breite und
ein Glasfeld statt eines Türknaufs (ein einzelner Punkt in einer Fläche kostet 14 Bytes je Bild),
zwei Sterne (Perioden 51 und 85 teilen 255), kein Schneefall. Wer ins Haus geht, verschwindet hinter
der Wand rechts vom Türrahmen. Keine Logos, keine Schrift.
"""
from basis import B, GELB, GOLD, HAUT, HELLBLAU, LILA, NACHTBLAU, PINK, WEISS, Bild, dimmen, sternschnuppe

NAME = "postbote"
TITEL = "Der Postbote bringt Weihnachtspost"

KANTE = (215, 225, 250)                        # Schneekante am Boden und auf dem Dach
BODEN = (78, 90, 140)                          # darunter gedämpft (große Fläche)
STERN = (255, 240, 200)
STERNE = [(4, 1, 0, 51), (29, 2, 20, 85)]      # x, y, Phase, Periode
ZAUN = (66, 27, 0)
HAUBE = (105, 118, 165)                        # Schnee auf den Latten: matt, sonst wirkt er wie Lichter
WAND = (62, 64, 80)                            # Hauswand: gedämpftes Grau, davor leuchten Gelb und Pakete
DACH = (120, 28, 22)
TUER = (0, 80, 30)
LICHT = (191, 142, 45)                         # warmes Licht in der offenen Tür (Fenstergelb, gedämpft)
SCHEIN = (255, 210, 120)                       # … und sein Schein auf dem Schnee davor
FENSTER = (255, 190, 60)
KASTEN = (230, 0, 0)
SCHLITZ = (110, 0, 0)
JACKE = GELB
TASCHE = (255, 120, 0)
MUETZE = (0, 70, 255)
HOSE = (0, 40, 150)
AUGE = (50, 25, 10)
WAGEN = (255, 180, 0)
RAD = (120, 120, 140)
SPEICHE = (200, 200, 215)
KARTON = (150, 62, 0)
SIEGEL = (255, 0, 40)
GESCHENK = (230, 0, 0)

BODEN_Y = 13                                   # Zeile der Schneekante; alle stehen darauf
ZAUN_BIS = 34                                  # Zaun von 0 bis hier, Latten zwei breit im Vierertakt
KASTEN_X, KASTEN_Y = 18, 6                     # Briefkasten 5×4, sitzt auf zwei Latten des Zauns
HAUS_X = 36
TUER_X, TUER_B, TUER_Y = 50, 6, 5              # Tür: Spalten 50 bis 55, Zeilen 5 bis 12
FENSTER_X = 58

# Postbote von der Seite (Blick nach rechts), 6 breit, 10 hoch: m Mütze, h Gesicht, a Auge,
# j Jacke, t Tasche, b Hose
KOPF = ["..mmm.", "..mmmm", "..hha.", "..hhh."]
RUMPF = ["..jjj.", "tttjj.", "tttjj.", "tttjj."]
BEINE = [["..b.b.", "..b.b."], ["..bbb.", "...b.."]]
FARBEN = {"m": MUETZE, "h": HAUT, "a": AUGE, "j": JACKE, "t": TASCHE, "b": HOSE}
OBEN = BODEN_Y - 10                            # oberste Zeile der Mütze

# Pakete: Karton mit Adressfeld, rotes Geschenk mit Goldband, kleines blaues
PAKETE = [(["kkkkk", "kwwkk", "kkkkk"], {"k": KARTON, "w": (230, 215, 190)}),
          (["rrgrr", "rrgrr", "rrgrr"], {"r": GESCHENK, "g": GELB}),
          (["hwh", "hwh"], {"h": HELLBLAU, "w": WEISS})]
AUF_WAGEN = [(1, 1), (1, 4), (2, 7)]           # Turm auf dem Wagen: (dx, Zeile)
VOR_TUER = [(45, 10), (45, 7), (46, 5)]        # Stapel links neben der Tür

# Haufen auf dem Briefkasten je Stufe (Zeilen 3 bis 5, Spalten 18 bis 22): w weiß, b blau, g gold
HAUFEN = [[],
          [".....", ".....", ".w..."],
          [".....", ".....", ".ww.."],
          [".....", "...b.", ".wwb."],
          [".....", ".w.b.", "wwwbb"],
          ["..g..", ".wgb.", "wwwbb"],
          [".wg.b", ".wgbb", "wwwbb"]]
HAUFEN_FARBEN = {"w": WEISS, "b": HELLBLAU, "g": GOLD}
UMSCHLAG = [["wrw", "www"], ["ww", "rw", "ww"]]            # der eine, der herausspringt (rotes Siegel)
FALL = [(21, 2, 0), (22, 0, 1), (23, 1, 0), (23, 3, 1), (23, 6, 0), (23, 8, 1), (23, 10, 0)]   # x, y, Lage
LIEGT = (23, 11)                               # dort bleibt er im Schnee liegen

# Kind (Bommel kommt extra dazu) und Mutter, Blick nach rechts: m Mütze, o Haar, j Jacke, l Pullover
KIND = ["mmm", "hha", "jjj", "jjj", "jjj"]
KIND_BEINE = [["b.b", "b.b"], ["bbb", ".b."]]
KIND_FARBEN = {"m": PINK, "h": HAUT, "a": AUGE, "j": (60, 255, 60), "b": (0, 60, 255)}
MUTTER = ["ooo", "hha", "hhh", "lll", "lll", "lll", "b.b", "b.b"]
MUTTER_FARBEN = {"o": (70, 28, 0), "h": HAUT, "a": AUGE, "l": LILA, "b": (0, 60, 255)}

# ── Ablauf ─────────────────────────────────────────────────────────
X1, X2 = 11, 35                                # linke Kante des Postboten: am Briefkasten, vor der Tür
T_HALT1 = 18                                   # steht am Briefkasten
BRIEF = 7                                      # Bilder je Brief, sechs Briefe
T_STOPFT = T_HALT1 + 1                         # 19
T_FAELLT = T_STOPFT + 5 * BRIEF + 4            # 58: der letzte Umschlag springt heraus
T_WEITER = T_STOPFT + 6 * BRIEF + 2            # 63: zieht weiter
T_HALT2 = T_WEITER + (X2 - X1)                 # 87: steht vor der Tür
HEBEN = 12                                     # Bilder je Paket
T_LAEDT = T_HALT2 + 1                          # 88
T_WACKELT = T_LAEDT + 3 * HEBEN                # 124
LEHNT = [0, 1, 1, 0, -1, -1, 0, 1, 2, 2, 1, 0, -1, -2]            # so weit neigt sich der Stapel (Spalten)
T_RUTSCHT = T_WACKELT + len(LEHNT)             # 138
# das kleine Paket rutscht ab, er fängt es (federt nach), hält es und stellt es bei (41, 11) ab
RUTSCHT = [(43, 5), (42, 6), (41, 8), (41, 9), (41, 8), (41, 8), (41, 8), (41, 10), (41, 11)]
T_FORT = T_RUTSCHT + 16                        # 154: zieht ab
T_TUER = T_FORT + 22                           # 176: die Tür geht auf (drei Bilder), der Wagen rollt noch vorbei
T_MUTTER = T_TUER + 3                          # 179
MUTTER_X = [55, 54, 53, 52, 51, 50, 50, 50, 50, 51, 52, 54, 56]
T_KIND = T_MUTTER + len(MUTTER_X)              # 192
KIND_HIN = 14                                  # Bilder bis zum Briefkasten (zwei Spalten je Bild)
KIND_X = 26                                    # dort steht es am Briefkasten
T_ZU = T_KIND + 45                             # 237: die Tür geht zu
T_SCHNUPPE = 243                               # Sternschnuppe über dem Zaun (bis 250)


def postbote(bild, x0, schritt=0, links=False):
    """Postbote mit linker Kante x0 (Tasche hinten); links = schaut nach links, der Rumpf bleibt stehen."""
    bild.figur(x0 + (1 if links else 0), OBEN, KOPF + RUMPF + BEINE[schritt], FARBEN, spiegeln=links)


def arm(bild, x0, hx, hy, laenge=4):
    """Arm von der Schulter in Richtung (hx, hy), höchstens laenge Pixel lang, vorn die Hand.
    Liegt das Ziel über dem Kopf, streckt er beide Arme neben dem Gesicht hoch."""
    if hy <= OBEN and abs(hx - (x0 + 3)) <= 3:
        for ax in (x0 + 1, x0 + 5):
            bild.rechteck(ax, hy + 1, 1, OBEN + 4 - hy, JACKE)
            bild.setze(ax, hy, HAUT)
        return
    sx, sy = x0 + (2 if hx < x0 + 3 else 4), OBEN + 4
    n = max(abs(hx - sx), abs(hy - sy), 1)
    k = min(n, laenge)
    ex, ey = round(sx + (hx - sx) * k / n), round(sy + (hy - sy) * k / n)
    bild.linie(sx, sy, ex, ey, JACKE)
    bild.setze(ex, ey, HAUT)


def paket(bild, nr, x, y):
    zeilen, farben = PAKETE[nr]
    bild.figur(x, y, zeilen, farben)


def wagen(bild, cx, f, rollt, turm):
    """Gelber Handwagen 7 breit mit Deichsel; turm = Nummern der Pakete, die noch darauf liegen."""
    bild.rechteck(cx, 9, 7, 2, WAGEN)
    bild.setze(cx, 8, WAGEN)
    bild.setze(cx + 6, 8, WAGEN)
    bild.rechteck(cx + 7, 9, 2, 1, RAD)                              # Deichsel
    for rx in (cx, cx + 5):
        bild.rechteck(rx, 11, 2, 2, RAD)
        dreh = (f // 2) % 2 if rollt else 0
        bild.setze(rx + dreh, 11 + dreh, SPEICHE)
    for nr in turm:
        dx, y = AUF_WAGEN[nr]
        if rollt and nr == turm[0]:                                  # das oberste Paket schwankt beim Rollen
            dx += (0, 1, 0, -1)[(f // 3) % 4]
        paket(bild, nr, cx + dx, y)


def bezier(a, b, c, t):
    return (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t * t * b


def kulisse(bild, f, stufe, tuer):
    for x, y, phase, periode in STERNE:                              # wenige Sterne, funkeln langsam
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    sternschnuppe(bild, f, T_SCHNUPPE, 17, 0, laenge=8)              # zum Schluss, wenn alles im Haus ist
    for x in range(ZAUN_BIS + 1):                                    # Lattenzaun mit Schneehäubchen
        bild.setze(x, 10, ZAUN)
        if x % 4 >= 2:
            bild.rechteck(x, 9, 1, 4, ZAUN)
            bild.setze(x, 8, HAUBE)
    bild.rechteck(KASTEN_X, KASTEN_Y, 5, 4, KASTEN)                  # Briefkasten
    bild.rechteck(KASTEN_X, KASTEN_Y + 1, 5, 1, SCHLITZ)           # Klappe: über die ganze Breite (billig)
    if stufe:
        bild.figur(KASTEN_X, KASTEN_Y - 3, HAUFEN[stufe], HAUFEN_FARBEN)
    bild.rechteck(HAUS_X, 4, B - HAUS_X, 9, WAND)                    # Haus
    bild.rechteck(HAUS_X - 1, 1, B - HAUS_X + 1, 1, KANTE)
    bild.rechteck(HAUS_X - 1, 2, B - HAUS_X + 1, 1, BODEN)
    bild.rechteck(HAUS_X - 1, 3, B - HAUS_X + 1, 1, DACH)
    bild.rechteck(FENSTER_X, 6, 5, 4, FENSTER)
    bild.rechteck(FENSTER_X + 2, 6, 1, 4, WAND)
    bild.rechteck(TUER_X, TUER_Y, TUER_B, 8, TUER)                   # Tür mit Glasfeld oben (kein Knauf: teuer)
    bild.rechteck(TUER_X, TUER_Y, TUER_B, 2, FENSTER)
    if tuer:                                                         # offen: Licht, das Türblatt links
        breit = (0, 2, 4, 5)[tuer]
        bild.rechteck(TUER_X + TUER_B - breit, TUER_Y, breit, 8, LICHT)
    bild.rechteck(0, BODEN_Y, B, 1, KANTE)
    bild.rechteck(0, BODEN_Y + 1, B, 2, BODEN)
    if tuer == 3:
        bild.rechteck(TUER_X + 1, BODEN_Y, TUER_B - 1, 1, SCHEIN)


def bewohner(bild, x, y, zeilen, farben, links=False):
    """Kind oder Mutter; rechts vom Türrahmen verdeckt sie die Hauswand (sie sind dann im Haus)."""
    for dy, zeile in enumerate(zeilen):
        for dx, c in enumerate(zeile):
            px = x + (len(zeile) - 1 - dx if links else dx)
            if c != "." and px < TUER_X + TUER_B:
                bild.setze(px, y + dy, farben[c])


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        # ── Zustand ──
        if f < T_STOPFT:
            stufe = 0
        elif f < T_WEITER:
            u = f - T_STOPFT
            stufe = min(6, u // BRIEF + (1 if u % BRIEF >= 4 else 0))
        else:
            stufe = 6
        c = f - T_KIND                                               # Kind
        if c >= KIND_HIN + 3:
            stufe = 3
        if c >= KIND_HIN + 7:
            stufe = 0
        liegt = T_FAELLT + len(FALL) <= f and c < KIND_HIN + 10
        tuer = 0
        if T_TUER <= f < T_ZU + 3:
            tuer = min(3, f - T_TUER + 1, T_ZU + 3 - f)
        kulisse(bild, f, stufe, tuer)
        if liegt:
            bild.figur(LIEGT[0], LIEGT[1], UMSCHLAG[0], {"w": WEISS, "r": SIEGEL})

        # ── Pakete vor der Tür ──
        v = f - T_LAEDT
        a = f - T_MUTTER
        lehne = LEHNT[f - T_WACKELT] if T_WACKELT <= f < T_RUTSCHT else (-1 if f == T_RUTSCHT else 0)
        hub = 1 if a >= 7 else 0                                     # die Mutter hebt den Stapel an
        if a < 8:
            for nr in (0, 1):
                if v >= nr * HEBEN + 9:
                    x, y = VOR_TUER[nr]
                    paket(bild, nr, x + ((lehne > 0) - (lehne < 0) if nr == 1 else 0), y - hub)
        s = f - T_RUTSCHT
        klein = None                                                 # wo das kleine Paket gerade ist
        if 2 * HEBEN + 9 <= v and s < 0:
            klein = (VOR_TUER[2][0] + lehne, VOR_TUER[2][1])
        elif 0 <= s and c < 33:
            klein = RUTSCHT[min(s, len(RUTSCHT) - 1)]

        # ── Mutter und Kind ──
        if 0 <= a < len(MUTTER_X):
            x = MUTTER_X[a]
            bewohner(bild, x, 5, MUTTER, MUTTER_FARBEN, links=a < 8)
            if a == 6:
                bild.setze(49, 8, HAUT)
            if a >= 8:                                               # trägt den Stapel vor sich her
                for nr in (0, 1):
                    zeilen, farben = PAKETE[nr]
                    bewohner(bild, x - 1, VOR_TUER[nr][1] - 1, zeilen, farben)
        if klein and c < 33:
            paket(bild, 2, klein[0], klein[1])
        if 0 <= c < 45:
            traegt_post = c >= KIND_HIN + 3
            if c <= KIND_HIN:                                        # rennt zum Briefkasten
                x, links, y = 54 - 2 * c, True, 0
            elif c < KIND_HIN + 9:                                   # hüpft zweimal nach den Briefen
                x, links, y = KIND_X, True, (0, -1, -2, -1)[(c - KIND_HIN - 1) % 4]
            elif c < KIND_HIN + 12:                                  # bückt sich nach dem Umschlag
                x, links, y = KIND_X, True, 0
            elif c < 32:                                             # zurück bis zum kleinen Paket
                x, links, y = min(37, KIND_X + 2 * (c - KIND_HIN - 11)), False, 0
            elif c < 35:
                x, links, y = 37, False, 0
            else:                                                    # mit Paket ins Haus
                x, links, y = 37 + 2 * (c - 34), False, 0
            rennt = c <= KIND_HIN or KIND_HIN + 12 <= c < 31 or c >= 35
            beine = KIND_BEINE[c % 2 if rennt else 0]
            bewohner(bild, x, 6 + y, KIND + beine, KIND_FARBEN, links=links)
            bild.setze(x + 1, 5 + y, WEISS if x + 1 < TUER_X + TUER_B else None)    # Bommel
            if KIND_HIN < c < KIND_HIN + 9 and y < 0:                # Arm nach oben zum Haufen
                bild.setze(x - 1, 7 + y, KIND_FARBEN["j"])
                bild.setze(x - 2, 6 + y, HAUT)
            if KIND_HIN + 9 <= c < KIND_HIN + 11:                    # Arm hinunter zum Umschlag
                bild.setze(x - 1, 10, KIND_FARBEN["j"])
                bild.setze(x - 1, 11, HAUT)
            if traegt_post:                                          # Briefe (und Paket) vor der Brust
                vorn = x - 1 if links else x + 2
                if c >= 33:
                    bewohner(bild, x + 1, 9, PAKETE[2][0], PAKETE[2][1])
                    bewohner(bild, x + 2, 8, ["ww"], {"w": WEISS})
                else:
                    bewohner(bild, vorn, 8 + y, ["ww", "ww"], {"w": WEISS})

        # ── Postbote und Wagen ──
        if f < T_FORT + 40:
            if f <= T_HALT1:
                x0, geht = f - 7, f < T_HALT1
            elif f < T_WEITER:
                x0, geht = X1, False
            elif f <= T_HALT2:
                x0, geht = X1 + f - T_WEITER, f < T_HALT2
            elif f < T_FORT:
                x0, geht = X2, False
            else:
                x0, geht = X2 + f - T_FORT, True
            turm = [nr for nr in (0, 1, 2) if v < nr * HEBEN + 1]
            wagen(bild, x0 - 9, f, geht, turm)
            links = 0 <= v < 3 * HEBEN and v % HEBEN < 5
            postbote(bild, x0, (f // 3) % 2 if geht else 0, links)
            # Briefe stopfen
            if T_STOPFT <= f < T_STOPFT + 6 * BRIEF:
                u = f - T_STOPFT
                n, k = u // BRIEF, u % BRIEF
                farbe = (WEISS, WEISS, HELLBLAU, WEISS, GOLD, WEISS)[n]
                if k == 0:
                    bild.rechteck(x0 + 2, OBEN + 4, 2, 1, farbe)
                elif k == 1:
                    arm(bild, x0, x0 + 4, OBEN + 4)
                    bild.rechteck(x0 + 5, OBEN + 4, 2, 1, farbe)
                elif k == 2:
                    arm(bild, x0, x0 + 5, OBEN + 3)
                    bild.rechteck(x0 + 6, OBEN + 3, 2, 1, farbe)
                elif k == 3:
                    arm(bild, x0, x0 + 6, OBEN + 3)
                    bild.rechteck(x0 + 7, OBEN + 2, 2, 1, farbe)
                elif k == 4:
                    arm(bild, x0, x0 + 6, OBEN + 2 if n == 5 else OBEN + 3)
                elif k == 5:
                    arm(bild, x0, x0 + 5, OBEN + 4)
            # Pakete über den Kopf zur Tür heben
            if 0 <= v < 3 * HEBEN:
                nr, k = v // HEBEN, v % HEBEN
                sx, sy = x0 - 9 + AUF_WAGEN[nr][0], AUF_WAGEN[nr][1]
                ex, ey = VOR_TUER[nr]
                breit = len(PAKETE[nr][0][0])
                hoch = len(PAKETE[nr][0])
                if 1 <= k < 9:
                    t = k / 9
                    px = round(sx + (ex - sx) * t)
                    py = max(0, round(bezier(sy, ey, -10, t)))
                    paket(bild, nr, px, py)
                    arm(bild, x0, px + breit // 2, py + hoch)
                elif k == 0:
                    arm(bild, x0 - 1, sx + breit, sy + hoch - 1)
                elif k == 9:
                    arm(bild, x0, ex - 1, ey)
            # der Stapel wackelt: Hände hoch, wenn er sich weit neigt
            if T_WACKELT <= f < T_RUTSCHT and abs(lehne) == 2:
                arm(bild, x0, x0 + 6, OBEN + 3)
            if 0 <= s < 16:
                if s < 2:
                    arm(bild, x0, x0 + 6, OBEN + 4)
                elif s < 9:                                          # fängt das Paket und stellt es ab
                    arm(bild, x0, klein[0] - 1, klein[1] + 1, laenge=5)
                elif 10 <= s < 15:                                   # wischt sich die Stirn
                    arm(bild, x0, x0 + 5, OBEN + 2)

        # ── der Umschlag springt aus dem Briefkasten ──
        j = f - T_FAELLT
        if 0 <= j < len(FALL):
            x, y, lage = FALL[j]
            bild.figur(x, y, UMSCHLAG[lage], {"w": WEISS, "r": SIEGEL})
        liste.append(bild)
    return liste
