#!/usr/bin/env python3
"""Anzeige der Matrix per Bluetooth ein- oder ausschalten (ohne Schaltsteckdose).

Die gespeicherte Animation bleibt erhalten; „aus“ schaltet nur die LEDs ab. Der Wächter macht
das ohne Steckdose selbst nach dem Zeitplan – zum Testen von Hand den Wächter vorher anhalten.

Aufruf: matrix_anzeige.py [-n NAME] an|aus
"""
import argparse
import asyncio
import os

from matrix_spieler import Matrix


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("zustand", choices=("an", "aus"))
    p.add_argument("-n", "--name", default=os.environ.get("MATRIX_NAME", ""))
    a = p.parse_args()
    m = Matrix(a.name)
    await m.verbinden()                         # schaltet die Anzeige ein
    try:
        await m.senden(bytes([0x71, 0x23 if a.zustand == "an" else 0x24]))
        print(f"Anzeige {a.zustand}")
    finally:
        await m.trennen()


if __name__ == "__main__":
    asyncio.run(main())
