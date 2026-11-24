#!/usr/bin/env python3
"""Spielt ein GIF auf der Surplife-LED-Matrix 64×16 (IOTBT…) ab, Bild für Bild über Bluetooth.

Die Matrix (Statusmeldung: 1024 LEDs) spricht das Protokoll des Surplife-LED-Vorhangs
(https://codeberg.org/ge0rg/surplife-curtain), nicht das der 90×12/96×16-Panels: Hochladen
mit ea 05/e0 30 (surplife-matrix-ble) beantwortet sie nicht. Der Pi zeichnet jedes Bild selbst:

  e2 0b HSV            alle LEDs eine Farbe
  e2 0c 90 HSV MASKE   LEDs mit gesetztem Bit (128 Bytes, zeilenweise ab links oben,
                       höchstes Bit zuerst) bekommen die Farbe, die übrigen bleiben
  71 23 / 71 24        an / aus

Farbe als 16 Bit: Farbton 7 Bit (0–127), Sättigung 4 Bit (0–15), Helligkeit 5 Bit (0–31).
Paket: [01][seq][80 00][len-1 BE16][len BE16][0a][Befehl]; vorher 0c, Zeit, Statusabfrage.

Gemessen am 23.11.2026 an einer Matrix 64×16:
- Die Matrix schafft nur ~3–7 Befehle pro Sekunde (bestätigt ~290 ms, gestaut ~140 ms),
  egal wie groß. Zu schnell ohne Bestätigung → sie staut oder trennt. Deshalb wird der
  letzte Befehl jedes Bildes bestätigt; das GIF läuft so mit ~1,5–2 Bildern pro Sekunde.
- BlueZ verbindet mit ~49 ms Intervall; die Matrix wünscht 7,5–20 ms. Nach dem Verbinden
  wird mit hcitool lecup auf 7,5–15 ms gestellt (hilft der Funkstrecke, nicht dem Tempo).
- Verbindungsaufbau scheitert oft (0x3e, WLAN 2,4 GHz teilt sich beim Pi 4 die Antenne);
  bleak versucht es innerhalb des Timeouts selbst mehrfach, sonst neuer Anlauf.
- Viele Verbindungen pro Einschalten machen dieser Matrix nichts (10+ ohne Hänger).

Aufruf zum Testen:  matrix_spieler.py [-n NAME] [--sekunden 30] [--modus alle|echtzeit] GIF
"""
import argparse
import asyncio
import os
import colorsys
import datetime
import logging
import re
import subprocess
import time

BREITE, HOEHE = 64, 16
PIXEL = BREITE * HOEHE
SCHREIBEN = "0000ff01-0000-1000-8000-00805f9b34fb"
MELDUNG = "0000ff02-0000-1000-8000-00805f9b34fb"
PAUSE = 0.03        # zwischen unbestätigten Befehlen eines Bildes
ZEITLIMIT = 10      # s je Bluetooth-Schritt; ohne Limit kann eine Antwort ewig ausbleiben

log = logging.getLogger("matrix-spieler")


# ── reine Funktionen (ohne Bluetooth, testbar) ─────────────────────
def hsv16(r, g, b):
    """RGB (0–255) in die 16-Bit-Farbe der Matrix (7/4/5 Bit H/S/V)."""
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return (round(h * 127) & 0x7F) << 9 | round(s * 15) << 5 | round(v * 31)


