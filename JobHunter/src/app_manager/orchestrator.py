"""Application orchestrator for coordinating all components."""

from src.logger import get_logger
from src.config import scraping_settings
from src.job_crawler.job_crawler_manager import JobCrawlerManager
from src.job_storage.job_storage_manager import JobStorageManager
from src.llm_communication.gemini_provider import GeminiProvider
from src.llm_communication.llm_communicator import LLMCommunicator
from src.job_filter.job_filter import JobFilter
from src.data_models import JobData, FilteredJobs
from typing import List


class JobHunterOrchestrator:
    """Orchestrates the complete JobHunter application workflow.
    
    This class coordinates all application components and manages
    the overall application flow from start to finish.
    """
    
    def __init__(self) -> None:
        """Initialize the orchestrator."""
        self.logger = get_logger("orchestrator")
        self.job_crawler_manager = JobCrawlerManager() ## Getting urls
        # self.job_storage_manager = JobStorageManager() ## Saving jobs
        # self.job_filter = JobFilter() ## Job Filter (Job Filter module)
        # self.gemini_provider = GeminiProvider() ## LLM Provider (LLM module)
        # self.llm_communicator = LLMCommunicator(self.gemini_provider) ## LLM Communicator (LLM module)
        self.jobs: List[JobData] = []

        self.logger.info("JobHunter orchestrator initialized")
    
    def run(self) -> None:
        """Run the complete application workflow."""

        urls: List[str] = scraping_settings.urls
        keywords: List[str] = scraping_settings.keywords
        
        try:
            self.logger.info("Starting JobHunter application")

            # Step 1: Crawl jobs
            self.logger.info(f"Starting Phase 1")
            self.jobs = self.job_crawler_manager.crawl_jobs(urls, keywords)

            # Step 2: Update job status using LLM
            # self.logger.info(f"Starting Phase 2: Updating job status for {len(self.jobs)} jobs using LLM")
            # self.llm_communicator.update_job_status(self.jobs)
            
            # # Step 3: Filter jobs based on relevance
            # self.logger.info(f"Starting Phase 3: Filtering {len(self.jobs)} jobs based on relevance")
            # filtered_jobs: FilteredJobs = self.job_filter.filter_jobs(self.jobs)
            
            # # Step 4: Save filtered jobs
            # self.logger.info(f"Starting Phase 4: Saving {len(filtered_jobs.relevant_jobs)} filtered jobs")
            # self.job_storage_manager.save_jobs(filtered_jobs.relevant_jobs)

            # # Step 5: Send summary to user
            # self.logger.info(f"Starting Phase 5: Sending summary to user")
            ## TODO: Implement summary sending to user

                
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Application failed: {e}")
            raise
        finally:
            self.logger.info("JobHunter application finished")
