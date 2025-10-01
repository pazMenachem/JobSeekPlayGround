"""Pytest configuration and fixtures for job scraper tests."""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Generator
from unittest.mock import Mock

import pytest
from selenium import webdriver

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_driver():
    """Create a mock WebDriver for testing."""
    driver = Mock(spec=webdriver.Chrome)
    driver.current_url = "https://example.com/jobs"
    driver.execute_script = Mock()
    driver.find_elements = Mock()
    driver.find_element = Mock()
    driver.back = Mock()
    driver.forward = Mock()
    driver.refresh = Mock()
    driver.get = Mock()
    driver.quit = Mock()
    return driver


@pytest.fixture
def sample_keywords():
    """Sample keywords for testing."""
    return ["python", "developer", "engineer"]


@pytest.fixture
def sample_urls():
    """Sample URLs for testing."""
    return [
        "https://example.com/jobs",
        "https://test.com/careers",
        "https://demo.com/positions"
    ]


@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return [
        {
            "url": "https://example.com/job1",
            "title": "Python Developer",
            "timestamp": "2025-01-01T10:00:00"
        },
        {
            "url": "https://example.com/job2", 
            "title": "Software Engineer",
            "timestamp": "2025-01-01T10:01:00"
        },
        {
            "url": "https://example.com/job3",
            "title": "Data Scientist", 
            "timestamp": "2025-01-01T10:02:00"
        }
    ]