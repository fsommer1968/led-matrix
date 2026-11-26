"""Strohsterne basteln: Am Fenster (draußen Nacht, ein paar Flocken) liegt goldgelbes Stroh auf
dem Tisch, rechts steht eine flache rote Schachtel. Zwei Hände legen die Halme über Kreuz – erst
ein Halm (zwei Strahlen), dann ein zweiter quer darüber (vier), dann ein gekreuztes Paar schräg
dazu (acht) – und wickeln in der Mitte roten Faden darum. Der fertige Strohstern blitzt auf,
schwebt ans Fenster, hängt sich an einen roten Faden, dreht sich langsam und glänzt (ein Lichtpunkt
wandert über die Strahlen). So entstehen nacheinander drei Sterne verschiedener Größe. Am Ende
klappt der Deckel der Schachtel auf, eine Hand nimmt die Sterne ab und legt sie hinein, der Deckel
klappt zu – dann liegt wieder nur das lose Stroh auf dem Tisch. 255 Bilder, kein Text. Die Runde
schließt ohne Sprung: Sie beginnt und endet mit dem leeren Fenster, die Flocken fallen in ganzen
Durchläufen je Runde.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ein Fenster mit nur einer Sprosse (alle Glasspalten
gleich), Arme als senkrechte Streifen aus drei gleichen Spalten, spiegelgleiche Sterne, Stroh und
Bindefaden waagerecht oder senkrecht, fünf Flocken ohne Seitwärtsbewegung.
"""
import math

from basis import B, GELB, GOLD, HAUT, ROT, Bild

NAME = "strohsterne"
TITEL = "Strohsterne basteln"

NACHT = (0, 5, 34)                             # Fensterglas: Nacht draußen
# Fensterrahmen (gedämpft). Genau dieser Ton: speichern() ändert bei zwei gleichen Nachbarbildern
# das Blau des Pixels oben links um 1; hier bleibt die 16-Bit-Farbe der Matrix dabei dieselbe.
RAHMEN = (84, 76, 67)
TISCH, TISCH_VORN = (82, 36, 6), (41, 15, 0)   # Holz dunkel, sonst leuchtet es orange
STROH, STROH_SCHRAEG = GELB, GOLD              # gerade Halme goldgelb, das schräge Paar etwas dunkler
GLANZ = (255, 255, 210)
FADEN = ROT                                    # Bindefaden
HAENGER = (170, 0, 0)                          # Faden, an dem der Stern hängt
AERMEL, BUND = (0, 120, 40), (210, 210, 230)
SCHACHTEL, DECKEL = (150, 0, 20), (255, 70, 70)
FLOCKE = (170, 180, 215)

SPROSSE_X = 29                                 # Sprosse zwischen den beiden Fensterflügeln
TISCH_Y = 13                                   # Tischkante; Glas in den Zeilen 1–12
WX, WY = 14, 7                                 # Bastelplatz: hier entsteht der Stern
GRIFF_X, GRIFF_Y = 2, 11                       # hier greift die linke Hand ins Stroh
SX, SB, SY = 53, 11, 9                         # Schachtel: linke Kante, Breite, Zeile des Deckels
SMX = SX + SB // 2                             # Mitte der Schachtel
AUF_AB, ZU_AB = 198, 248                       # der Deckel klappt auf und wieder zu (je vier Bilder)

# Sterne in der Reihenfolge des Bastelns: Strahlenlänge gerade/schräg, Platz am Fenster (Mitte),
# Beginn des Bastelns, Bilder fürs Schweben ans Fenster, Beginn des Abnehmens, Bilder fürs Tragen
# zur Schachtel, halbe Drehungen am Faden (er hängt genau so lange, dass er zum Abnehmen wieder
# von vorn zu sehen ist)
STERNE = [(3, 2, 48, 6, 3, 14, 204, 4, 3),
          (4, 3, 36, 7, 65, 12, 216, 7, 2),
          (2, 2, 24, 6, 127, 9, 231, 10, 1)]
ABHEBEN = 51                                   # so viele Bilder nach Beginn schwebt der Stern los
RING = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]   # Faden läuft um die Mitte
STRAHLEN = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]   # im Uhrzeigersinn

# Flocken: Spalte, Startzeile, Durchläufe je Runde (ganzzahlig: schließt ohne Sprung)
FLOCKEN = [(3, 2.0, 6), (20, 15.0, 5), (31, 9.5, 5), (43, 5.0, 7), (59, 13.0, 6)]
FALLHOEHE = 17


def weich(a):
    """Sanft anfahren und abbremsen (0 … 1)."""
    a = max(0.0, min(1.0, a))
    return a * a * (3 - 2 * a)


