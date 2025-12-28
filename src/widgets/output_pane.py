"""Output pane widget for Ops Deck."""


from textual.containers import Container, ScrollableContainer, Vertical
from textual.reactive import reactive
from textual.widgets import Label, Static

from ..models import Execution, OutputLine, StreamType


class OutputPane(Container):
    """Pane for displaying command output."""

    lines_count: reactive[int] = reactive(0)

    def __init__(self, *args, **kwargs):
        """Initialize output pane."""
        super().__init__(*args, **kwargs)
        self.output_lines: list[OutputLine] = []
        self._is_running = False
        self._current_execution: Execution | None = None
        self._user_scrolled = False  # Track if user manually scrolled
        self._auto_scroll_enabled = True  # Enable/disable auto-scroll

    def compose(self):
        """Compose the output pane."""
        with Vertical():
            yield Label("Output", id="output-header")
            with ScrollableContainer(id="output-container"):
                yield Static("Ready to execute commands...", id="output-content")

    def add_output_line(self, line: OutputLine) -> None:
        """Add an output line to the display.

        Args:
            line: OutputLine to add
        """
        self.output_lines.append(line)
        self.lines_count = len(self.output_lines)
        self._update_display()

    def clear_output(self) -> None:
        """Clear all output lines."""
        self.output_lines.clear()
        self.lines_count = 0
        self._update_display()

    def set_running(self, running: bool) -> None:
        """Set execution status.

        Args:
            running: True if command is running
        """
        self._is_running = running
        self._update_display()

    def set_execution_complete(self, execution: Execution) -> None:
        """Handle execution completion.

        Args:
            execution: Completed Execution object
        """
        self._current_execution = execution
        self._is_running = False
        self._update_display()

    def start_command(self, execution: Execution) -> None:
        """Handle start of a new command execution.

        Args:
            execution: Execution object for the new command
        """
        # Add command header
        self._is_running = True
        self._current_execution = execution
        self._auto_scroll_enabled = True
        self._user_scrolled = False

        # Add header to output lines as special marker
        # We'll format this separately in display
        self._update_display()

    def _get_stream_class(self, stream_type: StreamType) -> str:
        """Get CSS class for stream type.

        Args:
            stream_type: Type of stream (STDOUT or STDERR)

        Returns:
            CSS class name
        """
        return "stdout" if stream_type == StreamType.STDOUT else "stderr"

    def _format_output_line(self, line: OutputLine) -> str:
        """Format an OutputLine for display.

        Args:
            line: OutputLine to format

        Returns:
            Formatted string
        """
        # Add stream prefix to distinguish stdout vs stderr
        prefix = "[OUT] " if line.stream == StreamType.STDOUT else "[ERR] "
        return f"{prefix}{line.content}"

    def _format_completion_message(self) -> str:
        """Format the completion status message.

        Returns:
            Formatted completion message with status indicator
        """
        if not self._current_execution:
            return ""

        if self._current_execution.exit_code == 0:
            return "✓ Command succeeded"
        else:
            return f"✗ Command failed (exit code: {self._current_execution.exit_code})"

    def _format_command_header(self) -> str:
        """Format the command execution header.

        Returns:
            Formatted command header with name and start time
        """
        if not self._current_execution:
            return ""

        command_name = self._current_execution.command.name
        start_time = (
            self._current_execution.start_time.strftime("%H:%M:%S")
            if self._current_execution.start_time
            else "unknown"
        )
        return f"[START] {command_name} at {start_time}"

    def _update_display(self) -> None:
        """Update the output display."""
        try:
            content_widget = self.query_one("#output-content", Static)

            if not self.output_lines and not self._current_execution:
                content_widget.update(
                    "Ready to execute commands..." if not self._is_running else "Running..."
                )
            else:
                # Build output with all lines
                output_lines = []

                # Add command header if execution is running or just started
                if self._current_execution and (self._is_running or self.output_lines):
                    # Only show header once at the start
                    if not self.output_lines or len(self.output_lines) == 0:
                        header = self._format_command_header()
                        if header:
                            output_lines.append(header)
                            output_lines.append("-" * 50)

                # Add command output lines
                for line in self.output_lines:
                    formatted = self._format_output_line(line)
                    output_lines.append(formatted)

                # Add completion message if execution finished
                if self._current_execution and not self._is_running:
                    completion_msg = self._format_completion_message()
                    if completion_msg:
                        # Add blank line before completion message
                        output_lines.append("")
                        # Color the message based on exit code
                        if self._current_execution.exit_code == 0:
                            output_lines.append(f"[SUCCESS] {completion_msg}")
                        else:
                            output_lines.append(f"[ERROR] {completion_msg}")

                # Limit to max_output_lines (default 10000)
                content = "\n".join(output_lines[-10000:])
                content_widget.update(content)

                # Auto-scroll to bottom by scrolling the container
                try:
                    container = self.query_one("#output-container", ScrollableContainer)

                    # Check if user has scrolled up
                    if hasattr(container, 'vertical_scroll'):
                        max_scroll = container.scrollable_content_size.height - container.size.height  # type: ignore
                        current_scroll = container.vertical_scroll
                        # If we're not at the bottom, user has scrolled up
                        if current_scroll < max_scroll - 5:
                            self._user_scrolled = True
                        elif self._user_scrolled and current_scroll >= max_scroll - 5:
                            # User scrolled back to bottom, resume auto-scroll
                            self._user_scrolled = False

                    # Only auto-scroll if enabled and user hasn't scrolled up
                    if self._auto_scroll_enabled and not self._user_scrolled:
                        container.scroll_end(animate=False)
                except Exception:
                    pass

        except Exception:
            # Widget not yet mounted
            pass

    def get_output_text(self) -> str:
        """Get all output as text.

        Returns:
            All output lines as newline-separated text
        """
        return "\n".join(self._format_output_line(line) for line in self.output_lines)

