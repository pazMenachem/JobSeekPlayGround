"""Configuration settings for the job scraper application."""

from typing import List

# Browser settings
BROWSER_TYPE = "firefox"  # Options: "chrome", "firefox", "edge"
HEADLESS_MODE = False  # Set to True to run browser in background
IMPLICIT_WAIT = 10  # Seconds to wait for elements to load

# Scraping settings
PAGE_LOAD_TIMEOUT = 30  # Maximum time to wait for page to load
SCROLL_PAUSE_TIME = 2  # Time to pause between scrolls
MAX_PAGES_PER_URL = 10  # Maximum pages to scrape per URL

# Output settings
OUTPUT_FILE = "found_jobs.txt"  # File to save found job URLs
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR

# Common job site selectors (you can modify these based on the sites you're scraping)
JOB_TITLE_SELECTORS = [
    "h2 a",  # Common for job titles
    "h3 a",
    ".job-title a",
    ".title a",
    "[data-testid='job-title'] a"
]

NEXT_PAGE_SELECTORS = [
    "a[aria-label='Next']",
    "a[aria-label='next']",
    ".next-page",
    "a:contains('Next')",
    "a:contains('>')",
    ".pagination .next"
]

# Keywords to search for (modify this list as needed)
DEFAULT_KEYWORDS = [
    "engineer",
    # "python",
    # "developer",
    # "software engineer",
    # "data scientist",
    # "machine learning"
]

# URLs to scrape (add your target job sites here)
TARGET_URLS = [
    "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52bbe14cf9326c&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78",
    "https://copyleaks.com/careers",
    # "https://www.indeed.com/jobs?q=python+developer",
    # "https://www.linkedin.com/jobs/search/?keywords=software%20engineer",
    # Add more URLs as needed
    # "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=python",
    # "https://www.ziprecruiter.com/jobs-search?search=python+developer",
]
