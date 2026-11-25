"""Zur Christmette: Heilige Nacht im verschneiten Dorf. Rechts die kleine Kirche, der Turm mit dem
Portal steht vorn, im Langhaus leuchten drei bunte Glasfenster (rot, blau, gold). Von links stapfen
kleine Gestalten mit Laternen einzeln und in Grüppchen durch den Schnee und verschwinden in der
hell erleuchteten Tür. Im Turm schwingt die Glocke, ein großer Stern steht über allem, es schneit
sacht. Es kommen immer neue Leute nach, darum geht die Runde ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ein flacher Boden, Langhaus und Dach aus Rechtecken
(gleiche Nachbarspalten), drei gleich gebaute Fenster ohne Spitzbogen (der kostete 7 KB),
Gestalten als Blöcke mit drei fast gleichen Spalten (ein Gesicht im Profil kostete 4 KB), sechs
Flocken und keine kleinen Sterne (jeder kostete 2 KB). Das Glimmen der Fenster, der Tür, der
Glockenstube und der Laternen ändert nur Farben und kostet darum keinen Speicher. Alle Takte
teilen 255.
"""
from basis import GELB, GOLD, NACHTBLAU, WEISS, Bild, dimmen

NAME = "christmette"
TITEL = "Zur Christmette"

RUNDE = 255
KANTE = (215, 225, 250)                        # Oberkante der Schneedecke
BODEN = (78, 90, 140)                          # darunter gedämpft
BODEN_Y = 14
DACHSCHNEE = (150, 160, 205)
DACH = (44, 36, 84)
MAUER = (74, 64, 100)
SCHALL = (14, 6, 0)                            # Glockenstube im Turm
SCHALL_HELL = (80, 26, 0)                      # … glimmt beim Anschlag
BRONZE = (255, 140, 0)
TUER = (255, 190, 60)
TUER_HELL = (255, 235, 150)                    # wenn gerade jemand eintritt
ROT_GLAS = (255, 20, 0)
BLAU_GLAS = (0, 70, 255)
GOLD_GLAS = (255, 170, 0)
STERNGELB = (255, 225, 110)
LATERNE = (255, 190, 40)
BUEGEL = (150, 80, 0)                          # Bügel und Dach der Laterne
SCHEIN = (255, 170, 60)                        # Schein von Laterne und Tür auf dem Schnee
HAUT = (255, 170, 110)
STIEFEL = (110, 70, 40)
FLOCKE = (140, 150, 190)

# ── Kirche: Turm (Spalten 41 … 47) mit Portal, Langhaus (48 … 63) ──
TURM_X = 41
TURM = ["...g...",
        "...s...",
        "..sds..",
        ".sddds.",
        "sddddds",
        "twwwwwt",
        "twwwwwt",
        "twwwwwt",
        "ttttttt",
        "tttlttt",
        "ttllltt",
        "ttllltt",
        "ttllltt",
        "ttllltt"]
TUER_X = TURM_X + 2                            # linke Spalte der Tür (drei breit)
# Glocke in der Glockenstube (5 breit, 3 hoch): Mitte, nach links, nach rechts; b Glocke, k Klöppel
GLOCKE = {0: ["..b..", ".bbb.", ".bkb."],
          -1: ["..b..", ".bb..", "bbbk."],
          1: ["..b..", "..bb.", ".kbbb"]}
SCHWUNG = 17                                   # Bilder je Hin und Her
HAUS_X = 48
FENSTER = [(49, ROT_GLAS, 0), (54, BLAU_GLAS, 17), (59, GOLD_GLAS, 34)]     # x, Farbe, Phase des Glimmens
GLIMMEN = 51                                   # Bilder je Auf und Ab der Fenster

SX, SY = 21, 3                                 # Mitte des großen Sterns
FUNKELN = 51                                   # Bilder je Aufleuchten

# ── Leute (Blick nach rechts): m Mütze, h Gesicht, j Mantel, b Stiefel ──
# Schritt: Beine auseinander, Beine zusammen (alle drei Spalten bleiben fast gleich)
GROSS = [["mmm", "hhh", "jjj", "jjj", "b.b"],
         ["mmm", "hhh", "jjj", "jjj", "bbb"]]
KLEIN = [["mmm", "hhh", "jjj", "b.b"],
         ["mmm", "hhh", "jjj", "bbb"]]
TEMPO = 2                                      # Bilder je Pixel
START_X = -4
# Start im Umlauf, Vorlage, Mütze, Mantel, Laterne (ja/nein): einer allein, ein Paar,
# Eltern mit Kind, Großmutter mit Enkel. In einem Grüppchen liegen die Starts zehn Bilder (fünf
# Pixel) auseinander; die Grüppchen starten abwechselnd gerade und ungerade, damit sich in jedem
# Bild etwas bewegt.
LEUTE = [(0, GROSS, (255, 0, 0), (0, 150, 60), True),
         (61, GROSS, (0, 200, 255), (200, 40, 255), True),
         (71, GROSS, (255, 210, 0), (0, 90, 255), False),
         (124, GROSS, (255, 0, 160), (0, 160, 160), False),
         (134, KLEIN, (255, 210, 0), (255, 60, 0), True),
         (144, GROSS, (0, 220, 120), (170, 30, 40), True),
         (201, GROSS, (255, 120, 0), (60, 80, 255), True),
         (211, KLEIN, (0, 200, 255), (255, 0, 120), True)]
