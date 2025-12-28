"""Execution model for Ops Deck.

Represents a single execution of a command.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from .command import Command


class ExecutionStatus(str, Enum):
    """Status of a command execution."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"


class Execution(BaseModel):
    """Represents a single command execution."""

    id: str = Field(..., description="Unique execution ID")
    command: Command = Field(..., description="The command being executed")
    start_time: datetime | None = Field(None, description="Execution start time")
    end_time: datetime | None = Field(None, description="Execution end time")
    exit_code: int | None = Field(None, description="Process exit code")
    status: ExecutionStatus = Field(
        default=ExecutionStatus.PENDING, description="Current execution status"
    )
    error_message: str | None = Field(None, description="Error message if failed")

    class Config:
        """Pydantic config."""

        use_enum_values = False
        json_schema_extra = {  # noqa: RUF012
            "example": {
                "id": "exec_2025_001",
                "command": {"name": "list_files", "command": "ls -la /tmp"},
                "start_time": "2025-12-28T10:30:00",
                "end_time": "2025-12-28T10:30:01",
                "exit_code": 0,
                "status": "success",
                "error_message": None,
            }
        }

    def __str__(self) -> str:
        """String representation."""
        return f"Execution({self.command.name}): {self.status.value}"

    def duration_seconds(self) -> float | None:
        """Calculate execution duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def is_running(self) -> bool:
        """Check if execution is currently running."""
        return self.status == ExecutionStatus.RUNNING

    def is_complete(self) -> bool:
        """Check if execution is complete."""
        return self.status in (
            ExecutionStatus.SUCCESS,
            ExecutionStatus.ERROR,
            ExecutionStatus.TIMEOUT,
        )
