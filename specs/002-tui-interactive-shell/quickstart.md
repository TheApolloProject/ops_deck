# Quickstart Guide: Interactive Shell Commands

**Feature**: 002-tui-interactive-shell  
**For**: Developers implementing this feature  
**Date**: 2026-01-24

## Overview

This guide helps you implement interactive shell command support in ops deck. After following this guide, users will be able to launch vim, bash, and other interactive tools directly from the TUI.

---

## Prerequisites

1. **Existing ops deck codebase** with:
   - Python 3.10+
   - Textual 0.30+ installed
   - Existing `AsyncCommandRunner` service
   - Command palette UI working

2. **Read first**:
   - `research.md` - Technical decisions and rationale
   - `data-model.md` - Data structures
   - `contracts/service-api.md` - Service interfaces

---

## Implementation Steps

### Step 1: Add pexpect Dependency (Optional)

**Note**: Research recommends `pexpect`, but `subprocess` with stdin inheritance works for simple cases. Start with subprocess, add pexpect if needed.

```bash
# If using pexpect (optional):
# Add to pyproject.toml dependencies:
"pexpect>=4.8.0",

# Then install:
pip install -e ".[dev]"
```

---

### Step 2: Create InteractiveSession Model

**File**: `src/models/interactive.py`

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

class SessionType(str, Enum):
    SHELL = "shell"
    EDITOR = "editor"
    MULTIPLEXER = "multiplexer"
    OTHER = "other"

