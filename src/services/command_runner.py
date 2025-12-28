"""Command execution service for Ops Deck.

Provides async command execution with output streaming.
"""

import asyncio
import uuid
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime

from ..exceptions import ExecutionError
from ..exceptions import TimeoutError as OpsTimeoutError
from ..models import Command, Execution, ExecutionStatus, OutputLine, StreamType


class CommandRunner(ABC):
    """Abstract base class for command execution."""

    @abstractmethod
    async def run(
        self,
        command: Command,
        output_callback: Callable[[OutputLine], None] | None = None,
        completion_callback: Callable[[Execution], None] | None = None,
    ) -> Execution:
        """Execute a command and stream its output.

        Args:
            command: Command to execute
            output_callback: Optional callback for each output line
            completion_callback: Optional callback when execution completes

        Returns:
            Completed Execution object

        Raises:
            ExecutionError: If execution fails
            TimeoutError: If execution exceeds timeout
        """


class AsyncCommandRunner(CommandRunner):
    """Async command runner using asyncio subprocess."""

    async def run(
        self,
        command: Command,
        output_callback: Callable[[OutputLine], None] | None = None,
        completion_callback: Callable[[Execution], None] | None = None,
    ) -> Execution:
        """Execute command asynchronously with output streaming.

        Args:
            command: Command to execute
            output_callback: Optional callback for each output line
            completion_callback: Optional callback when execution completes

        Returns:
            Completed Execution object

        Raises:
            ExecutionError: If execution fails
            TimeoutError: If execution exceeds timeout
        """
        execution_id = f"exec_{uuid.uuid4().hex[:8]}"
        execution = Execution(
            id=execution_id,
            command=command,
            start_time=None,
            end_time=None,
            exit_code=None,
            error_message=None,
        )

        try:
            execution.status = ExecutionStatus.RUNNING
            execution.start_time = datetime.now()

            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                command.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=command.env or None,
            )

            # Stream output from both stdout and stderr
            stdout_task = self._stream_output(
                process.stdout, execution_id, StreamType.STDOUT, output_callback
            )
            stderr_task = self._stream_output(
                process.stderr, execution_id, StreamType.STDERR, output_callback
            )

            try:
                # Wait for all output and process completion
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, process.wait()),
                    timeout=command.timeout,
                )

            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                execution.status = ExecutionStatus.TIMEOUT
                execution.error_message = f"Command exceeded timeout of {command.timeout}s"
                execution.end_time = datetime.now()
                raise OpsTimeoutError(execution.error_message)

            execution.exit_code = process.returncode
            execution.end_time = datetime.now()

            if process.returncode == 0:
                execution.status = ExecutionStatus.SUCCESS
            else:
                execution.status = ExecutionStatus.ERROR
                execution.error_message = f"Command failed with exit code {process.returncode}"

        except OpsTimeoutError:
            raise
        except ExecutionError:
            raise
        except Exception as e:
            execution.status = ExecutionStatus.ERROR
            execution.error_message = str(e)
            execution.end_time = datetime.now()
            raise ExecutionError(f"Command execution failed: {e}")

        finally:
            # Call completion callback if provided
            if completion_callback:
                completion_callback(execution)

        return execution

    async def _stream_output(
        self,
        reader: asyncio.StreamReader | None,
        execution_id: str,
        stream_type: StreamType,
        callback: Callable[[OutputLine], None] | None = None,
    ) -> None:
        """Stream output from a subprocess stream.

        Args:
            reader: Subprocess stream reader
            execution_id: ID of the execution
            stream_type: Type of stream (stdout/stderr)
            callback: Optional callback for each line
        """
        if not reader:
            return

        line_num = 0
        while True:
            try:
                data = await reader.readline()
                if not data:
                    break

                # Decode output
                try:
                    content = data.decode("utf-8").rstrip("\n")
                except UnicodeDecodeError:
                    content = data.decode("utf-8", errors="replace").rstrip("\n")

                # Skip empty lines
                if not content:
                    continue

                # Create output line object
                output_line = OutputLine(
                    id=f"out_{uuid.uuid4().hex[:8]}",
                    execution_id=execution_id,
                    timestamp=datetime.now(),
                    stream=stream_type,
                    content=content,
                )

                # Call callback if provided
                if callback:
                    callback(output_line)

                line_num += 1

            except Exception as e:
                # Log error but continue streaming
                if callback:
                    error_line = OutputLine(
                        id=f"out_{uuid.uuid4().hex[:8]}",
                        execution_id=execution_id,
                        timestamp=datetime.now(),
                        stream=StreamType.STDERR,
                        content=f"[ERROR] Failed to read output: {e}",
                    )
                    callback(error_line)

