"""Barbarazweig: Auf der Fensterbank steht eine blaue Vase mit einem dunklen, verzweigten
Kirschzweig, rechts neben der Sprosse brennt eine rote Kerze, draußen vor dem Fenster schneit es
leicht. Die Knospen schwellen an, zeigen Rosa und gehen eine nach der anderen in weiß-rosa Blüten
auf; nach der vollen Blüte lösen sich die Blütenblätter, sinken schaukelnd auf die Fensterbank und
vergehen dort, und am Zweig sitzen neue Knospen wie am Anfang – 255 Bilder. Kein Text.
Die Runde schließt ohne Sprung: Sie beginnt und endet mit dem Zweig voller Knospen, Flocken und
Flamme laufen in ganzen Schwingungen je Runde.

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild
wird einzeln und spaltenweise komprimiert; eine Spalte, die einer früheren gleicht, kostet fast
nichts, jeder Wechsel der Spaltenart etwa 4 Bytes. Darum steigt der Zweig in Stufen aus gleichen
Spalten, die Blüten sitzen mittig auf den Stufen (linke und rechte Blütenspalte gleich), Vase und
Kerze sind spiegelgleich, das Fenster hat oben keinen Balken, der Schnee auf dem äußeren Sims ist
ein durchgehender Streifen, und es fallen nie mehr als sechs Flocken (im Mittel vier).
"""
import math

from basis import B, Bild

NAME = "barbarazweig"
TITEL = "Barbarazweig blüht auf"

RUNDE = 255
NACHT = (0, 5, 34)                             # Fensterglas: Nacht draußen
# Fensterrahmen und Sprosse (große Fläche, gedämpft). Genau dieser Ton: speichern() ändert bei zwei
# gleichen Nachbarbildern das Blau des Pixels oben links um 1; hier bleibt die 16-Bit-Farbe der
# Matrix dabei dieselbe, sonst kostete jedes Standbild etwa 8 Bytes mehr.
RAHMEN = (84, 76, 67)
SPROSSE_X = 45                                 # zwei Spalten breit: links der Zweig, rechts die Kerze
SCHNEE_AUSSEN = (110, 120, 160)                # Schnee auf dem äußeren Sims, Zeile 13
SIMS, SIMS_VORN = (82, 36, 6), (41, 15, 0)     # Fensterbank aus Holz: Oberseite, Vorderkante
FLOCKE = (170, 180, 215)
# Flocken: Spalten (reihum, eine je Durchlauf), Startzeile, Durchläufe je Runde. Die Zahl der
# Durchläufe ist ganz und ein Vielfaches der Spaltenzahl: schließt ohne Sprung. Keine Flocke in
# den ersten Glasspalten 2–5 (dort kostet sie das Doppelte) und keine direkt neben der Kerze.
FLOCKEN = [((6, 33, 18), 5.3, 3), ((40, 11), 9.7, 4), ((47, 60, 57), 3.5, 3),
           ((30, 58, 16, 49), 14.1, 4), ((37, 13, 41), 11.0, 3), ((61, 10, 36), 7.4, 3)]
FALLHOEHE = 18                                 # Zeilen 0–12 sichtbar, danach Pause bis zur nächsten Flocke

VX = 26                                        # Mitte der Vase
VASE, VASE_HELL = (0, 60, 255), (110, 190, 255)
VASE_FORM = [".hhh.",                          # Zeilen 9–13, spiegelgleich
             ".bbb.",
             "bbbbb",
             "bbbbb",
             ".bbb."]

ZWEIG = (82, 33, 4)                            # dunkles Kirschholz (Helligkeitsstufe 10)
ZX = 4                                         # linke Spalte der Zeichnung
# Zeilen 0–8; z Holz, G große Blüte (3×3), K kleine Blüte (Kreuz) – der Buchstabe ist die Mitte
ZWEIG_FORM = ["......................................",
              "........K.....G........G..............",
              "...Gzzz.z.....z........z...K..........",
              ".......zzz....z........z...z...zzzG...",
              "..........zKz.z........z...z.zK.......",
              ".............zzz......z....zz.........",
              "................zKz...z..Kz...........",
              "...................zz.z.z.............",
              ".....................zzz.............."]
