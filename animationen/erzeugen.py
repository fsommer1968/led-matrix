#!/usr/bin/env python3
"""Erzeugt die Matrix-Animationen als GIF (64×16) und 8-fache Vorschau nach led/.

Aufruf (vom Repo-Ordner):
  .venv/bin/python led/animationen/erzeugen.py            alle
  .venv/bin/python led/animationen/erzeugen.py kamin …    nur diese (Modulnamen)
  .venv/bin/python led/animationen/erzeugen.py --bogen    zusätzlich Bildbogen (PNG) je Animation
  … erzeugen.py --ziel /opt/matrix/gifs --ohne-vorschau adventskalender   (auf dem Pi, täglich)

Die Reihenfolge in ANIMATIONEN ist auch die Reihenfolge für den täglichen Wechsel
(MATRIX_GIFS in led/pi/matrix-waechter.default).
"""
import importlib
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basis import B, H, MAX_BILDER, speichern  # noqa: E402

ANIMATIONEN = ["bunt", "kamin", "schlitten", "schneemann", "polarlicht", "advent", "lebkuchen",
               "glocken", "pinguine", "krippe", "hohoho", "schneeflocken", "eislaufen", "zug", "rentier",
               "auspacken", "werkstatt", "geschenkeberg", "plaetzchen", "wunschzettel",
               "adventskalender", "hirten", "stille_nacht", "nikolaus",
               "weihnachtsmarkt", "lichterhaus", "baum_schmuecken", "schneeballschlacht", "rodeln",
               "futterhaus", "winterwald", "bratapfel", "stadt_schnee",
               # Winter ohne Weihnachtsbezug
               "skifahrer", "schneepflug", "schneekugel", "hundeschlitten", "eisbaer", "iglu", "eule",
               "schneemann_bauen",
               # Erzgebirge, Schwarzwald und Katze
               "kuckucksuhr",
               "schwibbogen",
               "nussknacker",
               "schwarzwald",
               "katze_baum",
               "pyramide",
               "raeuchermann",
               "gluecksschwein",
               "weihnachtsmann_kamin",
               "kirschtorte",
               "rakete",
               "kirchturm",
               "wunderkerzen",
               "hermelin",
               "muehle",
               "holzfaeller",
               "pistenraupe",
               "wasserfall",
               "eishockey",
               "kerze",
               "wachsgiessen",
               "spaziergang",
               "bescherung",
               "festessen",
               "christmette",
               "raclette",
               # HEIMAT
               # Silvester (ab 27.12.) und der Gruß um 23:59
               "feuerwerk", "countdown", "sekt", "gluecksbringer", "jahreswechsel", "neujahr_2027"]
LED = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def bogen(bilder, pfad, anzahl=16, faktor=5):
    schritt = len(bilder) / anzahl
    auswahl = [bilder[int(i * schritt)] for i in range(anzahl)]
    w, h = B * faktor + 6, H * faktor + 6
    b = Image.new("RGB", (2 * w, (anzahl // 2) * h), (45, 45, 45))
    for k, im in enumerate(auswahl):
        b.paste(im.resize((B * faktor, H * faktor), Image.NEAREST), ((k % 2) * w, (k // 2) * h))
    b.save(pfad)


def erzeugen(modulname, mit_bogen=False, ordner=LED, vorschau=True):
    m = importlib.import_module(modulname)
    for name, titel, kw in getattr(m, "VARIANTEN", [(m.NAME, m.TITEL, {})]):
        _eine(m, name, titel, kw, mit_bogen, ordner, vorschau)


def _eine(m, name, titel, kw, mit_bogen, ordner, vorschau):
    bilder = [b.image() for b in m.bilder(**kw)]
    assert len(bilder) <= MAX_BILDER, f"{name}: {len(bilder)} Bilder"
    ziel = os.path.join(ordner, f"{name}_64x16.gif")
    tmp = ziel + ".neu.gif"                     # erst fertig schreiben, dann tauschen
    n = speichern(bilder, tmp)
    os.replace(tmp, ziel)
    if vorschau:
        speichern(bilder, os.path.join(ordner, f"{name}_64x16_vorschau.gif"), faktor=8)
    if mit_bogen:
        bogen(bilder, os.path.join(ordner, f"{name}_bogen.png"))
    print(f"{name}_64x16.gif: {len(bilder)} Bilder, {n} Farben – {titel}")


if __name__ == "__main__":
    argv = sys.argv[1:]
    ordner = LED
    if "--ziel" in argv:
        i = argv.index("--ziel")
        ordner = argv[i + 1]
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    for name in args or ANIMATIONEN:
        erzeugen(name, "--bogen" in argv, ordner, "--ohne-vorschau" not in argv)
