# JobHunter - Project Planning Document

## Project Overview
JobHunter is a CLI application that automates job searching by scraping job listings from specified URLs, filtering them using LLM, and sending notifications via Gmail/Telegram.

## Architecture Design

### Core Components
```
JobHunter/
├── src/
│   ├── data_models/           # Data classes for type safety
│   ├── job_crawler/           # Job scraping (existing)
│   ├── job_filter/            # LLM filtering (new)
│   ├── job_storage/           # Data persistence (existing)
│   ├── message_formatter/     # Content formatting (new)
│   ├── notification_service/  # Communication (new)
│   ├── logger/                # Logging (new)
│   └── app_manager/          # Orchestrator (existing)
├── data/                      # JSON storage
├── models/                    # Local LLM models
├── main.py                    # CLI entry point
└── requirements.txt
```

### Data Flow
```
1. SearchRequest → JobCrawler → List[JobData]
2. List[JobData] → JobFilter → FilteredJobs
3. FilteredJobs → MessageFormatter → MessageData
4. MessageData → NotificationService → Send notifications
```

## Data Models

### JobData
```python
@dataclass
class JobData:
    id: str
    title: str
    company: str
    url: str
    found_date: datetime = None
    source_url: str = ""
    
    def __post_init__(self):
        if self.found_date is None:
            self.found_date = datetime.now()
```

### SearchRequest
```python
@dataclass
class SearchRequest:
    urls: List[str]
    keywords: List[str]
    max_pages: int = 5
    delay_seconds: float = 1.0
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

### FilteredJobs
```python
@dataclass
class FilteredJobs:
    relevant_jobs: List[JobData]
    total_found: int
    filtered_count: int
    filter_timestamp: datetime = None
    
    def __post_init__(self):
        if self.filter_timestamp is None:
            self.filter_timestamp = datetime.now()
```

### MessageData
```python
@dataclass
class MessageData:
    subject: str
    content: str
    job_count: int
    channels: List[str]  # ['gmail', 'telegram']
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

## Component Analysis

### ✅ Existing Components (Ready)
1. **JobCrawler** - Job scraping functionality
   - `job_scraper.py` - Core scraping logic
   - `browser_manager.py` - WebDriver management
   - `url_manager.py` - URL navigation and pagination
   - `results_manager.py` - Data storage and results management

2. **AppManager** - Application orchestration
   - `app_manager.py` - Main application flow
   - `config.py` - Configuration management

### 🔄 Components to Refactor
1. **ConfigManager** - Extract from existing config.py
2. **JobStorage** - Refactor from results_manager.py
3. **Logger** - Extract logging logic from app_manager.py

### 🆕 New Components to Create
1. **JobFilter** - LLM filtering with Ollama
2. **MessageFormatter** - Content formatting
3. **NotificationService** - Gmail/Telegram integration

## Implementation Steps - Detailed Micro-Steps

### Phase 1: Project Structure Setup

#### Step 1.1: Create Package Folders
- [x] Create `src/data_models/` folder
- [x] Create `src/job_crawler/` folder  
- [x] Create `src/job_filter/` folder
- [x] Create `src/job_storage/` folder
- [x] Create `src/message_formatter/` folder
- [x] Create `src/notification_service/` folder
- [x] Create `src/logger/` folder
- [x] Create `src/app_manager/` folder
- [x] Create `data/` folder
- [x] Create `models/` folder

#### Step 1.2: Create __init__.py Files
- [x] Create `src/data_models/__init__.py`
- [x] Create `src/job_crawler/__init__.py`
- [x] Create `src/job_filter/__init__.py`
- [x] Create `src/job_storage/__init__.py`
- [x] Create `src/message_formatter/__init__.py`
- [x] Create `src/notification_service/__init__.py`
- [x] Create `src/logger/__init__.py`
- [x] Create `src/app_manager/__init__.py`

