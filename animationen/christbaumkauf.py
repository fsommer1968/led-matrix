"""Christbaumkauf: Christbaummarkt am Abend – drei verschneite Tannen lehnen am Zaun, darüber eine
bunte Lichterkette, daneben der Netztrichter. Ein kleines rotes Auto rollt von links heran, Kind,
Vater und Mutter steigen aus und gehen an den Bäumen entlang; das Kind zeigt auf den letzten und
hüpft, der Vater schüttelt ihn (der Schnee rieselt herunter). Die Mutter geht zum Auto zurück, das
Kind schaut zu, wie der Vater den Baum durch den Trichter zieht (er kommt schmal und eingenetzt
heraus), ihn aufs Autodach stemmt und festzurrt. Das Auto fährt nach rechts davon, die
Abgaswölkchen bleiben kurz stehen; ein neuer Baum rückt an den Zaun, und die Runde beginnt von
vorn – 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum einfarbiger Himmel mit nur drei Sternen, Zaun, Tannen und
Lichterkette im selben Achtertakt und spiegelgleich (die zweite und dritte Tanne sind Kopien der
ersten), Lichterkette nur über dem Stand und je Bild nur zwei Farben, rechts davon glatter Grund,
Trichter und Figuren aus gleichen Nachbarspalten, kein Schneefall.
"""
from basis import GELB, HAUT, NACHTBLAU, PINK, ROT, WEISS, B, Bild, dimmen

NAME = "christbaumkauf"
TITEL = "Christbaumkauf"

KANTE = (215, 225, 250)                        # Oberkante des Schnees (Zeile 14), Schnee auf den Tannen
BODEN = (78, 90, 140)                          # darunter gedämpft
ZAUN = (66, 30, 4)
TANNE = (0, 95, 35)                            # Tannen am Zaun (gedämpft)
TANNE_VORN = (0, 180, 50)                      # der ausgesuchte Baum, sobald ihn jemand anfasst
STAMM = (66, 30, 4)
NETZ = (150, 235, 170)                         # eingenetzter Baum: blasses Grün …
MASCHE = WEISS                                 # … mit weißen Ringen
STAHL = (120, 125, 150)                        # Netztrichter
DRAHT = (30, 30, 40)                           # Lichterkette
KETTE = [ROT, GELB, (0, 200, 0), (0, 90, 255), PINK]
AUTO = (215, 0, 0)
FENSTER = (30, 50, 100)
RAD = (90, 90, 100)
SCHEINWERFER = (255, 230, 120)
GURT = GELB
HOSE = (45, 45, 80)
AUGE = (50, 25, 10)
LICHTKEGEL = (200, 170, 70)                    # Scheinwerferlicht auf dem Schnee
ABGAS = [(200, 200, 215), (120, 120, 140), (60, 60, 75)]
STERN = (255, 240, 200)
# x, y, Phase, Periode – nur drei, über Trichter und Parkplatz (dort sind die Spalten ohnehin nicht glatt)
STERNE = [(33, 1, 0, 51), (51, 2, 30, 51), (60, 0, 20, 85)]

V_FARBEN = {"m": (255, 120, 0), "h": HAUT, "a": AUGE, "j": (0, 110, 255), "b": HOSE}
M_FARBEN = {"m": WEISS, "h": HAUT, "a": AUGE, "j": PINK, "b": HOSE}
K_FARBEN = {"m": GELB, "h": HAUT, "a": AUGE, "j": (0, 220, 220), "b": HOSE}
BAUM_FARBEN = {"t": TANNE, "s": STAMM, "w": KANTE}
VORN_FARBEN = {"t": TANNE_VORN, "s": STAMM, "w": MASCHE, "p": NETZ}

FUSS = 13                                      # unterste Zeile der Figuren, darunter der Schnee
TAKT = 8                                       # Zaunpfosten, Tannen und Lichterkette im Achtertakt
BAEUME = 3
STAND_BIS = BAEUME * TAKT                      # letzter Pfosten
DRAHT_HOCH = [0, 0, 1, 1, 1, 1, 1, 0]          # die Kette hängt zwischen den Pfosten durch
LICHTER = (0, 2, 4, 6)
PFOSTEN_OBEN, MAST_OBEN = 7, 2                 # Zaunpfosten; die beiden Masten am Rand tragen die Kette

