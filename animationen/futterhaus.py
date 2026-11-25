"""Futterhaus: verschneites Vogelhaus am Pfahl in der Dämmerung; Blaumeise, Rotkehlchen, Gimpel und
Kohlmeise fliegen an, picken Körner, hüpfen und flattern weiter; Zweige mit Beeren, leiser Schnee.
Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (23.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum Dach in drei breiten Stufen, Zweige aus waagerechten
Stücken, Beeren paarweise, wenige Flocken.
"""
import math

from basis import B, WEISS, Bild, Schnee, dimmen

# Holz-, Fell- und Hauttöne am 25.11.2026 auf die an der Matrix gewählten Töne umgerechnet (vorher leuchteten sie orange)
NAME = "futterhaus"
TITEL = "Vögel am Futterhaus"

HIMMEL = (8, 18, 48)                           # Dämmerung, damit die Vögel leuchten
KANTE = (215, 225, 250)
BODEN = (105, 118, 165)
HOLZ = (58, 34, 14)
HOLZ_DUNKEL = (33, 19, 7)
DACH = (150, 50, 25)
ZWEIG = (41, 26, 12)
BEERE = (255, 0, 30)
KORN = (230, 180, 60)
SCHNEE = Schnee(anzahl=6, saat=951, farbe=(120, 130, 175))   # wenige Flocken: jede kostet in jedem Bild
HX = 31                                        # Mitte des Futterhauses
RUNDE = 255
FLUG = 22                                      # Bilder für An- und Abflug

# Figuren (Blick nach rechts): c Kappe, w Wange, e Auge, k Schnabel, r Rücken/Flügel, b Brust,
# u Bauch, t Schwanz, l Bein
SITZT = ["...ccc.", "...wewk", "trrbbb.", ".rruuu.", "....l.."]
PICKT = ["t.......", ".rrr....", ".rrrccc.", "..uuwewk", "....l..."]
FLIEGT = [["..rr....", "..rrccc.", "trrbwewk", "..uuu...", "........"],
          ["........", "....ccc.", "trrbwewk", "..rru...", "..rr...."]]

AUGE = (15, 15, 40)
SCHNABEL = (215, 170, 70)
ARTEN = {
    "blaumeise": {"c": (30, 110, 255), "w": WEISS, "r": (40, 130, 255), "b": (255, 215, 0),
                  "u": (255, 215, 0), "t": (30, 110, 255)},
    "rotkehlchen": {"c": (160, 100, 45), "w": (255, 85, 0), "r": (160, 100, 45), "b": (255, 85, 0),
                    "u": (225, 205, 175), "t": (120, 75, 35)},
    "gimpel": {"c": (80, 80, 120), "w": (255, 35, 75), "r": (150, 150, 175), "b": (255, 35, 75),
               "u": (255, 35, 75), "t": (80, 80, 115)},
    "kohlmeise": {"c": (35, 45, 120), "w": WEISS, "r": (125, 175, 40), "b": (255, 215, 0),
                  "u": (255, 215, 0), "t": (90, 120, 200)},
}


def vogel(bild, x, fuss_y, pose, art, nach_links):
    farben = {"e": AUGE, "k": SCHNABEL, "l": (190, 120, 70), **ARTEN[art]}
    breite = 8
    zeilen = [z.ljust(breite, ".") for z in pose]
    bild.figur(round(x), round(fuss_y) - 4, zeilen, farben, spiegeln=nach_links)


def _flug(von, nach, a, bremsen):
    """Punkt auf dem Flug von → nach; beim Anflug bremsend, beim Abflug beschleunigend."""
    e = 1 - (1 - a) ** 2 if bremsen else a ** 2
    bogen = -3.0 * math.sin(math.pi * a) * (1 if bremsen else 0.4)   # leichter Bogen nach oben
    return von[0] + (nach[0] - von[0]) * e, von[1] + (nach[1] - von[1]) * e + bogen * (0.5 if bremsen else 1)


def _sitzen(f, takt, versatz):
    """Pose und kleiner Hüpfer beim Sitzen: regelmäßig picken, ab und zu hüpfen."""
    u = (f + versatz) % takt
    if u < 4:
        return PICKT, 0
    if u == takt - 5 or u == takt - 4:
        return SITZT, -1
    return SITZT, 0


