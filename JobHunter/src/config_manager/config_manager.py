"""Config manager for application configuration."""

from typing import List
from .config import DEFAULT_KEYWORDS, LOG_LEVEL, TARGET_URLS
from src.logger import get_logger


class ConfigManager:
    """Manages application configuration.
    
    This class handles loading and providing configuration settings
    for the application components.
    """
    
    def __init__(self) -> None:
        """Initialize the config manager."""
        self.logger = get_logger("config_manager")
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration settings."""
        self.logger.info("Loading configuration settings")
        
        # Load from config file
        self.urls = TARGET_URLS
        self.keywords = DEFAULT_KEYWORDS
        self.log_level = LOG_LEVEL
        
        self.logger.info(f"Loaded {len(self.urls)} URLs and {len(self.keywords)} keywords")
    
    def get_urls(self) -> List[str]:
        """Get target URLs for scraping.
        
        Returns:
            List of URLs to scrape
        """
        return self.urls
    
    def get_keywords(self) -> List[str]:
        """Get keywords for job searching.
        
        Returns:
            List of keywords to search for
        """
        return self.keywords
    
    def get_log_level(self) -> str:
        """Get logging level.
        
        Returns:
            Logging level string
        """
        return self.log_level
