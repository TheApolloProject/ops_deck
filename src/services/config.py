"""Configuration loading and validation service.

Loads and validates YAML configuration files.
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError as PydanticValidationError

from ..exceptions import ConfigError
from ..models import AppConfig, Command


class ConfigLoader:
    """Loads and validates configuration from YAML files."""

    def load(self, path: str) -> dict[str, Any]:
        """Load configuration from a YAML file.

        Args:
            path: Path to the YAML configuration file

        Returns:
            Dictionary containing the configuration

        Raises:
            ConfigError: If file cannot be read or YAML is invalid
        """
        config_path = Path(path)

        if not config_path.exists():
            raise ConfigError(f"Configuration file not found: {path}")

        if not config_path.is_file():
            raise ConfigError(f"Path is not a file: {path}")

        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)  # type: ignore

            if config is None:
                config = {}

            return config  # type: ignore
        except yaml.YAMLError as e:
            # Extract line number from YAML error if available
            error_msg = str(e)
            if hasattr(e, "problem_mark"):
                line = e.problem_mark.line + 1
                raise ConfigError(f"Invalid YAML at line {line} in {path}: {error_msg}")
            raise ConfigError(f"Invalid YAML in {path}: {error_msg}")
        except OSError as e:
            raise ConfigError(f"Cannot read configuration file {path}: {e}")

    def validate(self, config: dict) -> tuple[list[Command], AppConfig]:
        """Validate configuration dictionary.

        Args:
            config: Dictionary containing commands and app config

        Returns:
            Tuple of (commands list, AppConfig)

        Raises:
            ConfigError: If configuration is invalid
        """
        try:
            # Load commands
            commands_data = config.get("commands", [])
            if not isinstance(commands_data, list):
                raise ConfigError("Invalid config: 'commands' must be a list")

            commands = []
            for i, cmd_data in enumerate(commands_data):
                try:
                    command = Command(**cmd_data)
                    commands.append(command)
                except PydanticValidationError as e:
                    # Extract field information from validation error
                    error_details = []
                    for err in e.errors():
                        field = ".".join(str(f) for f in err["loc"])
                        msg = err["msg"]
                        error_details.append(f"{field}: {msg}")
                    error_msg = "; ".join(error_details)
                    raise ConfigError(
                        f"Invalid command at index {i}: {error_msg}\n"
                        f"Required fields: name, command\n"
                        f"Optional fields: description, tags, timeout, env"
                    )

            # Load app config
            app_config_data = config.get("app", {})
            if not isinstance(app_config_data, dict):
                raise ConfigError("Invalid config: 'app' must be a dictionary")

            try:
                app_config = AppConfig(**app_config_data)
            except PydanticValidationError as e:
                error_details = []
                for err in e.errors():
                    field = ".".join(str(f) for f in err["loc"])
                    msg = err["msg"]
                    error_details.append(f"{field}: {msg}")
                error_msg = "; ".join(error_details)
                raise ConfigError(
                    f"Invalid app configuration: {error_msg}\n"
                    f"Optional fields: theme, refresh_rate, log_level, command_timeout, max_output_lines, auto_scroll"
                )

            return commands, app_config

        except ConfigError:
            raise
        except Exception as e:
            raise ConfigError(f"Configuration validation failed: {e}")

    def load_and_validate(self, path: str) -> tuple[list[Command], AppConfig]:
        """Load and validate configuration in one step.

        Args:
            path: Path to the YAML configuration file

        Returns:
            Tuple of (commands list, AppConfig)

        Raises:
            ConfigError: If file cannot be loaded or validation fails
        """
        config = self.load(path)
        return self.validate(config)

