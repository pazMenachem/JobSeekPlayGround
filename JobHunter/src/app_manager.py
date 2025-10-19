"""Application orchestrator for coordinating all components."""

from src.logger import get_logger
from src.config import scraping_settings
# from src.job_storage.job_storage import JobStorage
from src.job_crawler_service.job_crawler_service import JobCrawlerService
from src.llm_service.factory import LLMProviderFactory
from src.llm_service.llm_service import LLMService
from src.job_filter.job_filter import JobFilter
from src.notification_service.notifier_service import NotifierService
from src.data_models import JobData, FilteredJobs, RelevanceStatus, SegmentedMessage
from src.message_formatter import MessageFormatterService
from src.exceptions.exceptions import JobCrawlerException, LLMException, NotifierException
from typing import List

TEST_DATA = [
    JobData(
        id="1",
        title="Data Engineer",
        company="Copyleaks",
        url="https://copyleaks.com/careers/data-engineer",
        source_url="https://copyleaks.com/careers",
        relevant=RelevanceStatus.YES,
        reason="Data Engineer"
    ),
    JobData(
        id="2",
        title="QA AUTOMATION ENGINEER",
        company="Copyleaks",
        url="https://copyleaks.com/careers/qa-automation-engineer",
        source_url="https://copyleaks.com/careers",
        relevant=RelevanceStatus.MAYBE,
        reason="QA Automation Engineer"
    ),
    JobData(
        id="3",
        title="Bookkeeper",
        company="Copyleaks",
        url="https://copyleaks.com/careers/bookkeeper",
        source_url="https://copyleaks.com/careers",
        relevant=RelevanceStatus.NO,
        reason="Bookkeeper"
    ),
]


## TODO: >>
# [ ] **Job Storage System Redesign** - Define requirements and implement
# [ ] **Duplicate Job Detection** - Integrate with storage
# [ ] **Handle >20 Jobs with LLM** - Implement batching strategy
# [X] **Telegram Message Length Validation** - Add splitting/truncation
# [X] **Error Message Formatting** - User-friendly notifications


class JobHunterOrchestrator:
    """Orchestrates the complete JobHunter application workflow.
    
    This class coordinates all application components and manages
    the overall application flow from start to finish.
    """
    
    def __init__(self) -> None:
        """Initialize the orchestrator."""
        self.logger = get_logger("orchestrator")
        self.job_crawler_manager = None
        self.job_storage_manager = None
        self.job_filter = None
        self.llm_service = None
        self.notifier_service = None
        self.jobs: List[JobData] = []

        self._setup()
        self.logger.info("JobHunter orchestrator initialized")

    def _setup(self) -> None:
        """Setup the orchestrator."""
        self.job_crawler_service = JobCrawlerService()
        self.llm_provider = LLMProviderFactory.create_provider()
        self.llm_service = LLMService(self.llm_provider)
        self.job_filter = JobFilter()
        self.notifier_service = NotifierService()

        ## TODO: shouldnt be hardcoded, should be set in the config file.
        self.notifier_service.set_providers("telegram")
    
    def run(self) -> None:
        """Run the complete application workflow."""

        try:
            filtered_jobs: FilteredJobs = None
            self.jobs = [
                JobData(
                    id=f"{i}",
                    title=f"Data Engineer {i}",
                    company=f"Company {i}",
                    url=f"https://company{i}.com/careers/data-engineer",
                    source_url=f"https://company{i}.com/careers",
                    relevant=RelevanceStatus.YES,
                    reason=f"Data Engineer {i}"
                )
                for i in range(1, 101)
            ]

            self.logger.info("********* Starting to run *********")
            
            # Step 1: Crawl jobs
            self._crawl_jobs()

            # Step 2: Update job status using LLM
            self._update_job_status()
            
            # Step 3: Filter jobs based on relevance
            filtered_jobs: FilteredJobs = self._filter_jobs()
            
            # Step 4: Send summary to user
            self._send_summary(filtered_jobs=filtered_jobs)
            
            self.logger.info("********* Application finished successfully *********")
            
        except (JobCrawlerException, LLMException, NotifierException) as e:
            self._send_component_error(error=e)

        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")

        except Exception as e:
            self._send_unknown_error(error=e)
            
        finally:
            self.logger.info("********* Finished running *********")
        
    def _crawl_jobs(self) -> None:
        """Crawl jobs."""
        self.logger.info(f"Starting Phase 1: Crawling jobs")
        self.jobs = self.job_crawler_service.crawl_jobs()

    def _update_job_status(self) -> None:
        """Update job status using LLM."""
        self.logger.info(f"Starting Phase 2: Updating job status for {len(self.jobs)} jobs using LLM")
        prompt: str = MessageFormatterService.format_llm_prompt(self.jobs[:20])
        self.llm_service.update_job_status(jobs=self.jobs, prompt=prompt)
        
    def _filter_jobs(self) -> FilteredJobs:
        """Filter jobs based on relevance."""
        self.logger.info(f"Starting Phase 3: Filtering {len(self.jobs)} jobs based on relevance")
        filtered_jobs: FilteredJobs = self.job_filter.filter_jobs(jobs=self.jobs)
        return filtered_jobs
        
    def _send_summary(self, *, filtered_jobs: FilteredJobs) -> None:
        """Send summary to user."""
        self.logger.info(f"Starting Phase 4: Sending summary to user")

        for provider in self.notifier_service.providers:
            summary: SegmentedMessage = MessageFormatterService.format_summary(
                filtered_jobs=filtered_jobs,
                max_length=provider.max_message_length
                )
        self._send_message(message=summary)
    
    def _send_component_error(self, *, error: Exception) -> None:
        """Send component error to user."""
        self.logger.error(f"Error in {error.__class__.__name__}")
        
        message: SegmentedMessage = SegmentedMessage(
            header="",
            message_parts=[str(error.message)]
        )
        self._send_message(message=message)
    
    def _send_unknown_error(self, *, error: Exception) -> None:
        """Send unknown error to user."""
        self.logger.error(f"Application failed: {error}")
        
        message: SegmentedMessage = SegmentedMessage(
            header="",
            message_parts=["Unknown error occurred, Check the logs."]
        )
        self._send_message(message=message)
    
    def _send_message(self, *, message: SegmentedMessage) -> None:
        """Send message to user."""
        for provider in self.notifier_service.providers:
            self.notifier_service.send_notification(
                    provider=provider,
                    message=message
                )