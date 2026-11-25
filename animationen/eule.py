"""Schneeeule: Winternacht mit großem Vollmond, davor ein kahler, verschneiter Baum, dessen langer
Ast bis vor den Mond reicht, darunter die verschneite Ebene. Eine Schneeeule kommt mit langsamen,
großen Flügelschlägen von links, gleitet mit ruhigen Flügeln vor dem Mond vorbei, landet auf dem
Ast (der Ast wippt, Schnee rieselt), faltet die Flügel, dreht den Kopf nach links und rechts,
zwinkert und fliegt nach rechts wieder ab. Anfang und Ende zeigen dieselbe leere Nacht, die Runde
geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum waagerechte Äste (gleiche Nachbarspalten), Flügel in
Stufen aus je zwei gleichen Spalten, vier Krater in Zweierspalten, drei Sterne (ihre Perioden
teilen 255), kein Schneefall. Der Mond ist gedämpft gelb, damit die weiße Eule davor lesbar bleibt.
"""
import math

from basis import B, NACHTBLAU, WEISS, Bild, dimmen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "eule"
TITEL = "Schneeeule gleitet durch die Winternacht"

MOND = (205, 155, 35)                          # gedämpftes Gelb: die Eule davor bleibt weiß lesbar
KRATER = (165, 118, 25)
STERN = (255, 240, 200)
STERNE = [(5, 2, 0, 85), (36, 0, 30, 51), (61, 3, 60, 85)]            # x, y, Phase, Periode (teilt 255)
KANTE = (215, 225, 250)                        # Oberkante der Schneedecke
EBENE = (78, 90, 140)                          # darunter gedämpft
HOLZ = (33, 19, 8)
AST_SCHNEE = (150, 165, 220)                   # Schnee auf den Ästen: gedämpfter als die Eule
SCHATTEN = (150, 160, 205)                     # Unterseite der Flügel, angelegte Flügel
TUPFEN = (85, 88, 110)
AUGE = (255, 200, 0)
LID = TUPFEN                                   # Auge zu: dunkler Strich
SCHNABEL = (255, 110, 0)

MOND_X, MOND_Y, MOND_R = 20, 6, 6.5
KRATER_FLECKEN = [(17, 2, 2, 2), (22, 5, 2, 1), (16, 8, 2, 1), (20, 9, 2, 2)]   # x, y, Breite, Höhe
AST_Y = 10                                     # Schnee auf dem Ast; das Holz eine Zeile darunter
AST_VON, AST_KNICK, STAMM_X = 22, 33, 54      # Astspitze, Knick, Stamm
X_AST = 41                                     # hier sitzt die Eule (Mitte)
X_START, X_ENDE = -12, 76                      # Mitte der Eule außerhalb des Bildes
SCHLAG = 20                                    # Bilder je Flügelschlag
GLEITEN = (0.4, 1.0, 1.0, 0.4)                 # Hub der vier Flügelstufen im Gleiten: leicht gewölbt

ANFLUG, LANDET, SITZT, STARTET, ABFLUG, WEG = 4, 82, 100, 196, 206, 250   # Bildnummern im Ablauf
GLEITET = 43                                   # Mitte des Gleitens: die Eule ist vor dem Mond

# Kopf (7 breit, Blick nach vorn / halb links / links): w weiß, Y Auge, k Schnabel
KOPF = {
    "vorn": ["..www..", ".wwwww.", ".wYwYw.", ".wwkww."],
    "halb": ["..www..", ".wwwww.", ".YwYww.", ".wkwww."],
    "seite": ["..www..", ".wwwww.", ".wYwww.", "kwwwww."],
}
# Rumpf im Sitzen: f angelegte Flügel, t Tupfen
RUMPF = ["fwwwwwf", "ftwwwtf", "fwwtwwf", "ftwwwtf", ".wwwww."]
FALTEN = [(8, 4), (8, 2), (8, 0), (7, -2), (6, -4), (5, -6), (4, -7), (3, -8), (2, -8)]   # Länge, Spitze