# Reihenfolge, in der die Blüten aufgehen (Nummern von links nach rechts) und abblühen
AUF_FOLGE = [4, 7, 1, 9, 2, 6, 3, 8, 0, 5]
KNOSPE, KNOSPE_HELL = (60, 110, 20), (90, 200, 40)
ROSA, BLASS, MITTE = (255, 110, 165), (255, 205, 225), (255, 40, 110)
ROSA_MATT = (120, 50, 76)                      # liegendes Blatt, kurz bevor es vergeht

ZU, PRALL, SPITZE, HALB, OFFEN, KREUZ = range(6)   # Zustände einer Blüte
SCHWELLEN_AB, SPITZE_AB, SCHWELLEN_TAKT = 8, 22, 2   # Knospen schwellen nacheinander an, zeigen dann Rosa
AUF_AB, AUF_TAKT = 44, 11                      # … und gehen nacheinander auf
FALL_AB, FALL_TAKT = 186, 2                    # Blütenblätter lösen sich
FALL_TEMPO = 0.36                              # Zeilen je Bild
LIEGT, BLASST = 12, 4                          # so lange liegt ein Blatt auf der Fensterbank, zuletzt blasser

KX = 54                                        # Mitte der Kerze
KERZE, KERZE_WARM, KERZE_SAUM = (190, 0, 25), (230, 30, 25), (255, 100, 40)   # Rumpf, angestrahlt, Rand
KERN, GELB_F, ORANGE_F = (255, 250, 200), (255, 215, 50), (255, 125, 0)
SIMS_LICHT = (140, 62, 8)                      # Lichtfleck der Kerze auf der Fensterbank


def _blueten():
    """Blüten aus der Zeichnung: (x, y, groß), von links nach rechts."""
    liste = []
    for dy, zeile in enumerate(ZWEIG_FORM):
        for dx, c in enumerate(zeile):
            if c in "GK":
                liste.append((ZX + dx, dy, c == "G"))
    return sorted(liste)


BLUETEN = _blueten()
RANG = {nr: k for k, nr in enumerate(AUF_FOLGE)}                     # Blüte → Platz in der Reihenfolge
# abblühen: die obersten zuerst (sie fallen am längsten)
FALL_RANG = {nr: k for k, nr in enumerate(sorted(range(len(BLUETEN)),
                                                 key=lambda n: (BLUETEN[n][1], RANG[n])))}


