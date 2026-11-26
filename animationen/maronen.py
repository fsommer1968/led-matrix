"""Heiße Maronen: Abends auf dem verschneiten Platz steht der Maronenverkäufer (Mütze, Schal, Schürze)
an seinem schwarzen Ofen auf Rädern. Unten pulsiert die Glut, in der Röstpfanne wendet er die
Kastanien mit der Schaufel; einzelne springen mit einem kleinen Hüpfer auf (helle Kerbe), Dampf
steigt auf. Ein Kind kommt, er füllt zwei Schaufeln Maronen in eine spitze Papiertüte und reicht
sie hinüber; das Kind wärmt sich daran die Finger und läuft davon. Zum Schluss schüttet er aus dem
Eimer frische Kastanien nach und wendet weiter – die Runde geht ohne Sprung in sich über, 255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Ofen und Pfanne aus waagerechten Streifen, die Glut im
Zweiertakt der Spalten, einfarbiger Kastanienhaufen, waagerechter Schaufelstiel, wenig Dampf, kein
Schneefall. Gemessen: die erste Laterne kostet rund 7,6 KB, die zweite gleiche nur 1 KB, die
Lichtflecke im Schnee 2,5 KB, ein Stern 1,6 KB, die Radnaben 2,2 KB, der Schnurrbart 1,4 KB.
"""
import math

from basis import B, BLAU, GRUEN, HAUT, NACHTBLAU, PINK, ROT, TUERKIS, WEISS, Bild

NAME = "maronen"
TITEL = "Heiße Maronen"

KANTE = (150, 160, 200)                        # Schnee: Oberkante, darunter gedämpft
BODEN = (78, 90, 140)
OFEN = (38, 38, 48)                            # „schwarz“, aber auf der Matrix noch zu sehen
PFANNE = (130, 130, 150)
RAD = (95, 95, 110)
GLUT = [(140, 0, 0), (230, 40, 0), (255, 110, 0)]                    # drei deutliche Stufen
SCHEIN = [(150, 160, 200), (200, 150, 150), (255, 150, 110)]         # Glut scheint auf den Schnee
KASTANIE = (80, 32, 0)                         # Braun dunkel halten, sonst leuchtet es orange
KERBE = (255, 225, 150)                        # aufgeplatzte Schale
STIEL = (150, 121, 100)                        # blasses Holz
BLATT = (170, 170, 190)
TUETE = (255, 215, 110)                        # Papiertüte
SCHUERZE = (170, 175, 200)
BART = (235, 235, 255)
HOSE = (41, 27, 15)
KINDERHOSE = (0, 40, 170)
AUGE = (50, 25, 10)
EIMER = (100, 105, 125)                       # Blecheimer
EIMERRAND = (170, 175, 200)
DAMPF = [(150, 150, 175), (100, 100, 120), (60, 60, 75), None]             # von frisch bis verweht
MAST = (60, 60, 75)                            # Laterne
LICHT = (255, 190, 60)
STERN = (255, 240, 200)
LICHTFLECK = (255, 215, 130)
LATERNEN = (5, 58)                             # zwei gleiche (die zweite kostet fast nichts)
STERNE = [(50, 3, 30, 85)]                     # x, y, Phase, Periode (teilt 255)

P = 16                                         # Pfanne: linke Kante (16 breit, Rand in Zeile 9)
KUPPEN = "oo.oo.oo.oo.oo"                      # Kastanien: Spalten P+1 bis P+14 in Zeile 8, Kuppen in Zeile 7
RUHE = P + 7                                   # hier ruht das Schaufelblatt
AN_TUETE = P + 13                              # hier kippt die Schaufel in die Tüte
V_X = P + 18                                   # Verkäufer: Mützenschirm, Körper vier Spalten rechts davon
K_X = P + 29                                   # hier bleibt das Kind stehen

# Verkäufer (Blick nach links), 5 breit, Zeilen 1 bis 13: m Mütze, h Gesicht, a Auge, u Schnurrbart,
# s Schal, j Jacke, w Schürze, b Hose
VERKAEUFER = [".mmmm", "mmmmm", ".ahhh", ".uuhh", ".ssss", ".jjjj", ".wwwj", ".wwwj", ".wwwj", ".wwwj",
              ".wwwj", ".bbbb", ".bbbb"]
V_FARBEN = {"m": GRUEN, "h": HAUT, "a": AUGE, "u": BART, "s": ROT, "j": BLAU, "w": SCHUERZE, "b": HOSE}

