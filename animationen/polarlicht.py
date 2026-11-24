"""Polarlicht: wogende Nordlicht-Vorhänge über verschneiten Bergen und einer Hütte – 255 Bilder.

Grün–Türkis–Violett, die Strahlen-Vorhänge wandern und pulsieren (nahtlos über 255 Bilder),
der Schnee spiegelt das Licht; Sterne funkeln, Sternschnuppen; in der Hütte brennt Licht,
aus dem Kamin steigt Rauch.

Die Matrix speichert nur 80 KB je Animation und packt jedes Bild einzeln, Spalte für Spalte:
gleiche Nachbarspalten kosten fast nichts, jede Abweichung rund 4 Bytes. Darum ist alles in
ein festes Raster gesetzt: der Vorhang besteht aus Strahlen von RASTER Spalten Breite mit
wenigen klaren Farben (keine Verläufe), die Berge steigen in Stufen im selben Raster, das
Schneefeld hat in allen Spalten dieselbe Farbe und pulsiert als Ganzes mit dem Licht.
"""
import math

from basis import B, GRAU, NACHTBLAU, SCHNEEDECKE, Bild, dimmen, mischen, sternschnuppe

NAME = "polarlicht"
TITEL = "Polarlicht über Bergen und Hütte"

RASTER = 4                              # Breite eines Strahls / einer Bergstufe in Spalten
GRUPPEN = B // RASTER
GRUENLICHT = (40, 255, 110)
TUERKISLICHT = (0, 220, 230)
VIOLETT = (200, 40, 255)
BERG = (30, 36, 70)
BERG_HELL = (48, 56, 100)
GIPFEL = (150, 165, 215)
SCHNEEFELD = (70, 80, 125)
TANNE = (0, 85, 40)
STERNLICHT = (255, 240, 200)
STERNE = [(2, 1, 0, 24), (13, 0, 9, 32), (22, 2, 17, 40), (38, 1, 22, 32), (50, 0, 13, 40),
          (58, 2, 30, 24)]              # x, y, Phase, Periode
# oberste Zeile des Berges je Gruppe (13 = kein Berg); Gipfel bei Gruppe 2 und 10
BERG_OBEN = [10, 8, 6, 8, 10, 10, 11, 13, 10, 7, 5, 7, 9, 9, 9, 8]
BERG_GIPFEL = (2, 10)
HX = 25                                 # Hütte: linke Dachkante
TANNEN = (6, 56)                        # linke Spalte je Tanne (am Rand einer Rastergruppe)


def strahl(g, w):
    """Ein Strahl des Vorhangs: (Unterkante, Höhe, Stärke 0–2, Farbe); w = 2π·f/255 (nahtlos)."""
    unten = 5.2 + 1.5 * math.sin(g * 0.55 + 2 * w) + 1.0 * math.sin(g * 1.3 - 3 * w + 1.0)
    huelle = 0.5 + 0.5 * math.sin(g * 0.45 - 2 * w + 0.6) + 0.25 * math.sin(4 * w + g * 0.2)
    hoehe = 4 + round(3 * (0.5 + 0.5 * math.sin(g * 1.9 + 5 * w)))
    staerke = 0 if huelle < 0.12 else 1 if huelle < 0.55 else 2
    farbe = GRUENLICHT if math.sin(g * 0.4 + 2 * w + 2.0) > -0.2 else TUERKISLICHT
    return round(unten), hoehe, staerke, farbe


def vorhang(bild, f):
    """Strahlen: unten hell, darüber gedämpft, oben ein violetter Saum."""
    w = 2 * math.pi * f / 255
    for g in range(GRUPPEN):
        unten, hoehe, staerke, farbe = strahl(g, w)
        if not staerke:
            continue
        for y in range(max(0, unten - hoehe + 1), unten + 1):
            if y < unten - 2:                                    # Saum: je Strahl verschieden hoch
                c = dimmen(VIOLETT, 0.55 if staerke == 2 else 0.35)
            elif y >= unten - (staerke - 1):
                c = farbe if staerke == 2 else dimmen(farbe, 0.55)
            else:
                c = dimmen(farbe, 0.55 if staerke == 2 else 0.3)
            bild.rechteck(g * RASTER, y, RASTER, 1, c)


