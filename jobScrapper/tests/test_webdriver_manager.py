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
        
        # Only test that the manager is properly initialized
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
        
        assert manager.options == options
    
    @pytest.mark.unit
    def test_get_chrome_options_default(self):
        """Test getting Chrome options with default settings."""
        manager = WebDriverManager()
        options = manager._get_chrome_options()
        
        assert isinstance(options, Options)
    
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
        
        with patch('src.browser_manager.webdriver.Chrome', return_value=mock_chrome_driver):
            driver = manager._get_driver()
            
            assert driver == mock_chrome_driver
    
    @pytest.mark.unit
    def test_get_driver_firefox(self, mock_firefox_driver):
        """Test getting Firefox driver."""
        manager = WebDriverManager(browser="firefox")
        
        with patch('src.browser_manager.webdriver.Firefox', return_value=mock_firefox_driver):
            driver = manager._get_driver()
            
            assert driver == mock_firefox_driver
    
    @pytest.mark.unit
    def test_get_driver_edge(self, mock_edge_driver):
        """Test getting Edge driver."""
        manager = WebDriverManager(browser="edge")
        
        with patch('src.browser_manager.webdriver.Edge', return_value=mock_edge_driver):
            with patch('src.browser_manager.EdgeChromiumDriverManager') as mock_manager:
                mock_manager.return_value.install.return_value = "/fake/path/msedgedriver.exe"
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
        
        with patch('src.browser_manager.webdriver.Chrome', side_effect=Exception("Driver error")):
            with pytest.raises(Exception, match="Driver error"):
                manager._get_driver()
    
    @pytest.mark.unit
    def test_context_manager_enter(self, mock_chrome_driver):
        """Test WebDriverManager as context manager - enter."""
        manager = WebDriverManager()

        with patch.object(manager, 'get_driver', return_value=mock_chrome_driver):
            driver = manager.__enter__()

            assert driver == mock_chrome_driver
    
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

        with patch.object(manager, 'get_driver', return_value=mock_chrome_driver):
            with manager as driver:
                assert driver == mock_chrome_driver
    
    
    
    @pytest.mark.unit
    def test_driver_initialization_with_options(self, mock_chrome_driver):
        """Test driver initialization with custom options."""
        custom_options = Options()
        custom_options.add_argument("--test-arg")
        
        manager = WebDriverManager(browser="chrome", options=custom_options)
        
        with patch('src.browser_manager.webdriver.Chrome', return_value=mock_chrome_driver) as mock_chrome:
            with patch('src.browser_manager.ChromeDriverManager') as mock_manager:
                mock_manager.return_value.install.return_value = "/fake/path/chromedriver.exe"
                driver = manager._get_driver()
                
                # Verify Chrome was called with custom options and service
                mock_chrome.assert_called_once()
                call_args = mock_chrome.call_args
                assert 'options' in call_args.kwargs
                assert 'service' in call_args.kwargs
                assert call_args.kwargs['options'] == custom_options
                assert driver == mock_chrome_driver
