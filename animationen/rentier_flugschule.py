"""Rentier-Flugschule: verschneite Wiese bei Nacht mit Mond, Sternen und ein paar Tannen. Das große
Rentier macht es vor – Anlauf, Absprung, ein eleganter Bogen vor dem Mond, Landung – und schaut
dann zu. Das junge Rentier (kurzes Geweih, Schal) versucht es nach: beim ersten Mal hüpft es nur
und purzelt kopfüber in den Schnee, schüttelt sich; beim zweiten Mal flattert es zappelnd hoch,
bleibt in der Luft stehen und plumpst aufs Hinterteil; beim dritten Mal hebt es ab und fliegt
glücklich eine Schleife bis zum Startplatz. Das große fliegt hinterher, beide stehen wieder am
Anfang – 255 Bilder, die Runde schließt ohne Sprung.

Sparsam gezeichnet (26.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum ebener Boden (alle Spalten gleich), vier Sterne mit
Perioden, die in 255 aufgehen, drei gleiche einfarbige Tannen am Rand der Wiese (Kopien kosten fast
nichts, und die Mitte bleibt frei für die Figuren), kein Schneefall; Schnee stiebt nur kurz in
fünf Punkten, die Glitzerspur hat drei bis sechs Funken.

0–8      beide am Startplatz, das große nickt: „schau gut zu“
8–56     großes Rentier: Anlauf, Absprung, Bogen vor dem Mond, Landung rechts, dreht sich um
60–108   erster Versuch: Anlauf, Hüpfer, Purzelbaum, Kopf im Schnee, aufrappeln, schütteln
108–158  zweiter Versuch: zappelt schaukelnd hoch, hängt kurz in der Luft, plumpst aufs Hinterteil
158–222  dritter Versuch (nach links): hebt ab, Schleife, kleiner Bogen zum Startplatz
192–236  großes Rentier fliegt hinterher und landet auf seinem Platz
238–255  Freudensprünge, das große nickt; beide stehen wie im ersten Bild
"""
import math

from basis import B, GELB, NACHTBLAU, ROT, TUERKIS, WEISS, Bild, dimmen

NAME = "rentier_flugschule"
TITEL = "Rentier-Flugschule"

KANTE = (215, 225, 250)                        # Oberkante der Schneedecke
BODEN = (105, 118, 165)                        # darunter gedämpft
TANNE = (0, 95, 35)
MOND = (240, 230, 170)
STERN = (255, 240, 200)
FELL = (58, 30, 10)                            # großes Rentier (auf den LEDs Braun, am Bildschirm fast schwarz)
FELL_JUNG = (82, 44, 12)                       # junges: etwas heller
LAUF = (33, 16, 5)                             # hintere Läufe
GEWEIH = (225, 190, 130)
AUGE = (200, 200, 220)
GLOCKE = (255, 190, 0)
FUNKE = (255, 190, 40)                         # Glitzerspur beim Fliegen
BODEN_Y = 13                                   # Zeile der Schneekante; die Hufe stehen auf Zeile 12

STERNE = [(7, 2, 60, 85), (17, 0, 0, 51), (27, 4, 20, 85), (56, 1, 34, 51)]   # x, y, Phase, Periode (teilt 255)
TANNEN = (0, 46, 63)                           # Mitte x; alle gleich hoch (Kopien kosten fast nichts)
TANNE_HOCH = 7
MOND_X, MOND_Y = 40, 3

# ── Großes Rentier (Blick nach rechts, 11 breit): a Geweih, h Fell, e Auge, t Schwanz, c Halsband,
#    g Glöckchen, d hintere Läufe
G_OBEN = ["......a.a.a", ".......aaa.", ".......hhh.", ".......hehh", "t......hh..", "thhhhhhcc..",
          ".hhhhhhhg.."]
G_NICKT = ["...........", "......a.a.a", ".......aaa.", ".......hhh.", "t......hehh", "thhhhhhcc..",
           ".hhhhhhhg.."]
G_BEINE = {"stehen": [".h.d..d.h..", ".h.d..d.h..", ".h.d..d.h.."],
           "strecken": [".h.d..d.h..", "h.d....d.h.", "h.d....d.h."],
           "sammeln": [".h.d..d.h..", "..hd..dh...", "...hddh...."]}
