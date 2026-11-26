#!/usr/bin/env python3
"""Erzeugt die Wechsellisten (MATRIX_GIFS…) für den Matrix-Wächter: Wechsel alle 15 Minuten
(vorher 30).
Alle Daten (Adventssonntage, Nikolaus, Weihnachten, Silvester, Ende) entstehen aus dem Jahr:
ab Juli gilt die kommende Saison (MATRIX_JAHR=2027 erzwingt Neujahr 2027). Danach die
Silvester-Animationen neu erzeugen (Jahreszahl), sie heißen dann neujahr_<Jahr>.
Ursprünglich (23.11.2026) jede Phase als exakte Liste von Plätzen (je SCHRITT) ab ihrem Beginn.

Regeln:
  - Animationen nur auf Plätze, in denen die Matrix an ist (Zeitplan + Sonnenuntergang);
    ein unsichtbarer Platz bekommt dasselbe GIF wie der nächste sichtbare (kein Upload bei aus).
  - Vor dem 1. Advent: allgemeine Winter-/Vorweihnachts-Animationen.
  - Adventswochen (ab 29.11., 6.12., 13.12., 20.12. 05:30): Kranz der Woche Sonntag früh
    06:30 und 07:30, Sonntagabend zu jeder vollen Stunde, Mittwoch und Freitag 18:00;
    Adventskalender täglich 17:00; Nikolaus am 6.12. früh 07:00/08:00 und abends zur
    halben Stunde.
  - Weihnachten 25./26.12. (Grüße), Silvester ab 27.12. (31.12.: 23:00 Feuerwerk, 23:30 Countdown),
    Neujahrsgruß 31.12. 23:59:18.
  - Übrige reihum, nie zweimal hintereinander.

Aufruf:  python3 pi/plan_erzeugen.py            schreibt den Block in die Vorlage
         python3 pi/plan_erzeugen.py --zeigen   Plan Tag für Tag ausgeben
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matrix_zeitplan as zp  # noqa: E402

Z = zp.ZONE
SCHRITT = datetime.timedelta(minutes=15)                         # 25.11.2026 (vorher 30)
WECHSEL = " ".join(f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15))

ALLGEMEIN = ["kamin", "schlittenflug", "polarlicht", "lebkuchen", "zug", "glocken", "pinguine",
             "weihnachtsmarkt", "rentier", "schneeballschlacht", "auspacken", "lichterhaus",
             "eislaufen", "plaetzchen", "futterhaus", "werkstatt", "winterwald", "schneeflocken",
             "baum_schmuecken", "rodeln", "wunschzettel", "bratapfel", "geschenkeberg", "stadt_schnee",
             "weihnachtsmann_rentier",
             # Winter
             "skifahrer", "schneepflug", "schneekugel", "hundeschlitten", "eisbaer", "iglu", "eule",
             "schneemann_bauen"]
ADVENT_EXTRA = ["hirten", "krippe", "stille_nacht"]          # erst im Advent
WEIHNACHTEN = ["weihnacht_bunt", "krippe", "hohoho", "stille_nacht", "schneemann", "auspacken",
               "hirten", "baum_schmuecken", "geschenkeberg", "rentier"]
SILVESTER = ["feuerwerk", "countdown", "sekt", "gluecksbringer", "jahreswechsel"]
# Erzgebirge, Schwarzwald und Katze: im allgemeinen Wechsel und an Weihnachten
HEIMAT = ["kuckucksuhr", "schwibbogen", "nussknacker", "schwarzwald", "katze_baum", "pyramide", "raeuchermann", "glasblaeser", "schneesturm"]
ALLGEMEIN += HEIMAT
WEIHNACHTEN += HEIMAT
# Weitere: Silvester ab 27.12., Winter allgemein, Weihnachten auch am 25./26.
SILVESTER_NEU = ["gluecksschwein", "rakete", "kirchturm", "wunderkerzen", "wachsgiessen", "spaziergang", "raclette", "feuerzangenbowle", "neujahrsbrezel", "schornsteinfeger", "tischfeuerwerk", "silvesterparty"]
SILVESTER += SILVESTER_NEU
WINTER_NEU = ["kirschtorte", "hermelin", "muehle", "holzfaeller", "pistenraupe", "wasserfall", "eishockey", "eichhoernchen", "rentier_flugschule", "maronen", "rotkehlchen", "igel", "eisstock", "schneehase", "schneeschuh", "sternschnuppen"]
ALLGEMEIN += WINTER_NEU
FEST_NEU = ["weihnachtsmann_kamin", "kerze", "christkind", "barbarazweig", "wichtel_teig", "christbaumkauf", "postbote", "gluehwein", "strohsterne", "windlichter"]
ALLGEMEIN += FEST_NEU
WEIHNACHTEN += FEST_NEU
WEIHNACHT_NEU = ["bescherung", "festessen", "christmette", "orgel", "krippenspiel"]                                           # nur am 25./26.12.
WEIHNACHTEN += WEIHNACHT_NEU


# Geschichten: Statt reihum laufen die Animationen als kleine Geschichten
# nacheinander. Jede Phase nimmt aus dieser Reihenfolge, was in ihrem Vorrat ist; noch nicht
# eingespielte Namen (Ideenliste) werden übersprungen und erscheinen von selbst, sobald es sie gibt.
# Was in keiner Geschichte steht, läuft am Ende jeder Runde.
GESCHICHTEN = [
    ("Im verschneiten Dorf", ["stadt_schnee", "schneepflug", "postbote", "lichterhaus", "windlichter",
                              "schneekugel", "zug"]),
    ("Weihnachtsmarkt", ["christbaumkauf", "weihnachtsmarkt", "gluehwein", "maronen", "lebkuchen", "glocken"]),
    ("Weihnachtsbäckerei", ["plaetzchen", "wichtel_teig", "bratapfel", "kirschtorte", "strohsterne"]),
    ("Beim Weihnachtsmann", ["wunschzettel", "werkstatt", "geschenkeberg", "rentier_flugschule", "rentier",
                             "weihnachtsmann_rentier", "schlittenflug", "weihnachtsmann_kamin"]),
    ("Kinder im Schnee", ["schneemann_bauen", "schneeballschlacht", "rodeln", "iglu", "eislaufen", "eishockey",
                          "eisstock", "skifahrer", "pistenraupe", "schneeschuh"]),
    ("Tiere im Winterwald", ["futterhaus", "rotkehlchen", "eichhoernchen", "hermelin", "winterwald",
                             "schneehase", "igel", "eule", "sternschnuppen", "schneeflocken"]),
    ("Schwarzwald", ["holzfaeller", "muehle", "wasserfall", "glasblaeser", "kuckucksuhr", "schneesturm",
                     "schwarzwald"]),
    ("Weihnachtsstube", ["barbarazweig", "kerze", "schwibbogen", "pyramide", "nussknacker", "raeuchermann",
                         "katze_baum", "kamin"]),
    ("Hoher Norden", ["hundeschlitten", "eisbaer", "pinguine", "polarlicht"]),
    ("Heilige Nacht", ["hirten", "krippe", "krippenspiel", "christmette", "orgel", "stille_nacht"]),
    ("Heiligabend zu Hause", ["baum_schmuecken", "christkind", "bescherung", "auspacken", "festessen"]),
    ("Weihnachtsgrüße", ["weihnacht_bunt", "hohoho", "schneemann"]),
    ("Zwischen den Jahren", ["spaziergang", "raclette", "feuerzangenbowle", "neujahrsbrezel", "wachsgiessen"]),
    ("Silvesternacht", ["gluecksschwein", "schornsteinfeger", "gluecksbringer", "tischfeuerwerk",
                        "silvesterparty", "sekt", "kirchturm", "rakete", "wunderkerzen", "feuerwerk",
                        "jahreswechsel", "countdown"]),
]


def ordnen(pool):
    """Vorrat einer Phase in Geschichten-Reihenfolge (jeder Name einmal), Rest am Ende."""
    pool = list(dict.fromkeys(pool))
    geordnet = [n for _, namen in GESCHICHTEN for n in namen if n in pool]
    geordnet = list(dict.fromkeys(geordnet))
    return geordnet + [n for n in pool if n not in geordnet]


def neues_jahr(heute=None):
    """Das Jahr, das an Silvester beginnt (ab Juli das folgende); MATRIX_JAHR setzt es fest."""
    if os.environ.get("MATRIX_JAHR"):
        return int(os.environ["MATRIX_JAHR"])
    heute = heute or datetime.date.today()
    return heute.year + 1 if heute.month >= 7 else heute.year


NEU = neues_jahr()
JAHR = NEU - 1                                                   # Jahr der Adventszeit


def adventssonntage(jahr):
    """1.–4. Advent: der 4. ist der Sonntag am oder vor dem 24.12."""
    heilig = datetime.date(jahr, 12, 24)
    vierter = heilig - datetime.timedelta(days=(heilig.weekday() + 1) % 7)
    return [vierter - datetime.timedelta(weeks=3 - k) for k in range(4)]


def _um(d, h, m, s=0):
    return datetime.datetime(d.year, d.month, d.day, h, m, s, tzinfo=Z)


ADVENTE = [_um(d, 5, 30) for d in adventssonntage(JAHR)]
START = ADVENTE[0] - datetime.timedelta(days=7)                  # eine Woche vor dem 1. Advent
NIKOLAUS = datetime.date(JAHR, 12, 6)
WEIHNACHT_AB = _um(datetime.date(JAHR, 12, 25), 5, 30)
SILVESTER_AB = _um(datetime.date(JAHR, 12, 27), 5, 30)
SILVESTER_TAG = datetime.date(JAHR, 12, 31)
NEUJAHR_AB = f"{JAHR}-12-31 23:59:18"                    # Upload ~42 s (70 KB) → läuft um 0 Uhr
ENDE = _um(datetime.date(NEU, 1, 1), 1, 0)
ENDE_TEXT = f"{NEU}-01-01 01:00"
EXTRA = [f"{JAHR}-12-31T21:30/{NEU}-01-01T01:00"]


def sichtbar(t):
    """Ist die Matrix im Platz (SCHRITT) ab t irgendwann an?"""
    return any(zp.soll_an(t + datetime.timedelta(minutes=m), extra=EXTRA, ende=ENDE_TEXT)
               for m in range(0, SCHRITT.seconds // 60, 5))


def fest(t, woche):
    """Fester Platz (Kranz, Kalender, Nikolaus, Silvester-Abend) oder None."""
    if t.date() == SILVESTER_TAG:                               # zu Mitternacht hin
        if (t.hour, t.minute) == (23, 0):
            return "feuerwerk"
        if (t.hour, t.minute) in ((23, 30), (23, 45)):          # die letzte halbe Stunde
            return "countdown"
    hm, tag = (t.hour, t.minute), (t.date() - ADVENTE[woche].date()).days if woche is not None else None
    if woche is None or woche < 0:
        return None
    kranz = f"advent{woche + 1}"
    if t.date() == NIKOLAUS:                                    # Nikolaus und 2. Advent
        if hm in ((7, 0), (8, 0)) or (t.hour >= 16 and t.minute == 30):
            return "nikolaus"
        if hm in ((6, 30), (7, 30)) or (t.hour >= 16 and t.minute == 0):
            return kranz
    if tag == 0 and (hm in ((6, 30), (7, 30)) or (t.hour >= 16 and t.minute == 0)):
        return kranz                                            # Sonntag
    if tag in (3, 5) and hm == (18, 0):                         # Mittwoch, Freitag
        return kranz
    if hm == (17, 0):
        return "adventskalender"
    return None


def phase_liste(von, bis, pool, woche=None, zaehler=None):
    """Liste der GIF-Namen je Platz (SCHRITT) von `von` bis `bis`."""
    plaetze = []
    t = von
    while t < bis:
        plaetze.append(t)
        t += SCHRITT
    namen = [None] * len(plaetze)
    letzter = None
    for i, t in enumerate(plaetze):
        if not sichtbar(t):
            continue
        name = fest(t, woche)
        if name is None:
            for _ in range(len(pool)):
                kandidat = pool[zaehler[0] % len(pool)]
                zaehler[0] += 1
                if kandidat != letzter:
                    name = kandidat
                    break
        namen[i] = letzter = name
    for i in range(len(namen) - 1, -1, -1):                     # unsichtbar: wie der nächste sichtbare
        if namen[i] is None:
            namen[i] = namen[i + 1] if i + 1 < len(namen) else letzter
    return namen


def plan():
    zaehler = [0]
    phasen = [(START, phase_liste(START, ADVENTE[0], ordnen(ALLGEMEIN), None, zaehler))]
    for w, ab in enumerate(ADVENTE):
        bis = ADVENTE[w + 1] if w + 1 < len(ADVENTE) else WEIHNACHT_AB
        phasen.append((ab, phase_liste(ab, bis, ordnen(ALLGEMEIN + ADVENT_EXTRA), w, zaehler)))
    phasen.append((WEIHNACHT_AB, phase_liste(WEIHNACHT_AB, SILVESTER_AB, ordnen(WEIHNACHTEN), None, [0])))
    phasen.append((SILVESTER_AB, phase_liste(SILVESTER_AB, ENDE, ordnen(SILVESTER), -1, [0])))
    return phasen


def block(phasen):
    zeilen = ["# Wechsellisten, erzeugt mit pi/plan_erzeugen.py (nicht von Hand ändern): alle 15 Minuten",
              "# ein Platz je Viertelstunde ab Phasenbeginn; Namen ohne _64x16.gif. Phasen: 1 vor Advent,",
              "# 2–5 Adventswochen, 6 Weihnachten, 7 Silvester, 8 Neujahrsgruß.",
              f'MATRIX_GIF_WECHSEL="{WECHSEL}"']
    for i, (ab, liste) in enumerate(phasen, 1):
        name = "MATRIX_GIFS" if i == 1 else f"MATRIX_GIFS_{i}"
        zeilen.append(f'{name}="{" ".join(liste)}"')
        zeilen.append(f'MATRIX_GIFS_START="{ab:%Y-%m-%d %H:%M}"' if i == 1 else f'{name}_AB="{ab:%Y-%m-%d %H:%M}"')
    zeilen.append(f'MATRIX_GIFS_8="neujahr_{NEU}"')
    zeilen.append(f'MATRIX_GIFS_8_AB="{NEUJAHR_AB}"')
    zeilen.append(f'MATRIX_ZEITPLAN_EXTRA="{EXTRA[0]}"')
    zeilen.append(f'MATRIX_ENDE="{ENDE_TEXT}"')
    return "\n".join(zeilen) + "\n"


def zeigen(phasen):
    for ab, liste in phasen:
        t, vorher = ab, None
        for name in liste:
            if sichtbar(t) and name != vorher:
                print(f"{t:%a %d.%m. %H:%M}  {name}")
            if sichtbar(t):
                vorher = name
            t += SCHRITT


if __name__ == "__main__":
    phasen = plan()
    if "--zeigen" in sys.argv:
        zeigen(phasen)
        sys.exit(0)
    vorlage = os.path.join(os.path.dirname(os.path.abspath(__file__)), "matrix-waechter.default")
    with open(vorlage) as f:
        s = f.read()
    s = re.sub(r'^MATRIX_GIF_WECHSEL=.*\n', '', s, flags=re.M)
    s = re.sub(r'^MATRIX_(ZEITPLAN_EXTRA|ENDE)=.*\n', '', s, flags=re.M)
    s = re.sub(r'^MATRIX_GIFS(_\d)?(_AB|_START)?=.*\n', '', s, flags=re.M)
    s = re.sub(r'^# Wechsellisten.*\n(^#.*\n)*', '', s, flags=re.M)
    s = s.rstrip("\n") + "\n" + block(phasen)
    with open(vorlage, "w") as f:
        f.write(s)
    print(f"{sum(len(l) for _, l in phasen)} Plätze in {len(phasen) + 1} Phasen geschrieben")