# Plan je Vogel: Art, Platz (x, Fuß-y), Blick nach links?, Anflug ab, Abflug ab, woher, wohin, Picktakt
PLAN = [
    ("blaumeise", (16, 9), False, 6, 120, (13, -9), (70, -6), 13),
    ("rotkehlchen", (40, 9), True, 48, 178, (72, 2), (72, 4), 17),
    ("gimpel", (53, 4), True, 100, 232, (72, -6), (-12, -4), 31),
    ("kohlmeise", (2, 5), False, 170, 286, (-12, 12), (72, -5), 23),
]


def voegel(bild, f):
    for i, (art, platz, links, an, ab, woher, wohin, takt) in enumerate(PLAN):
        t = (f - an) % RUNDE
        dauer = ab - an
        if t < FLUG:                                                 # Anflug
            x, y = _flug(woher, platz, t / FLUG, True)
            vogel(bild, x, y, FLIEGT[(f // 2) % 2], art, platz[0] < woher[0])
        elif t < dauer:
            pose, hupf = _sitzen(f, takt, i * 5)
            x, y, blick = platz[0], platz[1], links
            if art == "rotkehlchen" and t >= 92:                     # hüpft hinunter in den Schnee
                s = t - 92
                if s < 9:
                    x, y = _flug(platz, (49, 13), s / 9, True)
                    pose, hupf, blick = FLIEGT[(f // 2) % 2], 0, False
                else:
                    schritt = min((s - 9) // 9, 3)
                    x, y, blick = 49 + schritt * 2, 13, False
                    hupf = -1 if (s - 9) % 9 < 2 and schritt < 3 and s > 9 else 0
                    pose = PICKT if (s - 9) % 9 in (4, 5, 6) else SITZT
            vogel(bild, x, y + hupf, pose, art, blick)
        elif t < dauer + FLUG + 4:                                   # Abflug
            start = platz if art != "rotkehlchen" else (55, 13)
            x, y = _flug(start, wohin, (t - dauer) / (FLUG + 4), False)
            vogel(bild, x, y, FLIEGT[(f // 2) % 2], art, wohin[0] < start[0])


def kulisse(bild):
    bild.rechteck(0, 14, B, 1, KANTE)
    bild.rechteck(0, 15, B, 1, BODEN)
    # Zweige mit Schnee: waagerechte Stücke mit einer Stufe; Beeren paarweise an den Stufen und Enden
    # (gleiche Nachbarspalten kosten beim Komprimieren fast nichts)
    for stuecke, beeren in ((((0, 4, 5), (5, 12, 6)), ((3, 6), (4, 6), (11, 7), (12, 7))),
                            (((50, 58, 5), (59, 63, 4)), ((50, 6), (51, 6), (59, 5), (60, 5)))):
        for x0, x1, y in stuecke:
            bild.rechteck(x0, y - 1, x1 - x0 + 1, 1, KANTE)
            bild.rechteck(x0, y, x1 - x0 + 1, 1, ZWEIG)
        for bx, by in beeren:
            bild.setze(bx, by, BEERE)
    # Futterhaus: Pfahl, Brett, Pfosten, Dach in drei Stufen mit Schneehaube
    bild.rechteck(HX, 11, 1, 3, HOLZ_DUNKEL)
    bild.rechteck(HX - 15, 10, 31, 1, HOLZ)
    bild.rechteck(HX - 5, 6, 1, 4, HOLZ_DUNKEL)
    bild.rechteck(HX + 5, 6, 1, 4, HOLZ_DUNKEL)
    for halb, y, hoch in ((8, 4, 2), (5, 2, 2), (2, 1, 1)):          # Dach y 5 … 1, darauf Schnee
        bild.rechteck(HX - halb, y - 1, 2 * halb + 1, 1, KANTE)
        bild.rechteck(HX - halb, y, 2 * halb + 1, hoch, DACH)
    bild.rechteck(HX - 4, 9, 9, 1, KORN)                             # Körnerhaufen
    bild.rechteck(HX - 2, 8, 5, 1, KORN)
    bild.rechteck(HX - 15, 9, 2, 1, KANTE)                           # Schnee auf den Brettenden
    bild.rechteck(HX + 14, 9, 2, 1, KANTE)
    bild.rechteck(55, 14, 2, 1, dimmen(KORN, 0.8))                   # Körner im Schnee


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(HIMMEL)
        SCHNEE.zeichnen(bild, f)
        kulisse(bild)
        voegel(bild, f)
        liste.append(bild)
    return liste
