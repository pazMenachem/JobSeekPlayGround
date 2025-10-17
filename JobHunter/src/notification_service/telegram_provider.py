"""Telegram notification provider implementation."""

import asyncio
from telegram import Bot
from telegram.error import TelegramError
from src.notification_service.notifier_interface import NotifierInterface
from src.logger import get_logger


class TelegramProvider(NotifierInterface):
    """Telegram notification provider using python-telegram-bot."""
    
    def __init__(self, bot_token: str, chat_id: str) -> None:
        """Initialize the Telegram provider.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
        """
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=self.bot_token)
        self.logger.info("Telegram provider initialized")
    
    def _send_notification(self, message: str) -> None:
        """Send a notification message to Telegram.
        
        Args:
            message: Message text to send
            
        Raises:
            RuntimeError: If sending fails
        """
        try:
            # Run the async function in a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            loop.run_until_complete(self._send_message_async(message))

        finally:
                loop.close()
    
    async def _send_message_async(self, message: str) -> None:
        """Async method to send Telegram message.
        
        Args:
            message: Message text to send
        """
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

