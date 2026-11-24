#!/usr/bin/env python3
"""Matrix-Wächter für den Matrix-Pi: sorgt dafür, dass das gewünschte GIF in der Matrix steckt.

Die Matrix 64×16 (Name IOTBT…) speichert eine hochgeladene Animation und spielt sie selbst ab,
auch nach einem Stromausfall (geprüft am 23.11.2026). Der Wächter lädt deshalb nur hoch,
wenn sich etwas geändert hat (GIF, Tempo oder Helligkeit), und merkt sich das in STAND.
Mit MATRIX_HELL_TAG/NACHT wechselt die Helligkeit nach Tageslicht (siehe matrix_zeitplan);
das ist ein neuer Upload, also zwei Schreibvorgänge am Tag:

  suchen (ohne Verbindung) → Stand anders? → verbinden, hochladen (matrix_upload) → merken

Scheitert das Hochladen, wird die Pause länger (bis PAUSE_MAX). Nach NEUSTART_NACH
Fehlschlägen in Folge schaltet er die Matrix über die Schaltsteckdose kurz stromlos
(höchstens einmal je NEUSTART_ABSTAND Sekunden).

Wurde über die iPhone-App etwas anderes hochgeladen: `rm /var/lib/matrix-waechter/stand`
und `systemctl restart matrix-waechter` – dann lädt er das GIF wieder.

Einstellungen in /etc/default/matrix-waechter (siehe matrix-waechter.default).
"""
import asyncio
import hashlib
import logging
import os
import re
import subprocess
import sys
import time
import urllib.request

from matrix_spieler import Matrix
from matrix_upload import MAX_BILDER, MAX_BYTES, gif_bilder, hochladen, vorrat_lesen
import matrix_zeitplan

MATRIX_NAME = os.environ.get("MATRIX_NAME", "")          # leer = erste IOTBT*
GIF = os.environ.get("MATRIX_GIF", "/opt/matrix/gifs/weihnachtsmann_rentier_64x16.gif")
TEMPO = int(os.environ.get("MATRIX_TEMPO", "75"))         # 1–75 (App: 75)
HELL = int(os.environ.get("MATRIX_HELL", "100"))          # 0–100
STAND = os.environ.get("MATRIX_STAND", "/var/lib/matrix-waechter/stand")
SCAN_ABSTAND = int(os.environ.get("MATRIX_SCAN_ABSTAND", "30"))
SCAN_DAUER = float(os.environ.get("MATRIX_SCAN_DAUER", "8"))
PAUSE_MAX = int(os.environ.get("MATRIX_PAUSE_MAX", "600"))
STECKDOSE = os.environ.get("MATRIX_STECKDOSE", "").rstrip("/")   # leer = keine
AUS_SEKUNDEN = int(os.environ.get("MATRIX_AUS_SEKUNDEN", "10"))
NEUSTART_NACH = int(os.environ.get("MATRIX_NEUSTART_NACH", "3"))
NEUSTART_ABSTAND = int(os.environ.get("MATRIX_NEUSTART_ABSTAND", "900"))
# Täglicher Wechsel (23.11.2026): MATRIX_GIFS = Liste (Leerzeichen; ohne Pfad →
# /opt/matrix/gifs/), gewechselt zu jeder Uhrzeit in MATRIX_GIF_WECHSEL (z. B. "15:00" oder
# "05:30 15:00"); ab MATRIX_GIFS_START läuft das erste. Leer = nur MATRIX_GIF.
GIFS = os.environ.get("MATRIX_GIFS", "").split()
GIF_ORDNER = os.environ.get("MATRIX_GIF_ORDNER", "/opt/matrix/gifs")
GIF_WECHSEL = os.environ.get("MATRIX_GIF_WECHSEL", "15:00").split()
GIFS_START = os.environ.get("MATRIX_GIFS_START", "2026-11-23 15:00")
# Weitere Phasen: MATRIX_GIFS_2 ab MATRIX_GIFS_2_AB, MATRIX_GIFS_3 ab MATRIX_GIFS_3_AB … (z. B.
# Silvester ab 27.12., Neujahrsgruß ab 31.12. 23:58:40). Ein Phasenbeginn wird sekundengenau
# abgepasst. Nach MATRIX_ENDE (matrix_zeitplan.ENDE) tut der Wächter nichts mehr.
PHASEN = [(GIFS_START, GIFS)] + [
    (os.environ[f"MATRIX_GIFS_{i}_AB"], os.environ[f"MATRIX_GIFS_{i}"].split())
    for i in range(2, 10) if os.environ.get(f"MATRIX_GIFS_{i}") and os.environ.get(f"MATRIX_GIFS_{i}_AB")]
