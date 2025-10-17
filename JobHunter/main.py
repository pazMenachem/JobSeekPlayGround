"""Main application entry point for JobHunter."""

from src.app_manager import JobHunterOrchestrator

def main() -> None:
    """Main application function."""
    JobHunterOrchestrator().run()

if __name__ == "__main__":
    main()
