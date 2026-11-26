"""Kirchenorgel an Weihnachten: die Orgel von vorn, fünfzehn silberne Pfeifen mit goldenem Labium,
zur Mitte hin länger, im dunklen Holzgehäuse (Pfosten mit goldener Zier, Rückwand, Sockel) mit
Tannengirlande und roten Beeren; links und rechts brennt eine rote Kerze. Es wird gespielt: erst ein
Choral (Bass in der Mitte, die Melodie wandert außen), dann ein Lauf von außen zur Mitte und zurück,
ein Glissando von links nach rechts und vier Akkorde im Wechsel. Die klingenden Pfeifen leuchten
warmweiß und klingen kurz nach; bunte Noten steigen hinter ihnen auf und schweben in sanftem Bogen
nach oben weg. Der volle Schlussakkord klingt von außen zur Mitte aus, dann sind die Pfeifen wieder
ruhig, nur die Kerzen flackern – 255 Bilder, die Runde schließt ohne Sprung (das Flackern geht in
255 auf). Kein Text.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum alle Pfeifen im selben Raster (zwei gleiche Spalten,
eine Lücke), die rechte Hälfte spiegelgleich zur linken, Girlande und Beeren im Raster der Pfeifen
(alle Lücken sind gleiche Spalten), schwarzer Grund, schlanke Flamme, zwei bis fünf Noten zugleich
(jede kostet etwa 25 Bytes je Bild). Das Aufleuchten ändert nur Farben und kostet fast nichts.
"""
import math

from basis import BRAUN, DUNKELGRUEN, GELB, HELLBLAU, HELLGRUEN, ORANGE, PINK, ROT, SCHWARZ, Bild

NAME = "orgel"
TITEL = "Kirchenorgel an Weihnachten"

RUNDE = 255
# ── Orgel ──────────────────────────────────────────────────────────
PFEIFEN = 15
X0 = 10                                        # linke Spalte der ersten Pfeife; jede 2 breit + 1 Lücke
OBEN = [10, 9, 8, 7, 6, 5, 4, 3]               # oberste Zeile, vom Rand zur Mitte
LABIUM_Y, FUSS_Y = 12, 13
SOCKEL_Y = 14                                  # Holzgehäuse: Zeilen 14 und 15
PFOSTEN = (7, 55)                              # linke Spalte der beiden Pfosten (2 breit)
PFOSTEN_OBEN = 9
WAND_Y = 11                                    # ab hier Rückwand hinter den Pfeifenfüßen

SILBER = (120, 128, 150)
LABIUM = (190, 120, 0)
HELL = (255, 225, 150)                         # Pfeife klingt: warmweiß
HELL_LABIUM = (255, 190, 40)
NACH = (200, 165, 100)                         # klingt nach
NACH_LABIUM = (230, 150, 0)
BEERE = (200, 0, 0)

# ── Kerzen ─────────────────────────────────────────────────────────
KERZEN = (1, 60)                               # linke Spalte (3 breit)
KERZE_OBEN = 8
WACHS = (190, 0, 20)
SAUM = (255, 110, 30)                          # geschmolzener Rand der Kerze
LEUCHTER = (190, 120, 0)
KERN, FLAMME, SPITZE = (255, 245, 190), (255, 200, 40), (255, 110, 0)
FLACKER = "AAAAALLLAAAHHHRRR"                   # Spitze der Flamme je Bild: mittig, links, hoch, rechts
FLACKERN = len(FLACKER)                        # 17 teilt 255

# ── Noten ──────────────────────────────────────────────────────────
ACHTEL = [".xx", ".x.", ".x.", "xx.", "xx."]
DOPPEL = [".xxxx", ".x..x", ".x..x", "xx.xx", "xx.xx"]
STEIGEN = 3                                    # Bilder je Zeile
BUNT = [ROT, GELB, HELLBLAU, PINK, HELLGRUEN, ORANGE]

# ── Das Stück ──────────────────────────────────────────────────────
NACHKLANG = 3                                  # so viele Bilder klingt eine Pfeife nach
CHORAL, SCHLAG = 12, 8                         # Beginn, Bilder je Schlag
MELODIE = [3, 11, 2, 12, 4, 10, 1, 13]         # je Schlag eine Pfeife außen, dazu der Bass in der Mitte
LAUF = 78                                      # Lauf von außen zur Mitte und zurück, 3 Bilder je Pfeife
GLISSANDO = 124                                # einmal von links nach rechts, 2 Bilder je Pfeife
AKKORDE, AKKORD = 156, 10                      # vier Akkorde im Wechsel: gerade, ungerade Pfeifen
SCHLUSS, SCHLUSS_DAUER = 198, 20               # voller Schlussakkord, klingt von außen zur Mitte aus
AUSKLANG = 3                                   # Bilder je Pfeifenpaar beim Ausklingen


def pfeife_oben(i):
    return OBEN[min(i, PFEIFEN - 1 - i)]


def pfeife_x(i):
    return X0 + 3 * i


