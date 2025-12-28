"""Application configuration model for Ops Deck.

Represents the global application settings.
"""

from enum import Enum

from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    """Logging level options."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class AppConfig(BaseModel):
    """Global application configuration."""

    theme: str = Field(default="dark", description="UI theme (dark, light, etc.)")
    refresh_rate: float = Field(
        default=1.0, ge=0.1, le=10.0, description="UI refresh rate in Hz"
    )
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    command_timeout: int = Field(
        default=300, ge=1, le=3600, description="Default timeout for commands (seconds)"
    )
    max_output_lines: int = Field(
        default=10000, ge=100, le=1000000, description="Maximum output lines to keep"
    )
    auto_scroll: bool = Field(
        default=True, description="Auto-scroll output pane to bottom"
    )

    class Config:
        """Pydantic config."""

        use_enum_values = False
        json_schema_extra = {  # noqa: RUF012
            "example": {
                "theme": "dark",
                "refresh_rate": 1.0,
                "log_level": "INFO",
                "command_timeout": 300,
                "max_output_lines": 10000,
                "auto_scroll": True,
            }
        }

    def __str__(self) -> str:
        """String representation."""
        return f"AppConfig(theme={self.theme}, refresh_rate={self.refresh_rate}Hz)"