def maske(indizes):
    """128-Byte-Bitmaske, Bit für Pixel i = Zeile*64+Spalte, höchstes Bit zuerst."""
    m = bytearray(PIXEL // 8)
    for i in indizes:
        m[i >> 3] |= 0x80 >> (i & 7)
    return bytes(m)


def befehle_fuer_bild(vorher, nachher):
    """Befehle, die die Matrix von Bild `vorher` (None = unbekannt) zu `nachher` bringen.

    Ein Bild ist eine Liste von 1024 Farben (hsv16). Nur geänderte Pixel werden gesendet,
    je Farbe ein e2 0c. Ist das Bild unbekannt, zuerst mit der häufigsten Farbe füllen."""
    befehle = []
    if vorher is None:
        haeufigste = max(set(nachher), key=nachher.count)
        befehle.append(b"\xe2\x0b" + haeufigste.to_bytes(2, "big"))
        vorher = [haeufigste] * PIXEL
    je_farbe = {}
    for i, (a, b) in enumerate(zip(vorher, nachher)):
        if a != b:
            je_farbe.setdefault(b, []).append(i)
    for farbe, idx in sorted(je_farbe.items()):
        befehle.append(b"\xe2\x0c\x90" + farbe.to_bytes(2, "big") + maske(idx))
    return befehle


def bild_zur_zeit(dauern, vergangen):
    """Index des Bildes, das nach `vergangen` Sekunden dran ist (GIF läuft in Schleife)."""
    gesamt = sum(dauern)
    t = vergangen % gesamt if gesamt > 0 else 0
    for i, d in enumerate(dauern):
        if t < d:
            return i
        t -= d
    return len(dauern) - 1


def paket(seq, inner):
    n = len(inner)
    return bytes([0x01, seq & 0xFF, 0x80, 0x00]) + (n - 1).to_bytes(2, "big") \
        + n.to_bytes(2, "big") + inner


def gif_laden(pfad):
    """Liefert [(bild, dauer_s)], bild = 1024 hsv16-Farben."""
    from PIL import Image, ImageSequence
    bilder = []
    with Image.open(pfad) as im:
        for frame in ImageSequence.Iterator(im):
            dauer = (frame.info.get("duration") or 100) / 1000
            rgb = frame.convert("RGB")
            if rgb.size != (BREITE, HOEHE):
                rgb = rgb.resize((BREITE, HOEHE))
            px = [rgb.getpixel((x, y)) for y in range(HOEHE) for x in range(BREITE)]
            bilder.append(([hsv16(*p) for p in px], dauer))
    return bilder


# ── Bluetooth ──────────────────────────────────────────────────────
def intervall_verkuerzen(adresse, min_int=6, max_int=12):
    """Verbindungsintervall auf 7,5–15 ms (Einheit 1,25 ms) stellen (Wunsch der Matrix)."""
    try:
        con = subprocess.run(["hcitool", "con"], capture_output=True, text=True, timeout=5).stdout
        m = re.search(rf"{adresse}\s+handle\s+(\d+)", con, re.I)
        if not m:
            log.warning("Intervall: Verbindung %s nicht in hcitool con", adresse)
            return False
        r = subprocess.run(["hcitool", "lecup", "--handle", m.group(1), "--min", str(min_int),
                            "--max", str(max_int), "--latency", "0", "--timeout", "100"],
                           capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError) as e:
        log.warning("Intervall nicht geändert: %s", e)
        return False


class Matrix:
    def __init__(self, name):
        self.name = name
        self.client = None
        self.seq = 0
        self.rx = None          # Antworten der Matrix (asyncio.Queue), ab verbinden()

    async def verbinden(self, timeout=45):
        from bleak import BleakClient, BleakScanner
        if self.name:
            dev = await BleakScanner.find_device_by_name(self.name, timeout=20)
        else:                                       # ohne Namen: erste IOTBT*-Matrix
            dev = await BleakScanner.find_device_by_filter(
                lambda d, a: (d.name or "").startswith("IOTBT"), timeout=20)
            if dev is not None:
                self.name = dev.name
        if dev is None:
            raise RuntimeError(f"{self.name} nicht gefunden")
        self.client = BleakClient(dev, timeout=timeout)
        await asyncio.wait_for(self.client.connect(), timeout + 15)
        log.debug("Verbindung steht, Handschlag …")
        self.rx = asyncio.Queue(maxsize=100)
        await asyncio.wait_for(self.client.start_notify(MELDUNG, self._meldung), ZEITLIMIT)
        jetzt = datetime.datetime.now()
        ts = bytes([0x10, 0x14, jetzt.year - 2000, jetzt.month, jetzt.day, jetzt.hour,
                    jetzt.minute, jetzt.second, jetzt.isoweekday(), 0x00, 0x0F])
        await self._roh(b"\x0c")
        await asyncio.sleep(0.5)
        await self.senden(ts + bytes([sum(ts) & 0xFF]))
        await self.senden(b"\xea\x81\x8a\x8b\x59")
        await asyncio.sleep(3)          # Matrix braucht nach der Statusabfrage etwas Zeit
        await self.senden(b"\x71\x23")  # an
        intervall_verkuerzen(dev.address)

    def _meldung(self, _h, d):
        log.debug("<< %s", bytes(d).hex())
        if self.rx is not None:
            if self.rx.full():                  # nur die letzten 100 behalten
                self.rx.get_nowait()
            self.rx.put_nowait(bytes(d))

    @property
    def verbunden(self):
        return self.client is not None and self.client.is_connected

    async def _roh(self, inner, bestaetigt=True):
        self.seq += 1
        await asyncio.wait_for(
            self.client.write_gatt_char(SCHREIBEN, paket(self.seq, inner), response=bestaetigt),
            ZEITLIMIT)

    async def senden(self, befehl, bestaetigt=True):
        await self._roh(b"\x0a" + befehl, bestaetigt)

    async def trennen(self):
        if self.verbunden:
            await asyncio.wait_for(self.client.disconnect(), ZEITLIMIT)

    async def bild_zeigen(self, vorher, bild):
        """Ändert die Matrix von `vorher` auf `bild`; letzter Befehl bestätigt (kein Stau)."""
        bf = befehle_fuer_bild(vorher, bild)
        for i, b in enumerate(bf):
            letzter = i == len(bf) - 1
            await self.senden(b, bestaetigt=letzter)
            if not letzter:
                await asyncio.sleep(PAUSE)

    async def abspielen(self, bilder, modus="alle", sekunden=None):
        """Spielt in Schleife, bis die Verbindung weg ist (oder `sekunden` um sind).

        modus "alle": jedes Bild, mindestens so lange wie im GIF (Zeitlupe, weil die Matrix
        langsam ist). "echtzeit": Tempo des GIFs, Bilder werden ausgelassen."""
        start = time.monotonic()
        ende = start + sekunden if sekunden else None
        dauern = [d for _b, d in bilder]
        aktuell, i, gezeigt = None, 0, 0
        while self.verbunden and (ende is None or time.monotonic() < ende):
            t0 = time.monotonic()
            if modus == "echtzeit":
                i = bild_zur_zeit(dauern, t0 - start)
            bild, dauer = bilder[i]
            if bild != aktuell:
                await self.bild_zeigen(aktuell, bild)
                aktuell = bild
                gezeigt += 1
            if modus == "echtzeit":
                await asyncio.sleep(0.01)
            else:
                rest = dauer - (time.monotonic() - t0)
                if rest > 0:
                    await asyncio.sleep(rest)
                i = (i + 1) % len(bilder)
        return gezeigt


async def _main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("gif")
    p.add_argument("-n", "--name", default=os.environ.get("MATRIX_NAME", ""))
    p.add_argument("--sekunden", type=float, default=30)
    p.add_argument("--modus", default="alle", choices=["alle", "echtzeit"])
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(message)s")
    bilder = gif_laden(a.gif)
    m = Matrix(a.name)
    await m.verbinden()
    log.info("Verbunden mit %s, %d Bilder", a.name, len(bilder))
    try:
        t0 = time.monotonic()
        n = await m.abspielen(bilder, a.modus, a.sekunden)
        dt = time.monotonic() - t0
        log.info("%d Bilder in %.1f s gezeigt (%.1f je Sekunde), verbunden=%s",
                 n, dt, n / dt, m.verbunden)
    finally:
        await m.trennen()


if __name__ == "__main__":
    asyncio.run(_main())
