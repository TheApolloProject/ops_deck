# Implementation Plan: TUI CLI Dashboard

**Branch**: `001-tui-cli-dashboard` | **Date**: 2025-12-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-tui-cli-dashboard/spec.md`

## Summary

Build a Python TUI dashboard using Textual that displays a command palette for predefined CLI commands and streams their output in real-time. The architecture separates UI (Textual widgets), command execution (asyncio workers), and configuration (YAML files) into distinct layers to enable non-blocking execution and independent testability.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Textual (TUI framework), PyYAML (config parsing)  
**Storage**: N/A (in-memory output only, config from filesystem)  
**Testing**: pytest with pytest-asyncio for async tests  
**Target Platform**: Linux/macOS/Windows terminal (cross-platform)  
**Project Type**: Single project  
**Performance Goals**: <200ms output latency, 60fps UI responsiveness  
**Constraints**: <100MB memory, UI must respond within 100ms during command execution  
**Scale/Scope**: Single-user local application, ~5-10 screens/widgets

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Separation of Concerns | Runner/UI/Config layers isolated | ✅ PASS | Design has 3 distinct layers |
| II. Non-Blocking Async-First | asyncio workers, no main loop blocking | ✅ PASS | Textual workers + asyncio subprocess |
| III. Observable Output Streams | stdout/stderr distinct, exit codes shown | ✅ PASS | FR-004, FR-005, FR-006 cover this |
| IV. Configuration-Driven | External YAML config, validated at startup | ✅ PASS | FR-008, FR-009 require this |
| V. Simplicity & YAGNI | Core features only, minimal deps | ✅ PASS | Only 2 external deps (Textual, PyYAML) |

**Quality Gates Compliance**:
- Lint Gate: Will configure ruff
- Type Gate: Will use mypy (warnings acceptable initially)
- Test Gate: pytest-asyncio for async testing
- UI Responsiveness Gate: Manual verification in acceptance testing
- Config Validation Gate: FR-009 ensures this

## Project Structure

### Documentation (this feature)

```text
specs/001-tui-cli-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (internal interfaces)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── app.py               # Textual App class, main entry point
├── models/
│   ├── __init__.py
│   ├── command.py       # Command dataclass
│   └── execution.py     # Execution state tracking
├── services/
│   ├── __init__.py
│   ├── config_loader.py # YAML config loading and validation
│   └── runner.py        # Async subprocess execution
├── widgets/
│   ├── __init__.py
│   ├── command_palette.py  # Sidebar command list widget
│   └── output_view.py      # Scrollable output display widget
└── styles/
    └── app.tcss         # Textual CSS for layout and styling

tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── unit/
│   ├── test_command.py
│   ├── test_config_loader.py
│   └── test_runner.py
└── integration/
    └── test_app.py      # Full app integration tests

commands.yaml            # Example configuration file
pyproject.toml           # Project metadata and dependencies
```

**Structure Decision**: Single project structure selected. This is a standalone TUI application with no frontend/backend split or mobile components. The `src/` directory contains application code organized by layer (models, services, widgets), and `tests/` mirrors this structure.

## Complexity Tracking

> No constitution violations requiring justification. Design adheres to all 5 principles.

---

## Constitution Re-Check (Post Phase 1 Design)

*Verified after completing research.md, data-model.md, and contracts/*

| Principle | Design Artifact | Compliance Evidence |
|-----------|-----------------|---------------------|
| I. Separation of Concerns | contracts/*.md | 3 separate contracts (ConfigLoader, CommandRunner, Messages) enforce layer boundaries |
| II. Non-Blocking Async-First | research.md §1-2 | Textual @work decorator + asyncio.create_subprocess_shell pattern documented |
| III. Observable Output Streams | data-model.md | OutputLine entity with StreamType enum; research.md §5 shows dual-stream capture |
| IV. Configuration-Driven | contracts/config_loader.md | Full validation contract with error types; YAML schema in research.md §3 |
| V. Simplicity & YAGNI | plan.md Dependencies | Only 3 deps (Textual, PyYAML, Pydantic); no unnecessary abstractions |

**Post-Design Status**: ✅ ALL GATES PASS

**Ready for**: `/speckit.tasks` to generate implementation tasks
