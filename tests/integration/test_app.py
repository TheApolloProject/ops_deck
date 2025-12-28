"""Integration tests for Ops Deck application."""

import pytest

from src.services.command_runner import AsyncCommandRunner
from src.services.config import ConfigLoader
from src.widgets import OpsApp


def test_config_loader_integration(sample_command, valid_config):
    """Test ConfigLoader with valid configuration."""
    loader = ConfigLoader()
    commands, app_config = loader.load_and_validate("commands.yaml")

    assert len(commands) > 0
    assert app_config is not None
    assert app_config.theme in ["dark", "light"]


@pytest.mark.asyncio
async def test_command_runner_with_loaded_config():
    """Test CommandRunner with commands loaded from config."""
    loader = ConfigLoader()
    commands, _ = loader.load_and_validate("commands.yaml")

    # Get first command
    if commands:
        command = commands[0]
        runner = AsyncCommandRunner()
        execution = await runner.run(command)

        # Should complete (may succeed or fail based on command)
        assert execution.is_complete()


def test_app_initialization():
    """Test OpsApp initialization with config and commands."""
    loader = ConfigLoader()
    commands, app_config = loader.load_and_validate("commands.yaml")

    app = OpsApp(commands, app_config)

    assert app.commands == commands
    assert app.config == app_config
    assert app.TITLE == "Ops Deck"


def test_command_list_panel_creation():
    """Test CommandListPanel creation and selection."""
    from src.models import Command
    from src.widgets import CommandListPanel

    commands = [
        Command(name="cmd1", command="echo 1", description="First"),
        Command(name="cmd2", command="echo 2", description="Second"),
        Command(name="cmd3", command="echo 3", description="Third"),
    ]

    panel = CommandListPanel(commands)

    assert len(panel.commands) == 3
    assert panel.selected_index == 0
    assert panel.get_selected_command() == commands[0]


def test_command_list_navigation():
    """Test CommandListPanel navigation."""
    from src.models import Command
    from src.widgets import CommandListPanel

    commands = [
        Command(name="cmd1", command="echo 1"),
        Command(name="cmd2", command="echo 2"),
        Command(name="cmd3", command="echo 3"),
    ]

    panel = CommandListPanel(commands)

    # Start at first command
    assert panel.selected_index == 0

    # Navigate down
    panel.navigate_down()
    assert panel.selected_index == 1

    panel.navigate_down()
    assert panel.selected_index == 2

    # Can't go past last
    panel.navigate_down()
    assert panel.selected_index == 2

    # Navigate up
    panel.navigate_up()
    assert panel.selected_index == 1

    panel.navigate_up()
    assert panel.selected_index == 0

    # Can't go before first
    panel.navigate_up()
    assert panel.selected_index == 0


def test_output_pane_basic():
    """Test OutputPane basic functionality."""
    from datetime import datetime

    from src.models import OutputLine, StreamType
    from src.widgets import OutputPane

    pane = OutputPane()

    # Should start empty
    assert pane.lines_count == 0
    assert len(pane.output_lines) == 0

    # Add a line
    line = OutputLine(
        id="test_1",
        execution_id="exec_1",
        timestamp=datetime.now(),
        stream=StreamType.STDOUT,
        content="test output",
    )
    pane.add_output_line(line)

    assert pane.lines_count == 1
    assert len(pane.output_lines) == 1

    # Clear output
    pane.clear_output()
    assert pane.lines_count == 0


def test_output_pane_multiple_lines():
    """Test OutputPane with multiple output lines."""
    from datetime import datetime

    from src.models import OutputLine, StreamType
    from src.widgets import OutputPane

    pane = OutputPane()

    # Add multiple lines
    for i in range(5):
        line = OutputLine(
            id=f"test_{i}",
            execution_id="exec_1",
            timestamp=datetime.now(),
            stream=StreamType.STDOUT if i % 2 == 0 else StreamType.STDERR,
            content=f"line {i}",
        )
        pane.add_output_line(line)

    assert pane.lines_count == 5
    assert len(pane.output_lines) == 5


def test_app_config_loading():
    """Test loading app config with various settings."""
    from src.models import AppConfig, LogLevel

    config = AppConfig(
        theme="dark",
        refresh_rate=2.0,
        log_level=LogLevel.DEBUG,
        command_timeout=600,
        max_output_lines=50000,
    )

    assert config.theme == "dark"
    assert config.refresh_rate == 2.0
    assert config.log_level == LogLevel.DEBUG
    assert config.command_timeout == 600
    assert config.max_output_lines == 50000
