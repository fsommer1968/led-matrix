"""Rodeln: drei Kinder sausen nacheinander auf dem Schlitten den verschneiten Hang hinunter
(Schal flattert, Schnee stäubt), jubeln unten und stapfen mit dem Schlitten am Seil wieder hinauf;
Tannen, Mond, Sterne. Die Runde geht ohne Sprung in sich über – 255 Bilder.

Sparsam gezeichnet (23.11.2026): Die Matrix speichert nur 80 KB je Animation, jedes Bild wird
einzeln und spaltenweise komprimiert. Darum gleiche Nachbarspalten (Schlitten ohne Lücken, Kinder
drei Spalten breit mit zwei gleichen), waagerechtes Seil, drei Sterne, eine schlanke Tanne.
"""
from basis import B, GELB, HAUT, NACHTBLAU, PINK, ROT, WEISS, Bild, dimmen

NAME = "rodeln"
TITEL = "Kinder rodeln den Hang hinunter"

KANTE = (215, 225, 250)                        # Oberkante des Hangs
HANG = (78, 90, 140)                           # darunter gedämpft (große Fläche)
HOLZ = (210, 120, 30)
KUFE = (140, 140, 165)
SEIL = (150, 130, 90)
HOSE = (120, 80, 45)
AUGE = (50, 25, 10)
TANNE = (0, 95, 35)
STAMM = (90, 50, 20)
MOND = (240, 230, 170)
STERN = (255, 240, 200)
STERNE = [(13, 1, 0, 32), (36, 3, 11, 40), (47, 0, 23, 24)]          # x, y, Phase, Periode

RUNDE = 255
AB, UNTEN, AUF = 46, 62, 226                   # bis hierhin abwärts, unten jubeln, hinauf; danach oben warten
X_OBEN, X_UNTEN = 4, 54

# Kinder: Mütze, Jacke, Schal, Start im Umlauf
KINDER = [(ROT, (0, 110, 255), GELB, 0), (PINK, (0, 190, 70), (255, 120, 0), 85),
          (GELB, (200, 40, 255), (0, 220, 220), 170)]

# auf dem Schlitten (Blick nach rechts), 9 breit; s Schal, w Holz, r Kufe
FAHRT = [["..mmm....", "..mmm....", "sshha....", "..jjj....", "..jjjb...", ".wwwwwwww", ".rrrrrrrr"],
         ["..mmm....", "..mmm....", "..hha....", "ssjjj....", "..jjjb...", ".wwwwwwww", ".rrrrrrrr"]]
JUBEL = [["g.mmm.g..", ".jmmmj...", "..hha....", "..jjj....", "..jjjb...", ".wwwwwwww", ".rrrrrrrr"],
         ["..mmm....", "gjmmmjg..", "..hha....", "..jjj....", "..jjjb...", ".wwwwwwww", ".rrrrrrrr"]]
# zu Fuß (Blick nach links) mit Seil und Schlitten dahinter, 12 breit; die beiden hinteren
# Spalten des Kindes sind gleich, der Schritt wechselt zwischen vorderem und hinterem Bein
GEHEN = [["mmm.........", "mmm.........", "ahh.........", "jjj.........", "jjj.........", "bbbsswwwwwww", "b....rrrrrrr"],
         ["mmm.........", "mmm.........", "ahh.........", "jjj.........", "jjj.........", "bbbsswwwwwww", ".bb..rrrrrrr"]]
STEHT = ["mmm..", "mmm..", "hha..", "jjj..", "jjj..", "bbb..", "bbb.."]     # oben neben dem Schlitten
SCHLITTEN = ["wwwwwww", "rrrrrrr"]


def hang_y(x):
    """Oberkante des Hangs: oben eine Kuppe, dann gleichmäßig hinunter, unten ein Auslauf."""
    if x <= 7:
        return 7
    if x >= 55:
        return 14
    return 7 + (x - 2) // 7                                          # alle sieben Spalten eine Stufe


