# Tasks: Dual-Mode Terminal Integration

**Feature**: 002-tui-interactive-shell (Dual-Mode Enhancement)
**Input**: Design documents from `/specs/002-tui-interactive-shell/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Context**: This extends the EXISTING native mode (suspend/resume) implementation with embedded terminal support for in-pane command execution. Native mode is already fully implemented and working.

**Tests**: Tests are NOT explicitly requested in the specification and are therefore OPTIONAL.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **Checkbox**: Always `- [ ]` at start
- **[ID]**: Sequential task ID (T001, T002, etc.)
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

All paths relative to repository root (`/home/sthe/ops_deck/`)

---

## Phase 1: Setup & Dependencies

**Purpose**: Install textual-terminal and verify compatibility

- [ ] T001 Fork textual-terminal to fix Textual v6 compatibility (DEFAULT_COLORS deprecation)
- [ ] T002 Add textual-terminal>=0.3.0 to pyproject.toml dependencies
- [ ] T003 Add pyte to pyproject.toml dependencies (required by textual-terminal)
- [ ] T004 Install dependencies with pip install -e ".[dev]"
- [ ] T005 [P] Verify textual-terminal imports successfully
- [ ] T006 [P] Test basic Terminal widget mounting in Textual app

**Checkpoint**: textual-terminal installed and compatible with Textual 6.11.0

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and routing logic that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create SessionMode enum (NATIVE, EMBEDDED, AUTO) in src/models/interactive.py
- [ ] T008 Add mode:SessionMode field to Command model in src/models/command.py with default AUTO
- [ ] T009 Create EmbeddedSession dataclass in src/models/embedded.py
- [ ] T010 Create ModeRouter class skeleton in src/services/mode_router.py
- [ ] T011 Implement detect_mode() method in ModeRouter for AUTO mode detection
- [ ] T012 Implement dispatch logic in ModeRouter.execute() to route to native vs embedded
- [ ] T013 Create EmbeddedTerminalRunner class skeleton in src/services/embedded_runner.py
- [ ] T014 Create EmbeddedTerminalWidget wrapper class in src/widgets/embedded_terminal.py
- [ ] T015 [P] Add SessionMode and EmbeddedSession exports to src/models/__init__.py
- [ ] T016 [P] Add ModeRouter and EmbeddedTerminalRunner exports to src/services/__init__.py
- [ ] T017 [P] Add EmbeddedTerminalWidget export to src/widgets/__init__.py
- [ ] T018 Update config.py to parse mode field from commands.yaml in src/services/config.py
- [ ] T019 Add mode auto-detection logic in config.py (vim→native, bash→embedded)

**Checkpoint**: Foundation ready - dual-mode routing operational

---

## Phase 3: User Story 1 - Native Mode Editors (Priority: P1) 🎯

**Goal**: Ensure existing vim/nano native mode continues to work with new dual-mode architecture

**Independent Test**: Launch TUI, select "Edit Config (vim)" from palette, edit file in vim with :wq, verify TUI restores and mode=native was used

**Note**: Native mode is ALREADY IMPLEMENTED. This phase verifies integration with ModeRouter.

### Implementation for User Story 1

- [ ] T020 [US1] Update action_execute() in src/widgets/app.py to route through ModeRouter
- [ ] T021 [US1] Add ModeRouter instantiation in OpsApp.__init__() in src/widgets/app.py
- [ ] T022 [US1] Verify InteractiveRunner.run_session() is called for mode=NATIVE commands
- [ ] T023 [US1] Update "Edit Config" command in commands.yaml with explicit mode: native
- [ ] T024 [US1] Update "Edit Readme" command in commands.yaml with explicit mode: native
- [ ] T025 [P] [US1] Add mode display in command list (show "📝 native" badge)

**Checkpoint**: User Story 1 complete - Native mode editors work through new routing

---

## Phase 4: User Story 2 - Embedded Shell Sessions (Priority: P1) 🚀

**Goal**: Enable bash commands to run in embedded terminal widget within output pane

**Independent Test**: Launch TUI, select "Quick Shell (embedded)" from palette, run ls/pwd commands in-pane, see output live, type exit, verify TUI stays responsive

### Implementation for User Story 2

- [ ] T026 [US2] Implement start_embedded_session() in EmbeddedTerminalRunner
- [ ] T027 [US2] Create Terminal widget instance from textual-terminal in EmbeddedTerminalRunner
- [ ] T028 [US2] Implement widget mounting logic in EmbeddedTerminalRunner
- [ ] T029 [US2] Implement subprocess lifecycle management in EmbeddedTerminalRunner
- [ ] T030 [US2] Implement widget cleanup on session end in EmbeddedTerminalRunner
- [ ] T031 [US2] Add terminal size detection and resize handling in EmbeddedTerminalRunner
- [ ] T032 [US2] Implement error handling for subprocess failures in EmbeddedTerminalRunner
- [ ] T033 [US2] Extend OutputPane to support conditional rendering (Static vs Terminal widget)
- [ ] T034 [US2] Add render_embedded_terminal() method in src/widgets/output_pane.py
- [ ] T035 [US2] Add render_static_output() method to restore normal output display
- [ ] T036 [US2] Implement widget swap logic in OutputPane.compose()
- [ ] T037 [US2] Add environment variable forwarding to embedded terminal in EmbeddedTerminalRunner
- [ ] T038 [US2] Add working directory preservation for embedded sessions
- [ ] T039 [US2] Implement exit code capture from embedded terminal process
- [ ] T040 [US2] Display session summary (exit code, duration) after embedded session ends
- [ ] T041 [US2] Add "Quick Shell" command with mode: embedded to commands.yaml
- [ ] T042 [P] [US2] Add "Run Command" command with mode: embedded for quick one-liners

**Checkpoint**: User Story 2 complete - Bash commands run in-pane with live output

---

## Phase 5: User Story 3 - Native Mode Multiplexers (Priority: P2)

**Goal**: Ensure tmux/screen work via native mode (suspend/resume)

**Independent Test**: Launch TUI, select "Open tmux" from palette, create windows in tmux, exit tmux, verify TUI restores

**Note**: tmux/screen are NOT supported in embedded mode due to terminal-in-terminal complexity

### Implementation for User Story 3

- [ ] T043 [P] [US3] Update session_type auto-detection for tmux/screen → MULTIPLEXER
- [ ] T044 [P] [US3] Force mode=NATIVE for session_type=MULTIPLEXER in ModeRouter
- [ ] T045 [US3] Add "Open tmux" command with mode: native session_type: multiplexer to commands.yaml
- [ ] T046 [P] [US3] Add "Open screen" command with mode: native session_type: multiplexer to commands.yaml

**Checkpoint**: User Story 3 complete - tmux/screen work via native mode

---

## Phase 6: User Story 4 - Seamless Integration (Priority: P2)

**Goal**: Ensure async commands, native mode, and embedded mode all coexist without conflicts

**Independent Test**: Run async command (deploy), then native vim, then embedded bash, verify all three modes work independently

### Implementation for User Story 4

- [ ] T047 [US4] Verify async command execution still works after ModeRouter integration
- [ ] T048 [US4] Add mode detection bypass for non-interactive commands in ModeRouter
- [ ] T049 [US4] Implement session state tracking to prevent mode conflicts
- [ ] T050 [US4] Add UI indicator showing current execution mode (async/native/embedded)
- [ ] T051 [US4] Ensure OutputPane correctly switches between async output and embedded terminal
- [ ] T052 [US4] Verify command history is preserved across mode switches
- [ ] T053 [P] [US4] Add mixed-mode example commands to commands.yaml (async, native, embedded)

**Checkpoint**: User Story 4 complete - All execution modes coexist smoothly

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final quality improvements, edge cases, and documentation

- [ ] T054 [P] Add CSS styles for embedded terminal widget in src/styles/app.css
- [ ] T055 [P] Add terminal color scheme configuration (ANSI colors)
- [ ] T056 [P] Implement graceful fallback to native mode if textual-terminal fails
- [ ] T057 [P] Add mode override capability via command palette (force native/embedded)
- [ ] T058 Add comprehensive docstrings to ModeRouter class
- [ ] T059 Add comprehensive docstrings to EmbeddedTerminalRunner class
- [ ] T060 Add comprehensive docstrings to EmbeddedTerminalWidget class
- [ ] T061 [P] Update README.md with dual-mode usage examples
- [ ] T062 [P] Add troubleshooting section for Mac compatibility issues
- [ ] T063 [P] Document mode selection algorithm in docs/
- [ ] T064 Verify scrollbar fix is still working after OutputPane changes
- [ ] T065 Add example commands demonstrating both modes to commands.yaml

**Checkpoint**: Feature complete - ready for production use

---

## Dependencies & Execution Order

### Critical Path (Must Complete in Order)

1. **Phase 1** (Setup) → **Phase 2** (Foundation)
2. **Phase 2** → **Phase 3** (US1 Native Integration)
3. **Phase 2** → **Phase 4** (US2 Embedded Shell) ← **Main Development**
4. **Phase 4** → **Phase 5** (US3 Multiplexers)
5. **Phase 3, 4, 5** → **Phase 6** (US4 Integration)
6. **Phase 6** → **Phase 7** (Polish)

### User Story Dependencies

- **US1** (Native Editors): No dependencies (native mode already implemented)
- **US2** (Embedded Shells): Depends on Phase 2 foundation
- **US3** (Multiplexers): Depends on US1 (reuses native mode)
- **US4** (Integration): Depends on US1, US2, US3

### Parallel Execution Opportunities

**Within Phase 2** (can run simultaneously):
- T007-T009 (models)
- T010-T014 (services)
- T015-T017 (exports)

**Within Phase 4** (can run simultaneously after T026-T032):
- T033-T036 (OutputPane changes)
- T037-T040 (session management)
- T041-T042 (config examples)

**Within Phase 7** (most tasks independent):
- T054-T057, T061-T063 (can all run in parallel)

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Phases 1-4** deliver a working dual-mode system:
- Native mode for vim/nano (already working, integrated with router)
- Embedded mode for bash shells (new capability)
- Mode auto-detection working
- Both modes operational

**Estimated Effort**: 24-32 hours

### Full Feature Scope

**Phases 1-7** deliver complete dual-mode terminal:
- All user stories implemented
- tmux support verified
- Polish and documentation complete
- Production-ready

**Estimated Effort**: 40-50 hours

### Incremental Delivery Plan

1. **Week 1**: Phases 1-2 (Setup + Foundation) → 8-12 hours
2. **Week 2**: Phases 3-4 (Native integration + Embedded shell) → 16-20 hours
3. **Week 3**: Phases 5-7 (Multiplexers + Integration + Polish) → 16-18 hours

---

## Validation Checklist

After completing all tasks, verify:

- [ ] vim launches via native mode (mode=native)
- [ ] bash launches in embedded terminal (mode=embedded)
- [ ] tmux launches via native mode (mode=native)
- [ ] Async commands still work normally
- [ ] Mode auto-detection works (AUTO mode)
- [ ] User can override mode in commands.yaml
- [ ] OutputPane switches correctly between Static and Terminal widget
- [ ] Terminal widget cleans up properly after session ends
- [ ] Working directory preserved in both modes
- [ ] Environment variables preserved in both modes
- [ ] Exit codes captured correctly in both modes
- [ ] TUI remains responsive during embedded commands
- [ ] Scrollbar still works in command list
- [ ] All constitution principles satisfied (with justified violations documented)

---

## Notes for Implementation

### Native Mode (US1, US3)
- Already implemented in `src/services/interactive_runner.py`
- Uses `app.suspend()` and `app.resume()`
- No changes needed to core logic
- Just integrate with ModeRouter for dispatch

### Embedded Mode (US2)
- New implementation in `src/services/embedded_runner.py`
- Uses `textual-terminal.Terminal` widget
- Mounted in OutputPane during execution
- Widget lifecycle: create → mount → attach subprocess → wait → cleanup

### Mode Detection Logic
```python
def detect_mode(command: Command) -> SessionMode:
    if command.mode != SessionMode.AUTO:
        return command.mode  # Explicit override
    
    # Auto-detect based on command name
    if any(editor in command.command for editor in ['vim', 'nano', 'emacs']):
        return SessionMode.NATIVE
    if any(shell in command.command for shell in ['bash', 'zsh', 'fish']):
        return SessionMode.EMBEDDED
    if any(mux in command.command for mux in ['tmux', 'screen']):
        return SessionMode.NATIVE
    
    return SessionMode.NATIVE  # Default to native for safety
