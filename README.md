# ostjob_scraper

## 📜 Übersicht

`ostjob_scraper` ist ein Python-Skript zum Scrapen der Jobplattform [ostjob.ch](https://www.ostjob.ch). Es durchsucht die Jobangebote nach bestimmten Jobtiteln, die in einer Standardliste definiert sind, und generiert eine Markdown-Ausgabe (".md"), die die gesammelten Informationen zu den relevanten Jobangeboten enthält.

## ➜ Verwendung des Scrapers

Der Scraper kann über die Kommandozeile mit verschiedenen Parametern verwendet werden, um die Ergebnisse zu personalisieren:

### 🛠️ Parameter der Kommandozeile

- `-d`, `--days`: Anzahl der Tage, die zurück durchsucht werden sollen (Standard: 1). Damit kann gesteuert werden, wie alt die gescrapten Jobinserate maximal sein dürfen.
- `-t`, `--titles`: Liste der Jobtitel, nach denen gefiltert wird. Diese kann übergeben werden, um nur spezifische Jobangebote zu finden.
- `-n`, `--nosave`: Wenn dieser Parameter gesetzt ist, wird die Ausgabe nicht in eine Datei gespeichert, sondern direkt in der Konsole ausgegeben.
- `-f`, `--file`: Pfad zur Ausgabedatei (Standard: "ostjob.ch-scraper-out.md").
- `-l`, `--logging`: Aktiviert das Logging (Optional: Log-Dateiname). Falls kein Dateiname angegeben wird, werden Logs in der Konsole ausgegeben.
- `-v`, `--verbose`: Aktiviert detailliertere Logs für Debugging-Zwecke.

### Beispielaufruf

```sh
python ostjob_scraper.py -d 7 -t "System Engineer" "DevOps Engineer" -f "jobs_output.md" -v
```
Dieser Aufruf durchsucht die letzten 7 Tage nach den Jobtiteln "System Engineer" und "DevOps Engineer" und speichert das Ergebnis in der Datei "jobs_output.md". Das Log-Level ist auf "verbose" gesetzt.

## ➜ Standardparameter ändern

Die Standardparameter des Scrapers können direkt im Code angepasst werden:

- **Anzahl der Tage**: Der Standardwert für die Anzahl der zu durchsuchenden Tage wird in der Variablen `DEFAULT_DAYS` festgelegt (aktuell: `1`).
- **Ausgabedatei**: Der Standardpfad zur Ausgabedatei wird in der Variablen `DEFAULT_OUTPUT_FILE` definiert (aktuell: "ostjob.ch-scraper-out.md").
- **Jobtitel-Liste**: Die Jobtitel, nach denen standardmäßig gesucht wird, sind in der Liste `JOB_TITLES` gespeichert. Diese kann beliebig angepasst oder erweitert werden, um andere Titel einzuschließen.

## 🛠️ Weiterentwicklung

Sie können den Code anpassen, um beispielsweise weitere Jobplattformen hinzuzufügen oder das Scraping auf andere Weise zu erweitern. Wir freuen uns über Verbesserungsvorschläge oder Pull-Requests!

Falls Sie Fragen haben oder Fehler finden, erstellen Sie bitte ein Issue im Repository.

---
**Kontakt**: Falls Sie Fragen haben oder Hilfe benötigen, können Sie mich direkt über GitHub kontaktieren.

**Lizenz**: Dieses Projekt steht unter der MIT-Lizenz.

