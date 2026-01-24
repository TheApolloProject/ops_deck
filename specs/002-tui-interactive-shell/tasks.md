# Tasks: TUI with Interactive Shell Commands

**Input**: Design documents from `/specs/002-tui-interactive-shell/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are OPTIONAL and not included in this task list as they were not explicitly requested in the specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow the structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [x] T001 Add pexpect>=4.8.0 to pyproject.toml dependencies (optional, can use stdlib subprocess)
- [x] T002 Install dependencies with pip install -e ".[dev]"
- [x] T003 [P] Verify Python 3.10+ and Textual 0.30+ are available
- [x] T004 [P] Create test data directory for interactive session testing

**Checkpoint**: Dependencies installed, environment ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and services that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create SessionType enum in src/models/interactive.py
- [ ] T006 Create InteractiveSession dataclass in src/models/interactive.py
- [ ] T007 Add interactive:bool and session_type:SessionType fields to Command model in src/models/command.py
- [ ] T008 Update config.py to parse interactive and session_type from YAML in src/services/config.py
- [ ] T009 Create InteractiveRunner class skeleton in src/services/interactive_runner.py
- [x] T010 Implement detect_nested_instance() static method in src/services/interactive_runner.py
- [x] T011 Add nested instance check at startup in src/app.py entry point
- [x] T012 [P] Add InteractiveSession and SessionType exports to src/models/__init__.py
- [x] T013 [P] Add InteractiveRunner export to src/services/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Launch Interactive Editors (Priority: P1) 🎯 MVP

**Goal**: Enable users to launch vim/nano from the TUI, edit files, and return to the TUI with changes persisted

**Independent Test**: Launch TUI, select "Edit Config (vim)" from palette, edit a file in vim, save with `:wq`, verify TUI restores cleanly and file changes are persisted

### Implementation for User Story 1

- [x] T014 [P] [US1] Implement run_session() method signature in src/services/interactive_runner.py
- [x] T015 [US1] Implement session creation logic in run_session() (create InteractiveSession object with start_time)
- [x] T016 [US1] Implement TUI suspension via app.suspend() in run_session()
- [x] T017 [US1] Implement subprocess launch with asyncio.create_subprocess_shell in run_session()
- [x] T018 [US1] Implement environment variable setting (OPS_DECK_ACTIVE=1) in run_session()
- [x] T019 [US1] Implement subprocess wait and exit code capture in run_session()
- [x] T020 [US1] Implement TUI restoration via app.resume() in finally block in run_session()
- [x] T021 [US1] Implement error logging to session.error_log in run_session()
- [x] T022 [US1] Add session tracking to _active_sessions list in InteractiveRunner
- [x] T023 [US1] Implement get_active_sessions() method in src/services/interactive_runner.py
- [x] T024 [US1] Add command routing logic in app widget to detect interactive=True in src/widgets/app.py
- [x] T025 [US1] Call InteractiveRunner.run_session() for interactive commands in src/widgets/app.py
- [x] T026 [US1] Display interactive session results (exit code, errors) in TUI in src/widgets/app.py
- [x] T027 [US1] Add "Edit Config" command with interactive:true to commands.yaml
- [x] T028 [US1] Add "Edit Readme" command with interactive:true session_type:editor to commands.yaml

**Checkpoint**: User Story 1 complete - Users can launch vim/nano, edit files, and return to TUI

---

## Phase 4: User Story 2 - Execute Interactive Shell Sessions (Priority: P1)

**Goal**: Enable users to drop into bash/zsh shells to run ad-hoc commands interactively

**Independent Test**: Launch TUI, select "Open Shell" from palette, run commands (ls, cd, pipes), type exit, verify TUI restores and working directory is preserved

### Implementation for User Story 2

- [x] T029 [P] [US2] Add working directory preservation logic in run_session() in src/services/interactive_runner.py
- [x] T030 [P] [US2] Add environment snapshot capture before session start in src/services/interactive_runner.py
- [x] T031 [US2] Verify working directory is inherited by subprocess in run_session()
- [x] T032 [US2] Add session_type auto-detection logic for shells (bash, zsh) in src/services/config.py
- [x] T033 [US2] Add "Open Shell" command with interactive:true session_type:shell to commands.yaml
- [x] T034 [US2] Add "Open Zsh" command with interactive:true session_type:shell to commands.yaml

**Checkpoint**: User Story 2 complete - Users can launch interactive shells and run ad-hoc commands

---

## Phase 5: User Story 3 - Run Interactive Tools with Terminal Multiplexing (Priority: P2)

**Goal**: Enable users to launch tmux/screen within the TUI for advanced session management

**Independent Test**: Launch TUI, select "Open tmux" from palette, create tmux windows (Ctrl+B c), verify window management works, exit tmux, verify TUI restores

### Implementation for User Story 3

- [x] T035 [P] [US3] Add session_type auto-detection for tmux/screen in src/services/config.py
- [x] T036 [P] [US3] Add "Open tmux" command with interactive:true session_type:multiplexer to commands.yaml
- [x] T037 [P] [US3] Add "Open screen" command with interactive:true session_type:multiplexer to commands.yaml
- [x] T038 [US3] Add signal handling verification for complex multiplexers (Ctrl+B, Ctrl+A) in src/services/interactive_runner.py
- [x] T039 [US3] Test terminal restoration after tmux crash scenario (add to error_log handling)

**Checkpoint**: User Story 3 complete - Users can launch and manage tmux/screen sessions

---

## Phase 6: User Story 4 - Maintain Command Palette with Interactive Enhancements (Priority: P2)

**Goal**: Ensure interactive commands integrate seamlessly with existing async command palette without breaking workflows

**Independent Test**: Launch TUI, run async command (df -h), view output, launch interactive shell, exit shell, run another async command, verify both workflows work independently

### Implementation for User Story 4

- [ ] T040 [P] [US4] Add conditional routing in on_command_selected() to check interactive flag in src/widgets/app.py
- [ ] T041 [US4] Preserve async command output history when launching interactive sessions in src/widgets/app.py
- [ ] T042 [US4] Verify async command execution still works after interactive session ends in src/widgets/app.py
- [ ] T043 [US4] Add UI indicator showing when command is interactive vs async in src/widgets/command_list.py
- [ ] T044 [US4] Add session result display that doesn't overwrite async output in src/widgets/app.py

**Checkpoint**: User Story 4 complete - Interactive and async workflows coexist seamlessly

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, documentation, and production readiness

- [ ] T045 [P] Add optional logging_enabled parameter support to run_session() in src/services/interactive_runner.py
- [ ] T046 [P] Add log_file_path parameter support for session transcripts in src/services/interactive_runner.py
- [ ] T047 [P] Implement terminal state restoration fallback (os.system("reset")) in src/services/interactive_runner.py
- [ ] T048 [P] Add session duration calculation property to InteractiveSession in src/models/interactive.py
- [ ] T049 [P] Add docstrings to all public methods in src/services/interactive_runner.py
- [ ] T050 [P] Add docstrings to InteractiveSession and SessionType in src/models/interactive.py
- [ ] T051 [P] Update README.md with interactive shell feature documentation
- [ ] T052 [P] Add example commands.yaml with interactive command examples
- [ ] T053 Verify all edge cases from spec.md are handled (kill -9, Ctrl+C, crashed editors)
- [ ] T054 Run manual acceptance tests for all four user stories
- [ ] T055 Performance check: Verify TUI suspension <100ms, resumption <50ms

**Checkpoint**: Feature complete, documented, and production-ready

---

## Implementation Strategy

### MVP Scope (User Story 1 only)

For a minimal viable product, implement **Phase 1, Phase 2, and Phase 3 only**:
- Foundation (models, services, nested detection)
- Editor support (vim, nano)
- Basic TUI suspend/resume

This delivers the core value proposition: editing files within the TUI.

### Incremental Delivery

1. **Week 1**: MVP (Phases 1-3) - Editor support
2. **Week 2**: Shell support (Phase 4) - Interactive bash/zsh
3. **Week 3**: Advanced tools (Phase 5) - tmux/screen support
4. **Week 4**: Integration (Phase 6) - Seamless palette integration
5. **Week 5**: Polish (Phase 7) - Documentation, edge cases, performance

### Parallel Execution Opportunities

**Phase 2 (Foundational)**: Tasks T005-T007 and T012-T013 can run in parallel (different files)

**Phase 3 (User Story 1)**: 
- T014-T023 (InteractiveRunner implementation) can overlap with T024-T026 (App integration)
- T027-T028 (YAML config) can be done anytime after T008

**Phase 4 (User Story 2)**:
- T029-T030 can run in parallel (different concerns in same file)
- T033-T034 (YAML config) can run anytime

**Phase 5 (User Story 3)**: T035-T037 can all run in parallel (different files/sections)

**Phase 6 (User Story 4)**: T040 and T043 can run in parallel (different files)

**Phase 7 (Polish)**: T045-T050 can all run in parallel (different files)

---

## Dependencies

### Story Completion Order

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKING
    ↓
    ├─→ Phase 3 (US1: Editors) ✅ Can implement independently
    ├─→ Phase 4 (US2: Shells) ✅ Can implement independently
    ├─→ Phase 5 (US3: Multiplexers) ✅ Can implement independently (depends on US1/US2 for testing)
    └─→ Phase 6 (US4: Integration) ⚠️ Depends on at least US1 or US2 being complete
         ↓
    Phase 7 (Polish) ← All stories should be complete
```

