# JobHunter

Automated job search and filtering application that crawls job listings, analyzes them using AI, and sends relevant opportunities directly to you.

## Features

- 🔍 **Automated Job Crawling** - Scrapes job listings from company career pages
- 🤖 **AI-Powered Filtering** - Uses LLM (Gemini) to analyze job relevance based on your criteria
- 📱 **Smart Notifications** - Sends filtered job opportunities via Telegram
- 💾 **Job Storage** - Tracks sent jobs to avoid duplicates
- ⏰ **Scheduled Runs** - Automatically runs at specified times
- 🐳 **Docker Support** - Run in containers for consistent environments
- 🔧 **Highly Configurable** - Customize keywords, job sites, and AI analysis prompts

## Quick Start

Choose your preferred setup method:

### Option 1: Native Python (Recommended for Beginners)

Run JobHunter directly with Python and a virtual environment.

👉 **[See Native Python Setup Guide](SETUP_NATIVE.md)**

**Quick steps:**
1. Install Python 3.13 or higher
2. Create virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Setup `.env` file with API keys
5. Configure `src/config.py` with your job search criteria
6. Run: `python main.py`

### Option 2: Docker

Run JobHunter in a Docker container for consistent, isolated execution.

👉 **[See Docker Setup Guide](SETUP_DOCKER.md)**

**Quick steps:**
1. Install Docker Desktop (Windows/macOS) or Docker Engine (Linux)
2. Build image: `docker build -t jobhunter .`
3. Setup `.env` file with API keys
4. Configure `src/config.py` with your job search criteria
5. Run: `docker run --env-file .env -v "$(pwd)/data:/app/data" -v "$(pwd)/logs:/app/logs" jobhunter`

## Scheduling

### Windows

Use the built-in scheduler script:

```powershell
python scheduler\scheduler.py create
```

👉 See [Native Python Setup](SETUP_NATIVE.md#9-setup-scheduled-tasks) or [Docker Setup](SETUP_DOCKER.md#8-setup-scheduled-tasks) for details.

### Linux

Use native schedulers (cron or systemd):

👉 **[See Linux Scheduler Guide](LINUX_SCHEDULER.md)**

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
LLM_API_KEY=your_gemini_api_key_here
TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_API_CHAT_ID=your_telegram_chat_id
```

👉 See setup guides for detailed instructions on obtaining these values.

### Application Settings

Edit `src/config.py` to customize:

- **Keywords to search for** (lines 14-19)
- **Keywords to exclude** (lines 21-28)
- **Target job sites** (lines 30-34)
- **LLM analysis prompt** (lines 38-80)
- **Job filter level** (line 82)

👉 See setup guides for detailed configuration instructions.

## Project Structure

```
JobHunter/
├── src/                    # Application source code
│   ├── app_manager.py      # Main orchestrator
│   ├── config.py           # Configuration settings
│   ├── job_crawler_service/ # Web scraping
│   ├── llm_service/        # AI analysis
│   ├── notification_service/ # Notifications
│   └── ...
├── scheduler/              # Windows scheduler script
│   ├── scheduler.py        # Main scheduler entry point
│   └── scheduler_config.json
├── data/                   # Job storage (generated)
├── logs/                   # Application logs (generated)
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
└── README.md               # This file
```

## Requirements

- **Python**: 3.13 or higher
- **Docker** (optional): For containerized execution
- **API Keys**:
  - Google Gemini API key (for LLM analysis)
  - Telegram Bot Token and Chat ID (for notifications)

## Documentation

- **[Native Python Setup Guide](SETUP_NATIVE.md)** - Complete setup instructions for Python venv
- **[Docker Setup Guide](SETUP_DOCKER.md)** - Complete setup instructions for Docker
- **[Linux Scheduler Guide](LINUX_SCHEDULER.md)** - Cron and systemd scheduling examples

## How It Works

1. **Crawl Jobs** - Scrapes job listings from configured company career pages
2. **Filter Duplicates** - Removes jobs that have already been sent
3. **AI Analysis** - Uses LLM to analyze each job's relevance based on your criteria
4. **Filter by Relevance** - Keeps only jobs matching your filter level (YES/MAYBE)
5. **Send Notifications** - Sends relevant jobs to your Telegram
6. **Mark as Sent** - Stores sent jobs to prevent duplicates

## Extending JobHunter

### Adding Notification Providers

Implement the provider abstract class. See existing implementations in `src/notification_service/` for reference.

### Adding LLM Providers

Implement the LLM provider abstract class. See existing implementations in `src/llm_service/` for reference.

## Troubleshooting

### Common Issues

- **Environment variables not loading**: Ensure `.env` file is in project root
- **Docker build fails**: Check Docker is running and you have internet connection
- **Scheduled tasks not running**: Verify scheduler configuration and check logs
- **No jobs found**: Check your target URLs and keywords in `src/config.py`

👉 See setup guides for detailed troubleshooting sections.

## License

**MIT License** - Open source and free to use, modify, and distribute.

## Contributing

Contributions are welcome! Here are some guidelines:

### How to Contribute

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the existing code style
3. **Test your changes** to ensure they work correctly
4. **Update documentation** if you've changed functionality
5. **Submit a pull request** with a clear description of your changes

### Contribution Guidelines

- **Code Style**: Follow existing code patterns and use type hints for function parameters
- **Documentation**: Update relevant documentation files when adding features
- **Testing**: Test your changes before submitting
- **Commit Messages**: Write clear, descriptive commit messages
- **Pull Requests**: Provide a clear description of what was changed and why

### Getting Help

If you have questions or need help, feel free to open an issue for discussion.

---

**Need help?** Check the detailed setup guides or open an issue.