# Tanne, 7 breit, Zeilen 5 bis 13 (spiegelgleich: jede Spalte kommt zweimal vor); w Schnee
BAUM = ["...w...",
        "...t...",
        "..wtw..",
        "..ttt..",
        ".wtttw.",
        ".ttttt.",
        "wtttttw",
        "ttttttt",
        "ttttttt"]
SCHNEE_AB = [(c, r) for r, zeile in enumerate(BAUM) for c, z in enumerate(zeile) if z == "w"]
# kippt dem Vater in die Hand (Stamm unten rechts)
KIPPT = ["tt......",
         "tttt....",
         ".ttttt..",
         "..ttttt.",
         "..tttttt",
         "...ttttt",
         "....ttts"]
# liegend (Spitze links, Stamm rechts an der Hand)
LIEGT = ["......ttt.",
         "....ttttt.",
         "ttttttttts",
         "....ttttt.",
         "......ttt."]
# eingenetzt: schmal und länger, zwei Zeilen
NETZBAUM = [".ppwppwpp.",
            "pppwppwpps"]
# Netztrichter: weiter Ring links, Netzrolle rechts, auf einem Fuß; Zeilen 8 bis 13
TRICHTER = ["ss....",
            "ssssww",
            "ssssww",
            "ssssww",
            "..ss..",
            "..ss.."]
TRICHTER_X = 28
FREI_X = TRICHTER_X + 6                        # ab hier kommt der Baum eingenetzt heraus
# Auto (fährt nach rechts), Zeilen 8 bis 13
WAGEN = ["....rrrrrrr...",
         "...rfffrfffr..",
         ".rrrrrrrrrrrr.",
         "rrrrrrrrrrrrrl",
         "rroorrrrrroorr",
         "..oo......oo.."]
PARK = 48
START = -19                                    # so weit links, dass auch der Lichtkegel noch draußen ist
KOEPFE = {"k": 5, "v": 8, "m": 10}             # Spalte im Fenster (die Mutter fährt)

VATER = ["mmm", "hha", "jjj", "jjj", "jjj", "jjj", "bbb"]
MUTTER = ["mmm", "hha", "jjj", "jjj", "jjj", "jjj"]
KIND = ["mmm", "hha", "jjj", "jjj"]
BEINE = ["bb.", ".bb"]                         # immer zwei gleiche Spalten

# ── Ablauf ─────────────────────────────────────────────────────────
RUNDE = 255
AN = 26                                        # Auto steht
K_RAUS, K_DA = 28, 58                          # Kind läuft voraus und zeigt
V_RAUS, V_DA = 32, 74
M_RAUS, M_DA = 36, 71
SCHUETTELN, KIPPEN, ZIEHEN = 80, 98, 100
K_LOS, K_SCHAUT = 98, 126                      # Kind läuft zum Auto und schaut von dort zu
M_LOS, M_DUCKT, M_DRIN = 107, 142, 145
AM_NETZ, DURCH = 123, 150                      # Vater zieht den Baum zum Trichter und hindurch
OBEN, DRUEBEN, AUF_DACH = 158, 170, 172        # über den Kopf, übers Dach, abgelegt
K_EIN, K_HINTEN, K_DRIN = 173, 176, 181
GURT1, GURT2 = 175, 179
V_GEHT, V_DUCKT, V_DRIN = 182, 189, 190       # hinter Auto und Baum ist er gleich verdeckt
LICHT = 192
ABFAHRT = 195
WEG = ABFAHRT + 19
NEU, NEU_DA = 224, 236                         # der nächste Baum rückt an den Zaun

V_X, K_X, M_X = 8, 13, 19                      # Plätze am Baum
K_AUTO, V_AUTO, M_AUTO = 52, 54, 57            # hinter dem Auto (dort steigen sie ein und aus)
K_VORN = 49                                    # hier schaut das Kind zu
V_NETZ, V_ENDE = TRICHTER_X + 1, 44


def zwischen(s, s0, s1, x0, x1):
    return x0 + (x1 - x0) * (s - s0) / (s1 - s0)