# Ohne Schaltsteckdose schaltet der Wächter die Anzeige nach dem Zeitplan per Bluetooth
# (71 23 = an, 71 24 = aus); der gemerkte Zustand steht in ANZEIGE.
ANZEIGE = os.environ.get("MATRIX_ANZEIGE_STAND", "/var/lib/matrix-waechter/anzeige")
HOCHLADEN_MAX = int(os.environ.get("MATRIX_HOCHLADEN_MAX", "150"))   # s je Versuch

log = logging.getLogger("matrix-waechter")


# ── reine Funktionen (testbar) ─────────────────────────────────────
def soll_stand(gif_bytes, name, tempo, hell):
    """Kennung für "dieses GIF mit diesen Einstellungen auf dieser Matrix"."""
    return f"{name} {hashlib.sha256(gif_bytes).hexdigest()[:16]} tempo={tempo} hell={hell}"


def stand_lesen(pfad=STAND):
    try:
        with open(pfad) as f:
            return f.read().strip()
    except OSError:
        return ""


def stand_schreiben(text, pfad=STAND):
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    tmp = pfad + ".neu"
    with open(tmp, "w") as f:
        f.write(text + "\n")
    os.replace(tmp, pfad)


def naechste_pause(fehlversuche, grund=SCAN_ABSTAND, hoechstens=PAUSE_MAX):
    """Wartezeit nach Fehlschlägen: 30 s, 60 s, 120 s … bis `hoechstens`."""
    return min(grund * 2 ** max(fehlversuche - 1, 0), hoechstens) if fehlversuche else grund


def neustart_noetig(fehlversuche, seit_letztem, nach=NEUSTART_NACH, abstand=NEUSTART_ABSTAND):
    """Grund für einen Strom-Neustart oder None. seit_letztem: s seit dem letzten (None = keiner)."""
    if seit_letztem is not None and seit_letztem < abstand:
        return None
    if fehlversuche >= nach:
        return f"{fehlversuche} Upload-Versuche gescheitert"
    return None


def passt(name, gesucht=MATRIX_NAME):
    return name.startswith("IOTBT") and (not gesucht or name == gesucht or name.endswith(gesucht))


def helligkeit(jetzt=None):
    """Aktuelle Soll-Helligkeit: nach Tageslicht (MATRIX_HELL_TAG/NACHT) oder fest HELL."""
    import datetime
    jetzt = jetzt or datetime.datetime.now(matrix_zeitplan.ZONE)
    h = matrix_zeitplan.hell_soll(jetzt)
    return HELL if h is None else h


def _uhrzeiten(texte):
    import datetime
    return sorted(datetime.time(*map(int, t.split(":"))) for t in texte)


def wechsel_nummer(jetzt, start, wechsel):
    """Wie viele Wechselzeitpunkte seit `start` (beide naiv oder beide mit Zone) vergangen sind."""
    zeiten = _uhrzeiten(wechsel)
    vorbei = lambda t: sum(1 for w in zeiten if t.time() >= w)  # noqa: E731
    tage = (jetzt.date() - start.date()).days
    return tage * len(zeiten) + vorbei(jetzt) - vorbei(start)


def gif_pfad(name):
    """Name aus der Liste → Pfad; Kurzname ohne .gif bekommt _64x16.gif angehängt."""
    if not name.endswith(".gif"):
        name += "_64x16.gif"
    return name if os.path.isabs(name) else os.path.join(GIF_ORDNER, name)


def _zeit(text, zone):
    import datetime
    return datetime.datetime.fromisoformat(text).replace(tzinfo=zone)


def phase_jetzt(jetzt, phasen):
    """(start, liste) der Phase, die zu `jetzt` gilt (die letzte, die schon begonnen hat)."""
    gueltig = [(_zeit(a, jetzt.tzinfo), liste) for a, liste in phasen if liste]
    gueltig.sort(key=lambda p: p[0])
    aktuell = gueltig[0]
    for start, liste in gueltig:
        if start <= jetzt:
            aktuell = (start, liste)
    return aktuell


