"""Krippenspiel der Kinder: eine kleine Bühne mit rotem Vorhang, davor die dunklen Köpfe des
Publikums. Der Vorhang geht auf: Josef (brauner Mantel, Stab) und Maria (blaues Tuch) stehen an der
Krippe mit Stroh, darüber wackelt ein Stern an der Schnur; links der Engel mit dem Goldstern am
Stab, rechts ein Kind als Schaf – es steht verkehrt herum und wedelt mit dem Schwanz, bis Josef mit
dem Stab klopft: Es erschrickt und dreht sich zur Krippe, das Publikum lacht. Der Engel hebt den
Stern und schwenkt ihn, dann verneigen sich alle zweimal (nicht ganz im Takt, das Schaf beim
zweiten Mal wieder in die falsche Richtung), das Publikum klatscht mit erhobenen Händen. Der
Vorhang geht zu, und das Schaf lugt unten noch einmal durch den Spalt. Die Runde beginnt und endet
mit geschlossenem Vorhang und geht darum ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (25.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum stehen die Köpfe im Achtertakt und die Falten des
Vorhangs im Vierertakt (gleiche Spalten wiederholen sich; der Vorhang gleitet mit festem
Faltenmuster zur Seite, statt sich wie eine Ziehharmonika zu raffen), die Köpfe sitzen als
Rechtecke auf einem durchgehenden Schulterband (Schultern je Kopf kosteten 6 KB mehr, Köpfe in
zwei Größen 4 KB), beim Klatschen gibt es nur „Arme hoch" und „Arme unten", die Kulisse ist
einfarbig ohne gemalte Sterne (jeder kostete rund 1 KB), und die Kinder sind Blöcke aus zwei bis
drei gleichen Spalten.
"""
from basis import B, GELB, HAUT, WEISS, Bild, dimmen

NAME = "krippenspiel"
TITEL = "Krippenspiel der Kinder"

RUNDE = 255
VORHANG = (150, 0, 10)                         # große Fläche: gedämpftes Rot
FALTE = (80, 0, 8)
SCHABRACKE = (100, 0, 10)                      # Querbehang oben
BORTE = (170, 105, 0)
KULISSE = (0, 4, 36)                           # gemalter Nachthimmel
HOLZ = (66, 30, 4)                             # Bühnenkante und Krippe
KOPF = (36, 40, 70)                            # Publikum: dunkle Schattenrisse
HAND = (80, 86, 135)
SCHNUR = (90, 90, 100)
MANTEL = (66, 26, 2)                           # Josef
TUCH = (0, 110, 30)                            # … sein Kopftuch
STAB = (84, 44, 6)
BLAU = (0, 60, 255)                            # Marias Tuch
KLEID = (150, 200, 255)
FLUEGEL = (110, 170, 255)
WOLLE = (190, 200, 235)                        # Schaf
BEIN = (90, 90, 100)
OHR = (255, 100, 140)
STROH = (255, 200, 0)

# ── Ablauf ─────────────────────────────────────────────────────────
AUF_VON, AUF_BIS = 8, 36                       # Vorhang öffnet sich
ZU_VON, ZU_BIS = 192, 220                      # … und schließt sich
OFFEN, ZU = 5, 32                              # Breite einer Vorhanghälfte
KLOPFT_VON, KLOPFT_BIS = 50, 62                # Josef klopft mit dem Stab
SCHAF_MERKT, SCHAF_DREHT, SCHAF_RICHTIG = 61, 63, 68     # das Schaf erschrickt und dreht sich zur Krippe
SCHAF_WIEDER, SCHAF_FALSCH = 156, 160          # … und beim zweiten Verneigen wieder weg
LACHEN_VON, LACHEN_BIS = 62, 74                # das Publikum lacht über das Schaf
NEIGT = [(72, 82), (120, 130)]                 # Maria beugt sich zum Kind
HEBEN = [(86, 134), (178, 222)]                # der Engel hebt den Stern
BEUGEN = [(140, 154), (160, 174)]              # zwei Verneigungen
KLATSCHEN_VON, KLATSCHEN_BIS = 144, 238
LUGT_VON, LUGT_BIS = 224, 250                  # das Schaf lugt durch den Vorhang

ENGEL_X, JOSEF_X, KRIPPE_X, MARIA_X, SCHAF_X = 9, 21, 28, 36, 47     # linke Spalte der Vorlagen
STERN_X = 31                                   # Stern an der Schnur über der Krippe

