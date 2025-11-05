"""Simple CLI application that will be called by the Windows service.

This script demonstrates a basic application that can be executed by a service.
It prints a message with timestamp and logs to a file for verification.

Example:
    Run directly from command line:
        $ python hello_app.py
        $ python hello_app.py "Custom message"
"""

import sys
import os
from datetime import datetime


def log_message(message: str, log_file: str = "logs/hello_app.log") -> None:
    """Write a timestamped message to the log file.

    Args:
        message: The message to log.
        log_file: Path to the log file. Defaults to "logs/hello_app.log".
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    # Ensure logs directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Append to log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    # Also print to console (for testing purposes)
    print(log_entry.strip())


def main() -> None:
    """Main entry point for the hello application.
    
    Accepts an optional command-line argument for a custom message.
    If no argument is provided, uses a default "Hello World" message.
    """
    # Get message from command line or use default
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = "Hello World from hello_app!"
    
    # Log the message
    log_message(f"Application executed: {message}")
    
    # Return success
    return 0


if __name__ == "__main__":
    sys.exit(main())

