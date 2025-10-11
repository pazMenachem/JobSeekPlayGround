"""Job crawler manager for coordinating job scraping operations."""

from typing import List
from .job_scraper import JobScraper
from .browser_manager import WebDriverManager
from .url_manager import URLManager
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
        self.url_manager = None
    
    def crawl_jobs(self, urls: List[str], keywords: List[str]) -> List[JobData]:
        """Crawl jobs from specified URLs.
        
        Args:
            urls: List of URLs to crawl
            keywords: List of keywords to search for
            
        Returns:
            List of JobData objects for found jobs
        """
        self.logger.info(f"Starting job crawl for {len(urls)} URLs")
        
        all_found_jobs = []
        
        try:
            with WebDriverManager() as driver:
                # Initialize components
                self.job_scraper = JobScraper(driver)
                self.url_manager = URLManager(driver)
                
                # Process all URLs
                job_tuples = self.url_manager.process_urls(
                    urls,
                    lambda: self.job_scraper.find_jobs_with_keywords(keywords)
                )
                
                # Convert tuples to JobData objects
                for i, (job_url, job_title) in enumerate(job_tuples):
                    job_data = JobData(
                        id=f"job_{i+1}",
                        title=job_title,
                        company="Unknown",  # Will be extracted later
                        url=job_url,
                        source_url=urls[0] if urls else ""
                    )
                    all_found_jobs.append(job_data)
                
                self.logger.info(f"Found {len(all_found_jobs)} jobs")
                
        except Exception as e:
            self.logger.error(f"Error during job crawling: {e}")
            raise
        
        return all_found_jobs
