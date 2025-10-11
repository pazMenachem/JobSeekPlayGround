"""Main application entry point for JobHunter."""

from src.app_manager.orchestrator import JobHunterOrchestrator


def main() -> None:
    """Main application function."""
    orchestrator = JobHunterOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()
