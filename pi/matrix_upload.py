#!/usr/bin/env python3
"""Lädt ein GIF als Animation in die Surplife-Matrix 64×16; die Matrix spielt es dann selbst ab.

Ermittelt am 23.11.2026 aus einem Mitschnitt der iPhone-App (PacketLogger, Test-GIF
led/test_app_64x16.gif). Ablauf wie bei der App:

  ea 01 KOPF        38 Bytes; Byte 0 = 01, Byte 3 = 0x18, Bytes 21–22 = Bildanzahl
  ea 02 TAB         je Bild Position (4 Bytes) und Länge (2 Bytes), big-endian
  ea 03 NNNN DATEN  je Bild (NNNN ab 1), a2pl-komprimiert (siehe a2pl.py)
  ea 04 00          Ende                 (höchstens 255 Bilder, ab 256 bricht die Matrix ab)
  e2 09 01 TT HH 00 Tempo TT (App: 0x4b = 75) und Helligkeit HH (0–100)

Die Matrix quittiert mit 15 ea 01 00 / 15 ea 02 00 / 15 ea 03 00 NN / 15 ea 04 00.
Ein Bild sind 1024 Pixel à 2 Bytes (16-Bit-Farbe wie in matrix_spieler.hsv16, big-endian),
**spaltenweise**: Spalte für Spalte von links, in der Spalte von oben nach unten.

Befehle über 509 Bytes werden in Stücke geteilt (Paketkopf 41 statt 01):
  erstes Stück  [41][seq][00 00][Gesamtlänge-1 BE16][Stücklänge BE16] + 501 Bytes
  weitere       [41][seq][Nr BE16, beim letzten | 0x8000][Stücklänge BE16] + bis 503 Bytes

Aufruf:  matrix_upload.py [-n NAME] [--tempo 75] [--hell 100] GIF
"""
import argparse
import asyncio
import hashlib
import logging
import os
import struct
import sys
import time

import a2pl
from matrix_spieler import BREITE, HOEHE, SCHREIBEN, ZEITLIMIT, Matrix, hsv16

log = logging.getLogger("matrix-upload")
STUECK = 509          # MTU 512 - 3
MAX_BILDER = 255      # gemessen 23.11.2026: 255 gehen, ab 256 bricht die Matrix bei ea 02 ab


# ── reine Funktionen (testbar) ─────────────────────────────────────
def bild_spaltenweise(pixel_rgb):
    """1024 RGB-Pixel (zeilenweise) → 2048 Bytes spaltenweise für die Matrix."""
    out = bytearray()
    for x in range(BREITE):
        for y in range(HOEHE):
            out += hsv16(*pixel_rgb[y * BREITE + x]).to_bytes(2, "big")
    return bytes(out)


def kopf(anzahl):
    k = bytearray(38)
    k[0], k[3] = 0x01, 0x18
    k[21:23] = anzahl.to_bytes(2, "big")
    return b"\xea\x01" + bytes(k)


def tabelle(laengen):
    t = bytearray(b"\xea\x02")
    pos = 0
    for n in laengen:
        t += pos.to_bytes(4, "big") + n.to_bytes(2, "big")
        pos += n
    return bytes(t)


def upload_befehle(bilder_a2pl):
    """Alle Befehle (ohne 0a-Vorsatz) für den Upload der komprimierten Bilder."""
    if not 1 <= len(bilder_a2pl) <= MAX_BILDER:
        raise ValueError(f"{len(bilder_a2pl)} Bilder – die Matrix nimmt 1 bis {MAX_BILDER}")
    bf = [kopf(len(bilder_a2pl)), tabelle([len(b) for b in bilder_a2pl])]
    bf += [b"\xea\x03" + i.to_bytes(2, "big") + b for i, b in enumerate(bilder_a2pl, 1)]
    bf.append(b"\xea\x04\x00")
    return bf


