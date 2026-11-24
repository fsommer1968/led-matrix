"""Neujahrsgruß für Silvester kurz vor Mitternacht (Jahreszahl automatisch, basis.NEUES_JAHR;
Datei heißt neujahr_<Jahr>): Feuerwerk ohne Pause, davor groß und fett "ALLES GUTE"
(über die ganze Breite), dann "FÜR" und die Jahreszahl "2027" bildfüllend (erst golden, dann läuft
ein Regenbogen durch); solange Schrift steht, glimmt das Feuerwerk nur gedämpft dahinter, zwischen
den Wörtern und im Finale in voller Helligkeit – 255 Bilder.
"""
import colorsys
import math

from basis import (NEUES_JAHR, B, GELB, GOLD, HELLBLAU, LILA, PINK, ROT, SCHRIFT, TUERKIS, WEISS, Bild, mischen,
                   regenbogen)
from feuerwerk import Feuerwerk, jedes_bild_anders

NAME = f"neujahr_{NEUES_JAHR}"
TITEL = f"ALLES GUTE FÜR {NEUES_JAHR} mit Feuerwerk"

HIMMEL = (0, 0, 12)
ANZAHL = 255

# Ablauf: (von, bis) je Schrift, dazwischen nur Feuerwerk
ALLES_GUTE = (20, 84)
FUER = (98, 130)
JAHR = (140, 226)
JAHR_BUNT = 184                                 # ab hier Regenbogen in der Jahreszahl

# Buchstaben, die fett anders besser lesbar sind: G mit offenem Bauch (sonst wie eine 6), Ü mit eigenen Punkten
FETT = {"G": ["01110", "10001", "10000", "10011", "10001", "10001", "01110"],
        "Ü": ["00000", "00000", "10001", "10001", "10001", "10001", "01110"]}
NULL_GROSS = ["...XXXXXXXXX...", "..XXXXXXXXXXX..", ".XXXX.....XXXX.", "XXX.........XXX", "XXX.........XXX",
              "XXX.........XXX", "XXX.........XXX", "XXX.........XXX", "XXX.........XXX", "XXX.........XXX",
              "XXX.........XXX", ".XXXX.....XXXX.", "..XXXXXXXXXXX..", "...XXXXXXXXX..."]


def fett_text(bild, x, y, text, farbe, wortabstand=3):
    """5×7-Schrift doppelt hoch und einen Pixel fetter (6 breit, 1 Abstand); farbe(i) je Zeichen,
    None = Zeichen noch nicht da. "ALLES GUTE" füllt so genau die 64 Spalten."""
    for i, z in enumerate(text):
        if z == " ":
            x += wortabstand
            continue
        c = farbe(i) if callable(farbe) else farbe
        if c is not None:
            for gy, zeile in enumerate(FETT.get(z, SCHRIFT[z])):
                for gx, p in enumerate(zeile):
                    if p == "1":
                        bild.rechteck(x + gx, y + gy * 2, 2, 2, c)
            if z == "Ü":
                bild.rechteck(x + 1, y, 1, 2, c)
                bild.rechteck(x + 4, y, 1, 2, c)
        x += 7


def jahreszahl(bild, farbe):
    """"2027" bildfüllend: jede Ziffer 15×14 (5×7 mal 3×2), ein Pixel Abstand."""
    for i, z in enumerate(str(NEUES_JAHR)):
        x0 = 1 + i * 16
        zeilen = NULL_GROSS if z == "0" else [
            "".join(c * 3 for c in zeile.replace("1", "X").replace("0", ".")) for zeile in SCHRIFT[z] for _ in (0, 1)]
        for gy, zeile in enumerate(zeilen):
            for gx, c in enumerate(zeile):
                if c == "X":
                    bild.setze(x0 + gx, 1 + gy, farbe(x0 + gx, 1 + gy, i))