# Kind (Blick nach links), 3 breit, Zeilen 6 bis 13: w Bommel, m Mütze, j Jacke
K_STEHT = ["..w", "mmm", "mmm", "ahh", "jjj", "jjj", "bbb", "b.b"]
K_GEHT = ["..w", "mmm", "mmm", "ahh", "jjj", "jjj", "bbb", ".b."]
K_FARBEN = {"w": WEISS, "m": PINK, "h": HAUT, "a": AUGE, "j": TUERKIS, "b": KINDERHOSE}

# Ablauf
T_KIND, T_KIND_DA = 46, 84                     # Kind kommt von rechts (halbe Spalte je Bild)
T_TUETE = 60                                   # Tüte in der Hand
T_SCHAUFEL1, T_SCHAUFEL2 = 62, 88              # zwei Schaufeln in die Tüte, je 26 Bilder; dann liegt die Schaufel
T_DREHT, T_REICHT, T_NIMMT = 120, 124, 134     # Übergabe
T_WENDET2 = 142                                # wendet wieder, während das Kind sich die Finger wärmt
T_LAEUFT = 178                                 # Kind dreht sich um und läuft davon
T_WINKT, T_WINKT_BIS = 182, 200                # Verkäufer winkt ihm nach
T_ZURUECK = 202                                # … und steht wieder am Ofen
T_EIMER, T_KIPPT, T_EIMER_AB, T_EIMER_WEG = 204, 214, 230, 236       # frische Kastanien
T_WENDET3 = 235                                # letzter Schaufelzug bis zum Rundenende
SPRUENGE = [(11, P + 2), (16, P + 11), (40, P + 8), (100, P + 4), (128, P + 2), (153, P + 2), (173, P + 5),
            (190, P + 14)]                     # Kastanie springt auf: Bild, Spalte
SPRUNG = [1, 2, 3, 3, 3, 2, 1, 0]


def glut_stufe(f, versatz=0):
    """Glut pulsiert langsam: fünf Atemzüge je Runde, drei Stufen."""
    return round(1 + math.sin(2 * math.pi * (f + versatz) / 51))


def ruehren(p):
    """Schaufelblatt beim Wenden: in 20 Bildern von der Ruhelage fünf Spalten nach links und zurück."""
    return RUHE - (p + 1) // 2 if p < 10 else RUHE - 5 + (p - 9) // 2


def zug(f):
    """Schritt im Schaufelzug (0 bis 19), solange der Verkäufer wendet, sonst None."""
    if f < T_TUETE:
        return f % 20
    if T_WENDET2 <= f < T_WINKT:
        return (f - T_WENDET2) % 20
    return f - T_WENDET3 if f >= T_WENDET3 else None


