"""Configuration settings for the job scraper application."""

from typing import List

# Browser settings
BROWSER_TYPE = "firefox"  # Options: "chrome", "firefox", "edge"
HEADLESS_MODE = False  # Set to True to run browser in background
IMPLICIT_WAIT = 10  # Seconds to wait for elements to load

# Scraping settings
PAGE_LOAD_TIMEOUT = 30  # Maximum time to wait for page to load
SCROLL_PAUSE_TIME = 2  # Time to pause between scrolls
MAX_PAGES_PER_URL = 3  # Maximum pages to scrape per URL

# Output settings
OUTPUT_FILE = "found_jobs.txt"  # File to save found job URLs
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR

# Common job site selectors (you can modify these based on the sites you're scraping)
JOB_TITLE_SELECTORS = [
    "h2 a",  # Common for job titles
    "h3 a",
    ".job-title a",
    ".title a",
    "[data-testid='job-title'] a",
    # Additional selectors for various job sites
    "a[href*='job']",  # Links containing 'job' in href
    "a[href*='career']",  # Links containing 'career' in href
    ".job-listing a",  # Job listing links
    ".career-item a",  # Career item links
    ".position a",  # Position links
    "li a",  # List item links (common for job lists)
    "div a",  # Div links (fallback)
    "span a",  # Span links
    "p a"  # Paragraph links
]

# Keywords to search for (modify this list as needed)
DEFAULT_KEYWORDS = [
    "engineer",
    "graduate",
    "junior",
    "software engineer",
]

# URLs to scrape (add your target job sites here)
TARGET_URLS = [
    "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52bbe14cf9326c&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78&workerSubType=0c40f6bd1d8f10adf6dae161b1844a15&workerSubType=ab40a98049581037a3ada55b087049b7&timeType=5509c0b5959810ac0029943377d47364",
    "https://copyleaks.com/careers",
]