#### Step 1.3: Create Data Model Files
- [x] Create `src/data_models/job_data.py` - JobData class
- [x] Create `src/data_models/search_request.py` - SearchRequest class
- [x] Create `src/data_models/filtered_jobs.py` - FilteredJobs class
- [x] Create `src/data_models/message_data.py` - MessageData class
- [x] Update `src/data_models/__init__.py` - Export all classes

#### Step 1.4: Test Basic Structure
- [x] Test import: `from src.data_models import JobData`
- [x] Test import: `from src.data_models import SearchRequest`
- [x] Test import: `from src.data_models import FilteredJobs`
- [x] Test import: `from src.data_models import MessageData`

### Phase 2: Refactor Existing Components

#### Step 2.1: Extract ConfigManager
- [x] Create `src/config_manager/__init__.py`
- [x] Create `src/config_manager/config_manager.py` - Config management
- [x] Create `src/config_manager/config.py` - Configuration settings
- [x] Move config logic from `JobCrawler/src/config.py`
- [x] Test ConfigManager imports

#### Step 2.2: Refactor JobStorage
- [x] Create `src/job_storage/__init__.py`
- [x] Create `src/job_storage/job_storage_manager.py` - Storage management
- [x] Create `src/job_storage/results_manager.py` - Results handling
- [x] Move logic from `JobCrawler/src/results_manager.py`
- [x] Test JobStorage imports

#### Step 2.3: Extract Logger
- [x] Create `src/logger/__init__.py`
- [x] Create `src/logger/log_manager.py` - Main logging logic
- [x] Extract logging from `JobCrawler/src/app_manager.py`
- [x] Test Logger imports

#### Step 2.4: Update AppManager
- [x] Create `src/app_manager/__init__.py`
- [x] Create `src/app_manager/orchestrator.py` - Main orchestration
- [x] Create `src/app_manager/app_manager.py` - Legacy manager
- [x] Move logic from `JobCrawler/src/app_manager.py`
- [x] Test AppManager imports

### Phase 3: Create New Components

#### Step 3.1: Create LLM Communication Package with Gemini Flash ✅ COMPLETED
- [x] Create `src/llm_communication/__init__.py`
- [x] Create `src/llm_communication/llm_interface.py` - Abstract LLM interface
- [x] Create `src/llm_communication/gemini_provider.py` - Gemini Flash API client
  - [x] Implement `is_available()` - Check API connectivity
  - [x] Implement `send_to_llm()` - Async API call with executor
- [x] Create `src/llm_communication/llm_communicator.py` - LLM communication manager
  - [x] Implement `update_job_status()` - Batch job analysis
  - [x] Implement `_parse_batch_response()` - JSON response parsing
- [x] Create `src/llm_communication/prompt_formatter.py` - Batch prompt formatting
- [x] Implement structured JSON output schema:
  ```json
  {
    "jobs": [
      {"index": 0, "relevant": "yes", "reason": "matches criteria"},
      {"index": 1, "relevant": "no", "reason": "not related"}
    ]
  }
  ```
- [x] Update JobData model with `relevant` and `reason` attributes
- [x] Test LLM communication with Gemini API
- [x] Add error handling for batch failures

#### Step 3.2: Create Job Filter Package ✅ COMPLETED
- [x] Create `src/message_formatter/job_filter.py` - Job filtering logic
  - [x] Implement `filter_jobs()` - Filter based on relevance status
  - [x] Implement `_should_include_job()` - Filter level logic (yes/maybe/no/all)
- [x] Update FilteredJobs data model
- [x] Test JobFilter with different filter levels

#### Step 3.3: Create MessageFormatter Package
- [x] Create `src/message_formatter/__init__.py`
- [ ] Create `src/message_formatter/formatter.py` - Format job data
- [ ] Create `src/message_formatter/template_engine.py` - Message templates
- [ ] Create `src/message_formatter/sanitizer.py` - Remove sensitive data
- [ ] Test MessageFormatter imports

