"""Page navigation for handling URLs and pagination."""

import logging
import time
from typing import Optional, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from src.config import scraping_settings


class PageNavigator:
    """Page navigation for job scraping.
    
    Handles URL navigation and pagination for comprehensive job scraping.
    """
    
    # Quick selectors (most common pagination elements)
    QUICK_SELECTORS: List[str] = [
        "a[aria-label='Next']",
        "a[aria-label='next']", 
        ".next-page",
        ".pagination .next",
        "a:contains('Next')",
        "a:contains('>')"
    ]
    
    # XPath queries for text-based search
    XPATH_QUERIES: List[str] = [
        "//a[contains(text(), 'Next')]",
        "//a[contains(text(), '>')]",
        "//button[contains(text(), 'Next')]"
    ]
    
    # Fallback selectors (less common but still useful)
    FALLBACK_SELECTORS: List[str] = [
        ".pagination-next",
        ".next",
        "[data-testid='pagination-next']",
        "button[aria-label='Next']",
        ".pagination a:last-child"
    ]
    
    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox | webdriver.Edge) -> None:
        """Initialize the page navigator.
        
        Args:
            driver: WebDriver instance for browser automation.
        """
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.current_page = 1
    
    def go_to_next_page(self) -> bool:
        """Navigate to the next page if available.
        
        Returns:
            True if successfully moved to next page, False if no next page available.
        """
        try:
            if not self._check_page_limit():
                return False
            
            next_page_element = self._find_next_page_element()

            if next_page_element is None:
                self.logger.info("No next page found")
                return False
            
            current_url = self.driver.current_url
            self.logger.info(f"Attempting to navigate from page {self.current_page} to next page")
            
            if not self._click_next_page_element(next_page_element):
                return False
            
            # Driver timeout already handles page loading
            
            self.current_page += 1
            self.logger.info(f"Successfully moved to page {self.current_page}")
            return True
            
        except TimeoutException:
            self.logger.warning("Timeout waiting for next page to load")
            return False
        except Exception as e:
            self.logger.warning(f"Error navigating to next page: {str(e)[:100]}...")
            return False
    
    def _check_page_limit(self) -> bool:
        """Check if we've reached the maximum pages limit."""
        if self.current_page >= scraping_settings.max_pages_per_url:
            self.logger.info(f"Reached maximum pages limit ({scraping_settings.max_pages_per_url})")
            return False
        return True
    
    def _click_next_page_element(self, next_page_element: webdriver.remote.webelement.WebElement) -> bool:
        """Click the next page element using multiple methods."""
        # Scroll to element and wait
        self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_element)
        time.sleep(2)  # Give more time for dynamic content
        
        # Try different click methods
        click_methods = [
            lambda: next_page_element.click(),
            lambda: self.driver.execute_script("arguments[0].click();", next_page_element),
            lambda: ActionChains(self.driver).move_to_element(next_page_element).click().perform()
        ]
        
        for click_method in click_methods:
            try:
                click_method()
                return True
            except Exception as e:
                continue

        self.logger.error("All click methods failed")
        return False
    
    
    def _find_next_page_element(self) -> Optional[webdriver.remote.webelement.WebElement]:
        """Find the next page button/link."""
        self.logger.info("Searching for next page element...")
        
        # Try all selector types in order
        selector_groups = [
            (self.QUICK_SELECTORS, By.CSS_SELECTOR, "quick selector"),
            (self.XPATH_QUERIES, By.XPATH, "XPath"),
            (self.FALLBACK_SELECTORS, By.CSS_SELECTOR, "fallback selector")
        ]
        
        for selectors, by_method, selector_type in selector_groups:
            element = self._try_selectors(selectors, by_method, selector_type)
            if element:
                return element
        
        self.logger.warning("No next page element found")
        return None
    
    def _try_selectors(
        self, 
        selectors: List[str], 
        by_method: By, 
        selector_type: str
        ) -> Optional[webdriver.remote.webelement.WebElement]:
        """Try a list of selectors and return the first valid element found."""
        for selector in selectors:
            try:
                elements = self.driver.find_elements(by_method, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        self.logger.info(f"Found next page element with {selector_type}: {selector}")
                        return element
            except Exception:
                continue
        return None
