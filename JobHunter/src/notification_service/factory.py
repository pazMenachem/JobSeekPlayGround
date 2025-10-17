"""Factory for creating notification providers."""

from src.notification_service.notifier_interface import NotifierInterface
from src.notification_service.telegram_provider import TelegramProvider
from src.notification_service.gmail_provider import GmailProvider
from src.config import telegram_settings, gmail_settings

class NotifierFactory:
    """Factory class for creating notifier providers based on configuration."""
    
    @staticmethod
    def create_provider(provider_type: str) -> NotifierInterface:
        """
        Create and return the appropriate notifier provider based on configuration.
        """
        match provider_type.lower():
            case "gmail":
                return NotifierFactory._create_gmail_provider()
            case "telegram":
                return NotifierFactory._create_telegram_provider()
            case _:
                raise ValueError(f"Unsupported notifier provider: {provider_type}")
    
    @staticmethod
    def _create_telegram_provider() -> TelegramProvider:
        """Create a Telegram provider instance."""
        if telegram_settings.enabled:
            return TelegramProvider(
                bot_token=telegram_settings.bot_token,
                chat_id=telegram_settings.chat_id
                )
        raise ValueError("Telegram notifications are not enabled")
    @staticmethod
    def _create_gmail_provider() -> GmailProvider:
        """Create a Gmail provider instance."""
        if gmail_settings.enabled:
            return GmailProvider(
                email=gmail_settings.email,
                password=gmail_settings.password
                )
        raise ValueError("Gmail notifications are not enabled")