#### Step 3.4: Create NotificationService Package
- [x] Create `src/notification_service/__init__.py`
- [ ] Create `src/notification_service/gmail_sender.py` - Gmail integration
- [ ] Create `src/notification_service/telegram_sender.py` - Telegram integration
- [ ] Create `src/notification_service/message_router.py` - Route messages
- [ ] Test NotificationService imports

### Phase 4: Integration & Testing

#### Step 4.1: Update Imports
- [ ] Update all import statements in existing files
- [ ] Fix import paths for new package structure
- [ ] Test all imports work correctly

#### Step 4.2: Integrate Data Flow
- [ ] Connect JobCrawler → JobStorage
- [ ] Connect JobStorage → JobFilter
- [ ] Connect JobFilter → MessageFormatter
- [ ] Connect MessageFormatter → NotificationService

#### Step 4.3: Test Components
- [ ] Test JobCrawler independently
- [ ] Test JobFilter independently
- [ ] Test MessageFormatter independently
- [ ] Test NotificationService independently

#### Step 4.4: Test Full Workflow
- [ ] Test complete data flow
- [ ] Test error handling
- [ ] Test logging system
- [ ] Test configuration loading

### Phase 5: CLI & Scheduling

#### Step 5.1: Create CLI Interface
- [ ] Update `main.py` with CLI commands
- [ ] Add command-line arguments
- [ ] Test CLI functionality

#### Step 5.2: Windows Task Scheduler
- [ ] Create batch file for running
- [ ] Set up Windows Task Scheduler
- [ ] Test automated runs

#### Step 5.3: Final Testing
- [ ] End-to-end testing
- [ ] Error scenario testing
- [ ] Performance testing
- [ ] Documentation updates

## Technical Specifications

### Gemini Flash API Integration

#### Batch Processing Strategy
Instead of making one API request per job (100 jobs = 100 requests), we use **batch processing**:
- **Single Request**: All jobs analyzed in one API call
- **Structured Output**: JSON format for reliable parsing
- **Rate Limit Solution**: 1 request instead of 100 (no 15 RPM limit issue)
- **Token Efficiency**: ~30,000 tokens for 100 jobs (well within free tier)

#### Request Format
```python
prompt = f"""
Analyze the following {len(jobs)} jobs for relevance to a software developer position.
Return a JSON object with this exact structure:
{{
  "jobs": [
    {{"index": 0, "relevant": "yes/no/maybe", "reason": "brief explanation"}},
    ...
  ]
}}

Jobs to analyze:
{job_list_formatted}
"""
```

#### Response Parsing
- Parse JSON response
- Map each result to corresponding JobData object by index
- Apply filter level logic (yes/maybe/no/all)
- Handle parsing errors with fallback to individual analysis

### Dependencies
- `requests` - HTTP requests
- `selenium` - Browser automation
- `google-generativeai` - Gemini API integration (FREE tier)
- `schedule` - Task scheduling (future)

