"""Schneeflocken: vier große Eiskristalle wachsen von der Mitte aus (erst die Arme, dann die
Seitenäste), drehen sich in kleinen Schritten, schmelzen und wachsen in neuer Form und Farbe
nach; ein Glitzerschein wandert über die Kristalle, im Hintergrund rieselt feiner Schnee –
255 Bilder, läuft nahtlos im Kreis.

Die Kristalle sind scharf gezeichnet (ein Punkt ist an oder aus) und drehen sich in Schritten
von 15°: Die Matrix speichert je Animation nur 80 KB (Ziel ≤ 76000 Bytes, siehe groesse.py),
jedes Bild wird einzeln gepackt, und geglättete Kanten mit ihren vielen Helligkeitsstufen
brauchten gut das Doppelte. Scharfe Punkte flimmern bei stufenweiser Drehung auch nicht.
"""
import math

from basis import (B, H, HELLBLAU, WEISS, Bild, Schnee, dimmen, mischen)

NAME = "schneeflocken"
TITEL = "Wachsende, drehende Eiskristalle"

HINTERGRUND = (0, 3, 26)
FARBEN = [HELLBLAU, (150, 170, 255), (0, 255, 190), (200, 120, 255), (120, 255, 255), (90, 140, 255)]
KLEIN = Schnee(anzahl=6, saat=101, farbe=(60, 70, 120))
PERIODE = 127.5                                  # Leben eines Kristalls; zwei je Durchlauf
# Platz: Mitte x, Mitte y (ganze Punkte, dann sind die Kristalle spiegelgleich), Radius, Start,
# Drehsinn
PLAETZE = [(8, 8, 7, 0, 1), (24, 7, 6, 96, -1), (40, 8, 7, 32, 1), (56, 8, 6, 64, -1)]
# Form: Äste als (Ansatz, Länge) in Anteilen des Radius; Sechseck-Ring (Anteil oder None)
FORMEN = [
    {"aeste": [(0.50, 0.32), (0.80, 0.15)], "ring": None},
    {"aeste": [(0.74, 0.24)], "ring": 0.38},
    {"aeste": [(0.36, 0.18), (0.66, 0.27)], "ring": None},
    {"aeste": [(0.60, 0.32)], "ring": 0.20},
]
COS30, SIN30 = math.cos(math.pi / 6), 0.5
SECHSTEL = math.pi / 3
SCHRITT = math.pi / 12                           # Drehung in Schritten von 15°
# Takt über 16 Bilder: In den spiegelgleichen Lagen (0° und 30°) steht der Kristall je sechs
# Bilder, die schiefen Zwischenlagen (teurer) dauern nur je zwei.
TAKT = (0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3)


def _abstand(u, v, x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    l2 = dx * dx + dy * dy
    t = 0 if l2 == 0 else max(0, min(1, ((u - x0) * dx + (v - y0) * dy) / l2))
    return math.hypot(u - x0 - t * dx, v - y0 - t * dy)


def kristall(bild, cx, cy, radius, winkel, form, wuchs, farbe, kraft, glanz_x):
    """wuchs 0…1: erst wachsen die Arme, dann die Äste. kraft 0…1: Helligkeit (Schmelzen)."""
    arm = radius * min(1, wuchs / 0.6)
    aeste = []
    for ansatz, laenge in form["aeste"]:
        if arm > ansatz * radius:
            l = laenge * radius * max(0, min(1, (wuchs - 0.35) / 0.65)) + 0.01
            aeste.append((ansatz * radius, l))
    ring = form["ring"] * radius if form["ring"] and arm > form["ring"] * radius else None
    farbe = dimmen(farbe, kraft)
    mitte = dimmen(WEISS, kraft)
    glanz = mischen(farbe, mitte, 0.7)
    for y in range(max(0, cy - radius), min(H, cy + radius + 1)):
        for x in range(max(0, cx - radius), min(B, cx + radius + 1)):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy)
            if r > arm + 0.5:
                continue
            w = (math.atan2(dy, dx) - winkel) % SECHSTEL          # in einen 30°-Keil falten
            if w > SECHSTEL / 2:
                w = SECHSTEL - w
            u, v = r * math.cos(w), r * math.sin(w)
            d = _abstand(u, v, 0, 0, arm, 0)
            for ansatz, l in aeste:
                d = min(d, _abstand(u, v, ansatz, 0, ansatz + l * 0.5, l * 0.866))
            if ring:
                d = min(d, abs(u * COS30 + v * SIN30 - ring * COS30))
            if d > 0.5:
                continue
            if r < 0.9:
                bild.setze(x, y, mitte)
            else:
                bild.setze(x, y, glanz if abs(x - glanz_x) < 2.5 else farbe)   # Glitzerschein


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HINTERGRUND)
        KLEIN.zeichnen(bild, f)
        glanz_x = (f * 1.0) % 127.5 - 30
        for i, (cx, cy, radius, start, sinn) in enumerate(PLAETZE):
            t = (f - start) % PERIODE
            runde = int((f - start) % 255 // PERIODE)
            if t < 34:
                wuchs, kraft = t / 34, 1.0                          # wachsen
            elif t < 97:
                wuchs, kraft = 1.0, 1.0
            elif t < 115:
                wuchs = 1 - 0.45 * (t - 97) / 18                  # schmelzen
                kraft = 1 - round((t - 97) / 18 * 4) / 5
            else:
                continue
            winkel = sinn * (4 * (f // 16) + TAKT[f % 16]) * SCHRITT
            kristall(bild, cx, cy, radius, winkel, FORMEN[(i + runde * 2) % len(FORMEN)], wuchs,
                     FARBEN[(i * 2 + runde * 3) % len(FARBEN)], kraft, glanz_x)
        liste.append(bild)
    return liste
