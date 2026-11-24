"""Schneemann: wird gebaut, bekommt Hut, Nase, Knöpfe und bunten Schal, winkt – 255 Bilder.

0–45   drei Schneekugeln rollen herein (die untere von links, Mitte und Kopf von rechts) und
       springen auf den Stapel
45–90  Hut fällt, Augen, Karottennase, Knöpfe, bunter Schal erscheinen
90–255 winkt, Schal weht, ein Rotkehlchen besucht ihn; rechts läuft "FROHES FEST" in
       wechselnden Farben durch
"""
import math

from basis import (B, BUNT, GELB, GOLD, HELLBRAUN, NACHTBLAU, ORANGE, ROT, SCHNEEDECKE, Bild, Schnee,
                   Sterne, dimmen, regenbogen, textbreite)

NAME = "schneemann"
TITEL = "Schneemann mit buntem Schal und FROHES FEST"

KOHLE = (0, 0, 0)
SCHNEEBALL = (235, 240, 255)
SCHATTEN = (150, 165, 215)
HUT = (60, 50, 200)
HUTBAND = GOLD
VOGEL = (190, 110, 45)
CX = 11
# Die drei Kugeln als Sprites (w = Schnee, s = Schatten); obere linke Ecke am fertigen Schneemann
BASIS = [".wwwwwww.", "wwwwwwwws", "wwwwwwwws", "wwwwwwwss", ".wwwwsss."]
MITTE = [".wwwww.", "wwwwwws", "wwwwwss"]
KOPF = [".www.", "wwwww", "wwwws", ".wws."]
SCHNEE_FARBEN = {"w": SCHNEEBALL, "s": SCHATTEN}
#          Sprite, x, y am Ziel, rollt von..bis, springt bis, kommt von (x)
TEILE = [(BASIS, CX - 4, 10, 0, 16, 16, -9),
         (MITTE, CX - 3, 7, 10, 28, 35, B),
         (KOPF, CX - 2, 3, 24, 38, 45, B)]
ABSPRUNG = CX + 8                                           # von hier springen Mitte und Kopf hinauf
SCHAL = [ROT, GELB, ROT, GELB, ROT]
# Jeder Stern, jede Flocke und jeder Hügel kostet in jedem Bild Speicher (die Matrix fasst 80 KB):
# daher wenige Sterne, die beim Funkeln ganz ausgehen, 8 Flocken, flacher Boden ohne Hügel und
# eine Schrift in drei Farbtönen (gleiche Farben lassen sich besser packen als elf verschiedene).
HIMMEL_SCHNEE = Schnee(anzahl=8, saat=9, farbe=(200, 205, 240))
STERNE = Sterne(anzahl=6, saat=4, y_max=6)
STERNLICHT = (255, 240, 200)
TEXT = "FROHES FEST"
LINKS = 24                                                  # Schrift erst ab hier
VOGEL_SITZT = ["yrb..", ".rbbb", "..b.."]                   # schaut nach links zum Schneemann
VOGEL_FLIEGT = [["b...", "yrbb", ".rb."], ["....", "yrbb", ".rbb"]]


def sterne(bild, f):
    """Sterne funkeln in drei Stufen und sind im Tal der Helligkeit ganz aus."""
    for x, y, phase, periode in STERNE.sterne:
        t = (f + phase) % periode / periode
        h = round((0.25 + 0.75 * (0.5 + 0.5 * math.cos(2 * math.pi * t))) * 4) / 4
        if h > 0.25:
            bild.setze(x, y, dimmen(STERNLICHT, h))


def rollen(bild, sprite, x, y, weg):
    """Kugel unterwegs: ganz weiß, ein Schattenfleck wandert im Kreis (sie rollt)."""
    b, h = len(sprite[0]), len(sprite)
    bild.figur(x, y, sprite, {"w": SCHNEEBALL, "s": SCHNEEBALL})
    w = weg / (b / 2)
    for k in ((0, math.pi) if h > 3 else (0,)):
        px = x + (b - 1) / 2 + (b / 2 - 1.5) * math.cos(w + k)
        py = y + (h - 1) / 2 + (h / 2 - 1.2) * math.sin(w + k)
        bild.setze(px, py, SCHATTEN)


