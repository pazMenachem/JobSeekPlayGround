"""Job filter manager using abstract LLM interface."""

from typing import List
from src.data_models import JobData, FilteredJobs
from src.logger import get_logger
from src.config_manager.config import JOB_FILTER_LEVEL, JOB_FILTER_PROMPT
from .llm_interface import LLMInterface


class JobFilterManager:
    """Manages job filtering using any LLM provider.
    
    This class uses the abstract LLMInterface, making it easy to switch
    between different LLM providers (Ollama, OpenAI, Gemini, etc.).
    """
    
    def __init__(self, llm_provider: LLMInterface) -> None:
        """Initialize the job filter manager.
        
        Args:
            llm_provider: LLM provider implementing LLMInterface
        """
        self.llm_provider = llm_provider
        self.logger = get_logger("job_filter_manager")
        self.logger.info("Job filter manager initialized")
    
    def filter_jobs(self, jobs: List[JobData]) -> FilteredJobs:
        """Filter jobs based on relevance using LLM analysis.
        
        Args:
            jobs: List of JobData objects to filter
            
        Returns:
            FilteredJobs object with relevant jobs and analysis results
        """
        self.logger.info(f"Starting job filtering for {len(jobs)} jobs")
        
        if not jobs:
            self.logger.warning("No jobs provided for filtering")
            return FilteredJobs(
                relevant_jobs=[],
                total_found=0,
                filtered_count=0
            )
        
        # Check if LLM is available
        if not self.llm_provider.is_available():
            self.logger.error("LLM service not available - this is a critical error")
            raise RuntimeError("LLM service is not available. Cannot filter jobs without LLM.")
        
        # Analyze jobs for relevance
        relevant_jobs = []
        
        for job in jobs:
            self.logger.debug(f"Analyzing job: {job.title}")
            
            # Analyze job relevance using the LLM provider
            response = self.llm_provider.analyze_job_relevance(job, JOB_FILTER_PROMPT)
            
            # Check if job is relevant based on filter level
            if self._should_include_job(response):
                relevant_jobs.append(job)
                self.logger.debug(f"Job '{job.title}' marked as relevant (response: {response})")
            else:
                self.logger.debug(f"Job '{job.title}' marked as not relevant: {response}")
        
        self.logger.info(f"Job filtering complete: {len(relevant_jobs)}/{len(jobs)} jobs relevant")
        
        return FilteredJobs(
            relevant_jobs=relevant_jobs,
            total_found=len(jobs),
            filtered_count=len(relevant_jobs)
        )
    
    def is_llm_available(self) -> bool:
        """Check if LLM service is available.
        
        Returns:
            True if LLM service is available, False otherwise
        """
        return self.llm_provider.is_available()
    
    def _should_include_job(self, response: str) -> bool:
        """Determine if a job should be included based on filter level.
        
        Args:
            response: LLM response ('yes', 'no', 'maybe')
            
        Returns:
            True if job should be included, False otherwise
        """
        filter_level = JOB_FILTER_LEVEL.lower()
        response_lower = response.lower()
        
        if filter_level == "all":
            return True
        elif filter_level == "yes":
            return response_lower == "yes"
        elif filter_level == "maybe":
            return response_lower in ["yes", "maybe"]
        elif filter_level == "no":
            return response_lower == "yes"  # Only include clear yes responses
        else:
            # Default to yes only
            return response_lower == "yes"
