"""Schneemann bauen: Zwei Kinder rollen im verschneiten Garten Schneekugeln, die beim Rollen
wachsen, und setzen sie aufeinander (groß, mittel, klein). Dann bekommt der Schneemann Kohleaugen,
Knöpfe, Karottennase, Hut, Schal und Besen; die Kinder hüpfen vor Freude, der Schneemann zwinkert
und winkt. Zum Schluss laufen die Kinder weg, die Sonne strahlt und der Schneemann schmilzt zu
einem Häufchen, das vergeht – die Runde geht ohne Sprung in sich über. Kein Text – 255 Bilder.

0–42    Kind A rollt die große Kugel von links in die Mitte, Kind B die mittlere von rechts
46–57   B hebt die mittlere Kugel auf die große; A läuft nach links und rollt den Kopf (67–91)
91–102  A hebt den Kopf hinauf; B holt inzwischen den Hut (wirft ihn 106–115)
108–157 A setzt Augen und Knöpfe und wirft Karotte und Schal hinüber; B holt den Besen (da 168)
172–208 beide hüpfen mit erhobenen Armen, der Schneemann zwinkert zweimal und winkt
208–232 die Kinder laufen hinaus; ab 212 strahlt die Sonne, 220–247 schmilzt der Schneemann,
        bis 252 vergeht das Häufchen

Sparsam gezeichnet: Die Matrix speichert nur 80 KB je Animation, jedes Bild wird einzeln und
spaltenweise komprimiert. Darum Himmel und Wiese als waagerechte Bänder (alle Spalten gleich),
ein Zaun im festen Sechsertakt, Kinder drei Spalten breit, eine schlanke Tanne, kein Schneefall,
keine Sterne.
"""
import math

from basis import B, GELB, GOLD, HAUT, ORANGE, PINK, ROT, Bild

NAME = "schneemann_bauen"
TITEL = "Kinder bauen einen Schneemann"

HIMMEL = (5, 32, 90)                           # Tag, gedämpft (große Fläche)
KANTE = (125, 140, 195)                        # Horizont: Schneekante, deutlich dunkler als die Kugeln
WIESE = (78, 90, 140)                          # verschneite Wiese, gedämpft (große Fläche)
KUGEL = (235, 240, 255)
SCHATTEN = (150, 165, 215)                     # Schattenseite der Kugeln, geschlossenes Auge
KOHLE = (0, 0, 0)
SONNE = (255, 200, 0)
SONNE_HELL = (255, 235, 90)                    # wenn sie strahlt
STRAHL = (255, 170, 0)
TANNE = (0, 95, 35)
ZAUN = (110, 60, 20)
HUT = (130, 40, 255)
HOLZ = (170, 90, 30)
STROH = (255, 190, 40)
HOSE = (120, 80, 45)
AUGE = (50, 25, 10)

HORIZONT = 10                                  # Zeile der Schneekante; darunter Wiese
FUSS = 14                                      # unterste Zeile der Figuren und Kugeln
CX = 31                                        # Mitte des Schneemanns
SONNE_X, SONNE_Y = 7, 2
TANNE_X = 57

KIND_A = {"m": ROT, "j": (0, 110, 255), "g": GELB, "h": HAUT, "a": AUGE, "b": HOSE}
KIND_B = {"m": PINK, "j": (0, 190, 70), "g": (255, 120, 0), "h": HAUT, "a": AUGE, "b": HOSE}

# Kinder (Blick nach rechts), 7 breit, Rumpf in den Spalten 2–4; m Mütze, h Gesicht, a Auge,
# j Jacke, g Handschuh. Darunter kommen zwei Zeilen Beine (b).
_KOPF = ["..mmm..", "..mmm..", "..hha..", "..hhh.."]
_VOR = ["...mmm.", "...mmm.", "...hha.", "...hhh."]                    # vorgebeugt beim Schieben
POSEN = {
    "steht": _KOPF + ["..jjj..", "..jjj..", "..jjj.."],
    "schiebt": _VOR + ["...jjjg", "..jjj..", "..jjj.."],            # Hände oben an der großen Kugel
    "schiebt_tief": _VOR + ["...jjj.", "..jjjjg", "..jjj.."],       # Hände unten an der kleinen
    "jubel": ["g.mmm.g", ".jmmmj.", "..hha..", "..hhh..", "..jjj..", "..jjj..", "..jjj.."],
    "reicht": ["..mmm.g", "..mmmj.", "..hha..", "..hhh..", "..jjj..", "..jjj..", "..jjj.."],
    "traegt": _KOPF + ["..jjj..", "..jjjg.", "..jjj.."],            # hält den Besenstiel vor sich
}
BEINE = [["..bbb..", "..b.b.."], ["..bbb..", "...b..."]]

