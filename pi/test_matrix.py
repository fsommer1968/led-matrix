"""Tests für Abspieler und Wächter ohne Bluetooth.  Aufruf: python3 -m unittest led/pi/test_matrix.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import matrix_spieler as sp  # noqa: E402
import matrix_waechter as mw  # noqa: E402
import matrix_upload as mu  # noqa: E402
import a2pl  # noqa: E402
import matrix_zeitplan as zp  # noqa: E402

# Aus dem Mitschnitt der iPhone-App vom 23.11.2026 (Test-GIF led/test_app_64x16.gif)
APP_KOPF = "ea010100001800000000000000000000000000000000000003000000000000000000000000000000"
APP_TABELLE = "ea020000000000140000001400180000002c0013"
APP_BILDER = ["3f001f000100ffffffffffffffec500000000000",
              "3f01ff0001000a0f2000ffffffffffffffcf500000000000",
              "2f51ff0200ffffffffffffffed50ff51ff51ff"]


class Farben(unittest.TestCase):
    def test_werte_wie_am_geraet_geprueft(self):
        self.assertEqual(sp.hsv16(255, 0, 0), 0x01FF)      # rot
        self.assertEqual(sp.hsv16(255, 255, 255), 0x001F)  # weiß
        self.assertEqual(sp.hsv16(0, 0, 0), 0x0000)        # schwarz
        self.assertEqual(sp.hsv16(0, 255, 0) >> 9, 42)     # grün, Farbton 1/3


class Maske(unittest.TestCase):
    def test_zeilenweise_ab_links_oben(self):
        # Am Gerät: erste 64 Bits = oberste Zeile, erste 16 = linker Anfang davon
        self.assertEqual(sp.maske(range(64)), b"\xff" * 8 + bytes(120))
        m = sp.maske([0, 9, 1023])
        self.assertEqual((m[0], m[1], m[127]), (0x80, 0x40, 0x01))
        self.assertEqual(len(m), 128)


class Befehle(unittest.TestCase):
    def test_erstes_bild_fuellt_mit_haeufigster_farbe(self):
        bild = [0] * 1024
        bild[5] = 0x01FF
        bf = sp.befehle_fuer_bild(None, bild)
        self.assertEqual(bf[0], b"\xe2\x0b\x00\x00")
        self.assertEqual(bf[1], b"\xe2\x0c\x90\x01\xff" + sp.maske([5]))
        self.assertEqual(len(bf), 2)

    def test_nur_aenderungen_je_farbe(self):
        a = [0] * 1024
        b = list(a)
        b[1], b[2], b[3] = 0x01FF, 0x01FF, 0x001F
        bf = sp.befehle_fuer_bild(a, b)
        self.assertEqual(len(bf), 2)                         # zwei Farben geändert
        self.assertEqual(sp.befehle_fuer_bild(b, b), [])     # nichts geändert

    def test_zurueck_auf_schwarz(self):
        a = [0x01FF] * 1024
        bf = sp.befehle_fuer_bild(a, [0] * 1024)
        self.assertEqual(bf, [b"\xe2\x0c\x90\x00\x00" + b"\xff" * 128])


class Paket(unittest.TestCase):
    def test_kopf_wie_am_geraet(self):
        # Mitschnitt 23.11.2026: 01 03 80 00 00 05 00 06 0a ea 81 8a 8b 59
        self.assertEqual(sp.paket(3, b"\x0a\xea\x81\x8a\x8b\x59").hex(),
                         "01038000000500060aea818a8b59")


class Zeit(unittest.TestCase):
    def test_bild_zur_zeit(self):
        d = [0.1, 0.2, 0.1]
        self.assertEqual(sp.bild_zur_zeit(d, 0), 0)
        self.assertEqual(sp.bild_zur_zeit(d, 0.15), 1)
        self.assertEqual(sp.bild_zur_zeit(d, 0.35), 2)
        self.assertEqual(sp.bild_zur_zeit(d, 0.45), 0)       # Schleife


class Waechter(unittest.TestCase):
    def test_pause_waechst_bis_hoechstens(self):
        self.assertEqual([mw.naechste_pause(n, 30, 600) for n in range(7)],
                         [30, 30, 60, 120, 240, 480, 600])

    def test_name(self):
        self.assertTrue(mw.passt("IOTBT1A2", ""))
        self.assertTrue(mw.passt("IOTBT1A2", "1A2"))
        self.assertFalse(mw.passt("IOTBT1A2", "FC9"))
        self.assertFalse(mw.passt("BatteryProtect", ""))


class Wechsel(unittest.TestCase):
    import datetime as dt
    Z = zp.ZoneInfo("Europe/Berlin")
    START = dt.datetime(2026, 11, 23, 15, 0, tzinfo=Z)
    GIFS = ["a.gif", "b.gif", "c.gif"]

    def n(self, s, wechsel=("15:00",)):
        return mw.wechsel_nummer(self.dt.datetime.fromisoformat(s).replace(tzinfo=self.Z),
                                 self.START, list(wechsel))

    def test_einmal_am_tag_um_15(self):
        self.assertEqual(self.n("2026-11-23T18:00"), 0)
        self.assertEqual(self.n("2026-11-24T14:59"), 0)
        self.assertEqual(self.n("2026-11-24T15:00"), 1)
        self.assertEqual(self.n("2026-11-25T07:00"), 1)
        self.assertEqual(self.n("2026-12-24T16:00"), 31)

    def test_zweimal_am_tag(self):
        w = ("05:30", "15:00")
        self.assertEqual(self.n("2026-11-23T18:00", w), 0)
        self.assertEqual(self.n("2026-11-24T06:00", w), 1)
        self.assertEqual(self.n("2026-11-24T16:00", w), 2)

    def test_liste_beginnt_von_vorn(self):
        jetzt = lambda s: self.dt.datetime.fromisoformat(s).replace(tzinfo=self.Z)  # noqa: E731
        g = lambda s: mw.gif_jetzt(jetzt(s), self.GIFS, self.START, ["15:00"])  # noqa: E731
        self.assertEqual(g("2026-11-23T20:00"), os.path.join(mw.GIF_ORDNER, "a.gif"))
        self.assertTrue(g("2026-11-25T20:00").endswith("c.gif"))
        self.assertTrue(g("2026-11-26T20:00").endswith("a.gif"))
        self.assertEqual(mw.gif_jetzt(jetzt("2026-11-26T20:00"), ["/x/y.gif"], self.START, ["15:00"]),
                         "/x/y.gif")


class Silvester(unittest.TestCase):
    import datetime as dt
    Z = zp.ZoneInfo("Europe/Berlin")
    PHASEN = [("2026-11-23 15:00", ["w1.gif", "w2.gif"]),
              ("2026-12-27 05:30", ["s1.gif", "s2.gif", "s3.gif"]),
              ("2026-12-31 23:58:40", ["neujahr.gif"])]

    def t(self, s):
        return self.dt.datetime.fromisoformat(s).replace(tzinfo=self.Z)

    def g(self, s):
        return os.path.basename(mw.gif_jetzt(self.t(s), wechsel=["05:30", "15:00", "19:00"],
                                             phasen=self.PHASEN))

    def test_phasen(self):
        self.assertTrue(self.g("2026-12-27T05:29").startswith("w"))
        self.assertEqual(self.g("2026-12-27T05:30"), "s1.gif")
        self.assertEqual(self.g("2026-12-27T15:00"), "s2.gif")
        self.assertEqual(self.g("2026-12-27T19:00"), "s3.gif")
        self.assertEqual(self.g("2026-12-28T05:30"), "s1.gif")
        self.assertTrue(self.g("2026-12-31T23:58:39").startswith("s"))
        self.assertEqual(self.g("2026-12-31T23:58:40"), "neujahr.gif")
        self.assertEqual(self.g("2027-01-01T00:30"), "neujahr.gif")

    def test_naechster_phasenbeginn(self):
        self.assertEqual(mw.naechster_phasenbeginn(self.t("2026-12-31T23:58:20"), self.PHASEN),
                         self.t("2026-12-31T23:58:40"))
        self.assertIsNone(mw.naechster_phasenbeginn(self.t("2027-01-01T00:00"), self.PHASEN))

    def test_zeitplan_silvester_und_ende(self):
        kw = dict(morgen="06:00-08:30", abend_vor=30, abend_bis="22:00", zone=self.Z,
                  breite=47.995, laenge=7.849, extra=["2026-12-31T22:00/2027-01-01T01:00"],
                  ende="2027-01-01 01:00")
        an = lambda s: zp.soll_an(self.t(s), **kw)  # noqa: E731
        self.assertFalse(an("2026-12-30T22:30"))          # sonst ab 22:00 aus
        self.assertTrue(an("2026-12-31T22:30"))           # Silvester bis 01:00
        self.assertTrue(an("2027-01-01T00:59"))
        self.assertFalse(an("2027-01-01T01:00"))
        self.assertFalse(an("2027-01-01T06:30"))          # nie wieder an
        self.assertFalse(an("2027-01-15T17:00"))
        self.assertTrue(zp.ende_erreicht(self.t("2027-01-01T01:00"), "2027-01-01 01:00", self.Z))
        self.assertFalse(zp.ende_erreicht(self.t("2027-01-01T00:59"), "2027-01-01 01:00", self.Z))


class Groesse(unittest.TestCase):
    def test_zu_gross_wird_abgelehnt(self):
        import asyncio
        gross = [bytes(1000)] * 90                                      # 90 KB "komprimiert"
        with self.assertRaises(ValueError):
            asyncio.run(mu.hochladen(None, [bytes(2048)] * 90, komprimiert=gross))


class Jahr(unittest.TestCase):
    def test_adventssonntage_und_neues_jahr(self):
        import datetime as dt
        import plan_erzeugen as pe
        self.assertEqual(pe.adventssonntage(2026)[0], dt.date(2026, 11, 29))
        self.assertEqual(pe.adventssonntage(2028)[3], dt.date(2028, 12, 24))   # Heiligabend ist Sonntag
        self.assertEqual(pe.adventssonntage(2027)[3], dt.date(2027, 12, 19))
        self.assertEqual(pe.neues_jahr(dt.date(2026, 11, 24)), 2027)
        self.assertEqual(pe.neues_jahr(dt.date(2027, 1, 5)), 2027)


class AnzeigeOhneSteckdose(unittest.TestCase):
    def test_nur_ohne_steckdose(self):
        import datetime as dt
        t = dt.datetime(2026, 11, 24, 12, 0, tzinfo=zp.ZONE)                 # mittags: aus
        self.assertIsNone(mw.anzeige_soll(t, steckdose="http://x"))
        self.assertEqual(mw.anzeige_soll(t, steckdose=""), "aus")
        abends = dt.datetime(2026, 11, 24, 19, 0, tzinfo=zp.ZONE)
        self.assertEqual(mw.anzeige_soll(abends, steckdose=""), "an")


class StromlosNachZeitplan(unittest.TestCase):
    def test_nicht_hochladen_wenn_steckdose_aus(self):
        import datetime as dt
        mittags = dt.datetime(2026, 11, 24, 12, 0, tzinfo=zp.ZONE)
        abends = dt.datetime(2026, 11, 24, 19, 0, tzinfo=zp.ZONE)
        self.assertTrue(mw.stromlos_nach_zeitplan(mittags, steckdose="http://x"))
        self.assertFalse(mw.stromlos_nach_zeitplan(abends, steckdose="http://x"))
        self.assertFalse(mw.stromlos_nach_zeitplan(mittags, steckdose=""))   # ohne Steckdose: BLE


class Startzeile(unittest.TestCase):
    def test_wechselzeiten_kurz(self):
        self.assertEqual(mw.wechsel_text(["05:30", "15:00"]), "um 05:30 und 15:00")
        halb = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
        self.assertEqual(mw.wechsel_text(halb), "48-mal am Tag (00:00 … 23:30)")


class Journal(unittest.TestCase):
    def test_stufe_als_vorsatz(self):
        import logging
        f = zp._JournalFormat("%(message)s")
        rec = lambda lv: logging.LogRecord("x", lv, "", 0, "Text", None, None)  # noqa: E731
        self.assertEqual(f.format(rec(logging.INFO)), "Text")            # Stufe aus SyslogLevel=
        self.assertEqual(f.format(rec(logging.WARNING)), "<4>Text")
        self.assertEqual(f.format(rec(logging.ERROR)), "<3>Text")
        self.assertEqual(f.format(rec(logging.DEBUG)), "<7>Text")


class Kurznamen(unittest.TestCase):
    def test_gif_pfad(self):
        self.assertEqual(mw.gif_pfad("kamin"), os.path.join(mw.GIF_ORDNER, "kamin_64x16.gif"))
        self.assertEqual(mw.gif_pfad("x.gif"), os.path.join(mw.GIF_ORDNER, "x.gif"))
        self.assertEqual(mw.gif_pfad("/a/b.gif"), "/a/b.gif")


class Vorrat(unittest.TestCase):
    def test_schreiben_lesen_und_anlegen(self):
        import shutil
        import tempfile
        quelle = os.path.join(os.path.dirname(__file__), "..", "test_app_64x16.gif")
        with tempfile.TemporaryDirectory() as d:
            gif = os.path.join(d, "x.gif")
            shutil.copy(quelle, gif)
            with open(gif, "rb") as f:
                gb = f.read()
            self.assertIsNone(mu.vorrat_lesen(gb, d))
            self.assertTrue(mu.vorrat_anlegen(gif, d))
            self.assertFalse(mu.vorrat_anlegen(gif, d))                 # schon da
            bilder, _ = mu.gif_bilder(gif)
            self.assertEqual(mu.vorrat_lesen(gb, d), [a2pl.compress(b) for b in bilder])
            self.assertEqual([k.hex()[:16] for k in mu.vorrat_lesen(gb, d)][0][:4],
                             a2pl.compress(bilder[0]).hex()[:4])


class GifHolen(unittest.TestCase):
    def test_neu_lesen_bei_aenderung_und_fehlend(self):
        import shutil
        import tempfile
        quelle = os.path.join(os.path.dirname(__file__), "..", "test_app_64x16.gif")
        with tempfile.TemporaryDirectory() as d:
            pfad = os.path.join(d, "x.gif")
            cache = {}
            self.assertIsNone(mw.gif_holen(pfad, cache))                 # fehlt
            shutil.copy(quelle, pfad)
            erst = mw.gif_holen(pfad, cache)
            self.assertEqual(len(erst[1]), 3)
            self.assertIs(mw.gif_holen(pfad, cache), erst)               # unverändert: Zwischenspeicher
            os.utime(pfad, (1, 1))
            self.assertIsNot(mw.gif_holen(pfad, cache), erst)            # geändert: neu gelesen


class Adventskalender(unittest.TestCase):
    def test_laufschrift(self):
        import datetime
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "animationen"))
        import adventskalender as ak
        d = datetime.date
        self.assertEqual(ak.laufschrift(d(2026, 11, 23)), "NOCH 31 TAGE BIS WEIHNACHTEN")
        self.assertEqual(ak.laufschrift(d(2026, 12, 23)), "MORGEN IST HEILIGABEND")
        self.assertEqual(ak.laufschrift(d(2026, 12, 24)), "HEUTE IST HEILIGABEND")
        self.assertEqual(ak.laufschrift(d(2026, 12, 26)), "FROHE WEIHNACHTEN")
        self.assertEqual(len(ak.bilder(d(2026, 12, 1))), 255)

    def test_adventskranz_je_woche(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "animationen"))
        import advent
        self.assertEqual(advent.zuendzeiten(1), [100, None, None, None])
        self.assertEqual(advent.zuendzeiten(3), [55, 63, 100, None])
        self.assertIsNone(advent.einlauf_versatz(3, 4))                # noch nicht da
        self.assertEqual(advent.einlauf_versatz(4, 4), -14)             # fällt von oben
        self.assertEqual(advent.einlauf_versatz(30, 4), 0)              # steht
        self.assertEqual([v[0] for v in advent.VARIANTEN], ["advent1", "advent2", "advent3", "advent4"])


class Neustart(unittest.TestCase):
    def test_gruende_und_sperre(self):
        n = lambda f, seit=None: mw.neustart_noetig(f, seit, nach=3, abstand=900)  # noqa: E731
        self.assertIsNone(n(0))
        self.assertIsNone(n(2))
        self.assertIn("3 Upload-Versuche", n(3))
        self.assertIsNone(n(5, seit=100))                   # zu kurz nach dem letzten
        self.assertIsNotNone(n(5, seit=1000))

    def test_stand(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            pfad = os.path.join(d, "sub", "stand")
            self.assertEqual(mw.stand_lesen(pfad), "")
            soll = mw.soll_stand(b"GIF89a", "IOTBT1A2", 75, 100)
            mw.stand_schreiben(soll, pfad)
            self.assertEqual(mw.stand_lesen(pfad), soll)
        self.assertNotEqual(soll, mw.soll_stand(b"GIF89a", "IOTBT1A2", 50, 100))
        self.assertNotEqual(soll, mw.soll_stand(b"GIF89b", "IOTBT1A2", 75, 100))

    def test_steckdose_aufruf(self):
        import http.server
        import threading
        pfade = []

        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                pfade.append(self.path)
                self.send_response(200)
                self.end_headers()

            def log_message(self, *a):
                pass
        srv = http.server.HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.handle_request, daemon=True).start()
        self.assertTrue(mw.steckdose("aus", f"http://127.0.0.1:{srv.server_port}"))
        self.assertEqual(pfade, ["/aus"])
        srv.server_close()
        self.assertFalse(mw.steckdose("ein", f"http://127.0.0.1:{srv.server_port}"))


class Upload(unittest.TestCase):
    def test_kopf_und_tabelle_wie_app(self):
        self.assertEqual(mu.kopf(3).hex(), APP_KOPF)
        self.assertEqual(mu.tabelle([20, 24, 19]).hex(), APP_TABELLE)

    def test_a2pl_wie_app(self):
        for h in APP_BILDER:
            fb = a2pl.decompress(bytes.fromhex(h))
            self.assertEqual(len(fb), 2048)
            self.assertEqual(a2pl.compress(fb).hex(), h)

    def test_bilder_spaltenweise_wie_app(self):
        schwarz, weiss, rot = (0, 0, 0), (255, 255, 255), (255, 0, 0)
        b1 = [schwarz] * 1024
        b1[0] = weiss                                        # Pixel links oben
        b2 = [rot if i < 64 else schwarz for i in range(1024)]   # oberste Zeile
        self.assertEqual(a2pl.compress(mu.bild_spaltenweise(b1)).hex(), APP_BILDER[0])
        self.assertEqual(a2pl.compress(mu.bild_spaltenweise(b2)).hex(), APP_BILDER[1])

    def test_befehlsfolge(self):
        bf = mu.upload_befehle([bytes.fromhex(h) for h in APP_BILDER])
        self.assertEqual(bf[2].hex(), "ea030001" + APP_BILDER[0])
        self.assertEqual(bf[4].hex(), "ea030003" + APP_BILDER[2])
        self.assertEqual(bf[-1].hex(), "ea0400")

    def test_hoechstens_255_bilder(self):
        self.assertEqual(len(mu.upload_befehle([b"\x00"] * 255)), 255 + 3)
        with self.assertRaises(ValueError):
            mu.upload_befehle([b"\x00"] * 256)
        with self.assertRaises(ValueError):
            mu.upload_befehle([])

    def test_kleines_paket_wie_app(self):
        # App: 01 04 80 00 00 14 00 15 0a ea 02 …
        p = mu.pakete(4, b"\x0a" + bytes.fromhex(APP_TABELLE))
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0][:8].hex(), "0104800000140015")

    def test_grosses_paket_in_stuecken_wie_app(self):
        # App: Befehl mit 2051 Bytes → 41 04 0000 0802 01f5 …, 41 04 0001 01f7 …, … 41 04 8004 0029
        ps = mu.pakete(4, bytes(2051))
        self.assertEqual([p[:8].hex() if i == 0 else p[:6].hex() for i, p in enumerate(ps)],
                         ["41040000080201f5", "4104000101f7", "4104000201f7", "4104000301f7",
                          "4104800400" "29"])
        self.assertTrue(all(len(p) <= 509 for p in ps))


class Zeitplan(unittest.TestCase):
    import datetime as dt
    Z = zp.ZoneInfo("Europe/Berlin")
    FREIBURG = dict(breite=47.995, laenge=7.849)

    def t(self, s):
        return self.dt.datetime.fromisoformat(s).replace(tzinfo=self.Z)

    def test_sonnenuntergang_freiburg(self):
        # veröffentlichte Werte Freiburg i. Br. (±6 min Toleranz: Näherung, 12 km Abstand)
        for tag, soll in [("2026-11-23", "16:42"), ("2026-12-21", "16:37"),
                          ("2026-06-21", "21:31"), ("2027-01-15", "17:01")]:
            su = zp.sonnenuntergang(self.dt.date.fromisoformat(tag), zone=self.Z, **self.FREIBURG)
            h, m = map(int, soll.split(":"))
            self.assertLessEqual(abs(su.hour * 60 + su.minute - (h * 60 + m)), 6, (tag, su))

    def test_fenster_und_soll(self):
        kw = dict(morgen="06:00-08:30", abend_vor=30, abend_bis="22:00", zone=self.Z, **self.FREIBURG)
        an = lambda s: zp.soll_an(self.t(s), **kw)  # noqa: E731
        self.assertFalse(an("2026-11-23T05:59"))
        self.assertTrue(an("2026-11-23T06:00"))
        self.assertTrue(an("2026-11-23T08:29"))
        self.assertFalse(an("2026-11-23T08:30"))
        self.assertFalse(an("2026-11-23T15:30"))
        self.assertTrue(an("2026-11-23T16:30"))         # Untergang ~16:43, ab ~16:13
        self.assertTrue(an("2026-11-23T21:59"))
        self.assertFalse(an("2026-11-23T22:00"))
        self.assertFalse(an("2026-06-21T20:30"))         # Sommer: erst ab ~21:01
        self.assertTrue(an("2026-06-21T21:15"))

    def test_abend_entfaellt_wenn_zu_spaet(self):
        f = zp.fenster(self.dt.date(2026, 6, 21), morgen="", abend_vor=0, abend_bis="21:00",
                       zone=self.Z, **self.FREIBURG)
        self.assertEqual(f, [])

    def test_sonnenaufgang_freiburg(self):
        # veröffentlichte Werte Freiburg i. Br. (±6 min)
        for tag, soll in [("2026-11-23", "07:46"), ("2026-12-21", "08:15"),
                          ("2026-06-21", "05:27"), ("2027-03-20", "06:30")]:
            sa = zp.sonnenaufgang(self.dt.date.fromisoformat(tag), zone=self.Z, **self.FREIBURG)
            h, m = map(int, soll.split(":"))
            self.assertLessEqual(abs(sa.hour * 60 + sa.minute - (h * 60 + m)), 6, (tag, sa))

    def test_helligkeit_nach_tageslicht(self):
        kw = dict(tag=100, nacht=67, nach=30, zone=self.Z, **self.FREIBURG)
        h = lambda s: zp.hell_soll(self.t(s), **kw)  # noqa: E731
        self.assertEqual(h("2026-11-23T06:00"), 67)      # vor Sonnenaufgang (~07:46)
        self.assertEqual(h("2026-11-23T08:00"), 100)
        self.assertEqual(h("2026-11-23T17:00"), 100)     # Untergang ~16:43, +30 = ~17:13
        self.assertEqual(h("2026-11-23T17:20"), 67)
        self.assertEqual(h("2026-06-21T06:00"), 100)     # Sommer: morgens schon hell
        self.assertEqual(h("2026-06-21T21:59"), 100)     # … und abends bis 22:00 noch
        self.assertIsNone(zp.hell_soll(self.t("2026-11-23T12:00"), tag=None))

    def test_status_von_der_steckdose(self):
        seite = ("Schaltaktor:\nLetzter Neustart    : 23.11.2026 12:56:37 External System\n"
                 "PIN Status          : 23.11.2026 12:56:42 ein\n"
                 "Letztes Web Kommando: 23.11.2026 12:56:42 Pin 12,ein\n")
        self.assertTrue(zp.status_lesen(seite))
        self.assertFalse(zp.status_lesen(seite.replace("42 ein\n", "42 aus\n", 1)))
        self.assertIsNone(zp.status_lesen("Schaltaktor:\nBetriebszeit : 00:00:29\n"))


if __name__ == "__main__":
    unittest.main()
