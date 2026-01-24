# Implementation Plan: Dual-Mode Terminal Integration

**Branch**: `002-tui-interactive-shell` | **Date**: 2026-01-24 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-tui-interactive-shell/spec.md`

**Note**: This is an enhanced plan for Option B: Dual-Mode terminal support

## Summary

This feature adds **dual-mode terminal support** to the ops deck TUI:

1. **Native Mode** (suspend/resume): For complex interactive tools (vim, tmux, nano) that require full terminal control - suspends the TUI, hands off the terminal to the native process, then resumes when complete
2. **Embedded Mode** (in-pane): For simple shell commands and live output viewing - runs commands in an embedded terminal emulator within the output pane using `textual-terminal`

This hybrid approach provides the best of both worlds: reliable full-featured editors via native mode, and convenient in-pane command execution via embedded mode. Users can specify which mode to use per command via the `mode` field in commands.yaml.

## Technical Context

**Language/Version**: Python 3.10+ (currently 3.12.3)
**Primary Dependencies**: 
- Textual 6.11.0 (TUI framework)
- textual-terminal 0.3.0 (embedded terminal emulator)
- pyte (Linux terminal emulator, dependency of textual-terminal)
- asyncio (stdlib - subprocess management)
- PyYAML (config parsing)

**Storage**: File-based (commands.yaml, optional session logs)
**Testing**: pytest with pytest-asyncio for async tests
**Target Platform**: Linux primary, macOS support (with known textual-terminal limitations)
**Project Type**: Single Python application with TUI
**Performance Goals**: 
- Interactive command launch <1s
- UI remains responsive during all subprocess execution
- Terminal emulation overhead <100ms for typical commands
**Constraints**: 
- Must not break existing async command execution
- Native mode (suspend/resume) must preserve terminal state
- Embedded mode limited to Linux (textual-terminal Mac issues)
- No Windows support (out of scope)
**Scale/Scope**: 
- 50+ commands in palette
- Support for both simple and complex interactive tools
- Dual rendering paths (embedded vs native)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Separation of Concerns ✅ PASS

- **Runner Layer**: Dual-mode architecture maintains separation
  - Native mode: `InteractiveRunner` service handles suspend/resume
  - Embedded mode: `EmbeddedTerminalRunner` service manages terminal widget lifecycle
  - Both isolated from UI layer
- **UI Layer**: Textual widgets (CommandListPanel, OutputPane) contain no execution logic
  - OutputPane conditionally renders either Static output or Terminal widget
- **Configuration Layer**: Command mode specified in commands.yaml via `mode` field
- **Data Flow**: Unidirectional: User Input → Mode Router → Native/Embedded Runner → UI Update

**Compliance**: Full compliance. Adding a second runner maintains existing separation.

### Principle II: Non-Blocking Async-First ⚠️ CONDITIONAL PASS

- **Native Mode**: Uses `app.suspend()` which BLOCKS the event loop by design
  - **Justification**: This is intentional - vim/tmux need full terminal control
  - Called as `await self.interactive_runner.run_session()` in async context
  - Blocking is required for native terminal handoff
- **Embedded Mode**: Fully async
  - Terminal widget runs subprocess with asyncio
  - Non-blocking I/O via pyte terminal emulator
  - UI remains interactive during embedded command execution

**Compliance**: Native mode violates async-first BUT is justified - native editors require synchronous terminal handoff. Embedded mode provides the non-blocking alternative for simple commands.

### Principle III: Observable Output Streams ✅ PASS

- **Native Mode**: 
  - Live output goes to native terminal (user sees it directly)
  - Summary (exit code, duration) displayed in OutputPane after completion
  - Error log captured for debugging
- **Embedded Mode**:
  - stdout/stderr streamed live to embedded terminal widget
  - Terminal widget provides colored ANSI output rendering
  - Exit codes and errors shown in-pane

**Compliance**: Full compliance. Both modes provide observable output appropriate to their context.

### Principle IV: Configuration-Driven Commands ✅ PASS

- Commands defined in commands.yaml with new `mode` field:
  ```yaml
  - name: Edit Config
    command: vim config.yaml
    interactive: true
    mode: native  # or "embedded"
  ```
- Mode field optional, defaults based on command type:
  - Editors (vim, nano, emacs) → `native`
  - Shells (bash, zsh) → `embedded`
  - User can override via explicit mode field
- No code changes needed to add new commands

**Compliance**: Full compliance. Dual-mode is configuration-driven.

### Principle V: Simplicity & YAGNI ✅ PASS

- Uses existing InteractiveRunner for native mode (already implemented)
- Adds textual-terminal dependency (mature, 0.3.0 release)
- Embedded mode is optional - users can use native-only if preferred
- Minimal abstractions: ModeRouter dispatches to appropriate runner
- No speculative features: just two modes as specified

**Compliance**: Full compliance. Adds complexity only for proven need (in-pane output viewing).

### Overall Status: ✅ PASS with justified violation

One principle (II: Async-First) has a justified violation for native mode terminal handoff. This is by design and unavoidable for full terminal control.

## Project Structure

### Documentation (this feature)

```text
specs/002-tui-interactive-shell/
├── plan.md              # This file (dual-mode architecture)
├── research.md          # Phase 0: textual-terminal evaluation, compatibility fixes
├── data-model.md        # Phase 1: SessionMode enum, EmbeddedSession model
├── quickstart.md        # Phase 1: dual-mode integration guide
├── contracts/           # Phase 1: EmbeddedTerminalRunner API, mode detection
│   └── service-api.md
└── tasks.md             # Phase 2: implementation task breakdown
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── command.py           # [EXTEND] Add 'mode' field (native|embedded|auto)
│   ├── interactive.py       # [EXISTING] InteractiveSession for native mode
│   └── embedded.py          # [NEW] EmbeddedSession model
├── services/
│   ├── interactive_runner.py        # [EXISTING] Native mode (suspend/resume)
│   ├── embedded_runner.py           # [NEW] Embedded terminal widget manager
│   ├── mode_router.py               # [NEW] Dispatch to native vs embedded
│   └── config.py                    # [EXTEND] Detect mode from command type
├── widgets/
│   ├── command_list.py              # [EXISTING] Command palette
│   ├── output_pane.py               # [EXTEND] Conditional render: Static | Terminal
│   ├── embedded_terminal.py         # [NEW] Wrapper for textual-terminal widget
│   └── app.py                       # [EXTEND] Route via ModeRouter
└── styles/
    └── app.css                      # [EXTEND] Terminal widget styles

