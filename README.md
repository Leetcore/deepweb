# Deep Web Scanner
Dieses Script findet Websites, die per IPv4-Adresse erreichbar sind und speichert
deren Metadaten. Die Ausgabe im Terminal wird nach bestimmten Keywords gefiltert.

Aber in der Logdatei sind alle erreichten Websites drin.

Die gleichen Ergebnisse können mit der Internetsuchmaschine Shodan oder teilweise
auch mit Google erreicht werden.

## Ip-Adressen
Die Eingabedatei ist eine CSV, die IP-Adressen aus Deutschland enthält.
Das IP-Ranges sollten im Format: 1.1.1.1-2.2.2.2 sein.

## Suche
Über die Textdatei lässt sich schnell mit `grep`suchen.

``` bash
grep -i "nginx" deep-web.txt
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

## "Screenshots"
Mit dem Skript auto_shotter.sh können aus einer Quelldatei Screenshots erstellt werden. Davor müsst ihr aber ein paar Packete installieren.
Bleibt bitte in Ordner des Git-Repositories, indem das Skript auto_shotter.sh liegt, da die Module im gleichen Verzeichnis sein müssen.

```bash
sudo apt update
sudo apt install npm
npm i puppeteer delay
```

Anwendung: `./auto_shotter.sh $Quelldatei $Orndername`
Beispiel:  `./auto_shotter.sh input.txt IndexOf`

input.txt erstellen mit `grep -i 'index of' deep-web.txt >> input.txt`

