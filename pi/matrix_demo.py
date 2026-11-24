#!/usr/bin/env python3
"""Demo: möglichst viele Animationen nacheinander, eine Verbindung für alles (23.11.2026).

Vorher den Wächter anhalten (systemctl stop matrix-waechter), danach den Stand löschen und ihn
wieder starten – sonst glaubt er, die Matrix habe noch sein GIF:
    rm /var/lib/matrix-waechter/stand; systemctl start matrix-waechter

Aufruf: matrix_demo.py [--minuten 10] [--zeigen 15] [--hell 67] GIF …
Reihenfolge wie angegeben; aus dem Vorrat (schnell), sonst wird vorher komprimiert (~20 s).
"""
import argparse
import asyncio
import logging
import os
import time

from matrix_spieler import Matrix
from matrix_upload import gif_bilder, hochladen, vorrat_lesen

log = logging.getLogger("matrix-demo")


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("gifs", nargs="+")
    p.add_argument("--minuten", type=float, default=10)
    p.add_argument("--zeigen", type=float, default=15)
    p.add_argument("--hell", type=int, default=67)
    p.add_argument("--tempo", type=int, default=75)
    p.add_argument("-n", "--name", default=os.environ.get("MATRIX_NAME", ""))
    a = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    liste = [(0, gif, None) for gif in a.gifs]                     # Reihenfolge wie angegeben
    ende = time.monotonic() + a.minuten * 60
    m = Matrix(a.name)
    await m.verbinden()
    try:
        for nr, (_, gif, _k) in enumerate(liste, 1):
            if time.monotonic() > ende - 20:
                break
            with open(gif, "rb") as f:
                k = vorrat_lesen(f.read())                         # Vorrat wächst nebenher
            bilder, _ = gif_bilder(gif)
            log.info("%d/%d %s (%s)", nr, len(liste), os.path.basename(gif),
                     f"{sum(map(len, k)) // 1024} KB aus dem Vorrat" if k else "wird komprimiert")
            for versuch in range(2):
                try:
                    if not m.verbunden:
                        await m.verbinden()
                    await hochladen(m, bilder, a.tempo, a.hell, k)
                    break
                except Exception as e:
                    log.warning("Fehler (%s), verbinde neu", str(e) or type(e).__name__)
                    try:
                        await m.trennen()
                    except Exception:
                        pass
                    await asyncio.sleep(3)
            await asyncio.sleep(min(a.zeigen, max(0, ende - time.monotonic())))
    finally:
        await m.trennen()
    log.info("Demo fertig")


if __name__ == "__main__":
    asyncio.run(main())
