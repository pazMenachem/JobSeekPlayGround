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

#### Step 3.1: Create JobFilter Package
- [x] Create `src/job_filter/__init__.py`
- [ ] Create `src/job_filter/ollama_client.py` - Ollama API client
- [ ] Create `src/job_filter/relevance_analyzer.py` - Analyze job relevance
- [ ] Create `src/job_filter/prompt_templates.py` - LLM prompt templates
- [ ] Test JobFilter imports

#### Step 3.2: Create MessageFormatter Package
- [x] Create `src/message_formatter/__init__.py`
- [ ] Create `src/message_formatter/formatter.py` - Format job data
- [ ] Create `src/message_formatter/template_engine.py` - Message templates
- [ ] Create `src/message_formatter/sanitizer.py` - Remove sensitive data
- [ ] Test MessageFormatter imports

#### Step 3.3: Create NotificationService Package
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

### Dependencies
- `requests` - HTTP requests
- `selenium` - Browser automation
- `ollama` - Local LLM integration
- `schedule` - Task scheduling

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
    "provider": "ollama",
    "model": "llama2"
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

## Success Criteria
- [ ] All components work independently
- [ ] Data flows correctly between components
- [ ] LLM filtering works with Ollama
- [ ] Notifications sent via Gmail/Telegram
- [ ] CLI interface functional
- [ ] Windows Task Scheduler integration
- [ ] Error handling implemented
- [ ] Logging system working
- [ ] Documentation complete

## Next Steps
1. Create package structure
2. Implement data models
3. Refactor existing components
4. Create new components
5. Integrate and test