def fenster(bild, f):
    """Glas mit Schneestreifen und Flocken, Rahmen links und rechts, Sprosse, Fensterbank."""
    bild.rechteck(0, 13, B, 1, SCHNEE_AUSSEN)
    for spalten, start, runden in FLOCKEN:                           # draußen schneit es leicht
        weg = start + f * runden * FALLHOEHE / RUNDE
        if weg % FALLHOEHE < 13:
            bild.setze(spalten[int(weg // FALLHOEHE) % len(spalten)], int(weg % FALLHOEHE), FLOCKE)
    bild.rechteck(0, 0, 2, 14, RAHMEN)
    bild.rechteck(B - 2, 0, 2, 14, RAHMEN)
    bild.rechteck(SPROSSE_X, 0, 2, 14, RAHMEN)
    bild.rechteck(0, 14, B, 1, SIMS)
    bild.rechteck(0, 15, B, 1, SIMS_VORN)


def kerze(bild, f):
    """Rote Kerze, die Flamme atmet (fünf Atemzüge je Runde) und neigt sich ab und zu; ihr Licht
    liegt als heller Fleck auf der Fensterbank und atmet mit."""
    wiegen = math.sin(2 * math.pi * 6 * f / RUNDE) + 0.6 * math.sin(2 * math.pi * 17 * f / RUNDE + 1)
    neigung = -1 if wiegen < -0.9 else 1 if wiegen > 0.9 else 0
    hoch = math.sin(2 * math.pi * 5 * f / RUNDE) > -0.3
    bild.rechteck(KX - 1, 8, 3, 6, KERZE)
    bild.rechteck(KX - 1, 8, 3, 1, KERZE_SAUM)
    bild.rechteck(KX - 1, 9, 3, 1, KERZE_WARM)
    halb = 4 if hoch else 3
    bild.rechteck(KX - halb, 14, 2 * halb + 1, 1, SIMS_LICHT)
    bild.setze(KX, 7, KERN)
    bild.setze(KX, 6, GELB_F)
    if hoch:
        bild.setze(KX + neigung, 5, ORANGE_F)


def stufe(nr, f):
    """Zustand der Blüte nr im Bild f: ZU (Knospe), PRALL (geschwollen, hellgrün), SPITZE (Rosa
    schaut heraus), HALB (rosa Kreuz), OFFEN, beim Abblühen KREUZ (große Blüte ohne Ecken)."""
    t = f - (FALL_AB + FALL_RANG[nr] * FALL_TAKT)
    if t >= 0:                                                       # alle drei Bilder löst sich ein Blatt
        teile = 3 if BLUETEN[nr][2] else 2
        return ZU if t >= 3 * (teile - 1) else SPITZE if t >= 3 * (teile - 2) else KREUZ
    auf = AUF_AB + RANG[nr] * AUF_TAKT
    if f >= auf + 5:
        return OFFEN
    if f >= auf:
        return HALB
    if f >= SPITZE_AB + RANG[nr] * SCHWELLEN_TAKT:
        return SPITZE
    if f >= SCHWELLEN_AB + RANG[nr] * SCHWELLEN_TAKT:
        return PRALL
    return ZU


def bluete(bild, x, y, gross, s):
    """Blüte im Zustand s; (x, y) ist die Mitte und zugleich der Platz der Knospe am Holz."""
    if s == ZU:
        bild.setze(x, y, KNOSPE)
    elif s in (PRALL, SPITZE):
        bild.setze(x, y, KNOSPE_HELL)
        if s == SPITZE:
            bild.setze(x, y - 1, ROSA)
    else:
        if s == OFFEN and gross:                                     # große Blüte: rosa Ecken
            bild.rechteck(x - 1, y - 1, 3, 3, ROSA)
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            bild.setze(x + dx, y + dy, ROSA if s == HALB else BLASS)
        bild.setze(x, y, MITTE)


def blatt(bild, nr, teil, x, y, f):
    """Ein Blütenblatt der Blüte nr löst sich und sinkt schaukelnd auf die Fensterbank."""
    t = f - (FALL_AB + FALL_RANG[nr] * FALL_TAKT) - teil * 3
    if t < 0:
        return
    x0 = x + (-1, 1, 0)[teil]
    unten = math.ceil((14 - y) / FALL_TEMPO)                         # in diesem Bild landet es
    if t >= unten:                                                   # liegt auf der Fensterbank
        if t < unten + LIEGT:
            bild.setze(x0 + round(math.sin(unten / 5 + nr + teil * 2)), 14,
                       ROSA if t < unten + LIEGT - BLASST else ROSA_MATT)
        return
    bild.setze(x0 + round(math.sin(t / 5 + nr + teil * 2)), int(y + t * FALL_TEMPO),
               BLASS if teil != 1 else ROSA)


def bilder():
    liste = []
    for f in range(RUNDE):
        bild = Bild(NACHT)
        fenster(bild, f)
        for dy, zeile in enumerate(ZWEIG_FORM):                      # Zweig vor dem Fenster
            for dx, c in enumerate(zeile):
                if c != ".":
                    bild.setze(ZX + dx, dy, ZWEIG)
        bild.figur(VX - 2, 9, VASE_FORM, {"b": VASE, "h": VASE_HELL})
        kerze(bild, f)
        for nr, (x, y, gross) in enumerate(BLUETEN):
            bluete(bild, x, y, gross, stufe(nr, f))
        for nr, (x, y, gross) in enumerate(BLUETEN):                 # fallende Blätter vor allem anderen
            for teil in range(3 if gross else 2):                    # große Blüte drei, kleine zwei
                blatt(bild, nr, teil, x, y, f)
        liste.append(bild)
    return liste
