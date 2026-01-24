# Research Report: TUI Interactive Shell Support

**Feature**: 002-tui-interactive-shell  
**Date**: 2026-01-24  
**Status**: Complete

## Executive Summary

This research resolves all technical unknowns for implementing interactive shell/editor support in the ops deck TUI. Key decisions:
- **PTY Library**: Use `pexpect` for subprocess management
- **Textual Suspension**: Use built-in `app.suspend()` and `app.resume()` methods
- **Terminal State**: Textual handles restoration automatically
- **Signal Forwarding**: Combine pexpect's `interact()` with proper subprocess stdin/stdout inheritance
- **Nested Instance Detection**: Use environment variable flag

---

## Research Findings

### 1. PTY Library Selection

**Decision**: Use **pexpect 4.8+**

**Rationale**:
- **Async compatibility**: Works with asyncio via `run_in_executor()` or direct subprocess integration
- **Production-proven**: Used by Ansible, salt-ssh for interactive SSH sessions
- **Signal handling**: Native support for Ctrl+C, Ctrl+Z, Ctrl+D forwarding to child processes
- **Terminal restoration**: Automatic cleanup via `interact()` method
- **Active maintenance**: Regular updates and security patches
- **Clear API**: Well-documented suspend/resume patterns

**Alternatives Considered**:

| Library | Rejected Because |
|---------|------------------|
| **stdlib pty** | Fully synchronous, no signal forwarding, manual terminal restoration required |
| **python-pty** | Unmaintained since 2018, minimal documentation, small user base, security risk |

**Implementation Notes**:
```python
# Add to pyproject.toml dependencies
"pexpect>=4.8.0",

# Usage pattern:
import pexpect
child = pexpect.spawn("vim file.txt", timeout=None)
child.interact()  # Hands off TTY control, auto-restores on exit
exit_code = child.exitstatus
```

---

### 2. Textual Suspension API

**Decision**: Use Textual's built-in **`app.suspend()` and `app.resume()` methods**

**Rationale**:
- Textual provides first-class support for suspending the TUI to yield TTY control
- `suspend()` restores terminal to normal mode (cooked mode, shows cursor)
- `resume()` re-enters Textual's raw mode and re-renders the UI
- No manual terminal state capture needed (colors, cursor position, screen buffer handled automatically)

**Alternatives Considered**:

| Approach | Rejected Because |
|----------|------------------|
| **Manual termios save/restore** | Redundant with Textual's built-in methods; error-prone |
| **Run in separate terminal emulator** | Breaks seamless UX; adds complexity |

**Implementation Notes**:
```python
from textual.app import App
import subprocess

class OpsDeckApp(App):
    async def action_launch_vim(self) -> None:
        """Launch vim with full TTY control."""
        self.suspend()  # Restore terminal to normal mode
        try:
            # External process inherits TTY when stdin/stdout=None
            process = await asyncio.create_subprocess_shell(
                "vim file.txt",
                stdin=None,
                stdout=None,
                stderr=None
            )
            await process.wait()
        finally:
            self.resume()  # Re-enter Textual raw mode
```

**Key Finding**: Setting `stdin=None, stdout=None, stderr=None` in `create_subprocess_shell` makes the subprocess inherit the parent's TTY directly. This is more reliable than pexpect for simple cases.

---

### 3. Terminal State Management

**Decision**: Rely on **Textual's automatic terminal restoration** via `suspend()`/`resume()`

**Rationale**:
- Textual internally uses `tcgetattr`/`tcsetattr` to save/restore termios settings
- Cursor position and screen buffer are managed by the framework
- Manual state capture only needed for edge cases (interactive process crashes before cleanup)

**Alternatives Considered**:

| Approach | Rejected Because |
|----------|------------------|
| **Manual termios capture** | Duplicate of Textual's internal logic; maintenance burden |
| **Screen buffer snapshots** | Complex, unnecessary for TTY handoff pattern |

**Implementation Notes**:
```python
# Textual handles this automatically:
self.suspend()   # Saves: termios attrs, cursor pos, screen state
# ... external process runs ...
self.resume()    # Restores: raw mode, cursor, redraws widgets

# Edge case handling (if external process crashes):
import os
finally:
    os.system("reset")  # Nuclear option: full terminal reset
    self.resume()
```

---

### 4. Signal Handling Strategy

**Decision**: Use **`subprocess.create_subprocess_shell` with stdin/stdout inheritance + process group management**

**Rationale**:
- When subprocess inherits TTY (`stdin=None`), signals are automatically delivered to the foreground process group
- No custom signal routing needed for Ctrl+C, Ctrl+Z, Ctrl+D
- Parent TUI process is suspended (`suspend()` called), so signals go to child
- On subprocess exit, `resume()` restores TUI signal handlers

**Alternatives Considered**:

| Approach | Rejected Because |
|----------|------------------|
| **pexpect.interact()** | Heavier than subprocess for simple TTY handoff; adds dependency complexity |
| **Manual signal forwarding** | Error-prone; subprocess.create_subprocess handles this natively |

