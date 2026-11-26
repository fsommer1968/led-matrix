"""Der Weg der Windlichter: Ein verschneiter Weg zieht von links vorn nach rechts hinten zu einem
kleinen Haus. Am Wegrand stehen sechs Windlichter auf kurzen Stäben. Eine Gestalt mit roter
Zipfelmütze und brennendem Span geht den Weg entlang und zündet eines nach dem anderen an; jedes
flammt kurz auf, brennt dann ruhig und wirft einen warmen Schein in den Schnee. Leuchtet der ganze
Weg, löscht sie den Span und schaut zurück; die Haustür geht auf, warmes Licht fällt heraus, sie
geht hinein, die Tür fällt zu. Über dem leuchtenden Weg zieht eine Sternschnuppe; dann verlöschen
die Lichter der Reihe nach mit einem Rauchfaden – Anfang und Ende zeigen denselben dunklen Weg.
255 Bilder.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Himmel, Waldsaum und Schneefeld in waagerechten
Streifen (gleiche Spalten); der Weg steigt in drei Stufen jeweils mitten zwischen zwei Lichtern
und wird hinten schmaler (das ist die ganze Perspektive); alle Lichter sind gleich gebaut und
brennen meist im selben Zustand (Kopien kosten fast nichts); das Haus hat ein gerades Dach, der
Schornstein steht über dem Fenster; kein Schneefall, kein Mond (hätte rund 3500 Bytes gekostet),
keine Tannenspitzen am Waldsaum (rund 4500), drei Sterne.
"""
import random

from basis import B, HAUT, NACHTBLAU, ROT, SCHWARZ, Bild, dimmen, sternschnuppe

NAME = "windlichter"
TITEL = "Der Weg der Windlichter"

# ── Farben (deutliche Stufen, große Flächen gedämpft) ──
STERN = (255, 240, 200)
WALD = (0, 52, 26)                             # Waldsaum am Horizont
KANTE = (150, 165, 215)                        # Schneekante am Horizont und auf dem Dach
FELD = (45, 55, 95)                            # Schneefeld bei Nacht
WEG = (22, 28, 58)                             # ausgetretener Weg, dunkler
STAB = SCHWARZ                                 # Stab und Deckel der Windlichter
GLAS_AUS = (110, 125, 160)                     # Glas ohne Licht
GLAS = [None, (150, 55, 0), (255, 115, 0), (255, 165, 20)]           # glimmt, brennt, flammt auf
FLAMME = [None, (255, 150, 0), (255, 215, 50), (255, 245, 170)]
SCHEIN_INNEN = (165, 95, 25)                   # Schein im Schnee: am Fuß des Lichts
SCHEIN_AUSSEN = (95, 60, 40)                   # … am Rand
SCHEIN_WEG = (70, 42, 22)                      # … und auf dem dunklen Weg
RAUCH = (150, 150, 165)                        # Rauchfaden nach dem Verlöschen
WAND = (49, 19, 0)
DACH = (36, 30, 44)
TUER = (100, 0, 12)
FENSTER = [(200, 120, 10), (255, 160, 20)]     # Fenster: ruhig, Kaminfeuer flackert kurz heller
TUERLICHT = (255, 200, 90)
MUETZE = ROT
JACKE = (0, 190, 70)
AUGE = (50, 25, 10)
BEIN = (0, 70, 255)
SPAN = (150, 130, 90)
FEUER = [(255, 215, 50), (255, 120, 0)]        # Flamme am Span, flackert

# ── Aufbau ──
HORIZONT = 8                                   # Zeile der Schneekante hinten
STUFEN = [(0, 14), (19, 13), (33, 12), (47, 11)]                     # ab Spalte: obere Zeile des Wegs
SCHMAL = (33, 47)                              # hier hinten ist der Weg nur eine Zeile breit (Ferne)
LICHTER = [8, 15, 22, 29, 36, 43]              # Spalte des Stabs
HAUS_X, HAUS_B, HAUS_OBEN, HAUS_UNTEN = 48, 15, 4, 11
TUER_X, TUER_OBEN = 50, 5                      # Tür 3 × 7
FENSTER_X, FENSTER_Y = 56, 6                   # Fenster 3 × 3
SCHORNSTEIN_X = 56                             # zwei Spalten über dem Fenster
STERNE = [(5, 1, 51, 0.0), (27, 3, 85, 0.4), (40, 0, 51, 0.7)]       # x, y, Periode, Phase
KAMIN_TAKT = 51                                # das Fenster flackert in einem Muster, das in die Runde passt
KAMIN_HELL = (6, 7, 8, 20, 21, 29, 30, 31, 43, 44)

# Gestalt (Blick nach rechts): m Mütze, h Gesicht, a Auge, j Jacke, b Beine, s Span, f Flamme
GEHT = [[".m....", "mmm...", "hha...", "jjj.f.", "jjjjs.", "jjj...", "b.b..."],
        [".m....", "mmm...", "hha...", "jjj.f.", "jjjjs.", "jjj...", ".b...."]]