def widerschein():
    """Farbe des Schneefelds je Bild: SCHNEEFELD, getönt mit dem Licht darüber. Stärke und
    Grün-Anteil des Vorhangs sind über 13 Bilder gemittelt und grob gestuft, damit das Feld
    ruhig von Grün nach Türkis wandert statt zu flackern (eine Farbe für alle Spalten)."""
    roh = []
    for f in range(255):
        strahlen = [strahl(g, 2 * math.pi * f / 255) for g in range(GRUPPEN)]
        summe = sum(s[2] for s in strahlen)
        gruen = sum(s[2] for s in strahlen if s[3] == GRUENLICHT)
        roh.append((summe / (2 * GRUPPEN), gruen / max(1, summe)))
    farben = []
    for f in range(255):
        fenster = [roh[(f + d) % 255] for d in range(-6, 7)]
        staerke = sum(r[0] for r in fenster) / len(fenster)
        anteil = sum(r[1] for r in fenster) / len(fenster)
        licht = mischen(TUERKISLICHT, GRUENLICHT, round(anteil * 4) / 4)
        farben.append(mischen(SCHNEEFELD, licht, 0.2 + 0.2 * round(min(1.0, staerke * 1.6) * 2) / 2))
    return farben


def sterne(bild, f):
    for x, y, phase, periode in STERNE:
        v = 0.5 + 0.5 * math.cos(2 * math.pi * (f + phase) / periode)
        if v > 0.4 and bild.hole(x, y) == NACHTBLAU:
            bild.setze(x, y, dimmen(STERNLICHT, 0.5 if v < 0.6 else 0.75 if v < 0.85 else 1.0))


def landschaft(bild, f, feld):
    for g, oben in enumerate(BERG_OBEN):                         # Berge in Stufen, Schneekuppen
        links = any(g < gipfel and gipfel - g < 5 for gipfel in BERG_GIPFEL) and g not in BERG_GIPFEL
        for y in range(oben, 13):
            kuppe = y < oben + (2 if g in BERG_GIPFEL else 1) and oben < 9
            bild.rechteck(g * RASTER, y, RASTER, 1, GIPFEL if kuppe else BERG_HELL if links else BERG)
    bild.rechteck(0, 13, B, 1, mischen(feld, SCHNEEDECKE, 0.35))  # Schneefeld spiegelt das Licht
    bild.rechteck(0, 14, B, 2, feld)
    for tx in TANNEN:                                            # Tannen: 2 breit, Schnee auf der Spitze
        bild.rechteck(tx, 10, 2, 3, TANNE)
        bild.rechteck(tx, 9, 2, 1, GIPFEL)
    huette(bild, f)


def huette(bild, f):
    bild.rechteck(HX + 7, 7, 2, 3, (110, 45, 30))                # Kamin mit Schneehaube
    bild.rechteck(HX + 7, 7, 2, 1, SCHNEEDECKE)
    t = (f * 2 // 3) % 16                                        # Rauch
    if t < 9:
        bild.setze(HX + 7 + (t // 3) % 2, 6 - t // 3, dimmen(GRAU, 1 - t // 3 * 0.25))
    bild.rechteck(HX + 1, 11, 9, 4, (105, 55, 22))               # Wand
    bild.rechteck(HX, 10, 11, 1, (150, 50, 35))                  # Dach mit Schnee
    bild.rechteck(HX + 1, 8, 9, 2, SCHNEEDECKE)
    bild.rechteck(HX + 7, 8, 2, 1, (110, 45, 30))
    flackern = (f // 9) % 7 == 0
    licht = (255, 160, 40) if flackern else (255, 195, 60)
    bild.rechteck(HX + 2, 12, 3, 2, licht)                       # Fenster
    bild.rechteck(HX + 7, 12, 2, 3, (60, 28, 10))                # Tür


def bilder():
    liste = []
    felder = widerschein()
    for f in range(255):
        bild = Bild(NACHTBLAU)
        vorhang(bild, f)
        sterne(bild, f)
        sternschnuppe(bild, f, 40, 50, 0)
        sternschnuppe(bild, f, 170, 25, 1)
        landschaft(bild, f, felder[f])
        liste.append(bild)
    return liste