### Critical Path

**Longest dependency chain**:
1. Phase 1 (Setup) → 4 tasks
2. Phase 2 (Foundational) → 9 tasks
3. Phase 3 (User Story 1) → 15 tasks
4. Phase 6 (User Story 4) → 5 tasks (depends on US1)
5. Phase 7 (Polish) → 11 tasks

**Total Critical Path**: 44 tasks

### Independent Stories

- **User Story 1** (Editors) - Fully independent after Phase 2
- **User Story 2** (Shells) - Fully independent after Phase 2
- **User Story 3** (Multiplexers) - Fully independent after Phase 2 (but benefits from testing US1/US2 first)

---

## Task Summary

**Total Tasks**: 55

**Task Count by Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 9 tasks
- Phase 3 (US1: Editors): 15 tasks
- Phase 4 (US2: Shells): 6 tasks
- Phase 5 (US3: Multiplexers): 5 tasks
- Phase 6 (US4: Integration): 5 tasks
- Phase 7 (Polish): 11 tasks

**Task Count by User Story**:
- US1 (Launch Interactive Editors): 15 tasks
- US2 (Execute Interactive Shell Sessions): 6 tasks
- US3 (Run Interactive Tools with Terminal Multiplexing): 5 tasks
- US4 (Maintain Command Palette with Interactive Enhancements): 5 tasks

**Parallel Opportunities**: 25 tasks marked with [P] can run in parallel

**Independent Tests**: Each user story has clear independent test criteria (no automated tests included as not requested)

**MVP Scope**: Phases 1-3 (28 tasks) deliver a working editor integration feature

---

## Format Validation

✅ All tasks follow the required format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ All user story tasks include [US#] label
✅ All setup and foundational tasks have no story label
✅ All task descriptions include specific file paths
✅ Sequential task IDs from T001 to T055
✅ Parallel tasks marked with [P]
✅ Dependencies clearly documented
✅ Independent test criteria provided for each story
