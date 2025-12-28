# Phase 3 Pre-Implementation Plan: User Story 1 MVP - Command Execution

**Date**: 2025-12-28  
**Phase**: 3 of 7  
**Duration Estimate**: 120 minutes

## Overview

Phase 3 implements the first user story (US1): "As a DevOps engineer, I can execute CLI commands and see their output in real-time." This is the MVP that enables core application functionality - command execution with streaming output.

## Phase Scope

| Area | Tasks | Deliverables |
|------|-------|--------------|
| Command Runner | T017-T019 (3 tasks) | Async subprocess executor with output streaming |
| Textual Application | T020-T022 (3 tasks) | Main app widget, command selection, output display |
| Message Integration | T023-T024 (2 tasks) | Connect message system to widgets, event handlers |
| Testing | T025-T026 (2 tasks) | Unit tests for CommandRunner, integration tests for app |

## Task Breakdown

### Command Runner Service (T017-T019)

**T017: CommandRunner Interface**
- File: `src/services/command_runner.py`
- Abstract base class: ABC with abstract method `run(command, callback)`
- Callback signature: `async def callback(output_line: OutputLine) -> None`
- Dependency: Command, OutputLine, Execution models

**T018: CommandRunner Implementation**
- Full async subprocess implementation
- Create Execution object with ID and timestamps
- Spawn subprocess with `asyncio.create_subprocess_exec`
- Capture stdout and stderr separately
- Call callback for each output line
- Handle timeouts and process termination
- Set exit code and final status
- Raises ExecutionError on failure

**T019: Output Streamer**
- Helper function: `async stream_output(reader, execution_id, stream_type) -> AsyncIterator[OutputLine]`
- Reads from subprocess pipe (stdout or stderr)
- Creates OutputLine objects with timestamps
- Handles binary-to-text conversion (UTF-8 with error handling)
- Yields OutputLine objects as they arrive

### Textual Application (T020-T022)

**T020: Main Application Widget**
- File: `src/widgets/app.py`
- Class: `OpsApp(App)`
- Compose method: creates Header, Main content, Footer
- CSS binding: links to src/styles/app.css
- Key bindings: Ctrl+C to quit, Enter to execute, Up/Down for navigation
- Action methods: action_quit(), action_execute(), action_navigate()

**T021: Command List Widget**
- File: `src/widgets/command_list.py`
- Class: `CommandListPanel(Container)`
- Displays list of available commands
- Show name and description
- Highlight selected command
- Post StatusUpdate message on selection
- Respond to Up/Down key events

**T022: Output Display Widget**
- File: `src/widgets/output_pane.py`
- Class: `OutputPane(Container)`
- Scrollable container for output lines
- Render OutputLine objects as formatted text
- Color code stdout (white) vs stderr (red)
- Auto-scroll to bottom on new output
- Show loading spinner during execution
- Show status/error messages

### Message Integration (T023-T024)

**T023: App Message Handlers**
- File: `src/widgets/app.py` (update)
- Methods: on_command_output(), on_status_update(), on_execution_complete()
- Command execution flow:
  1. User selects command → StatusUpdate(PENDING)
  2. App executes command → CommandStarted + Execution
  3. CommandRunner produces CommandOutput messages
  4. Display each output line
  5. CommandRunner produces ExecutionComplete
  6. Update status and show summary

**T024: Widget Communication**
- Command list → App: StatusUpdate(command_selected)
- App → CommandRunner: Execute selected command
- CommandRunner → Output pane: CommandOutput messages
- CommandRunner → App: ExecutionComplete message
- App → Status bar: StatusUpdate messages

### Testing (T025-T026)

**T025: CommandRunner Unit Tests**
- File: `tests/unit/test_command_runner.py`
- Test: Simple echo command execution
- Test: Capture stdout and stderr separately
- Test: Output streaming callback
- Test: Timeout handling
- Test: Process exit codes

**T026: Application Integration Tests**
- File: `tests/integration/test_app.py`
- Test: App initialization
- Test: Command list loading
- Test: Command execution flow
- Test: Message passing between widgets

