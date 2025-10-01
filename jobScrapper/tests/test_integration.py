"""Integration tests for the job scraper application."""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.job_scraper import JobScraper
from src.results_manager import ResultsManager


class TestIntegration:
    """Integration tests for the job scraper application."""
    
    @pytest.mark.integration
    def test_results_manager_basic_functionality(self, temp_dir, sample_job_data):
        """Test ResultsManager basic functionality."""
        # Create results manager
        manager = ResultsManager()
        manager.results_dir = Path(temp_dir)
        
        # Add job data
        for job in sample_job_data:
            manager.add_job_url(job["url"], job["title"])
        
        # Save in different formats
        txt_file = manager.save_results("txt")
        json_file = manager.save_results("json")
        
        # Verify files exist
        assert Path(txt_file).exists()
        assert Path(json_file).exists()
        
        # Verify content
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Job Scraping Results" in content
            assert "Total jobs found: 3" in content
    
    @pytest.mark.integration
    def test_job_scraper_keyword_matching(self):
        """Test JobScraper keyword matching functionality."""
        # Mock driver
        mock_driver = Mock()
        mock_driver.find_elements = Mock()
        
        # Create mock elements
        mock_elements = [
            self._create_mock_element("Python Developer", "https://example.com/job1"),
            self._create_mock_element("Java Engineer", "https://example.com/job2"),
            self._create_mock_element("Data Scientist", "https://example.com/job3"),
        ]
        
        mock_driver.find_elements.return_value = mock_elements
        
        # Create job scraper
        scraper = JobScraper(mock_driver)
        
        # Test keyword matching
        keywords = ["python", "developer"]
        found_urls = scraper.find_jobs_with_keywords(keywords)
        
        # Should find matching jobs
        assert len(found_urls) > 0
        assert "https://example.com/job1" in found_urls
    
    def _create_mock_element(self, text: str, href: str) -> Mock:
        """Create a mock element for testing."""
        element = Mock()
        element.text = text
        element.get_attribute.return_value = href
        return element