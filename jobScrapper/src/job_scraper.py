"""Job scraper for finding keywords in job listings."""

import logging
import time
from typing import List, Set, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.config import JOB_TITLE_SELECTORS, SCROLL_PAUSE_TIME


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
    
    def find_jobs_with_keywords(self, keywords: List[str]) -> List[str]:
        """Find job listings that contain any of the specified keywords.
        
        Args:
            keywords: List of keywords to search for in job titles.
            
        Returns:
            List of URLs of jobs that match the keywords.
        """
        self.logger.info(f"Searching for jobs with keywords: {keywords}")
        found_urls = []
        
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
                    job_title = element.text.strip().lower()
                    job_url = element.get_attribute('href')
                    
                    if not job_url:
                        continue
                    
                    # Check if any keyword matches
                    if self._contains_keywords(job_title, keywords):
                        self.logger.info(f"Found matching job: {job_title[:50]}...")
                        found_urls.append(job_url)
                        self.found_jobs.add(job_url)
                        
                except Exception as e:
                    self.logger.warning(f"Error processing job element: {str(e)[:100]}...")
                    continue
                    
        except TimeoutException:
            self.logger.error("Timeout waiting for page to load")
        except Exception as e:
            self.logger.error(f"Error finding jobs: {e}")
        
        return found_urls
    
    def _find_job_elements(self) -> List[webdriver.remote.webelement.WebElement]:
        """Find all job title elements on the current page.
        
        Returns:
            List of WebElement objects representing job titles.
        """
        job_elements = []
        
        for selector in JOB_TITLE_SELECTORS:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    self.logger.info(f"Found {len(elements)} elements with selector: {selector}")
                    job_elements.extend(elements)
                    break  # Use the first working selector
            except Exception as e:
                self.logger.debug(f"Selector {selector} failed: {e}")
                continue
        
        return job_elements
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the specified keywords.
        
        Args:
            text: Text to search in.
            keywords: List of keywords to search for.
            
        Returns:
            True if any keyword is found in the text.
        """
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    
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
