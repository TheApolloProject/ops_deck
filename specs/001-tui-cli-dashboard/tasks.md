# Tasks: TUI CLI Dashboard

**Input**: Design documents from `/specs/001-tui-cli-dashboard/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Not explicitly requested in spec - tests are OPTIONAL but recommended for services.

**Organization**: Tasks grouped by user story (P1-P4) for independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4)
- File paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and tooling

- [ ] T001 Create project directory structure per plan.md in src/, tests/, src/models/, src/services/, src/widgets/, src/styles/
- [ ] T002 Create pyproject.toml with dependencies: textual, pyyaml, pydantic, pytest, pytest-asyncio, ruff, mypy
- [ ] T003 [P] Create src/__init__.py with package metadata
- [ ] T004 [P] Create tests/__init__.py and tests/conftest.py with shared fixtures
- [ ] T005 [P] Configure ruff.toml for linting rules
- [ ] T006 Create example commands.yaml configuration file at repository root

**Checkpoint**: Project structure exists, `pip install -e .` works, `ruff check src/` runs

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and base infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Create Command model with Pydantic validation in src/models/command.py
- [ ] T008 [P] Create StreamType enum and OutputLine dataclass in src/models/execution.py
- [ ] T009 [P] Create ExecutionStatus enum in src/models/execution.py
- [ ] T010 Create Execution model with state tracking in src/models/execution.py (depends on T008, T009)
- [ ] T011 [P] Create AppConfig model with commands list in src/models/command.py
- [ ] T012 [P] Create ConfigError, ConfigNotFoundError, ConfigValidationError exceptions in src/services/config_loader.py
- [ ] T013 Create ConfigLoader.load() method per contract in src/services/config_loader.py (depends on T007, T011, T012)
- [ ] T014 Create ConfigLoader.load_default() method with search paths in src/services/config_loader.py (depends on T013)
- [ ] T015 [P] Create Textual message classes in src/messages.py per contracts/messages.md
- [ ] T016 Create base Textual CSS layout in src/styles/app.tcss (grid with sidebar + main content)

**Checkpoint**: Models importable, ConfigLoader loads commands.yaml, messages defined

---

## Phase 3: User Story 1 - Execute Command from Palette (Priority: P1) 🎯 MVP

**Goal**: User selects command from palette, sees streaming output in real-time

**Independent Test**: Launch app, click command, see live output streaming line-by-line

### Implementation for User Story 1

- [ ] T017 [US1] Implement CommandRunner.run() async iterator in src/services/runner.py per contracts/command_runner.md
- [ ] T018 [US1] Implement dual-stream capture (stdout/stderr interleaved) in src/services/runner.py using asyncio Queue pattern from research.md
- [ ] T019 [US1] Create CommandPalette widget displaying command list in src/widgets/command_palette.py
- [ ] T020 [US1] Implement CommandPalette.on_click handler to post CommandSelected message in src/widgets/command_palette.py
- [ ] T021 [US1] Create OutputView widget with scrollable RichLog in src/widgets/output_view.py
- [ ] T022 [US1] Implement OutputView.on_output_received handler to append lines in src/widgets/output_view.py
- [ ] T023 [US1] Create OpsDeckApp class with compose() layout in src/app.py
- [ ] T024 [US1] Implement App.on_command_selected handler to start worker in src/app.py
- [ ] T025 [US1] Implement @work decorated execute_command worker in src/app.py that streams to OutputView
- [ ] T026 [US1] Add __main__.py entry point to run OpsDeckApp in src/__main__.py

**Checkpoint**: `python -m src` launches, command palette shows commands, clicking runs command with live output

---

## Phase 4: User Story 2 - Distinguish Success from Errors (Priority: P2)

**Goal**: stderr appears in different color, exit code indicator shows success/failure

**Independent Test**: Run command producing stderr, verify different color; run failing command, verify error indicator

### Implementation for User Story 2

- [ ] T027 [US2] Add stdout/stderr CSS classes with distinct colors in src/styles/app.tcss
- [ ] T028 [US2] Update OutputView to apply stream-specific CSS class per line in src/widgets/output_view.py
- [ ] T029 [US2] Add ExecutionCompleted message handling in OutputView in src/widgets/output_view.py
- [ ] T030 [US2] Display success indicator (✓ green) on exit code 0 in src/widgets/output_view.py
- [ ] T031 [US2] Display error indicator (✗ red) on non-zero exit code in src/widgets/output_view.py
- [ ] T032 [US2] Update CommandRunner to post ExecutionCompleted with exit code in src/services/runner.py

**Checkpoint**: stderr lines show in red/orange, command completion shows ✓ or ✗ indicator

---

## Phase 5: User Story 3 - Responsive UI During Long Commands (Priority: P3)

**Goal**: UI remains scrollable and clickable during long-running command execution

**Independent Test**: Run `sleep 5 && echo done`, verify UI scrolling and palette clicking works during execution

### Implementation for User Story 3

- [ ] T033 [US3] Verify @work(exclusive=False) allows parallel command execution in src/app.py
- [ ] T034 [US3] Add execution status indicator (running spinner) to CommandPalette in src/widgets/command_palette.py
- [ ] T035 [US3] Implement auto-scroll to bottom with scroll-lock on user scroll in src/widgets/output_view.py
- [ ] T036 [US3] Add command header with name and start time when execution begins in src/widgets/output_view.py

**Checkpoint**: Long command runs, UI stays interactive, multiple commands can run in parallel

---

## Phase 6: User Story 4 - Configure Custom Commands (Priority: P4)

**Goal**: User edits YAML config, restarts app, sees new commands in palette

**Independent Test**: Add new command to commands.yaml, restart, verify it appears in palette

### Implementation for User Story 4

- [ ] T037 [US4] Add command description display in CommandPalette tooltip or subtitle in src/widgets/command_palette.py
- [ ] T038 [US4] Improve ConfigValidationError messages with line numbers in src/services/config_loader.py
- [ ] T039 [US4] Add startup error screen for config errors in src/app.py
- [ ] T040 [US4] Document configuration format in README.md at repository root

**Checkpoint**: Custom commands appear, invalid config shows clear error, description visible in palette

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Quality improvements affecting all user stories

- [ ] T041 [P] Add type hints to all public functions and run mypy in src/
- [ ] T042 [P] Add docstrings to all public classes and methods in src/
- [ ] T043 [P] Create unit tests for ConfigLoader in tests/unit/test_config_loader.py
- [ ] T044 [P] Create unit tests for CommandRunner in tests/unit/test_runner.py
- [ ] T045 Run quickstart.md validation checklist
- [ ] T046 [P] Add keyboard shortcuts (q to quit, / for command search) in src/app.py

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
     │
     ▼
Phase 2 (Foundational) ──────────────────┐
     │                                    │
     ▼                                    ▼
Phase 3 (US1: MVP)                   Phases 4-6 BLOCKED
     │                                    │
     ├──── Can validate MVP here ─────────┤
     ▼                                    ▼
Phase 4 (US2)                        Phase 5 (US3)
     │                                    │
     └────────────┬───────────────────────┘
                  ▼
           Phase 6 (US4)
                  │
                  ▼
           Phase 7 (Polish)
```

