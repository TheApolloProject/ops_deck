"""Textual message classes for inter-widget communication.

Messages are used to communicate between widgets in the TUI.
"""


from textual.message import Message

from .models import Execution, ExecutionStatus, OutputLine


class CommandOutput(Message):
    """Message sent when command output is received.

    Attributes:
        execution_id: ID of the execution producing output
        output_line: The output line object
    """

    def __init__(
        self, execution_id: str, output_line: OutputLine, **kwargs
    ) -> None:
        """Initialize the message."""
        super().__init__(**kwargs)
        self.execution_id = execution_id
        self.output_line = output_line


class StatusUpdate(Message):
    """Message sent when execution status changes.

    Attributes:
        execution_id: ID of the execution
        status: New execution status
        message: Optional status message
    """

    def __init__(
        self, execution_id: str, status: ExecutionStatus, message: str | None = None, **kwargs
    ) -> None:
        """Initialize the message."""
        super().__init__(**kwargs)
        self.execution_id = execution_id
        self.status = status
        self.message = message


class ExecutionComplete(Message):
    """Message sent when command execution completes.

    Attributes:
        execution: The completed execution object
    """

    def __init__(self, execution: Execution, **kwargs) -> None:
        """Initialize the message."""
        super().__init__(**kwargs)
        self.execution = execution


class ExecutionError(Message):
    """Message sent when command execution fails.

    Attributes:
        execution_id: ID of the execution
        error: Error message
    """

    def __init__(self, execution_id: str, error: str, **kwargs) -> None:
        """Initialize the message."""
        super().__init__(**kwargs)
        self.execution_id = execution_id
        self.error = error


class CommandStarted(Message):
    """Message sent when a command starts executing.

    Attributes:
        execution: The execution object
    """

    def __init__(self, execution: Execution, **kwargs) -> None:
        """Initialize the message."""
        super().__init__(**kwargs)
        self.execution = execution