@dataclass
class InteractiveSession:
    """Represents an interactive subprocess session with TTY control."""
    session_id: str = field(default_factory=lambda: str(uuid4()))
    command: str = ""
    session_type: SessionType = SessionType.OTHER
    pid: int | None = None
    exit_code: int | None = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    working_directory: str = ""
    environment_snapshot: dict[str, str] = field(default_factory=dict)
    error_log: list[str] = field(default_factory=list)
    logging_enabled: bool = False
    log_file_path: str | None = None

    @property
    def duration(self) -> float | None:
        """Duration in seconds, or None if still running."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds()
```

---

### Step 3: Extend Command Model

**File**: `src/models/command.py`

Add two fields to existing `Command` dataclass:

```python
from dataclasses import dataclass
from models.interactive import SessionType

@dataclass
class Command:
    name: str
    command: str
    description: str = ""
    interactive: bool = False  # NEW
    session_type: SessionType | None = None  # NEW
```

---

### Step 4: Create InteractiveRunner Service

**File**: `src/services/interactive_runner.py`

```python
import asyncio
import os
from datetime import datetime
from textual.app import App

from models.command import Command
from models.interactive import InteractiveSession, SessionType

class InteractiveRunner:
    """Manages interactive subprocess sessions with TTY control."""
    
    def __init__(self):
        self._active_sessions: list[InteractiveSession] = []
    
    async def run_session(
        self,
        command: Command,
        app: App,
        logging_enabled: bool = False,
        log_file_path: str | None = None
    ) -> InteractiveSession:
        """Launch interactive session, suspend TUI, restore on exit."""
        
        # Validation
        if not command.interactive:
            raise ValueError(f"Command '{command.name}' is not marked as interactive")
        
        # Create session
        session = InteractiveSession(
            command=command.command,
            session_type=command.session_type or SessionType.OTHER,
            start_time=datetime.now(),
            working_directory=os.getcwd(),
            environment_snapshot=dict(os.environ),
            logging_enabled=logging_enabled,
            log_file_path=log_file_path
        )
        
        # Suspend TUI
        app.suspend()
        
        try:
            # Set environment flag to block nested instances
            env = os.environ.copy()
            env["OPS_DECK_ACTIVE"] = "1"
            
            # Launch subprocess with TTY inheritance
            process = await asyncio.create_subprocess_shell(
                session.command,
                stdin=None,   # Inherit parent TTY
                stdout=None,
                stderr=None,
                env=env
            )
            
            session.pid = process.pid
            self._active_sessions.append(session)
            
            # Wait for subprocess to exit
            exit_code = await process.wait()
            session.exit_code = exit_code
            
        except Exception as e:
            session.error_log.append(f"[ERROR] {type(e).__name__}: {str(e)}")
            session.exit_code = -1
        
        finally:
            # Always restore TUI
            app.resume()
            session.end_time = datetime.now()
            if session in self._active_sessions:
                self._active_sessions.remove(session)
        
        return session
    
    @staticmethod
    def detect_nested_instance() -> bool:
        """Check if ops-deck is already running."""
        return os.environ.get("OPS_DECK_ACTIVE") == "1"
    
    def get_active_sessions(self) -> list[InteractiveSession]:
        """Get currently running sessions."""
        return self._active_sessions.copy()
```

---

### Step 5: Update Command Configuration Loader

**File**: `src/services/config.py`

Extend YAML parsing to handle `interactive` and `session_type` fields:

```python
def load_commands_from_yaml(file_path: str) -> list[Command]:
    """Load commands from YAML, including interactive flag."""
    with open(file_path) as f:
        data = yaml.safe_load(f)
    
    commands = []
    for item in data.get("commands", []):
        cmd = Command(
            name=item["name"],
            command=item["command"],
            description=item.get("description", ""),
            interactive=item.get("interactive", False),  # NEW
            session_type=SessionType(item["session_type"]) if "session_type" in item else None  # NEW
        )
        commands.append(cmd)
    
    return commands
```

---

### Step 6: Update App to Route Interactive Commands

**File**: `src/widgets/app.py` (or wherever command execution happens)

```python
from services.interactive_runner import InteractiveRunner

class OpsDeckApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interactive_runner = InteractiveRunner()
    
    async def on_command_selected(self, command: Command) -> None:
        """Route command to appropriate runner."""
        if command.interactive:
            # Interactive path: suspend TUI, run subprocess
            session = await self.interactive_runner.run_session(command, self)
            self._display_interactive_result(session)
        else:
            # Existing async path
            execution = await self.async_runner.run_command(command)
            self._display_async_result(execution)
    
    def _display_interactive_result(self, session: InteractiveSession) -> None:
        """Show result of interactive session."""
        if session.exit_code == 0:
            self.notify(f"'{session.command}' completed successfully")
        else:
            self.notify(
                f"'{session.command}' exited with code {session.exit_code}",
                severity="error"
            )
            for error in session.error_log:
                self.log(error)
```

---

### Step 7: Block Nested Instances at Startup

**File**: `src/app.py` (entry point)

```python
from services.interactive_runner import InteractiveRunner
import sys

def main():
    # Block nested TUI instances
    if InteractiveRunner.detect_nested_instance():
        print("Error: Cannot run ops-deck within an ops-deck session.", file=sys.stderr)
        print("Exit the current session first.", file=sys.stderr)
        sys.exit(1)
    
    # Normal startup
    app = OpsDeckApp()
    app.run()

if __name__ == "__main__":
    main()
```

---

### Step 8: Update commands.yaml

Add interactive commands to your configuration:

```yaml
commands:
  - name: "Edit Config"
    command: "vim config.yaml"
    description: "Edit configuration file"
    interactive: true
    session_type: editor

  - name: "Open Shell"
    command: "bash"
    description: "Interactive bash shell"
    interactive: true
    session_type: shell

  - name: "Check Disk"
    command: "df -h"
    description: "Show disk usage"
    # interactive: false (default)
```

---

## Testing

### Manual Test 1: Launch vim

```bash
ops-deck
# Select "Edit Config" from palette
# vim should open in full screen
# Edit file, save with :wq
# TUI should restore cleanly
```

### Manual Test 2: Launch shell

```bash
ops-deck
# Select "Open Shell"
# bash prompt should appear
# Run: ls, pwd, echo "test"
# Type: exit
# TUI should restore
```

### Manual Test 3: Block nested instance

```bash
ops-deck
# Select "Open Shell"
# In bash, try to run: ops-deck
# Should see error: "Cannot run ops-deck within an ops-deck session"
```

---

## Troubleshooting

### Problem: TUI doesn't restore after vim exit

**Solution**: Check that `app.resume()` is in `finally` block. Try adding:
```python
finally:
    os.system("reset")  # Nuclear option
    app.resume()
```

### Problem: Keyboard input doesn't work in vim

**Solution**: Ensure subprocess stdin is `None` (not PIPE):
```python
stdin=None,  # NOT stdin=asyncio.subprocess.PIPE
```

### Problem: Ctrl+C kills the TUI

**Solution**: Signals are being forwarded correctly. Ctrl+C should go to the subprocess. If TUI crashes, check that `app.suspend()` is called before subprocess launch.

---

## Next Steps

1. ✅ Implement steps 1-8 above
2. Test with vim, nano, bash
3. Add unit tests (see `contracts/service-api.md`)
4. Consider adding session history UI (optional)
5. Document for end users

---

## Key Takeaways

- **Suspend/Resume**: `app.suspend()` before subprocess, `app.resume()` in finally block
- **TTY Inheritance**: `stdin=None, stdout=None, stderr=None` gives subprocess full TTY control
- **Nested Detection**: Set `OPS_DECK_ACTIVE=1` env var, check at startup
- **Signal Handling**: Works automatically when subprocess inherits TTY

---

## Reference

- Research: [research.md](./research.md)
- Data Model: [data-model.md](./data-model.md)
- API Contracts: [contracts/service-api.md](./contracts/service-api.md)
