#!/usr/bin/env python3
"""Versuche an der Matrix. Wächter vorher anhalten!

  matrix_test.py hell N        nur Tempo/Helligkeit setzen (e2 09 01 75 N 00), ohne Upload
  matrix_test.py vorschau K    auffälliges Testbild (magenta/türkis im Wechsel) hochladen, mit
                               Byte 0 des Upload-Kopfs (ea 01) = K statt 01 – Suche nach einer
                               Kennung "nur anzeigen, nicht speichern"

Ergebnisse 25.11.2026 (an der Matrix):
  - hell: wirkt sofort ohne Upload (5/100 im Wechsel deutlich sichtbar) → MATRIX_HELL_OHNE_UPLOAD=1
  - vorschau 0x00 und 0x02: Bild erscheint und ist nach 10 s stromlos weiterhin da → beide werden
    gespeichert; Byte 0 ist keine Vorschau-Kennung. Andere Kopf-Bytes ungeprüft.
"""
import argparse
import asyncio
import logging
import os

import matrix_upload as mu
from matrix_spieler import BREITE, HOEHE, Matrix

MAGENTA, TUERKIS, SCHWARZ = (255, 0, 200), (0, 255, 200), (0, 0, 0)


def testbilder():
    """Zwei Bilder mit nur wenigen Punkten in der obersten Zeile: erst drei
    magentafarbene Punkte links, dann drei türkise daneben – blinkt im Wechsel, sonst alles aus."""
    bilder = []
    for farbe, xs in ((MAGENTA, (1, 5, 9)), (TUERKIS, (3, 7, 11))):
        px = [SCHWARZ] * (BREITE * HOEHE)
        for x in xs:
            px[x] = farbe                                  # Zeile 0
        bilder.append(mu.bild_spaltenweise(px))
    return bilder


async def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("was", choices=("hell", "vorschau"))
    p.add_argument("wert", type=lambda s: int(s, 0))
    p.add_argument("-n", "--name", default=os.environ.get("MATRIX_NAME") or "IOTBT1A2")
    a = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    m = Matrix(a.name)
    await m.verbinden()
    try:
        if a.was == "hell":
            await m.senden(bytes([0xE2, 0x09, 0x01, 75, a.wert, 0x00]))
            print(f"Helligkeit {a.wert} gesetzt (ohne Upload)")
        else:
            alt = mu.kopf

            def kopf(anzahl):
                k = bytearray(alt(anzahl))
                k[2] = a.wert                      # Byte 0 nach "ea 01"
                return bytes(k)
            mu.kopf = kopf
            await mu.hochladen(m, testbilder(), 10, 100)
            print(f"Testbild mit Kopf-Byte 0 = 0x{a.wert:02x} hochgeladen")
        await asyncio.sleep(1)
    finally:
        await m.trennen()


if __name__ == "__main__":
    asyncio.run(main())