ZUENDET = [".m....", "mmm...", "hha...", "jjj..f", "jjjjs.", "jjj...", "b.b..."]   # Flamme ans Glas
OHNE = [[".m.", "mmm", "hha", "jjj", "jjj", "jjj", "b.b"],
        [".m.", "mmm", "hha", "jjj", "jjj", "jjj", ".b."]]

# ── Ablauf ──
KOMMT = 2                                      # die Gestalt tritt links ins Bild
TEMPO = 2                                      # Bilder je Spalte
ZUENDEN = 8                                    # so lange steht sie an jedem Licht
SCHAUT = 12                                    # nach dem letzten Licht: Span aus, schaut zurück
TUER_TAKT = 2                                  # Bilder je Türspalte beim Öffnen und Schließen
IN_TUER = 4                                    # steht in der offenen Tür
RUHE = 18                                      # alle Lichter brennen, niemand mehr da
AUS_TAKT = 8                                   # Abstand, in dem die Lichter verlöschen
VERLISCHT = [2, 1, 2, 1, 1]                    # Stufen beim Verlöschen


def plan():
    """Weg der Gestalt als (Bild, linke Spalte) und die Bilder, in denen die Lichter angehen."""
    weg, an = [(KOMMT, -4)], []
    f, x = KOMMT, -4
    for lx in LICHTER:
        f += (lx - 6 - x) * TEMPO
        x = lx - 6
        weg += [(f, x), (f + ZUENDEN, x)]
        an.append(f + 3)
        f += ZUENDEN
    fertig = f
    f += SCHAUT
    weg.append((f, x))
    f += (TUER_X - x) * TEMPO
    weg += [(f, TUER_X), (f + IN_TUER + 3 * TUER_TAKT, TUER_X)]
    return weg, an, fertig, f


WEG_PLAN, AN, FERTIG, DRIN = plan()            # FERTIG: letztes Licht brennt; DRIN: sie steht in der Tür
TUER_AUF = FERTIG + SCHAUT - 3 * TUER_TAKT + 1                       # die Tür geht auf
TUER_ZU = DRIN + IN_TUER                       # … und wieder zu
AUS = [TUER_ZU + 3 * TUER_TAKT + RUHE + k * AUS_TAKT for k in range(len(LICHTER))]
SCHNUPPE = (AUS[0] - 12, 22, 0)                # Bild, Spalte, Zeile: Sternschnuppe über dem leuchtenden Weg
_z = random.Random(2026)
FLACKERN = [[_z.random() < 0.12 for _ in range(128)] for _ in LICHTER]   # je zwei Bilder: flammt kurz höher


def weg_y(x):
    """Obere Zeile des Wegs in Spalte x (dort gehen die Füße)."""
    y = STUFEN[0][1]
    for x0, zeile in STUFEN:
        if x >= x0:
            y = zeile
    return y


def gestalt_x(f):
    """Linke Spalte der Gestalt, None solange sie nicht zu sehen ist."""
    for (f0, x0), (f1, x1) in zip(WEG_PLAN, WEG_PLAN[1:]):
        if f0 <= f < f1:
            return x0 + (x1 - x0) * (f - f0) // (f1 - f0)
    return None


def geht(f):
    """Ist die Gestalt in Bild f unterwegs (und steht nicht an einem Licht oder in der Tür)?"""
    return gestalt_x(f) != gestalt_x(f + 1) or gestalt_x(f) != gestalt_x(f - 1)