# Im Sitzen: (Dauer, Kopf, nach rechts?, linkes Auge auf, rechtes Auge auf); zusammen STARTET - SITZT
# Bilder: Kopf nach links, nach rechts, zweimal beide Augen zu, einmal mit einem Auge gezwinkert
BLICKE = [(8, "vorn", 0, 1, 1), (3, "halb", 0, 1, 1), (20, "seite", 0, 1, 1), (3, "halb", 0, 1, 1),
          (6, "vorn", 0, 1, 1), (3, "halb", 1, 1, 1), (20, "seite", 1, 1, 1), (3, "halb", 1, 1, 1),
          (6, "vorn", 0, 1, 1), (4, "vorn", 0, 0, 0), (5, "vorn", 0, 1, 1), (4, "vorn", 0, 0, 0),
          (4, "vorn", 0, 1, 1), (5, "vorn", 0, 1, 0), (2, "vorn", 0, 1, 1)]


def runden(v):
    """Kaufmännisch runden (round() rundet halbe Werte zur geraden Zahl: Flügel würden zucken)."""
    return int(math.floor(v + 0.5))


def fluegel(bild, cx, y, n, hub):
    """Beide Flügel ab der Schulterzeile y, n Spalten lang; hub[s] = Zeilen, um die Stufe s (je
    zwei gleiche Nachbarspalten) gehoben ist (< 0: gesenkt). Innen drei Zeilen dick, außen eine;
    die unterste Zeile liegt im Schatten."""
    stufen, vorher = [], 0
    for wert in hub:                                                 # höchstens eine Zeile je Stufe: keine Lücken
        vorher = max(vorher - 1, min(vorher + 1, runden(wert)))
        stufen.append(vorher)
    for seite in (-1, 1):
        for d in range(1, n + 1):
            x = cx + seite * (3 + d)
            oben = y - stufen[(d - 1) // 2]
            dick = min(3, 1 + (n - d) // 2)
            for k in range(dick):
                bild.setze(x, oben + k, SCHATTEN if k and k == dick - 1 else WEISS)


def schlag(phase, kraft=1.0):
    """Flügelstellung im Flug: Die Spitze läuft dem Arm etwas nach, das macht den Schlag weich.
    kraft 0 = Gleiten: Flügel ruhig, leicht gewölbt."""
    return [ruhe + kraft * s * math.sin(phase - 0.35 * (s - 1)) for s, ruhe in zip((1, 2, 3, 4), GLEITEN)]


def gerade(h):
    """Gestreckter Flügel, Spitze um h Zeilen gehoben (beim Landen, Falten und Ausbreiten)."""
    return [h * s / 4 for s in (1, 2, 3, 4)]


def eule(bild, cx, y, rumpf=5, kopf="vorn", rechts=False, augen=(1, 1), n=0, hub=None):
    """Eule mit Kopfoberkante y; rumpf = Zeilen des Rumpfs (3 im Flug, 5 im Sitzen)."""
    if n:
        fluegel(bild, cx, y + 4, n, hub)
    farben = {"w": WEISS, "Y": AUGE, "k": SCHNABEL, "t": TUPFEN, "f": SCHATTEN if n == 0 else WEISS}
    bild.figur(cx - 3, y, KOPF[kopf], farben, spiegeln=rechts)
    if kopf == "vorn":                                               # Lider: Auge zu
        for auf, x in zip(augen, (cx - 1, cx + 1)):
            if not auf:
                bild.setze(x, y + 2, LID)
    bild.figur(cx - 3, y + 4, RUMPF[:rumpf - 1] + RUMPF[-1:], farben)


def hintergrund(bild, f, federt=0):
    """Nacht, Mond, Ebene und Baum; federt = 1: die Astspitze ist eine Zeile tiefer (Ast wippt)."""
    for x, y, phase, periode in STERNE:                              # wenige Sterne, funkeln langsam
        bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
    bild.kreis(MOND_X, MOND_Y, MOND_R, MOND)
    for x, y, b, h in KRATER_FLECKEN:
        bild.rechteck(x, y, b, h, KRATER)
    bild.rechteck(0, 14, B, 1, KANTE)                                # verschneite Ebene
    bild.rechteck(0, 15, B, 1, EBENE)
    # kahler Baum: Stamm, langer Ast nach links bis vor den Mond (Spitze eine Zeile höher), kurze Äste
    bild.rechteck(STAMM_X, 4, 3, 10, HOLZ)
    bild.rechteck(AST_KNICK, AST_Y, STAMM_X - AST_KNICK, 1, AST_SCHNEE)
    bild.rechteck(AST_KNICK, AST_Y + 1, STAMM_X - AST_KNICK, 1, HOLZ)
    bild.rechteck(AST_VON, AST_Y - 1 + federt, AST_KNICK - AST_VON, 1, AST_SCHNEE)
    bild.rechteck(AST_VON + 1, AST_Y + federt, AST_KNICK - AST_VON - 1, 1, HOLZ)
    bild.rechteck(47, 5, 7, 1, AST_SCHNEE)                           # oberer Ast links
    bild.rechteck(48, 6, 6, 1, HOLZ)
    bild.rechteck(57, 7, 7, 1, AST_SCHNEE)                           # Ast nach rechts aus dem Bild
    bild.rechteck(57, 8, 7, 1, HOLZ)
    bild.rechteck(STAMM_X + 1, 0, 1, 4, HOLZ)                        # Wipfel mit Gabel
    for seite in (-1, 1):
        bild.setze(STAMM_X + 1 + seite * 2, 2, HOLZ)
        bild.setze(STAMM_X + 1 + seite * 3, 1, HOLZ)
        bild.setze(STAMM_X + 1 + seite * 3, 0, AST_SCHNEE)


def federn(t):
    """Der Ast wippt nach, t Bilder nach dem Stoß: Spitze tief, hoch, noch einmal kurz tief."""
    return 1 if 0 <= t < 5 or 9 <= t < 12 else 0


def rieseln(bild, t):
    """Schnee rieselt vom Ast, t Bilder nach dem Stoß: unter der Eule und an der Astspitze."""
    for x, spaet in ((X_AST - 3, 0), (X_AST + 2, 3), (AST_VON + 5, 5)):
        y = AST_Y + 2 + (t - spaet) // 3
        if t >= spaet and y < 14:
            bild.setze(x, y, AST_SCHNEE)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        hintergrund(bild, f, federn(f - LANDET - 2) or federn(f - ABFLUG - 1))
        rieseln(bild, f - LANDET - 2)
        rieseln(bild, f - ABFLUG - 1)
        if ANFLUG <= f < LANDET:                                     # gleitet von links heran
            t = (f - ANFLUG) / (LANDET - ANFLUG)
            x = X_START + (X_AST - X_START) * (1 - (1 - t) ** 1.4)
            y = 1 + 2 * (1 - (1 - t) ** 2)
            kraft = min(1.0, max(0.0, (abs(f - GLEITET) - 8) / 6))   # vor dem Mond: Flügel ruhig
            phase = 2 * math.pi * (f - LANDET) / SCHLAG + math.pi / 2 + 0.5   # kommt mit Flügeln oben an
            eule(bild, runden(x), runden(y), rumpf=3, n=8, hub=schlag(phase, kraft))
        elif LANDET <= f < SITZT:                                    # setzt auf, richtet sich auf, faltet
            i = min(2, (f - LANDET) // 3)
            k = f - LANDET - 8
            n, h = FALTEN[max(0, min(len(FALTEN) - 1, k))]
            eule(bild, X_AST, 3 - i, rumpf=3 + i, n=n if k < len(FALTEN) else 0, hub=gerade(h))
        elif SITZT <= f < STARTET:                                   # sitzt: Kopf drehen, zwinkern
            u = f - SITZT
            for dauer, kopf, rechts, links_auf, rechts_auf in BLICKE:
                if u < dauer:
                    break
                u -= dauer
            eule(bild, X_AST, 1, kopf=kopf, rechts=bool(rechts), augen=(links_auf, rechts_auf))
        elif STARTET <= f < ABFLUG:                                  # breitet die Flügel aus, duckt sich
            n, h = FALTEN[max(0, len(FALTEN) - 1 - (f - STARTET))]
            ducken = 1 if f >= ABFLUG - 3 else 0
            eule(bild, X_AST, 1 + ducken, rumpf=5 - ducken, n=n, hub=gerade(h))
        elif ABFLUG <= f < WEG:                                      # stößt sich ab, fliegt nach rechts oben
            t = (f - ABFLUG) / (WEG - ABFLUG)
            x = X_AST + (X_ENDE - X_AST) * t ** 1.5
            y = 1 - 1.4 * t
            phase = 2 * math.pi * (f - ABFLUG) / SCHLAG + math.pi / 2
            eule(bild, runden(x), runden(y), rumpf=max(3, 5 - (f - ABFLUG) // 2), n=8, hub=schlag(phase))
        liste.append(bild)
    return liste