tests/
├── unit/
│   ├── test_mode_detection.py      # [NEW] Mode selection logic
│   ├── test_embedded_runner.py     # [NEW] Embedded terminal lifecycle
│   └── test_mode_router.py         # [NEW] Dispatch logic
├── integration/
│   ├── test_native_mode.py         # [EXISTING] vim/nano/tmux tests
│   └── test_embedded_mode.py       # [NEW] bash/simple commands in-pane
└── fixtures/
    └── test_commands.yaml           # [EXTEND] Add mode examples

requirements.txt                     # [EXTEND] Add textual-terminal==0.3.0
```

**Structure Decision**: Single Python application with dual execution paths. Embedded mode adds a new service layer (`embedded_runner.py`) and widget wrapper (`embedded_terminal.py`) while preserving the existing native mode implementation. The `ModeRouter` service acts as a facade to dispatch commands to the appropriate runner based on the `mode` field.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **Principle II: Async-First** (Native Mode blocks event loop) | Full terminal control for vim/tmux requires synchronous handoff via `app.suspend()`. These editors need raw TTY access and cannot run in background workers. | **Terminal Emulation Only**: Would break vim plugin systems, complex escape sequences, and provide degraded experience. Native terminal is required for full-featured editors. |
| **Dual execution paths** (Native + Embedded) | Users need both reliable editors (native) AND in-pane output viewing (embedded). Neither mode alone satisfies all use cases. | **Native Only**: Users can't see command output in TUI context. **Embedded Only**: Vim/tmux broken or degraded, Mac users blocked by textual-terminal bugs. |
| **textual-terminal dependency** (unmaintained, Mac issues) | No viable alternative for in-pane terminal emulation in Textual. Building our own terminal emulator would be 3-6 months of work. | **Custom emulator**: Too complex, 3-6 month project. **Alternative libraries**: None exist for Textual ecosystem. **Fork textual-terminal**: Planned for Textual v6 compatibility fixes. |

## Implementation Phases

### Phase 0: Research & Dependency Evaluation

**Goal**: Validate textual-terminal compatibility and identify required fixes

**Tasks**:
1. Fork textual-terminal and fix Textual v6 compatibility (DEFAULT_COLORS deprecation)
2. Test embedded terminal with bash, nano, and simple commands
3. Document known limitations (Mac issues, Windows not supported)
4. Research mode auto-detection heuristics (command name patterns)
5. Design ModeRouter dispatch logic

**Deliverable**: `research.md` with textual-terminal fork details and compatibility matrix

### Phase 1: Design & Contracts

**Goal**: Define data models and service contracts for dual-mode execution

**Tasks**:
1. Design `SessionMode` enum (NATIVE, EMBEDDED, AUTO)
2. Design `EmbeddedSession` model (extends base session concept)
3. Define `EmbeddedTerminalRunner` service API contract
4. Define `ModeRouter` service contract
5. Specify OutputPane conditional rendering logic
6. Document mode detection algorithm

**Deliverables**:
- `data-model.md`: SessionMode, EmbeddedSession, Command extensions
- `contracts/service-api.md`: EmbeddedTerminalRunner, ModeRouter APIs
- `quickstart.md`: Integration guide for both modes

### Phase 2: Task Breakdown

**Goal**: Generate actionable implementation tasks

**Tasks**: Run `/speckit.tasks` to generate tasks.md based on Phase 1 design

**Deliverable**: `tasks.md` with dependency-ordered implementation steps

### Phase 3: Implementation

**Goal**: Execute tasks.md to build dual-mode terminal support

**Major Components**:
1. Install and patch textual-terminal dependency
2. Implement `EmbeddedTerminalRunner` service
3. Implement `ModeRouter` dispatch logic
4. Extend `Command` model with `mode` field
5. Update `OutputPane` for conditional rendering
6. Add `EmbeddedTerminalWidget` wrapper
7. Update `action_execute()` to route via ModeRouter
8. Add mode auto-detection to ConfigLoader
9. Update commands.yaml with mode examples
10. Write integration tests for both modes

**Deliverable**: Working dual-mode terminal in ops deck TUI

## Key Technical Decisions

### Decision 1: Why Dual-Mode Instead of Embedded-Only?

**Context**: textual-terminal provides in-pane terminal emulation

**Decision**: Implement BOTH native (suspend/resume) and embedded modes

**Rationale**:
- vim/tmux have complex terminal requirements that break in emulators
- Native mode provides 100% compatibility for advanced tools
- Embedded mode provides convenient in-pane viewing for simple commands
- Users can choose mode per command based on their needs

**Alternatives Considered**:
- Embedded-only: Rejected due to vim/tmux compatibility issues
- Native-only: Rejected due to lack of in-pane output viewing
- Build custom emulator: Rejected due to 3-6 month timeline

### Decision 2: Mode Selection Strategy

**Context**: Need to decide which mode to use for each command

**Decision**: Three-tier selection:
1. Explicit `mode` field in commands.yaml (highest priority)
2. Auto-detection based on command name (vim → native, bash → embedded)
3. Default to native for interactive commands, embedded for unknown

**Rationale**:
- Explicit mode gives users full control
- Auto-detection provides sensible defaults
- Fallback to native ensures compatibility

### Decision 3: textual-terminal Fork vs Upstream

**Context**: textual-terminal has Textual v6 compatibility issues

**Decision**: Fork, fix, and use our fork until upstream updates

**Rationale**:
- Upstream unmaintained (last commit Jan 2023)
- Fix is simple (update DEFAULT_COLORS API)
- Can't block on upstream maintainer response

**Implementation**: Fork at `[your-org]/textual-terminal` with v6 compatibility branch

### Decision 4: OutputPane Rendering Strategy

**Context**: OutputPane needs to show either static output or embedded terminal

**Decision**: Conditional rendering based on command mode:
- Native mode: Show static summary after completion (existing behavior)
- Embedded mode: Replace Static widget with Terminal widget during execution

**Rationale**:
- Avoids complex multi-widget management
- Clean separation between modes
- Existing async command output behavior preserved

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| textual-terminal Mac issues | High | Medium | Document Mac limitations, fallback to native mode on Mac |
| vim rendering issues in embedded | Medium | High | Use native mode for vim (already planned) |
| Terminal widget lifecycle leaks | Medium | Medium | Implement proper cleanup in EmbeddedTerminalRunner |
| Mode detection incorrect | Low | Low | Allow explicit override in commands.yaml |
| Performance overhead | Low | Low | Embedded mode only for simple commands, native for heavy tools |

## Success Metrics

### Phase Completion Criteria

**Phase 0 Complete**:
- ✅ textual-terminal fork created with Textual v6 fixes
- ✅ Compatibility matrix documented
- ✅ Mode detection algorithm specified

**Phase 1 Complete**:
- ✅ All data models defined in data-model.md
- ✅ Service contracts specified in contracts/
- ✅ Quickstart guide written

**Phase 2 Complete**:
- ✅ tasks.md generated with all implementation steps
- ✅ Dependencies identified and task order validated

**Phase 3 Complete**:
- ✅ Native mode: vim, nano, tmux work via suspend/resume
- ✅ Embedded mode: bash commands run in-pane with live output
- ✅ Mode auto-detection working for common commands
- ✅ User can override mode in commands.yaml
- ✅ Integration tests pass for both modes

### User Acceptance Criteria

- User can edit files in vim without leaving TUI context (native mode)
- User can run bash commands and see output in-pane (embedded mode)
- User can choose mode per command in configuration
- Both modes maintain working directory and environment variables
- Terminal state restored correctly in both modes
