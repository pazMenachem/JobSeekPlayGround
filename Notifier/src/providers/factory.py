"""Factory for creating notification providers."""

from typing import Dict, Any, Type
from .base import BaseNotificationProvider
from .telegram_provider import TelegramProvider
from .email_provider import EmailProvider


class NotificationProviderFactory:
    """Factory class for creating notification providers.
    
    This factory creates the appropriate notification provider based on the
    provider type specified in the configuration.
    """
    
    _providers: Dict[str, Type[BaseNotificationProvider]] = {
        'telegram': TelegramProvider,
        'email': EmailProvider,
    }
    
    @classmethod
    def create_provider(cls, *, provider_type: str, config: Dict[str, Any]) -> BaseNotificationProvider:
        """Create a notification provider instance.
        
        Args:
            provider_type: Type of provider to create ('telegram', 'email', etc.)
            config: Configuration dictionary for the provider
            
        Returns:
            BaseNotificationProvider: Instance of the requested provider
            
        Raises:
            ValueError: If provider_type is not supported
        """
        if provider_type not in cls._providers:
            available_providers = ', '.join(cls._providers.keys())
            raise ValueError(f"Unsupported provider type: {provider_type}. Available: {available_providers}")
        
        provider_class = cls._providers[provider_type]
        return provider_class(config)
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get list of available provider types.
        
        Returns:
            list[str]: List of available provider type names
        """
        return list(cls._providers.keys())
