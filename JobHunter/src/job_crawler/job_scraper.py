"""Job scraper for finding keywords in job listings."""

import logging
import time
from typing import List, Set, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.config_manager.config import JOB_TITLE_SELECTORS, SCROLL_PAUSE_TIME


class JobScraper:
    """Scrapes job listings for specific keywords.
    
    This class handles the core functionality of scanning job titles for keywords,
    clicking on matching jobs, and collecting their URLs.
    """
    
    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox | webdriver.Edge) -> None:
        """Initialize the job scraper.
        
        Args:
            driver: WebDriver instance for browser automation.
        """
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.found_jobs: Set[str] = set()  # Store unique job URLs
    
    def find_jobs_with_keywords(self, keywords: List[str]) -> List[Tuple[str, str]]:
        """Find job listings that contain any of the specified keywords.
        
        Args:
            keywords: List of keywords to search for in job titles.
            
        Returns:
            List of tuples containing (job_url, job_title) for jobs that match the keywords.
        """
        self.logger.info(f"Searching for jobs with keywords: {keywords}")
        found_jobs = []
        
        try:
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll to load more content
            self._scroll_page()
            
            # Find all job title elements
            job_elements = self._find_job_elements()
            self.logger.info(f"Found {len(job_elements)} job elements on page")
            
            for element in job_elements:
                try:
                    job_title = element.text.strip()
                    job_url = element.get_attribute('href')
                    
                    if not job_url or not job_title:
                        self.logger.debug(f"Skipping element - missing URL or title: '{job_title}' -> '{job_url}'")
                        continue
                    
                    self.logger.debug(f"Checking job: '{job_title}' -> '{job_url}'")
                    
                    # Check if any keyword matches (case-insensitive)
                    if self._contains_keywords(job_title.lower(), keywords):
                        # Only add if we haven't seen this URL before
                        if job_url not in self.found_jobs:
                            self.logger.info(f"Found matching job: {job_title[:50]}...")
                            found_jobs.append((job_url, job_title))
                            self.found_jobs.add(job_url)
                        else:
                            self.logger.debug(f"Job '{job_title}' already found, skipping duplicate")
                    else:
                        self.logger.debug(f"Job '{job_title}' did not match keywords: {keywords}")
                        
                except Exception as e:
                    self.logger.warning(f"Error processing job element: {str(e)[:100]}...")
                    continue
                    
        except TimeoutException:
            self.logger.error("Timeout waiting for page to load")
        except Exception as e:
            self.logger.error(f"Error finding jobs: {e}")
        
        return found_jobs
    
    def _find_job_elements(self) -> List[webdriver.remote.webelement.WebElement]:
        """Find all job title elements on the current page.
        
        Returns:
            List of WebElement objects representing job titles.
        """
        job_elements = []
        found_selectors = []
        
        for selector in JOB_TITLE_SELECTORS:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    self.logger.info(f"Found {len(elements)} elements with selector: {selector}")
                    job_elements.extend(elements)
                    found_selectors.append(selector)
            except Exception as e:
                self.logger.debug(f"Selector {selector} failed: {e}")
                continue
        
        # Remove duplicates while preserving order
        seen_elements = set()
        unique_elements = []
        for element in job_elements:
            element_id = id(element)
            if element_id not in seen_elements:
                seen_elements.add(element_id)
                unique_elements.append(element)
        
        self.logger.info(f"Total unique job elements found: {len(unique_elements)} using {len(found_selectors)} selectors")
        return unique_elements
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the specified keywords.
        
        Args:
            text: Text to search in.
            keywords: List of keywords to search for.
            
        Returns:
            True if any keyword is found in the text.
        """
        text_lower = text.lower()
        # Pre-compute lowercase keywords for better performance
        keywords_lower = [keyword.lower() for keyword in keywords]
        
        # Check for any keyword match (faster than individual checks)
        return any(keyword in text_lower for keyword in keywords_lower)
    
    
    def _scroll_page(self) -> None:
        """Scroll the page to load more content."""
        try:
            # Get initial page height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for new content to load
                time.sleep(SCROLL_PAUSE_TIME)
                
                # Calculate new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # If no new content loaded, break
                if new_height == last_height:
                    break
                    
                last_height = new_height
                
        except Exception as e:
            self.logger.warning(f"Error scrolling page: {str(e)[:100]}...")
    
    def get_found_jobs(self) -> Set[str]:
        """Get all unique job URLs found during scraping.
        
        Returns:
            Set of unique job URLs.
        """
        return self.found_jobs.copy()
    
    def clear_found_jobs(self) -> None:
        """Clear the list of found jobs."""
        self.found_jobs.clear()
