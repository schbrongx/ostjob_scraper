"""
This script scrapes job listings from the website ostjob.ch. It allows users to specify job titles and a time frame (number of days) to search for relevant job postings. The results can be saved to a file or displayed on the console. The script uses requests to fetch web pages and BeautifulSoup to parse the HTML content.

Key features:
- Configurable search for specific job titles.
- Ability to specify how many days back the search should include.
- Option to save results to a file or print to the console.
- Logging support for debugging and tracking scraping progress.
"""

import requests
from bs4 import BeautifulSoup
import argparse
import os
import sys
import logging
from datetime import datetime, timedelta
import re
import webbrowser

# Default configuration
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

# Function to initialize logging
def init_logging(logfile=None, verbose=False):
    log_level = logging.DEBUG if verbose else logging.INFO
    if logfile:
        logging.basicConfig(filename=logfile, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(stream=sys.stdout, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to validate the output directory
def validate_output_directory(filepath):
    """
    Validates if the output directory exists; exits if it does not.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        logging.error(f"Output directory '{directory}' does not exist.")
        sys.exit(1)

# Function to fetch a page and extract job listings
def scrape_page(url, job_titles, days):
    """
    Fetches the content from the given URL and extracts job listings based on the criteria provided.
    
    Args:
        url (str): The URL of the page to scrape.
        job_titles (list): List of job titles to filter.
        days (int): Number of recent days to filter job listings.
    
    Returns:
        list: A list of job entries found on the page.
        bool: Whether there are more recent jobs.
        int: The total number of jobs on the page.
    """
    logging.debug(f"Fetching page: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f"Failed to fetch URL: {url} (Status code: {response.status_code})")
        return [], True, 0

    soup = BeautifulSoup(response.content, 'html.parser')
    job_entries = []
    today = datetime.today()
    min_date = (today - timedelta(days=days - 1)).date()

    has_recent_jobs = False
    total_jobs_on_page = len(soup.find_all("div", class_="vacancy-list-card__body"))

    for job in soup.find_all("div", class_="vacancy-list-card__body"):
        logging.debug(f"Processing job entry: {job}")
        # Extract job title
        title_tag = job.find("h2").find("span", class_="vacancy-list-card__title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        logging.debug(f"Job title found: {title}")

        # Extract company name, location, date, and employment type
        info_div = job.find("div", class_="vacancy-list-card__info")
        if not info_div:
            logging.debug("No company information found, skipping this job entry.")
            continue
        company = info_div.find("li", class_="vacancy-list-card__companyname").find("h3").get_text(strip=True)
        location_tag = info_div.find("li", class_="vacancy-list-card__location").find("h3")
        zip_code = location_tag.find("span", class_="vacancy-list-card__zip").get_text(strip=True) if location_tag else ""
        location = zip_code + " " + location_tag.get_text(strip=True).replace(zip_code, "") if location_tag else ""
        date = info_div.find("li", class_="vacancy-list-card__date").find("h3").get_text(strip=True)
        employment_type = info_div.find("li", class_="vacancy-list-card__type").find("h3").get_text()
        date_obj = datetime.strptime(date, "%d.%m.%Y")

        logging.debug(f"Company: {company}, Location: {location}, Date: {date}, Employment Type: {employment_type}")

        # Extract link and job excerpt
        link_tag = job.find("a", class_="vacancy-list-card__link-content")
        link = "https://www.ostjob.ch" + link_tag["href"] if link_tag else ""
        excerpt_tag = link_tag.find("div", class_="vacancy-list-card__text") if link_tag else None
        excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""
        logging.debug(f"Link: {link}, Excerpt: {excerpt}")

        # Filter by date and job title
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

# Main function to scrape multiple pages
def scrape_ostjob(job_titles, days, output_file, no_save):
    """
    Scrapes job listings from ostjob.ch based on provided parameters.
    
    Args:
        job_titles (list): List of job titles to filter.
        days (int): Number of recent days to filter job listings.
        output_file (str): File path for saving the output.
        no_save (bool): Flag to prevent saving the output.
    """
    page = 1
    all_jobs = []
    more_recent_jobs = True
    total_jobs_inspected = 0

    while more_recent_jobs:
        if page == 1:
            url = "https://www.ostjob.ch/job/alle-jobs-nach-datum"
        else:
            url = f"https://www.ostjob.ch/job/alle-jobs-nach-datum-seite-{page}"
        
        logging.info(f"Scraping page {page}: {url}")
        jobs, more_recent_jobs, jobs_on_page = scrape_page(url, job_titles, days)

        total_jobs_inspected += jobs_on_page

        if jobs:
            all_jobs.extend(jobs)
        else:
            logging.debug(f"No more jobs found on page {page}.")

        page += 1

    output = []
    for job in all_jobs:
        output.append(f"# [{job['title']}]({job['link']})\n_{job['company']}_, _{job['location']}_, _{job['employment_type']}_, _{job['date']}_ \n\n{job['excerpt']}\n")

    logging.info(f"Total job listings inspected: {total_jobs_inspected}, Matches found: {len(all_jobs)}")

    if not no_save:
        logging.info(f"Saving results to file: {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output))
        logging.info(f"Opening: {output_file}")
        webbrowser.open(output_file)
    else:
        logging.info("Printing results to stdout.")
        print("\n".join(output))

# Command-line arguments handling
def main():
    """
    Main function to handle command-line arguments and start the scraping process.
    """
    parser = argparse.ArgumentParser(description="Web Scraper for ostjob.ch")
    parser.add_argument("-d", "--days", type=int, default=DEFAULT_DAYS, help="Number of days back to search (default: 1)")
    parser.add_argument("-t", "--titles", nargs='*', default=JOB_TITLES, help="List of job titles to filter")
    parser.add_argument("-n", "--nosave", action="store_true", help="Prevent saving the output to file")
    parser.add_argument("-f", "--file", type=str, default=DEFAULT_OUTPUT_FILE, help="Path to output file (default: ostjob.ch-scraper-out.md)")
    parser.add_argument("-l", "--logging", nargs="?", const=True, help="Enable logging (Optional: filename)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging output")

    args = parser.parse_args()

    # Initialize logging
    init_logging(args.logging if isinstance(args.logging, str) else None, args.verbose)

    # Validate output directory
    if not args.nosave:
        validate_output_directory(args.file)

    # Start scraping
    scrape_ostjob(args.titles, args.days, args.file, args.nosave)

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")