"""Application orchestrator for coordinating all components."""

from typing import List
from src.logger import get_logger
from src.config_manager.config_manager import ConfigManager
from src.job_crawler.job_crawler_manager import JobCrawlerManager
from src.job_storage.job_storage_manager import JobStorageManager


class JobHunterOrchestrator:
    """Orchestrates the complete JobHunter application workflow.
    
    This class coordinates all application components and manages
    the overall application flow from start to finish.
    """
    
    def __init__(self) -> None:
        """Initialize the orchestrator."""
        # Get logger
        self.logger = get_logger("orchestrator")
        
        # Initialize component managers
        self.config_manager = ConfigManager()
        self.job_crawler_manager = JobCrawlerManager()
        self.job_storage_manager = JobStorageManager()
        
        self.logger.info("JobHunter orchestrator initialized")
    
    def run(self) -> None:
        """Run the complete application workflow."""
        
        try:
            self.logger.info("Starting JobHunter application")
            
            # Get configuration
            urls = self.config_manager.get_urls()
            keywords = self.config_manager.get_keywords()
            
            self.logger.info(f"Processing {len(urls)} URLs with {len(keywords)} keywords")
            
            # Step 1: Crawl jobs
            found_jobs = self.job_crawler_manager.crawl_jobs(urls, keywords)
            
            if found_jobs:
                # Step 2: Save jobs
                self.job_storage_manager.save_jobs(found_jobs)
                
                # Step 3: Print summary
                summary = self.job_storage_manager.get_jobs_summary()
                self.logger.info(f"Application completed. Summary: {summary}")
            else:
                self.logger.info("No jobs found matching the specified keywords")
                
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Application failed: {e}")
            raise
        finally:
            self.logger.info("JobHunter application finished")