def hand(bild, x, y, greift=None):
    """Hand von unten: 3×3 Haut, Bündchen, Ärmel bis zum unteren Bildrand. greift = "r", "l" oder
    "o": Daumen und Zeigefinger stehen nach rechts, links oder oben vor, dazwischen sitzt der Halm."""
    bild.rechteck(x, y, 3, 3, HAUT)
    bild.rechteck(x, y + 3, 3, 1, BUND)
    bild.rechteck(x, y + 4, 3, 16, AERMEL)
    if greift in ("r", "l"):
        for dy in (0, 2):
            bild.setze(x + (3 if greift == "r" else -1), y + dy, HAUT)
    elif greift == "o":
        for dx in (0, 2):
            bild.setze(x + dx, y - 1, HAUT)


def glanzweg(r, d):
    """Weg des Lichtpunkts: von einer Strahlspitze quer über die Mitte zur gegenüberliegenden,
    dann von der Nachbarspitze wieder zurück – so wandert er reihum über alle acht Strahlen."""
    weg, i = [], 0
    for _ in range(8):
        lang = d if i % 2 else r
        weg += [(STRAHLEN[i][0] * k, STRAHLEN[i][1] * k) for k in range(lang, -lang - 1, -1)]
        i = (i + 5) % 8
    return weg


def stern(bild, cx, cy, r, d, laengs=True, hoch=True, schraeg=True, knoten=True, s=1.0,
          glanz=None, blitz=False, y_max=99):
    """Strohstern um (cx, cy): gerade Strahlen der Länge r, schräge der Länge d; s staucht die
    Breite (Drehung um den Faden), glanz = Punkt (dx, dy) mit dem Lichtpunkt."""
    punkte = {}
    if schraeg:
        for k in range(1, d + 1):
            for vx in (-1, 1):
                for vy in (-1, 1):
                    punkte[(vx * k, vy * k)] = STROH_SCHRAEG
    if laengs:
        for k in range(-r, r + 1):
            punkte[(k, 0)] = STROH
    if hoch:
        for k in range(-r, r + 1):
            punkte[(0, k)] = STROH
    if blitz:
        punkte = {p: GLANZ for p in punkte}
    if glanz is not None:
        punkte[glanz] = GLANZ
    if knoten:
        punkte[(0, 0)] = FADEN
    # Drehung: die Spitzen rücken zur Mitte (gerade Strahlen auf breit, schräge auf schmal Spalten),
    # die Punkte dazwischen folgen ihrer Spitze – so bleibt jeder Strahl eine saubere Linie
    breit = int(abs(s) * r + 0.5)
    schmal = int(abs(s) * d + 0.5)
    seite = 1 if s >= 0 else -1
    rang = {STROH_SCHRAEG: 0, STROH: 1, GLANZ: 2, FADEN: 3}
    fertig = {}
    for (dx, dy), farbe in punkte.items():
        weit = abs(dx) * schmal / d if dy else abs(dx) * breit / r
        ziel = (math.ceil(weit - 0.5) * (1 if dx > 0 else -1) * seite, dy)
        if ziel not in fertig or rang[farbe] > rang[fertig[ziel]]:
            fertig[ziel] = farbe
    for (dx, dy), farbe in fertig.items():
        if cy + dy <= y_max:
            bild.setze(cx + dx, cy + dy, farbe)