def naechster_phasenbeginn(jetzt, phasen=None):
    starts = sorted(_zeit(a, jetzt.tzinfo) for a, liste in (phasen or PHASEN)[1:] if liste)
    return next((t for t in starts if t > jetzt), None)


def gif_jetzt(jetzt=None, gifs=None, start=None, wechsel=None, phasen=None):
    """Pfad des GIFs, das jetzt laufen soll."""
    import datetime
    if gifs is not None:                        # eine Liste ab `start` (für Tests)
        phasen = [(start.strftime("%Y-%m-%d %H:%M:%S") if start else GIFS_START, gifs)]
    phasen = phasen or PHASEN
    if not any(liste for _a, liste in phasen):
        return GIF
    jetzt = jetzt or datetime.datetime.now(matrix_zeitplan.ZONE)
    beginn, liste = phase_jetzt(jetzt, phasen)
    n = max(0, wechsel_nummer(jetzt, beginn, wechsel or GIF_WECHSEL)) if jetzt >= beginn else 0
    return gif_pfad(liste[n % len(liste)])


def wechsel_text(zeiten):
    """Für die Startzeile: wenige Zeiten einzeln, viele zusammengefasst (48 je Tag)."""
    if len(zeiten) <= 4:
        return "um " + " und ".join(zeiten)
    return f"{len(zeiten)}-mal am Tag ({zeiten[0]} … {zeiten[-1]})"


def stromlos_nach_zeitplan(jetzt, steckdose=None):
    """True, wenn die Steckdose die Matrix jetzt ausschaltet (oder schon aus hat): dann nicht
    suchen und nicht hochladen. Sonst begann um 08:30 ein Upload in derselben Sekunde, in der
    der Zeitplan die Steckdose ausschaltete, und scheiterte jeden Tag (24.11.2026)."""
    return bool(STECKDOSE if steckdose is None else steckdose) and not matrix_zeitplan.soll_an(jetzt)


def anzeige_soll(jetzt=None, steckdose=None):
    """'an'/'aus' nach Zeitplan, wenn KEINE Steckdose da ist; sonst None (Steckdose schaltet)."""
    import datetime
    if (STECKDOSE if steckdose is None else steckdose):
        return None
    jetzt = jetzt or datetime.datetime.now(matrix_zeitplan.ZONE)
    return "an" if matrix_zeitplan.soll_an(jetzt) else "aus"


async def anzeige_setzen(m, soll):
    """Anzeige ein- oder ausschalten (Verbindung steht schon)."""
    await m.senden(bytes([0x71, 0x23 if soll == "an" else 0x24]))


async def anzeige_schalten(name, soll):
    """Verbinden (schaltet die Anzeige an), bei 'aus' wieder ausschalten, trennen. True = geklappt."""
    m = Matrix(name)
    try:
        await asyncio.wait_for(m.verbinden(), 60)
        await anzeige_setzen(m, soll)
        return True
    except Exception as e:
        log.warning("Anzeige %s auf %s fehlgeschlagen: %s", soll, name, text(e))
        return False
    finally:
        try:
            await m.trennen()
        except Exception:
            pass


def text(e):
    return str(e) or type(e).__name__


# ── Steckdose und Bluetooth ────────────────────────────────────────
def steckdose(befehl, basis=STECKDOSE):
    """GET <basis>/<befehl> (ein|aus). True = Antwort 200."""
    try:
        with urllib.request.urlopen(f"{basis}/{befehl}", timeout=10) as r:
            return r.status == 200
    except OSError as e:
        log.warning("Steckdose %s/%s nicht erreichbar: %s", basis, befehl, e)
        return False


async def strom_neustart(grund):
    log.warning("Matrix-Neustart über die Steckdose: %s", grund)
    aus = steckdose("aus")
    await asyncio.sleep(AUS_SEKUNDEN)
    ein = steckdose("ein")
    if not ein:                                 # nie aus lassen
        await asyncio.sleep(5)
        ein = steckdose("ein")
    log.info("Steckdose aus=%s ein=%s, warte 20 s auf die Matrix", aus, ein)
    await asyncio.sleep(20)
    return ein