### User Story Independence

| Story | Can Start After | Dependencies on Other Stories |
|-------|-----------------|-------------------------------|
| US1 (P1) | Phase 2 | None - this is the MVP |
| US2 (P2) | Phase 2 | Uses OutputView from US1, but adds features |
| US3 (P3) | Phase 2 | Uses worker pattern from US1, enhances UX |
| US4 (P4) | Phase 2 | Uses ConfigLoader from Foundation |

### Parallel Opportunities

```bash
# Phase 1 parallel tasks:
T003, T004, T005, T006 can run together

# Phase 2 parallel tasks:
T007, T008, T009, T011, T012, T015, T016 can run together
(T010 waits for T008, T009; T013 waits for T007, T011, T012; T014 waits for T013)

# After Phase 2, all user stories can start in parallel if staffed
```

---

## Implementation Strategy

### MVP First (Recommended)

1. ✅ Phase 1: Setup (T001-T006)
2. ✅ Phase 2: Foundational (T007-T016)
3. ✅ Phase 3: User Story 1 (T017-T026)
4. **STOP AND VALIDATE**: App launches, commands run with streaming output
5. Continue to US2, US3, US4 as needed

### Task Count Summary

| Phase | Tasks | Parallel |
|-------|-------|----------|
| Setup | 6 | 4 |
| Foundational | 10 | 7 |
| US1 (P1) | 10 | 0 (sequential) |
| US2 (P2) | 6 | 0 |
| US3 (P3) | 4 | 0 |
| US4 (P4) | 4 | 0 |
| Polish | 6 | 5 |
| **Total** | **46** | **16** |

---

## Notes

- All file paths are relative to repository root `/home/sthe/ops_deck/`
- No external API contracts - this is a local TUI application
- Textual CSS in `src/styles/app.tcss` should be updated incrementally per story
- Commit after each task or logical group of tasks
- Run `ruff check src/` and `python -m src` after each phase to validate
