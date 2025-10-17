"""Prompt formatter for creating LLM prompts from job data."""

from typing import List
from src.data_models import JobData, FilteredJobs
from src.config import llm_settings

class MessageFormatterService:
    """Message formatter service for creating messages from job data."""

    @staticmethod
    def format_llm_prompt(
        jobs: List[JobData], 
        base_prompt: str = llm_settings.base_llm_prompt
        ) -> str:
        """Format jobs into a LLM prompt for analysis.
        
        Args:
            jobs: List of JobData objects to analyze
            base_prompt: Base prompt template (default is BASE_LLM_PROMPT from config)

        Returns:
            Formatted message string for LLM analysis
        """
        # Format jobs for the message
        jobs_text = "\n".join([
            f"\nid: {i}:\n"
            f"  Title: {job.title}\n"
            f"  Company: {job.company}\n"
            f"  URL: {job.url}\n"
            f"  Source: {job.source_url}\n"
            for i, job in enumerate(jobs)
        ])
            
        message_result = f"""{base_prompt}\nJobs to analyze:\n{jobs_text}"""

        return message_result

    @staticmethod
    def format_summary(filtered_jobs: FilteredJobs) -> str:
        """Format a readable summary of the filtered jobs for notifications.
        
        Args:
            filtered_jobs: FilteredJobs object containing the filtered jobs

        Returns:
            Formatted, readable summary string for user notifications
        """
        # Create summary with all jobs
        summary_lines = [
            "JobHunter Results Summary",
            "",
            f"Total jobs found: {filtered_jobs.total_found}",
            f"Relevant jobs: {filtered_jobs.filtered_count}",
            f"Filtered out: {filtered_jobs.total_found - filtered_jobs.filtered_count}",
            "",
            "Job Matches:"
        ]
        
        # Add all job details
        for i, job in enumerate(filtered_jobs.relevant_jobs, 1):
            reason = job.reason[:100] + "..." if len(job.reason) > 100 else job.reason
            job_line = f"{i}. {job.title} at {job.company} ({job.relevant.value})"
            summary_lines.append(job_line)
            summary_lines.append(f"   {reason}")
            summary_lines.append(f"   {job.url}")
            summary_lines.append("")
        
        # Add timestamp
        timestamp = filtered_jobs.filter_timestamp.strftime("%Y-%m-%d %H:%M:%S") if filtered_jobs.filter_timestamp else "Unknown"
        summary_lines.append(f"Generated: {timestamp}")
        
        return "\n".join(summary_lines)