def auflegen(bild, schrift, saum):
    """Legt die Schrift über das Bild; mit saum bleibt ringsum ein dunkler Rand."""
    if saum:
        for y in range(16):
            for x in range(B):
                if schrift.px[y][x] is None and any(
                        schrift.hole(x + dx, y + dy) is not None for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    bild.setze(x, y, HIMMEL)
    for y in range(16):
        for x in range(B):
            if schrift.px[y][x] is not None:
                bild.setze(x, y, schrift.px[y][x])


def regenbogen_fein(grad):
    r, g, b = colorsys.hsv_to_rgb(int(grad % 360 / 7.5) / 48, 1, 1)
    return (round(r * 255), round(g * 255), round(b * 255))


def sichtbar(f, von, bis):
    """0..1: Anteil der Schrift, der noch steht – am Ende wird sie in 4 Bildern nach rechts weggewischt."""
    if not von <= f < bis:
        return 0.0
    return min(1.0, (bis - f) / 4)


def wischen(schrift, anteil):
    for y in range(16):
        for x in range(round(B * (1 - anteil))):
            schrift.px[y][x] = None


def bilder():
    farben = (ROT, GOLD, PINK, HELLBLAU, TUERKIS, GELB, LILA)
    arten = ("kugel", "doppel", "ring", "gold", "kugel")
    fw = Feuerwerk(saat=20270101, abstand=(5, 10), start=-5, ende=JAHR[1] - 8, y_bereich=(3, 10), arten=arten,
                   farben=farben)
    finale = Feuerwerk(saat=1, abstand=(2, 5), start=JAHR[1] - 8, ende=ANZAHL - 20, y_bereich=(3, 10), arten=arten,
                       farben=farben)
    liste = []
    for f in range(ANZAHL):
        bild = Bild(HIMMEL)
        # hinter bildfüllender Schrift glimmt das Feuerwerk nur
        voll = max(sichtbar(f, *ALLES_GUTE), sichtbar(f, *JAHR))
        fw.zeichnen(bild, f, boden=15, hell=1 - 0.55 * math.ceil(voll))
        finale.zeichnen(bild, f, boden=15)
        schrift = Bild(None)

        a = sichtbar(f, *ALLES_GUTE)
        if a:
            def farbe(i, a=a):
                t = f - ALLES_GUTE[0] - i
                if t < 0:
                    return None
                return WEISS if t < 2 else mischen(GOLD, (255, 235, 140), round(2 + 2 * math.sin(f / 4 - i * 0.9)) / 4)
            fett_text(schrift, 0, 1, "ALLES GUTE", farbe)

        a = sichtbar(f, *FUER)
        if a:
            def farbe(i, a=a):
                t = f - FUER[0] - i * 2
                if t < 0:
                    return None
                return WEISS if t < 2 else regenbogen(i * 45 + (f // 3) * 15)
            fett_text(schrift, 22, 1, "FÜR", farbe)

        a = sichtbar(f, *JAHR)
        if a:
            t = f - JAHR[0]

            def farbe(x, y, i, a=a, t=t):
                if t < i * 3:                                      # Ziffern schlagen nacheinander auf
                    return None
                # Die Farbe wechselt nur von Strich zu Strich (3 Spalten, das Raster der Ziffern) und nicht
                # mehr schräg von Pixel zu Pixel: Die Matrix komprimiert spaltenweise, gleiche Spalten
                # nebeneinander kosten fast nichts – der schräge Regenbogen brauchte 550 bis 660 Bytes je
                # Bild, im Mittel sind nur 298 frei (80 KB Speicher je Animation).
                strich = (x - 1 - 16 * i) // 3 + 5 * i             # 0 … 19 über alle vier Ziffern
                if t < i * 3 + 2:
                    c = WEISS
                elif f < JAHR_BUNT or x > (f - JAHR_BUNT) * 5:     # golden, der Regenbogen wächst von links herein
                    c = mischen(GOLD, GELB, round(2 + 2 * math.sin(f / 4 - strich / 2)) / 4)
                    if 0 <= x + y - (t - 12) * 4 < 3:              # ein Lichtstreif zieht durch
                        c = WEISS
                else:
                    c = regenbogen_fein(strich * 9 - f * 6)
                return c
            jahreszahl(schrift, farbe)

        for spanne in (ALLES_GUTE, FUER, JAHR):
            a = sichtbar(f, *spanne)
            if 0 < a < 1:
                wischen(schrift, a)
        auflegen(bild, schrift, saum=True)
        liste.append(bild)
    return jedes_bild_anders(liste, HIMMEL)
