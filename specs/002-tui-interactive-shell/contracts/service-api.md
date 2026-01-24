# Service Contracts: Interactive Session Management

**Feature**: 002-tui-interactive-shell  
**Date**: 2026-01-24  
**Type**: Internal Python API (not REST/GraphQL)

## Overview

This document defines the service contracts for managing interactive shell sessions in the ops deck TUI. Since this is a local TUI application (not a web service), these are Python class interfaces rather than REST/GraphQL APIs.

---

## InteractiveRunner Service

### Class: `InteractiveRunner`

**Module**: `src/services/interactive_runner.py`

**Purpose**: Manage lifecycle of interactive subprocess sessions with TTY control.

---

### Method: `run_session`

Launch an interactive session, suspend the TUI, and restore it on exit.

**Signature**:
```python
async def run_session(
    self,
    command: Command,
    app: App,
    logging_enabled: bool = False,
    log_file_path: str | None = None
) -> InteractiveSession
```

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `command` | `Command` | Yes | Command definition with `interactive=True` |
| `app` | `App` | Yes | Textual App instance for suspend/resume |
| `logging_enabled` | `bool` | No | Enable full I/O logging (default: False) |
| `log_file_path` | `str \| None` | No | Path to write session log |

**Returns**: `InteractiveSession` with exit_code, end_time, error_log populated

**Raises**:
- `ValueError`: If `command.interactive != True`
- `FileNotFoundError`: If log_file_path directory doesn't exist
- `RuntimeError`: If subprocess fails or terminal restoration fails

---

## YAML Configuration Schema

```yaml
commands:
  - name: string              # Display name
    command: string           # Shell command
    description: string       # Optional description
    interactive: boolean      # NEW: Requires TTY (default: false)
    session_type: string      # NEW: shell|editor|multiplexer|other
```

---

## Error Handling

| Scenario | Exception | Handling |
|----------|-----------|----------|
| Nested TUI detected | `RuntimeError` | Block launch |
| Subprocess fails | `OSError` | Log error, restore TUI |
| Terminal restoration fails | `RuntimeError` | Force `reset` |

---

## Performance Targets

- TUI Suspension: <100ms
- TUI Resumption: <100ms
- Subprocess Launch: <500ms