def schaufel(f):
    """→ (Spalte des Blatts, Zeile des Stiels, angehoben?, beladen?)."""
    if zug(f) is not None:
        return ruehren(zug(f)), 6, False, False
    for start, von in ((T_SCHAUFEL1, P + 7), (T_SCHAUFEL2, P + 10)):
        t = f - start
        if 0 <= t < 26:
            an = 6 + 2 * (AN_TUETE - von)                            # ab hier steht das Blatt an der Tüte
            if t < 4:                                                # schiebt das Blatt unter die Kastanien
                return (von if start == T_SCHAUFEL1 else max(von, P + 12 - t)), 6, False, False
            if t < 6:
                return von, 6, True, True                            # hebt an
            if t < an + 2:
                return min(AN_TUETE, von + (t - 6) // 2), 5, True, True
            if t < an + 6:
                return AN_TUETE, 5, True, False                      # in die Tüte gekippt
            if start == T_SCHAUFEL1:
                return P + 12, 6, False, False
            return max(RUHE, P + 12 - (t - an - 6)), 6, False, False     # zurück in die Ruhelage
    return RUHE, 6, False, False


def fuellung(f):
    """Maronen in der Tüte: 0, 1 oder 2 Schaufeln."""
    return (f >= T_SCHAUFEL1 + 8 + 2 * 6) + (f >= T_SCHAUFEL2 + 8 + 2 * 3)


def kerbe_bis(start, x):
    """Die helle Kerbe einer aufgesprungenen Kastanie bleibt zu sehen, bis sie in die Tüte geschaufelt,
    beim Wenden umgedreht oder von den frischen Kastanien zugedeckt wird."""
    if x in (P + 7, P + 8, P + 10, P + 11):
        return (T_SCHAUFEL1 if x < P + 9 else T_SCHAUFEL2) + 4
    for f in range(start + len(SPRUNG), 255):
        if zug(f) is not None and ruehren(zug(f)) == x:
            return f
    return T_KIPPT + 4


KERBEN = [(start, x, kerbe_bis(start, x)) for start, x in SPRUENGE]


def kuppen(f):
    """Kuppen des Kastanienhaufens (Zeile 7): Spalte → Farbe. Die Schaufeln nehmen vier heraus, der
    Eimer füllt sie wieder auf; aufgesprungene zeigen die helle Kerbe."""
    k = {}
    for i, c in enumerate(KUPPEN):
        x = P + 1 + i
        if c != "o":
            continue
        if x in (P + 7, P + 8) and T_SCHAUFEL1 + 4 <= f < T_KIPPT + 12:
            continue
        if x in (P + 10, P + 11) and T_SCHAUFEL2 + 4 <= f < T_KIPPT + 6:
            continue
        k[x] = KASTANIE
    for start, x, bis in KERBEN:
        if start <= f < start + len(SPRUNG):                         # gerade in der Luft
            k.pop(x, None)
        elif start <= f < bis:
            k[x] = KERBE
    return k


def tuete(bild, x, y, voll):
    """Spitze Papiertüte (3 breit, 4 hoch), oben schauen die Maronen heraus."""
    bild.rechteck(x, y, 3, 2, TUETE)
    bild.rechteck(x + 1, y + 2, 1, 2, TUETE)
    if voll >= 1:
        bild.setze(x + 1, y - 1, KASTANIE)
    if voll >= 2:
        bild.setze(x, y - 1, KERBE)
        bild.setze(x + 2, y - 1, KASTANIE)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # ein Stern, funkelt langsam
            bild.setze(x, y, STERN if (f + phase) % periode < periode * 0.6 else (128, 120, 100))
        bild.rechteck(0, 14, B, 1, KANTE)
        bild.rechteck(0, 15, B, 1, BODEN)
        for x in LATERNEN:                                           # Schneehaube, Licht, Mast, Lichtfleck im Schnee
            bild.rechteck(x - 1, 2, 3, 1, KANTE)
            bild.rechteck(x - 1, 3, 3, 2, LICHT)
            bild.rechteck(x, 5, 1, 9, MAST)
            bild.rechteck(x - 2, 14, 5, 1, LICHTFLECK)

        # Eimer mit frischen Kastanien: kommt hinter der Pfanne hoch, wird gekippt, verschwindet wieder
        eimer_oben = None
        if T_EIMER <= f < T_EIMER_WEG:
            eimer_oben = (max(3, 8 - (f - T_EIMER)) if f < T_KIPPT else 3 if f < T_EIMER_AB
                          else 3 + (f - T_EIMER_AB))
            form = ["rqq.", "rqqq", "rqq."] if T_KIPPT <= f < T_EIMER_AB else ["rrrr", "qqqq", ".qq."]
            bild.figur(P + 11, eimer_oben, form, {"q": EIMER, "r": EIMERRAND})

        # Ofen auf Rädern, Glut pulsiert
        bild.rechteck(P + 2, 10, 12, 4, OFEN)
        for x in range(P + 4, P + 12):
            for y in (11, 12):
                bild.setze(x, y, GLUT[glut_stufe(f, 25 * ((x + y) % 2))])
        for x in (P + 1, P + 12):
            bild.rechteck(x, 11, 3, 3, RAD)
            bild.setze(x + 1, 12, OFEN)
        bild.rechteck(P + 4, 14, 8, 1, SCHEIN[glut_stufe(f)])
        # Pfanne mit Kastanien
        bild.rechteck(P, 9, 16, 1, PFANNE)
        bild.rechteck(P + 1, 8, 14, 1, KASTANIE)
        for x, farbe in kuppen(f).items():
            bild.setze(x, 7, farbe)

        # Schaufel
        bx, zeile, hoch, last = schaufel(f)
        hand = V_X - 1 - (RUHE - bx) // 2                            # beim Wenden geht die Hand mit
        ende = hand - 1 if zug(f) is not None else P + 15
        if hoch:
            bild.rechteck(bx, zeile, 2, 1, BLATT)
            bild.rechteck(bx + 2, zeile, max(0, ende - bx - 1), 1, STIEL)
            if last:
                bild.setze(bx, zeile - 1, KASTANIE)
                bild.setze(bx + 1, zeile - 1, KERBE)
        else:
            bild.rechteck(bx + 1, zeile, ende - bx, 1, STIEL)
            bild.rechteck(bx, zeile, 1, 2, BLATT)
        for start, x in SPRUENGE:                                    # Hüpfer: Kerbe oben, Schale darunter
            if start <= f < start + len(SPRUNG):
                dy = SPRUNG[f - start]
                bild.setze(x, 7 - dy, KERBE)
                if dy:
                    bild.setze(x, 8 - dy, KASTANIE)
        if T_KIPPT <= f < T_EIMER_AB - 3:                            # Kastanien purzeln aus dem Eimer
            bild.setze(P + 10, 4 + f % 4, KASTANIE)
            bild.setze(P + 9, 5 + (f + 2) % 3, KASTANIE)

        # Verkäufer
        if T_DREHT <= f < T_WENDET2 or T_WINKT <= f < T_ZURUECK:     # dem Kind zugewandt
            bild.figur(V_X + 1, 1, VERKAEUFER, V_FARBEN, spiegeln=True)
            if f < T_REICHT:                                         # hält die Tüte vor sich
                bild.setze(V_X + 5, 7, BLAU)
                bild.setze(V_X + 6, 7, HAUT)
                tuete(bild, V_X + 6, 5, 2)
            elif f < T_NIMMT:                                        # reicht sie hinüber
                bild.setze(V_X + 5, 7, BLAU)
                bild.setze(V_X + 6, 8, BLAU)
                bild.setze(V_X + 7, 8, HAUT)
                tuete(bild, V_X + 7, 6, 2)
            elif T_WINKT <= f < T_WINKT_BIS:                         # winkt dem Kind nach
                bild.setze(V_X + 5, 6, BLAU)
                bild.setze(V_X + 6, 5, BLAU)
                bild.setze(V_X + 6 + (f // 3) % 2, 4, HAUT)
        else:
            bild.figur(V_X, 1, VERKAEUFER, V_FARBEN)
            bild.setze(V_X, 6, BLAU)                                 # Arm zur Pfanne
            if zug(f) is not None:                                   # Hand am Schaufelstiel
                bild.rechteck(hand + 1, 6, V_X - hand, 1, BLAU)
                bild.setze(hand, 6, HAUT)
            elif T_TUETE <= f < T_DREHT:                             # Tüte in der Linken am Pfannenrand
                bild.setze(V_X, 7, BLAU)
                bild.setze(V_X - 1, 7, HAUT)
                tuete(bild, V_X - 3, 5 + max(0, 2 - (f - T_TUETE)), fuellung(f))
            elif T_EIMER <= f < T_EIMER_WEG:                         # greift den Eimer
                bild.linie(V_X, 6, V_X - 3, eimer_oben + 1, BLAU)
                bild.setze(V_X - 3, eimer_oben + 1, HAUT)
            else:
                bild.setze(V_X - 1, 7, HAUT)

        # Kind
        if T_KIND <= f < T_KIND_DA:                                  # kommt von rechts
            x = K_X + (T_KIND_DA - f) // 2
            bild.figur(x, 6, K_GEHT if (f // 3) % 2 else K_STEHT, K_FARBEN)
        elif T_KIND_DA <= f < T_LAEUFT:
            freut = T_KIND_DA + 4 <= f < T_DREHT and (f // 4) % 2    # hüpft vor Vorfreude
            bild.figur(K_X, 6 - (1 if freut else 0), K_STEHT, K_FARBEN)
            if T_REICHT + 2 <= f < T_NIMMT:                          # streckt die Hand aus
                bild.setze(K_X - 1, 10, TUERKIS)
                bild.setze(K_X - 2, 10, HAUT)
            elif f >= T_NIMMT:                                       # wärmt sich die Finger an der Tüte
                hebt = 1 if (f - T_NIMMT) % 20 >= 12 else 0
                tuete(bild, K_X - 3, 8 - hebt, 2)
                bild.setze(K_X - 3, 10 - hebt, HAUT)
                bild.setze(K_X - 1, 10 - hebt, HAUT)
                if (f // 4) % 2:                                     # die Tüte dampft
                    bild.setze(K_X - 2, 5 - hebt, DAMPF[2])
        elif f >= T_LAEUFT:                                          # dreht sich um und läuft davon
            x = K_X + max(0, f - T_LAEUFT - 3)
            if x < B:
                bild.figur(x, 6, K_GEHT if (f // 2) % 2 else K_STEHT, K_FARBEN, spiegeln=True)
                tuete(bild, x + 3, 8, 2)
                bild.setze(x + 3, 10, HAUT)

        # Dampf über der Pfanne (nur vor dem Nachthimmel): drei Fahnen, je zwei Punkte
        for k, x0 in enumerate((P + 3, P + 12, P + 6)):
            t = (f - k * 17) % 51
            if t < 24:
                y = 5 - t // 4
                x = x0 + (1 if (t // 4) % 3 == 1 else 0)
                for dy in (0, -1):                                   # unten heller, verblasst nach oben
                    if bild.hole(x, y + dy) == NACHTBLAU:
                        bild.setze(x, y + dy, DAMPF[t // 8 - dy])
        liste.append(bild)
    return liste
