"""Adventskalender mit Countdown – ändert sich jeden Tag (wird auf dem Pi täglich neu erzeugt).

Teil 1  Kalender mit Türchen; das heutige (große fette Zahl = Tage bis Heiligabend) zittert,
        schwingt auf, warmes Licht fällt heraus und zeigt groß das Motiv des Tages (Stern, Baum,
        Kerze, Glocke, Geschenk, Herz, Mond, Schneemann – je nach Datum), Funken ringsum
Teil 2  "NOCH 29 TAGE BIS WEIHNACHTEN" läuft durch (am 24.12. "HEUTE IST HEILIGABEND",
        danach "FROHE WEIHNACHTEN"), gleichmäßig 1,5 Pixel je Bild; kurze Texte starten später

Aufruf ohne Datum: heute (Ortszeit des Rechners). Für Tests: bilder(datetime.date(...)).

Größe (23.11.2026): Die Matrix speichert je Animation nur 80 KB und komprimiert jedes Bild
einzeln, spaltenweise; Ziel für den Kalender höchstens 72000 Bytes an jedem Datum (vorher
82000–91000). Deshalb: das Licht im offenen Türchen hat je Spalte eine Farbe (zwei Stufen, innen
heller) statt eines runden Verlaufs in 40 Stufen; die kleinen Türchen verlieren ihre Zahlen,
sobald sie zurücktreten (die Ziffern kosten in jedem Bild rund 130 Bytes); 8 statt 10 Flocken.
"""
import datetime
import math
import random

from basis import (B, BUNT, GELB, GOLD, SCHRIFT, WEISS, Bild, Schnee, dimmen, klein_text, mischen,
                   regenbogen, textbreite)

NAME = "adventskalender"
TITEL = "Adventskalender mit Countdown (täglich neu)"

HINTERGRUND = (25, 0, 8)
TUER = (170, 10, 25)
TUER_HELL = (230, 60, 50)
TUER_DUNKEL = (95, 0, 15)
RAHMEN = (220, 160, 30)
INNEN = (10, 4, 30)
SCHNEE = Schnee(anzahl=8, saat=606, farbe=(150, 140, 170))    # 8 statt 10 Flocken: Abstand zur Größengrenze
TUER_X, TUER_B = 22, 20                     # großes Türchen
MITTE_X, MITTE_Y = TUER_X + TUER_B // 2, 8
TEMPO = 1.5                                 # Laufschrift: Pixel je Bild
SCHEIN_INNEN, SCHEIN_AUSSEN, SCHEIN_BREIT = 0.17, 0.07, 7   # Licht im offenen Türchen

# ── Motive (etwa 11×12) ────────────────────────────────────────────
STERN = ["....yy....",
         "....yy....",
         "...yyyy...",
         "yyyywwyyyy",
         ".yywwwwyy.",
         "..ywwwwy..",
         "..yyyyyy..",
         ".yyyyyyyy.",
         ".yyy..yyy.",
         "yy......yy"]
BAUM = ["....ss....",
        "....gg....",
        "...gGGg...",
        "..gGGGGg..",
        "...gGGg...",
        "..gGGGGg..",
        ".gGGGGGGg.",
        "..gGGGGg..",
        ".gGGGGGGg.",
        "gGGGGGGGGg",
        "....bb....",
        "....bb...."]
KERZE = ["...rrrr...",
         "...Rrrr...",
         "...Rrrr...",
         "...Rrrr...",
         "...Rrrr...",
         "...Rrrr...",
         ".oooooooo.",
         "..oooooo.."]
GLOCKE = ["..rr..rr..",
          "...rrrr...",
          "...oooo...",
          "..oOoooo..",
          "..oOoooo..",
          "..oOoooo..",
          "..oOoooo..",
          ".oOoooooo.",
          "oooooooooo"]
GESCHENK = ["..yy..yy..",
            "...yyyy...",
            "bbbbyybbbb",
            "BBBByyBBBB",
            "BBBByyBBBB",
            "yyyyyyyyyy",
            "BBBByyBBBB",
            "BBBByyBBBB",
            "BBBByyBBBB"]
HERZ = [".rrr..rrr.",
        "rRRrrrrrrr",
        "rRrrrrrrrr",
        "rrrrrrrrrr",
        "rrrrrrrrrr",
        ".rrrrrrrr.",
        "..rrrrrr..",
        "...rrrr...",
        "....rr...."]
MOND = ["...mmmm...",
        ".mmmm.....",
        ".mmm......",
        "mmmm......",
        "mmmm......",
        "mmmm......",
        "mmmmm.....",
        ".mmmmm...m",
        ".mmmmmmmm.",
        "...mmmmm.."]
SCHNEEMANN = ["...kkkk...",
              "...kkkk...",
              "..kkkkkk..",
              "...wwww...",
              "...wwww.o.",
              "..rrrrrr..",
              "..wwwwrr..",
              ".wwwwwww..",
              ".wwwkwww..",
              ".wwwwwww..",
              ".wwwkwww..",
              "..wwwww..."]
