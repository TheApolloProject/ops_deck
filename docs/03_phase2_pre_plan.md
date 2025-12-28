# Phase 2 Pre-Implementation Plan: Foundational Models & Services

**Date**: 2025-12-28  
**Phase**: 2 of 7  
**Duration Estimate**: 90 minutes

## Overview

Phase 2 builds the foundational layer that all user stories depend on. We'll implement data models, exception handling, service interfaces, and message definitions for the Textual TUI.

## Phase Scope

| Area | Tasks | Deliverables |
|------|-------|--------------|
| Data Models | T007-T011 (5 tasks) | Command, Execution, OutputLine, AppConfig, Config models |
| Exception Layer | T012 (1 task) | Custom exceptions (ConfigError, ExecutionError, etc.) |
| Service Interfaces | T013-T014 (2 tasks) | ConfigLoader (load/validate), CommandRunner contract |
| Message System | T015 (1 task) | Textual message classes (CommandOutput, StatusUpdate, etc.) |
| UI Layout | T016 (1 task) | Base CSS layout for Textual widgets |

## Task Breakdown

### Data Models (T007-T011)

**T007: Command Model**
- File: `src/models/command.py`
- Dependencies: pydantic
- Input: Command entity definition from data-model.md
- Output: Pydantic model with fields (name, command, description, tags, timeout, env)
- Validation: Non-empty strings, positive timeout, dict env

**T008: Execution Model**
- File: `src/models/execution.py`
- Dependencies: Command model, datetime
- Fields: id, command, start_time, end_time, exit_code, status
- Validation: status must be pending|running|success|error

**T009: OutputLine Model**
- File: `src/models/output.py`
- Dependencies: datetime, enum
- Fields: id, execution_id, timestamp, stream (stdout/stderr), content
- Validation: Non-empty content, valid stream type

**T010: AppConfig Model**
- File: `src/models/config.py`
- Dependencies: pydantic
- Fields: theme, refresh_rate, log_level, command_timeout, max_output_lines
- Defaults: theme='dark', refresh_rate=1.0, log_level='INFO', timeout=300, max_lines=10000

**T011: Config Root Model**
- File: `src/models/__init__.py` (update)
- Combines AppConfig, commands list
- Serialization support (to_dict)

### Exception Layer (T012)

**T012: Custom Exceptions**
- File: `src/exceptions.py`
- Types: ConfigError, ExecutionError, TimeoutError, ValidationError
- Parent class: OpsException (inherits Exception)
- Use in: ConfigLoader validation, CommandRunner execution

### Service Interfaces (T013-T014)

**T013: ConfigLoader Interface**
- File: `src/services/config.py`
- Methods: load(path: str) → Config, validate(config: Config) → bool
- Behavior: Load YAML, validate against schema, return Config object
- Uses: Pydantic, PyYAML

**T014: ConfigLoader Implementation**
- Extends service interface
- Handles missing files, invalid YAML, validation errors
- Raises ConfigError on failure
- Test: Load commands.yaml successfully

### Message System (T015)

**T015: Textual Messages**
- File: `src/messages.py`
- Classes: CommandOutput, StatusUpdate, ExecutionComplete, CommandError
- Parent: textual.message.Message
- Payload: execution_id, content/status/output
- Use: Widget-to-widget communication

### UI Layout (T016)

**T016: Base CSS Layout**
- File: `src/styles/app.css`
- Elements: Header, footer, output pane, command panel
- Grid layout: header (5 rows), body (scrollable), footer (3 rows)
- Colors: dark theme with accent (blue/cyan)

## Dependency Graph

```
All Phase 2 tasks depend on Phase 1 ✅

T007 (Command)
    ↓
T008 (Execution uses Command)
T009 (OutputLine)
    ↓
T010 (AppConfig)
T011 (Config root - uses all models)
    ↓
T012 (Exceptions - independent)
T013 (ConfigLoader interface - independent)
    ↓
T014 (ConfigLoader impl - uses exceptions, config)
T015 (Messages - independent)
T016 (CSS layout - independent)

Execution order: 7→8→9→10→11 (sequential)
Then: 12,13 parallel; 14 after 13; 15,16 parallel
```

## File Checklist

Before Phase 2:
- [ ] Phase 1 post-implementation doc created
- [ ] All Phase 1 tasks marked complete in tasks.md

Phase 2 deliverables:
- [ ] `src/models/command.py` - Command Pydantic model
- [ ] `src/models/execution.py` - Execution Pydantic model
- [ ] `src/models/output.py` - OutputLine Pydantic model
- [ ] `src/models/config.py` - AppConfig Pydantic model
- [ ] `src/models/__init__.py` - Updated with Config root model
- [ ] `src/exceptions.py` - Custom exception classes
- [ ] `src/services/config.py` - ConfigLoader service
- [ ] `src/messages.py` - Textual message classes
- [ ] `src/styles/app.css` - Base layout

Phase 2 validation:
- [ ] Ruff check passes
- [ ] Mypy type check passes
- [ ] All models import without errors
- [ ] ConfigLoader loads commands.yaml
- [ ] Pytest discovery works

## Reference Materials

- **data-model.md**: Entity definitions
- **contracts/config_loader.md**: ConfigLoader interface spec
- **contracts/command_runner.md**: CommandRunner interface spec
- **commands.yaml**: Example config for loading test

## Assumptions

- PyYAML for YAML parsing (in pyproject.toml)
- Pydantic v2 for models (installed in Phase 1)
- Textual for message system (installed in Phase 1)
- Python 3.10+ type hints (PEP 604 union syntax)

## Success Criteria

✅ All 10 models and services implemented  
✅ Custom exception hierarchy complete  
✅ ConfigLoader successfully loads example YAML  
✅ Textual messages defined  
✅ Base CSS layout created  
✅ Ruff linting passes  
✅ Type checking (mypy) passes  
✅ Imports work without circular dependencies  

## Execution Strategy

1. Create models first (T007-T011) - bottom-up dependency order
2. Create exceptions (T012) - needed by services
3. Create service interfaces and implementations (T013-T014)
4. Create message and UI (T015-T016) - can run parallel with services

**Execution Time**: ~90 minutes  
**Parallelizable**: T012, T013, T015, T016 can run after their dependencies

