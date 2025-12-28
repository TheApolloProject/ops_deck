# Research: TUI CLI Dashboard

**Feature**: 001-tui-cli-dashboard  
**Date**: 2025-12-28  
**Purpose**: Resolve technical unknowns and document best practices for implementation

## Research Tasks

Based on Technical Context, the following areas required research:

1. Textual worker pattern for background tasks
2. asyncio subprocess streaming (line-by-line output capture)
3. YAML configuration schema validation
4. Textual CSS layout patterns (sidebar + main content)
5. Separate stdout/stderr capture with asyncio

---

## 1. Textual Worker Pattern

**Decision**: Use `@work` decorator with `thread=False` for async workers

**Rationale**: Textual provides a built-in worker system that integrates with its message-passing architecture. Using `@work(thread=False)` runs the worker as an asyncio task, which is ideal for our async subprocess execution.

**Alternatives Considered**:
- `thread=True` workers: Rejected because asyncio subprocess already handles concurrency; threading adds complexity
- Manual asyncio.create_task: Rejected because Textual workers provide cancellation, progress tracking, and proper cleanup

**Pattern**:
```python
from textual.worker import Worker, get_current_worker

class App(textual.app.App):
    @work(exclusive=False)  # Allow multiple commands to run
    async def run_command(self, command: str) -> None:
        worker = get_current_worker()
        async for line in stream_subprocess(command):
            if worker.is_cancelled:
                break
            self.post_message(OutputLine(line))
```

**Source**: Textual documentation - Workers guide

---

## 2. Asyncio Subprocess Streaming

**Decision**: Use `asyncio.create_subprocess_shell` with `asyncio.StreamReader` for line-by-line capture

**Rationale**: This approach captures stdout and stderr separately as async streams, enabling real-time line-by-line updates to the UI without blocking.

**Alternatives Considered**:
- `subprocess.Popen` with threads: Rejected because it requires threading for non-blocking I/O
- `subprocess.run`: Rejected because it blocks until command completion
- Third-party libs (trio, anyio): Rejected per Constitution V (Simplicity) - asyncio stdlib is sufficient

**Pattern**:
```python
import asyncio
from dataclasses import dataclass
from typing import AsyncIterator

@dataclass
class OutputLine:
    text: str
    stream: str  # "stdout" or "stderr"

async def stream_command(cmd: str) -> AsyncIterator[OutputLine]:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    async def read_stream(stream, name: str):
        while True:
            line = await stream.readline()
            if not line:
                break
            yield OutputLine(line.decode().rstrip('\n'), name)
    
    # Interleave stdout and stderr
    async for line in merge_streams(
        read_stream(proc.stdout, "stdout"),
        read_stream(proc.stderr, "stderr")
    ):
        yield line
    
    await proc.wait()
    # Return exit code via separate mechanism
```

**Consideration**: Merging stdout/stderr while preserving order requires `asyncio.Queue` or similar pattern to interleave lines as they arrive.

---

## 3. YAML Configuration Schema

**Decision**: Use PyYAML with Pydantic for schema validation

**Rationale**: PyYAML handles parsing; Pydantic provides runtime validation with clear error messages. This ensures malformed configs fail fast with actionable errors (FR-009).

**Alternatives Considered**:
- YAML + manual validation: Rejected because error messages would be unclear
- JSON Schema: Rejected because YAML is more human-readable for config files
- TOML: Rejected because YAML is more common for this use case and already chosen per assumptions

**Schema Structure**:
```yaml
# commands.yaml
commands:
  - name: "Check Disk Space"
    command: "df -h"
    description: "Display disk usage in human-readable format"
  
  - name: "Git Status"
    command: "git status"
    description: "Show working tree status"
  
  - name: "Ping Server"
    command: "ping -c 4 google.com"
    description: "Test network connectivity"
```

**Pydantic Model**:
```python
from pydantic import BaseModel, Field
from typing import Optional

class CommandConfig(BaseModel):
    name: str = Field(..., min_length=1)
    command: str = Field(..., min_length=1)
    description: Optional[str] = None

class AppConfig(BaseModel):
    commands: list[CommandConfig] = Field(..., min_length=1)
```

---

## 4. Textual CSS Layout

**Decision**: Docked sidebar on left (fixed width), scrollable output view on right (flexible)

**Rationale**: Standard dashboard pattern. Textual CSS supports CSS Grid and docking, making this layout straightforward.

**Alternatives Considered**:
- Horizontal split (top/bottom): Rejected because sidebar is more conventional for command selection
- Tabs for commands: Rejected because sidebar provides always-visible command list

**Layout Pattern**:
```css
/* app.tcss */
Screen {
    layout: grid;
    grid-size: 2;
    grid-columns: 1fr 3fr;
}

#command-palette {
    dock: left;
    width: 25%;
    min-width: 20;
    max-width: 40;
    background: $surface;
    border-right: solid $primary;
}

#output-view {
    width: 100%;
    height: 100%;
    overflow-y: scroll;
}

.stdout {
    color: $text;
}

.stderr {
    color: $error;
}

.success-indicator {
    color: $success;
}

.error-indicator {
    color: $error;
}
```

---

## 5. Separate stdout/stderr Capture

**Decision**: Use two concurrent async readers with a shared queue for ordered output

**Rationale**: Reading stdout and stderr concurrently ensures neither blocks the other. A queue preserves arrival order for display.

**Pattern**:
```python
import asyncio
from asyncio import Queue

async def capture_output(proc) -> AsyncIterator[OutputLine]:
    queue: Queue[OutputLine | None] = Queue()
    
    async def reader(stream, name: str):
        while True:
            line = await stream.readline()
            if not line:
                break
            await queue.put(OutputLine(line.decode().rstrip(), name))
        await queue.put(None)  # Signal completion
    
    # Start both readers
    tasks = [
        asyncio.create_task(reader(proc.stdout, "stdout")),
        asyncio.create_task(reader(proc.stderr, "stderr")),
    ]
    
    completed = 0
    while completed < 2:
        item = await queue.get()
        if item is None:
            completed += 1
        else:
            yield item
    
    await asyncio.gather(*tasks)
```

---

## Summary

All technical unknowns resolved:

| Topic | Decision | Key Insight |
|-------|----------|-------------|
| Textual workers | `@work(exclusive=False)` | Allows parallel command execution |
| Subprocess streaming | `asyncio.create_subprocess_shell` + StreamReader | Native async, no threads needed |
| Config validation | PyYAML + Pydantic | Clear error messages on invalid config |
| Layout | Grid layout with docked sidebar | Standard dashboard pattern |
| stdout/stderr | Concurrent readers with Queue | Preserves line arrival order |

**Ready for Phase 1**: Data model and contracts design.
