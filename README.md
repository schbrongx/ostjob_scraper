# ostjob_scraper

## Übersicht

`ostjob_scraper` ist ein Python-Skript zum Scrapen der Jobplattform [ostjob.ch](https://www.ostjob.ch). Es durchsucht die Jobangebote nach bestimmten Jobtiteln, die in einer Standardliste definiert sind, und generiert eine Markdown-Ausgabe (".md"), die die gesammelten Informationen zu den relevanten Jobangeboten enthält.


## Verwendung des Scrapers

Der Scraper kann über die Kommandozeile mit verschiedenen Parametern verwendet werden, um die Ergebnisse zu personalisieren:

### Parameter der Kommandozeile

- `-d`, `--days`: Anzahl der Tage, die zurück durchsucht werden sollen (Standard: 1). Damit kann gesteuert werden, wie alt die gescrapten Jobinserate maximal sein dürfen.
- `-t`, `--titles`: Liste der Jobtitel, nach denen gefiltert wird. Diese kann übergeben werden, um nur spezifische Jobangebote zu finden. **Nicht verwendbar in Kombination mit `-j`**.
- `-j`, `--jobtitlefile`: Pfad zu einer Datei, die eine Liste von Jobtiteln enthält (einen Jobtitel pro Zeile). Diese Datei wird verwendet, um die Jobtitel für das Scraping festzulegen. **Nicht verwendbar in Kombination mit `-t`**.
- `-m`, `--menu`: Interaktiver Modus, in dem der Benutzer zur Laufzeit nach den benötigten Parametern (wie z.B. Anzahl der Tage) gefragt wird.
- `-n`, `--nosave`: Wenn dieser Parameter gesetzt ist, wird die Ausgabe nicht in eine Datei gespeichert, sondern direkt in der Konsole ausgegeben.
- `-f`, `--file`: Pfad zur Ausgabedatei (Standard: "ostjob.ch-scraper-out.md").
- `-l`, `--logging`: Aktiviert das Logging (Optional: Log-Dateiname). Falls kein Dateiname angegeben wird, werden Logs in der Konsole ausgegeben.
- `-v`, `--verbose`: Aktiviert detailliertere Logs für Debugging-Zwecke.

### Interaktiver Modus (`-m`)

Der interaktive Modus erlaubt es dem Benutzer, Parameter wie die Anzahl der Tage zur Laufzeit über Eingabeaufforderungen festzulegen. Falls keine Eingabe erfolgt, wird der voreingestellte Standardwert verwendet.

### Jobtitel-Datei (`-j`)

Statt Jobtitel manuell über `-t` anzugeben, kann eine Datei mit Jobtiteln verwendet werden, die den Jobtiteln eine Zeile pro Jobtitel enthält. Wenn der Parameter `-j` angegeben ist, wird die angegebene Datei verwendet. 

Falls die Datei nicht existiert oder leer ist, wird das Skript mit einer Fehlermeldung abgebrochen.

### Beispielaufrufe

**1. Interaktiver Modus**:
```sh
python ostjob_scraper.py -m
```
In diesem Modus werden die Parameter zur Laufzeit abgefragt, z.B. die Anzahl der Tage, die durchsucht werden sollen.

**2. Jobtitel aus Datei**:
```sh
python ostjob_scraper.py -d 5 -j "jobtitles.txt" -f "output.md"
```
Dieser Aufruf durchsucht die letzten 5 Tage und verwendet die Jobtitel aus der Datei jobtitles.txt. Das Ergebnis wird in der Datei output.md gespeichert.

**3. Standardaufruf mit Titelliste**:
```sh
python ostjob_scraper.py -d 7 -t "System Engineer" "DevOps Engineer" -f "jobs_output.md" -v
```
Dieser Aufruf durchsucht die letzten 7 Tage nach den Jobtiteln "System Engineer" und "DevOps Engineer" und speichert das Ergebnis in der Datei "jobs_output.md". Das Log-Level ist auf "verbose" gesetzt.


## Download des Releases

Das erste Release des `ostjob_scraper` steht als ausführbare Datei (.exe) zur Verfügung, die ohne Python-Installation direkt unter Windows genutzt werden kann.

- **[Download ostjob_scraper.exe](https://github.com/schbrongx/ostjob_scraper/releases/download/v1.0.0/ostjob_scraper.exe)**

Dieses Release enthält die grundlegende Funktionalität zum Scrapen von Jobangeboten von ostjob.ch. Laden Sie die `.exe`-Datei herunter, um den Scraper einfach und bequem auszuführen.


## Standardparameter ändern

Die Standardparameter des Scrapers können direkt im Code angepasst werden:

- **Anzahl der Tage**: Der Standardwert für die Anzahl der zu durchsuchenden Tage wird in der Variablen `DEFAULT_DAYS` festgelegt (aktuell: `1`).
- **Ausgabedatei**: Der Standardpfad zur Ausgabedatei wird in der Variablen `DEFAULT_OUTPUT_FILE` definiert (aktuell: "ostjob.ch-scraper-out.md").
- **Jobtitel-Liste**: Die Jobtitel, nach denen standardmäßig gesucht wird, sind in der Liste `JOB_TITLES` gespeichert. Diese kann beliebig angepasst oder erweitert werden, um andere Titel einzuschließen.


## Weiterentwicklung

Sie können den Code anpassen, um beispielsweise weitere Jobplattformen hinzuzufügen oder das Scraping auf andere Weise zu erweitern. Wir freuen uns über Verbesserungsvorschläge oder Pull-Requests!

Falls Sie Fragen haben oder Fehler finden, erstellen Sie bitte ein Issue im Repository.

---
**Kontakt**: Falls Sie Fragen haben oder Hilfe benötigen, können Sie mich direkt über GitHub kontaktieren.

**Lizenz**: Dieses Projekt steht unter der MIT-Lizenz.