def auto_x(s):
    if s < AN:                                 # rollt aus
        return round(START + (PARK - START) * (1 - (1 - s / AN) ** 1.4))
    if s < ABFAHRT:
        return PARK
    return PARK + round(0.05 * (s - ABFAHRT) ** 2)


def figur(bild, x, zeilen, farben, links=False, schritt=None, dy=0):
    """Person, drei Spalten breit, Füße auf Zeile FUSS; schritt None = steht. Mit dy > 0 taucht
    sie hinter dem Auto ab (dann ohne die Zeile unter dem Wagenboden)."""
    alle = zeilen + ["bbb" if schritt is None else BEINE[schritt]]
    y0 = FUSS + 1 - len(alle) + dy
    for r, zeile in enumerate(alle):
        if y0 + r > FUSS - (1 if dy > 0 else 0):
            break
        for c, z in enumerate(zeile):
            if z != ".":
                bild.setze(x + (2 - c if links else c), y0 + r, farben[z])


def sprite(bild, x0, y0, zeilen, farben, von=-99, bis=99):
    for r, zeile in enumerate(zeilen):
        for c, z in enumerate(zeile):
            if z != "." and von <= x0 + c <= bis:
                bild.setze(x0 + c, y0 + r, farben[z])


def kulisse(bild, s):
    for x, y, phase, periode in STERNE:        # funkeln langsam
        bild.setze(x, y, dimmen(STERN, 1.0 if (s + phase) % periode < periode * 0.6 else 0.5))
    bild.rechteck(0, 14, B, 1, KANTE)
    bild.rechteck(0, 15, B, 1, BODEN)
    # Zaun mit zwei Masten, dazwischen die Lichterkette
    bild.rechteck(0, 8, STAND_BIS + 1, 1, ZAUN)
    bild.rechteck(0, 11, STAND_BIS + 1, 1, ZAUN)                     # untere Latte: nur in der Lücke zu sehen
    for x in range(0, STAND_BIS + 1, TAKT):
        oben = MAST_OBEN if x in (0, STAND_BIS) else PFOSTEN_OBEN
        bild.rechteck(x, oben, 1, FUSS + 1 - oben, ZAUN)
    # je Bild nur zwei Farben im Wechsel; alle 1,7 s tauschen sie, alle 5,1 s rückt eine neue nach
    z = s // 17
    paar = [KETTE[z // 3 % 5], KETTE[(z // 3 + 1) % 5]]
    if z % 3 == 1:
        paar.reverse()
    for x in range(STAND_BIS + 1):
        hoch = DRAHT_HOCH[x % TAKT]
        bild.setze(x, hoch, DRAHT)
        if x % TAKT in LICHTER:
            bild.setze(x, hoch + 1, paar[LICHTER.index(x % TAKT) % 2])


def bilder():
    liste = []
    for s in range(RUNDE):
        bild = Bild(NACHTBLAU)
        kulisse(bild, s)
        for k in range(1, BAEUME):
            sprite(bild, 1 + k * TAKT, 5, BAUM, BAUM_FARBEN)
        # der Baum ganz links: steht, wird geschüttelt, kippt, ist weg, der nächste rückt nach
        if s < SCHUETTELN or s >= NEU_DA:
            sprite(bild, 1, 5, BAUM, BAUM_FARBEN)
        elif s < KIPPEN:                       # nach zwei Rucken ist der Schnee ab
            sprite(bild, 1 + [0, 1, 0, -1][(s // 2) % 4], 5, BAUM,
                   {**VORN_FARBEN, "w": KANTE if s < SCHUETTELN + 2 else TANNE_VORN})
        elif s < ZIEHEN:
            sprite(bild, 0, 7, KIPPT, VORN_FARBEN)
        elif s >= NEU:
            sprite(bild, round(zwischen(s, NEU, NEU_DA, -7, 1)), 5, BAUM, BAUM_FARBEN)

        # ── wo ist wer ──
        ax = auto_x(s)
        hinten, vorn = [], []                  # Figuren hinter und vor dem Auto

        def stelle(x, zeilen, farben, links, geht, dy=0, takt=3, nach=None):
            schritt = (s // takt) % 2 if geht else None
            x = round(x)
            (nach if nach is not None else hinten if x >= PARK - 2 else vorn).append(
                (x, zeilen, farben, links, schritt, dy))

        # Kind
        jubel = None                           # x des Kindes, wenn es im Hüpfer die Arme hochreißt
        if K_RAUS <= s < K_DA:
            stelle(zwischen(s, K_RAUS, K_DA, K_AUTO, K_X), KIND, K_FARBEN, True, True, takt=2)
        elif K_DA <= s < K_LOS:
            hupf = -1 if s >= K_DA + 4 and (s // 3) % 2 else 0
            stelle(K_X, KIND, K_FARBEN, True, False, dy=hupf)
            if s >= SCHUETTELN and hupf:       # jubelt beim Schütteln
                jubel = K_X
        elif K_LOS <= s < K_SCHAUT:
            stelle(zwischen(s, K_LOS, K_SCHAUT, K_X, K_VORN), KIND, K_FARBEN, False, True, takt=2, nach=vorn)
        elif K_SCHAUT <= s < K_EIN:            # hüpft vor dem Auto, immer zwei Hüpfer, dann Pause
            hupf = -1 if (s // 3) % 2 and (s // 12) % 2 else 0
            stelle(K_VORN, KIND, K_FARBEN, s < OBEN, False, dy=hupf, nach=vorn)
            if hupf:
                jubel = K_VORN
        elif K_EIN <= s < K_HINTEN:            # läuft ums Heck
            stelle(zwischen(s, K_EIN, K_HINTEN, K_VORN, PARK - 3), KIND, K_FARBEN, True, True, takt=2, nach=vorn)
        elif K_HINTEN <= s < K_DRIN:
            stelle(zwischen(s, K_HINTEN, K_DRIN, PARK - 3, K_AUTO), KIND, K_FARBEN, False, True, takt=2, nach=hinten)
        # Mutter
        if M_RAUS - 3 <= s < M_RAUS:
            stelle(M_AUTO, MUTTER, M_FARBEN, True, False, dy=M_RAUS - s)
        elif M_RAUS <= s < M_DA:
            stelle(zwischen(s, M_RAUS, M_DA, M_AUTO, M_X), MUTTER, M_FARBEN, True, True)
        elif M_DA <= s < M_LOS:
            stelle(M_X, MUTTER, M_FARBEN, True, False)
        elif M_LOS <= s < M_DUCKT:
            stelle(zwischen(s, M_LOS, M_DUCKT, M_X, M_AUTO), MUTTER, M_FARBEN, False, True)
        elif M_DUCKT <= s < M_DRIN:
            stelle(M_AUTO, MUTTER, M_FARBEN, False, False, dy=s - M_DUCKT + 1)
        # Vater
        vx = None
        if V_RAUS - 3 <= s < V_RAUS:
            stelle(V_AUTO, VATER, V_FARBEN, True, False, dy=V_RAUS - s)
        elif V_RAUS <= s < V_DA:
            stelle(zwischen(s, V_RAUS, V_DA, V_AUTO, V_X), VATER, V_FARBEN, True, True)
        elif V_DA <= s < ZIEHEN:
            stelle(V_X, VATER, V_FARBEN, True, False)
        elif ZIEHEN <= s < DURCH:
            if s < AM_NETZ:
                vx = round(zwischen(s, ZIEHEN, AM_NETZ, V_X, V_NETZ))
            else:
                vx = round(zwischen(s, AM_NETZ, DURCH, V_NETZ, V_ENDE))
            stelle(vx, VATER, V_FARBEN, vx >= FREI_X, True, nach=vorn)
        elif DURCH <= s < V_GEHT:
            stelle(V_ENDE, VATER, V_FARBEN, s < OBEN, False, nach=vorn)
        elif V_GEHT <= s < V_DUCKT:
            stelle(zwischen(s, V_GEHT, V_DUCKT, V_ENDE, V_AUTO), VATER, V_FARBEN, False, True)
        elif V_DUCKT <= s < V_DRIN:
            stelle(V_AUTO, VATER, V_FARBEN, False, False, dy=s - V_DUCKT + 1)

        for p in hinten:
            figur(bild, *p)
        # ── Auto ──
        if s < WEG:
            licht = s < AN + 2 or s >= LICHT
            sprite(bild, ax, 8, WAGEN, {"r": AUTO, "f": FENSTER, "o": RAD, "l": SCHEINWERFER if licht else AUTO})
            if licht:                          # Lichtkegel auf dem Schnee
                bild.rechteck(ax + 14, 14, 5, 1, LICHTKEGEL)
            drin = {"k": s < K_RAUS or s >= K_DRIN, "v": s < V_RAUS - 3 or s >= V_DRIN,
                    "m": s < M_RAUS - 3 or s >= M_DRIN}
            for wer, spalte in KOEPFE.items():
                if drin[wer]:
                    bild.setze(ax + spalte, 9, HAUT)
            if s >= AUF_DACH:
                sprite(bild, ax + 2, 6, NETZBAUM, VORN_FARBEN)
                if s >= GURT1:
                    bild.rechteck(ax + 9, 6, 1, 2, GURT)
                if s >= GURT2:
                    bild.rechteck(ax + 4, 6, 1, 2, GURT)
        # ── der Baum unterwegs ──
        if ZIEHEN <= s < DURCH:                # gezogen: vor dem Trichter breit, dahinter im Netz
            hoch = 8 if vx >= V_NETZ - 3 else 9                      # zum Trichter hin angehoben
            sprite(bild, vx - 10, hoch, LIEGT, VORN_FARBEN, bis=TRICHTER_X - 1)
            sprite(bild, vx - 10, 10, NETZBAUM, VORN_FARBEN, von=FREI_X)
        elif DURCH <= s < OBEN:                # hochgestemmt
            sprite(bild, V_ENDE - 10, round(zwischen(s, DURCH, OBEN, 10, 4)), NETZBAUM, VORN_FARBEN)
        elif OBEN <= s < DRUEBEN:              # über den Kopf aufs Dach geschoben
            sprite(bild, round(zwischen(s, OBEN, DRUEBEN, V_ENDE - 10, PARK + 2)), 4, NETZBAUM, VORN_FARBEN)
        elif DRUEBEN <= s < AUF_DACH:
            sprite(bild, PARK + 2, 5, NETZBAUM, VORN_FARBEN)
        sprite(bild, TRICHTER_X, 8, TRICHTER, {"s": STAHL, "w": WEISS})
        for p in vorn:
            figur(bild, *p)
        # Kind zeigt auf den Baum, Vater packt ihn
        if K_DA <= s < SCHUETTELN:
            bild.rechteck(K_X - 2, 11 - (1 if s >= K_DA + 4 and (s // 3) % 2 else 0), 2, 1, K_FARBEN["j"])
        if jubel is not None:
            bild.setze(jubel - 1, 9, K_FARBEN["j"])
            bild.setze(jubel + 3, 9, K_FARBEN["j"])
        if SCHUETTELN <= s < KIPPEN:
            bild.setze(V_X - 1, 9, V_FARBEN["j"])
        elif DURCH <= s < OBEN:                # stemmt: der Arm geht mit dem Baum hoch
            bild.setze(V_ENDE - 1, round(zwischen(s, DURCH, OBEN, 10, 4)) + 1, V_FARBEN["j"])
        elif OBEN <= s < GURT2 + 2:            # schiebt und zurrt mit erhobenem Arm
            bild.rechteck(V_ENDE + 3, 6, 1, 3, V_FARBEN["j"])
        for k, (c, r) in enumerate(reversed(SCHNEE_AB)):             # der Schnee rieselt, unten zuerst
            y = 5 + r + (s - SCHUETTELN - 2 - k) * 2 // 3
            if s >= SCHUETTELN + 2 + k and y <= FUSS:
                bild.setze(1 + c, y, KANTE)
        # Abgaswölkchen bleiben stehen
        for start, x in [(ABFAHRT - 3, PARK - 3), (ABFAHRT + 4, PARK - 2), (ABFAHRT + 9, PARK + 1)]:
            stufe = (s - start) // 6           # steigt und verblasst in drei Stufen
            if s >= start and stufe < 3:
                bild.rechteck(x, 11 - stufe, 2, 2 if stufe < 2 else 1, ABGAS[stufe])
        liste.append(bild)
    return liste