### Logging Format
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [MODULE] [MESSAGE]
```

### Error Handling
- **Non-Critical**: Continue + notify (invalid URL, scrape failure)
- **Critical**: Stop + notify (config corruption, storage failure)

### Rate Limiting
- 1 second delay between requests
- Respectful scraping practices

## Configuration Structure
```json
{
  "urls": ["https://example.com/jobs"],
  "keywords": ["python", "developer"],
  "llm": {
    "provider": "gemini",
    "model": "gemini-2.5-flash",
    "api_key": "env:GEMINI_API_KEY",
    "batch_processing": true,
    "output_format": "json"
  },
  "notifications": {
    "gmail": {
      "enabled": true,
      "to": "your-email@gmail.com"
    },
    "telegram": {
      "enabled": true,
      "bot_token": "env:TELEGRAM_BOT_TOKEN",
      "chat_id": "env:TELEGRAM_CHAT_ID"
    }
  }
}
```

## Current System Status

### ✅ COMPLETED & WORKING
1. Complete job scraping pipeline with Playwright
2. Gemini AI job analysis (batch processing up to 20 jobs)
3. Telegram notifications (fully functional)
4. Job filtering by relevance (RelevanceStatus enum)
5. Logging system (console + timestamped files)
6. Configuration management (settings classes + env vars)
7. Error handling (custom exception hierarchy)
8. Message formatting (LLM prompts + notification summaries)
9. All core data models (JobData, FilteredJobs, RelevanceStatus, etc.)
10. Factory patterns for LLM and Notifier providers
11. Main orchestration workflow (JobHunterOrchestrator)

### 🔴 MVP ISSUES TO RESOLVE

#### 1. Job Storage System
**Current State:** Code exists but not integrated, doesn't store LLM analysis results

**Requirements to Define:**
- What data to persist? (URL, LLM analysis, timestamps, notification status)
- Storage format? (SQLite, JSON, CSV)
- Duplicate detection strategy? (by URL, by company+title, time-based expiry)
- Primary use case? (avoid re-sending, analytics, resume interrupted runs)

**Files Affected:**
- `src/job_storage/job_storage_manager.py`
- `src/job_storage/results_manager.py`
- `src/app_manager.py` (integration)

#### 2. Duplicate Job Detection
**Current State:** Not implemented

**Requirements:**
- Track previously seen/sent jobs
- Depends on Job Storage implementation
- Define deduplication logic (URL-based, title+company-based, or both)

**Files Affected:**
- `src/job_storage/` (storage layer)
- `src/app_manager.py` (filtering duplicates before analysis)

#### 3. Handling >20 Jobs with LLM
**Current State:** Only first 20 jobs analyzed (line 96 in app_manager.py: `prompt = MessageFormatterService.format_llm_prompt(self.jobs[:20])`)

**Gemini Limitation:** URL context tool limited to 20 URLs per request

**Solutions:**
- Option A: Batch into multiple requests of 20 jobs each
- Option B: Analyze without URL context (just title/company)
- Option C: Hybrid approach (first 20 with context, rest without)

**Files Affected:**
- `src/app_manager.py` (batching logic)
- `src/llm_service/llm_service.py` (batch processing)
- `src/message_formatter.py` (prompt formatting)

#### 4. Telegram Message Length Validation
**Current State:** No validation, Telegram has 4096 character limit

**Requirements:**
- Detect when summary exceeds limit
- Split into multiple messages or truncate
- Maintain readability

**Files Affected:**
- `src/message_formatter.py` (length checking)
- `src/notification_service/telegram_provider.py` (message splitting)

#### 5. Error Message Formatting for Notifications
**Current State:** Line 110 in app_manager.py sends raw exception string: `self.notifier_service.send_notification(message=str(e))`

**Requirements:**
- User-friendly error messages
- Include context (which phase failed, what to check)
- Proper formatting for Telegram

**Files Affected:**
- `src/exceptions/exceptions.py` (better error messages)
- `src/app_manager.py` (error formatting)
- `src/message_formatter.py` (error message templates)

### 📋 POST-MVP FEATURES
1. CLI Argument Parsing (argparse/click for runtime configuration)
2. Windows Task Scheduler Integration (automated runs)
3. Containerization (Docker for cross-platform deployment)

## Implementation Priority List

### Phase 1: Core Fixes (MVP Completion)
1. **Job Storage System Redesign** - Define requirements and implement
2. **Duplicate Job Detection** - Integrate with storage
3. **Handle >20 Jobs with LLM** - Implement batching strategy
4. **Telegram Message Length Validation** - Add splitting/truncation
5. **Error Message Formatting** - User-friendly notifications

### Phase 2: Post-MVP Enhancements
6. **CLI Argument Parsing** - Runtime configuration
7. **Windows Task Scheduler** - Automated execution
8. **Containerization** - Docker setup for portability