MOTIVE = [STERN, BAUM, KERZE, GLOCKE, GESCHENK, HERZ, MOND, SCHNEEMANN]
MOTIV_FARBEN = {"y": GELB, "w": WEISS, "s": GELB, "g": (0, 110, 25), "G": (0, 190, 40), "b": (130, 60, 15),
                "r": (255, 0, 30), "R": (255, 110, 110), "o": GOLD, "O": (255, 225, 110),
                "B": (0, 110, 255), "m": (255, 225, 120), "k": (70, 70, 85)}


def tage_bis_heiligabend(datum):
    return (datetime.date(datum.year, 12, 24) - datum).days


def laufschrift(datum):
    n = tage_bis_heiligabend(datum)
    if n > 1:
        return f"NOCH {n} TAGE BIS WEIHNACHTEN"
    if n == 1:
        return "MORGEN IST HEILIGABEND"
    if n == 0:
        return "HEUTE IST HEILIGABEND"
    return "FROHE WEIHNACHTEN"


def motiv(bild, art, cx, cy, f):
    """Motiv des Tages, mittig um (cx, cy), mit kleiner Bewegung."""
    zeilen = MOTIVE[art]
    farben = dict(MOTIV_FARBEN)
    x0, y0 = cx - 5, cy - len(zeilen) // 2
    if art == 0:                                                  # Stern funkelt
        farben["y"] = GELB if (f // 5) % 3 else (255, 240, 150)
        farben["w"] = WEISS if (f // 5) % 3 else GELB
    elif art == 2:                                                # Kerze: Platz für die Flamme
        y0 += 2
    elif art == 5 and (f // 6) % 2:                               # Herz pocht
        farben["r"] = (255, 60, 90)
    elif art == 3:                                                # Glocke schwingt
        x0 += (0, 1, 0, -1)[(f // 4) % 4]
        y0 -= 1
    bild.figur(x0, y0, zeilen, farben)
    if art == 1:                                                  # Baum: Lichter blinken
        for k, (dx, dy) in enumerate(((4, 3), (6, 5), (3, 6), (5, 8), (7, 8), (2, 9))):
            if (f // 5 + k) % 3:
                bild.setze(x0 + dx, y0 + dy, BUNT[(k * 2 + f // 15) % len(BUNT)])
        bild.rechteck(x0 + 4, y0, 2, 1, WEISS if (f // 4) % 2 else GELB)
    elif art == 2:                                                # Kerze: Flamme flackert
        w = (0, 0, 1, 0, -1, 0)[(f // 3) % 6]
        bild.rechteck(cx - 1, y0 - 2, 2, 2, (255, 230, 120))
        bild.setze(cx - 2, y0 - 2, (255, 120, 0))
        bild.setze(cx + 1, y0 - 2, (255, 120, 0))
        bild.setze(cx - 1 + (w > 0), y0 - 3, (255, 170, 0))
        bild.setze(cx - 1 + (w >= 0) - (w < 0), y0 - 4, (255, 90, 0) if w else None)
    elif art == 3:                                                # Glocke: Klöppel
        bild.rechteck(cx - 1 - (0, 2, 0, -2)[(f // 4) % 4], y0 + 9, 2, 2, (255, 225, 110))
    elif art == 6:                                                # Mond: Sternchen
        for k, (dx, dy) in enumerate(((7, 1), (9, 4), (6, 5))):
            bild.setze(x0 + dx, y0 + dy, WEISS if (f // 5 + k) % 3 else dimmen(GELB, 0.5))
    elif art == 7:                                                # Schneemann: Möhre, Augen
        bild.setze(x0 + 6, y0 + 4, (255, 110, 0))
        bild.setze(x0 + 4, y0 + 3, (40, 40, 60))


def fett(bild, x, y, text, farbe, schatten=None):
    """5×7-Schrift, jeder Strich zwei Pixel breit (je Zeichen 6 + 2 Pixel); die Null ohne
    Schrägstrich, sonst läuft sie zu."""
    for z in text:
        glyph = SCHRIFT["O" if z == "0" else z]
        for gy, zeile in enumerate(glyph):
            for gx, c in enumerate(zeile):
                if c == "1":
                    if schatten:
                        bild.setze(x + gx + 2, y + gy + 1, schatten)
        for gy, zeile in enumerate(glyph):
            for gx, c in enumerate(zeile):
                if c == "1":
                    bild.setze(x + gx, y + gy, farbe)
                    bild.setze(x + gx + 1, y + gy, farbe)
        x += 8


def kleine_tuerchen(bild, datum, hell):
    """Acht kleine Türchen; treten sie zurück (hell unter 0,55), verschwinden ihre Zahlen – die
    Ziffern machen jede Spalte anders und kosten in jedem Bild rund 130 Bytes."""
    z = random.Random(datum.toordinal())
    zahlen = z.sample(range(1, 25), 8)
    for i, (x, y) in enumerate(((1, 1), (11, 1), (1, 9), (11, 9), (44, 1), (54, 1), (44, 9), (54, 9))):
        gruen = (i + (i // 2) % 2) % 2 == 0                       # Schachbrett rot/grün
        bild.rechteck(x, y, 9, 6, dimmen((0, 100, 35) if gruen else (150, 10, 25), hell))
        bild.rechteck(x, y, 9, 1, dimmen(RAHMEN, hell))
        if hell > 0.55:
            klein_text(bild, x + (1 if zahlen[i] >= 10 else 3), y + 1, str(zahlen[i]),
                       dimmen((255, 240, 200), hell))


def kalender(bild, datum, t, f):
    n = tage_bis_heiligabend(datum)
    art = datum.toordinal() % 8
    # 0–14 ruhig, 15–29 zittert, 30–45 schwingt auf, danach Motiv
    offen = 0.0 if t < 30 else min(1.0, (t - 30) / 15)
    kleine_tuerchen(bild, datum, 1.0 if t < 30 else max(0.45, 1 - (t - 27) // 3 * 0.2))   # treten zurück
    bild.rechteck(TUER_X - 1, 0, TUER_B + 2, 16, RAHMEN)
    bild.rechteck(TUER_X, 1, TUER_B, 14, INNEN)
    if offen > 0:                                                 # warmes Licht aus dem Türchen
        glanz = min(1.0, (t - 30) / 10) * (0.85 + 0.15 * math.sin(f / 4))
        for x in range(TUER_X, TUER_X + TUER_B):                   # je Spalte eine Farbe, innen heller
            staerke = SCHEIN_INNEN if abs(x - MITTE_X + 0.5) < SCHEIN_BREIT else SCHEIN_AUSSEN
            bild.rechteck(x, 1, 1, 14, mischen(INNEN, (255, 150, 30), round(staerke * glanz * 40) / 40))
    if offen > 0.45:
        motiv(bild, art, MITTE_X, MITTE_Y, f)
    if offen >= 1:                                                # Funken in den Ecken
        for k, (dx, dy) in enumerate(((-8, -5), (7, -4), (-7, 4), (8, 5), (-8, 0), (7, 1))):
            phase = (t // 3 + k * 2) % 6
            if phase < 3:
                bild.setze(MITTE_X + dx, MITTE_Y + dy, (WEISS, GELB, dimmen(GOLD, 0.6))[phase])
    breite = round(TUER_B * (1 - offen))                          # Tür schwingt um die linke Kante
    zittern = (1 if (t // 2) % 2 else 0) if 15 <= t < 30 and t % 8 < 6 else 0
    if breite > 1:
        tuer = mischen(TUER, TUER_DUNKEL, offen * 0.8)
        bild.rechteck(TUER_X + zittern, 1, breite, 14, tuer)
        bild.rechteck(TUER_X + zittern, 1, breite, 1, mischen(TUER_HELL, TUER_DUNKEL, offen * 0.6))
        bild.rechteck(TUER_X + zittern + breite - 1, 1, 1, 14, TUER_HELL if offen else tuer)
        if offen == 0:
            zahl = str(n) if n >= 0 else "24"
            x = TUER_X + (TUER_B - (len(zahl) * 8 - 2)) // 2 + zittern
            fett(bild, x, 4, zahl, GELB if 15 <= t < 30 and (t // 4) % 2 else GOLD,
                 TUER_DUNKEL if len(zahl) < 3 else None)          # dreistellig (ab Januar): ohne Schatten
    else:
        bild.rechteck(TUER_X, 1, 1, 14, TUER_HELL)                # Tür steht offen (Kante)


def bilder(datum=None):
    datum = datum or datetime.date.today()
    text = laufschrift(datum)
    breite = textbreite(text)
    dauer = math.ceil((B + breite) / TEMPO) + 1
    start = 255 - dauer                                           # kurze Texte: Motiv länger
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        SCHNEE.zeichnen(bild, f)
        if f < start:
            kalender(bild, datum, f, f)
        else:
            g = f - start
            x = B - int(g * TEMPO)
            bild.text(x, 4, text,
                      lambda i: GOLD if text[i].isdigit() else regenbogen(i * 23 + f * 1.5))
            for i, sx in enumerate(range(3, B, 8)):               # Lichterreihen oben und unten
                hell = 0.45 + 0.4 * round(2 * math.sin((f + i * 9) / 6)) / 2
                bild.setze(sx, 1, dimmen(GELB, max(0.25, hell)))
                bild.setze(sx + 4, 14, dimmen(GELB, max(0.25, 0.9 - hell)))
        liste.append(bild)
    return liste
