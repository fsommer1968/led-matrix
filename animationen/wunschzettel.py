"""Wunschzettel: Briefumschläge mit Flügeln fliegen einer nach dem anderen durch die Polarnacht
zum verschneiten roten Briefkasten am Nordpol (rot-weißer Pfahl mit goldener Kugel); der
Kasten schluckt jeden Brief mit einem Hüpfer und einem Herzchen, am Ende ist er voll, die
Fahne geht hoch und "NORDPOL" erscheint in Gold – 255 Bilder.
"""
import math

from basis import (B, GELB, GOLD, HELLBLAU, NACHTBLAU, PINK, ROT, TUERKIS, WEISS, Bild, Sterne,
                   dimmen, sternschnuppe)

NAME = "wunschzettel"
TITEL = "Wunschzettel fliegen zum Nordpol"

STERNE = Sterne(anzahl=16, saat=505, y_max=11)
STERNE.sterne = [s for s in STERNE.sterne if s[0] < 43]              # nicht hinter dem Kasten


def sterne(bild, f):
    """Wie Sterne.zeichnen, aber die dunkelste Stufe (auf den LEDs kaum zu sehen) bleibt aus:
    Jeder Stern kostet in jedem Bild Speicher, und die Matrix nimmt höchstens 80 KB je Animation
    (Ziel 76000 Bytes, vorher 75462 – so bleibt Abstand; (23.11.2026)."""
    for x, y, phase, periode in STERNE.sterne:
        t = (f + phase) % periode / periode
        h = round((0.25 + 0.75 * (0.5 + 0.5 * math.cos(2 * math.pi * t))) * 4) / 4
        if h > 0.25:
            bild.setze(x, y, dimmen((255, 240, 200), h))


UMSCHLAG = ["wwwwwww",
            "wvwwwvw",
            "wwvwvww",
            "wwwvwww",
            "wwwwwww"]
KASTEN = [".sssssssss.",
          "srrrrrrrrrs",
          "rrrrrrrrrrd",
          "rkkkkkkkrrd",
          "rrrrrrrrrrd",
          "rrrrggrrrrd",
          "rrrrrrrrrrd"]
KASTEN_X, KASTEN_Y = 45, 4                  # linke obere Ecke des Kastens
SCHLITZ = (KASTEN_X + 1, KASTEN_Y + 3)      # hier fliegen die Briefe hinein
PFAHL_X = 59
BRIEFE = 6
ABSTAND, FLUG = 32, 44                      # Start alle 32 Bilder, Flug 44 Bilder
SIEGEL = [ROT, (0, 200, 60), PINK, GOLD, HELLBLAU, TUERKIS]
PAPIER = (255, 245, 220)
TEXT_AB = 212


def boden(bild):
    for x in range(B):
        huegel = 13 if math.sin(x / 5) + math.sin(x / 11 + 1) > 0.9 else 14   # sanfte Wehen
        for y in range(huegel, 16):
            bild.setze(x, y, (150, 165, 215) if y == huegel else (95, 105, 150))