def kugeln(bild, f):
    """Die untere Kugel rollt von links herein, Mitte und Kopf von rechts – sie springen im
    Bogen auf den Stapel."""
    for sprite, zx, zy, von, rollt_bis, bis, start in TEILE:
        if f < von:
            continue
        if f >= bis:
            bild.figur(zx, zy, sprite, SCHNEE_FARBEN)
            continue
        boden_y = 15 - len(sprite)
        absprung = zx if bis == rollt_bis else ABSPRUNG
        if f < rollt_bis:
            t = (f - von) / (rollt_bis - von)
            x = start + (absprung - start) * t
            rollen(bild, sprite, round(x), boden_y, x)
        else:                                                   # Sprung im Bogen
            t = (f - rollt_bis) / (bis - rollt_bis)
            x = absprung + (zx - absprung) * t
            y = boden_y + (zy - boden_y) * t - 4 * math.sin(math.pi * t)
            rollen(bild, sprite, round(x), round(y), x)


def schneemann(bild, f):
    kugeln(bild, f)
    if f < 45:
        return
    g = f - 45
    hy = min(0, -4 + g // 2)                                    # Hut fällt
    bild.rechteck(CX - 1, hy, 3, 2, HUT)
    bild.rechteck(CX - 1, hy + 1, 3, 1, HUTBAND)
    bild.rechteck(CX - 2, hy + 2, 5, 1, HUT)
    if g >= 10:                                                 # Augen (blinzeln)
        offen = (f % 60) > 2
        for dx in (-1, 1):
            bild.setze(CX + dx, 4, KOHLE if offen else SCHATTEN)
    if g >= 16:                                                 # Nase wächst
        for dx in range(0, min(3, (g - 16) // 3 + 1)):
            bild.setze(CX + dx, 5, ORANGE)
    for k, y in enumerate((8, 11, 13)):                         # bunte Knöpfe
        if g >= 24 + k * 3:
            bild.setze(CX, y, BUNT[(k * 2 + f // 40) % len(BUNT)])
    if g >= 36:                                                 # Schal mit Streifen, Ende weht
        for dx in range(-2, 3):
            bild.setze(CX + dx, 6, SCHAL[dx + 2])
        wehen = round(math.sin(f / 6))
        bild.setze(CX - 2, 7, SCHAL[1])
        bild.setze(CX - 2 - (wehen > 0), 8, SCHAL[0])
    if g >= 43:                                                 # Arme; der linke winkt
        bild.linie(CX + 4, 8, CX + 7, 6, HELLBRAUN)
        bild.setze(CX + 8, 6, HELLBRAUN)
        bild.setze(CX + 7, 5, HELLBRAUN)
        hoch = (f // 7) % 2 if f > 90 else 0
        bild.linie(CX - 4, 8, CX - 7, 6 - hoch * 2, HELLBRAUN)
        bild.setze(CX - 8, 5 - hoch * 2, HELLBRAUN)
        bild.setze(CX - 8, 7 - hoch * 2, HELLBRAUN)


def vogel(bild, f):
    """Rotkehlchen fliegt 120–150 von rechts herein, sitzt bis 200 auf dem Arm, fliegt weg."""
    if f < 120 or f > 232:
        return
    farben = {"b": VOGEL, "r": ROT, "y": GELB}
    if 150 <= f < 200:                                          # sitzt, wippt ab und zu
        wipp = 1 if (f // 12) % 2 and f % 12 < 3 else 0
        bild.figur(CX + 7, 3 - wipp, VOGEL_SITZT, farben)
        return
    if f < 150:
        t = 150 - f
        x, y = CX + 7 + t * 1.5, 3 - round(2 * math.sin(t / 5))
        bild.figur(round(x), y, VOGEL_FLIEGT[(f // 3) % 2], farben)
    else:
        t = f - 200
        x, y = CX + 7 + t * 1.5, 3 - round(2 * math.sin(t / 5))
        bild.figur(round(x), y, VOGEL_FLIEGT[(f // 3) % 2], farben, spiegeln=True)


def bilder():
    breite = textbreite(TEXT)
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        sterne(bild, f)
        HIMMEL_SCHNEE.zeichnen(bild, f)
        bild.rechteck(0, 15, B, 1, SCHNEEDECKE)
        if f >= 60:                                             # Schrift rechts vom Schneemann
            schrift = Bild(None)
            x = B - (f - 60) % (breite + B - LINKS)
            schrift.text(x, 5, TEXT, lambda i: regenbogen(i % 3 * 120 + f * 6))
            for y in range(16):
                for xx in range(LINKS, B):
                    if schrift.px[y][xx] is not None:
                        bild.setze(xx, y, schrift.px[y][xx])
        schneemann(bild, f)
        vogel(bild, f)
        liste.append(bild)
    return liste
