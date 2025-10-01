# Job Scraper Test Suite

This directory contains comprehensive tests for the job scraper application.

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── fixtures/                # Test data and HTML files
│   └── test_job_page.html   # Sample HTML page for testing
├── test_config.py           # Configuration tests
├── test_job_scraper.py      # JobScraper class tests
├── test_webdriver_manager.py # WebDriverManager tests
├── test_url_manager.py      # URLManager tests
├── test_results_manager.py  # ResultsManager tests
├── test_app_manager.py      # AppManager tests
├── test_integration.py      # Integration tests
├── run_tests.py            # Test runner script
└── README.md               # This file
```

## Test Types

### Unit Tests
- **Configuration Tests** (`test_config.py`): Test configuration settings and validation
- **JobScraper Tests** (`test_job_scraper.py`): Test job finding and keyword matching
- **WebDriverManager Tests** (`test_webdriver_manager.py`): Test browser management
- **URLManager Tests** (`test_url_manager.py`): Test URL navigation and pagination
- **ResultsManager Tests** (`test_results_manager.py`): Test result saving and loading
- **AppManager Tests** (`test_app_manager.py`): Test application lifecycle

### Integration Tests
- **End-to-End Tests** (`test_integration.py`): Test complete workflows
- **HTML Testing**: Tests with real HTML files using WebDriver
- **Error Handling**: Test error scenarios and recovery
- **File Operations**: Test file I/O operations

## Running Tests

### Prerequisites
Make sure you have the virtual environment activated and dependencies installed:

```bash
# Activate virtual environment
source scripts/activate.sh

# Install dependencies (including test dependencies)
pip install -r requirements.txt
```

### Running All Tests
```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Running Specific Test Types
```bash
# Run only unit tests
python -m pytest tests/ -m unit

# Run only integration tests
python -m pytest tests/ -m integration

# Run only WebDriver tests (requires browser)
python -m pytest tests/ -m webdriver

# Run specific test file
python -m pytest tests/test_job_scraper.py
```

### Using the Test Runner Script
```bash
# Run all tests
python tests/run_tests.py

# Run unit tests only
python tests/run_tests.py --type unit

# Run integration tests only
python tests/run_tests.py --type integration

# Run quietly
python tests/run_tests.py --quiet
```

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit`: Unit tests (fast, no external dependencies)
- `@pytest.mark.integration`: Integration tests (may use external resources)
- `@pytest.mark.webdriver`: Tests requiring WebDriver (need browser)
- `@pytest.mark.slow`: Slow-running tests

## Test Fixtures

### Common Fixtures
- `mock_driver`: Mock WebDriver for testing
- `temp_dir`: Temporary directory for test files
- `sample_keywords`: Sample keywords for testing
- `sample_urls`: Sample URLs for testing
- `sample_job_data`: Sample job data for testing

### HTML Testing
- `test_html_file`: Path to test HTML file
- `chrome_options`: Chrome options for headless testing

## Test Data

### HTML Test Page (`fixtures/test_job_page.html`)
Contains sample job listings with:
- Multiple job titles with various keywords
- Pagination elements
- Different CSS selectors for testing
- Realistic job board structure

### Sample Data
- **Keywords**: `["python", "developer", "engineer"]`
- **URLs**: Various job board URLs
- **Job Data**: Structured job information with URLs, titles, and metadata

## Coverage

The test suite aims for comprehensive coverage of:
- ✅ Configuration validation
- ✅ Job finding and keyword matching
- ✅ WebDriver management
- ✅ URL navigation and pagination
- ✅ Result saving and loading
- ✅ Application lifecycle
- ✅ Error handling
- ✅ File operations
- ✅ Integration workflows

## Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes
markers =
    unit: Unit tests
    integration: Integration tests
    webdriver: Tests that require WebDriver
    slow: Slow running tests
```

## Continuous Integration

The test suite is designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    python -m pytest tests/ --cov=src --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Troubleshooting

### Common Issues

1. **WebDriver not found**: Install Chrome/Firefox and ensure drivers are available
2. **Import errors**: Make sure virtual environment is activated
3. **Permission errors**: Ensure test directories are writable
4. **Timeout errors**: Increase timeout values for slow tests

### Debug Mode
```bash
# Run tests with debug output
python -m pytest tests/ -v -s --tb=long

# Run specific test with debug
python -m pytest tests/test_job_scraper.py::TestJobScraper::test_find_jobs_with_keywords_success -v -s
```

## Adding New Tests

### Unit Test Template
```python
@pytest.mark.unit
def test_function_name(self, fixture_name):
    """Test description."""
    # Arrange
    # Act
    # Assert
    assert result == expected
```

### Integration Test Template
```python
@pytest.mark.integration
def test_workflow_name(self, mock_driver, sample_data):
    """Test complete workflow."""
    # Setup
    # Execute
    # Verify
    assert workflow_result == expected
```

## Best Practices

1. **Use fixtures** for common test data
2. **Mock external dependencies** in unit tests
3. **Test error conditions** and edge cases
4. **Use descriptive test names** and docstrings
5. **Keep tests independent** and isolated
6. **Use appropriate markers** for test categorization
7. **Test both success and failure scenarios**
