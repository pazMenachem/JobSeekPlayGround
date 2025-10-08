#!/usr/bin/env python3
"""Main entry point for the Notifier application."""

import sys
from dotenv import load_dotenv

load_dotenv()

from src.services.notification_service import NotificationService
from src.config import settings

DEFAULT_PROVIDER = "email"
TEST_MESSAGE = "Hello! This is a test notification from the Notifier app."

def main():
    """Main function."""
    try:
        provider_settings = settings.get_email_config()

        email_notifier = NotificationService(
            provider_type='email', 
            provider_config=provider_settings.to_dict()
        )

        print("Email message sent successfully!")
        email_notifier.send_message(TEST_MESSAGE)
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


