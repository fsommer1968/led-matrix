"""Weihnachtspyramide: eine Pyramide aus dem Erzgebirge steht auf der Fensterbank vor dem
Nachthimmel. Vier Kerzen flackern, ihre Wärme treibt oben das Flügelrad, und am Mittelstab drehen
sich zwei Etagen: unten ziehen zwei Hirten und zwei Schafe um die Krippe (die sich auf der Stelle
mitdreht), oben drei Engel mit goldenen Flügeln. Vorn wandern die Figuren nach rechts, hinten
kommen sie als dunkle Schatten zurück. Zwei volle Umdrehungen in 255 Bildern, die Runde geht ohne
Sprung in sich über (Drehung, Flackern und Sterne gehen alle in 255 auf).

Sparsam gezeichnet (24.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum waagerechte Teller und Sockel (gleiche Nachbarspalten),
Figuren drei bis vier Spalten breit mit gleichen Außenspalten, hinten nur einfarbige Schatten,
Flügel als gerade Klötze, schmale Kerzen, die nur alle fünf Bilder flackern, und vier Sterne, von
denen die rechten zwei eine verschobene Kopie der linken sind.
"""
import math

from basis import B, GELB, HAUT, NACHTBLAU, WEISS, Bild, dimmen

NAME = "pyramide"
TITEL = "Weihnachtspyramide dreht sich im Kerzenschein"

RUNDE = 255
UMDREHUNGEN = 2                                # je Runde; alles sitzt auf demselben Stab
CX = 32                                        # Mittelstab

HOLZ = (200, 125, 45)
HOLZ_DUNKEL = (120, 66, 20)
BANK_KANTE = (100, 54, 18)                     # Fensterbank: Oberkante
BANK = (58, 30, 10)                            # … darunter gedämpft (große Fläche)
KNAUF = (230, 30, 20)                          # roter Knauf auf dem Stab
FLUEGEL = (240, 205, 140)                      # helles Holz, hebt sich von den Flammen ab
FLUEGEL_HINTEN = (90, 70, 40)
KERZE = (230, 30, 20)
FLAMME = (255, 215, 60)
SPITZE = (255, 110, 0)
STROH = (230, 180, 40)
STERN = (255, 240, 200)
# Sterne: x, y, Phase, Periode (Teiler von 255). Das rechte Paar ist das linke, um 52 Spalten
# verschoben und im gleichen Takt: So packt die Matrix den rechten Rand als Kopie des linken.
STERNE = [(5, 7, 0, 51), (9, 2, 12, 85), (57, 7, 0, 51), (61, 2, 12, 85)]

RAD_R, RAD_FLUEGEL = 11, 8                     # Flügelrad: Radius, Zahl der Flügel
OBEN_R, OBEN_Y, OBEN_TELLER = 5, 3, 7          # obere Etage: Bahnradius, oberste Zeile, halbe Tellerbreite
UNTEN_R, UNTEN_Y, UNTEN_TELLER = 10, 7, 12     # untere Etage
RAND = 0.3                                     # so nah am Wendepunkt (Kosinus) ist die Figur halb abgedunkelt
KERZEN = [(CX - 18, 0), (CX - 15, 23), (CX + 15, 46), (CX + 18, 18)]  # x, Versatz im Flackern (Schritte)

# Figuren (Blick nach rechts): k Kleid oder Fell (hinten die Farbe des Schattens), h Kopf,
# f Flügel, n Schafskopf
ENGEL = [".h.", "fkf", "kkk"]
HIRTE = [".h.", "kkk", "kkk", "k.k"]
SCHAF = ["....", "kkkn", "kkk.", "k.k."]
OBEN = [(ENGEL, {"k": WEISS, "h": HAUT, "f": GELB}), (ENGEL, {"k": (0, 200, 255), "h": HAUT, "f": GELB}),
        (ENGEL, {"k": (255, 60, 160), "h": HAUT, "f": GELB})]
UNTEN = [(HIRTE, {"k": (0, 190, 60), "h": HAUT}), (SCHAF, {"k": WEISS, "n": (150, 150, 170)}),
         (HIRTE, {"k": (40, 110, 255), "h": HAUT}), (SCHAF, {"k": WEISS, "n": (150, 150, 170)})]
# Krippe mitten auf dem unteren Teller, dreht sich auf der Stelle mit: längs, schräg, von
# der Kopfseite, von der Fußseite (die Gegenrichtungen gespiegelt)
KRIPPE = ["shkks", "bbbbb"]
KRIPPE_SCHRAEG = ["hkk", "bbb"]
KRIPPE_KOPF = ["shs", "bbb"]
KRIPPE_FUSS = ["sks", "bbb"]
KRIPPE_FARBEN = {"s": STROH, "h": HAUT, "k": WEISS, "b": HOLZ_DUNKEL}

