"""Interactive subprocess session management for TUI."""

import asyncio
import os
from datetime import datetime

from ..models import Command, InteractiveSession, SessionType


class InteractiveRunner:
    """Manages interactive subprocess sessions with TTY control."""

    def __init__(self) -> None:
        """Initialize the runner."""
        self._active_sessions: list[InteractiveSession] = []

    async def run_session(
        self,
        command: Command,
        app,  # Textual App instance
        logging_enabled: bool = False,
        log_file_path: str | None = None,
    ) -> InteractiveSession:
        """Launch interactive session, suspend TUI, restore on exit.

        Args:
            command: Command definition with interactive=True
            app: Textual App instance for suspend/resume
            logging_enabled: Enable full I/O logging for this session
            log_file_path: Path to write session log (if logging_enabled)

        Returns:
            InteractiveSession with exit_code, end_time, error_log populated

        Raises:
            ValueError: If command.interactive != True
            RuntimeError: If subprocess fails or terminal restoration fails
        """
        # Validation
        if not command.interactive:
            raise ValueError(f"Command '{command.name}' is not marked as interactive")

        # Create session
        session = InteractiveSession(
            command=command.command,
            session_type=command.session_type or SessionType.OTHER,
            start_time=datetime.now(),
            working_directory=os.getcwd(),
            environment_snapshot=dict(os.environ),
            logging_enabled=logging_enabled,
            log_file_path=log_file_path,
        )

        # Suspend TUI
        app.suspend()

        try:
            # Set environment flag to block nested instances
            env = os.environ.copy()
            env["OPS_DECK_ACTIVE"] = "1"

            # Launch subprocess with TTY inheritance
            process = await asyncio.create_subprocess_shell(
                session.command,
                stdin=None,  # Inherit parent TTY
                stdout=None,
                stderr=None,
                env=env,
            )

            session.pid = process.pid
            self._active_sessions.append(session)

            # Wait for subprocess to exit
            exit_code = await process.wait()
            session.exit_code = exit_code

        except Exception as e:
            session.error_log.append(f"[ERROR] {type(e).__name__}: {str(e)}")
            session.exit_code = -1

        finally:
            # Always restore TUI
            app.resume()
            session.end_time = datetime.now()
            if session in self._active_sessions:
                self._active_sessions.remove(session)

        return session

    @staticmethod
    def detect_nested_instance() -> bool:
        """Check if ops-deck is already running in parent environment."""
        return os.environ.get("OPS_DECK_ACTIVE") == "1"

    def get_active_sessions(self) -> list[InteractiveSession]:
        """Get currently running sessions."""
        return self._active_sessions.copy()
