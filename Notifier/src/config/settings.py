"""Configuration settings for the Notifier application."""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TelegramConfig:
    """Telegram provider configuration."""
    bot_token: str
    chat_id: str
    
    @classmethod
    def from_env(cls) -> 'TelegramConfig':
        """Load Telegram configuration from environment variables."""
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        if not chat_id:
            raise ValueError("TELEGRAM_CHAT_ID environment variable is required")

        return cls(
            bot_token=bot_token, 
            chat_id=chat_id
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for provider initialization."""
        return {
            'bot_token': self.bot_token,
            'chat_id': self.chat_id
        }


@dataclass
class EmailConfig:
    """Email provider configuration."""
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    from_email: str
    to_email: str
    subject: str = "Job Notification"
    
    @classmethod
    def from_env(cls) -> 'EmailConfig':
        """Load Email configuration from environment variables."""
        smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        username = os.getenv('EMAIL_USERNAME')
        password = os.getenv('EMAIL_PASSWORD')
        from_email = os.getenv('EMAIL_FROM')
        to_email = os.getenv('EMAIL_TO')
        subject = os.getenv('EMAIL_SUBJECT', 'Job Notification')
        
        # Validate required fields
        if not username:
            raise ValueError("EMAIL_USERNAME environment variable is required")
        if not password:
            raise ValueError("EMAIL_PASSWORD environment variable is required")
        if not from_email:
            raise ValueError("EMAIL_FROM environment variable is required")
        if not to_email:
            raise ValueError("EMAIL_TO environment variable is required")
            
        return cls(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            username=username,
            password=password,
            from_email=from_email,
            to_email=to_email,
            subject=subject
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for provider initialization."""
        return {
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'username': self.username,
            'password': self.password,
            'from_email': self.from_email,
            'to_email': self.to_email,
            'subject': self.subject
        }


class Settings:
    """Main settings class for the Notifier application."""
    
    def __init__(self):
        """Initialize settings from environment variables."""
        self._telegram_config: Optional[TelegramConfig] = None
        self._email_config: Optional[EmailConfig] = None
    
    def get_telegram_config(self) -> TelegramConfig:
        """Get Telegram configuration."""
        if self._telegram_config is None:
            self._telegram_config = TelegramConfig.from_env()
        return self._telegram_config
    
    def get_email_config(self) -> EmailConfig:
        """Get Email configuration."""
        if self._email_config is None:
            self._email_config = EmailConfig.from_env()
        return self._email_config

settings = Settings()
