"""Configuration settings for the job scraper application."""

from typing import List
from src.data_models import RelevanceStatus

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
    # "https://copyleaks.com/careers",
]

DEFAULT_BASE_PROMPT = """
    You are a helpful assistant that analyzes job postings and determines if they are relevant to a software engineer.
    You will be given a job posting and you will need to determine if it is relevant to a software engineer.
    You will need to determine if the job posting is relevant to a software engineer.
    You will need to determine if the job posting is relevant to a software engineer.
    Is this job relevant for a software engineer? Answer with one word: yes, no, or maybe.
"""

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

class BrowserSettings:
    """Browser settings for the job scraper application."""

    def __init__(
        self, 
        browser_type: str = "firefox",
        headless_mode: bool = False, 
        implicit_wait: int = 5,
        page_load_timeout: int = 10
        ) -> None:
        """Initialize the browser settings.
        
        Args:
            browser_type: Type of browser to use ('chrome', 'firefox').
            headless_mode: Whether to run browser in headless mode.
            implicit_wait: Seconds to wait for elements to load
            page_load_timeout: Maximum time to wait for page to load
        """
        self.browser_type = browser_type
        self.headless_mode = headless_mode
        self.implicit_wait = implicit_wait
        self.page_load_timeout = page_load_timeout

class ScrapingSettings:
    """Scraping settings for the job scraper application."""

    def __init__(
        self, 
        scroll_pause_time: int = 2, 
        max_pages_per_url: int = 3,
        urls: List[str] = TARGET_URLS,
        keywords: List[str] = DEFAULT_KEYWORDS
        ) -> None:
        """
        Initialize the scraping settings.
        
        Args:
            page_load_timeout: Maximum time to wait for page to load
            scroll_pause_time: Time to pause between scrolls
            max_pages_per_url: Maximum pages to scrape per URL
            urls: URLs to scrape
            keywords: Keywords to search for
        """

        self.scroll_pause_time = scroll_pause_time
        self.max_pages_per_url = max_pages_per_url
        self.urls = urls
        self.keywords = keywords


class OutputSettings:
    """Output settings for the job scraper application."""

    def __init__(self, output_file: str = "found_jobs.txt", log_level: str = "INFO") -> None:
        """Initialize the output settings.
        
        Args:
            output_file: File to save found job URLs
            log_level: Logging level: DEBUG, INFO, WARNING, ERROR
        """
        self.output_file = output_file
        self.log_level = log_level


class JobFilterSettings:
    """Job filtering settings for the job scraper application."""
    
    def __init__(self, default_job_filter_level: RelevanceStatus = RelevanceStatus.ALL) -> None:
        """Initialize the job filtering settings.
        
        Args:
            default_job_filter_level: Default filtering level: "yes", "no", "maybe", "all"
        """
        self.default_job_filter_level = default_job_filter_level

class LLMSettings:
    """LLM settings for the job scraper application."""
    
    def __init__(
        self, 
        base_llm_prompt: str = DEFAULT_BASE_PROMPT,
        llm_provider: str = "gemini",
        llm_model: str = "gemini-2.5-flash"
        ) -> None:
        """Initialize the LLM settings.
        
        Args:
            base_llm_prompt: Base LLM prompt
            llm_provider: LLM provider: "gemini", "openai"
            llm_model: LLM model: "gemini-2.5-flash", "gpt-4o"
        """
        self.base_llm_prompt = base_llm_prompt
        self.llm_provider = llm_provider
        self.llm_model = llm_model

class JobSiteSelectors:
    """Job site selectors for the job scraper application."""
    
    def __init__(self, job_title_selectors: List[str] = JOB_TITLE_SELECTORS) -> None:
        """Initialize the job site selectors.
        
        Args:
            job_title_selectors: Job title selectors
        """
        self.job_title_selectors = job_title_selectors

browser_settings = BrowserSettings()
scraping_settings = ScrapingSettings()
output_settings = OutputSettings()
job_filter_settings = JobFilterSettings()
llm_settings = LLMSettings()
job_site_selectors = JobSiteSelectors()
