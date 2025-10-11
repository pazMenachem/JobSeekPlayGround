"""Results management for saving job data."""

import json
import logging
import os
from datetime import datetime
from typing import List
from pathlib import Path
from src.data_models import JobData


class ResultsManager:
    """Manages saving job data to JSON files.
    
    This class handles saving job data using our data models
    and provides simple JSON storage functionality.
    """
    
    def __init__(self) -> None:
        """Initialize the results manager."""
        self.logger = logging.getLogger(__name__)
        self.jobs: List[JobData] = []
        self.run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data_dir = self._setup_data_directory()
    
    def _setup_data_directory(self) -> Path:
        """Set up the data directory for storing results."""
        # Get the directory where the main script is located
        main_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up to the project root (JobHunter directory)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(main_dir)))
        
        # Create data directory next to main.py
        data_dir = Path(project_root) / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        return data_dir
    
    def add_jobs(self, jobs: List[JobData]) -> None:
        """Add job data to the results.
        
        Args:
            jobs: List of JobData objects to add
        """
        self.jobs.extend(jobs)
        self.logger.info(f"Added {len(jobs)} jobs to results")
    
    def save_to_json(self) -> str:
        """Save results to JSON file.
        
        Returns:
            Path to the saved JSON file
        """
        if not self.jobs:
            self.logger.warning("No jobs to save")
            return ""
        
        # Convert JobData objects to dictionaries
        jobs_data = []
        for job in self.jobs:
            job_dict = {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "url": job.url,
                "found_date": job.found_date.isoformat(),
                "source_url": job.source_url
            }
            jobs_data.append(job_dict)
        
        # Create output data
        output_data = {
            "run_timestamp": self.run_timestamp,
            "total_jobs": len(self.jobs),
            "jobs": jobs_data
        }
        
        # Save to file
        filename = f"jobs_{self.run_timestamp}.json"
        filepath = self.data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to: {filepath}")
        return str(filepath)
    
    def get_jobs_count(self) -> int:
        """Get the number of jobs stored.
        
        Returns:
            Number of jobs
        """
        return len(self.jobs)
    
    def get_summary(self) -> str:
        """Get a summary of the stored jobs.
        
        Returns:
            Summary string
        """
        return f"Found {len(self.jobs)} jobs in run {self.run_timestamp}"