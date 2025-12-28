"""Entry point for Ops Deck TUI application."""

import sys
from pathlib import Path

from .exceptions import ConfigError
from .models import AppConfig, Command
from .services import ConfigLoader
from .widgets.app import OpsApp


def main() -> None:
    """Load configuration and run the Ops Deck TUI application.

    Loads configuration from commands.yaml and initializes the app.
    If configuration fails, displays an error screen instead of crashing.
    """
    # Determine config file path
    config_path = Path("commands.yaml")
    config: AppConfig | None = None
    commands: list[Command] = []
    error_title: str | None = None
    error_message: str | None = None
    error_details: str | None = None

    try:
        # Load configuration
        config_loader = ConfigLoader()
        commands, config = config_loader.load_and_validate(str(config_path))

    except ConfigError as e:
        # Handle configuration errors
        error_title = "Configuration Error"
        error_message = str(e)
        error_details = "Check your commands.yaml file for errors."
    except FileNotFoundError:
        # Handle missing config file
        error_title = "Configuration File Not Found"
        error_message = f"Could not find {config_path}"
        error_details = "Create a commands.yaml file in the current directory."
    except Exception as e:
        # Handle unexpected errors
        error_title = "Unexpected Error"
        error_message = str(e)
        error_details = "An unexpected error occurred during startup."

    # Create and configure app
    app = OpsApp(commands, config=config)

    # If there was an error, show it
    if error_title and error_message:
        app.show_error(error_title, error_message, error_details or "")

    # Run the app
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
