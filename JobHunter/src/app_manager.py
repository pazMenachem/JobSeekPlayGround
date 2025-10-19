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
# [ ] **Telegram Message Length Validation** - Add splitting/truncation
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
            self.jobs = TEST_DATA

            self.logger.info("********* Starting to run *********")
            # # Step 1: Crawl jobs
            # self.logger.info(f"Starting Phase 1")
            # self.jobs = self.job_crawler_service.crawl_jobs()

            # # Step 2: Update job status using LLM
            # self.logger.info(f"Starting Phase 2: Updating job status for {len(self.jobs)} jobs using LLM")
            # prompt: str = MessageFormatterService.format_llm_prompt(self.jobs[:20])
            # self.llm_service.update_job_status(jobs=self.jobs, prompt=prompt)
            
            # # Step 3: Filter jobs based on relevance
            self.logger.info(f"Starting Phase 3: Filtering {len(self.jobs)} jobs based on relevance")
            filtered_jobs: FilteredJobs = self.job_filter.filter_jobs(jobs=self.jobs)

            # # Step 4: Send summary to user
            self.logger.info(f"Starting Phase 4: Sending summary to user")
            
            for provider in self.notifier_service.providers:
                summary: SegmentedMessage = MessageFormatterService.format_summary(
                    filtered_jobs=filtered_jobs,
                    max_length=provider.max_message_length
                    )
                self.notifier_service.send_notification(provider=provider, message=summary)

        except (JobCrawlerException, LLMException, NotifierException) as e:
            for provider in self.notifier_service.providers:
                self.notifier_service.send_notification(provider=provider, message=SegmentedMessage(
                    header="",
                    message_parts=[str(e)]
                ))

        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Application failed: {e}")
            self.notifier_service.send_notification(message="Unknown error occurred")
        finally:
            self.logger.info("********* Finished running *********")
