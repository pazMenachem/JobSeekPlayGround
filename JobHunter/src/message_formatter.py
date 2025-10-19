"""Prompt formatter for creating LLM prompts from job data."""

from typing import List
from src.data_models import JobData, FilteredJobs, SegmentedMessage
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
    def format_summary(filtered_jobs: FilteredJobs) -> SegmentedMessage:
        """Format a readable summary of the filtered jobs for notifications.
        
        Args:
            filtered_jobs: FilteredJobs object containing the filtered jobs

        Returns:
            SegmentedMessage with header and message_parts for user notifications
        """
        # Build header
        header = (
            "JobHunter Results Summary\n"
            "\n"
            f"Total jobs found: {filtered_jobs.total_found}\n"
            f"Relevant jobs: {filtered_jobs.filtered_count}\n"
            f"Filtered out: {filtered_jobs.total_found - filtered_jobs.filtered_count}\n"
            "\n"
            "Job Matches:\n"
        )
        
        message_parts = []
        current_part = ""
        
        for i, job in enumerate(filtered_jobs.relevant_jobs, 1):
            reason = job.reason[:100] + "..." if len(job.reason) > 100 else job.reason
            
            job_text = (
                f"{i}. {job.title} at {job.company} ({job.relevant.value})\n"
                f"   {reason}\n"
                f"   {job.url}\n"
                f"\n"
            )
            
            # Check if adding this job would exceed effective limit
            if len(current_part) + len(job_text) > EFFECTIVE_MAX_LENGTH:
                # Save current part and start new one
                message_parts.append(current_part.rstrip())
                current_part = job_text
            else:
                # Add to current part
                current_part += job_text
        
        # Add final part
        if current_part:
            message_parts.append(current_part.rstrip())
        
        # Add timestamp to last part
        timestamp = filtered_jobs.filter_timestamp.strftime("%Y-%m-%d %H:%M:%S") if filtered_jobs.filter_timestamp else "Unknown"
        message_parts[-1] += f"\n\nGenerated: {timestamp}"
        
        return SegmentedMessage(
            header=header,
            message_parts=message_parts
        )