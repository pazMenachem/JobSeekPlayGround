"""URL management for handling multiple URLs and pagination."""

import logging
import time
from typing import List, Optional, Callable, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.config import MAX_PAGES_PER_URL


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
            # Check if we've reached the maximum pages limit
            if self.current_page >= MAX_PAGES_PER_URL:
                self.logger.info(f"Reached maximum pages limit ({MAX_PAGES_PER_URL})")
                return False
            
            next_page_element = self._find_next_page_element()
            
            if next_page_element is None:
                self.logger.info("No next page found")
                return False
            
            # Get current URL before clicking
            current_url = self.driver.current_url
            self.logger.info(f"Attempting to navigate from page {self.current_page} to next page")
            
            # Scroll to element and wait
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_element)
            time.sleep(2)  # Give more time for dynamic content
            
            # Try different click methods
            click_success = False
            
            # Method 1: Regular click
            try:
                next_page_element.click()
                click_success = True
                self.logger.debug("Regular click succeeded")
            except Exception as e:
                self.logger.debug(f"Regular click failed: {str(e)[:50]}...")
            
            # Method 2: JavaScript click
            if not click_success:
                try:
                    self.driver.execute_script("arguments[0].click();", next_page_element)
                    click_success = True
                    self.logger.debug("JavaScript click succeeded")
                except Exception as e:
                    self.logger.debug(f"JavaScript click failed: {str(e)[:50]}...")
            
            # Method 3: ActionChains click
            if not click_success:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(self.driver).move_to_element(next_page_element).click().perform()
                    click_success = True
                    self.logger.debug("ActionChains click succeeded")
                except Exception as e:
                    self.logger.debug(f"ActionChains click failed: {str(e)[:50]}...")
            
            if not click_success:
                self.logger.warning("All click methods failed")
                return False
            
            # Wait for page to load and URL to change
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda driver: driver.current_url != current_url
                )
                self.logger.info(f"URL changed from {current_url} to {self.driver.current_url}")
            except TimeoutException:
                # Sometimes the URL doesn't change but content does (AJAX)
                self.logger.info("URL didn't change, but page content may have updated")
            
            # Wait for page to be ready
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
        self.logger.info("Searching for next page element...")
        
        # Quick check: try the most common selectors first (fastest)
        quick_selectors = [
            "a[aria-label='Next']",
            "a[aria-label='next']", 
            ".next-page",
            ".pagination .next",
            "a:contains('Next')",
            "a:contains('>')"
        ]
        
        for selector in quick_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for element in elements:
                        try:
                            if element.is_displayed() and element.is_enabled():
                                self.logger.info(f"Found next page element with quick selector: {selector}")
                                return element
                        except Exception:
                            continue
            except Exception:
                continue
        
        # If quick selectors fail, try XPath for text-based search (faster than complex CSS)
        try:
            xpath_queries = [
                "//a[contains(text(), 'Next')]",
                "//a[contains(text(), '>')]",
                "//button[contains(text(), 'Next')]"
            ]
            
            for xpath in xpath_queries:
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    if elements:
                        for element in elements:
                            try:
                                if element.is_displayed() and element.is_enabled():
                                    self.logger.info(f"Found next page element with XPath: {xpath}")
                                    return element
                            except Exception:
                                continue
                except Exception:
                    continue
        except Exception:
            pass
        
        # Last resort: try remaining CSS selectors (but limit to 5 most likely)
        fallback_selectors = [
            ".pagination-next",
            ".next",
            "[data-testid='pagination-next']",
            "button[aria-label='Next']",
            ".pagination a:last-child"
        ]
        
        for selector in fallback_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for element in elements:
                        try:
                            if element.is_displayed() and element.is_enabled():
                                self.logger.info(f"Found next page element with fallback selector: {selector}")
                                return element
                        except Exception:
                            continue
            except Exception:
                continue
        
        self.logger.warning("No next page element found")
        return None
    
    
    def process_urls(self, urls: List[str], scraper_callback: Callable[[], List[Tuple[str, str]]]) -> List[Tuple[str, str]]:
        """Process multiple URLs with pagination.
        
        Args:
            urls: List of URLs to process.
            scraper_callback: Function to call for each page (should accept no arguments).
            
        Returns:
            List of all found job tuples (url, title).
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
            
            self.logger.info(f"Completed processing {url}, found {len([job for job in all_found_jobs if url in job[0]])} jobs")
        
        return all_found_jobs
