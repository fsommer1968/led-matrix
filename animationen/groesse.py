#!/usr/bin/env python3
"""Komprimierte Größe der GIFs, so wie die Matrix sie speichert (a2pl, spaltenweise).

Die Matrix speichert höchstens 80 KB (81920 Bytes) je Animation; was darüber liegt, fehlt am
Ende der Runde. Ziel: höchstens 76000 Bytes (Upload-Grenze im Wächter: 78000).

Aufruf (vom Repo-Ordner):  python3 animationen/groesse.py kamin advent1 …
                           python3 animationen/groesse.py          (alle GIFs im Hauptordner)
"""
import glob
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
LED = os.path.dirname(HIER)
sys.path.insert(0, os.path.join(LED, "pi"))
import a2pl  # noqa: E402
from matrix_upload import gif_bilder  # noqa: E402

ZIEL, GRENZE = 76000, 78000


def groesse(pfad):
    bilder, _ = gif_bilder(pfad)
    return len(bilder), sum(len(a2pl.compress(b)) for b in bilder)


if __name__ == "__main__":
    namen = sys.argv[1:]
    pfade = ([os.path.join(LED, f"{n}_64x16.gif") for n in namen] if namen
             else sorted(p for p in glob.glob(os.path.join(LED, "*_64x16.gif"))))
    for p in pfade:
        n, b = groesse(p)
        zeichen = "ok" if b <= ZIEL else ("knapp" if b <= GRENZE else "ZU GROSS")
        print(f"{os.path.basename(p)[:-10]:22s} {n:3d} Bilder  {b:6d} Bytes  {zeichen}")
