"""Tests for ResultsManager class."""

import json
import csv
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, mock_open

import pytest
from src.results_manager import ResultsManager


class TestResultsManager:
    """Test ResultsManager functionality."""
    
    @pytest.fixture
    def results_manager(self, temp_dir):
        """Create a ResultsManager instance for testing."""
        with patch('src.results_manager.Path') as mock_path:
            mock_path.return_value.mkdir.return_value = None
            mock_path.return_value.__truediv__ = lambda self, other: Path(temp_dir) / other
            manager = ResultsManager()
            manager.results_dir = Path(temp_dir)
            return manager
    
    @pytest.mark.unit
    def test_init(self, results_manager):
        """Test ResultsManager initialization."""
        assert results_manager.found_jobs == set()
        assert results_manager.results_data == []
        assert results_manager.results_dir is not None
        assert isinstance(results_manager.run_timestamp, str)
    
    @pytest.mark.unit
    def test_add_job_url_single(self, results_manager):
        """Test adding a single job URL."""
        url = "https://example.com/job1"
        title = "Test Job"
        
        results_manager.add_job_url(url, title)
        
        assert url in results_manager.found_jobs
        assert len(results_manager.results_data) == 1
        assert results_manager.results_data[0]["url"] == url
        assert results_manager.results_data[0]["title"] == title
        assert "found_at" in results_manager.results_data[0]
    
    @pytest.mark.unit
    def test_add_job_url_duplicate(self, results_manager):
        """Test adding duplicate job URLs."""
        url = "https://example.com/job1"
        
        results_manager.add_job_url(url)
        results_manager.add_job_url(url)  # Duplicate
        
        assert len(results_manager.found_jobs) == 1
        assert len(results_manager.results_data) == 1
    
    @pytest.mark.unit
    def test_add_job_urls_multiple(self, results_manager):
        """Test adding multiple job URLs."""
        jobs = [
            ("https://example.com/job1", "Job 1"),
            ("https://example.com/job2", "Job 2"),
            ("https://example.com/job3", "Job 3")
        ]
        
        results_manager.add_job_urls(jobs)
        
        assert len(results_manager.found_jobs) == 3
        assert len(results_manager.results_data) == 3
        for url, title in jobs:
            assert url in results_manager.found_jobs
    
    @pytest.mark.unit
    def test_save_results_txt(self, results_manager, temp_dir):
        """Test saving results as text file."""
        # Add some test data
        results_manager.add_job_url("https://example.com/job1", "Test Job 1")
        results_manager.add_job_url("https://example.com/job2", "Test Job 2")
        
        # Mock the file writing
        with patch('builtins.open', mock_open()) as mock_file:
            file_path = results_manager.save_results("txt")
            
            # Verify file was opened for writing
            mock_file.assert_called_once()
            
            # Verify content was written
            written_content = ''.join(call.args[0] for call in mock_file().write.call_args_list)
            assert "Job Scraping Results" in written_content
            assert "https://example.com/job1" in written_content
            assert "https://example.com/job2" in written_content
            assert "Test Job 1" in written_content
            assert "Test Job 2" in written_content
    
    @pytest.mark.unit
    def test_save_results_json(self, results_manager, temp_dir):
        """Test saving results as JSON file."""
        # Add some test data
        results_manager.add_job_url("https://example.com/job1", "Test Job 1")
        results_manager.add_job_url("https://example.com/job2", "Test Job 2")
        
        # Mock the file writing
        with patch('builtins.open', mock_open()) as mock_file:
            file_path = results_manager.save_results("json")
            
            # Verify file was opened for writing
            mock_file.assert_called_once()
            
            # Verify JSON content was written
            written_content = ''.join(call.args[0] for call in mock_file().write.call_args_list)
            json_data = json.loads(written_content)
            
            assert "metadata" in json_data
            assert "jobs" in json_data
            assert json_data["metadata"]["total_jobs"] == 2
            assert len(json_data["jobs"]) == 2
    
    @pytest.mark.unit
    def test_save_results_csv(self, results_manager, temp_dir):
        """Test saving results as CSV file."""
        # Add some test data
        results_manager.add_job_url("https://example.com/job1", "Test Job 1")
        results_manager.add_job_url("https://example.com/job2", "Test Job 2")
        
        # Mock the file writing
        with patch('builtins.open', mock_open()) as mock_file:
            file_path = results_manager.save_results("csv")
            
            # Verify file was opened for writing
            mock_file.assert_called_once()
    
    @pytest.mark.unit
    def test_save_results_invalid_format(self, results_manager):
        """Test saving results with invalid format."""
        results_manager.add_job_url("https://example.com/job1")
        
        with pytest.raises(ValueError, match="Unsupported format type"):
            results_manager.save_results("invalid")
    
    @pytest.mark.unit
    def test_save_results_empty(self, results_manager):
        """Test saving empty results."""
        with patch('builtins.open', mock_open()) as mock_file:
            file_path = results_manager.save_results("txt")
            assert file_path == ""
    
    @pytest.mark.unit
    def test_save_run_summary(self, results_manager, temp_dir):
        """Test saving run summary."""
        # Add some test data
        results_manager.add_job_url("https://example.com/job1", "Test Job 1")
        results_manager.add_job_url("https://example.com/job2", "Test Job 2")
        
        # Mock the file writing
        with patch('builtins.open', mock_open()) as mock_file:
            file_path = results_manager.save_run_summary()
            
            # Verify file was opened for writing
            mock_file.assert_called_once()
            
            # Verify content was written
            written_content = ''.join(call.args[0] for call in mock_file().write.call_args_list)
            assert "Job Scraper Run Summary" in written_content
            assert "Total Jobs Found: 2" in written_content
            assert "https://example.com/job1" in written_content
            assert "https://example.com/job2" in written_content
    
    @pytest.mark.unit
    def test_get_results_summary(self, results_manager):
        """Test getting results summary."""
        # Add some test data
        results_manager.add_job_url("https://example.com/job1", "Test Job 1")
        results_manager.add_job_url("https://example.com/job2", "Test Job 2")
        
        summary = results_manager.get_results_summary()
        
        assert summary["total_jobs"] == 2
        assert summary["unique_urls"] == 2
        assert "scraped_at" in summary
        assert "jobs" in summary
        assert len(summary["jobs"]) == 2
    
    @pytest.mark.unit
    def test_clear_results(self, results_manager):
        """Test clearing results."""
        # Add some test data
        results_manager.add_job_url("https://example.com/job1", "Test Job 1")
        results_manager.add_job_urls([("https://example.com/job2", "Test Job 2")])
        
        assert len(results_manager.found_jobs) == 2
        assert len(results_manager.results_data) == 2
        
        results_manager.clear_results()
        
        assert len(results_manager.found_jobs) == 0
        assert len(results_manager.results_data) == 0
    
    @pytest.mark.unit
    def test_load_results_from_json(self, results_manager, temp_dir):
        """Test loading results from JSON file."""
        # Create mock JSON data
        json_data = {
            "jobs": [
                {
                    "url": "https://example.com/job1",
                    "title": "Test Job 1",
                    "found_at": "2025-01-01T12:00:00"
                },
                {
                    "url": "https://example.com/job2",
                    "title": "Test Job 2",
                    "found_at": "2025-01-01T12:01:00"
                }
            ]
        }
        
        # Mock file reading
        with patch('builtins.open', mock_open(read_data=json.dumps(json_data))):
            success = results_manager.load_results_from_file("test.json")
            
            assert success is True
            assert len(results_manager.found_jobs) == 2
            assert len(results_manager.results_data) == 2
    
    @pytest.mark.unit
    def test_load_results_from_txt(self, results_manager, temp_dir):
        """Test loading results from text file."""
        # Create mock text data
        txt_data = """# Job Results
https://example.com/job1
https://example.com/job2
https://example.com/job3
"""
        
        # Mock file reading
        with patch('builtins.open', mock_open(read_data=txt_data)):
            success = results_manager.load_results_from_file("test.txt")
            
            assert success is True
            assert len(results_manager.found_jobs) == 3
            assert len(results_manager.results_data) == 3
    
    @pytest.mark.unit
    def test_load_results_invalid_format(self, results_manager):
        """Test loading results from invalid file format."""
        success = results_manager.load_results_from_file("test.xyz")
        assert success is False
    
    @pytest.mark.unit
    def test_load_results_file_not_found(self, results_manager):
        """Test loading results from non-existent file."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            success = results_manager.load_results_from_file("nonexistent.json")
            assert success is False
    
    @pytest.mark.unit
    def test_results_manager_with_custom_output_file(self, temp_dir):
        """Test ResultsManager with custom output file."""
        custom_file = "custom_output.txt"
        manager = ResultsManager(custom_file)
        assert manager.output_file == custom_file
    
    @pytest.mark.unit
    def test_timestamp_format(self, results_manager):
        """Test that timestamp is in correct format."""
        timestamp = results_manager.run_timestamp
        # Should be in format YYYYMMDD_HHMMSS
        assert len(timestamp) == 15  # 8 + 1 + 6
        assert timestamp[8] == "_"
        assert timestamp[:8].isdigit()  # Date part
        assert timestamp[9:].isdigit()  # Time part