```

### textual-terminal Integration
- Fork: Fix `DEFAULT_COLORS` deprecation (replace with `app.theme.foreground`)
- Widget: `from textual_terminal import Terminal`
- Mount: `await self.mount(Terminal(command="bash"))`
- Start: `terminal.start()`
- Cleanup: `await terminal.remove()`

---

## Risk Mitigation

| Risk | Mitigation Strategy | Task Reference |
|------|---------------------|----------------|
| textual-terminal Mac issues | Document Mac limitations, fallback to native | T056, T062 |
| Widget lifecycle leaks | Proper cleanup in finally blocks | T030 |
| OutputPane rendering conflicts | Clear separation of Static vs Terminal rendering | T033-T036 |
| Mode detection incorrect | Allow explicit override in commands.yaml | T023-T024, T041 |
| Performance degradation | Embedded mode only for simple commands | T026-T032 |

---

**Total Tasks**: 65
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundation): 13 tasks
- Phase 3 (US1 Native): 6 tasks
- Phase 4 (US2 Embedded): 17 tasks
- Phase 5 (US3 Multiplexers): 4 tasks
- Phase 6 (US4 Integration): 7 tasks
- Phase 7 (Polish): 12 tasks

**Parallel Opportunities**: 24 tasks marked [P] can run simultaneously

**MVP Scope**: Phases 1-4 (42 tasks) delivers working dual-mode terminal

**Independent Test Criteria Defined**: ✅ All 4 user stories have clear test scenarios
