"""Interactive session models for TUI subprocess management."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class SessionType(str, Enum):
    """Categories of interactive sessions."""

    SHELL = "shell"
    EDITOR = "editor"
    MULTIPLEXER = "multiplexer"
    OTHER = "other"


@dataclass
class InteractiveSession:
    """Represents an interactive subprocess session with TTY control."""

    session_id: str = field(default_factory=lambda: str(uuid4()))
    command: str = ""
    session_type: SessionType = SessionType.OTHER
    pid: int | None = None
    exit_code: int | None = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    working_directory: str = ""
    environment_snapshot: dict[str, str] = field(default_factory=dict)
    error_log: list[str] = field(default_factory=list)
    logging_enabled: bool = False
    log_file_path: str | None = None

    @property
    def duration(self) -> float | None:
        """Duration in seconds, or None if still running."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds()
