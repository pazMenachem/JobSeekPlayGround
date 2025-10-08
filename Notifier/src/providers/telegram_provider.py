"""Telegram notification provider implementation."""

from telegram import Bot
from telegram.error import TelegramError
from .base import BaseNotificationProvider


class TelegramProvider(BaseNotificationProvider):
    """Telegram notification provider using Telegram Bot API."""
    
    def _send_notification(self, message: str) -> None:
        """Send notification message via Telegram.
        
        Args:
            message: The message string to send
        
        Raises:
            Exception: If notification fails
        """
        try:
            bot_token = self.config['bot_token']
            chat_id = self.config['chat_id']

            bot = Bot(token=bot_token)
            
            bot.send_message(
                chat_id=chat_id,
                text=message
            )
            
        except TelegramError as e:
            raise Exception(f"Telegram API error: {e}")
        except Exception as e:
            raise Exception(f"Failed to send Telegram notification: {e}")
    