def haengende_trennen():
    """Trennt IOTBT-Verbindungen, die BlueZ offen hält (sonst taucht die Matrix nicht auf)."""
    try:
        out = subprocess.run(["bluetoothctl", "devices", "Connected"], capture_output=True,
                             text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError) as e:
        log.warning("bluetoothctl nicht nutzbar: %s", e)
        return []
    getrennt = []
    for adresse, name in re.findall(r"Device\s+([0-9A-F:]{17})\s+(\S+)", out, re.I):
        if passt(name):
            subprocess.run(["bluetoothctl", "disconnect", adresse], capture_output=True, timeout=15)
            log.info("Hängende Verbindung zu %s (%s) getrennt", name, adresse)
            getrennt.append(adresse)
    return getrennt


async def matrix_suchen():
    from bleak import BleakScanner
    for g in await BleakScanner.discover(timeout=SCAN_DAUER):
        if passt(g.name or ""):
            return g.name
    return None


def gif_holen(pfad, cache):
    """(bytes, bilder) für `pfad`, neu gelesen, wenn sich die Datei geändert hat; None bei
    fehlender oder zu großer Datei (einmal gemeldet). cache: Pfad → (mtime, daten)."""
    try:
        mtime = os.path.getmtime(pfad)
    except OSError:
        if cache.get(pfad, (None,))[0] != "fehlt":
            log.error("GIF nicht gefunden: %s", pfad)
        cache[pfad] = ("fehlt", None)
        return None
    if pfad in cache and cache[pfad][0] == mtime:
        return cache[pfad][1]
    bilder, _dauern = gif_bilder(pfad)
    daten = None
    if len(bilder) > MAX_BILDER:
        log.error("GIF %s hat %d Bilder, die Matrix nimmt höchstens %d – übersprungen",
                  pfad, len(bilder), MAX_BILDER)
    else:
        with open(pfad, "rb") as f:
            daten = (f.read(), bilder)
        if pfad in cache:
            log.info("GIF %s hat sich geändert, neu gelesen", os.path.basename(pfad))
    cache[pfad] = (mtime, daten)
    return daten


async def _verbinden_hochladen(m, bilder, hell, komprimiert):
    await m.verbinden()
    await hochladen(m, bilder, TEMPO, hell, komprimiert)
    if anzeige_soll() == "aus":                 # Verbinden hat die Anzeige eingeschaltet
        await anzeige_setzen(m, "aus")


async def einmal_hochladen(name, bilder, hell=HELL, komprimiert=None):
    """Verbinden, hochladen, trennen. True = geklappt."""
    m = Matrix(name)
    try:
        # Obergrenze für alles: bei schwachem Signal hing bleak hier schon > 3 min
        # (23.11.2026); 255 Bilder brauchen ~40 s, dazu bis 45 s Verbindungsaufbau.
        await asyncio.wait_for(_verbinden_hochladen(m, bilder, hell, komprimiert), HOCHLADEN_MAX)
        return True
    except Exception as e:
        log.warning("Hochladen auf %s fehlgeschlagen: %s", name, text(e))
        return False
    finally:
        try:
            await m.trennen()
        except Exception:
            pass


