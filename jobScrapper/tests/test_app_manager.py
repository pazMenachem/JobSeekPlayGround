"""Tests for AppManager class."""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.app_manager import AppManager


class TestAppManager:
    """Test AppManager functionality."""
    
    @pytest.fixture
    def app_manager(self):
        """Create an AppManager instance for testing."""
        return AppManager()
    
    @pytest.fixture
    def mock_driver(self):
        """Create a mock WebDriver for testing."""
        driver = Mock()
        driver.quit = Mock()
        return driver
    
    @pytest.fixture
    def mock_webdriver_manager(self):
        """Create a mock WebDriverManager for testing."""
        manager = Mock()
        manager.__enter__ = Mock(return_value=Mock())
        manager.__exit__ = Mock(return_value=None)
        return manager
    
    @pytest.mark.unit
    def test_init(self, app_manager):
        """Test AppManager initialization."""
        assert app_manager.logger is not None
        assert app_manager.driver_manager is None
        assert app_manager.job_scraper is None
        assert app_manager.url_manager is None
        assert app_manager.results_manager is None
    
    @pytest.mark.unit
    def test_setup_logging(self, app_manager, temp_dir):
        """Test logging setup."""
        with patch('src.app_manager.os.makedirs'):
            with patch('src.app_manager.logging.basicConfig') as mock_basic_config:
                with patch('src.app_manager.logging.getLogger') as mock_get_logger:
                    mock_logger = Mock()
                    mock_get_logger.return_value = mock_logger
                    
                    app_manager.setup_logging()
                    
                    # Verify logging was configured
                    mock_basic_config.assert_called_once()
                    mock_get_logger.assert_called()
    
    @pytest.mark.unit
    def test_setup_logging_creates_logs_dir(self, app_manager):
        """Test that setup_logging creates logs directory."""
        with patch('src.app_manager.os.makedirs') as mock_makedirs:
            with patch('src.app_manager.logging.basicConfig'):
                with patch('src.app_manager.logging.getLogger'):
                    app_manager.setup_logging()
                    
                    # Verify logs directory was created
                    mock_makedirs.assert_called_with("logs", exist_ok=True)
    
    @pytest.mark.unit
    def test_setup_logging_sets_external_loggers(self, app_manager):
        """Test that setup_logging sets external logger levels."""
        with patch('src.app_manager.os.makedirs'):
            with patch('src.app_manager.logging.basicConfig'):
                with patch('src.app_manager.logging.getLogger') as mock_get_logger:
                    mock_logger = Mock()
                    mock_get_logger.return_value = mock_logger
                    
                    app_manager.setup_logging()
                    
                    # Verify external loggers were set to WARNING
                    assert mock_logger.setLevel.call_count >= 3
    
    @pytest.mark.unit
    def test_initialize_components(self, app_manager, mock_driver):
        """Test component initialization."""
        app_manager.initialize_components(mock_driver)
        
        assert app_manager.job_scraper is not None
        assert app_manager.url_manager is not None
        assert app_manager.results_manager is not None
    
    @pytest.mark.unit
    def test_initialize_components_creates_instances(self, app_manager, mock_driver):
        """Test that initialize_components creates proper instances."""
        with patch('src.app_manager.JobScraper') as mock_job_scraper:
            with patch('src.app_manager.URLManager') as mock_url_manager:
                with patch('src.app_manager.ResultsManager') as mock_results_manager:
                    app_manager.initialize_components(mock_driver)
                    
                    # Verify instances were created with correct parameters
                    mock_job_scraper.assert_called_once_with(mock_driver)
                    mock_url_manager.assert_called_once_with(mock_driver)
                    mock_results_manager.assert_called_once()
    
    @pytest.mark.unit
    def test_save_results_with_jobs(self, app_manager):
        """Test saving results when jobs are found."""
        found_jobs = ["https://example.com/job1", "https://example.com/job2"]
        
        # Mock results manager
        mock_results_manager = Mock()
        mock_results_manager.save_results.side_effect = ["jobs.json", "jobs.txt"]
        app_manager.results_manager = mock_results_manager
        
        app_manager._save_results(found_jobs)
        
        # Verify results were saved in both formats
        assert mock_results_manager.save_results.call_count == 2
        mock_results_manager.save_results.assert_any_call("json")
        mock_results_manager.save_results.assert_any_call("txt")
    
    @pytest.mark.unit
    def test_save_results_no_jobs(self, app_manager):
        """Test saving results when no jobs are found."""
        found_jobs = []
        
        # Mock results manager
        mock_results_manager = Mock()
        app_manager.results_manager = mock_results_manager
        
        app_manager._save_results(found_jobs)
        
        # Should not call save_results when no jobs
        mock_results_manager.save_results.assert_not_called()
    
    @pytest.mark.unit
    def test_save_results_none_jobs(self, app_manager):
        """Test saving results when jobs is None."""
        found_jobs = None
        
        # Mock results manager
        mock_results_manager = Mock()
        app_manager.results_manager = mock_results_manager
        
        app_manager._save_results(found_jobs)
        
        # Should not call save_results when jobs is None
        mock_results_manager.save_results.assert_not_called()
    
    @pytest.mark.unit
    def test_print_summary(self, app_manager):
        """Test printing summary."""
        # Mock results manager
        mock_results_manager = Mock()
        mock_results_manager.get_results_summary.return_value = {
            "total_jobs": 5,
            "unique_urls": 5,
            "scraped_at": "2025-01-01T12:00:00"
        }
        app_manager.results_manager = mock_results_manager
        
        app_manager._print_summary()
        
        # Verify summary was retrieved and logged
        mock_results_manager.get_results_summary.assert_called_once()
    
    @pytest.mark.integration
    def test_run_scraping_session_success(self, app_manager, mock_driver):
        """Test successful scraping session."""
        # Mock components
        mock_job_scraper = Mock()
        mock_url_manager = Mock()
        mock_results_manager = Mock()
        
        app_manager.job_scraper = mock_job_scraper
        app_manager.url_manager = mock_url_manager
        app_manager.results_manager = mock_results_manager
        
        # Mock URL processing
        mock_url_manager.process_urls.return_value = ["https://example.com/job1", "https://example.com/job2"]
        
        with patch.object(app_manager, '_save_results'):
            with patch.object(app_manager, '_print_summary'):
                app_manager.run_scraping_session()
                
                # Verify URL processing was called
                mock_url_manager.process_urls.assert_called_once()
                # Verify results were added
                mock_results_manager.add_job_urls.assert_called_once()
                # Verify run summary was saved
                mock_results_manager.save_run_summary.assert_called_once()
    
    @pytest.mark.integration
    def test_run_scraping_session_keyboard_interrupt(self, app_manager):
        """Test scraping session with keyboard interrupt."""
        with patch.object(app_manager, '_save_results'):
            with patch.object(app_manager, '_print_summary'):
                with patch.object(app_manager, 'url_manager') as mock_url_manager:
                    mock_url_manager.process_urls.side_effect = KeyboardInterrupt("User interrupt")
                    
                    # Should not raise exception
                    app_manager.run_scraping_session()
    
    @pytest.mark.integration
    def test_run_scraping_session_exception(self, app_manager):
        """Test scraping session with exception."""
        with patch.object(app_manager, '_save_results'):
            with patch.object(app_manager, '_print_summary'):
                with patch.object(app_manager, 'url_manager') as mock_url_manager:
                    mock_url_manager.process_urls.side_effect = Exception("Test exception")
                    
                    # Should raise the exception
                    with pytest.raises(Exception, match="Test exception"):
                        app_manager.run_scraping_session()
    
    @pytest.mark.integration
    def test_run_full_cycle(self, app_manager, mock_webdriver_manager):
        """Test complete application run."""
        with patch('src.app_manager.WebDriverManager', return_value=mock_webdriver_manager):
            with patch.object(app_manager, 'setup_logging'):
                with patch.object(app_manager, 'initialize_components'):
                    with patch.object(app_manager, 'run_scraping_session'):
                        app_manager.run()
                        
                        # Verify setup was called
                        app_manager.setup_logging.assert_called_once()
                        # Verify components were initialized
                        app_manager.initialize_components.assert_called_once()
                        # Verify scraping session was run
                        app_manager.run_scraping_session.assert_called_once()
    
    @pytest.mark.integration
    def test_run_exception(self, app_manager):
        """Test application run with exception."""
        with patch('src.app_manager.WebDriverManager', side_effect=Exception("Driver error")):
            with patch.object(app_manager, 'setup_logging'):
                with patch('src.app_manager.sys.exit') as mock_exit:
                    app_manager.run()
                    
                    # Should exit with error code
                    mock_exit.assert_called_once_with(1)
    
    @pytest.mark.unit
    def test_run_scraping_session_logs_info(self, app_manager):
        """Test that run_scraping_session logs information."""
        with patch.object(app_manager, 'url_manager') as mock_url_manager:
            with patch.object(app_manager, 'results_manager') as mock_results_manager:
                with patch.object(app_manager, '_save_results'):
                    with patch.object(app_manager, '_print_summary'):
                        mock_url_manager.process_urls.return_value = []
                        
                        app_manager.run_scraping_session()
                        
                        # Verify logger was used
                        assert app_manager.logger is not None
    
    @pytest.mark.unit
    def test_run_scraping_session_uses_config(self, app_manager):
        """Test that run_scraping_session uses configuration values."""
        with patch('src.app_manager.TARGET_URLS', ["https://test.com"]):
            with patch('src.app_manager.DEFAULT_KEYWORDS', ["python"]):
                with patch.object(app_manager, 'url_manager') as mock_url_manager:
                    with patch.object(app_manager, 'results_manager'):
                        with patch.object(app_manager, '_save_results'):
                            with patch.object(app_manager, '_print_summary'):
                                mock_url_manager.process_urls.return_value = []
                                
                                app_manager.run_scraping_session()
                                
                                # Verify process_urls was called with config values
                                mock_url_manager.process_urls.assert_called_once()
                                call_args = mock_url_manager.process_urls.call_args
                                assert call_args[0][0] == ["https://test.com"]
    
    @pytest.mark.unit
    def test_initialize_components_sets_attributes(self, app_manager, mock_driver):
        """Test that initialize_components sets all component attributes."""
        with patch('src.app_manager.JobScraper') as mock_job_scraper:
            with patch('src.app_manager.URLManager') as mock_url_manager:
                with patch('src.app_manager.ResultsManager') as mock_results_manager:
                    mock_job_scraper_instance = Mock()
                    mock_url_manager_instance = Mock()
                    mock_results_manager_instance = Mock()
                    
                    mock_job_scraper.return_value = mock_job_scraper_instance
                    mock_url_manager.return_value = mock_url_manager_instance
                    mock_results_manager.return_value = mock_results_manager_instance
                    
                    app_manager.initialize_components(mock_driver)
                    
                    assert app_manager.job_scraper == mock_job_scraper_instance
                    assert app_manager.url_manager == mock_url_manager_instance
                    assert app_manager.results_manager == mock_results_manager_instance
    
    @pytest.mark.unit
    def test_save_results_calls_both_formats(self, app_manager):
        """Test that _save_results calls both JSON and TXT formats."""
        found_jobs = ["https://example.com/job1"]
        
        mock_results_manager = Mock()
        mock_results_manager.save_results.side_effect = ["jobs.json", "jobs.txt"]
        app_manager.results_manager = mock_results_manager
        
        app_manager._save_results(found_jobs)
        
        # Verify both formats were called
        assert mock_results_manager.save_results.call_count == 2
        calls = mock_results_manager.save_results.call_args_list
        assert calls[0][0][0] == "json"
        assert calls[1][0][0] == "txt"
