"""Job filter manager using abstract LLM interface."""

import json
from typing import List
from src.data_models import JobData, RelevanceStatus
from src.data_models.job_data import log_job_data
from src.logger import get_logger
from src.llm_service.prompt_formatter import PromptFormatter
from src.llm_service.llm_base import LLMInterface


class LLMService:
    """LLM Service - handles job data list and updates status.
    
    This class manages the job data list and communicates with LLM providers
    to update job status. 
    """
    
    def __init__(self, llm_provider: LLMInterface) -> None:
        """Initialize the LLM service.
        
        Args:
            llm_provider: LLM provider implementing LLMInterface
            jobs: List of JobData objects to analyze and update
        """
        self.llm_provider = llm_provider
        self.prompt_formatter = PromptFormatter()
        self.logger = get_logger("llm_service")
        
        self.logger.info("LLM service initialized")

    def update_job_status(self, jobs: List[JobData]) -> None:
        """
        Update job status using LLM analysis.
        """
        self.logger.info(f"Updating status for {len(jobs)} jobs using LLM analysis")
        
        # self.llm_provider.is_available()

        ## Main logic
        # Step 1: Format the prompt
        batch_prompt:str = self.prompt_formatter.format_batch_prompt(jobs)
        self.logger.info(f"Formatted prompt: {batch_prompt}")

        # Step 2: Send the prompt to the LLM
        llm_response:str = self.llm_provider.send_to_llm(batch_prompt)
        self.logger.info(f"LLM response: {llm_response}")

        json_response:dict = self._clean_json_response(llm_response)
        
        # Step 3: Parse the response
        self._parse_batch_response(json_response, jobs)
        self.logger.info(f"Job status update complete..")

    def _parse_batch_response(self, json_response: list[dict], jobs: List[JobData]) -> None:
        """Parse the LLM response and update existing job list.
        
        Args:
            json_response: Raw JSON response from the LLM
        """
        try:

            for job_data in json_response:
                id = int(job_data.get("id"))
                reason = job_data.get("reason")
                relevant = RelevanceStatus.from_string(job_data.get("relevant"))
                
                jobs[id].relevant = relevant
                jobs[id].reason = reason

        except (json.JSONDecodeError) as e:
            self.logger.error(f"Failed to parse LLM response, try to check the prompt and the response format")
            raise e
        except (KeyError) as e:
            self.logger.error(f"KeyError: {e}, try to check the prompt and the response format")
            raise e
        except Exception as e:
            self.logger.error(f"General error: {e}")
            raise e

    def _clean_json_response(self, response: str) -> dict:
        """Clean LLM response by removing markdown code blocks and extra text.
        
        Args:
            response: Raw LLM response that may contain markdown formatting
            
        Returns:
            Cleaned JSON dictionary
        """
        self.logger.info(f"cleaning response and converting to json object..")

        # Remove markdown code blocks
        if "```json" in response:
            # Extract content between ```json and ```
            start = response.find("```json") + 7
            end = response.rfind("```")
            if end > start:
                response = response[start:end].strip()
        elif "```" in response:
            # Handle generic code blocks
            start = response.find("```") + 3
            end = response.rfind("```")
            if end > start:
                response = response[start:end].strip()
        
        # Remove any leading/trailing whitespace
        return json.loads(response.strip())