# im Flug (13 breit, Rumpf zwei Spalten weiter rechts): Läufe nach hinten und vorn gestreckt
G_FLUG = ["........a.a.a", ".........aaa.", ".........hhh.", "..t......hehh", "..thhhhhhcc..",
          "...hhhhhhhg.."]
G_FLUG_BEINE = ["hhd......dhh.", ".hd......dh.."]
G_FARBEN = {"a": GEWEIH, "h": FELL, "e": AUGE, "t": WEISS, "c": ROT, "g": GLOCKE, "d": LAUF}

# ── Junges Rentier (Blick nach rechts, 8 breit): kurze Geweihstummel, s Schal
J_OBEN = ["....a.a.", "....jjj.", "t...jejj", "tjjjss..", ".jjjjj.."]
J_BEINE = {"stehen": [".jd.dj..", ".jd.dj.."],
           "strecken": [".jd.dj..", "jd...dj."],
           "sammeln": [".jd.dj..", "..jddj.."]}
J_FLUG = [["......a.a.", "......jjj.", "..t..sjejj", "..tjjjss..", "...jjjjj..", "jjd....djj"],
          ["......a.a.", "....s.jjj.", "..t..sjejj", "..tjjjss..", "...jjjjj..", ".jd....dj."]]
J_SCHNEE = ["....awa.", "....jjj.", "t.wwjejj", "tjjjss..", ".jjjjj.."]         # nach dem Purzelbaum
J_SITZT = ["..a.a...", "..jjj...", "..jejj..", "..ss....", ".jjjd...", ".jjj...j", "tjjjjjjj"]   # Läufe nach vorn
J_FARBEN = {"a": GEWEIH, "j": FELL_JUNG, "e": AUGE, "t": WEISS, "s": TUERKIS, "d": LAUF, "w": KANTE}

# ── Ablauf ─────────────────────────────────────────────────────────
GX0, GX1 = 14, 51                              # großes Rentier: Startplatz, Zuschauerplatz rechts
JX0 = 3                                        # junges Rentier: Startplatz
G_ANLAUF, G_AB, G_LANDET, G_DREHT = 8, 20, 50, 56
G_HEIM, G_HEIM_AB, G_HEIM_LANDET, G_HEIM_DREHT = 192, 198, 230, 236
J1, J1_HUPF, J1_ROLLT, J1_LIEGT, J1_AUF = 60, 68, 74, 86, 96        # erster Versuch: Purzelbaum
J2, J2_FLATTERT, J2_FAELLT, J2_SITZT, J2_AUF = 108, 114, 136, 140, 152   # zweiter: aufs Hinterteil
J3, J3_AB, J3_SCHLEIFE, J3_WEITER, J3_LANDET, J3_UM = 158, 164, 170, 198, 216, 222   # dritter: Schleife
FREUDE = 238
FLATTERN = (1, 2, 2, 1, 2, 3, 3, 2, 3, 4, 4, 3, 4, 5, 5, 4)         # Höhe je Bild, danach hängt es oben
HAENGT = 5
X_ROLLT, X_FLATTERT, X_SITZT = 17, 26, 29
SCHLEIFE_MY, SCHLEIFE_RX, SCHLEIFE_RY, SCHLEIFE_DRIFT = 5.5, 4, 3, 2


def gedreht(zeilen, n):
    """Figur n-mal um 90° im Uhrzeigersinn gedreht."""
    for _ in range(n % 4):
        hoch = len(zeilen)
        zeilen = ["".join(zeilen[hoch - 1 - r][c] for r in range(hoch)) for c in range(len(zeilen[0]))]
    return zeilen


def gespiegelt(zeilen):
    return [z[::-1] for z in zeilen]


def gekippt(zeilen, kopf):
    """Figur um ein Pixel gekippt: die vordere Hälfte (ab Spalte 4) sitzt kopf Zeilen tiefer (−1 höher).
    Die Figur wird dabei eine Zeile höher; bei kopf = −1 steht der Rumpf eine Zeile tiefer im Raster."""
    leer = "." * len(zeilen[0])
    hinten = ([leer] + zeilen) if kopf < 0 else (zeilen + [leer])
    vorn = (zeilen + [leer]) if kopf < 0 else ([leer] + zeilen)
    return [h[:4] + v[4:] for h, v in zip(hinten, vorn)]


