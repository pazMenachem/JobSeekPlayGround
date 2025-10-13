"""Prompt formatter for creating LLM prompts from job data."""

from typing import List
from src.data_models import JobData
from src.logger import get_logger
from src.config import llm_settings

class PromptFormatter:
    """Formats job data into prompts for LLM analysis."""

    def __init__(self) -> None:
        """Initialize the prompt formatter."""
        self.logger = get_logger("prompt_formatter")
        self.logger.info("Prompt formatter initialized")

    def format_batch_prompt(
        self, 
        jobs: List[JobData], 
        base_prompt: str = llm_settings.base_llm_prompt
        ) -> str:
        """Format jobs into a batch prompt for LLM analysis.
        
        Args:
            jobs: List of JobData objects to analyze
            base_prompt: Base prompt template (default is JOB_FILTER_PROMPT from config)
            
        Returns:
            Formatted prompt string for batch analysis
        """
        # Format jobs for the prompt
        jobs_text = "\n".join([
            f"\nJob {i}:\n"
            f"  Title: {job.title}\n"
            f"  Company: {job.company}\n"
            f"  URL: {job.url}\n"
            f"  Source: {job.source_url}"
            for i, job in enumerate(jobs)
        ])
        
        message_result = f"""{base_prompt}\nJobs to analyze:{jobs_text}"""
        
        self.logger.info(f"Formatted prompt: {message_result}")

        return message_result
