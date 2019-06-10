Ein Script, mit dem wir News-Artikel aus Typo3 in Markdown konvertiert haben.

Es wird je Artikel ein Unterordner mit einer Datei `index.md` angelegt. Falls
in der Meldung Bilder verwendet wurden, werden diese im selben Ordner mit
abgelegt.

## Installation

```
virtualenv venv -p python3
source venv/bin/activate
pip3 install -r requirements.txt
```

## Anwendung

1. Extrahiere News-Artikel aus Typo3 als XML-Datei.
  
  Öffnet dazu das Kontextmenü im Typo3-Seitenbaum über den Ordner, der die News-Artikel enthält.

  ![Schritt 1](https://raw.githubusercontent.com/gruene-roesrath/typo3-ttnews-migration/master/docs/export1.png)

  Achte darauf, dass unter `Datei & Voreinstellungen` als Dateiformat `XML` ausgewählt ist.

  ![Schritt 2](https://raw.githubusercontent.com/gruene-roesrath/typo3-ttnews-migration/master/docs/export2.png)


2. Passe den Pfad in `parse.xml` an (ersetze `testdata/news-export.xml`).

3. Starte `python parse.xml`.

Das Ergebnis sollte im Ordner `export` zu finden sein.

