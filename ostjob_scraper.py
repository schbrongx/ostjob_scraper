import requests
from bs4 import BeautifulSoup
import argparse
import os
import sys
import logging
from datetime import datetime, timedelta
import re
import webbrowser

# Standardkonfiguration
DEFAULT_DAYS = 1
DEFAULT_OUTPUT_FILE = "ostjob.ch-scraper-out.md"
JOB_TITLES = [
    "ICT System Ingenieur", "ICT System Engineer", "IT System Ingenieur", "IT System Engineer",
    "System Ingenieur", "System Engineer", "System Administrator", "Systemadministrator",
    "System Architekt", "System Architect", "Netzwerkadministrator", "Network Administrator",
    "IT Infrastruktur Ingenieur", "IT Infrastructure Engineer", "IT Support Engineer", "Support Techniker",
    "Cloud Engineer", "Cloud Architekt", "DevOps Engineer", "Platform Engineer",
    "IT Spezialist", "IT Specialist", "IT Generalist", "Informatiker", "Informatik", "Netzwerk Ingenieur", "Network Engineer",
    "Infrastructure Engineer", "IT Operations Engineer", "IT Servicetechniker", "Systemtechniker"
]

# Funktion zum Initialisieren des Loggings
def init_logging(logfile=None, verbose=False):
    log_level = logging.DEBUG if verbose else logging.INFO
    if logfile:
        logging.basicConfig(filename=logfile, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(stream=sys.stdout, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Funktion zur Validierung des Ausgabe-Verzeichnisses
def validate_output_directory(filepath):
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        logging.error(f"Ausgabeverzeichnis '{directory}' existiert nicht.")
        sys.exit(1)

# Funktion zum Abrufen einer Seite und Extrahieren der Inserate
def scrape_page(url, job_titles, days):
    logging.debug(f"Abrufen der Seite: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f"Fehler beim Abrufen der URL: {url} (Statuscode: {response.status_code})")
        return [], True, 0

    soup = BeautifulSoup(response.content, 'html.parser')
    job_entries = []
    today = datetime.today()
    min_date = (today - timedelta(days=days - 1)).date()

    has_recent_jobs = False
    total_jobs_on_page = len(soup.find_all("div", class_="vacancy-list-card__body"))

    for job in soup.find_all("div", class_="vacancy-list-card__body"):
        logging.debug(f"Verarbeite Job-Eintrag: {job}")
        # Titel der Stelle extrahieren
        title_tag = job.find("h2").find("span", class_="vacancy-list-card__title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        logging.debug(f"Gefundener Titel: {title}")

        # Firmenname, PLZ+Ort, Datum und Anstellungsart extrahieren
        info_div = job.find("div", class_="vacancy-list-card__info")
        if not info_div:
            logging.debug("Keine Informationen zur Firma gefunden, überspringe diesen Job-Eintrag.")
            continue
        company = info_div.find("li", class_="vacancy-list-card__companyname").find("h3").get_text(strip=True)
        location_tag = info_div.find("li", class_="vacancy-list-card__location").find("h3")
        zip_code = location_tag.find("span", class_="vacancy-list-card__zip").get_text(strip=True) if location_tag else ""
        location = zip_code + " " + location_tag.get_text(strip=True).replace(zip_code, "") if location_tag else ""
        date = info_div.find("li", class_="vacancy-list-card__date").find("h3").get_text(strip=True)
        employment_type = info_div.find("li", class_="vacancy-list-card__type").find("h3").get_text(strip=True)
        date_obj = datetime.strptime(date, "%d.%m.%Y")

        logging.debug(f"Firma: {company}, Ort: {location}, Datum: {date}, Anstellungsart: {employment_type}")

        # Link und Textauszug extrahieren
        link_tag = job.find("a", class_="vacancy-list-card__link-content")
        link = "https://www.ostjob.ch" + link_tag["href"] if link_tag else ""
        excerpt_tag = link_tag.find("div", class_="vacancy-list-card__text") if link_tag else None
        excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""
        logging.debug(f"Link: {link}, Textauszug: {excerpt}")

        logging.debug(f"date_obj: {date_obj.date()}, min_date: {min_date}")

        # Filter nach Datum und Jobtitel
        if date_obj.date() >= min_date:
            has_recent_jobs = True
        title_normalized = re.sub(r'[-_]', ' ', title.lower())
        if date_obj.date() >= min_date and any(re.sub(r'[-_]', ' ', keyword.lower()) in title_normalized for keyword in job_titles):
            job_entries.append({
                "title": title,
                "company": company,
                "location": location,
                "date": date,
                "employment_type": employment_type,
                "excerpt": excerpt,
                "link": link
            })

    return job_entries, has_recent_jobs, total_jobs_on_page

# Hauptfunktion zum Durchsuchen mehrerer Seiten
def scrape_ostjob(job_titles, days, output_file, no_save):
    page = 1
    all_jobs = []
    more_recent_jobs = True
    total_jobs_inspected = 0

    while more_recent_jobs:
        if page == 1:
            url = "https://www.ostjob.ch/job/alle-jobs-nach-datum"
        else:
            url = f"https://www.ostjob.ch/job/alle-jobs-nach-datum-seite-{page}"
        
        logging.info(f"Scrape Seite {page}: {url}")
        jobs, more_recent_jobs, jobs_on_page = scrape_page(url, job_titles, days)

        total_jobs_inspected += jobs_on_page

        if jobs:
            all_jobs.extend(jobs)
        else:
            logging.debug(f"Keine weiteren Jobs auf Seite {page}.")

        page += 1

    output = []
    for job in all_jobs:
        output.append(f"# [{job['title']}]({job['link']})\n_{job['company']}_, _{job['location']}_ _{job['date']}_ _{job['employment_type']}_\n{job['excerpt']}\n")

    logging.info(f"Insgesamt begutachtete Inserate: {total_jobs_inspected}, Treffer: {len(all_jobs)}")

    if not no_save:
        logging.info(f"Speichere Ergebnisse in Datei: {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output))
        logging.info(f"Öffne: {output_file}")
        webbrowser.open(output_file)
    else:
        logging.info("Gebe Ergebnisse auf stdout aus.")
        print("\n".join(output))

# Kommandozeilenparameter verarbeiten
def main():
    parser = argparse.ArgumentParser(description="Web Scraper für ostjob.ch")
    parser.add_argument("-d", "--days", type=int, default=DEFAULT_DAYS, help="Anzahl der Tage zurück, die durchsucht werden sollen (Standard: 1)")
    parser.add_argument("-t", "--titles", nargs='*', default=JOB_TITLES, help="Liste der Jobtitel zum Filtern")
    parser.add_argument("-n", "--nosave", action="store_true", help="Speichern der Ausgabe verhindern")
    parser.add_argument("-f", "--file", type=str, default=DEFAULT_OUTPUT_FILE, help="Pfad zur Ausgabedatei (Standard: ostjob.ch-scraper-out.txt)")
    parser.add_argument("-l", "--logging", nargs="?", const=True, help="Logging aktivieren (Optional: Dateiname)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Debugging Log-Output aktivieren")

    args = parser.parse_args()

    # Logging initialisieren
    init_logging(args.logging if isinstance(args.logging, str) else None, args.verbose)

    # Verzeichnis validieren
    if not args.nosave:
        validate_output_directory(args.file)

    # Scraping starten
    scrape_ostjob(args.titles, args.days, args.file, args.nosave)

if __name__ == "__main__":
    main()
    input("Drücken Sie die Eingabetaste, um das Programm zu beenden...")