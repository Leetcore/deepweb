# Deep Web Scanner
Dieses Script findet Websites, die per IPv4-Adresse erreichbar sind und speichert
deren Metadaten. Die Ausgabe im Terminal wird nach bestimmten Keywords gefiltert, 
aber in der Logdatei sind alle erreichten Websites drin.

Was findet man damit? Webcams, Nischen-Websites und interessante Dashboards.

Die gleichen Ergebnisse können mit der Internetsuchmaschine Shodan oder teilweise
auch mit Google erreicht werden.

## Ip-Adressen
Die Eingabedatei ist eine CSV, die IP-Adressen aus Deutschland enthält.
Das IP-Ranges sollten im Format: 1.1.1.1-2.2.2.2 sein. Die IP-Adressen stammen 
von diesem Projekt: https://github.com/sapics/ip-location-db

## Vorraussetzung
* Python 3.9

Wenn du auf Python 3.8 bist, kannst du Python 3.9 parallel installieren. Dann 
muss die gewünschte Version explizit angegeben werden. `python3` bleibt weiterhin
die Version 3.8:

``` bash
sudo apt install python3.9
python3.9 -m pip install -r requirements.txt
python3.9 deep-web-scanner.py
```

## Installation
Installiere die benötigten Pakete:
``` bash
pip3 install -r requirements.txt
```

## Starten
Startet den Scanner mit Standardwerten. Im Terminal und im richtigen Ordner ausführen:
``` bash
python3 deep-web-scanner.py
```

Optionen:
* -i input.txt: Eingabedatei
* -o output.txt: Ausgabedatei
* -indexof true: Logs index of files (default: False)

## "Index of"
Diese Option zeigt verfügbare Dateien an: `-indexof true`:
``` bash
python3 deep-web-scanner.py -indexof true
```

## Suche
Über die Textdatei lässt sich schnell mit `grep`suchen.

``` bash
grep -i "nginx" deep-web.txt
```