EINTRITT = (TUER_X - START_X) * TEMPO          # nach so vielen Bildern steht die Gestalt in der Tür
IN_DER_TUER = 4                                # so lange ist sie dort noch als Schatten zu sehen

# Flocken: Spalte, Fallstufen je 15 Bilder (17 Zeilen Umlauf: schließt nach 255 Bildern), Phase
# (über dem Kirchendach kosten sie wenig, weil sie dahinter verschwinden)
FLOCKEN = [(4, 3, 0), (12, 4, 7), (30, 3, 12), (37, 4, 3), (55, 3, 9), (61, 4, 5)]


def kirche(bild, f, tritt_ein):
    """Langhaus (Schnee auf dem Dach, Dach, Mauer, Glasfenster) und davor der Turm mit Glocke und Tür."""
    bild.rechteck(HAUS_X, 6, 16, 1, DACHSCHNEE)
    bild.rechteck(HAUS_X, 7, 16, 1, DACH)
    bild.rechteck(HAUS_X, 8, 16, 6, MAUER)
    for x, farbe, phase in FENSTER:                                  # hohe Glasfenster glimmen langsam
        p = (f + phase) % GLIMMEN
        hell = 1.0 if p < 22 else 0.7 if 27 <= p < 46 else 0.85
        bild.rechteck(x, 9, 3, 4, dimmen(farbe, hell))
    p = f % SCHWUNG                                                  # Glocke: links, Mitte, rechts, Mitte
    lage = -1 if p < 5 else 0 if p < 8 else 1 if p < 13 else 0
    schlag = p < 2 or 8 <= p < 10                                    # Anschlag: die Stube glimmt auf
    farben = {"g": GOLD, "s": KANTE, "d": DACH, "t": MAUER, "w": SCHALL_HELL if schlag else SCHALL,
              "l": TUER_HELL if tritt_ein else TUER}
    bild.figur(TURM_X, 0, TURM, farben)
    bild.figur(TURM_X + 1, 5, GLOCKE[lage], {"b": BRONZE, "k": GELB})


def grosser_stern(bild, f):
    """Großer Stern: heller Kern, vier gleiche Strahlen (links und rechts je zwei gleiche Spalten) und
    gedämpfte Schrägen; alle 51 Bilder leuchtet er auf – die Schrägen werden hell, dann wachsen
    oben und unten Spitzen."""
    p = f % FUNKELN
    stufe = 2 if 33 <= p < 43 else 1 if 27 <= p < 49 else 0
    for k in (1, 2):
        for dx, dy in ((k, 0), (-k, 0), (0, k), (0, -k)):
            bild.setze(SX + dx, SY + dy, STERNGELB)
    for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        bild.setze(SX + dx, SY + dy, dimmen(STERNGELB, 0.75 if stufe else 0.4))
    if stufe == 2:
        bild.setze(SX, SY - 3, dimmen(STERNGELB, 0.4))
        bild.setze(SX, SY + 3, dimmen(STERNGELB, 0.4))
    bild.setze(SX, SY, WEISS)


def leute(bild, zeiten):
    for (start, vorlage, muetze, mantel, laterne), t in zip(LEUTE, zeiten):
        if t >= EINTRITT + IN_DER_TUER:
            continue                                                 # in der Kirche oder noch nicht unterwegs
        x = START_X + min(t, EINTRITT) // TEMPO
        farben = {"m": muetze, "h": HAUT, "j": mantel, "b": STIEFEL}
        if t >= EINTRITT:                                            # in der Tür: nur noch ein Schatten
            farben = {k: dimmen(v, 0.4) for k, v in farben.items()}
        zeilen = vorlage[(t // 4) % 2 if t < EINTRITT else 1]
        bild.figur(x, BODEN_Y - len(zeilen), zeilen, farben)
        if laterne and x + 3 < TUER_X + 3:                           # Laterne in der Hand: schwankt sanft
            hell = 1.0 if (t // 5) % 3 else 0.7                      # … und flackert
            y = BODEN_Y - len(zeilen) + 3 - (t // 8) % 2             # Kinder tragen sie tiefer
            bild.setze(x + 3, y - 1, BUEGEL)
            bild.setze(x + 3, y, dimmen(LATERNE, hell))
            if x + 3 < TUER_X:
                bild.setze(x + 3, BODEN_Y, dimmen(SCHEIN, hell))     # ihr Schein auf dem Schnee


def _bild(f):
    bild = Bild(NACHTBLAU)
    grosser_stern(bild, f)
    for x, stufen, phase in FLOCKEN:                                 # sachter Schneefall vor dem Himmel
        y = (phase + f * stufen // 15) % 17 - 1
        x += 1 if (f + 3 * phase) % 51 < 26 else 0                   # treibt ein wenig hin und her
        if bild.hole(x, y) == NACHTBLAU and y < BODEN_Y:
            bild.setze(x, y, FLOCKE)
    bild.rechteck(0, BODEN_Y, 64, 1, KANTE)
    bild.rechteck(0, BODEN_Y + 1, 64, 1, BODEN)
    zeiten = [(f - start) % RUNDE for start, *_ in LEUTE]
    tritt_ein = any(EINTRITT - 2 <= t < EINTRITT + IN_DER_TUER + 2 for t in zeiten)
    kirche(bild, f, tritt_ein)
    bild.rechteck(TUER_X, BODEN_Y, 3, 1, SCHEIN)                     # Lichtschein vor der Tür
    leute(bild, zeiten)
    return bild


def bilder():
    return [_bild(f) for f in range(RUNDE)]
