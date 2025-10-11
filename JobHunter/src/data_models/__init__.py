"""Data models package for JobHunter application."""

from .job_data import JobData
from .search_request import SearchRequest
from .filtered_jobs import FilteredJobs
from .message_data import MessageData

__all__ = ['JobData', 'SearchRequest', 'FilteredJobs', 'MessageData']