def stieben(bild, f, start, x):
    """Schnee stiebt am Aufschlag bei Spalte x hoch und fällt wieder: fünf Punkte, zehn Bilder."""
    a = f - start
    if not 0 <= a < 10:
        return
    for vx, vy in ((-1.1, 1.0), (-0.6, 1.5), (0.2, 1.7), (0.7, 1.4), (1.2, 0.9)):
        y = BODEN_Y - 1 - (vy * a - 0.17 * a * a)
        if y <= BODEN_Y - 1:
            bild.setze(x + vx * a, y, KANTE if a < 6 else BODEN)


def spur(bild, f, ort, von, bis, stufen=((3, 1.0), (6, 0.6), (9, 0.35))):
    """Glitzerspur: Funken dort, wo die Figur vor 3, 6, 9 … Bildern war, nach hinten dunkler."""
    for zurueck, hell in stufen:
        g = f - zurueck
        if von <= g < bis:
            x, y = ort(g)
            bild.setze(x, y, dimmen(FUNKE, hell))


# ── Großes Rentier ─────────────────────────────────────────────────
def gross_flug(f, ab, landet, x_von, x_bis):
    """Flugbogen: Ort der Figur (x des stehenden Rentiers, Höhe über dem Boden)."""
    t = (f - ab) / (landet - ab)
    return x_von + (x_bis - x_von) * t, round(4 * math.sin(math.pi * t))


