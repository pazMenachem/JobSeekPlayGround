"""Main notification service for sending messages."""

from typing import Dict, Any
from ..providers.factory import NotificationProviderFactory


class NotificationService:
    """Main service for sending notifications.
    
    This service handles sending string messages via configured notification providers.
    It's a simple message sender that takes a string and sends it using the specified provider.
    """
    
    def __init__(self, *, provider_type: str, provider_config: Dict[str, Any]) -> None:
        """Initialize the notification service.
        
        Args:
            provider_type: Type of provider to use ('telegram', 'email', etc.)
            provider_config: Configuration for the provider
        """
        self.provider = NotificationProviderFactory.create_provider(provider_type=provider_type, config=provider_config)
    
    def send_message(self, message: str) -> None:
        """Send a message via the configured provider.
        
        Args:
            message: The message string to send
            
        Raises:
            Exception: If sending fails
        """
        self.provider.send_notification(message=message)
    
    def get_provider_name(self) -> str:
        """Get the name of the current provider.
        
        Returns:
            str: Provider name
        """
        return self.provider.get_provider_name()
