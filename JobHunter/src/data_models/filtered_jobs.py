"""FilteredJobs data class for filtered job results."""

from dataclasses import dataclass
from typing import List
from datetime import datetime
from .job_data import JobData


@dataclass
class FilteredJobs:
    """Data class representing filtered job results.
    
    Attributes:
        relevant_jobs: List of relevant JobData objects
        total_found: Total number of jobs found before filtering
        filtered_count: Number of jobs after filtering
        filter_timestamp: Timestamp when filtering was performed (auto-generated if None)
    """
    relevant_jobs: List[JobData]
    total_found: int
    filtered_count: int
    filter_timestamp: datetime = None
    
    def __post_init__(self):
        """Set filter_timestamp to current time if not provided."""
        if self.filter_timestamp is None:
            self.filter_timestamp = datetime.now()
