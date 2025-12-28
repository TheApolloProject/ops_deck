# Contract: CommandRunner

**Layer**: Runner (Service)  
**Location**: `src/services/runner.py`

## Interface

```python
from typing import AsyncIterator
from src.models.command import Command
from src.models.execution import Execution, OutputLine

class CommandRunner:
    """Execute shell commands asynchronously with streaming output."""
    
    async def run(self, command: Command) -> AsyncIterator[OutputLine]:
        """
        Execute a command and stream output lines as they arrive.
        
        Args:
            command: The Command to execute
            
        Yields:
            OutputLine objects as stdout/stderr lines are received
            
        Note:
            The final item yielded will have is_complete=True
            and include the exit_code
        """
        ...
    
    async def run_with_execution(self, command: Command) -> tuple[Execution, AsyncIterator[OutputLine]]:
        """
        Execute a command and return both the Execution tracker and output stream.
        
        Args:
            command: The Command to execute
            
        Returns:
            Tuple of (Execution, AsyncIterator[OutputLine])
            - Execution object is updated as command runs
            - Iterator yields output lines
        """
        ...
    
    async def cancel(self, execution: Execution) -> bool:
        """
        Cancel a running execution.
        
        Args:
            execution: The Execution to cancel
            
        Returns:
            True if cancelled successfully, False if already completed
        """
        ...
```

## Output Protocol

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class StreamType(Enum):
    STDOUT = "stdout"
    STDERR = "stderr"

@dataclass
class OutputLine:
    text: str
    stream: StreamType
    timestamp: datetime
    
@dataclass
class ExecutionResult:
    exit_code: int
    duration_seconds: float
```

## Behavior Contracts

| Scenario | Expected Behavior |
|----------|-------------------|
| Command produces stdout | Yields OutputLine with stream=STDOUT |
| Command produces stderr | Yields OutputLine with stream=STDERR |
| Command completes with exit 0 | Execution.status = COMPLETED |
| Command completes with non-zero exit | Execution.status = FAILED |
| Command not found (bad shell command) | stderr contains shell error, exit_code != 0 |
| Cancel called on running command | Process terminated, Execution.status = CANCELLED |
| Cancel called on completed command | Returns False, no effect |
| Output interleaved stdout/stderr | Lines yielded in arrival order (not grouped by stream) |

## Concurrency Guarantees

- Multiple `run()` calls may execute concurrently (Constitution II: parallel execution allowed)
- Each `run()` is independent; cancelling one does not affect others
- Output lines are yielded in order of arrival from the subprocess
- No global state; runner is stateless between calls

## Usage Example

```python
runner = CommandRunner()
command = Command(name="Disk", command="df -h", description=None)

async for line in runner.run(command):
    if line.stream == StreamType.STDERR:
        print(f"[ERROR] {line.text}")
    else:
        print(line.text)
```

## Integration with Textual

The runner should be called from a Textual worker:

```python
@work(exclusive=False)
async def execute_command(self, command: Command) -> None:
    runner = CommandRunner()
    async for line in runner.run(command):
        self.post_message(OutputReceived(line))
```