def gross(bild, f):
    nach_links = G_DREHT <= f < G_HEIM_DREHT
    oben, beine, hoch, flug = G_OBEN, "stehen", 0, None
    if f < G_ANLAUF:
        x = GX0
        if 2 <= f < 6:                                               # „schau gut zu“
            oben = G_NICKT
    elif f < G_AB:                                                   # Anlauf im Galopp
        x = GX0 + (f - G_ANLAUF)
        beine = "strecken" if (f // 3) % 2 else "sammeln"
        hoch = beine == "sammeln"
    elif f < G_LANDET:                                               # eleganter Bogen
        x, hoch = gross_flug(f, G_AB, G_LANDET, GX0 + G_AB - G_ANLAUF, GX1 - 3)
        flug = (G_AB, G_LANDET, GX0 + G_AB - G_ANLAUF, GX1 - 3)
    elif f < G_LANDET + 3:                                           # setzt auf, läuft aus
        x = GX1 - 3 + (f - G_LANDET + 1)
        beine = "sammeln" if f == G_LANDET else "strecken"
    elif f < G_HEIM:                                                 # schaut zu
        x = GX1
        if J1_LIEGT + 2 <= f < J1_LIEGT + 8 or J2_SITZT + 4 <= f < J2_SITZT + 10:
            oben = G_NICKT                                           # lässt kurz den Kopf sinken: „oje“
    elif f < G_HEIM_AB:                                              # Anlauf zurück
        x = GX1 - (f - G_HEIM)
        beine = "strecken" if (f // 3) % 2 else "sammeln"
        hoch = beine == "sammeln"
    elif f < G_HEIM_LANDET:                                          # fliegt dem Jungen hinterher
        x, hoch = gross_flug(f, G_HEIM_AB, G_HEIM_LANDET, GX1 - (G_HEIM_AB - G_HEIM), GX0 + 3)
        flug = (G_HEIM_AB, G_HEIM_LANDET, GX1 - (G_HEIM_AB - G_HEIM), GX0 + 3)
    elif f < G_HEIM_LANDET + 3:
        x = GX0 + 3 - (f - G_HEIM_LANDET + 1)
        beine = "sammeln" if f == G_HEIM_LANDET else "strecken"
    else:
        x = GX0
        if FREUDE + 2 <= f < FREUDE + 12 and (f - FREUDE) // 2 % 2:  # nickt zweimal: „gut gemacht“
            oben = G_NICKT
    x = round(x)
    if flug:
        def ort(g):
            gx, gh = gross_flug(g, *flug)
            return (round(gx) + 11 if nach_links else round(gx) - 1), 9 - gh
        spur(bild, f, ort, flug[0], flug[1])
        zeilen = G_FLUG + [G_FLUG_BEINE[(f // 4) % 2]]
        bild.figur(x if nach_links else x - 2, 4 - hoch, zeilen, G_FARBEN, spiegeln=nach_links)
    else:
        zeilen = oben + G_BEINE[beine]
        bild.figur(x, BODEN_Y - len(zeilen) - hoch, zeilen, G_FARBEN, spiegeln=nach_links)


# ── Junges Rentier ─────────────────────────────────────────────────
def schleife(f):
    """Dritter Versuch ab dem Abheben: Mitte der Flugfigur (x, y) und Drehung (Vierteldrehungen)."""
    unten = SCHLEIFE_MY + SCHLEIFE_RY
    x_ab = X_SITZT - (J3_AB - J3) + 4.5
    x_ein = x_ab - (J3_SCHLEIFE - J3_AB) * 0.75
    if f < J3_SCHLEIFE:                                              # hebt ab, streicht flach über den Schnee
        return x_ab - (f - J3_AB) * 0.75, unten, 0
    if f < J3_WEITER:                                                # die Schleife
        t = (f - J3_SCHLEIFE) / (J3_WEITER - J3_SCHLEIFE)
        w = 2 * math.pi * t
        return (x_ein - SCHLEIFE_DRIFT * t - SCHLEIFE_RX * math.sin(w),
                SCHLEIFE_MY + SCHLEIFE_RY * math.cos(w), round(t * 4) % 4)
    t = (f - J3_WEITER) / (J3_LANDET - J3_WEITER)                    # kleiner Bogen bis zum Startplatz
    x_aus = x_ein - SCHLEIFE_DRIFT
    return x_aus + (JX0 + 4.5 - x_aus) * t, unten - round(3 * math.sin(math.pi * t)), 0


def mittig(bild, mx, my, zeilen, farben):
    bild.figur(round(mx - (len(zeilen[0]) - 1) / 2), round(my - (len(zeilen) - 1) / 2), zeilen, farben)


def jung(bild, f):
    """Zeichnet das junge Rentier (die Schneedecke kommt danach darüber und deckt den Kopf im Schnee)."""
    oben, beine, hoch, links, x = J_OBEN, "stehen", 0, False, JX0
    lauf = "strecken" if (f // 2) % 2 else "sammeln"
    if f < J1:                                                       # schaut zu, hüpft vor Aufregung
        if G_LANDET + 2 <= f < G_LANDET + 8:
            hoch = (1, 2, 1, 0, 1, 0)[f - G_LANDET - 2]
    elif f < J1_HUPF:                                                # erster Anlauf
        x, beine, hoch = JX0 + (f - J1), lauf, lauf == "sammeln"
    elif f < J1_ROLLT:                                               # hüpft nur
        x, beine = JX0 + (f - J1), "strecken"
        hoch = (1, 2, 3, 3, 2, 1)[f - J1_HUPF]
    elif f < J1_LIEGT:                                               # purzelt kopfüber durch den Schnee
        i = f - J1_ROLLT
        zeilen = gedreht(J_OBEN + J_BEINE["stehen"], i // 2 + 1)
        mx = X_ROLLT + 3.5 + i * 0.5
        bild.figur(round(mx - (len(zeilen[0]) - 1) / 2), BODEN_Y - len(zeilen), zeilen, J_FARBEN)
        return
    elif f < J1_AUF:                                                 # liegt auf dem Rücken, Kopf im Schnee
        zeilen = gedreht(J_OBEN + J_BEINE["strecken" if (f // 3) % 2 else "stehen"], 2)
        bild.figur(X_ROLLT + 6, BODEN_Y - len(zeilen) + 2, zeilen, J_FARBEN)
        return
    elif f < J2:                                                     # rappelt sich auf und schüttelt sich
        x = X_ROLLT + 6
        if f < J1_AUF + 2:                                           # noch Schnee auf Kopf und Rücken
            oben = J_SCHNEE
        elif f < J1_AUF + 10:                                        # … der beim Schütteln davonfliegt
            a = f - J1_AUF - 2
            x += 1 if f % 2 else -1
            for sx, sy in ((X_ROLLT + 4 - a, 8 + a // 3), (X_ROLLT + 15 + a, 7 + a // 2)):
                bild.setze(sx, sy, KANTE if a < 5 else BODEN)
    elif f < J2_FLATTERT:                                            # zweiter Anlauf
        x, beine, hoch = X_ROLLT + 6 + (f - J2) * 0.5, lauf, lauf == "sammeln"
    elif f < J2_FAELLT:                                              # flattert zappelnd hoch
        i = f - J2_FLATTERT
        x, hoch = X_SITZT, HAENGT                                    # … und merkt es: hängt still in der Luft
        if i < len(FLATTERN):
            x, hoch = X_FLATTERT + (X_SITZT - X_FLATTERT) * i / len(FLATTERN), FLATTERN[i]
            if i % 4 != 1:                                           # zappelt und schaukelt (Nase tief, Nase hoch)
                zeilen = gekippt(J_OBEN + J_BEINE[lauf], -1 if i % 4 in (2, 3) else 1)
                bild.figur(round(x), BODEN_Y - len(zeilen) - hoch + (i % 4 in (2, 3)), zeilen, J_FARBEN)
                return
    elif f < J2_AUF:                                                 # plumpst aufs Hinterteil
        hoch = (4, 3, 1, 0)[f - J2_FAELLT] if f < J2_SITZT else 0
        bild.figur(X_SITZT, BODEN_Y - len(J_SITZT) - hoch, J_SITZT, J_FARBEN)
        if J2_SITZT + 2 <= f < J2_AUF - 1:                           # sieht Sternchen
            w = (f - J2_SITZT) * 0.9
            for k in (0, 1):
                bild.setze(X_SITZT + 3 + 3 * math.cos(w + k * math.pi), 5 + math.sin(w + k * math.pi), GELB)
        return
    elif f < J3:                                                     # steht auf, dreht sich um
        x, links = X_SITZT, f >= J2_AUF + 3
    elif f < J3_AB:                                                  # dritter Anlauf, nach links
        x, beine, links, hoch = X_SITZT - (f - J3), lauf, True, lauf == "sammeln"
    elif f < J3_LANDET:                                              # hebt ab und fliegt die Schleife
        mx, my, n = schleife(f)
        spur(bild, f, lambda g: schleife(g)[:2], J3_AB, J3_LANDET,     # lange Spur: zeichnet die Schleife nach
             ((3, 1.0), (6, 1.0), (9, 0.6), (12, 0.6), (15, 0.35), (18, 0.35)))
        mittig(bild, mx, my, gedreht(gespiegelt(J_FLUG[(f // 3) % 2]), n), J_FARBEN)
        return
    elif f < J3_UM:                                                  # gelandet
        beine, links = "sammeln" if f < J3_LANDET + 2 else "stehen", True
    elif FREUDE <= f < FREUDE + 12:                                  # zwei Freudensprünge
        hoch = (1, 2, 3, 2, 1, 0)[(f - FREUDE) % 6]
        beine = "strecken" if hoch else "stehen"
    zeilen = oben + J_BEINE[beine]
    bild.figur(round(x), BODEN_Y - len(zeilen) - hoch, zeilen, J_FARBEN, spiegeln=links)


def tanne(bild, x):
    """Kleine Tanne am Wiesenrand: einfarbig, alle zwei Zeilen breiter, ein Schneepunkt auf der Spitze."""
    for k in range(TANNE_HOCH):
        halb = min(2, (k + 1) // 2)
        bild.rechteck(x - halb, BODEN_Y - TANNE_HOCH + k, 2 * halb + 1, 1, TANNE)
    bild.setze(x, BODEN_Y - TANNE_HOCH - 1, KANTE)


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        bild.kreis(MOND_X, MOND_Y, 2.2, MOND)
        for x in TANNEN:
            tanne(bild, x)
        gross(bild, f)
        jung(bild, f)
        bild.rechteck(0, BODEN_Y, B, 1, KANTE)                       # Schneedecke (deckt den Kopf im Schnee)
        bild.rechteck(0, BODEN_Y + 1, B, 2, BODEN)
        stieben(bild, f, G_AB, GX0 + G_AB - G_ANLAUF + 1)            # Schnee stiebt beim Absprung …
        stieben(bild, f, G_LANDET, GX1 + 3)                          # … bei der Landung
        stieben(bild, f, J1_ROLLT, X_ROLLT + 5)                      # … beim Purzeln
        stieben(bild, f, J1_LIEGT, X_ROLLT + 9)
        stieben(bild, f, J2_SITZT, X_SITZT + 2)                      # … beim Plumps
        stieben(bild, f, J3_AB, X_SITZT - (J3_AB - J3) + 6)          # … und wenn es endlich klappt
        stieben(bild, f, J3_LANDET, JX0 + 4)
        stieben(bild, f, G_HEIM_AB, GX1 - (G_HEIM_AB - G_HEIM) + 9)
        stieben(bild, f, G_HEIM_LANDET, GX0 + 6)
        liste.append(bild)
    return liste