# g Heiligenschein, h Gesicht, f Flügel, w Kleid
ENGEL = ["..ggg", "f.hhh", "ffwww", ".fwww", "..www", "..www", "..www", "..www"]
ENGEL_FLATTERT = ["..ggg", "..hhh", "ffwww", "f.www", "..www", "..www", "..www", "..www"]
# t Kopftuch, h Gesicht, m Mantel
JOSEF = ["ttt", "thh", "mmm", "mmm", "mmm", "mmm", "mmm"]
# b blaues Tuch, h Gesicht, w Kleid; zweite Fassung: beugt sich zum Kind
MARIA = ["..bbb", ".hhbb", ".bbbb", ".wwbb", ".wwbb", ".wwbb", ".wwbb"]
MARIA_NEIGT = [".bbb.", "hhbb.", ".bbbb", ".wwbb", ".wwbb", ".wwbb", ".wwbb"]
# y Stroh, h Kind, w Windel, k Holz
KRIPPE = ["yhwwwyy", "kyyyyyk", ".kkkkk.", ".k...k."]
# Schaf (Blick nach links): o Ohr, w Wolle, h Gesicht, g Beine
SCHAF = [".o.....", "ww.....", "hhwwww.", ".wwwww.", ".wwwww.", ".g...g."]
SCHAF_VORN = ["o...o", ".www.", ".hhh.", "wwwww", "wwwww", ".g.g."]
SCHAF_BEUGT = [".......", ".......", ".owwww.", "wwwwww.", "hhwwww.", ".g...g."]


def weich(t):
    """Sanft anfahren und abbremsen (0 … 1)."""
    return t * t * (3 - 2 * t)


def vorhang_breite(f):
    """Breite einer Vorhanghälfte in Spalten (32 = geschlossen)."""
    if AUF_VON <= f < AUF_BIS:
        return round(ZU - (ZU - OFFEN) * weich((f - AUF_VON + 1) / (AUF_BIS - AUF_VON)))
    if AUF_BIS <= f < ZU_VON:
        return OFFEN
    if ZU_VON <= f < ZU_BIS:
        return round(OFFEN + (ZU - OFFEN) * weich((f - ZU_VON + 1) / (ZU_BIS - ZU_VON)))
    return ZU


def beugung(f, spaet=0):
    """0 aufrecht, 1 halb, 2 tief verneigt; `spaet` Bilder später als die anderen."""
    for von, bis in BEUGEN:
        t = f - von - spaet
        if 0 <= t < bis - von:
            return 1 if t < 2 or t >= bis - von - 2 else 2
    return 0


def beugen(zeilen, stufe, scheitel):
    """Verneigung von vorn: der Kopf sinkt; ganz unten sieht man statt des Gesichts den Scheitel."""
    leer = "." * len(zeilen[0])
    if stufe == 0:
        return zeilen
    if stufe == 1:
        return [leer] + zeilen[:2] + zeilen[3:]
    return [leer, leer, scheitel] + zeilen[3:]


def stern(bild, x, y, funkelt=False):
    """Goldstern: heller Kern, vier Zacken; beim Funkeln glimmen die Ecken mit."""
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        bild.setze(x + dx, y + dy, GELB)
    bild.setze(x, y, WEISS)
    if funkelt:
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            bild.setze(x + dx, y + dy, dimmen(GELB, 0.5))


def gehoben(f):
    """Wie hoch der Engel seinen Stern hält: 0, 1 oder 2 Pixel über der Ruhelage."""
    for von, bis in HEBEN:
        if von <= f < bis:
            return 1 if f < von + 3 or f >= bis - 3 else 2
    return 0