# Flackern: je fünf Bilder ein Zustand (0 klein, 1 normal, 2 hell und hoch, 3 neigt sich nach
# rechts, 4 nach links), 51 Schritte = eine Runde; jede Kerze läuft versetzt durch dieselbe Folge
FLACKERN = "112110111311211014110112113110112110411211011131121"
assert len(FLACKERN) * 5 == RUNDE


def funkeln(t, periode):
    """Helligkeit eines Sterns: gut die halbe Periode hell, dann über eine Zwischenstufe dunkler
    und wieder zurück."""
    dunkel_ab = round(periode * 0.6)
    if t < dunkel_ab:
        return 1.0
    return 0.75 if t < dunkel_ab + 3 or t >= periode - 3 else 0.5


def etage(bild, figuren, winkel, radius, y, hinten):
    """Figuren auf ihrer Kreisbahn um den Stab: vorn (hinten=False) bunt und nach rechts, hinten
    gespiegelt als einfarbiger Schatten; an den Wendepunkten eine Zwischenstufe in der Helligkeit.
    Die zweite Spalte der Figur (Körpermitte) sitzt auf der Bahn."""
    for k, (zeilen, farben) in enumerate(figuren):
        w = winkel + 2 * math.pi * k / len(figuren)
        tiefe = math.cos(w)                                          # 1 ganz vorn, -1 ganz hinten
        if (tiefe < 0) != hinten:
            continue
        x = CX + round(radius * math.sin(w))
        if hinten:
            schatten = dimmen(farben["k"], 0.45 if tiefe > -RAND else 0.3)
            bild.figur(x - len(zeilen[0]) + 2, y, zeilen, {c: schatten for c in farben}, spiegeln=True)
        elif tiefe < RAND:
            bild.figur(x - 1, y, zeilen, {c: dimmen(farbe, 0.65) for c, farbe in farben.items()})
        else:
            bild.figur(x - 1, y, zeilen, farben)


def krippe(bild, winkel):
    """Die Krippe steht auf der Drehachse: Der Kopf des Kindes kommt von links nach vorn und
    wandert nach rechts, dann die Fußseite."""
    laengs, quer = math.cos(winkel), math.sin(winkel)
    if abs(laengs) >= 0.75:
        zeilen = KRIPPE
    elif abs(laengs) >= 0.3:
        zeilen = KRIPPE_SCHRAEG
    else:
        zeilen = KRIPPE_KOPF if quer > 0 else KRIPPE_FUSS
    bild.figur(CX - len(zeilen[0]) // 2, 9, zeilen, KRIPPE_FARBEN, spiegeln=laengs < 0)


def bilder():
    liste = []
    for f in range(RUNDE):
        winkel = 2 * math.pi * UMDREHUNGEN * f / RUNDE
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, funkeln((f + phase) % periode, periode)))
        bild.rechteck(0, 14, B, 1, BANK_KANTE)                       # Fensterbank
        bild.rechteck(0, 15, B, 1, BANK)
        # hinten: Figuren als Schatten, hintere Flügel
        etage(bild, OBEN, winkel, OBEN_R, OBEN_Y, hinten=True)
        etage(bild, UNTEN, winkel, UNTEN_R, UNTEN_Y, hinten=True)
        for k in range(RAD_FLUEGEL):
            w = winkel + 2 * math.pi * k / RAD_FLUEGEL
            if math.cos(w) < 0:
                bild.rechteck(CX + round(RAD_R * math.sin(w)), 0, 1, 2, FLUEGEL_HINTEN)
        # Gestell: Stab, Teller, Sockel
        bild.rechteck(CX, 0, 1, 13, HOLZ)
        bild.setze(CX, 0, KNAUF)
        bild.rechteck(CX - OBEN_TELLER, OBEN_Y + 3, 2 * OBEN_TELLER + 1, 1, HOLZ)
        bild.rechteck(CX - UNTEN_TELLER, UNTEN_Y + 4, 2 * UNTEN_TELLER + 1, 1, HOLZ)
        bild.rechteck(CX - 19, 13, 39, 1, HOLZ)
        krippe(bild, winkel)
        # vorn: Figuren, vordere Flügel
        etage(bild, OBEN, winkel, OBEN_R, OBEN_Y, hinten=False)
        etage(bild, UNTEN, winkel, UNTEN_R, UNTEN_Y, hinten=False)
        for k in range(RAD_FLUEGEL):
            w = winkel + 2 * math.pi * k / RAD_FLUEGEL
            if math.cos(w) >= 0:
                x = CX + round(RAD_R * math.sin(w))
                bild.rechteck(x, 0, 2 if math.cos(w) > 0.5 else 1, 2, FLUEGEL)
        # Kerzen
        for x, versatz in KERZEN:
            zustand = FLACKERN[(f // 5 + versatz) % len(FLACKERN)]
            bild.rechteck(x, 10, 1, 3, KERZE)
            bild.setze(x, 9, FLAMME)
            if zustand != "0":
                bild.setze(x + {"3": 1, "4": -1}.get(zustand, 0), 8, FLAMME if zustand == "2" else SPITZE)
        liste.append(bild)
    return liste
