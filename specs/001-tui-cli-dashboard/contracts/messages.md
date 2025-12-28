# Contract: Messages

**Layer**: Communication  
**Location**: `src/messages.py` (or within widget modules)

## Purpose

Textual uses message passing for component communication. These messages decouple the Runner layer from the UI layer (Constitution Principle I).

## Message Definitions

```python
from textual.message import Message
from src.models.command import Command
from src.models.execution import OutputLine, Execution, ExecutionStatus

class CommandSelected(Message):
    """User selected a command from the palette."""
    
    def __init__(self, command: Command) -> None:
        self.command = command
        super().__init__()

class ExecutionStarted(Message):
    """A command execution has begun."""
    
    def __init__(self, execution: Execution) -> None:
        self.execution = execution
        super().__init__()

class OutputReceived(Message):
    """A line of output was received from a running command."""
    
    def __init__(self, execution_id: str, line: OutputLine) -> None:
        self.execution_id = execution_id
        self.line = line
        super().__init__()

class ExecutionCompleted(Message):
    """A command execution has finished (success or failure)."""
    
    def __init__(self, execution: Execution) -> None:
        self.execution = execution
        super().__init__()

class ExecutionCancelled(Message):
    """A command execution was cancelled by the user."""
    
    def __init__(self, execution_id: str) -> None:
        self.execution_id = execution_id
        super().__init__()
```

## Message Flow

```
┌─────────────────┐                    ┌─────────────────┐
│ CommandPalette  │                    │   OutputView    │
│    (Widget)     │                    │    (Widget)     │
└────────┬────────┘                    └────────▲────────┘
         │                                      │
         │ CommandSelected                      │ OutputReceived
         ▼                                      │ ExecutionCompleted
┌─────────────────────────────────────────────────────────┐
│                       App                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Worker (async)                       │   │
│  │  ┌─────────────────┐    ┌──────────────────┐     │   │
│  │  │ CommandRunner   │───▶│ post_message()   │     │   │
│  │  └─────────────────┘    └──────────────────┘     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Handler Mapping

| Message | Handler Location | Action |
|---------|------------------|--------|
| `CommandSelected` | `App.on_command_selected` | Start worker to run command |
| `ExecutionStarted` | `OutputView.on_execution_started` | Clear view, show command name |
| `OutputReceived` | `OutputView.on_output_received` | Append line with appropriate styling |
| `ExecutionCompleted` | `OutputView.on_execution_completed` | Show success/failure indicator |

## Bubble Behavior

All messages bubble up to the App level by default. Widgets can handle them locally if needed (e.g., OutputView handles OutputReceived directly).