def engel(bild, f):
    """Engel mit Heiligenschein und Flügel; den Goldstern am Stab hebt er hoch und schwenkt ihn."""
    hoch = gehoben(f)
    flattert = hoch == 2 and f % 8 >= 4                              # vor Freude schlägt der Flügel
    zeilen = beugen(ENGEL_FLATTERT if flattert else ENGEL, beugung(f, 3), "f.ggg")
    bild.figur(ENGEL_X, 3, zeilen, {"g": GELB, "h": HAUT, "f": FLUEGEL, "w": WEISS})
    sx = ENGEL_X + 7
    bild.rechteck(sx, 7 - hoch, 1, 4, STAB)
    bild.setze(sx - 2, 7 - hoch, WEISS)                              # Ärmel und Hand
    bild.setze(sx - 1, 7 - hoch, HAUT)
    schwenk = 1 if hoch == 2 and f % 12 >= 6 else 0
    stern(bild, sx + schwenk, 5 - hoch, funkelt=hoch == 2 and (f // 3) % 2 == 0)


def josef(bild, f):
    """Josef mit Kopftuch und Stab; mit dem Stab klopft er, damit das Schaf sich umdreht."""
    zeilen = beugen(JOSEF, beugung(f), "ttt")
    bild.figur(JOSEF_X, 4, zeilen, {"t": TUCH, "h": HAUT, "m": MANTEL})
    auf = 1 if KLOPFT_VON <= f < KLOPFT_BIS and (f - KLOPFT_VON) % 4 < 2 else 0
    bild.rechteck(JOSEF_X + 4, 3 - auf, 1, 8, STAB)
    bild.setze(JOSEF_X + 3, 7 - auf, HAUT)


def maria(bild, f):
    """Maria im blauen Tuch; zwischendurch beugt sie sich zum Kind in der Krippe."""
    stufe = beugung(f, 1)
    neigt = stufe == 0 and any(von <= f < bis for von, bis in NEIGT)
    zeilen = beugen(MARIA_NEIGT if neigt else MARIA, stufe, ".bbbb")
    bild.figur(MARIA_X, 4, zeilen, {"b": BLAU, "h": HAUT, "w": KLEID})


def schaf(bild, f):
    """Das Kind als Schaf auf allen vieren: steht erst falsch herum (Blick nach rechts, wedelt mit
    dem Schwanz), erschrickt, dreht sich über vorn zur Krippe – und beim zweiten Verneigen wieder weg."""
    farben = {"w": WOLLE, "h": HAUT, "g": BEIN, "o": OHR}
    tief = beugung(f, 2) == 2
    if f < SCHAF_DREHT or f >= SCHAF_FALSCH:                         # falsch herum
        hupf = 1 if SCHAF_MERKT <= f < SCHAF_DREHT else 0
        bild.figur(SCHAF_X, 5 - hupf, SCHAF_BEUGT if tief else SCHAF, farben, spiegeln=True)
        bild.setze(SCHAF_X, 7 if (f // 3) % 2 or hupf else 6, WOLLE)
    elif f < SCHAF_RICHTIG or f >= SCHAF_WIEDER:                     # dreht sich: Blick ins Publikum
        bild.figur(SCHAF_X + 1, 5, SCHAF_VORN, farben)
    else:
        bild.figur(SCHAF_X, 5, SCHAF_BEUGT if tief else SCHAF, farben)
        bild.setze(SCHAF_X + 6, 7, WOLLE)


def buehne(bild, f):
    """Kulisse, Stern an der Schnur, Krippe und die vier Kinder (alles hinter dem Vorhang)."""
    bild.rechteck(0, 2, B, 9, KULISSE)
    # Stern an der Schnur: pendelt gemächlich hin und her, funkelt mit dem Stern des Engels um die Wette
    p = f % 20
    dx = 0 if p < 3 else 1 if p < 10 else 0 if p < 13 else -1
    bild.setze(STERN_X, 2, SCHNUR)
    stern(bild, STERN_X + dx, 4, funkelt=gehoben(f) == 2 and (f // 3) % 2 == 1)
    bild.figur(KRIPPE_X, 7, KRIPPE, {"y": STROH, "h": HAUT, "w": WEISS, "k": HOLZ})
    josef(bild, f)
    maria(bild, f)
    engel(bild, f)
    schaf(bild, f)


def vorhang(bild, f, breite):
    """Beide Vorhanghälften, `breite` Spalten breit; die Falten wandern mit der Kante."""
    for k in range(breite):
        farbe = FALTE if k % 4 == 0 else VORHANG
        bild.rechteck(breite - 1 - k, 2, 1, 9, farbe)
        bild.rechteck(B - breite + k, 2, 1, 9, farbe)
    if LUGT_VON <= f < LUGT_BIS:                                     # das Schaf lugt durch den Spalt
        t = f - LUGT_VON
        if t < 2 or t >= LUGT_BIS - LUGT_VON - 2:
            bild.rechteck(31, 9, 2, 1, WOLLE)
        else:
            blick = 0 if t < 8 else -1 if t < 13 else 1 if t < 18 else 0   # schaut nach links und rechts
            bild.rechteck(30, 8, 4, 3, WOLLE)
            bild.rechteck(31 + blick, 9, 2, 1, HAUT)
            bild.setze(30, 7, OHR)
            bild.setze(33, 7, OHR)


def publikum(bild, f):
    """Dunkle Köpfe im Achtertakt über einem durchgehenden Band aus Schultern; beim Klatschen
    reißen sie abwechselnd die Arme hoch (helle Hände)."""
    bild.rechteck(0, 15, B, 1, KOPF)
    for i in range(8):
        x = 8 * i + 2
        lacht = LACHEN_VON <= f < LACHEN_BIS and (f // 2 + i) % 2    # sie recken sich und lachen
        bild.rechteck(x, 12 if lacht else 13, 3, 3 if lacht else 2, KOPF)
        if KLATSCHEN_VON + (i % 3) * 2 <= f < KLATSCHEN_BIS + (i % 3) * 3 and (f // 2 + i) % 2:
            for arm in (x - 1, x + 3):
                bild.rechteck(arm, 13, 1, 2, KOPF)
                bild.setze(arm, 12, HAND)


def _bild(f):
    bild = Bild()
    breite = vorhang_breite(f)
    if breite < ZU:
        buehne(bild, f)
    vorhang(bild, f, breite)
    bild.rechteck(0, 0, B, 1, SCHABRACKE)
    bild.rechteck(0, 1, B, 1, BORTE)
    bild.rechteck(0, 11, B, 1, HOLZ)
    publikum(bild, f)
    return bild


def bilder():
    return [_bild(f) for f in range(RUNDE)]