# Kugeln wachsen beim Rollen: (Breite, Höhe) in Stufen bis zur fertigen Größe
GROSS = [(2, 2), (3, 2), (4, 3), (5, 3), (6, 4), (7, 4), (8, 5), (9, 5)]
MITTEL = [(2, 2), (3, 2), (4, 2), (5, 3), (6, 3), (7, 3)]
KLEIN = [(2, 2), (3, 2), (4, 3), (5, 4)]
# fertig abgelegt, mit Schattenseite rechts unten (w Schnee, s Schatten)
BASIS = [".wwwwwww.", "wwwwwwwws", "wwwwwwwws", "wwwwwwwss", ".wwwwsss."]
MITTE = [".wwwww.", "wwwwwws", ".wwwss."]
KOPF = [".www.", "wwwww", "wwwws", ".wws."]
SCHNEE = {"w": KUGEL, "s": SCHATTEN}

# ── Ablauf (Bildnummern) ───────────────────────────────────────────
A_DA = 42                                      # große Kugel liegt in der Mitte
B_START, B_DA = 4, 44                          # mittlere Kugel liegt rechts daneben
MITTE_HOCH, MITTE_DA = 46, 57                  # B hebt sie hinauf
A_ZURUECK, A_HOCKT, A_ROLLT, A_KOPF = 46, 63, 67, 91     # A läuft nach links, formt und rollt den Kopf
KOPF_DA = 102                                  # Kopf sitzt
B_WEG1, B_HUT, B_WURF, HUT_DA = 59, 82, 106, 115         # B holt den Hut und wirft ihn hinauf
AUGE1, AUGE2, KNOEPFE = 108, 116, 123
NASE_WURF, NASE_DA = 128, 136
SCHAL_WURF, SCHAL_DA = 148, 157
A_REICHT = (AUGE1, AUGE2, KNOEPFE, NASE_WURF, SCHAL_WURF)            # dazu streckt A jeweils kurz den Arm hoch
B_WEG2, B_BESEN, BESEN_DA = 116, 140, 168                # B holt den Besen und steckt ihn in den Schnee
JUBEL, ABGANG = 172, 208
ZWINKERN = ((180, 187), (196, 203))
STRAHLEN = 212
SCHMILZT, WEG, LEER = 220, 247, 252            # sinkt zusammen; danach vergeht das Häufchen

A_STEHT_X, B_STEHT_X = 19, 42                  # hier stehen die Kinder beim Schmücken und Jubeln


def kugel(bild, x, b, h, weg):
    """Rollende Schneekugel: linke Spalte x, b breit, h hoch; ab drei Zeilen runde Ecken. Ein
    Schattenfleck wandert mit dem Weg im Kreis (sie rollt)."""
    for k in range(h):
        rund = 1 if (h >= 3 and k in (0, h - 1)) or (b >= 4 and k == 0) else 0
        bild.rechteck(x + rund, FUSS - h + 1 + k, b - 2 * rund, 1, KUGEL)
    if b >= 4:
        w = weg / (b / 2)
        bild.setze(x + (b - 1) / 2 + (b / 2 - 1.5) * math.cos(w),
                   FUSS - (h - 1) / 2 + (h / 2 - 1.2) * math.sin(w), SCHATTEN)


def teil(bild, zeilen, x, unten=FUSS):
    """Fertige Kugel (BASIS, MITTE, KOPF): linke Spalte x, unterste Zeile `unten`."""
    bild.figur(x, unten - len(zeilen) + 1, zeilen, SCHNEE)


