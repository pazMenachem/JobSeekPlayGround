"""Job scraper for finding keywords in job listings."""

import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from src.config import job_site_selectors, scraping_settings
from src.logger import get_logger
from src.data_models.job_data import JobData

class JobScraper:
    """Scrapes job listings for specific keywords."""
    
    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox | webdriver.Edge) -> None:
        """Initialize the job scraper."""
        self.driver = driver
        self.logger = get_logger("job_scraper")
        self.jobs_counter = 1
    
    def scrape_jobs(self, keywords: List[str]) -> List[JobData]:
        """
        Find job listings that contain any of the specified keywords.
        
        Args:
            keywords: List of keywords to search for in job titles.
            
        Returns:
            List of JobData objects for jobs that match the keywords.
        """
        self.logger.info(f"Searching in url {self.driver.current_url} for jobs with keywords: {keywords}")
        result: List[JobData] = []
        
        try:
            self._scroll_page()
                        
            job_elements: List[WebElement] = self._find_job_elements()
            filtered_job_elements: List[WebElement] = self._filter_job_elements(job_elements, keywords)
            
            for element in filtered_job_elements:
                result.append(
                    self._extract_job_data(element, self.jobs_counter)
                    )
                self.jobs_counter += 1

        except TimeoutException:
            self.logger.error("Timeout waiting for page to load")
        except Exception as e:
            self.logger.error(f"Error finding jobs: {e}")
        
        return result

    def _filter_job_elements(self, job_elements: List[WebElement], keywords: List[str]) -> List[WebElement]:
        """
        Filter job elements to only include those that match the keywords.
        
        Args:
            job_elements: List of WebElements to filter.
            
        Returns:
            List of WebElements that match the keywords.
        """
        return [
            element for element in job_elements if 
            self._matches_keywords(element.text.strip(), keywords)
        ]
    
    def _extract_job_data(self, element: WebElement, index: int) -> JobData | None:
        """
        Extract job URL and title from element.
        
        Args:
            element: WebElement to extract job data from.
            
        Returns:
            JobData object, or None if extraction fails.
        """
        return JobData(
            id=f"{index}",
            title=element.text.strip(),
            url=element.get_attribute('href'),
            source_url=self.driver.current_url
        )
    
    def _matches_keywords(self, job_title: str, keywords: List[str]) -> bool:
        """
        Check if job title matches any keywords.
        
        Args:
            job_title: Job title to check.
            keywords: List of keywords to check against.
            
        Returns:
            True if job title matches any keywords, False otherwise.
        """

        title_lower = job_title.lower()
        keywords_lower = [keyword.lower() for keyword in keywords]

        return any(keyword in title_lower for keyword in keywords_lower)
    
    def _find_job_elements(self) -> List[webdriver.remote.webelement.WebElement]:
        """Find all job title elements on the current page."""
        job_elements = []
        
        ## TODO: need to do better job title selectors.
        for selector in job_site_selectors.job_title_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    job_elements.extend(elements)
            except Exception:
                continue
        
        # Remove duplicates
        seen_elements = set()
        unique_elements = []
        for element in job_elements:
            element_id = id(element)
            if element_id not in seen_elements:
                seen_elements.add(element_id)
                unique_elements.append(element)
        
        return unique_elements
    
    def _scroll_page(self) -> None:
        """Scroll the page to load more content."""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scraping_settings.scroll_pause_time)
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
        except Exception as e:
            self.logger.warning(f"Error scrolling page: {e}")
    
