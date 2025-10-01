# Job Scraper Application

A Python-based web scraper built with Selenium that automatically searches for job listings containing specific keywords across multiple URLs and pages.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python scripts/install.py
```

### 2. Activate Virtual Environment
```bash
source scripts/activate.sh
# IMPORTANT: Use 'source' not './scripts/activate.sh'
```

### 3. Configure Settings
Edit `src/config.py` to customize:
- URLs to scrape (`TARGET_URLS`)
- Keywords to search (`DEFAULT_KEYWORDS`)
- Browser settings, timeouts, etc.

### 4. Run the Application
```bash
scripts/run_app.sh
# or manually: python main.py
```

## 📁 Project Structure

```
jobScrapper/
├── src/                      # Source code
│   ├── __init__.py
│   ├── app_manager.py        # Application manager
│   ├── config.py             # Configuration settings
│   ├── webdriver_manager.py  # Browser management
│   ├── job_scraper.py        # Core scraping logic
│   ├── url_manager.py        # URL navigation
│   └── results_manager.py    # Results handling
├── scripts/                  # Utility scripts
│   ├── activate.sh          # Virtual environment activation
│   ├── run_app.sh           # Application runner
│   └── install.py           # Installation script
├── docs/                    # Documentation
│   ├── README.md
│   ├── APPLICATION_FLOW.md
│   └── ACTIVATION_INSTRUCTIONS.md
├── main.py                  # Clean entry point
├── requirements.txt         # Dependencies
└── venv/                    # Virtual environment
```

## 🎯 Key Features

- **Clean Architecture**: Organized in `src/` with proper separation of concerns
- **AppManager**: Centralized application logic management
- **Modular Design**: Each component has a specific responsibility
- **Easy Configuration**: All settings in `config.py`
- **Virtual Environment**: Isolated dependencies
- **Multiple Output Formats**: JSON, TXT, CSV

## 🔧 Configuration

Edit `src/config.py`:

```python
# URLs to scrape
TARGET_URLS = [
    "https://www.indeed.com/jobs?q=python+developer",
    "https://www.linkedin.com/jobs/search/?keywords=software%20engineer",
]

# Keywords to search for
DEFAULT_KEYWORDS = [
    "python",
    "developer",
    "software engineer",
    "data scientist",
    "machine learning"
]

# Browser settings
BROWSER_TYPE = "chrome"  # Options: "chrome", "firefox", "edge"
HEADLESS_MODE = False
```

## 📊 Output

### Results
Results are organized in timestamped directories:
```
results/
├── run_YYYYMMDD_HHMMSS/     # Each run gets its own directory
│   ├── jobs_YYYYMMDD_HHMMSS.json    # JSON format
│   ├── jobs_YYYYMMDD_HHMMSS.txt     # Human-readable
│   ├── jobs_YYYYMMDD_HHMMSS.csv     # Spreadsheet-compatible
│   └── run_summary.txt              # Run overview
└── README.md                        # Results documentation
```

### Logs
Logs are organized with timestamped files:
```
logs/
├── job_scraper_YYYYMMDD_HHMMSS.log  # Timestamped log files
└── README.md                        # Logs documentation
```

### File Formats:
- **JSON**: Structured data with metadata
- **TXT**: Human-readable format
- **CSV**: Spreadsheet-compatible format
- **Summary**: Quick overview of each run
- **Logs**: Detailed execution logs for debugging

## 🛠️ Development

### Virtual Environment Management
```bash
# Activate
source scripts/activate.sh

# Deactivate
deactivate

# Run application
scripts/run_app.sh
```

### Project Structure Benefits
- **Clean main.py**: Just imports and runs AppManager
- **Organized source**: All code in `src/`
- **Separated scripts**: Utilities in `scripts/`
- **Documentation**: All docs in `docs/`

## 📚 Documentation

- **Complete Documentation**: `docs/README.md`
- **Application Flow**: `docs/APPLICATION_FLOW.md`
- **Activation Instructions**: `docs/ACTIVATION_INSTRUCTIONS.md`

## ⚠️ Important Notes

- Always use `source scripts/activate.sh` (not `./scripts/activate.sh`)
- Edit configuration in `src/config.py`
- Virtual environment is required for all operations
- Check `docs/` for detailed documentation

## 🎉 Usage Example

```bash
# 1. Install
python scripts/install.py

# 2. Activate
source scripts/activate.sh

# 3. Configure (edit src/config.py)
# 4. Run
scripts/run_app.sh
```

That's it! The application will scrape your configured URLs and save results automatically.