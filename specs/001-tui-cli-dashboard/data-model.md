# Data Model: TUI CLI Dashboard

**Feature**: 001-tui-cli-dashboard  
**Date**: 2025-12-28  
**Source**: [spec.md](spec.md) Key Entities section

## Entities

### Command

A predefined operation the user can execute from the command palette.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Display label shown in command palette |
| command | string | Yes | Shell command string to execute |
| description | string | No | Help text shown alongside the command |

**Validation Rules**:
- `name` must be non-empty, max 50 characters
- `command` must be non-empty
- `description` max 200 characters if provided

**Source**: Configuration file (loaded at startup)

---

### Execution

A running or completed instance of a Command.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Unique identifier for this execution |
| command | Command | Yes | Reference to the executed Command |
| status | ExecutionStatus | Yes | Current state of the execution |
| start_time | datetime | Yes | When execution began |
| end_time | datetime | No | When execution completed (None if running) |
| exit_code | int | No | Process exit code (None if running) |
| output_lines | list[OutputLine] | Yes | Captured output in order of arrival |

**State Transitions**:
```
PENDING → RUNNING → COMPLETED
                  → FAILED
                  → CANCELLED
```

| Status | Description |
|--------|-------------|
| PENDING | Created but not yet started |
| RUNNING | Subprocess is executing |
| COMPLETED | Finished with exit code 0 |
| FAILED | Finished with non-zero exit code |
| CANCELLED | Terminated by user action |

**Derived Properties**:
- `duration`: `end_time - start_time` (None if running)
- `is_success`: `exit_code == 0`
- `is_running`: `status == RUNNING`

---

### OutputLine

A single line of output from a command execution.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | Yes | The line content (stripped of trailing newline) |
| stream | StreamType | Yes | Which stream this line came from |
| timestamp | datetime | Yes | When this line was captured |

**StreamType Enum**:
| Value | Description |
|-------|-------------|
| STDOUT | Standard output stream |
| STDERR | Standard error stream |

---

### AppConfig

Top-level configuration loaded from YAML file.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| commands | list[Command] | Yes | List of available commands |

**Validation Rules**:
- `commands` must contain at least one Command
- All Command entries must pass individual validation

---

## Entity Relationships

```
┌─────────────┐
│  AppConfig  │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐      1:N      ┌─────────────┐
│   Command   │◄──────────────│  Execution  │
└─────────────┘               └──────┬──────┘
                                     │ 1:N
                                     ▼
                              ┌─────────────┐
                              │ OutputLine  │
                              └─────────────┘
```

- **AppConfig → Command**: One config contains many commands (1:N)
- **Command → Execution**: One command can have many executions over time (1:N)
- **Execution → OutputLine**: One execution produces many output lines (1:N, ordered)

---

## Storage Notes

Per spec assumptions:
- **Commands**: Loaded from YAML file at startup; read-only during runtime
- **Executions**: In-memory only; not persisted across sessions
- **OutputLines**: In-memory, attached to parent Execution; may be trimmed if >10,000 lines

No database required. All state is ephemeral except the configuration file.
