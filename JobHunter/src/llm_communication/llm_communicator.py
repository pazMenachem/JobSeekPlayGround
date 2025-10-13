"""Job filter manager using abstract LLM interface."""

import json
from typing import List
from src.data_models import JobData, RelevanceStatus
from src.logger import get_logger
from src.config import llm_settings
from src.llm_communication.prompt_formatter import PromptFormatter
from .llm_interface import LLMInterface


class LLMCommunicator:
    """LLM Communicator - handles job data list and updates status.
    
    This class manages the job data list and communicates with LLM providers
    to update job status. 
    """
    
    def __init__(self, llm_provider: LLMInterface, jobs: List[JobData]) -> None:
        """Initialize the LLM communicator.
        
        Args:
            llm_provider: LLM provider implementing LLMInterface
            jobs: List of JobData objects to analyze and update
        """
        self.llm_provider = llm_provider
        self.jobs = jobs
        self.prompt_formatter = PromptFormatter()
        self.logger = get_logger("llm_communicator")
        
        self.logger.info("LLM communicator initialized")

    def update_job_status(self) -> None:
        """
        Update job status using LLM analysis.
        """
        self.logger.info(f"Updating status for {len(self.jobs)} jobs using LLM analysis")
        
        if not self.jobs:
            raise RuntimeError("No jobs provided for analysis")
        
        self.llm_provider.is_available()
        
        self.logger.info("Using batch processing for job analysis")
        
        ## Main logic
        batch_prompt = self.prompt_formatter.format_batch_prompt(self.jobs)
        llm_response = self.llm_provider.send_to_llm(batch_prompt)
        self._parse_batch_response(llm_response)
        
        self.logger.info(f"Job status update complete for {len(self.jobs)} jobs")

    def _parse_batch_response(self, llm_response: str) -> None:
        """Parse the LLM response and update existing job list.
        
        Args:
            llm_response: Raw JSON response from the LLM
        """
        try:
            response_data = json.loads(llm_response)
            jobs_response = response_data.get("jobs")
            
            for job_data in jobs_response:
                index = job_data.get("index")
                reason = job_data.get("reason")
                relevant = RelevanceStatus.from_string(job_data.get("relevant"))
                
                self.jobs[index].relevant = relevant
                self.jobs[index].reason = reason

        except (json.JSONDecodeError) as e:
            self.logger.error(f"Failed to parse LLM response, try to check the prompt and the response format")
            raise e
        except (KeyError) as e:
            self.logger.error(f"KeyError: {e}, try to check the prompt and the response format")
            raise e
        except Exception as e:
            self.logger.error(f"General error: {e}")
            raise e
