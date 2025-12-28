"""Unit tests for CommandRunner service."""

import pytest

from src.models import Command, ExecutionStatus
from src.services.command_runner import AsyncCommandRunner


@pytest.mark.asyncio
async def test_simple_echo_command():
    """Test executing a simple echo command."""
    runner = AsyncCommandRunner()
    command = Command(name="echo", command="echo hello", timeout=10)

    execution = await runner.run(command)

    assert execution.status == ExecutionStatus.SUCCESS
    assert execution.exit_code == 0
    assert execution.start_time is not None
    assert execution.end_time is not None


@pytest.mark.asyncio
async def test_command_with_error():
    """Test command that fails."""
    runner = AsyncCommandRunner()
    command = Command(name="fail", command="exit 42", timeout=10)

    execution = await runner.run(command)

    assert execution.status == ExecutionStatus.ERROR
    assert execution.exit_code == 42
    assert execution.error_message is not None


@pytest.mark.asyncio
async def test_output_callback():
    """Test that output callback is called."""
    runner = AsyncCommandRunner()
    command = Command(name="echo", command="echo -e 'line1\\nline2\\nline3'", timeout=10)

    output_lines = []

    def callback(line):
        output_lines.append(line)

    execution = await runner.run(command, output_callback=callback)

    assert execution.status == ExecutionStatus.SUCCESS
    assert len(output_lines) >= 1
    # At least some output should have been captured
    assert all(line.content for line in output_lines)


@pytest.mark.asyncio
async def test_stderr_capture():
    """Test capturing stderr separately."""
    runner = AsyncCommandRunner()
    command = Command(
        name="stderr",
        command="python3 -c \"import sys; sys.stderr.write('error line')\"",
        timeout=10,
    )

    output_lines = []

    def callback(line):
        output_lines.append(line)

    execution = await runner.run(command, output_callback=callback)

    assert execution.status == ExecutionStatus.SUCCESS
    assert len(output_lines) >= 1
    # Check that stderr was captured
    stderr_lines = [line for line in output_lines if line.is_error()]
    assert len(stderr_lines) >= 1


@pytest.mark.asyncio
async def test_timeout_handling():
    """Test timeout behavior."""
    runner = AsyncCommandRunner()
    command = Command(
        name="sleep",
        command="sleep 10",
        timeout=1,  # 1 second timeout
    )

    from src.exceptions import TimeoutError as OpsTimeoutError

    with pytest.raises(OpsTimeoutError):
        await runner.run(command)


@pytest.mark.asyncio
async def test_execution_metadata():
    """Test that execution metadata is properly set."""
    runner = AsyncCommandRunner()
    command = Command(name="test", command="echo test", timeout=10)

    execution = await runner.run(command)

    assert execution.id.startswith("exec_")
    assert execution.command.name == "test"
    assert execution.start_time is not None
    assert execution.end_time is not None
    assert execution.duration_seconds() is not None
    assert execution.duration_seconds() >= 0
