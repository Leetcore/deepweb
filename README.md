# Deep Web Scanner
Dieses Script findet Websites, die per IPv4-Adresse erreichbar sind und speichert
deren Metadaten. Die Ausgabe im Terminal wird nach bestimmten Keywords gefiltert.

Aber in der Logdatei sind alle erreichten Websites drin.

Die gleichen Ergebnisse können mit der Internetsuchmaschine Shodan oder teilweise
auch mit Google erreicht werden.

# Ip-Adressen
Die Eingabedatei ist eine CSV-Datei, die IP-Adressen aus Deutschland enthält.
Das IP-Ranges sollten im Format: 1.1.1.1-2.2.2.2 sein.

# Suche
Über die Textdatei lässt sich schnell mit `grep`suchen.

``` bash
grep -i "nginx" deep-web.txt
```