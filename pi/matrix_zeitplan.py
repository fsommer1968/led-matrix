#!/usr/bin/env python3
"""Schaltet die Matrix über die Schaltsteckdose nach Zeitplan ein und aus.

Standard (24.11.2026): morgens 06:30–08:30, abends von 30 min vor Sonnenuntergang
bis 21:30. Der Pi bleibt immer an; die Matrix behält ihre Animation auch ohne Strom und
spielt sie nach dem Einschalten von selbst.

Läuft jede Minute über matrix-zeitplan.timer: Soll-Zustand berechnen, Steckdose lesen
(PIN Status … ein/aus) und nur bei Abweichung schalten – so wird auch ein Schalten von Hand
in der nächsten Minute wieder zurechtgerückt.

Sonnenuntergang nach der NOAA-Näherung (auf etwa 1–2 min genau), für MATRIX_BREITE/LAENGE
(Standard Freiburg im Breisgau 47,995 / 7,849, in den Einstellungen anpassen).

Sonderzeiten: MATRIX_ZEITPLAN_EXTRA (zusätzliche Fenster), MATRIX_ENDE (danach immer aus).

Aufruf:  matrix_zeitplan.py            einmal prüfen und schalten (für den Timer)
         matrix_zeitplan.py plan [N]   Schaltzeiten der nächsten N Tage zeigen (Standard 7)
"""
import datetime
import logging
import math
import os
import re
import sys
import urllib.request
from zoneinfo import ZoneInfo

STECKDOSE = os.environ.get("MATRIX_STECKDOSE", "").rstrip("/")
BREITE = float(os.environ.get("MATRIX_BREITE", "47.995"))
LAENGE = float(os.environ.get("MATRIX_LAENGE", "7.849"))
MORGEN = os.environ.get("MATRIX_ZEITPLAN_MORGEN", "06:30-08:30")       # leer = kein Morgen
ABEND_VOR = int(os.environ.get("MATRIX_ZEITPLAN_ABEND_VOR", "30"))       # min vor Untergang
ABEND_BIS = os.environ.get("MATRIX_ZEITPLAN_ABEND_BIS", "21:30")         # leer = kein Abend
ZONE = ZoneInfo(os.environ.get("MATRIX_ZEITZONE", "Europe/Berlin"))
# Helligkeit nach Tageslicht (23.11.2026): HELL_TAG von Sonnenaufgang bis
# HELL_NACH_UNTERGANG min nach Sonnenuntergang, sonst HELL_NACHT. Leer = feste MATRIX_HELL.
_tag, _nacht = os.environ.get("MATRIX_HELL_TAG", ""), os.environ.get("MATRIX_HELL_NACHT", "")
HELL_TAG = int(_tag) if _tag.strip() else None
HELL_NACHT = int(_nacht) if _nacht.strip() else None
HELL_NACH_UNTERGANG = int(os.environ.get("MATRIX_HELL_NACH_UNTERGANG", "30"))
# Zusätzliche Einschaltzeiten "VON/BIS" (ISO, mit Leerzeichen getrennt), z. B. Silvester
# "2026-12-31T22:00/2027-01-01T01:00"; ab MATRIX_ENDE bleibt die Matrix für immer aus.
EXTRA = os.environ.get("MATRIX_ZEITPLAN_EXTRA", "").split()
ENDE = os.environ.get("MATRIX_ENDE", "").strip()


def _zeitpunkt(text, zone=ZONE):
    return datetime.datetime.fromisoformat(text).replace(tzinfo=zone)


def ende_erreicht(jetzt, ende=ENDE, zone=ZONE):
    return bool(ende) and jetzt >= _zeitpunkt(ende, zone)

TAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

log = logging.getLogger("matrix-zeitplan")


