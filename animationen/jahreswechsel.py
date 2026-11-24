"""Jahreswechsel (Jahreszahl automatisch, basis.NEUES_JAHR; alle Ziffern, die sich ändern, rollen):
große "2026" steht in vier Fenstern eines Zählwerks, die letzte Walze zuckt zweimal
und rollt dann von 6 auf 7 (rastet mit kleinem Nachschwingen ein), Funken sprühen, "2027" blitzt
auf und leuchtet erst golden im bunten Konfetti, dann läuft ein Regenbogen durch die Ziffern –
255 Bilder.
"""
import colorsys
import math
import random

from basis import NEUES_JAHR, B, BUNT, GELB, GOLD, SCHRIFT, WEISS, Bild, dimmen, mischen
from feuerwerk import jedes_bild_anders

NAME = "jahreswechsel"
NEU = str(NEUES_JAHR)
ALT = str(NEUES_JAHR - 1)
TITEL = f"{ALT} rollt um auf {NEU}"

HINTERGRUND = (8, 0, 20)
WALZE = (30, 14, 54)                            # Fenster des Zählwerks: schwacher Schimmer
HOCH, BREIT = 2, 2
FENSTER_B = 12                                  # Ziffer 10 breit + je 1 Rand
ABSTAND = 14                                    # von Fenster zu Fenster
X0 = (B - (3 * ABSTAND + FENSTER_B)) // 2
Y0 = 1
HOEHE = 16                                      # Weg einer Walze von Ziffer zu Ziffer
# Die Matrix speichert nur 80 KB je Animation und komprimiert jedes Bild einzeln und spaltenweise.
# Darum wechseln Goldschimmer und Regenbogen nur von Strich zu Strich (die Ziffern sind 2 Spalten je
# Strich breit, x // 2) und nicht mehr schräg von Pixel zu Pixel: zwei gleiche Spalten nebeneinander
# kosten fast nichts, der schräge Regenbogen brauchte dagegen 430 Bytes je Bild (frei sind im Mittel 298).

ROLLT = (48, 76)                                # die letzte Walze dreht
BLITZ = 76
BUNT_AB = 150                                   # ab hier Regenbogen statt Gold


def ziffer(bild, x, y, z, farbe, versatz=0):
    """Große Ziffer; versatz verschiebt nach oben (Rollen). farbe: Farbe oder f(x, y)."""
    for gy, zeile in enumerate(SCHRIFT["O" if z == "0" else z]):     # runde Null ohne Schrägstrich
        for gx, c in enumerate(zeile):
            if c == "1":
                for ky in range(HOCH):
                    for kx in range(BREIT):
                        xx, yy = x + gx * BREIT + kx, y + gy * HOCH + ky - versatz
                        bild.setze(xx, yy, farbe(xx, yy) if callable(farbe) else farbe)


def walzen(bild, hell=None):
    """Die vier Fenster; hell = Index eines aufgehellten Fensters."""
    for i in range(4):
        x = X0 + i * ABSTAND
        grund = mischen(WALZE, (70, 40, 90), 1.0) if hell == i else WALZE
        # Die dunkleren Randzeilen oben und unten (Wölbung der Walze) sind entfallen: auf den LEDs kaum
        # zu sehen, im Speicher der Matrix kosteten sie in jeder Fensterspalte zwei Läufe mehr (19 Bytes
        # je Bild, 4,8 KB je Animation). Wieder einbauen: zwei Zeilen in WALZE_RAND = (18, 6, 34).
        bild.rechteck(x, 0, FENSTER_B, 16, grund)


def rollweg(f):
    """Versatz der letzten Walze in Pixeln: zweimal zucken, dann rollen und einrasten."""
    for start, weite in ((26, 2), (37, 3)):
        t = f - start
        if 0 <= t < 6:
            return round(weite * math.sin(math.pi * t / 6))
    if f < ROLLT[0]:
        return 0
    t = (f - ROLLT[0]) / (ROLLT[1] - ROLLT[0])
    if t >= 1:
        k = f - ROLLT[1]                                           # Nachschwingen
        return HOEHE + (1 if k < 2 else (-1 if k < 4 else 0))
    return round(HOEHE * (t * t * (3 - 2 * t)))


