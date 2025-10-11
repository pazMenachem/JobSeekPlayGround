"""Application manager for the job scraper."""

import logging
import os
import sys
from datetime import datetime
from typing import List, Tuple
from src.job_crawler.job_scraper import JobScraper
from src.job_crawler.browser_manager import WebDriverManager
from src.job_crawler.url_manager import URLManager
from src.job_storage.results_manager import ResultsManager
from src.config_manager.config import DEFAULT_KEYWORDS, LOG_LEVEL, TARGET_URLS


class AppManager:
    """Manages the job scraper application lifecycle.
    
    This class handles the complete application flow from initialization
    to cleanup, providing a clean interface for the main application.
    """
    
    def __init__(self) -> None:
        """Initialize the application manager."""
        self.logger = logging.getLogger(__name__)
        self.driver_manager = None
        self.job_scraper = None
        self.url_manager = None
        self.results_manager = None

    def run(self) -> None:
        """Run the complete application."""
        try:
            # Setup logging
            self._setup_logging()
            
            # Initialize and run with WebDriver
            with WebDriverManager() as driver:
                self._initialize_components(driver)
                self._run_scraping_session()
     
        except Exception as e:
            self.logger.error(f"Application failed: {e}")
            sys.exit(1)
        
        self.logger.info("Job Scraper Application finished")

    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/job_scraper_{timestamp}.log"
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Create handlers
        handlers = [logging.StreamHandler(sys.stdout)]
        
        # Only add file handler if the log file can be created
        try:
            file_handler = logging.FileHandler(log_file)
            handlers.append(file_handler)
        except (OSError, IOError) as e:
            self.logger.warning(f"Could not create log file {log_file}: {e}")
        
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        
        # Disable verbose logging from external libraries
        logging.getLogger('WDM').setLevel(logging.WARNING)
        logging.getLogger('selenium').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        
        self.logger.info(f"Logging to file: {log_file}")
    
    def _initialize_components(self, driver) -> None:
        """Initialize all application components.
        
        Args:
            driver: WebDriver instance for browser automation.
        """
        self.job_scraper = JobScraper(driver)
        self.url_manager = URLManager(driver)
        self.results_manager = ResultsManager()
        
        self.logger.info("Application components initialized")
    
    def _run_scraping_session(self) -> None:
        """Run a complete scraping session."""
        self.logger.info("Starting Job Scraper Application")
        
        # Get configuration
        urls_to_scrape = TARGET_URLS
        keywords = DEFAULT_KEYWORDS
        
        self.logger.info(f"Scraping {len(urls_to_scrape)} URLs for keywords: {keywords}")
        
        try:
            # Process all URLs
            all_found_jobs = self.url_manager.process_urls(
                urls_to_scrape,
                lambda: self.job_scraper.find_jobs_with_keywords(keywords)
            )
            
            # Add found jobs to results manager
            self.results_manager.add_job_urls(all_found_jobs)
            
            # Save results
            self._save_results(all_found_jobs)
            
            # Mark end time and save run summary
            self.results_manager.mark_end_time()
            self.results_manager.save_run_summary(urls_to_scrape)
            
            # Print summary
            self._print_summary()
            
        except KeyboardInterrupt:
            self.logger.info("Scraping interrupted by user")
        except Exception as e:
            self.logger.error(f"An error occurred during scraping: {e}")
            raise
    
    def _save_results(self, found_jobs: List[Tuple[str, str]]) -> None:
        """Save scraping results to files.
        
        Args:
            found_jobs: List of found job tuples (url, title).
        """
        if found_jobs:
            json_file = self.results_manager.save_results("json")
            self.logger.info(f"Found {len(found_jobs)} jobs and saved to {json_file}")
            
            # Also save as text for easy reading
            txt_file = self.results_manager.save_results("txt")
            self.logger.info(f"Text version saved to {txt_file}")
        else:
            self.logger.info("No jobs found matching the specified keywords")
    
    def _print_summary(self) -> None:
        """Print scraping session summary."""
        summary = self.results_manager.get_results_summary()
        self.logger.info(f"Scraping completed. Summary: {summary}")
    
    