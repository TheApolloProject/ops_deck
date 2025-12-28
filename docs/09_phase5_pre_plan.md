# Phase 5 Pre-Implementation Plan: User Story 3 - Responsive UI

**Date**: 2025-12-28  
**Phase**: 5 of 7  
**Duration Estimate**: 60 minutes

## Overview

Phase 5 implements User Story 3: "As a user, I can start multiple long-running commands and interact with the UI while they execute, with live status indicators." This build upon Phase 4's error handling to add responsive UI and parallel execution support.

## Phase Scope

| Area | Tasks | Deliverables |
|------|-------|--------------|
| Parallel Execution | T033 (1 task) | Verify exclusive=False for concurrent commands |
| Status Indication | T034 (1 task) | Running spinner for active executions |
| Auto-scroll | T035 (1 task) | Bottom scroll with user scroll-lock detection |
| Command Headers | T036 (1 task) | Command name and start time display |

**Total Tasks**: 4 tasks

## Task Breakdown

### Parallel Execution (T033)

**T033: Verify @work(exclusive=False) allows parallel execution**
- File: `src/widgets/app.py` (verify/update)
- Check that multiple commands can execute concurrently
- Ensure Textual workers don't block each other
- Test with 2+ simultaneous commands
- No changes needed if already configured correctly

### Status Indication (T034)

**T034: Add execution status indicator (running spinner)**
- File: `src/widgets/command_palette.py` (update)
- Add running spinner next to executing commands
- Show which command is currently running
- Use Textual's spinner animation
- Display in command list or header area
- Update when execution completes

### Auto-scroll (T035)

**T035: Implement auto-scroll with scroll-lock**
- File: `src/widgets/output_view.py` (update)
- Auto-scroll to bottom as output arrives
- Detect user manual scroll
- Lock auto-scroll when user scrolls up
- Resume auto-scroll when user reaches bottom
- Prevent jarring scrolling during interaction

### Command Headers (T036)

**T036: Add command header with name and start time**
- File: `src/widgets/output_view.py` (update)
- Display when execution begins
- Show: "[START] Command Name at HH:MM:SS"
- Color: info/accent color
- Timestamp in ISO format or human-readable
- Separator before output lines

## Dependencies

```
T033 (Parallel execution) → independent, verify existing
T034 (Running spinner) → independent, CommandPalette
T035 (Auto-scroll) → independent, OutputView
T036 (Command headers) → independent, OutputView

Can run mostly in parallel with proper sequencing:
33 (verify), 34, 35, 36
All modifications are additive, no conflicts
```

## File Checklist

Before Phase 5:
- [x] Phase 4 post-implementation doc created
- [x] All Phase 4 tests passing (14/14)
- [x] CommandRunner with dual-stream capture working
- [x] OutputPane with status indicators ready

Phase 5 modifications:
- [ ] `src/widgets/app.py` - Verify parallel execution setup
- [ ] `src/widgets/command_palette.py` - Add running spinner indicator
- [ ] `src/widgets/output_view.py` - Auto-scroll and command headers

Phase 5 validation:
- [ ] Multiple commands can run concurrently
- [ ] Spinner shows for running commands
- [ ] Auto-scroll works correctly
- [ ] Command headers display properly
- [ ] All Phase 4 tests still pass
- [ ] Ruff check passes

## Reference Materials

- **Phase 4 output_view.py**: Current output display with completion handling
- **Phase 4 command_runner.py**: Async execution with callbacks
- **Textual docs**: Worker patterns, reactive properties
- **src/widgets/command_palette.py**: Command list display

## Key Features

### Parallel Execution
- ✅ Multiple commands run simultaneously
- ✅ Each command streams independently
- ✅ UI remains responsive

### Status Indicators
- ✅ Running spinner shows active commands
- ✅ Visual feedback for user
- ✅ Auto-updates on completion

### Auto-scroll
- ✅ Automatically follows output
- ✅ User can scroll up to review
- ✅ Resumes auto-scroll when needed
- ✅ Smooth, non-jarring animation

### Command Headers
- ✅ Command name and start time
- ✅ Clear separation between executions
- ✅ Aids in log reading and debugging

## Success Criteria

✅ Multiple commands execute in parallel  
✅ Spinner shows for running commands  
✅ Auto-scroll works with scroll detection  
✅ Command headers display with timestamps  
✅ All Phase 4 tests still pass  
✅ Ruff linting passes  
✅ No breaking changes to Phase 4  

## Testing Strategy

**Manual Testing**:
1. Run two commands simultaneously → should both run
2. Run long command (sleep 10) → should see spinner
3. Run command, scroll up → should stop auto-scrolling
4. Scroll to bottom → should resume auto-scrolling
5. New command → should show header with name and time

**Automated Testing** (Phase 7):
- Test spinner display
- Test scroll position tracking
- Test command header formatting

## Execution Plan

1. Verify parallel execution capability (T033)
2. Add spinner indicator (T034)
3. Implement auto-scroll with scroll-lock (T035)
4. Add command headers (T036)
5. Validate all changes work together
6. Run full test suite

**Execution Time**: ~60 minutes  
**Parallelizable**: 34, 35, 36 can be done in parallel after 33

## Architecture Impact

- **No new files**: Only modifications to existing widgets/app
- **No new models**: Reuses existing Execution/OutputLine
- **Message usage**: Leverages Phase 2-4 message system
- **Service layer**: No changes to CommandRunner

## Known Limitations & Notes

- Spinner animation depends on terminal capability
- Scroll detection may vary by terminal/OS
- Auto-scroll doesn't affect sorting/filtering (not implemented yet)
- No pause/resume functionality (future)

## Assumptions

- Textual @work decorator already supports exclusive parameter
- Command palette widget can be updated to show indicators
- Output view can track scroll position
- Timestamps can be formatted client-side

## Risk Assessment

**Low Risk**:
- ✅ All changes are additive
- ✅ No existing APIs modified
- ✅ Well-tested Textual patterns
- ✅ Clear backwards compatibility

**Testing Coverage**:
- ✅ Unit tests for scroll detection
- ✅ Integration tests for parallel execution
- ✅ Manual UI testing for spinners

