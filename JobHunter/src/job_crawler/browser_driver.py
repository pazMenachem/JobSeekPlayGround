"""Browser driver for automation."""

import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from src.config import browser_settings


class BrowserDriver:
    """Browser driver for automation.
    
    Creates and configures WebDriver instances for Chrome and Firefox browsers.
    """
    
    def __init__(
        self, 
        browser: str = browser_settings.browser_type, 
        headless: bool = browser_settings.headless_mode, 
        options: Optional[ChromeOptions | FirefoxOptions] = None
        ) -> None:
        """Initialize the browser driver.
        
        Args:
            browser: Type of browser to use ('chrome', 'firefox').
            headless: Whether to run browser in headless mode.
            options: Custom browser options to use.
        """
        self.browser = browser.lower()
        self.headless = headless
        self.options = options
        self.driver: Optional[webdriver.Chrome | webdriver.Firefox] = None
        self.logger = logging.getLogger(__name__)
    
    def create_driver(self) -> webdriver.Chrome | webdriver.Firefox:
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
                case _:
                    raise ValueError(f"Unsupported browser type: {self.browser}. Supported: chrome, firefox")

        except Exception as e:
            self.logger.error(f"Failed to create {self.browser} driver: {e}")
            raise
    
    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create and configure a Chrome WebDriver instance.
        
        Returns:
            Configured Chrome WebDriver instance.
        """
        options = self.options if self.options else ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        self._configure_driver(driver)
        return driver
    
    def _create_firefox_driver(self) -> webdriver.Firefox:
        """Create and configure a Firefox WebDriver instance.
        
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
    
    def _configure_driver(self, driver: webdriver.Chrome | webdriver.Firefox) -> None:
        """Configure driver settings.
        
        Args:
            driver: WebDriver instance to configure.
        """
        driver.implicitly_wait(browser_settings.implicit_wait)
        driver.set_page_load_timeout(browser_settings.page_load_timeout)
        driver.maximize_window()
    
    def __enter__(self) -> webdriver.Chrome | webdriver.Firefox:
        """Context manager entry.
        
        Returns:
            Configured WebDriver instance.
        """
        self.driver = self.create_driver()
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit.
        
        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")