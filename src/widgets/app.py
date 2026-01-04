"""Main application widget for Ops Deck TUI."""

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static

from ..models import AppConfig, Command
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
        """Execute the selected command."""
        if self.selected_command:
            # This will be handled by command_selected message
            pass

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
                command_list.set_command_running(command_index, True)
            else:
                if execution_id in self._running_command_indices:
                    command_list.set_command_running(command_index, False)
                    del self._running_command_indices[execution_id]
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