def partitur():
    """Liefert (anschläge, noten): Anschlag = (Beginn, Dauer, Pfeifen),
    Note = (Beginn, Pfeife, Form, Drift in Spalten je 12 Bilder)."""
    an, noten = [], []
    for n, p in enumerate(MELODIE):                                  # Choral
        f = CHORAL + n * SCHLAG
        an.append((f, 6, [p]))
        an.append((f, 7, [7] if n % 2 == 0 else [6, 8]))
        noten.append((f, p, DOPPEL if n in (2, 5) else ACHTEL, -1 if p < 7 else 1))
    f = LAUF                                                         # Lauf hinein und wieder hinaus
    for s in list(range(8)) + list(range(6, -1, -1)):
        an.append((f, 3, [s, 14 - s]))
        f += 3
    noten += [(LAUF + 3, 1, ACHTEL, -1), (LAUF + 12, 10, ACHTEL, 1), (LAUF + 27, 5, ACHTEL, 0),
              (LAUF + 33, 11, DOPPEL, 1), (LAUF + 39, 1, ACHTEL, 0)]
    for i in range(PFEIFEN):                                         # Glissando
        an.append((GLISSANDO + 2 * i, 2, [i]))
    noten += [(GLISSANDO + 4, 2, ACHTEL, -1), (GLISSANDO + 10, 5, ACHTEL, 0), (GLISSANDO + 16, 8, ACHTEL, 1),
              (GLISSANDO + 22, 11, ACHTEL, 0), (GLISSANDO + 26, 13, ACHTEL, 1)]
    for n in range(4):                                               # Akkorde im Wechsel
        f = AKKORDE + n * AKKORD
        an.append((f, 8, list(range(n % 2, PFEIFEN, 2))))
        noten.append((f, (2, 11, 4, 13)[n], DOPPEL if n == 1 else ACHTEL, (-1, 1, 0, 1)[n]))
    noten.append((AKKORDE + 2 * AKKORD + 4, 10, ACHTEL, 1))
    for k in range(8):                                               # Schlussakkord: Mitte klingt am längsten
        an.append((SCHLUSS, SCHLUSS_DAUER + (7 - k) * AUSKLANG, [7 - k, 7 + k]))
    noten += [(SCHLUSS, 1, ACHTEL, -1), (SCHLUSS + 3, 11, ACHTEL, 0), (SCHLUSS + 7, 4, DOPPEL, -1),
              (SCHLUSS + 11, 9, ACHTEL, 1), (SCHLUSS + 15, 2, ACHTEL, 0)]
    return an, noten


ANSCHLAEGE, NOTEN = partitur()


def klang(i, f):
    """0 = ruhig, 1 = klingt nach, 2 = klingt."""
    stufe = 0
    for start, dauer, pfeifen in ANSCHLAEGE:
        if i in pfeifen:
            if start <= f < start + dauer:
                return 2
            if start + dauer <= f < start + dauer + NACHKLANG:
                stufe = 1
    return stufe


def orgel(bild, f):
    bild.rechteck(PFOSTEN[0], WAND_Y, PFOSTEN[1] + 2 - PFOSTEN[0], 16 - WAND_Y, BRAUN)
    for x in PFOSTEN:
        bild.rechteck(x, PFOSTEN_OBEN, 2, SOCKEL_Y - PFOSTEN_OBEN, BRAUN)
        bild.rechteck(x, PFOSTEN_OBEN, 2, 1, LABIUM)                 # goldene Zier
    for i in range(PFEIFEN):
        x, oben = pfeife_x(i), pfeife_oben(i)
        stufe = klang(i, f)
        metall = (SILBER, NACH, HELL)[stufe]
        bild.rechteck(x, oben, 2, FUSS_Y + 1 - oben, metall)
        bild.rechteck(x, LABIUM_Y, 2, 1, (LABIUM, NACH_LABIUM, HELL_LABIUM)[stufe])
        bild.rechteck(x, SOCKEL_Y, 2, 1, DUNKELGRUEN)                # Girlande vor dem Sockel
    for x in range(X0 - 1, pfeife_x(PFEIFEN), 3):                    # Beeren in den Lücken
        bild.setze(x, SOCKEL_Y, BEERE)


def kerze(bild, x, f):
    bild.rechteck(x, KERZE_OBEN, 3, 14 - KERZE_OBEN, WACHS)
    bild.rechteck(x, KERZE_OBEN, 3, 1, SAUM)                         # geschmolzener Rand, leuchtet vom Feuer
    bild.rechteck(x, 14, 3, 1, LEUCHTER)
    bild.setze(x + 1, 15, LEUCHTER)
    form = FLACKER[f % FLACKERN]
    y = KERZE_OBEN - 1
    bild.setze(x + 1, y, KERN)
    bild.setze(x + 1, y - 1, FLAMME)
    if form == "H":                                                  # hoch
        bild.setze(x + 1, y - 2, FLAMME)
        bild.setze(x + 1, y - 3, SPITZE)
    else:                                                            # Spitze mittig, links, rechts
        bild.setze(x + 1 + {"A": 0, "L": -1, "R": 1}[form], y - 2, SPITZE)


def noten(bild, f):
    for k, (start, p, form, drift) in enumerate(NOTEN):
        t = f - start
        if t < 0:
            continue
        wiegen = round(1.3 * math.sin(t / 6)) * (1 if k % 2 else -1)   # schwebt in sanftem Bogen
        x0 = pfeife_x(p) - 1 + drift * (t // 12) + wiegen
        unten = pfeife_oben(p) + 2 - t // STEIGEN                    # Zeile unter der Note
        if unten <= 0:
            continue
        farbe = BUNT[k % len(BUNT)]
        for dy, zeile in enumerate(form):
            y = unten - len(form) + dy
            for dx, c in enumerate(zeile):                           # steigt hinter den Pfeifen auf
                if c == "x" and y < pfeife_oben(p) and bild.hole(x0 + dx, y) == SCHWARZ:
                    bild.setze(x0 + dx, y, farbe)


def bilder():
    liste = []
    for f in range(RUNDE):
        bild = Bild(SCHWARZ)
        orgel(bild, f)
        kerze(bild, KERZEN[0], f)
        kerze(bild, KERZEN[1], f + 6)
        noten(bild, f)
        liste.append(bild)
    return liste
