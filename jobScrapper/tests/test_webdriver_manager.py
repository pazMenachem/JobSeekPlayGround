"""Tests for WebDriverManager class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from src.browser_manager import WebDriverManager


class TestWebDriverManager:
    """Test WebDriverManager functionality."""
    
    @pytest.fixture
    def mock_chrome_driver(self):
        """Create a mock Chrome WebDriver."""
        driver = Mock(spec=webdriver.Chrome)
        driver.quit = Mock()
        return driver
    
    @pytest.fixture
    def mock_firefox_driver(self):
        """Create a mock Firefox WebDriver."""
        driver = Mock(spec=webdriver.Firefox)
        driver.quit = Mock()
        return driver
    
    @pytest.fixture
    def mock_edge_driver(self):
        """Create a mock Edge WebDriver."""
        driver = Mock(spec=webdriver.Edge)
        driver.quit = Mock()
        return driver
    
    @pytest.mark.unit
    def test_init_default(self):
        """Test WebDriverManager initialization with default settings."""
        manager = WebDriverManager()
        
        assert manager.browser == "chrome"
        assert manager.headless is True
        assert manager.options is None
    
    @pytest.mark.unit
    def test_init_custom(self):
        """Test WebDriverManager initialization with custom settings."""
        options = Options()
        manager = WebDriverManager(
            browser="firefox",
            headless=False,
            options=options
        )
        
        assert manager.browser == "firefox"
        assert manager.headless is False
        assert manager.options == options
    
    @pytest.mark.unit
    def test_get_chrome_options_default(self):
        """Test getting Chrome options with default settings."""
        manager = WebDriverManager()
        options = manager._get_chrome_options()
        
        assert isinstance(options, Options)
        # Check that headless option is set
        assert "--headless" in options.arguments
    
    @pytest.mark.unit
    def test_get_chrome_options_custom(self):
        """Test getting Chrome options with custom settings."""
        custom_options = Options()
        custom_options.add_argument("--custom-arg")
        
        manager = WebDriverManager(options=custom_options)
        options = manager._get_chrome_options()
        
        assert options == custom_options
    
    @pytest.mark.unit
    def test_get_firefox_options_default(self):
        """Test getting Firefox options with default settings."""
        manager = WebDriverManager(browser="firefox")
        options = manager._get_firefox_options()
        
        assert isinstance(options, FirefoxOptions)
        # Check that headless option is set
        assert options.arguments.get("--headless") is True
    
    @pytest.mark.unit
    def test_get_firefox_options_custom(self):
        """Test getting Firefox options with custom settings."""
        custom_options = FirefoxOptions()
        custom_options.add_argument("--custom-arg")
        
        manager = WebDriverManager(browser="firefox", options=custom_options)
        options = manager._get_firefox_options()
        
        assert options == custom_options
    
    @pytest.mark.unit
    def test_get_edge_options_default(self):
        """Test getting Edge options with default settings."""
        manager = WebDriverManager(browser="edge")
        options = manager._get_edge_options()
        
        assert isinstance(options, EdgeOptions)
        # Check that headless option is set
        assert "--headless" in options.arguments
    
    @pytest.mark.unit
    def test_get_edge_options_custom(self):
        """Test getting Edge options with custom settings."""
        custom_options = EdgeOptions()
        custom_options.add_argument("--custom-arg")
        
        manager = WebDriverManager(browser="edge", options=custom_options)
        options = manager._get_edge_options()
        
        assert options == custom_options
    
    @pytest.mark.unit
    def test_get_driver_chrome(self, mock_chrome_driver):
        """Test getting Chrome driver."""
        manager = WebDriverManager(browser="chrome")
        
        with patch('src.webdriver_manager.webdriver.Chrome', return_value=mock_chrome_driver):
            driver = manager._get_driver()
            
            assert driver == mock_chrome_driver
    
    @pytest.mark.unit
    def test_get_driver_firefox(self, mock_firefox_driver):
        """Test getting Firefox driver."""
        manager = WebDriverManager(browser="firefox")
        
        with patch('src.webdriver_manager.webdriver.Firefox', return_value=mock_firefox_driver):
            driver = manager._get_driver()
            
            assert driver == mock_firefox_driver
    
    @pytest.mark.unit
    def test_get_driver_edge(self, mock_edge_driver):
        """Test getting Edge driver."""
        manager = WebDriverManager(browser="edge")
        
        with patch('src.webdriver_manager.webdriver.Edge', return_value=mock_edge_driver):
            driver = manager._get_driver()
            
            assert driver == mock_edge_driver
    
    @pytest.mark.unit
    def test_get_driver_invalid_browser(self):
        """Test getting driver with invalid browser."""
        manager = WebDriverManager(browser="invalid")
        
        with pytest.raises(ValueError, match="Unsupported browser"):
            manager._get_driver()
    
    @pytest.mark.unit
    def test_get_driver_exception(self):
        """Test getting driver when exception occurs."""
        manager = WebDriverManager(browser="chrome")
        
        with patch('src.webdriver_manager.webdriver.Chrome', side_effect=Exception("Driver error")):
            with pytest.raises(Exception, match="Driver error"):
                manager._get_driver()
    
    @pytest.mark.unit
    def test_context_manager_enter(self, mock_chrome_driver):
        """Test WebDriverManager as context manager - enter."""
        manager = WebDriverManager()
        
        with patch.object(manager, '_get_driver', return_value=mock_chrome_driver):
            driver = manager.__enter__()
            
            assert driver == mock_chrome_driver
            assert manager.driver == mock_chrome_driver
    
    @pytest.mark.unit
    def test_context_manager_exit(self, mock_chrome_driver):
        """Test WebDriverManager as context manager - exit."""
        manager = WebDriverManager()
        manager.driver = mock_chrome_driver
        
        manager.__exit__(None, None, None)
        
        mock_chrome_driver.quit.assert_called_once()
    
    @pytest.mark.unit
    def test_context_manager_exit_with_exception(self, mock_chrome_driver):
        """Test WebDriverManager as context manager - exit with exception."""
        manager = WebDriverManager()
        manager.driver = mock_chrome_driver
        
        # Should still quit driver even with exception
        manager.__exit__(Exception("Test exception"), None, None)
        
        mock_chrome_driver.quit.assert_called_once()
    
    @pytest.mark.unit
    def test_context_manager_exit_no_driver(self):
        """Test WebDriverManager as context manager - exit without driver."""
        manager = WebDriverManager()
        
        # Should not raise exception when no driver
        manager.__exit__(None, None, None)
    
    @pytest.mark.unit
    def test_context_manager_exit_quit_exception(self, mock_chrome_driver):
        """Test WebDriverManager as context manager - exit when quit fails."""
        manager = WebDriverManager()
        manager.driver = mock_chrome_driver
        mock_chrome_driver.quit.side_effect = Exception("Quit failed")
        
        # Should not raise exception even if quit fails
        manager.__exit__(None, None, None)
    
    @pytest.mark.integration
    def test_context_manager_full_cycle(self, mock_chrome_driver):
        """Test WebDriverManager as context manager - full cycle."""
        manager = WebDriverManager()
        
        with patch.object(manager, '_get_driver', return_value=mock_chrome_driver):
            with manager as driver:
                assert driver == mock_chrome_driver
                assert manager.driver == mock_chrome_driver
            
            # Driver should be quit after context
            mock_chrome_driver.quit.assert_called_once()
    
    @pytest.mark.unit
    def test_headless_setting_chrome(self):
        """Test headless setting for Chrome."""
        # Test headless=True
        manager = WebDriverManager(browser="chrome", headless=True)
        options = manager._get_chrome_options()
        assert "--headless" in options.arguments
        
        # Test headless=False
        manager = WebDriverManager(browser="chrome", headless=False)
        options = manager._get_chrome_options()
        assert "--headless" not in options.arguments
    
    @pytest.mark.unit
    def test_headless_setting_firefox(self):
        """Test headless setting for Firefox."""
        # Test headless=True
        manager = WebDriverManager(browser="firefox", headless=True)
        options = manager._get_firefox_options()
        assert options.arguments.get("--headless") is True
        
        # Test headless=False
        manager = WebDriverManager(browser="firefox", headless=False)
        options = manager._get_firefox_options()
        assert options.arguments.get("--headless") is not True
    
    @pytest.mark.unit
    def test_headless_setting_edge(self):
        """Test headless setting for Edge."""
        # Test headless=True
        manager = WebDriverManager(browser="edge", headless=True)
        options = manager._get_edge_options()
        assert "--headless" in options.arguments
        
        # Test headless=False
        manager = WebDriverManager(browser="edge", headless=False)
        options = manager._get_edge_options()
        assert "--headless" not in options.arguments
    
    @pytest.mark.unit
    def test_browser_case_insensitive(self):
        """Test that browser name is case insensitive."""
        manager1 = WebDriverManager(browser="CHROME")
        manager2 = WebDriverManager(browser="chrome")
        manager3 = WebDriverManager(browser="Chrome")
        
        assert manager1.browser == "chrome"
        assert manager2.browser == "chrome"
        assert manager3.browser == "chrome"
    
    @pytest.mark.unit
    def test_driver_initialization_with_options(self, mock_chrome_driver):
        """Test driver initialization with custom options."""
        custom_options = Options()
        custom_options.add_argument("--test-arg")
        
        manager = WebDriverManager(browser="chrome", options=custom_options)
        
        with patch('src.webdriver_manager.webdriver.Chrome', return_value=mock_chrome_driver) as mock_chrome:
            driver = manager._get_driver()
            
            # Verify Chrome was called with custom options
            mock_chrome.assert_called_once_with(options=custom_options)
            assert driver == mock_chrome_driver