class _JournalFormat(logging.Formatter):
    """Unter systemd: Stufe als <N>-Vorsatz fürs Journal, ohne eigene Uhrzeit (die setzt journald)."""
    STUFE = {logging.DEBUG: 7, logging.WARNING: 4, logging.ERROR: 3, logging.CRITICAL: 2}

    def format(self, record):
        n = self.STUFE.get(record.levelno)
        text = super().format(record)
        return text if n is None else f"<{n}>{text}"     # INFO: Stufe aus SyslogLevel= der Unit


def log_einrichten(level=logging.INFO):
    """Ausgabe nach stdout: im Journal mit Stufe, von Hand gestartet mit Uhrzeit."""
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(_JournalFormat("%(message)s") if os.environ.get("JOURNAL_STREAM")
                   else logging.Formatter("%(asctime)s %(message)s"))
    logging.basicConfig(level=level, handlers=[h])


# ── reine Funktionen (testbar) ─────────────────────────────────────
def sonnenuntergang(datum, breite=BREITE, laenge=LAENGE, zone=ZONE):
    """Sonnenuntergang (Ortszeit, mit Zeitzone) am `datum` nach der NOAA-Näherung."""
    return _sonne(datum, breite, laenge, zone, aufgang=False)


def sonnenaufgang(datum, breite=BREITE, laenge=LAENGE, zone=ZONE):
    """Sonnenaufgang (Ortszeit, mit Zeitzone) am `datum` nach der NOAA-Näherung."""
    return _sonne(datum, breite, laenge, zone, aufgang=True)


def _sonne(datum, breite, laenge, zone, aufgang):
    n = datum.timetuple().tm_yday
    stunde = 6 if aufgang else 18
    g = 2 * math.pi / 365 * (n - 1 + (stunde - 12) / 24)    # Bruchteil des Jahres
    zgl = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    dekl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g)
            - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
            - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    phi = math.radians(breite)
    cos_ha = (math.cos(math.radians(90.833)) / (math.cos(phi) * math.cos(dekl))
              - math.tan(phi) * math.tan(dekl))
    ha = math.degrees(math.acos(max(-1.0, min(1.0, cos_ha))))
    minuten_utc = 720 - 4 * (laenge + ha if aufgang else laenge - ha) - zgl
    mitternacht = datetime.datetime(datum.year, datum.month, datum.day, tzinfo=datetime.timezone.utc)
    return (mitternacht + datetime.timedelta(minutes=minuten_utc)).astimezone(zone)


def _uhrzeit(datum, hhmm, zone=ZONE):
    h, m = map(int, hhmm.split(":"))
    return datetime.datetime(datum.year, datum.month, datum.day, h, m, tzinfo=zone)


def fenster(datum, morgen=MORGEN, abend_vor=ABEND_VOR, abend_bis=ABEND_BIS,
            breite=BREITE, laenge=LAENGE, zone=ZONE):
    """Liste der Einschaltfenster [(von, bis), …] am `datum` (Ortszeit)."""
    f = []
    if morgen:
        von, bis = morgen.split("-")
        f.append((_uhrzeit(datum, von, zone), _uhrzeit(datum, bis, zone)))
    if abend_bis:
        von = sonnenuntergang(datum, breite, laenge, zone) - datetime.timedelta(minutes=abend_vor)
        von = von.replace(second=0, microsecond=0)
        bis = _uhrzeit(datum, abend_bis, zone)
        if von < bis:                           # im Hochsommer kann der Abend entfallen
            f.append((von, bis))
    return f


def soll_an(jetzt, extra=None, ende=None, **kw):
    """True, wenn die Matrix zum Zeitpunkt `jetzt` (mit Zeitzone) an sein soll."""
    zone = kw.get("zone", ZONE)
    if ende_erreicht(jetzt, ENDE if ende is None else ende, zone):
        return False
    for teil in (EXTRA if extra is None else extra):
        von, bis = (_zeitpunkt(t, zone) for t in teil.split("/"))
        if von <= jetzt < bis:
            return True
    return any(von <= jetzt < bis for von, bis in fenster(jetzt.date(), **kw))