def pakete(seq, inner, stueck=STUECK):
    """inner (mit 0a) → Liste von Schreibpaketen, bei Bedarf in Stücke geteilt."""
    n = len(inner)
    if n + 8 <= stueck:
        return [bytes([0x01, seq & 0xFF, 0x80, 0x00]) + (n - 1).to_bytes(2, "big")
                + n.to_bytes(2, "big") + inner]
    erst = stueck - 8
    teile = [inner[:erst]] + [inner[i:i + stueck - 6] for i in range(erst, n, stueck - 6)]
    out = [bytes([0x41, seq & 0xFF, 0x00, 0x00]) + (n - 1).to_bytes(2, "big")
           + len(teile[0]).to_bytes(2, "big") + teile[0]]
    for nr, t in enumerate(teile[1:], 1):
        kennung = nr | (0x8000 if nr == len(teile) - 1 else 0)
        out.append(bytes([0x41, seq & 0xFF]) + kennung.to_bytes(2, "big")
                   + len(t).to_bytes(2, "big") + t)
    return out


def gif_bilder(pfad):
    """GIF → Liste von 2048-Byte-Bildern (spaltenweise) und Bilddauern in s."""
    from PIL import Image, ImageSequence
    bilder, dauern = [], []
    with Image.open(pfad) as im:
        for frame in ImageSequence.Iterator(im):
            rgb = frame.convert("RGB")
            if rgb.size != (BREITE, HOEHE):
                rgb = rgb.resize((BREITE, HOEHE))
            px = [rgb.getpixel((x, y)) for y in range(HOEHE) for x in range(BREITE)]
            bilder.append(bild_spaltenweise(px))
            dauern.append((frame.info.get("duration") or 100) / 1000)
    return bilder, dauern


# ── Bluetooth ──────────────────────────────────────────────────────
async def senden_gross(m, befehl):
    """Befehl senden, große in Stücken; letztes Stück bestätigt."""
    m.seq += 1
    ps = pakete(m.seq, b"\x0a" + befehl)
    for i, p in enumerate(ps):
        await asyncio.wait_for(
            m.client.write_gatt_char(SCHREIBEN, p, response=i == len(ps) - 1), ZEITLIMIT)


async def quittung(m, praefix, zeit=10):
    """Wartet auf eine Antwort, deren Inhalt mit praefix beginnt (Statusmeldungen überspringen)."""
    ende = time.monotonic() + zeit
    while True:
        rest = ende - time.monotonic()
        if rest <= 0:
            raise TimeoutError(f"keine Quittung {praefix.hex()}")
        raw = await asyncio.wait_for(m.rx.get(), rest)
        inner = raw[8:] if raw[0] & 0x01 else raw[7:]
        if inner.startswith(praefix):
            return inner


# Höchstens so viele komprimierte Bytes je Animation (23.11.2026): Die Matrix speichert nur
# 80 KB (81920 Bytes); was darüber liegt, fehlt am Ende der Runde (zuerst links). Gemessen:
# 78444 Bytes fehlerfrei, 84788 kurz am Schluss kaputt, 94346 und mehr deutlich. Früher: nach 254 KB
# (Polarlicht) war die Animation kaputt und die Matrix per Bluetooth unsichtbar, bis über die
# App eine andere geladen wurde. Mit Abstand darunter bleiben.
MAX_BYTES = int(os.environ.get("MATRIX_MAX_BYTES", "78000"))


# ── Vorrat: komprimierte Bilder im Voraus (spart ~20 s je Upload auf dem Pi) ──
VORRAT = os.environ.get("MATRIX_VORRAT", "/var/lib/matrix-waechter/vorrat")


def vorrat_pfad(gif_bytes, ordner=None):
    return os.path.join(ordner or VORRAT, hashlib.sha256(gif_bytes).hexdigest()[:16] + ".a2pl")