**Implementation Notes**:
```python
# Signal flow:
# 1. User presses Ctrl+C while vim is running
# 2. SIGINT goes to foreground process group (vim's process)
# 3. vim handles SIGINT (interrupt current operation)
# 4. On vim exit, TUI resumes and gets new foreground group

# No manual signal routing needed!
process = await asyncio.create_subprocess_shell(
    cmd,
    stdin=None,  # Inherits TTY, becomes foreground process
    stdout=None,
    stderr=None
)
await process.wait()  # TUI blocked until child exits
```

**Edge Case Handling**:
- **Multiple Ctrl+C presses**: Subprocess exits, TUI resumes normally
- **Ctrl+Z (suspend)**: Child process is stopped, TUI remains suspended until `fg` or `kill`
- **Unresponsive subprocess**: User must kill from another terminal (expected behavior)

---

### 5. Nested Instance Detection

**Decision**: Use **environment variable flag `OPS_DECK_ACTIVE=1`**

**Rationale**:
- Simple, reliable, no process tree inspection needed
- Set `OPS_DECK_ACTIVE=1` before spawning interactive sessions
- Check for flag in ops-deck startup code; exit with error if detected
- Prevents recursive TUI launches that would break terminal state

**Alternatives Considered**:

| Approach | Rejected Because |
|----------|------------------|
| **Process tree inspection** | Race conditions; complex; platform-dependent |
| **Command string parsing** | Fragile (aliases, symlinks, relative paths) |
| **PID file locking** | Doesn't prevent nested sessions (only concurrent instances) |

**Implementation Notes**:
```python
# In src/app.py (entry point):
if os.environ.get("OPS_DECK_ACTIVE") == "1":
    print("Error: Cannot run ops-deck within an ops-deck session.", file=sys.stderr)
    print("Exit the current session first.", file=sys.stderr)
    sys.exit(1)

# Set flag when spawning interactive sessions:
env = os.environ.copy()
env["OPS_DECK_ACTIVE"] = "1"

process = await asyncio.create_subprocess_shell(
    cmd,
    stdin=None,
    stdout=None,
    stderr=None,
    env=env  # Child inherits flag
)
```

---

## Summary of Technology Decisions

| Technical Area | Decision | Rationale |
|----------------|----------|-----------|
| **PTY Library** | pexpect 4.8+ | Production-proven, async-compatible, automatic terminal restoration |
| **Textual API** | `app.suspend()` / `app.resume()` | Built-in support, automatic terminal state management |
| **Signal Forwarding** | subprocess stdin inheritance | Native OS-level signal delivery, no custom routing needed |
| **Nested Detection** | Environment variable `OPS_DECK_ACTIVE=1` | Simple, reliable, platform-independent |
| **Error Logging** | Log only errors/exceptions (not full I/O) | Balances debuggability with minimal overhead (per spec) |

---

## Implementation Recommendations

### Phase 1 Design Priorities

1. **Create `models/interactive.py`**:
   - `InteractiveSession` model (command, PID, exit_code, start_time, end_time)
   - `SessionType` enum (SHELL, EDITOR, MULTIPLEXER)

2. **Create `services/interactive_runner.py`**:
   - `InteractiveRunner.run_session(command, app) -> InteractiveSession`
   - Handle suspend/resume lifecycle
   - Log errors only (per spec clarification Q1)
   - Set `OPS_DECK_ACTIVE` environment variable

3. **Extend `commands.yaml`**:
   - Add `interactive: true` field to command definition
   - Example: `{name: "Edit Config", command: "vim config.yaml", interactive: true}`

4. **Update `widgets/app.py`**:
   - Detect interactive commands in command selection handler
   - Route to `InteractiveRunner` instead of `AsyncCommandRunner`
   - Display exit code after interactive session ends

### Testing Strategy

```python
# Unit tests (src/tests/unit/test_interactive_runner.py):
- Test suspend/resume called in correct order
- Test environment variable set correctly
- Test exit code capture
- Test error logging (not full I/O logging)

# Integration tests (src/tests/integration/test_interactive_flow.py):
- Mock vim with `sleep 1 && echo "done"` (non-interactive test mode)
- Verify terminal restoration after subprocess exit
- Test Ctrl+C handling (send SIGINT to subprocess)
```

---

## Open Questions Resolved

All technical unknowns from plan.md Phase 0 section are now resolved:

1. ✅ **PTY Library**: pexpect
2. ✅ **Terminal State**: Textual `suspend()`/`resume()`
3. ✅ **Signal Forwarding**: subprocess stdin inheritance
4. ✅ **Textual Suspension API**: `app.suspend()` and `app.resume()`
5. ✅ **Nested TUI Detection**: `OPS_DECK_ACTIVE` environment variable

**Ready for Phase 1**: Design artifacts (data-model.md, contracts/, quickstart.md)
