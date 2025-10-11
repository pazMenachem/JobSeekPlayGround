"""JobData data class for representing job information."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class JobData:
    """Data class representing a job listing.
    
    Attributes:
        id: Unique identifier for the job
        title: Job title
        company: Company name
        url: Job URL
        found_date: Date when job was found (auto-generated if None)
        source_url: URL of the page where job was found
    """
    id: str
    title: str
    company: str
    url: str
    found_date: datetime = None
    source_url: str = ""
    
    def __post_init__(self):
        """Set found_date to current time if not provided."""
        if self.found_date is None:
            self.found_date = datetime.now()
