"""Notification service for managing different notification providers."""

from typing import List
from src.notification_service.notifier_interface import NotifierInterface
from src.notification_service.factory import NotifierFactory
from src.logger import get_logger
from src.exceptions.exceptions import NotifierException


class NotifierService:
    """Service for managing notification providers and sending messages."""
    
    def __init__(self) -> None:
        """Initialize the notifier service."""
        self.logger = get_logger("notifier_service")
        self.providers: List[NotifierInterface] = []
        self.logger.info("Notifier service initialized...")
    
    def set_providers(self, *args: List[str]) -> None:
        """Set the notification providers.
        
        Args:
            *args: The names of the providers to set
        """
        for provider_name in args:
            self.providers.append(
                NotifierFactory.create_provider(provider_name)
                )
            self.logger.info(f"Notification provider {provider_name} added")
    
    def send_notification(self, message: str) -> None:
        """Send notification to all available providers.
        
        Args:
            message: Message to send
        """
        if not self.providers:
            raise RuntimeError("No notification providers available")

        try:
            for provider in self.providers:
                provider.send_notification(message=message)
        except Exception as e:
            self.logger.error(f"Error sending notification: {e}")
            raise NotifierException()

