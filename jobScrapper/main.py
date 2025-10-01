"""Main application entry point for the job scraper."""

from src.app_manager import AppManager


def main() -> None:
    """Main application function."""
    app = AppManager()
    app.run()


if __name__ == "__main__":
    main()