async def main():
    matrix_zeitplan.log_einrichten()
    namen = [g for _a, liste in PHASEN for g in liste]
    alle = list(dict.fromkeys(gif_pfad(g) for g in namen)) or [GIF]
    cache = {}                                  # Pfad → (mtime, (bytes, bilder))
    geladen = {p: gif_holen(p, cache) for p in alle}
    if not any(geladen.values()):
        log.error("Kein brauchbares GIF")
        sys.exit(2)                             # Dienst startet dann nicht endlos neu
    if matrix_zeitplan.HELL_TAG is None:
        hell_text = str(HELL)
    else:
        hell_text = (f"{matrix_zeitplan.HELL_TAG} ab Sonnenaufgang, {matrix_zeitplan.HELL_NACHT} ab "
                     f"{matrix_zeitplan.HELL_NACH_UNTERGANG} min nach Sonnenuntergang")
    if GIFS:
        gif_text = (f"{sum(1 for v in geladen.values() if v)} von {len(alle)} GIFs in {len(PHASEN)} "
                    f"Phasen, Wechsel {wechsel_text(GIF_WECHSEL)}, jetzt {os.path.basename(gif_jetzt())}")
    else:
        gif_text = GIF
    log.info("Matrix-Wächter gestartet, %s, Tempo %d, Helligkeit %s, Steckdose %s",
             gif_text, TEMPO, hell_text, STECKDOSE or "keine")
    haengende_trennen()
    fehlversuche, letzter_neustart, gemeldet = 0, None, None
    import datetime
    zone = matrix_zeitplan.ZONE
    while True:
        jetzt = datetime.datetime.now(zone)
        if matrix_zeitplan.ende_erreicht(jetzt):   # Saison vorbei: nichts mehr tun
            if gemeldet != "ende":
                log.info("Ende erreicht (%s) – keine Uploads und kein Einschalten mehr", matrix_zeitplan.ENDE)
                gemeldet = "ende"
            await asyncio.sleep(600)
            continue
        name = None
        if not stromlos_nach_zeitplan(jetzt):
            try:
                name = await matrix_suchen()
            except Exception as e:              # Bluetooth kurz weg o. ä.
                log.warning("Suche fehlgeschlagen: %s", e)
        jetzt = datetime.datetime.now(zone)
        beginn = naechster_phasenbeginn(jetzt)
        if beginn and (beginn - jetzt).total_seconds() <= 20:   # Phasenbeginn sekundengenau
            await asyncio.sleep(max(0.0, (beginn - datetime.datetime.now(zone)).total_seconds()))
            log.info("Phasenbeginn %s", beginn.strftime("%d.%m.%Y %H:%M:%S"))
        pfad = gif_jetzt()
        daten = gif_holen(pfad, cache)          # liest neu, wenn sich die Datei geändert hat
        if name and daten is None:              # fehlt/zu groß: nichts hochladen
            name = None
        if name:
            gif_bytes, bilder = daten
            hell = helligkeit()
            soll = soll_stand(gif_bytes, name, TEMPO, hell)
            if stand_lesen() == soll:
                if gemeldet != soll:
                    log.info("%s hat das GIF schon (%s), nichts zu tun", name, soll)
                    gemeldet = soll
            else:
                vorrat = vorrat_lesen(gif_bytes)
                if vorrat and sum(map(len, vorrat)) > MAX_BYTES:          # zu groß: Matrix würde hängen
                    if gemeldet != "gross " + pfad:
                        log.error("%s ist komprimiert %d Bytes, zu groß (höchstens %d) – übersprungen",
                                  os.path.basename(pfad), sum(map(len, vorrat)), MAX_BYTES)
                        gemeldet = "gross " + pfad
                    await asyncio.sleep(naechste_pause(0))
                    continue
                log.info("%s: lade %s hoch (%s)", name, os.path.basename(pfad), soll)
                if await einmal_hochladen(name, bilder, hell, vorrat):
                    stand_schreiben(soll)
                    fehlversuche, gemeldet = 0, soll
                    if anzeige_soll():
                        stand_schreiben(anzeige_soll(), ANZEIGE)
                else:
                    fehlversuche += 1
            anzeige = anzeige_soll()                # ohne Steckdose: Anzeige nach Zeitplan
            if anzeige and stand_lesen(ANZEIGE) != anzeige:
                if await anzeige_schalten(name, anzeige):
                    stand_schreiben(anzeige, ANZEIGE)
                    log.info("Anzeige %s (Zeitplan, ohne Steckdose)", anzeige)
        if STECKDOSE:
            seit = None if letzter_neustart is None else time.monotonic() - letzter_neustart
            grund = neustart_noetig(fehlversuche, seit)
            if grund:
                await strom_neustart(grund)
                letzter_neustart, fehlversuche = time.monotonic(), 0
                continue
        pause = naechste_pause(fehlversuche)
        jetzt = datetime.datetime.now(zone)
        beginn = naechster_phasenbeginn(jetzt)
        if beginn:                              # rechtzeitig vorher suchen
            pause = min(pause, max(1.0, (beginn - jetzt).total_seconds() - SCAN_DAUER - 6))
        await asyncio.sleep(pause)


if __name__ == "__main__":
    asyncio.run(main())
