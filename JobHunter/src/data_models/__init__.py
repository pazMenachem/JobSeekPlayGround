"""Data models package for JobHunter application."""

from .job_data import JobData
from .search_request import SearchRequest
from .filtered_jobs import FilteredJobs
from .message_data import MessageData
from .relevance_status import RelevanceStatus
from .segmented_message import SegmentedMessage

__all__ = ['JobData', 'SearchRequest', 'FilteredJobs', 'MessageData', 'RelevanceStatus', 'SegmentedMessage']
