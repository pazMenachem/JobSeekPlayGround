"""Job crawler manager for coordinating job scraping operations."""

from typing import List
from .job_scraper import JobScraper
from .browser_driver import BrowserDriver
from .page_navigator import PageNavigator
from src.data_models import JobData
from src.logger import get_logger


class JobCrawlerManager:
    """Manages job crawling operations.
    
    This class coordinates the job scraping process, including
    browser management, URL navigation, and job data extraction.
    """
    
    def __init__(self) -> None:
        """Initialize the job crawler manager."""
        self.logger = get_logger("job_crawler")
        self.job_scraper = None
        self.page_navigator = None
    
    def crawl_jobs(self, urls: List[str], keywords: List[str]) -> List[JobData]:
        """Crawl jobs from specified URLs."""
        result: List[JobData] = []

        self.logger.info(f"Starting job crawl for {len(urls)} URLs with {len(keywords)} keywords")

        try:
            with BrowserDriver() as driver:
                self.job_scraper = JobScraper(driver)
                self.page_navigator = PageNavigator(driver)

                for url in urls:
                    driver.get(url)
                    result.extend(self._process_url(keywords, url))

        except Exception as e:
            raise RuntimeError(f"Error during job crawling: {e}")
        
        if not result:
            raise RuntimeError("No jobs found during crawling")

        self.logger.info(f"Found {len(result)}\njobs:\n")
        for i, job in enumerate(result, 1):
            self.logger.info(f"  {i}. {job.title} at {job.company}")
        return result
    
    def _process_url(self, keywords: List[str], url: str) -> List[JobData]:
        """
        Process all pages for current URL.
        
        Args:
            keywords: List of keywords to search for in job titles.
            all_found_jobs: List of all found jobs.
            url: URL to process.
        """        
        result: List[JobData] = []
        ongoing = True

        # The url is set at driver attribute.
        # Every time we go to next page, the url is updated.
        while ongoing:

            # Find jobs on the current page
            result.extend(
                self.job_scraper.scrape_jobs(keywords)
                )

            # Try to go to next page
            if not self.page_navigator.go_to_next_page():
                ongoing = False

        return result