def stufe(k, f):
    """Zustand des Lichts k: 0 aus, 1 glimmt, 2 brennt, 3 flammt auf."""
    if f < AN[k] or f >= AUS[k] + len(VERLISCHT):
        return 0
    if f >= AUS[k]:
        return VERLISCHT[f - AUS[k]]
    if f < AN[k] + 4:
        return (1, 3, 3, 3)[f - AN[k]]
    return 3 if FLACKERN[k][f // 2] else 2


def windlicht(bild, lx, s, rauch):
    """Windlicht auf dem Stab am Wegrand; s = Zustand, rauch = Bilder seit dem Verlöschen."""
    g = weg_y(lx)
    bild.setze(lx, g - 4, STAB)                                      # Deckel
    bild.rechteck(lx - 1, g - 3, 3, 2, GLAS[s] if s else GLAS_AUS)
    if s == 1:
        bild.setze(lx, g - 2, FLAMME[1])
    elif s:
        bild.rechteck(lx, g - 3, 1, 2, FLAMME[s])
    if s >= 2:                                                       # Schein im Schnee, rund um den Fuß
        bild.setze(lx - 2, g - 2, SCHEIN_AUSSEN)
        bild.setze(lx + 2, g - 2, SCHEIN_AUSSEN)
        bild.rechteck(lx - 2, g - 1, 5, 1, SCHEIN_INNEN)
        bild.rechteck(lx - 1, g, 3, 1, SCHEIN_WEG)
        if s == 3:                                                   # flammt auf: der Schein reicht weiter
            bild.setze(lx - 3, g - 1, SCHEIN_AUSSEN)
            bild.setze(lx + 3, g - 1, SCHEIN_AUSSEN)
    elif s == 1:
        bild.rechteck(lx - 1, g - 1, 3, 1, SCHEIN_AUSSEN)
    bild.setze(lx, g - 1, STAB)
    if 0 <= rauch < 4:                                               # Rauchfaden steigt auf
        bild.setze(lx, g - 5 - rauch // 2, RAUCH if rauch < 2 else dimmen(RAUCH, 0.5))


def haus(bild, offen, kamin):
    """Kleines Haus; offen = Zahl der Türspalten, aus denen Licht fällt (0 bis 3), kamin = das
    Feuer drinnen flackert gerade heller."""
    hoch = HAUS_UNTEN - TUER_OBEN + 1
    bild.rechteck(HAUS_X, HAUS_OBEN, HAUS_B, HAUS_UNTEN - HAUS_OBEN + 1, WAND)
    bild.rechteck(SCHORNSTEIN_X, HAUS_OBEN - 3, 2, 1, WAND)
    bild.rechteck(SCHORNSTEIN_X, HAUS_OBEN - 4, 2, 1, KANTE)         # Schneehaube
    bild.rechteck(HAUS_X - 1, HAUS_OBEN - 1, HAUS_B + 2, 1, KANTE)   # Schnee auf dem Dach, hängt an den
    bild.rechteck(HAUS_X, HAUS_OBEN - 2, HAUS_B, 1, KANTE)           # Enden eine Zeile tiefer
    bild.rechteck(HAUS_X, HAUS_OBEN - 1, HAUS_B, 1, DACH)            # Schatten unter der Traufe
    bild.rechteck(FENSTER_X, FENSTER_Y, 3, 3, FENSTER[1 if kamin else 0])
    bild.rechteck(TUER_X, TUER_OBEN, 3, hoch, TUER)
    bild.rechteck(TUER_X, TUER_OBEN, offen, hoch, TUERLICHT)
    bild.rechteck(TUER_X - 2, HAUS_UNTEN + 1, 2 * offen, 1, SCHEIN_INNEN)     # Licht fällt auf den Weg
    bild.rechteck(TUER_X - 4, HAUS_UNTEN + 2, 2 * offen, 1, SCHEIN_AUSSEN)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, periode, phase in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f / periode + phase) % 1 < 0.6 else 0.5))
        sternschnuppe(bild, f, *SCHNUPPE, laenge=6)                  # verschwindet hinter dem Wald
        bild.rechteck(0, HORIZONT - 2, B, 2, WALD)
        bild.rechteck(0, HORIZONT, B, 1, KANTE)
        bild.rechteck(0, HORIZONT + 1, B, 16 - HORIZONT - 1, FELD)
        for x in range(TUER_X + 3):                                  # Weg: vorn zwei Zeilen, hinten eine
            bild.rechteck(x, weg_y(x), 1, 1 if SCHMAL[0] <= x < SCHMAL[1] else 2, WEG)
        zu = max(0, min(3, (f - TUER_ZU) // TUER_TAKT + 1))          # Türspalten, die schon wieder zu sind
        offen = max(0, min(3 - zu, (f - TUER_AUF) // TUER_TAKT + 1))
        haus(bild, offen, f % KAMIN_TAKT in KAMIN_HELL)
        for k, lx in enumerate(LICHTER):
            windlicht(bild, lx, stufe(k, f), f - AUS[k] - len(VERLISCHT))
        x = gestalt_x(f)
        if x is not None:
            g = weg_y(x + 1)
            schritt = (f // TEMPO) % 2 if geht(f) else 0             # je Spalte ein Schritt
            farben = {"m": MUETZE, "h": HAUT, "a": AUGE, "j": JACKE, "b": BEIN, "s": SPAN,
                      "f": FEUER[(f // 2) % 2] if f < FERTIG else RAUCH}
            if f >= FERTIG + 2:                                      # ohne Span: schaut zurück, geht zur Tür
                zurueck = FERTIG + 3 <= f < FERTIG + SCHAUT - 1
                bild.figur(x, g - 6, OHNE[schritt], farben, spiegeln=zurueck)
            elif any(a - 2 <= f <= a for a in AN):                   # hält die Flamme ans Glas
                bild.figur(x, g - 6, ZUENDET, farben)
            else:
                bild.figur(x, g - 6, GEHT[schritt], farben)
            if f >= DRIN:                                            # die Tür schließt sich vor ihr
                bild.rechteck(TUER_X + offen, TUER_OBEN, 3 - offen, HAUS_UNTEN - TUER_OBEN + 1, TUER)
        liste.append(bild)
    return liste
