# Job Scraper Application

A Python-based web scraper built with Selenium that automatically searches for job listings containing specific keywords across multiple URLs and pages.

## Features

- **Keyword-based Job Search**: Scans job titles for specified keywords
- **Multi-URL Support**: Process multiple job sites in one run
- **Pagination Handling**: Automatically navigates through multiple pages
- **Modular Design**: Clean OOP architecture with separate concerns
- **Multiple Output Formats**: Save results as TXT, JSON, or CSV
- **Configurable**: Easy to customize for different job sites
- **Error Handling**: Robust error handling and logging

## Architecture

The application follows a modular design with these main components:

- **WebDriverManager**: Handles browser setup and configuration
- **JobScraper**: Core scraping logic for finding jobs with keywords
- **URLManager**: Manages URL navigation and pagination
- **ResultsManager**: Handles saving and organizing found results
- **Config**: Centralized configuration settings

## Installation

1. **Clone or download the project files**

2. **Run the installation script** (creates virtual environment automatically):
   ```bash
   python install.py
   ```

3. **Activate the virtual environment**:
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   # or simply run:
   activate.bat
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   # or simply run:
   ./activate.sh
   ```

4. **Browser drivers are installed automatically** by webdriver-manager:
   - Chrome (recommended)
   - Firefox
   - Edge

## Quick Start

### Basic Usage

1. **Edit the URLs in `config.py`**:
   ```python
   TARGET_URLS = [
       "https://www.indeed.com/jobs?q=python+developer",
       "https://www.linkedin.com/jobs/search/?keywords=software%20engineer",
       # Add your target job sites here
   ]
   ```

2. **Customize keywords in `config.py`**:
   ```python
   DEFAULT_KEYWORDS = [
       "python",
       "developer", 
       "software engineer",
       "data scientist",
       "machine learning"
   ]
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Advanced Usage

```python
from webdriver_manager import WebDriverManager
from job_scraper import JobScraper
from url_manager import URLManager
from results_manager import ResultsManager

# Custom keywords
keywords = ["python", "django", "flask", "fastapi"]

# Your target URLs
urls = [
    "https://example-job-site.com/search?q=python",
    "https://another-job-site.com/jobs"
]

# Run the scraper
with WebDriverManager() as driver:
    job_scraper = JobScraper(driver)
    url_manager = URLManager(driver)
    results_manager = ResultsManager()
    
    # Process URLs
    found_jobs = url_manager.process_urls(
        urls,
        lambda: job_scraper.find_jobs_with_keywords(keywords)
    )
    
    # Save results
    results_manager.add_job_urls(found_jobs)
    results_manager.save_results("json")
```

## Configuration

Edit `config.py` to customize the application:

### Browser Settings
```python
BROWSER_TYPE = "chrome"  # Options: "chrome", "firefox", "edge"
HEADLESS_MODE = False    # Set to True for background operation
IMPLICIT_WAIT = 10       # Wait time for elements to load
```

### Scraping Settings
```python
MAX_PAGES_PER_URL = 10   # Maximum pages to scrape per URL
PAGE_LOAD_TIMEOUT = 30   # Maximum time to wait for page load
```

### Job Site Selectors
```python
JOB_TITLE_SELECTORS = [
    "h2 a",              # Common job title selectors
    "h3 a",
    ".job-title a",
    ".title a"
]

NEXT_PAGE_SELECTORS = [
    "a[aria-label='Next']",
    ".next-page",
    "a:contains('Next')"
]
```

## Output Formats

The application supports multiple output formats:

- **TXT**: Human-readable text file
- **JSON**: Structured data with metadata
- **CSV**: Spreadsheet-compatible format

## Customization for Different Job Sites

### Adding New Job Sites

1. **Update selectors in `config.py`**:
   ```python
   JOB_TITLE_SELECTORS = [
       "h2 a",                    # General selectors
       "h3 a",
       ".job-title a",           # Indeed
       ".title a",               # LinkedIn
       "[data-testid='job-title'] a"  # Custom selectors
   ]
   ```

2. **Test selectors**:
   - Use browser developer tools to inspect job title elements
   - Add appropriate CSS selectors to the configuration

### Handling Different Pagination

Update `NEXT_PAGE_SELECTORS` in `config.py`:
```python
NEXT_PAGE_SELECTORS = [
    "a[aria-label='Next']",      # General
    ".next-page",                # Custom
    "a:contains('Next')",        # Text-based
    ".pagination .next"         # Pagination-specific
]
```

## Logging

The application provides comprehensive logging:

- **Console Output**: Real-time progress updates
- **Log File**: Detailed logs saved to `job_scraper.log`
- **Configurable Levels**: DEBUG, INFO, WARNING, ERROR

## Error Handling

The application includes robust error handling for:

- Network timeouts
- Element not found errors
- Browser crashes
- Invalid URLs
- Missing selectors

## Best Practices

1. **Respect robots.txt**: Check if the site allows scraping
2. **Rate Limiting**: Add delays between requests if needed
3. **User-Agent**: Consider setting custom user agents
4. **Legal Compliance**: Ensure compliance with website terms of service

## Virtual Environment Management

### Activating the Environment

**Simple activation (recommended):**
```bash
source ./activate.sh
# IMPORTANT: Use 'source' not './activate.sh'
```

**Manual activation (if needed):**
```bash
# Windows Git Bash
source venv/Scripts/activate

# Linux/Mac
source venv/bin/activate
```

**Troubleshooting:**
If activation doesn't work, run the diagnostic script:
```bash
./check_venv.sh
```

### Deactivating the Environment
```bash
deactivate
```

### Reinstalling Dependencies
If you need to reinstall packages:
```bash
# Activate environment first, then:
pip install -r requirements.txt
```

### Removing the Environment
To completely remove the virtual environment:
```bash
# Deactivate first, then delete the folder
rm -rf venv/  # Linux/Mac
rmdir /s venv  # Windows
```

## Troubleshooting

### Common Issues

1. **Virtual Environment Issues**:
   - Make sure to activate the virtual environment before running the application
   - If packages are missing, reactivate the environment and reinstall
   - Run `./check_venv.sh` to diagnose virtual environment issues
   - If activation fails, try: `source venv/Scripts/activate` (Windows Git Bash) or `source venv/bin/activate` (Linux/Mac)

2. **Browser Driver Issues**:
   - The application automatically downloads drivers
   - Ensure you have a stable internet connection

3. **Element Not Found**:
   - Update selectors in `config.py`
   - Check if the website structure has changed

4. **Timeout Errors**:
   - Increase `PAGE_LOAD_TIMEOUT` in `config.py`
   - Check your internet connection

### Debug Mode

Enable debug logging:
```python
LOG_LEVEL = "DEBUG"  # In config.py
```

## Example Output

### JSON Output
```json
{
  "metadata": {
    "total_jobs": 15,
    "scraped_at": "2024-01-15T10:30:00",
    "output_file": "jobs_20240115_103000.json"
  },
  "jobs": [
    {
      "url": "https://example.com/job/123",
      "title": "Senior Python Developer",
      "source_url": "https://example.com/search",
      "found_at": "2024-01-15T10:30:00"
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational and personal use only. Always respect website terms of service and robots.txt files. Use responsibly and ethically.
