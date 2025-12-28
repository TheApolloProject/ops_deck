"""Output line model for Ops Deck.

Represents a single line of output from a command execution.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class StreamType(str, Enum):
    """Type of output stream."""

    STDOUT = "stdout"
    STDERR = "stderr"


class OutputLine(BaseModel):
    """Represents a single line of command output."""

    id: str = Field(..., description="Unique output line ID")
    execution_id: str = Field(..., description="ID of the execution this output belongs to")
    timestamp: datetime = Field(..., description="When this output was captured")
    stream: StreamType = Field(..., description="Stream type (stdout or stderr)")
    content: str = Field(..., description="The actual output content", min_length=1)

    class Config:
        """Pydantic config."""

        use_enum_values = False
        json_schema_extra = {  # noqa: RUF012
            "example": {
                "id": "out_2025_001_001",
                "execution_id": "exec_2025_001",
                "timestamp": "2025-12-28T10:30:00.123456",
                "stream": "stdout",
                "content": "total 48",
            }
        }

    def __str__(self) -> str:
        """String representation."""
        return f"[{self.stream.value}] {self.content[:50]}..."

    def is_error(self) -> bool:
        """Check if this is an error output."""
        return self.stream == StreamType.STDERR
