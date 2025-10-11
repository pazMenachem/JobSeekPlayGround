"""Job storage manager for data persistence operations."""

from typing import List
from .results_manager import ResultsManager
from src.data_models import JobData
from src.logger import get_logger


class JobStorageManager:
    """Manages job data storage operations.
    
    This class handles saving job data using our data models
    and provides simple JSON storage functionality.
    """
    
    def __init__(self) -> None:
        """Initialize the job storage manager."""
        self.logger = get_logger("job_storage")
        self.results_manager = ResultsManager()
    
    def save_jobs(self, jobs: List[JobData]) -> None:
        """Save job data to storage.
        
        Args:
            jobs: List of JobData objects to save
        """
        self.logger.info(f"Saving {len(jobs)} jobs to storage")
        
        try:
            # Add jobs to results manager
            self.results_manager.add_jobs(jobs)
            
            # Save to JSON
            json_file = self.results_manager.save_to_json()
            
            self.logger.info(f"Jobs saved to {json_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving jobs: {e}")
            raise
    
    def get_jobs_summary(self) -> str:
        """Get summary of stored jobs.
        
        Returns:
            String summary of job data
        """
        return self.results_manager.get_summary()
