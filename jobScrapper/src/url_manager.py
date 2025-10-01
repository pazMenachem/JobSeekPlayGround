"""URL management for handling multiple URLs and pagination."""

import logging
import time
from typing import List, Optional, Callable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.config import NEXT_PAGE_SELECTORS, MAX_PAGES_PER_URL


class URLManager:
    """Manages URL navigation and pagination for job scraping.
    
    This class handles navigating through multiple URLs and pagination
    within each URL to ensure comprehensive job scraping.
    """
    
    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox | webdriver.Edge) -> None:
        """Initialize the URL manager.
        
        Args:
            driver: WebDriver instance for browser automation.
        """
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.current_url_index = 0
        self.current_page = 1
    
    def navigate_to_url(self, url: str) -> bool:
        """Navigate to a specific URL.
        
        Args:
            url: URL to navigate to.
            
        Returns:
            True if navigation was successful, False otherwise.
        """
        try:
            self.logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.current_page = 1
            self.logger.info("Successfully navigated to URL")
            return True
            
        except TimeoutException:
            self.logger.error(f"Timeout loading URL: {url}")
            return False
        except Exception as e:
            self.logger.error(f"Error navigating to URL {url}: {str(e)[:100]}...")
            return False
    
    def go_to_next_page(self) -> bool:
        """Navigate to the next page if available.
        
        Returns:
            True if successfully moved to next page, False if no next page available.
        """
        try:
            next_page_element = self._find_next_page_element()
            
            if next_page_element is None:
                self.logger.info("No next page found")
                return False
            
            # Check if we've reached the maximum pages limit
            if self.current_page >= MAX_PAGES_PER_URL:
                self.logger.info(f"Reached maximum pages limit ({MAX_PAGES_PER_URL})")
                return False
            
            # Click on next page
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_element)
            time.sleep(1)
            
            try:
                next_page_element.click()
            except Exception:
                # If regular click fails, try JavaScript click
                self.driver.execute_script("arguments[0].click();", next_page_element)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.current_page += 1
            self.logger.info(f"Successfully moved to page {self.current_page}")
            return True
            
        except TimeoutException:
            self.logger.warning("Timeout waiting for next page to load")
            return False
        except Exception as e:
            self.logger.warning(f"Error navigating to next page: {str(e)[:100]}...")
            return False
    
    def _find_next_page_element(self) -> Optional[webdriver.remote.webelement.WebElement]:
        """Find the next page button/link.
        
        Returns:
            WebElement for next page button if found, None otherwise.
        """
        for selector in NEXT_PAGE_SELECTORS:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Check if the element is clickable and not disabled
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            self.logger.info(f"Found next page element with selector: {selector}")
                            return element
            except Exception as e:
                self.logger.debug(f"Selector {selector} failed: {str(e)[:50]}...")
                continue
        
        # Try to find next page by text content
        try:
            next_links = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Next') or contains(text(), '>') or contains(text(), '→')]")
            for link in next_links:
                if link.is_displayed() and link.is_enabled():
                    self.logger.info("Found next page element by text content")
                    return link
        except Exception as e:
            self.logger.debug(f"Text-based search failed: {str(e)[:50]}...")
        
        return None
    
    def has_next_page(self) -> bool:
        """Check if there is a next page available.
        
        Returns:
            True if next page is available, False otherwise.
        """
        return self._find_next_page_element() is not None
    
    def get_current_page_number(self) -> int:
        """Get the current page number.
        
        Returns:
            Current page number.
        """
        return self.current_page
    
    def reset_pagination(self) -> None:
        """Reset pagination state."""
        self.current_page = 1
        self.logger.info("Pagination state reset")
    
    def process_urls(self, urls: List[str], scraper_callback: Callable[[], List[str]]) -> List[str]:
        """Process multiple URLs with pagination.
        
        Args:
            urls: List of URLs to process.
            scraper_callback: Function to call for each page (should accept no arguments).
            
        Returns:
            List of all found job URLs.
        """
        all_found_jobs = []
        
        for i, url in enumerate(urls):
            self.logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")
            self.current_url_index = i
            
            if not self.navigate_to_url(url):
                self.logger.warning(f"Failed to navigate to {url}, skipping")
                continue
            
            # Process current page and all subsequent pages
            while True:
                try:
                    # Call the scraper callback for current page
                    page_results = scraper_callback()
                    all_found_jobs.extend(page_results)
                    
                    # Try to go to next page
                    if not self.go_to_next_page():
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error processing page: {str(e)[:100]}...")
                    break
            
            self.logger.info(f"Completed processing {url}, found {len([job for job in all_found_jobs if url in job])} jobs")
        
        return all_found_jobs
