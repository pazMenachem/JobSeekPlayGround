"""WebDriver management for browser automation."""

import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from src.config import BROWSER_TYPE, HEADLESS_MODE, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT


class WebDriverManager:
    """Manages WebDriver instances for browser automation.
    
    This class handles the creation and configuration of WebDriver instances
    for different browsers (Chrome, Firefox, Edge) with proper setup and cleanup.
    """
    
    def __init__(self, browser_type: str = BROWSER_TYPE) -> None:
        """Initialize the WebDriver manager.
        
        Args:
            browser_type: Type of browser to use ('chrome', 'firefox', 'edge').
        """
        self.browser_type = browser_type.lower()
        self.driver: Optional[webdriver.Chrome | webdriver.Firefox | webdriver.Edge] = None
        self.logger = logging.getLogger(__name__)
    
    def create_driver(self) -> webdriver.Chrome | webdriver.Firefox | webdriver.Edge:
        """Create and configure a WebDriver instance.
        
        Returns:
            Configured WebDriver instance.
            
        Raises:
            ValueError: If unsupported browser type is specified.
        """
        try:
            match self.browser_type:
                case "chrome":
                    return self._create_chrome_driver()
                case "firefox":
                    return self._create_firefox_driver()
                case "edge":
                    return self._create_edge_driver()
                case _:
                    raise ValueError(f"Unsupported browser type: {self.browser_type}")

        except Exception as e:
            self.logger.error(f"Failed to create {self.browser_type} driver: {e}")
            raise
    
    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create and configure Chrome WebDriver.
        
        Returns:
            Configured Chrome WebDriver instance.
        """
        options = ChromeOptions()
        if HEADLESS_MODE:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        self._configure_driver(driver)
        return driver
    
    def _create_firefox_driver(self) -> webdriver.Firefox:
        """Create and configure Firefox WebDriver.
        
        Returns:
            Configured Firefox WebDriver instance.
        """
        options = FirefoxOptions()
        if HEADLESS_MODE:
            options.add_argument("--headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        self._configure_driver(driver)
        return driver
    
    def _create_edge_driver(self) -> webdriver.Edge:
        """Create and configure Edge WebDriver.
        
        Returns:
            Configured Edge WebDriver instance.
        """
        options = EdgeOptions()
        if HEADLESS_MODE:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        self._configure_driver(driver)
        return driver
    
    def _configure_driver(self, driver: webdriver.Chrome | webdriver.Firefox | webdriver.Edge) -> None:
        """Configure common driver settings.
        
        Args:
            driver: WebDriver instance to configure.
        """
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
    
    def get_driver(self) -> webdriver.Chrome | webdriver.Firefox | webdriver.Edge:
        """Get or create a WebDriver instance.
        
        Returns:
            WebDriver instance.
        """
        if self.driver is None:
            self.driver = self.create_driver()
        return self.driver
    
    def quit_driver(self) -> None:
        """Close and quit the WebDriver instance."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {e}")
            finally:
                self.driver = None
    
    def __enter__(self):
        """Context manager entry."""
        return self.get_driver()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.quit_driver()