def auf_hang(bild, x0, zeilen, farben):
    """Zeichnet die Figur so, dass jede Spalte auf dem Hang aufsitzt (folgt dem Gefälle)."""
    for dx in range(len(zeilen[0])):
        x = x0 + dx
        boden = hang_y(x)
        for dy, zeile in enumerate(zeilen):
            if zeile[dx] != ".":
                bild.setze(x, boden - len(zeilen) + dy, farben[zeile[dx]])


def tanne(bild, x, hoehe):
    """Schlanke Tanne: alle drei Zeilen eine Stufe breiter (höchstens fünf Spalten), Schneehaube, Stamm."""
    fuss = hang_y(x)
    for k in range(hoehe - 1):
        halb = min(2, (k + 1) // 3)
        bild.rechteck(x - halb, fuss - hoehe + k, 2 * halb + 1, 1, TANNE)
    bild.setze(x, fuss - 1, STAMM)
    bild.setze(x, fuss - hoehe, KANTE)                               # Schneehaube


def bilder():
    liste = []
    for f in range(255):
        bild = Bild(NACHTBLAU)
        for x, y, phase, periode in STERNE:                          # wenige Sterne, funkeln langsam
            bild.setze(x, y, dimmen(STERN, 1.0 if (f + phase) % periode < periode * 0.6 else 0.5))
        bild.kreis(57, 3, 2.2, MOND)
        tanne(bild, 27, 9)                                           # Tanne hinter der Bahn
        for x in range(B):
            y0 = hang_y(x)
            bild.setze(x, y0, KANTE)
            for y in range(y0 + 1, 16):
                bild.setze(x, y, HANG)
        vorn = []
        for muetze, jacke, schal, start in KINDER:
            t = (f - start) % RUNDE
            farben = {"m": muetze, "h": HAUT, "a": AUGE, "j": jacke, "s": schal, "g": schal,
                      "b": HOSE, "w": HOLZ, "r": KUFE}
            if t < AB:                                               # hinunter, schneller werdend
                x = X_OBEN + round((X_UNTEN - X_OBEN) * (t / AB) ** 1.7)
                staub = []
                if t > 8:                                            # Schnee stäubt hinter den Kufen
                    for k in range(2):
                        sx = x - 1 - k * 2 - (f % 2)
                        staub.append((sx, hang_y(sx) - 1 - (k + f) % 3 * (k > 0), dimmen(WEISS, 0.9 - k * 0.3)))
                vorn.append((x, FAHRT[(f // 2) % 2], farben, staub))
            elif t < UNTEN:                                          # unten ausrollen und jubeln
                x = X_UNTEN + min(2, (t - AB) // 3)
                vorn.append((x, JUBEL[(f // 3) % 2], farben, []))
            elif t < AUF:                                            # zu Fuß hinauf, Schlitten am Seil
                a = (t - UNTEN) / (AUF - UNTEN)
                x = round(X_UNTEN - 1 + (X_OBEN - 3 - (X_UNTEN - 1)) * a)
                auf_hang(bild, x, GEHEN[(t // 4) % 2], {**farben, "s": SEIL})
            else:                                                    # oben: aufsitzen und auf die Abfahrt warten
                wippen = 1 if (AUF + 12 < t and (t // 5) % 2) else 0
                if t < AUF + 10:                                     # stellt sich neben den Schlitten
                    auf_hang(bild, X_OBEN + 1, SCHLITTEN, farben)
                    auf_hang(bild, X_OBEN - 3, STEHT, farben)
                else:
                    vorn.append((X_OBEN - 1, (JUBEL if wippen else FAHRT)[0], farben, []))
        for x, zeilen, farben, staub in vorn:                        # Rodler vor den Fußgängern
            for sx, sy, farbe in staub:
                bild.setze(sx, sy, farbe)
            auf_hang(bild, x, zeilen, farben)
        liste.append(bild)
    return liste
