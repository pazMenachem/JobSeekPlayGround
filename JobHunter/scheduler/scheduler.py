"""Windows Task Scheduler management script for JobHunter.

This script manages Windows Task Scheduler tasks based on configuration
in scheduler_config.json. Supports both native Python and Docker execution modes.
"""

import argparse

from .commands import Commands


def run_scheduler() -> None:
    """Main scheduler logic."""
    commands = Commands()

    parser = argparse.ArgumentParser(
        description="JobHunter Windows Task Scheduler Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["create", "delete", "list", "help"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    command = args.command if args.command else "help"
    
    match command:
        case "help":
            commands.show_help()
        case "create":
            commands.handle_create()
        case "delete":
            commands.handle_delete()
        case "list":
            commands.handle_list()
        case _:
            commands.show_help()


def main() -> None:
    """Main entry point."""
    run_scheduler()


if __name__ == "__main__":
    main()