## Dependency Graph

```
Phase 2 complete ✅

T017 (CommandRunner interface) → independent
T018 (Implementation uses T017)
T019 (Output Streamer - uses Execution, OutputLine)
  ↓
T020 (Main App - uses models, messages)
T021 (Command List - independent widget)
T022 (Output Pane - independent widget)
  ↓
T023 (Message handlers - uses T020, T018)
T024 (Widget communication - orchestrates T021, T022, T023)
  ↓
T025 (CommandRunner tests - uses T017, T018, T019)
T026 (App integration tests - uses T020-T024)

Sequential execution: 17→18→19→20→21→22→23→24→25→26
Parallel opportunities: T020 and T021 can run parallel (after T019 completes)
```

## File Checklist

Before Phase 3:
- [ ] Phase 2 post-implementation doc created
- [ ] All Phase 2 tasks marked complete in tasks.md
- [ ] All Phase 2 code passing ruff/mypy checks

Phase 3 deliverables:
- [ ] `src/services/command_runner.py` - CommandRunner interface + implementation
- [ ] `src/widgets/app.py` - Main Textual application
- [ ] `src/widgets/command_list.py` - Command selection widget
- [ ] `src/widgets/output_pane.py` - Output display widget
- [ ] `src/widgets/__init__.py` - Widget exports
- [ ] `tests/unit/test_command_runner.py` - CommandRunner tests
- [ ] `tests/integration/test_app.py` - Integration tests

Phase 3 validation:
- [ ] Ruff check passes
- [ ] Mypy type check passes
- [ ] All imports work without errors
- [ ] pytest discovers all tests
- [ ] CommandRunner executes simple command
- [ ] App widget initializes
- [ ] Message passing works
- [ ] Tests pass (unit + integration)

## Reference Materials

- **Phase 2 models**: Command, Execution, OutputLine, AppConfig
- **Phase 2 services**: ConfigLoader
- **Phase 2 messages**: CommandOutput, StatusUpdate, ExecutionComplete
- **Textual docs**: Widget composition, message system, key bindings
- **asyncio docs**: asyncio.create_subprocess_exec, stream reading patterns

## Assumptions

- Python 3.10+ (asyncio context managers work)
- Textual 0.20+ (modern message system)
- Commands run in shell context (no special escaping needed)
- Output encoding is UTF-8
- Subprocess inherits parent environment

## Success Criteria

✅ CommandRunner executes commands asynchronously  
✅ Output captured and streamed via messages  
✅ Main app widget initializes and displays  
✅ Command list populated from configuration  
✅ User can select and execute commands  
✅ Output displays in real-time  
✅ Timeout handling works  
✅ Messages pass between components  
✅ All unit tests pass  
✅ Integration tests pass  
✅ Ruff linting passes  
✅ Type checking passes  

## Execution Strategy

1. Implement CommandRunner service first (T017-T019)
   - Non-UI code, easier to test
   - Can be tested independently with pytest

2. Implement Textual widgets (T020-T022)
   - Main app structure
   - Individual widgets
   - Can test each widget in isolation

3. Integrate messaging (T023-T024)
   - Connect widgets together
   - Test message flow

4. Write tests (T025-T026)
   - Unit tests for CommandRunner
   - Integration tests for message flow
   - Full app interaction tests

**Execution Time**: ~120 minutes  
**Parallelizable**: After T019, widgets can be developed in parallel; after widgets, message integration and tests can overlap

## Key Challenges

1. **Async output streaming**: Handling streams from subprocess without blocking
2. **Message ordering**: Ensuring messages arrive in correct order
3. **Thread safety**: If using threads for subprocess I/O
4. **Widget layout**: CSS grid system with docking
5. **State management**: Tracking execution state across widgets

## Notes

- US1 is critical path - all other user stories depend on working command execution
- Focus on MVP: select command → execute → see output
- Error handling for Phase 4 (US2)
- Performance optimization for Phase 6
- Logging and observability for Phase 7

