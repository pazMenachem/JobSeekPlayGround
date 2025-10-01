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
    
    def __init__(self, browser: str = BROWSER_TYPE, headless: bool = HEADLESS_MODE, options: Optional[ChromeOptions | FirefoxOptions | EdgeOptions] = None) -> None:
        """Initialize the WebDriver manager.
        
        Args:
            browser: Type of browser to use ('chrome', 'firefox', 'edge').
            headless: Whether to run browser in headless mode.
            options: Custom browser options to use.
        """
        self.browser = browser.lower()
        self.headless = headless
        self.options = options
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
            match self.browser:
                case "chrome":
                    return self._create_chrome_driver()
                case "firefox":
                    return self._create_firefox_driver()
                case "edge":
                    return self._create_edge_driver()
                case _:
                    raise ValueError(f"Unsupported browser type: {self.browser}")

        except Exception as e:
            self.logger.error(f"Failed to create {self.browser} driver: {e}")
            raise
    
    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create and configure Chrome WebDriver.
        
        Returns:
            Configured Chrome WebDriver instance.
        """
        options = self.options if self.options else ChromeOptions()
        if self.headless:
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
        options = self.options if self.options else FirefoxOptions()
        if self.headless:
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
        options = self.options if self.options else EdgeOptions()
        if self.headless:
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
    
    def _get_chrome_options(self) -> ChromeOptions:
        """Get Chrome options with current settings.
        
        Returns:
            Configured Chrome options.
        """
        options = self.options if self.options else ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        return options
    
    def _get_firefox_options(self) -> FirefoxOptions:
        """Get Firefox options with current settings.
        
        Returns:
            Configured Firefox options.
        """
        options = self.options if self.options else FirefoxOptions()
        if self.headless:
            options.add_argument("--headless")
        return options
    
    def _get_edge_options(self) -> EdgeOptions:
        """Get Edge options with current settings.
        
        Returns:
            Configured Edge options.
        """
        options = self.options if self.options else EdgeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options
    
    def _get_driver(self) -> webdriver.Chrome | webdriver.Firefox | webdriver.Edge:
        """Get or create a WebDriver instance (alias for get_driver).
        
        Returns:
            WebDriver instance.
        """
        return self.get_driver()