def nordpol(bild, f, schluckt, voll):
    """Pfahl und Briefkasten; schluckt = Bilder seit dem letzten Brief (oder None)."""
    for y in range(3, 14):                                        # Pfahl rot/weiß, Streifen wandern
        farbe = ROT if ((y + f // 8) // 2) % 2 else WEISS
        bild.setze(PFAHL_X, y, farbe)
        bild.setze(PFAHL_X + 1, y, dimmen(farbe, 0.7))
    bild.rechteck(PFAHL_X, 1, 2, 2, GOLD)
    bild.setze(PFAHL_X, 1, (255, 240, 150) if (f // 10) % 3 == 0 else GELB)
    bild.rechteck(KASTEN_X + 4, KASTEN_Y + 6, 3, 4, (120, 70, 30))  # Pfosten
    hopst = 1 if schluckt is not None and schluckt in (1, 2) else 0
    farben = {"s": WEISS, "r": (235, 0, 15), "d": (140, 0, 10), "k": (35, 0, 0), "g": GOLD}
    if schluckt is not None and schluckt < 4:
        farben["k"] = (255, 230, 120)                             # Schlitz leuchtet auf
    elif voll:
        farben["k"] = PAPIER                                      # Briefe schauen heraus
    bild.figur(KASTEN_X, KASTEN_Y - hopst, KASTEN, farben)
    if voll:                                                      # Fahne oben
        bild.rechteck(KASTEN_X + 11, KASTEN_Y, 1, 4, (200, 200, 215))
        bild.rechteck(KASTEN_X + 11, KASTEN_Y - 2, 2, 2, GELB)
    else:
        bild.rechteck(KASTEN_X + 11, KASTEN_Y + 4, 2, 1, (200, 200, 215))
    if schluckt is not None and 2 <= schluckt < 14:               # Herzchen steigt auf
        hx, hy = KASTEN_X + 5, KASTEN_Y - 2 - (schluckt - 2) // 6
        hell = 1 - (schluckt - 2) / 14
        for dx, dy in ((-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (0, 2)):
            bild.setze(hx + dx, hy + dy - 1, dimmen((255, 60, 120), hell))


def brief(bild, k, t, f):
    """Brief k, t Bilder nach dem Start: flattert in Wellen zum Schlitz und schlüpft hinein."""
    farbe = SIEGEL[k % len(SIEGEL)]
    a = t / FLUG
    zx, zy = SCHLITZ[0] - 3, SCHLITZ[1] - 2                       # linke obere Ecke am Ziel
    x = -9 + (zx + 9) * (1 - (1 - a) ** 1.6)                      # bremst vor dem Kasten ab
    welle = 3.5 * math.sin(t / 6 + k * 1.7) * (1 - a) ** 0.7
    y = 5 + welle + (zy - 5) * a
    x, y = round(x), round(y)
    rest = FLUG - t
    if rest <= 3:                                                 # schlüpft in den Schlitz
        bild.rechteck(SCHLITZ[0] - rest, SCHLITZ[1], rest + 3, 1, PAPIER)
        return
    for s in range(1, 4):                                         # Glitzerspur
        if (t + s) % 2 == 0:
            ts = t - s * 3
            if ts >= 0:
                bild.setze(x - 3 - s * 3, y + 2 + round(math.sin(ts / 3 + k)), dimmen(farbe, 1 - s * 0.25))
    bild.figur(x, y, UMSCHLAG, {"w": PAPIER, "v": farbe})
    fluegel = (210, 225, 255)
    if (t // 3) % 2:                                              # Flügel oben
        for dx, dy in ((-1, 1), (-2, 0), (-3, -1), (-2, 1), (7, 1), (8, 0), (9, -1), (8, 1)):
            bild.setze(x + dx, y + dy, fluegel)
    else:                                                         # Flügel unten
        for dx, dy in ((-1, 2), (-2, 3), (-3, 4), (-2, 2), (7, 2), (8, 3), (9, 4), (8, 2)):
            bild.setze(x + dx, y + dy, fluegel)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        sterne(bild, f)
        sternschnuppe(bild, f, 20, 40, 0)
        sternschnuppe(bild, f, 150, 30, 0)
        boden(bild)
        angekommen = [k * ABSTAND + FLUG for k in range(BRIEFE) if f >= k * ABSTAND + FLUG]
        schluckt = f - angekommen[-1] if angekommen else None
        voll = len(angekommen) == BRIEFE and schluckt >= 4
        nordpol(bild, f, schluckt, voll)
        for k in range(BRIEFE):
            t = f - k * ABSTAND
            if 0 <= t < FLUG:
                brief(bild, k, t, f)
        if f >= TEXT_AB:                                          # NORDPOL, Buchstabe für Buchstabe
            bild.rechteck(0, 2, 44, 9, NACHTBLAU)
            n = min(7, (f - TEXT_AB) // 2 + 1)
            glanz = (f - TEXT_AB - 16) // 2 % 12                  # ein Lichtschein läuft durch
            bild.text(2, 3, "NORDPOL"[:n],
                      lambda i: (255, 245, 170) if f >= TEXT_AB + 16 and i == glanz else GOLD)
            if voll and (f // 4) % 2:                             # der volle Kasten funkelt
                for dx, dy in ((-1, -1), (11, 6), (5, -3)):
                    bild.setze(KASTEN_X + dx, KASTEN_Y + dy, GELB)
        liste.append(bild)
    return liste