def schachtel(bild, f):
    """Flache Schachtel rechts auf dem Tisch. Der Deckel (rechts angeschlagen) klappt vor dem
    Abnehmen hoch und steht dann am Fensterrahmen; zum Schluss klappt er wieder zu."""
    stufe = 0
    if AUF_AB <= f < ZU_AB:
        stufe = min(3, 1 + (f - AUF_AB) // 2)
    elif ZU_AB <= f < ZU_AB + 4:
        stufe = 2 - (f - ZU_AB) // 2
    bild.rechteck(SX, SY + 1, SB, TISCH_Y - SY - 1, SCHACHTEL)
    if stufe == 0:
        bild.rechteck(SX, SY, SB, 1, DECKEL)
    elif stufe == 1:
        bild.linie(B - 1, SY - 1, SX + 1, SY - 5, DECKEL)
    elif stufe == 2:
        bild.linie(B - 1, SY - 1, B - 5, SY - 8, DECKEL)
    else:
        bild.rechteck(B - 1, SY - 7, 1, 7, DECKEL)


def basteln(bild, u, r, d):
    """Stern am Bastelplatz mit beiden Händen; u = Bilder seit Beginn."""
    lx, ly = WX - r - 3, WY - 1                                     # linke Hand hält den ersten Halm links
    if 9 <= u < ABHEBEN:
        stern(bild, WX, WY, r, d, hoch=u >= 16, schraeg=u >= 29, knoten=u >= 41, blitz=u in (49, 50))
    # linke Hand: greift ins Stroh, hebt einen Halm an den Bastelplatz und hält ihn
    if u < 3:
        hand(bild, GRIFF_X, (14, 12, GRIFF_Y)[u], "r")
    elif u < 9:
        a = (u - 2) / 6
        x, y = round(GRIFF_X + (lx - GRIFF_X) * a), round(GRIFF_Y + (ly - GRIFF_Y) * a)
        bild.rechteck(x + 3, y + 1, 2 * r + 1, 1, STROH)
        hand(bild, x, y, "r")
    elif u < 49:
        hand(bild, lx, ly, "r")
    else:
        hand(bild, lx, ly + (u - 48) * 3)
    # rechte Hand: zweiter Halm von unten, dann das schräge Paar, dann der Faden
    if 10 <= u <= 17:
        ab = max(0, 16 - u) * 2
        if ab:
            bild.rechteck(WX, WY - r + ab, 1, 2 * r + 1, STROH)
        hand(bild, WX - 1, WY + r + 1 + ab, "o")
    elif 18 <= u <= 20:
        hand(bild, WX - 1, WY + r + 1 + (u - 17) * 3)
    elif 22 <= u <= 30:
        ab = max(0, 29 - u)
        if ab:
            stern(bild, WX + ab, WY + ab, r, d, laengs=False, hoch=False, knoten=False)
        hand(bild, WX + d - 1 + ab, WY + d + 1 + ab, "o")
    elif 31 <= u <= 33:
        hand(bild, WX + d - 1, WY + d + 1 + (u - 30) * 3)
    elif 34 <= u <= 36:
        hand(bild, WX + r + 1, WY - 1 + (36 - u) * 3, "l")
    elif 37 <= u <= 47:                                             # wickelt den roten Faden um die Mitte
        dx, dy = RING[(u - 37) % 8]
        hand(bild, WX + r + 1, WY - 1 + dy, "l")
        bild.rechteck(WX + dx, WY + dy, r + 1 - dx, 1, FADEN)
    elif u == 48:
        hand(bild, WX + r + 1, WY - 1, "l")
    elif u >= 49:
        hand(bild, WX + r + 1, WY - 1 + (u - 48) * 3)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHT)
        bild.rechteck(0, 0, B, 1, RAHMEN)                            # Fensterrahmen oben und an den Seiten
        bild.rechteck(0, 0, 1, TISCH_Y, RAHMEN)
        bild.rechteck(B - 1, 0, 1, TISCH_Y, RAHMEN)
        bild.rechteck(SPROSSE_X, 0, 1, TISCH_Y, RAHMEN)
        bild.rechteck(0, TISCH_Y, B, 1, TISCH)
        bild.rechteck(0, TISCH_Y + 1, B, 2, TISCH_VORN)
        for x, phase, runden in FLOCKEN:                             # draußen fallen ein paar Flocken
            y = (phase + f * runden * FALLHOEHE / 255) % FALLHOEHE
            if y < TISCH_Y - 1:
                bild.setze(x, 1 + int(y), FLOCKE)
        bild.rechteck(1, 12, 8, 1, STROH)                            # loses Stroh auf dem Tisch
        bild.rechteck(3, 11, 5, 1, STROH_SCHRAEG)
        haende = []
        for r, d, hx, hy, beginn, schweben, ab, tragen, drehungen in STERNE:
            u = f - beginn - ABHEBEN                                 # Bilder seit dem Abheben
            g = f - ab                                               # Bilder seit Beginn des Abnehmens
            if u < 0:                                                # liegt noch als Stroh da oder wird gebastelt
                continue
            if u < schweben:                                         # schwebt ans Fenster
                a = weich((u + 1) / (schweben + 1))
                stern(bild, round(WX + (hx - WX) * a), round(WY + (hy - WY) * a), r, d)
            elif g < 3:                                              # hängt, dreht sich und glänzt
                t = u - schweben                                     # Bilder, seit er hängt
                dauer = ab + 2 - beginn - ABHEBEN - schweben         # … bis die Hand ihn greift
                s = math.cos(math.pi * drehungen * t / dauer)
                lang = min(hy - r - 1, t + 1)                        # der Faden wächst vom Stern zum Rahmen
                bild.rechteck(hx, hy - r - lang, 1, lang, HAENGER)
                weg = glanzweg(r, d)
                stern(bild, hx, hy, r, d, s=s, glanz=weg[(t // 2) % len(weg)])
                if g >= 0:                                           # Hand kommt, um ihn abzunehmen
                    haende.append((hx - r - 3, hy - 1 + (2 - g) * 3))
            else:
                oben = SY - r                                        # Mitte, wenn er über der Schachtel schwebt
                if g < 3 + tragen:                                   # wird zur Schachtel getragen
                    a = weich((g - 2) / tragen)
                    x, y = round(hx + (SMX - hx) * a), round(hy + (oben - hy) * a)
                else:                                                # sinkt in die Schachtel
                    x, y = SMX, oben + (g - 2 - tragen) * 2 + max(0, g - 5 - tragen)
                if y - r <= 12:
                    stern(bild, x, y, r, d, y_max=12)
                    haende.append((x - r - 3, y - 1))
        schachtel(bild, f)                                           # verdeckt, was hineinsinkt
        for r, d, hx, hy, beginn, schweben, ab, tragen, drehungen in STERNE:
            if 0 <= f - beginn < 53:
                basteln(bild, f - beginn, r, d)
        for x, y in haende:
            hand(bild, x, y, "r")
        liste.append(bild)
    return liste
