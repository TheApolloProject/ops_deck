"""Command list widget for Ops Deck."""

from textual.containers import Container, ScrollableContainer, Vertical
from textual.reactive import reactive
from textual.widgets import Label, Static
from textual.events import Key

from ..models import Command


class CommandListPanel(Container):
    """Panel displaying available commands."""

    selected_index: reactive[int] = reactive(0)
    
    BINDINGS = [
        ("up", "navigate_up", "Up"),
        ("down", "navigate_down", "Down"),
    ]

    def __init__(self, commands: list[Command], *args, **kwargs):
        """Initialize command list panel.

        Args:
            commands: List of available commands
        """
        super().__init__(*args, **kwargs)
        self.commands = commands
        self.selected_index = 0
        self._running_indices: set[int] = set()  # Track which commands are running

    def _format_command_line(self, index: int, command: Command) -> str:
        """Format a command line for display.

        Args:
            index: Command index
            command: Command object

        Returns:
            Formatted string
        """
        is_selected = index == self.selected_index
        is_running = index in self._running_indices

        # Show spinner if running, selection indicator if selected
        if is_running:
            prefix = "⟳ "  # Running indicator
        elif is_selected:
            prefix = "▶ "  # Selection indicator
        else:
            prefix = "  "  # Empty space

        # Truncate description to fit in wider 55 column panel
        desc = command.description[:40] if command.description else command.command[:40]
        return f"{prefix}{command.name:20} {desc}"

    def compose(self):
        """Compose the command list panel."""
        with Vertical():
            yield Label("Commands", id="command-header")
            with ScrollableContainer(id="command-scroll"):
                for i, cmd in enumerate(self.commands):
                    is_selected = i == self.selected_index
                    line = self._format_command_line(i, cmd)
                    yield Static(
                        line,
                        id=f"cmd_{i}",
                        classes="command-item" + (" active" if is_selected else ""),
                    )
            # Add description display for selected command
            yield Label("", id="command-description", classes="command-description")
        self._update_description_display()

    def _on_key(self, event: Key) -> None:
        """Handle keyboard input - prevent ScrollableContainer from consuming arrow keys."""
        if event.key == "up":
            self.navigate_up()
            event.stop()
        elif event.key == "down":
            self.navigate_down()
            event.stop()

    def action_navigate_up(self) -> None:
        """Action handler for navigate up binding."""
        self.navigate_up()

    def action_navigate_down(self) -> None:
        """Action handler for navigate down binding."""
        self.navigate_down()

    def navigate_up(self) -> None:
        """Move selection up."""
        if self.selected_index > 0:
            self.selected_index -= 1
            self._update_display()

    def navigate_down(self) -> None:
        """Move selection down."""
        if self.selected_index < len(self.commands) - 1:
            self.selected_index += 1
            self._update_display()

    def _update_display(self) -> None:
        """Update the display after selection change."""
        # Update all command items
        for i, cmd in enumerate(self.commands):
            try:
                item = self.query_one(f"#{f'cmd_{i}'}", Static)
                line = self._format_command_line(i, cmd)
                item.update(line)
                if i == self.selected_index:
                    item.add_class("active")
                    # Scroll to the selected item
                    item.scroll_visible()
                else:
                    item.remove_class("active")
            except Exception:
                pass
        self._update_description_display()

    def _update_description_display(self) -> None:
        """Update the description display for the selected command."""
        try:
            desc_label = self.query_one("#command-description", Label)
            selected_cmd = self.get_selected_command()
            if selected_cmd and selected_cmd.description:
                # Show full description truncated to panel width
                desc_text = f"📝 {selected_cmd.description}"
                desc_label.update(desc_text)
            else:
                desc_label.update("")
        except Exception:
            pass

    def get_selected_command(self) -> Command | None:
        """Get the currently selected command.

        Returns:
            Selected Command or None
        """
        if 0 <= self.selected_index < len(self.commands):
            return self.commands[self.selected_index]
        return None

    def set_command_running(self, index: int, running: bool) -> None:
        """Mark a command as running or completed.

        Args:
            index: Command index
            running: True if running, False if completed
        """
        if running:
            self._running_indices.add(index)
        else:
            self._running_indices.discard(index)
        self._update_display()