def bogen(t, von, nach, hoch):
    """Wurf im Bogen: Punkt zum Anteil t (0 … 1) zwischen von und nach, um `hoch` überhöht."""
    t = max(0.0, min(1.0, t))
    return (round(von[0] + (nach[0] - von[0]) * t),
            round(von[1] + (nach[1] - von[1]) * t - hoch * math.sin(math.pi * t)))


def hut(bild, x, y):
    """Hut: linke Spalte der Krempe x, oberste Zeile y."""
    bild.rechteck(x + 1, y, 3, 1, HUT)
    bild.rechteck(x + 1, y + 1, 3, 1, GOLD)                          # Hutband
    bild.rechteck(x, y + 2, 5, 1, HUT)


def besen(bild, x, unten=FUSS):
    """Besen, Borsten nach oben: Stiel in Spalte x."""
    bild.rechteck(x, unten - 8, 1, 9, HOLZ)
    bild.rechteck(x - 1, unten - 10, 3, 2, STROH)
    bild.setze(x - 1, unten - 11, STROH)                             # Borsten stehen oben auseinander
    bild.setze(x + 1, unten - 11, STROH)


def tanne(bild, x, hoehe):
    """Schlanke Tanne hinter dem Zaun: alle drei Zeilen eine Stufe breiter (höchstens fünf
    Spalten, jede Spalte ein Stück – das packt sich gut), Schneehaube."""
    for k in range(hoehe):
        halb = min(2, (k + 1) // 3)
        bild.rechteck(x - halb, HORIZONT - hoehe + k, 2 * halb + 1, 1, TANNE)
    bild.setze(x, HORIZONT - hoehe - 1, KANTE)


def garten():
    """Hintergrund: Himmel, Tanne, Gartenzaun am Horizont, verschneite Wiese."""
    bild = Bild(HIMMEL)
    tanne(bild, TANNE_X, 8)
    bild.rechteck(0, HORIZONT - 1, B, 1, ZAUN)                       # Zaunlatte …
    for x in range(2, B, 6):                                         # … und Pfosten im Sechsertakt
        bild.setze(x, HORIZONT - 2, ZAUN)
    bild.rechteck(0, HORIZONT, B, 1, KANTE)
    bild.rechteck(0, HORIZONT + 1, B, 16 - HORIZONT - 1, WIESE)
    return bild


def huepfer(t):
    """Hüpfen beim Jubeln: acht Bilder in der Luft (bis zwei Pixel hoch), vier am Boden."""
    return round(2 * math.sin(math.pi * (t % 12) / 8)) if t >= 0 and t % 12 < 8 else 0


def kind(bild, kx, pose, farben, schritt=0, links=False, dy=0):
    """Kind mit Rumpf in den Spalten kx … kx+2; dy < 0 hüpft, dy > 0 hockt (Beine im Schnee)."""
    zeilen = POSEN[pose] + BEINE[schritt]
    if dy > 0:
        zeilen = zeilen[:len(zeilen) - dy]
    bild.figur(kx - 2, FUSS - 8 + dy, zeilen, farben, spiegeln=links)


def schneemann(f):
    """Der Schneemann, so weit er im Bild f fertig ist, auf einer eigenen Ebene (zum Schmelzen)."""
    e = Bild(None)
    if f >= A_DA:
        teil(e, BASIS, CX - 4)
    if f >= MITTE_DA:
        teil(e, MITTE, CX - 3, unten=9)
    if f >= KOPF_DA:
        teil(e, KOPF, CX - 2, unten=6)
    if f >= AUGE1:
        e.setze(CX - 1, 4, KOHLE)
    if f >= AUGE2:
        zu = any(von <= f < bis for von, bis in ZWINKERN)
        e.setze(CX + 1, 4, SCHATTEN if zu else KOHLE)
    if f >= KNOEPFE:
        e.setze(CX, 8, KOHLE)
        e.setze(CX, 12, KOHLE)
    if f >= NASE_DA:
        e.rechteck(CX, 5, 2, 1, ORANGE)
    if f >= HUT_DA:
        hut(e, CX - 2, 0)
    if f >= SCHAL_DA:
        e.rechteck(CX - 2, 6, 5, 1, ROT)
        e.rechteck(CX - 2, 7, 1, 2, ROT)                             # das Ende hängt herab
    if f >= BESEN_DA:
        besen(e, CX + 6)
        e.rechteck(CX + 4, 8, 2, 1, HOLZ)                            # Arm hält den Besen
        if JUBEL <= f < ABGANG and (f - JUBEL) // 6 % 2:             # der andere winkt
            e.linie(CX - 4, 8, CX - 6, 6, HOLZ)
        else:
            e.rechteck(CX - 5, 8, 2, 1, HOLZ)
            e.setze(CX - 6, 7, HOLZ)
    return e


def auflegen(bild, ebene, tiefer=0):
    """Legt die Ebene ins Bild, um `tiefer` Zeilen in den Boden gesunken."""
    for y in range(FUSS + 1 - tiefer):
        for x in range(B):
            bild.setze(x, y + tiefer, ebene.px[y][x])


def kind_a(bild, f):
    """Kind A (links): große Kugel, Kopf, Gesicht und Schal."""
    lauf = (f // 2) % 2
    if f < A_DA:                                                     # rollt die große Kugel herein
        a = f / A_DA
        kx = round(-8 + 30 * a)
        b, h = GROSS[min(7, int(a * 8))]
        kugel(bild, kx + 5, b, h, kx)
        kind(bild, kx, "schiebt" if h > 3 else "schiebt_tief", KIND_A, (f // 3) % 2)
    elif f < A_ZURUECK:
        kind(bild, 22, "steht", KIND_A)
    elif f < A_HOCKT:                                                # läuft nach links zurück
        kx = round(22 - 18 * (f - A_ZURUECK) / (A_HOCKT - A_ZURUECK))
        kind(bild, kx, "steht", KIND_A, lauf, links=True)
    elif f < A_ROLLT:                                                # hockt sich hin und formt eine Kugel
        kind(bild, 4, "schiebt_tief", KIND_A, dy=2)
        if f >= A_HOCKT + 2:
            kugel(bild, 9, 2, 2, 0)
    elif f < A_KOPF:                                                 # rollt den Kopf heran
        a = (f - A_ROLLT) / (A_KOPF - A_ROLLT)
        kx = round(4 + 12 * a)
        b, h = KLEIN[min(3, int(a * 4))]
        kugel(bild, kx + 5, b, h, kx)
        kind(bild, kx, "schiebt_tief", KIND_A, (f // 3) % 2)
    elif f < KOPF_DA:                                                # hebt ihn hinauf
        x, y = bogen((f - A_KOPF) / (KOPF_DA - A_KOPF), (21, FUSS), (CX - 2, 6), 3)
        teil(bild, KOPF, x, unten=y)
        kind(bild, 16, "jubel", KIND_A)
    elif f < JUBEL:                                                  # schmückt
        kx = min(A_STEHT_X, 16 + (f - KOPF_DA))
        reicht = any(t - 2 <= f < t + 3 for t in A_REICHT)
        kind(bild, kx, "reicht" if reicht else "steht", KIND_A, lauf if kx < A_STEHT_X else 0)
        if NASE_WURF <= f < NASE_DA:                                 # Karotte fliegt hinüber
            x, y = bogen((f - NASE_WURF) / (NASE_DA - NASE_WURF), (kx + 5, 5), (CX, 5), 3)
            bild.rechteck(x, y, 2, 1, ORANGE)
        if SCHAL_WURF <= f < SCHAL_DA:                               # Schal fliegt hinüber
            x, y = bogen((f - SCHAL_WURF) / (SCHAL_DA - SCHAL_WURF), (kx + 5, 5), (CX - 2, 6), 3)
            bild.rechteck(x, y, 4, 1, ROT)
    elif f < ABGANG:                                                 # hüpft vor Freude
        kind(bild, A_STEHT_X, "jubel", KIND_A, dy=-huepfer(f - JUBEL))
    else:                                                            # läuft nach links hinaus
        kind(bild, A_STEHT_X - (f - ABGANG), "steht", KIND_A, lauf, links=True)


def kind_b(bild, f):
    """Kind B (rechts): mittlere Kugel, Hut und Besen."""
    lauf = (f // 2) % 2
    if f < B_START:
        return
    if f < B_DA:                                                     # rollt die mittlere Kugel herein
        a = (f - B_START) / (B_DA - B_START)
        kx = round(68 - 22 * a)
        b, h = MITTEL[min(5, int(a * 6))]
        kugel(bild, kx - 2 - b, b, h, kx)
        kind(bild, kx, "schiebt_tief", KIND_B, (f // 3) % 2, links=True)
    elif f < MITTE_HOCH:
        teil(bild, MITTE, 37)
        kind(bild, 46, "steht", KIND_B, links=True)
    elif f < MITTE_DA:                                               # hebt sie auf die große
        x, y = bogen((f - MITTE_HOCH) / (MITTE_DA - MITTE_HOCH), (37, FUSS), (CX - 3, 9), 3)
        teil(bild, MITTE, x, unten=y)
        kind(bild, 46, "jubel", KIND_B, links=True)
    elif f < B_WEG1:
        kind(bild, 46, "steht", KIND_B, links=True)
    elif f < B_HUT:                                                  # läuft hinaus, den Hut holen
        kind(bild, 46 + (f - B_WEG1), "steht", KIND_B, lauf)
    elif f < B_WURF:                                                 # trägt den Hut über dem Kopf herein
        kx = 68 - (f - B_HUT)
        kind(bild, kx, "jubel", KIND_B, lauf, links=True)
        hut(bild, kx - 1, 3)
    elif f < B_WEG2:
        if f < HUT_DA:                                               # wirft ihn hinauf
            x, y = bogen((f - B_WURF) / (HUT_DA - B_WURF), (43, 3), (CX - 2, 0), 1.5)
            hut(bild, x, y)
        kind(bild, 44, "jubel" if f < HUT_DA else "steht", KIND_B, links=True)
    elif f < B_BESEN:                                                # läuft hinaus, den Besen holen
        kind(bild, 44 + (f - B_WEG2), "steht", KIND_B, lauf)
    elif f < BESEN_DA:                                               # trägt den Besen herein
        kx = round(68 - 29 * (f - B_BESEN) / (BESEN_DA - B_BESEN))
        besen(bild, kx - 2, unten=FUSS - 1)
        kind(bild, kx, "traegt", KIND_B, lauf, links=True)
    elif f < JUBEL:                                                  # tritt zurück
        kind(bild, min(B_STEHT_X, 39 + (f - BESEN_DA)), "steht", KIND_B, lauf, links=True)
    elif f < ABGANG:                                                 # hüpft vor Freude
        kind(bild, B_STEHT_X, "jubel", KIND_B, links=True, dy=-huepfer(f - JUBEL - 4))   # etwas versetzt
    else:                                                            # läuft nach rechts hinaus
        kind(bild, B_STEHT_X + (f - ABGANG), "steht", KIND_B, lauf)


def sonne(bild, f):
    """Die Sonne; ab STRAHLEN leuchtet sie heller und wirft Strahlen (es taut)."""
    strahlt = STRAHLEN <= f < LEER
    bild.kreis(SONNE_X, SONNE_Y, 2.2, SONNE_HELL if strahlt else SONNE)
    if strahlt:
        gerade = ((-4, 0), (-5, 0), (4, 0), (5, 0), (0, 4), (0, 5))
        schraeg = ((-3, 3), (-4, 4), (3, 3), (4, 4))
        for dx, dy in (gerade if (f // 3) % 2 else schraeg):
            bild.setze(SONNE_X + dx, SONNE_Y + dy, STRAHL)


def bilder():
    grund = garten()
    liste = []
    for f in range(255):
        bild = Bild()
        bild.px = [zeile[:] for zeile in grund.px]
        sonne(bild, f)
        tiefer = 0 if f < SCHMILZT else min(FUSS + 1, round((FUSS + 1) * (f - SCHMILZT) / (WEG - SCHMILZT)))
        auflegen(bild, schneemann(f), tiefer)
        if SCHMILZT < f < LEER:                                      # Schmelzhäufchen wächst, dann vergeht es
            halb = min(6, 3 + tiefer // 3, LEER - f)
            bild.rechteck(CX - halb, FUSS, 2 * halb + 1, 1, KUGEL)
        kind_a(bild, f)
        kind_b(bild, f)
        liste.append(bild)
    return liste