def vorrat_lesen(gif_bytes, ordner=None):
    """Liste der komprimierten Bilder aus dem Vorrat oder None."""
    try:
        with open(vorrat_pfad(gif_bytes, ordner), "rb") as f:
            daten = f.read()
    except OSError:
        return None
    anzahl, pos, liste = struct.unpack_from(">H", daten, 0)[0], 2, []
    for _ in range(anzahl):
        n = struct.unpack_from(">I", daten, pos)[0]
        liste.append(daten[pos + 4:pos + 4 + n])
        pos += 4 + n
    return liste if pos == len(daten) else None


def vorrat_schreiben(gif_bytes, komprimiert, ordner=None):
    pfad = vorrat_pfad(gif_bytes, ordner)
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    teile = [struct.pack(">H", len(komprimiert))]
    for k in komprimiert:
        teile += [struct.pack(">I", len(k)), k]
    with open(pfad + ".neu", "wb") as f:
        f.write(b"".join(teile))
    os.replace(pfad + ".neu", pfad)


def vorrat_anlegen(gif, ordner=None):
    """GIF komprimieren und im Vorrat ablegen, falls noch nicht da. True = neu angelegt."""
    with open(gif, "rb") as f:
        gif_bytes = f.read()
    if vorrat_lesen(gif_bytes, ordner) is not None:
        return False
    bilder, _ = gif_bilder(gif)
    vorrat_schreiben(gif_bytes, [a2pl.compress(b) for b in bilder], ordner)
    return True


async def hochladen(m, bilder, tempo=75, hell=100, komprimiert=None):
    if not 1 <= len(bilder) <= MAX_BILDER:
        raise ValueError(f"{len(bilder)} Bilder – die Matrix nimmt 1 bis {MAX_BILDER}")
    t0 = time.monotonic()
    if komprimiert is None or len(komprimiert) != len(bilder):
        komprimiert = [a2pl.compress(b) for b in bilder]
        log.info("%d Bilder, komprimiert %d Bytes (%.1f s)", len(bilder), sum(map(len, komprimiert)),
                 time.monotonic() - t0)
    else:
        log.info("%d Bilder aus dem Vorrat, %d Bytes", len(bilder), sum(map(len, komprimiert)))
    if sum(map(len, komprimiert)) > MAX_BYTES:
        raise ValueError(f"{sum(map(len, komprimiert))} Bytes – die Matrix verkraftet höchstens "
                         f"etwa {MAX_BYTES} (sonst ist die Animation kaputt)")
    while not m.rx.empty():
        m.rx.get_nowait()
    for b in upload_befehle(komprimiert):
        await senden_gross(m, b)
        erwartet = b"\x15" + b[:2] + (b"\x00" + b[3:4] if b[1] == 0x03 else b"")
        await quittung(m, erwartet)
    await m.senden(bytes([0xE2, 0x09, 0x01, tempo, hell, 0x00]))
    log.info("Hochgeladen in %.1f s, Tempo %d, Helligkeit %d", time.monotonic() - t0, tempo, hell)


async def _main():
    if len(sys.argv) > 1 and sys.argv[1] == "--vorrat":         # matrix_upload.py --vorrat GIF …
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        for gif in sys.argv[2:]:
            t0 = time.monotonic()
            neu = vorrat_anlegen(gif)
            log.info("%s: %s (%.1f s)", os.path.basename(gif), "angelegt" if neu else "schon da",
                     time.monotonic() - t0)
        return
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("gif")
    p.add_argument("-n", "--name", default=os.environ.get("MATRIX_NAME", ""))
    p.add_argument("--tempo", type=int, default=75)
    p.add_argument("--hell", type=int, default=100)
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(message)s")
    bilder, dauern = gif_bilder(a.gif)
    m = Matrix(a.name)
    await m.verbinden()
    try:
        await hochladen(m, bilder, a.tempo, a.hell)
        await asyncio.sleep(2)
    finally:
        await m.trennen()


if __name__ == "__main__":
    asyncio.run(_main())