def hell_wechsel(datum, nach=HELL_NACH_UNTERGANG, breite=BREITE, laenge=LAENGE, zone=ZONE):
    """(hell_ab, dunkel_ab): Sonnenaufgang und `nach` Minuten nach Sonnenuntergang."""
    auf = sonnenaufgang(datum, breite, laenge, zone).replace(second=0, microsecond=0)
    ab = sonnenuntergang(datum, breite, laenge, zone) + datetime.timedelta(minutes=nach)
    return auf, ab.replace(second=0, microsecond=0)


def hell_soll(jetzt, tag=HELL_TAG, nacht=HELL_NACHT, **kw):
    """Helligkeit zum Zeitpunkt `jetzt`: `tag` von Sonnenaufgang bis `nach` min nach
    Sonnenuntergang, sonst `nacht`. Ohne `tag` (None) → None (feste Helligkeit)."""
    if tag is None:
        return None
    auf, ab = hell_wechsel(jetzt.date(), **kw)
    return tag if auf <= jetzt < ab else (nacht if nacht is not None else tag)


def status_lesen(seite):
    """Aus der Startseite des Schaltaktors: True (ein), False (aus) oder None."""
    m = re.search(r"PIN Status\s*:.*\b(ein|aus)\s*$", seite, re.M)
    return None if not m else m.group(1) == "ein"


# ── Steckdose ──────────────────────────────────────────────────────
def _get(pfad, basis=STECKDOSE):
    with urllib.request.urlopen(f"{basis}/{pfad}", timeout=10) as r:
        return r.read().decode("utf-8", "replace")


def einmal():
    jetzt = datetime.datetime.now(ZONE)
    soll = soll_an(jetzt)
    try:
        ist = status_lesen(_get(""))
    except OSError as e:
        log.warning("Steckdose %s nicht erreichbar: %s", STECKDOSE, e)
        return 1
    if ist == soll:
        return 0
    befehl = "ein" if soll else "aus"
    try:
        antwort = _get(befehl).strip()
    except OSError as e:
        log.warning("Steckdose %s/%s nicht erreichbar: %s", STECKDOSE, befehl, e)
        return 1
    log.info("Matrix %s (Zeitplan; vorher %s): %s", befehl,
             {True: "ein", False: "aus", None: "unbekannt"}[ist], antwort)
    return 0


def plan(tage=7):
    heute = datetime.datetime.now(ZONE).date()
    for i in range(tage):
        d = heute + datetime.timedelta(days=i)
        sa, su = sonnenaufgang(d), sonnenuntergang(d)
        teile = [f"{v:%H:%M}–{b:%H:%M}" for v, b in fenster(d)]
        zeile = (f"{TAGE[d.weekday()]} {d:%d.%m.%Y}  Sonne {sa:%H:%M}–{su:%H:%M}  "
                 f"an: {', '.join(teile) or '–'}")
        for teil in EXTRA:
            von, bis = (_zeitpunkt(t) for t in teil.split("/"))
            if von.date() == d:
                zeile += f", extra {von:%H:%M}–{bis:%d.%m. %H:%M}"
        if ENDE and _zeitpunkt(ENDE).date() <= d:
            zeile += f"  ENDE ab {_zeitpunkt(ENDE):%d.%m.%Y %H:%M}: aus"
        if HELL_TAG is not None:
            auf, ab = hell_wechsel(d)
            zeile += f"  Helligkeit {HELL_TAG} von {auf:%H:%M} bis {ab:%H:%M}, sonst {HELL_NACHT}"
        print(zeile)


if __name__ == "__main__":
    log_einrichten()
    if len(sys.argv) > 1 and sys.argv[1] == "plan":
        plan(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
        sys.exit(0)
    if not STECKDOSE:                           # Steckdose ist optional: dann nichts schalten
        sys.exit(0)
    sys.exit(einmal())
