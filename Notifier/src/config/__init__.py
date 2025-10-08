"""Configuration package for the Notifier application."""

from .settings import Settings, TelegramConfig, EmailConfig, settings

__all__ = ['Settings', 'TelegramConfig', 'EmailConfig', 'settings']
