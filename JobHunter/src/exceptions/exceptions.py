GENERAL_EXCEPTION_MESSAGE = "Unknown General Exception"
JOB_CRAWLER_EXCEPTION_MESSAGE = "Error during Job Crawler phase"
LLM_EXCEPTION_MESSAGE = "Error during LLM phase"
NOTIFIER_EXCEPTION_MESSAGE = "Error during Notifier phase"

class JobHunterException(Exception):
    """Base exception for JobHunter."""
    def __init__(self, message: str = GENERAL_EXCEPTION_MESSAGE) -> None:
        super().__init__(message)

class JobCrawlerException(JobHunterException):
    """Exception for job crawling."""
    def __init__(self, message: str = JOB_CRAWLER_EXCEPTION_MESSAGE) -> None:
        super().__init__(message)

class LLMException(JobHunterException):
    """Exception for LLM."""
    def __init__(self, message: str = LLM_EXCEPTION_MESSAGE) -> None:
        super().__init__(message)

class NotifierException(JobHunterException):
    """Exception for notifier."""
    def __init__(self, message: str = NOTIFIER_EXCEPTION_MESSAGE) -> None:
        super().__init__(message)
