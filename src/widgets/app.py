"""Main application widget for Ops Deck TUI."""

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static

from ..messages import CommandOutput, ExecutionComplete
from ..models import AppConfig, Command, OutputLine
from ..services.command_runner import AsyncCommandRunner
from ..services.interactive_runner import InteractiveRunner
from .command_list import CommandListPanel
from .output_pane import OutputPane


class ErrorScreen(Static):
    """Display configuration or startup errors."""

    DEFAULT_CSS = """
    ErrorScreen {
        background: $surface;
        color: $text;
        align: center middle;
        padding: 2 4;
    }
    """

    def __init__(self, title: str, message: str, details: str = ""):
        """Initialize error screen.

        Args:
            title: Error title
            message: Main error message
            details: Additional error details
        """
        super().__init__()
        self.title = title
        self.message = message
        self.details = details

    def render(self) -> str:
        """Render the error screen."""
        output = f"\n[bold red]{self.title}[/bold red]\n\n"
        output += f"{self.message}\n"
        if self.details:
            output += f"\n[dim]{self.details}[/dim]\n"
        output += "\n[yellow]Press Q to exit[/yellow]\n"
        return output


class OpsApp(App):
    """Main Ops Deck application."""

    TITLE = "Ops Deck"
    SUB_TITLE = "CLI Command Dashboard"
    CSS_PATH = "../styles/app.css"

    # Enable parallel execution by setting exclusive=False on workers
    # This allows multiple commands to run concurrently

    def __init__(self, commands: list[Command], config: AppConfig | None = None):
        """Initialize the app.

        Args:
            commands: List of available commands
            config: Application configuration (optional, for error screens)
        """
        super().__init__()
        self.commands = commands
        self.config = config
        self.selected_command: Command | None = None
        self._running_command_indices: dict[str, int] = {}  # Track execution ID to command index
        self._error_screen: ErrorScreen | None = None
        self.runner = AsyncCommandRunner()  # Command execution service
        self.interactive_runner = InteractiveRunner()  # Interactive session service
        self._running_executions: dict[str, int] = {}  # Map execution ID to command index

    def compose(self) -> ComposeResult:
        """Create child widgets for the layout."""
        if self._error_screen:
            # Show error screen if present
            yield Header()
            yield self._error_screen
            yield Footer()
        else:
            # Normal layout
            yield Header(show_clock=True)
            with Horizontal(id="main-content"):
                yield CommandListPanel(self.commands, id="command-panel")
                yield OutputPane(id="output-pane")
            yield Footer()

    def on_mount(self) -> None:
        """Handle app initialization."""
        # Note: Custom theme setting is currently disabled due to Textual's
        # strict theme registration requirements. Using default Textual theme.
        # TODO: Re-enable custom theme support when Textual theme API is clearer
        pass

    def action_quit(self) -> None:  # type: ignore
        """Quit the application."""
        self.exit()

    def action_execute(self) -> None:
        """Execute the selected command.

        Routes to interactive or async runner based on command.interactive flag.
        """
        # Get command list panel and selected command
        try:
            command_list = self.query_one(CommandListPanel)
            selected_command = command_list.get_selected_command()
            command_index = command_list.selected_index
        except Exception:
            return

        if not selected_command:
            return

        # Store reference for potential future use
        self.selected_command = selected_command

        # Check if this is an interactive command
        if selected_command.interactive:
            # Route to interactive runner
            self._execute_interactive(selected_command, command_index)
        else:
            # Route to async runner (existing behavior)
            self._execute_async(selected_command, command_index)

    def _execute_interactive(self, command: Command, command_index: int) -> None:
        """Execute an interactive command.

        Args:
            command: Command to execute
            command_index: Index of command in the command list
        """

        def run_interactive() -> None:
            """Worker function to run the interactive command."""
            import asyncio

            try:
                # Run the interactive session
                session = asyncio.run(self.interactive_runner.run_session(command, self))

                # Display result
                if session.exit_code == 0:
                    self.notify(f"✓ '{command.name}' completed successfully")
                else:
                    self.notify(
                        f"✗ '{command.name}' exited with code {session.exit_code}",
                        severity="error",
                    )
                    for error in session.error_log:
                        self.log(error)

                # Update output pane with session info
                try:
                    output_pane = self.query_one(OutputPane)
                    output_pane.clear_output()
                    output_pane.add_line(
                        OutputLine(
                            execution_id=f"interactive_{command_index}",
                            stream_type="stdout",
                            text=f"Session: {session.command}",
                            timestamp="",
                        )
                    )
                    output_pane.add_line(
                        OutputLine(
                            execution_id=f"interactive_{command_index}",
                            stream_type="stdout",
                            text=f"Exit Code: {session.exit_code}",
                            timestamp="",
                        )
                    )
                    if session.duration is not None:
                        output_pane.add_line(
                            OutputLine(
                                execution_id=f"interactive_{command_index}",
                                stream_type="stdout",
                                text=f"Duration: {session.duration:.2f}s",
                                timestamp="",
                            )
                        )
                except Exception:
                    pass

            except Exception as e:
                self.notify(f"Error running interactive session: {str(e)}", severity="error")

        # Mark as running
        self.mark_command_running(command_index, f"interactive_{command_index}", True)

        # Spawn the worker
        self.run_worker(run_interactive, thread=True)

    def _execute_async(self, command: Command, command_index: int) -> None:
        """Execute an async command (existing behavior).

        Args:
            command: Command to execute
            command_index: Index of command in the command list
        """
        # Get output pane and clear previous output
        try:
            output_pane = self.query_one(OutputPane)
            output_pane.clear_output()
        except Exception:
            return

        # Define output callback - called for each output line
        def output_callback(line: OutputLine) -> None:
            """Handle output line from command execution."""
            self.post_message(CommandOutput(line.execution_id, line))

        # Define completion callback - called when execution finishes
        def completion_callback(execution) -> None:  # type: ignore
            """Handle command completion."""
            self.post_message(ExecutionComplete(execution))

        # Create and run worker to execute command
        def run_command() -> None:
            """Worker function to run the command asynchronously."""
            import asyncio

            try:
                # Run the command with callbacks
                asyncio.run(
                    self.runner.run(
                        command,
                        output_callback=output_callback,
                        completion_callback=completion_callback,
                    )
                )
            except Exception as e:
                # If execution fails, post error and mark as complete
                from ..models import Execution, ExecutionStatus

                error_execution = Execution(
                    id=f"exec_error_{command_index}",
                    command=command,
                    start_time=None,
                    end_time=None,
                    exit_code=None,
                    status=ExecutionStatus.ERROR,
                    error_message=str(e),
                )
                completion_callback(error_execution)

        # Track execution with command index
        # We'll update this when we receive the execution ID from the first output
        self.mark_command_running(command_index, f"exec_{command_index}", True)

        # Spawn the worker (thread=True because run_command is sync and calls asyncio.run())
        self.run_worker(run_command, thread=True)

    def action_navigate_up(self) -> None:
        """Navigate up in command list."""
        try:
            command_list = self.query_one(CommandListPanel)
            command_list.navigate_up()
        except Exception:
            pass

    def action_navigate_down(self) -> None:
        """Navigate down in command list."""
        try:
            command_list = self.query_one(CommandListPanel)
            command_list.navigate_down()
        except Exception:
            pass

    def mark_command_running(self, command_index: int, execution_id: str, running: bool) -> None:
        """Mark a command as running or completed.

        Args:
            command_index: Index of the command in the list
            execution_id: ID of the execution
            running: True if running, False if completed
        """
        try:
            command_list = self.query_one(CommandListPanel)

            if running:
                self._running_command_indices[execution_id] = command_index
                self._running_executions[execution_id] = command_index
                command_list.set_command_running(command_index, True)
            else:
                if execution_id in self._running_command_indices:
                    command_list.set_command_running(command_index, False)
                    del self._running_command_indices[execution_id]
                if execution_id in self._running_executions:
                    del self._running_executions[execution_id]
        except Exception:
            pass

    def on_command_output(self, message: CommandOutput) -> None:
        """Handle output line from running command.

        Args:
            message: CommandOutput message with execution ID and output line
        """
        try:
            output_pane = self.query_one(OutputPane)
            output_pane.add_output_line(message.output_line)
        except Exception:
            pass

    def on_execution_complete(self, message: ExecutionComplete) -> None:
        """Handle command execution completion.

        Args:
            message: ExecutionComplete message with execution result
        """
        try:
            execution = message.execution
            output_pane = self.query_one(OutputPane)

            # Update output pane with completion status
            output_pane.set_execution_complete(execution)

            # Mark command as no longer running
            if execution.id in self._running_executions:
                command_index = self._running_executions[execution.id]
                self.mark_command_running(command_index, execution.id, False)
        except Exception:
            pass

    def show_error(self, title: str, message: str, details: str = "") -> None:
        """Display an error screen.

        Set error before calling app.run() to show error screen on startup.

        Args:
            title: Error title
            message: Main error message
            details: Additional error details
        """
        self._error_screen = ErrorScreen(title, message, details)

    BINDINGS = [  # noqa: RUF012
        ("q", "quit", "Quit"),
        ("enter", "execute", "Execute"),
        ("up", "navigate_up", "Up"),
        ("down", "navigate_down", "Down"),
    ]


