# Implementation Plan: TUI with Interactive Shell Commands

**Branch**: `002-tui-interactive-shell` | **Date**: 2026-01-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-tui-interactive-shell/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enable ops deck TUI to launch and manage interactive shell commands (vim, nano, bash, zsh, tmux) while maintaining responsive UI and command palette functionality. The system will use PTY (pseudo-terminal) allocation to give interactive processes full TTY control, then restore TUI state when sessions exit. Approach involves subprocess management with PTY, terminal state capture/restore, and signal handling for keyboard events.

## Technical Context

**Language/Version**: Python 3.10+ (project uses 3.10 minimum, runtime is 3.12)
**Primary Dependencies**: Textual 0.30+, asyncio (stdlib), pexpect or pty module (NEEDS CLARIFICATION: which PTY library?)
**Storage**: N/A (no persistence for this feature)
**Testing**: pytest with pytest-asyncio for async tests
**Target Platform**: Unix-like systems (Linux, macOS) with TTY support
**Project Type**: Single project (TUI application)
**Performance Goals**: TTY handoff <100ms, terminal restoration <50ms, zero UI freezing during interactive sessions
**Constraints**: Must maintain UI responsiveness during interactive sessions, clean terminal restoration 100% of time
**Scale/Scope**: Single-user TUI, supports concurrent interactive sessions (shell + tmux), handles editors with complex keybindings

## Key Technical Unknowns (Phase 0 Research)

1. **PTY Library Selection**: Should we use `pexpect`, stdlib `pty`, or `python-pty` for pseudo-terminal management?
2. **Terminal State Capture**: How to capture and restore terminal state (termios settings, cursor position, colors) across Textual suspension?
3. **Textual Suspension API**: Does Textual provide native suspend/resume for external TTY processes, or manual implementation needed?
4. **Signal Forwarding**: How to properly forward Ctrl+C, Ctrl+Z, Ctrl+D to child processes while preventing TUI interruption?
5. **Nested TUI Detection**: How to detect if an interactive command is attempting to launch another ops-deck instance (for blocking)?

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Before Phase 0)

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Separation of Concerns** | ✅ PASS | Interactive session management will live in `services/` layer; UI widgets delegate to service; command config remains in YAML |
| **II. Non-Blocking Async-First** | ⚠️ CONDITIONAL | Interactive sessions require blocking TUI while subprocess owns TTY; this is acceptable because users explicitly request TTY handoff. Non-interactive commands remain async. |
| **III. Observable Output Streams** | ✅ PASS | Error logging for interactive sessions aligns with stderr visibility principle; exit codes will be captured and displayed |
| **IV. Configuration-Driven Commands** | ✅ PASS | Interactive commands will be added to existing `commands.yaml`; no hardcoding of editors/shells |
| **V. Simplicity & YAGNI** | ✅ PASS | Feature directly supports user stories in spec; no speculative abstractions planned |

### Post-Phase 1 Re-evaluation

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Separation of Concerns** | ✅ PASS | Design maintains clean layers: `InteractiveSession` model, `InteractiveRunner` service, command routing in app layer. YAML config extended without breaking changes. |
| **II. Non-Blocking Async-First** | ✅ CONDITIONAL PASS | Conditional violation justified: interactive tools require exclusive TTY control by design. TUI suspension is intentional and user-initiated. Non-interactive commands unaffected. |
| **III. Observable Output Streams** | ✅ PASS | Exit codes captured, error_log populated, session metadata tracked. Aligns with observability principle for interactive sessions. |
| **IV. Configuration-Driven Commands** | ✅ PASS | Extended YAML schema (`interactive: true`, `session_type`) maintains configuration-driven approach. Auto-detection fallback for session_type. |
| **V. Simplicity & YAGNI** | ✅ PASS | Design uses stdlib subprocess + Textual's built-in suspend/resume. No over-engineering. pexpect added only if needed (optional). |

**Final Gate Result**: ✅ **PASS** (with justified conditional on Principle II)

### Conditional Pass Justification (Principle II)

**Violation**: Interactive sessions block the TUI event loop while subprocess owns TTY (cannot scroll, click, or cancel during vim session).

**Why Needed**: Interactive tools like vim require exclusive TTY control and raw keyboard input. Textual cannot render widgets while the terminal is in raw mode controlled by an external process. This is the expected behavior for full-screen interactive tools.

**Simpler Alternative Rejected**: Running interactive sessions in a tmux pane or subprocess terminal emulator would add significant complexity and break the seamless user experience. The blocking behavior is intentional and user-initiated.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

