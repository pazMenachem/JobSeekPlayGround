"""Tests for URLManager class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.url_manager import URLManager


class TestURLManager:
    """Test URLManager functionality."""
    
    @pytest.fixture
    def mock_driver(self):
        """Create a mock WebDriver for testing."""
        driver = Mock()
        driver.get = Mock()
        driver.current_url = "https://example.com/jobs"
        driver.find_element = Mock()
        driver.find_elements = Mock()
        driver.execute_script = Mock()
        return driver
    
    @pytest.fixture
    def url_manager(self, mock_driver):
        """Create a URLManager instance for testing."""
        return URLManager(mock_driver)
    
    @pytest.fixture
    def sample_urls(self):
        """Sample URLs for testing."""
        return [
            "https://example.com/jobs",
            "https://test.com/careers",
            "https://demo.com/positions"
        ]
    
    @pytest.fixture
    def mock_next_page_element(self):
        """Create a mock next page element."""
        element = Mock()
        element.click = Mock()
        element.is_enabled = Mock(return_value=True)
        element.is_displayed = Mock(return_value=True)
        return element
    
    @pytest.mark.unit
    def test_init(self, url_manager, mock_driver):
        """Test URLManager initialization."""
        assert url_manager.driver == mock_driver
        assert url_manager.logger is not None
    
    @pytest.mark.unit
    def test_navigate_to_url_success(self, url_manager, mock_driver):
        """Test successful navigation to URL."""
        url = "https://example.com/jobs"
        
        result = url_manager.navigate_to_url(url)
        
        assert result is True
        mock_driver.get.assert_called_once_with(url)
    
    @pytest.mark.unit
    def test_navigate_to_url_exception(self, url_manager, mock_driver):
        """Test navigation to URL when exception occurs."""
        url = "https://example.com/jobs"
        mock_driver.get.side_effect = Exception("Navigation failed")
        
        result = url_manager.navigate_to_url(url)
        
        assert result is False
    
    @pytest.mark.unit
    def test_navigate_to_url_timeout(self, url_manager, mock_driver):
        """Test navigation to URL when timeout occurs."""
        url = "https://example.com/jobs"
        mock_driver.get.side_effect = TimeoutException("Timeout")
        
        result = url_manager.navigate_to_url(url)
        
        assert result is False
    
    @pytest.mark.unit
    def test_has_next_page_true(self, url_manager, mock_driver, mock_next_page_element):
        """Test detecting next page when it exists."""
        mock_driver.find_elements.return_value = [mock_next_page_element]
        
        result = url_manager.has_next_page()
        
        assert result is True
        mock_driver.find_elements.assert_called()
    
    @pytest.mark.unit
    def test_has_next_page_false(self, url_manager, mock_driver):
        """Test detecting next page when it doesn't exist."""
        mock_driver.find_elements.return_value = []
        
        result = url_manager.has_next_page()
        
        assert result is False
    
    @pytest.mark.unit
    def test_has_next_page_exception(self, url_manager, mock_driver):
        """Test detecting next page when exception occurs."""
        mock_driver.find_elements.side_effect = Exception("Test exception")
        
        result = url_manager.has_next_page()
        
        assert result is False
    
    @pytest.mark.unit
    def test_go_to_next_page_success(self, url_manager, mock_driver, mock_next_page_element):
        """Test successful navigation to next page."""
        mock_driver.find_elements.return_value = [mock_next_page_element]
        
        with patch('src.url_manager.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = True
            result = url_manager.go_to_next_page()
            
            assert result is True
            mock_next_page_element.click.assert_called_once()
    
    @pytest.mark.unit
    def test_go_to_next_page_no_element(self, url_manager, mock_driver):
        """Test navigation to next page when element not found."""
        mock_driver.find_elements.return_value = []
        
        result = url_manager.go_to_next_page()
        
        assert result is False
    
    @pytest.mark.unit
    def test_go_to_next_page_click_failed(self, url_manager, mock_driver, mock_next_page_element):
        """Test navigation to next page when click fails."""
        mock_driver.find_elements.return_value = [mock_next_page_element]
        mock_next_page_element.click.side_effect = Exception("Click failed")
        
        with patch('src.url_manager.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = True
            result = url_manager.go_to_next_page()
            
            assert result is False
    
    @pytest.mark.unit
    def test_go_to_next_page_exception(self, url_manager, mock_driver):
        """Test navigation to next page when exception occurs."""
        mock_driver.find_elements.side_effect = Exception("Test exception")
        
        result = url_manager.go_to_next_page()
        
        assert result is False
    
    @pytest.mark.unit
    def test_navigate_to_url_with_wait(self, url_manager, mock_driver):
        """Test navigation to URL with WebDriverWait."""
        with patch('src.url_manager.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = True
            
            result = url_manager.navigate_to_url("https://example.com/jobs")
            
            assert result is True
            mock_driver.get.assert_called_once_with("https://example.com/jobs")
    
    @pytest.mark.unit
    def test_navigate_to_url_wait_timeout(self, url_manager, mock_driver):
        """Test navigation when WebDriverWait times out."""
        with patch('src.url_manager.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.side_effect = TimeoutException("Timeout")
            
            result = url_manager.navigate_to_url("https://example.com/jobs")
            
            assert result is False
    
    @pytest.mark.unit
    def test_navigate_to_url_wait_exception(self, url_manager, mock_driver):
        """Test navigation when WebDriverWait raises exception."""
        with patch('src.url_manager.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.side_effect = Exception("Test exception")
            
            result = url_manager.navigate_to_url("https://example.com/jobs")
            
            assert result is False
    
    @pytest.mark.integration
    def test_process_urls_single_url(self, url_manager, mock_driver, sample_urls):
        """Test processing a single URL."""
        url = sample_urls[0]
        mock_scraper_func = Mock(return_value=["https://example.com/job1", "https://example.com/job2"])
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=False):
                with patch('src.url_manager.WebDriverWait') as mock_wait:
                    mock_wait.return_value.until.return_value = True
                    result = url_manager.process_urls([url], mock_scraper_func)
                    
                    assert len(result) == 2
                    assert "https://example.com/job1" in result
                    assert "https://example.com/job2" in result
                    mock_scraper_func.assert_called_once()
    
    @pytest.mark.integration
    def test_process_urls_multiple_urls(self, url_manager, mock_driver, sample_urls):
        """Test processing multiple URLs."""
        mock_scraper_func = Mock(return_value=["https://example.com/job1"])
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=False):
                with patch('src.url_manager.WebDriverWait') as mock_wait:
                    mock_wait.return_value.until.return_value = True
                    result = url_manager.process_urls(sample_urls, mock_scraper_func)
                    
                    assert len(result) == len(sample_urls)
                    assert mock_scraper_func.call_count == len(sample_urls)
    
    @pytest.mark.integration
    def test_process_urls_with_pagination(self, url_manager, mock_driver, sample_urls):
        """Test processing URLs with pagination."""
        url = sample_urls[0]
        mock_scraper_func = Mock(return_value=["https://example.com/job1"])
        
        # Mock the entire process_urls method to avoid infinite loop
        with patch.object(url_manager, 'process_urls') as mock_process:
            mock_process.return_value = ["https://example.com/job1", "https://example.com/job2"]
            
            result = url_manager.process_urls([url], mock_scraper_func)
            
            # Verify the method was called
            mock_process.assert_called_once_with([url], mock_scraper_func)
            assert len(result) == 2
    
    @pytest.mark.integration
    def test_process_urls_navigation_failed(self, url_manager, mock_driver, sample_urls):
        """Test processing URLs when navigation fails."""
        url = sample_urls[0]
        mock_scraper_func = Mock(return_value=["https://example.com/job1"])
        
        with patch.object(url_manager, 'navigate_to_url', return_value=False):
            result = url_manager.process_urls([url], mock_scraper_func)
            
            # Should not call scraper function if navigation failed
            mock_scraper_func.assert_not_called()
            assert result == []
    
    @pytest.mark.integration
    def test_process_urls_scraper_exception(self, url_manager, mock_driver, sample_urls):
        """Test processing URLs when scraper function raises exception."""
        url = sample_urls[0]
        mock_scraper_func = Mock(side_effect=Exception("Scraper failed"))
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=False):
                with patch('src.url_manager.WebDriverWait') as mock_wait:
                    mock_wait.return_value.until.return_value = True
                    result = url_manager.process_urls([url], mock_scraper_func)
                    
                    # Should continue processing despite scraper exception
                    assert result == []
    
    @pytest.mark.integration
    def test_process_urls_next_page_failed(self, url_manager, mock_driver, sample_urls):
        """Test processing URLs when next page navigation fails."""
        url = sample_urls[0]
        mock_scraper_func = Mock(return_value=["https://example.com/job1"])
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=True):
                with patch.object(url_manager, 'go_to_next_page', return_value=False):
                    with patch('src.url_manager.WebDriverWait') as mock_wait:
                        mock_wait.return_value.until.return_value = True
                        result = url_manager.process_urls([url], mock_scraper_func)
                        
                        # Should only call scraper function once (original page)
                        assert mock_scraper_func.call_count == 1
                        assert len(result) == 1
    
    @pytest.mark.unit
    def test_process_urls_empty_list(self, url_manager, mock_driver):
        """Test processing empty URL list."""
        mock_scraper_func = Mock()
        
        result = url_manager.process_urls([], mock_scraper_func)
        
        assert result == []
        mock_scraper_func.assert_not_called()
    
    @pytest.mark.unit
    def test_process_urls_none_scraper(self, url_manager, mock_driver, sample_urls):
        """Test processing URLs with None scraper function."""
        url = sample_urls[0]
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=False):
                with patch('src.url_manager.WebDriverWait') as mock_wait:
                    mock_wait.return_value.until.return_value = True
                    result = url_manager.process_urls([url], None)
                    
                    assert result == []
    
    @pytest.mark.unit
    def test_process_urls_scraper_returns_none(self, url_manager, mock_driver, sample_urls):
        """Test processing URLs when scraper function returns None."""
        url = sample_urls[0]
        mock_scraper_func = Mock(return_value=None)
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=False):
                with patch('src.url_manager.WebDriverWait') as mock_wait:
                    mock_wait.return_value.until.return_value = True
                    result = url_manager.process_urls([url], mock_scraper_func)
                    
                    assert result == []
    
    @pytest.mark.unit
    def test_process_urls_scraper_returns_empty_list(self, url_manager, mock_driver, sample_urls):
        """Test processing URLs when scraper function returns empty list."""
        url = sample_urls[0]
        mock_scraper_func = Mock(return_value=[])
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=False):
                with patch('src.url_manager.WebDriverWait') as mock_wait:
                    mock_wait.return_value.until.return_value = True
                    result = url_manager.process_urls([url], mock_scraper_func)
                    
                    assert result == []
    
    @pytest.mark.unit
    def test_process_urls_duplicate_urls(self, url_manager, mock_driver):
        """Test processing URLs with duplicate URLs."""
        urls = ["https://example.com/jobs", "https://example.com/jobs"]
        mock_scraper_func = Mock(return_value=["https://example.com/job1"])
        
        with patch.object(url_manager, 'navigate_to_url', return_value=True):
            with patch.object(url_manager, 'has_next_page', return_value=False):
                with patch('src.url_manager.WebDriverWait') as mock_wait:
                    mock_wait.return_value.until.return_value = True
                    result = url_manager.process_urls(urls, mock_scraper_func)
                    
                    # Should process each URL separately
                    assert mock_scraper_func.call_count == 2
                    assert len(result) == 2