def regenbogen_fein(grad):
    r, g, b = colorsys.hsv_to_rgb(int(grad % 360 / 7.5) / 48, 1, 1)
    return (round(r * 255), round(g * 255), round(b * 255))


def bilder():
    z = random.Random(2026)
    konfetti = []
    funken = []
    liste = []
    xl = X0 + 3 * ABSTAND + 1
    for f in range(255):
        bild = Bild(HINTERGRUND)
        rollt = ROLLT[0] <= f < ROLLT[1]
        walzen(bild, hell=3 if rollt else None)

        # ── Konfetti (hinter den Ziffern) ──
        if f == BLITZ:
            for _ in range(30):
                konfetti.append([z.uniform(0, B), z.uniform(-22, 0), z.uniform(0.28, 0.55), z.uniform(0, 6.3),
                                 BUNT[z.randrange(len(BUNT))]])
        if BLITZ < f < BUNT_AB - 28 and f % 4 == 0:
            konfetti.append([z.uniform(0, B), -2.0, z.uniform(0.28, 0.55), z.uniform(0, 6.3),
                             BUNT[z.randrange(len(BUNT))]])
        for k in konfetti:
            x = k[0] + 1.5 * math.sin(k[1] / 3 + k[3])             # taumelt
            quer = int(k[1] / 2 + k[3]) % 2                        # dreht sich: mal hoch, mal quer
            for px, py in ((x, k[1]), (x + (1 if quer else 0), k[1] + (0 if quer else 1))):
                im_fenster = bild.hole(px, py) not in (HINTERGRUND, None)
                bild.setze(px, py, dimmen(k[4], 0.65) if im_fenster else k[4])
            k[1] += k[2]
        konfetti = [k for k in konfetti if k[1] < 17]

        # ── Ziffern ──
        if f < BLITZ:
            glanz = (f - 6) * 3                                    # ein Lichtstreif zieht einmal durch

            def farbe(x, y, glanz=glanz):
                return WEISS if 0 <= x + y - glanz < 3 else GOLD
        elif f < BLITZ + 6:
            farbe = mischen(WEISS, GELB, (f - BLITZ) / 6)
        elif f < BUNT_AB:
            def farbe(x, y, f=f):
                return mischen(GOLD, GELB, round(2 + 2 * math.sin(f / 4 - (x // 2) / 2.5)) / 4)
        else:
            an = min(1.0, (f - BUNT_AB) / 12)                      # Regenbogen wächst von links herein

            def farbe(x, y, f=f, an=an):
                if x > X0 + an * 60:
                    return GELB
                if 0 <= x + y - ((f - BUNT_AB) % 45) * 4 + 20 < 3:    # ab und zu ein Lichtstreif
                    return WEISS
                return regenbogen_fein((x // 2) * 6 - f * 6)
        v = rollweg(f)
        for i, (a, n) in enumerate(zip(ALT, NEU)):
            xi = X0 + i * ABSTAND + 1
            if a == n:                                             # bleibt stehen
                ziffer(bild, xi, Y0, a, farbe)
                continue
            fenster = Bild(None)                                   # rollende Walze: nur im Fenster sichtbar
            ziffer(fenster, xi, Y0, a, farbe, versatz=v)
            ziffer(fenster, xi, Y0 + HOEHE, n, farbe, versatz=v)
            for y in range(16):
                for x in range(xi - 1, xi + FENSTER_B - 1):
                    if fenster.px[y][x] is not None:
                        bild.setze(x, y, fenster.px[y][x])

        # ── Funken beim Einrasten ──
        if f == BLITZ:
            for i in range(18):
                w = i * 2 * math.pi / 18 + z.uniform(-0.1, 0.1)
                funken.append([xl + 5, 8, 1.9 * math.cos(w) * z.uniform(0.6, 1.1), 1.2 * math.sin(w), 0])
        for s in funken:
            hell = 1 - s[4] / 12
            bild.setze(s[0], s[1], dimmen(WEISS if s[4] < 3 else GELB, round(hell * 6) / 6))
            s[0] += s[2]
            s[1] += s[3]
            s[2] *= 0.9
            s[3] = s[3] * 0.9 + 0.05
            s[4] += 1
        funken = [s for s in funken if s[4] < 12]
        liste.append(bild)
    return jedes_bild_anders(liste, HINTERGRUND)