## Project Structure

### Documentation (this feature)

```text
specs/002-tui-interactive-shell/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   ├── command.py         # Existing: Command model
│   ├── execution.py       # Existing: Execution tracking
│   ├── output.py          # Existing: Output capture
│   └── interactive.py     # NEW: Interactive session model
│
├── services/
│   ├── __init__.py
│   ├── config.py          # Existing: Config loader
│   ├── command_runner.py  # Existing: Async command execution
│   └── interactive_runner.py  # NEW: PTY session manager
│
├── widgets/
│   ├── __init__.py
│   ├── app.py             # Existing: Main TUI app
│   ├── command_list.py    # Existing: Command palette
│   ├── output_pane.py     # Existing: Output display
│   └── interactive_shell.py  # NEW: Interactive session widget (optional)
│
└── app.py                 # Existing: Entry point

tests/
├── unit/
│   ├── test_interactive_runner.py  # NEW: PTY manager tests
│   └── test_models.py              # Existing: Model tests
│
└── integration/
    └── test_interactive_flow.py    # NEW: End-to-end interactive tests
```

**Structure Decision**: Single project structure maintained. Interactive session management follows existing patterns: model in `models/`, business logic in `services/`, UI delegation in `widgets/`. No new top-level directories needed.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle II: Blocking TUI during interactive sessions | Interactive tools (vim, nano) require exclusive TTY control and raw keyboard input; TUI cannot render while terminal is owned by subprocess | Running in tmux pane or terminal emulator adds complexity, breaks seamless UX, and defeats purpose of integrated TUI experience |

## Phase 0: Research & Technical Decisions

### Research Tasks

The following technical unknowns must be resolved before design phase:

1. **PTY Library Evaluation**
   - Evaluate: stdlib `pty`, `pexpect`, `python-pty`
   - Criteria: async compatibility, termios control, signal forwarding
   - Decision needed: Which library provides best control for Textual integration?

2. **Textual Suspension Patterns**
   - Research: Does Textual have native suspend/resume API?
   - Investigate: Context managers, async context, or manual terminal restoration
   - Decision needed: Pattern for yielding TTY control to subprocess

3. **Terminal State Management**
   - Research: Capture termios settings, cursor position, screen buffer
   - Investigate: `termios` module, `curses` integration, ANSI escape sequences
   - Decision needed: State capture strategy before PTY handoff

4. **Signal Handling Strategy**
   - Research: Forward signals (SIGINT, SIGTSTP, SIGQUIT) to child process
   - Investigate: Process group management, signal masking during interactive session
   - Decision needed: Signal routing to prevent TUI crash while preserving child control

5. **Nested Instance Detection**
   - Research: Detect `ops-deck` process in subprocess command string
   - Investigate: Environment variable flags, process tree inspection
   - Decision needed: Method to block recursive TUI launches

### Research Output

✅ **COMPLETE** - See [research.md](./research.md)

**Key Decisions**:
- PTY Library: Use `pexpect` (optional) or stdlib subprocess with stdin inheritance
- Textual API: Use built-in `app.suspend()` and `app.resume()`
- Terminal State: Automatic restoration via Textual
- Signal Handling: Native OS forwarding via TTY inheritance
- Nested Detection: `OPS_DECK_ACTIVE=1` environment variable

---

## Phase 1: Design & Contracts

### Design Artifacts

✅ **COMPLETE** - All design documents generated

**Artifacts Created**:

1. **[data-model.md](./data-model.md)** - Data structures
   - `InteractiveSession` model with lifecycle tracking
   - `SessionType` enum for categorization
   - Extended `Command` model with `interactive` field

2. **[contracts/service-api.md](./contracts/service-api.md)** - Service interfaces
   - `InteractiveRunner.run_session()` API
   - YAML configuration schema extension
   - Error handling contracts
   - Performance targets

3. **[quickstart.md](./quickstart.md)** - Implementation guide
   - Step-by-step implementation instructions
   - Code examples and snippets
   - Testing procedures
   - Troubleshooting guide

### Agent Context Update

✅ **COMPLETE** - GitHub Copilot context updated

- Added Python 3.10+ language information
- Added project type (Single project TUI)
- Updated `.github/agents/copilot-instructions.md`

---

## Phase 2: Task Breakdown

**Status**: ⏳ **READY FOR `/speckit.tasks` COMMAND**

The planning phase is complete. All design artifacts are ready. Next step:

```bash
/speckit.tasks
```

This will generate `tasks.md` with detailed implementation tasks based on the design artifacts above.
