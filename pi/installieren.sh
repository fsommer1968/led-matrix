#!/bin/bash
# Richtet den Matrix-Pi ohne Rückfragen ein: prüfen, alle Pakete aktualisieren, Programme
# installieren, Bluetooth prüfen, nach der Matrix suchen (ohne Verbindung).
# Aufruf auf dem Pi im Ordner led/pi:  sudo ./installieren.sh
# Bericht danach auch in /opt/matrix/einrichtung.log
set -euo pipefail
cd "$(dirname "$0")"
ZIEL=/opt/matrix
mkdir -p "$ZIEL/gifs"
exec > >(tee "$ZIEL/einrichtung.log") 2>&1
export DEBIAN_FRONTEND=noninteractive
APT_OPT=(-y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold)

abschnitt() { echo; echo "===== $* ====="; }

abschnitt "Prüfung vorher"
echo "Rechner:  $(hostname)  ($(hostname -I 2>/dev/null))"
grep PRETTY_NAME /etc/os-release || true
echo "Modell:   $(tr -d '\0' < /proc/device-tree/model 2>/dev/null || echo unbekannt)"
echo "Kernel:   $(uname -r)"
echo "Laufzeit: $(uptime -p)"
df -h / | tail -1 | awk '{print "SD-Karte: " $3 " belegt von " $2 ", frei " $4}'
free -h | awk '/Mem:/ {print "Speicher: " $3 " belegt von " $2}'
command -v vcgencmd >/dev/null && echo "Temperatur: $(vcgencmd measure_temp)" \
    && echo "Drosselung: $(vcgencmd get_throttled)  (0x0 = alles gut)"
python3 --version

abschnitt "Pakete aktualisieren"
apt-get update
apt-get "${APT_OPT[@]}" full-upgrade
apt-get "${APT_OPT[@]}" install git python3-venv python3-pip bluez rfkill
apt-get "${APT_OPT[@]}" autoremove
apt-get clean

abschnitt "Bluetooth"
rfkill unblock bluetooth || true
systemctl enable --now bluetooth
sleep 2
if bluetoothctl show | grep -q "Powered: yes"; then
    bluetoothctl show | grep -E "Controller|Name|Powered"
else
    bluetoothctl power on || true
    bluetoothctl show | grep -E "Controller|Powered" || echo "WARNUNG: kein Bluetooth-Adapter gefunden"
fi

abschnitt "Python-Umgebung (bleak, Pillow)"
python3 -m venv "$ZIEL/.venv"
"$ZIEL/.venv/bin/pip" install --upgrade pip bleak pillow

abschnitt "Matrix-Wächter installieren (noch nicht eingeschaltet)"
install -m 0644 ../*_64x16.gif "$ZIEL/gifs/"
install -m 0755 matrix_waechter.py matrix_spieler.py matrix_upload.py matrix_zeitplan.py matrix_demo.py matrix_anzeige.py a2pl.py "$ZIEL/"
# Einstellungen: ältere Fassungen (ohne MATRIX_HELL) durch die neue ersetzen
if [ ! -f /etc/default/matrix-waechter ] || ! grep -q '^MATRIX_HELL=' /etc/default/matrix-waechter; then
    install -m 0644 matrix-waechter.default /etc/default/matrix-waechter
fi
grep -q '^MATRIX_ZEITPLAN_MORGEN=' /etc/default/matrix-waechter \
    || sed -n '/^# Zeitplan/,$p' matrix-waechter.default >> /etc/default/matrix-waechter
grep -q '^MATRIX_HELL_TAG=' /etc/default/matrix-waechter \
    || sed -n '/^# Helligkeit nach Tageslicht/,$p' matrix-waechter.default >> /etc/default/matrix-waechter
grep -q '^MATRIX_GIFS=' /etc/default/matrix-waechter \
    || sed -n '/^# Täglicher Wechsel/,$p' matrix-waechter.default >> /etc/default/matrix-waechter
grep -q '^MATRIX_GIFS_2=' /etc/default/matrix-waechter \
    || sed -n '/^# Silvester/,$p' matrix-waechter.default >> /etc/default/matrix-waechter
install -d "$ZIEL/animationen"
install -m 0644 ../animationen/*.py "$ZIEL/animationen/"
install -m 0644 matrix-waechter.service matrix-zeitplan.service matrix-zeitplan.timer \
    matrix-adventskalender.service matrix-adventskalender.timer /etc/systemd/system/
systemctl daemon-reload
# Vorrat: alle GIFs im Voraus komprimieren (Upload ~20 s schneller), läuft im Hintergrund
systemd-run --unit=matrix-vorrat --nice=10 "$ZIEL/.venv/bin/python" "$ZIEL/matrix_upload.py" --vorrat "$ZIEL"/gifs/*_64x16.gif || true
# Adventskalender (Countdown) für heute erzeugen und täglich neu
systemctl start matrix-adventskalender.service && systemctl enable --now matrix-adventskalender.timer
ls -l "$ZIEL/gifs"

abschnitt "Nach der Matrix suchen (ohne Verbindung)"
timeout 30 "$ZIEL/.venv/bin/python" -c "
import asyncio
from bleak import BleakScanner
async def m():
    for d in await BleakScanner.discover(timeout=15):
        if (d.name or '').startswith('IOTBT'): print('gefunden:', d.name, d.address)
asyncio.run(m())" || echo "Suche ohne Ergebnis (Matrix an? App zu?)"

abschnitt "Fertig"
if [ -f /var/run/reboot-required ]; then
    echo "Neustart nötig (neuer Kernel o. ä.):  sudo reboot"
fi
echo "Nächste Schritte (iPhone-App geschlossen, Matrix an):"
echo "  1. Test-Upload:    cd $ZIEL && .venv/bin/python matrix_upload.py gifs/weihnachtsmann_rentier_64x16.gif"
echo "  2. Wächter an:     sudo systemctl enable --now matrix-waechter"
echo "  3. Zeitplan an:    sudo systemctl enable --now matrix-zeitplan.timer   (nur mit Steckdose; Plan: $ZIEL/matrix_zeitplan.py plan)"
echo "  Log:               journalctl -u matrix-waechter -f"
echo "Bericht: $ZIEL/einrichtung.log"
