"""Tests for JobScraper class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from src.job_scraper import JobScraper


class TestJobScraper:
    """Test JobScraper functionality."""
    
    @pytest.fixture
    def mock_driver(self):
        """Create a mock WebDriver for testing."""
        driver = Mock()
        driver.execute_script = Mock()
        driver.find_elements = Mock()
        driver.current_url = "https://example.com/jobs"
        return driver
    
    @pytest.fixture
    def job_scraper(self, mock_driver):
        """Create a JobScraper instance for testing."""
        return JobScraper(mock_driver)
    
    @pytest.fixture
    def mock_job_elements(self):
        """Create mock job elements for testing."""
        elements = []
        job_data = [
            ("Python Developer", "https://example.com/job1"),
            ("Software Engineer", "https://example.com/job2"),
            ("Data Scientist", "https://example.com/job3"),
            ("Frontend Developer", "https://example.com/job4"),
            ("Backend Engineer", "https://example.com/job5")
        ]
        
        for title, url in job_data:
            element = Mock()
            element.text = title
            element.get_attribute.return_value = url
            elements.append(element)
        
        return elements
    
    @pytest.mark.unit
    def test_init(self, job_scraper, mock_driver):
        """Test JobScraper initialization."""
        assert job_scraper.driver == mock_driver
        assert job_scraper.found_jobs == set()
        assert job_scraper.logger is not None
    
    @pytest.mark.unit
    def test_contains_keywords_true(self, job_scraper):
        """Test keyword matching when keywords are found."""
        text = "Senior Python Developer"
        keywords = ["python", "developer"]
        
        result = job_scraper._contains_keywords(text, keywords)
        assert result is True
    
    @pytest.mark.unit
    def test_contains_keywords_false(self, job_scraper):
        """Test keyword matching when keywords are not found."""
        text = "Marketing Manager"
        keywords = ["python", "developer"]
        
        result = job_scraper._contains_keywords(text, keywords)
        assert result is False
    
    @pytest.mark.unit
    def test_contains_keywords_case_insensitive(self, job_scraper):
        """Test keyword matching is case insensitive."""
        text = "PYTHON DEVELOPER"
        keywords = ["python", "developer"]
        
        result = job_scraper._contains_keywords(text, keywords)
        assert result is True
    
    @pytest.mark.unit
    def test_contains_keywords_partial_match(self, job_scraper):
        """Test keyword matching with partial matches."""
        text = "Python Programming Expert"
        keywords = ["python", "programming"]
        
        result = job_scraper._contains_keywords(text, keywords)
        assert result is True
    
    @pytest.mark.unit
    def test_contains_keywords_empty_keywords(self, job_scraper):
        """Test keyword matching with empty keywords list."""
        text = "Python Developer"
        keywords = []
        
        result = job_scraper._contains_keywords(text, keywords)
        assert result is False
    
    @pytest.mark.unit
    def test_contains_keywords_empty_text(self, job_scraper):
        """Test keyword matching with empty text."""
        text = ""
        keywords = ["python", "developer"]
        
        result = job_scraper._contains_keywords(text, keywords)
        assert result is False
    
    @pytest.mark.unit
    def test_find_job_elements_success(self, job_scraper, mock_driver, mock_job_elements):
        """Test finding job elements successfully."""
        # Mock the driver to return elements for the first selector
        mock_driver.find_elements.return_value = mock_job_elements
        
        elements = job_scraper._find_job_elements()
        
        assert len(elements) == len(mock_job_elements)
        # The method now tries multiple selectors, so we expect multiple calls
        assert mock_driver.find_elements.call_count >= 1
    
    @pytest.mark.unit
    def test_find_job_elements_no_elements(self, job_scraper, mock_driver):
        """Test finding job elements when no elements are found."""
        mock_driver.find_elements.return_value = []
        
        elements = job_scraper._find_job_elements()
        
        assert elements == []
    
    @pytest.mark.unit
    def test_find_job_elements_exception(self, job_scraper, mock_driver):
        """Test finding job elements when exception occurs."""
        mock_driver.find_elements.side_effect = Exception("Test exception")
        
        elements = job_scraper._find_job_elements()
        
        assert elements == []
    
    @pytest.mark.unit
    def test_scroll_page_success(self, job_scraper, mock_driver):
        """Test scrolling page successfully."""
        # Mock scroll height changes
        mock_driver.execute_script.side_effect = [1000, 1000, 1500, 1500, 1500]
        
        job_scraper._scroll_page()
        
        # Should call execute_script multiple times
        assert mock_driver.execute_script.call_count >= 2
    
    @pytest.mark.unit
    def test_scroll_page_exception(self, job_scraper, mock_driver):
        """Test scrolling page when exception occurs."""
        mock_driver.execute_script.side_effect = Exception("Test exception")
        
        # Should not raise exception
        job_scraper._scroll_page()
    
    @pytest.mark.unit
    def test_get_found_jobs(self, job_scraper):
        """Test getting found jobs."""
        # Add some jobs
        job_scraper.found_jobs.add("https://example.com/job1")
        job_scraper.found_jobs.add("https://example.com/job2")
        
        found_jobs = job_scraper.get_found_jobs()
        
        assert len(found_jobs) == 2
        assert "https://example.com/job1" in found_jobs
        assert "https://example.com/job2" in found_jobs
        # Should return a copy, not the original set
        assert found_jobs is not job_scraper.found_jobs
    
    @pytest.mark.unit
    def test_clear_found_jobs(self, job_scraper):
        """Test clearing found jobs."""
        # Add some jobs
        job_scraper.found_jobs.add("https://example.com/job1")
        job_scraper.found_jobs.add("https://example.com/job2")
        
        assert len(job_scraper.found_jobs) == 2
        
        job_scraper.clear_found_jobs()
        
        assert len(job_scraper.found_jobs) == 0
    
    @pytest.mark.integration
    def test_find_jobs_with_keywords_success(self, job_scraper, mock_driver, mock_job_elements):
        """Test finding jobs with keywords successfully."""
        # Mock WebDriverWait
        with patch('src.job_scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = True
            
            # Mock finding job elements
            mock_driver.find_elements.return_value = mock_job_elements
            
            # Mock scrolling
            with patch.object(job_scraper, '_scroll_page'):
                keywords = ["python", "developer"]
                found_urls = job_scraper.find_jobs_with_keywords(keywords)
                
                # Should find jobs with matching keywords
                assert len(found_urls) > 0
                assert len(job_scraper.found_jobs) > 0
    
    @pytest.mark.integration
    def test_find_jobs_with_keywords_timeout(self, job_scraper, mock_driver):
        """Test finding jobs when timeout occurs."""
        with patch('src.job_scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.side_effect = TimeoutException("Timeout")
            
            keywords = ["python", "developer"]
            found_urls = job_scraper.find_jobs_with_keywords(keywords)
            
            assert found_urls == []
    
    @pytest.mark.integration
    def test_find_jobs_with_keywords_exception(self, job_scraper, mock_driver):
        """Test finding jobs when exception occurs."""
        with patch('src.job_scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.side_effect = Exception("Test exception")
            
            keywords = ["python", "developer"]
            found_urls = job_scraper.find_jobs_with_keywords(keywords)
            
            assert found_urls == []
    
    @pytest.mark.unit
    def test_find_jobs_with_keywords_no_href(self, job_scraper, mock_driver):
        """Test finding jobs when elements have no href attribute."""
        # Create mock elements without href
        element = Mock()
        element.text = "Python Developer"
        element.get_attribute.return_value = None  # No href
        
        mock_driver.find_elements.return_value = [element]
        
        with patch('src.job_scraper.WebDriverWait'):
            with patch.object(job_scraper, '_scroll_page'):
                keywords = ["python"]
                found_urls = job_scraper.find_jobs_with_keywords(keywords)
                
                # Should not find any jobs
                assert found_urls == []
    
    @pytest.mark.unit
    def test_find_jobs_with_keywords_element_exception(self, job_scraper, mock_driver):
        """Test finding jobs when processing individual elements fails."""
        # Create mock element that raises exception
        element = Mock()
        element.text = "Python Developer"
        element.get_attribute.side_effect = Exception("Test exception")
        
        mock_driver.find_elements.return_value = [element]
        
        with patch('src.job_scraper.WebDriverWait'):
            with patch.object(job_scraper, '_scroll_page'):
                keywords = ["python"]
                found_urls = job_scraper.find_jobs_with_keywords(keywords)
                
                # Should continue processing despite exception
                assert found_urls == []
    
    @pytest.mark.unit
    def test_find_jobs_with_keywords_empty_keywords(self, job_scraper, mock_driver):
        """Test finding jobs with empty keywords list."""
        with patch('src.job_scraper.WebDriverWait'):
            with patch.object(job_scraper, '_scroll_page'):
                keywords = []
                found_urls = job_scraper.find_jobs_with_keywords(keywords)
                
                assert found_urls == []
    
    @pytest.mark.unit
    def test_find_jobs_with_keywords_no_matching_keywords(self, job_scraper, mock_driver, mock_job_elements):
        """Test finding jobs when no keywords match."""
        with patch('src.job_scraper.WebDriverWait'):
            mock_driver.find_elements.return_value = mock_job_elements
            
            with patch.object(job_scraper, '_scroll_page'):
                keywords = ["marketing", "sales"]  # No matching keywords
                found_urls = job_scraper.find_jobs_with_keywords(keywords)
                
                assert found_urls == []
                assert len(job_scraper.found_jobs) == 0
