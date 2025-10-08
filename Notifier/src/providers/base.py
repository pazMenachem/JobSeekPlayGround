"""Abstract base class for notification providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseNotificationProvider(ABC):
    """Abstract base class for all notification providers.
    
    This class defines the interface that all notification providers must implement.
    It provides a common structure for sending job notifications via different channels.
    """
        
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the notification provider.
        
        Args:
            config: Configuration dictionary containing provider-specific settings
        """
        self.config = config
    
    def send_notification(self, *, message: str) -> None:
        """Send a notification message.
        
        Args:
            message: The message string to send
            
        Raises:
            Exception: If notification fails
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        self._send_notification(message)
    
    @abstractmethod
    def _send_notification(self, message: str) -> None:
        """Send a notification message (concrete implementation).
        
        Args:
            message: The message string to send
            
        Raises:
            Exception: If notification fails
        """
        pass
    
    def get_provider_name(self) -> str:
        """Get the name of this provider.
        
        Returns:
            str: Provider name
        """
        return self.__class__.__name__.replace('Provider', '').lower()
    