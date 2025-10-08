# Notifier

A simple Python application for sending notifications via Telegram or Email.

## Features

- **Simple Interface**: Just pass a string message and send it
- **Multiple Providers**: Support for Telegram and Email
- **Easy Configuration**: Environment variable based configuration
- **Flexible**: Can be integrated into any application

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Provider Selection (telegram or email)
NOTIFICATION_PROVIDER=email

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Email Configuration
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@gmail.com
EMAIL_SUBJECT=Job Notification
```

### 3. Run the Application

```bash
python main.py
```

## Email Configuration (Gmail)

### Getting Gmail App Password

Gmail requires **App Passwords** for SMTP access, not your regular password:

#### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Turn on **2-Step Verification** (required for App Passwords)

#### Step 2: Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **"Mail"** as the app
3. Copy the generated password (looks like: `abcd efgh ijkl mnop`)

#### Step 3: Use in .env file
```env
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop  # App password, not regular password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@gmail.com
```

### Why App Passwords?

- **Security**: Prevents apps from accessing your main Gmail account
- **Control**: You can revoke app passwords without changing your main password
- **Audit**: Google can track which apps are accessing your email

### Alternative Email Providers

If you don't want to set up App Passwords, you can use:

- **Outlook/Hotmail**: Usually works with regular password
- **Yahoo**: Requires App Password (similar to Gmail)
- **Company email**: Often works with regular credentials

## Telegram Configuration

### Getting Telegram Bot Token

1. **Create a Bot**:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` command
   - Follow the instructions to create your bot
   - Copy the bot token

2. **Get Chat ID**:
   - Add your bot to a chat or message it directly
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Use in .env file**:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

## Usage in Your Code

### Simple Usage

```python
from src.services.notification_service import NotificationService
from src.config import settings

# Get configuration
email_config = settings.get_email_config()
telegram_config = settings.get_telegram_config()

# Create services
email_service = NotificationService(
    provider_type='email', 
    provider_config=email_config.to_dict()
)

telegram_service = NotificationService(
    provider_type='telegram', 
    provider_config=telegram_config.to_dict()
)

# Send messages
email_service.send_message("Hello from email!")
telegram_service.send_message("Hello from Telegram!")
```

### Direct Configuration

```python
from src.config import TelegramConfig, EmailConfig

# Telegram
telegram_config = TelegramConfig(
    bot_token='your_token',
    chat_id='your_chat_id'
)

# Email
email_config = EmailConfig(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    username='your_email@gmail.com',
    password='your_app_password',
    from_email='your_email@gmail.com',
    to_email='recipient@gmail.com'
)

# Use with services
service = NotificationService('email', email_config.to_dict())
service.send_message("Hello!")
```

## Project Structure

```
Notifier/
├── src/
│   ├── config/
│   │   ├── __init__.py          # Config package exports
│   │   └── settings.py          # Settings classes and global settings
│   ├── providers/
│   │   ├── base.py              # Abstract base class
│   │   ├── telegram_provider.py # Telegram implementation
│   │   ├── email_provider.py    # Email implementation
│   │   └── factory.py           # Provider factory
│   └── services/
│       └── notification_service.py # Main service
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

## Requirements

- Python 3.8+
- python-telegram-bot==21.7 (Not have to if provider not used)
- python-dotenv==1.0.1

## Troubleshooting

### Common Issues

1. **"EMAIL_USERNAME environment variable is required"**
   - Make sure your `.env` file exists and has the correct variables
   - Check that `load_dotenv()` is called before importing settings

2. **"SMTP error: Username and Password not accepted"**
   - Use Gmail App Password, not your regular password
   - Make sure 2-factor authentication is enabled
   - Verify the App Password is correct

3. **"Telegram API error: You must pass the token"**
   - Check your bot token is correct
   - Make sure the bot is not blocked
   - Verify the chat ID is correct

4. **"Unsupported provider type"**
   - Use 'telegram' or 'email' as provider type
   - Check spelling and case sensitivity

## License

This project is open source and available under the MIT License.
