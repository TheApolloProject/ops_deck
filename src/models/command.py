"""Command model for Ops Deck.

Represents a CLI command that can be executed.
"""

from pydantic import BaseModel, Field

from .interactive import SessionType


class Command(BaseModel):
    """Represents a CLI command configuration."""

    name: str = Field(..., description="Command name (must be unique)")
    command: str = Field(..., description="Shell command to execute")
    description: str = Field(default="", description="User-friendly description")
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")
    timeout: int = Field(default=300, ge=1, description="Execution timeout in seconds")
    env: dict[str, str] = Field(
        default_factory=dict, description="Environment variables for execution"
    )
    interactive: bool = Field(
        default=False, description="Whether this command requires TTY control"
    )
    session_type: SessionType | None = Field(
        default=None, description="Type of interactive session (if interactive=True)"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {  # noqa: RUF012
            "example": {
                "name": "list_files",
                "command": "ls -la /tmp",
                "description": "List all files in /tmp",
                "tags": ["filesystem", "listing"],
                "timeout": 10,
                "env": {},
            }
        }

    def __str__(self) -> str:
        """String representation."""
        return f"{self.name}: {self.command}"

    def __repr__(self) -> str:
        """Debug representation."""
        return f"Command(name={self.name!r}, command={self.command!r})"
