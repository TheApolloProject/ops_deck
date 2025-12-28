# Phase 4 Pre-Implementation Plan: User Story 2 - Error Handling

**Date**: 2025-12-28  
**Phase**: 4 of 7  
**Duration Estimate**: 90 minutes

## Overview

Phase 4 implements User Story 2: "As a DevOps engineer, I can distinguish between successful and failed command executions, with stderr displayed differently." This builds on Phase 3's working MVP to add error visibility and command status indicators.

## Phase Scope

| Area | Tasks | Deliverables |
|------|-------|--------------|
| Error Display | T027-T028 (2 tasks) | CSS styling for stderr, stream-specific formatting |
| Status Indication | T029-T031 (3 tasks) | Success/error indicators, completion handling |
| Service Updates | T032 (1 task) | ExecutionCompleted message posting |

**Total Tasks**: 6 tasks (this phase focuses on error handling, not execution)

## Task Breakdown

### Error Display Styling (T027-T028)

**T027: Add stdout/stderr CSS classes**
- File: `src/styles/app.css`
- Add stream-specific CSS classes:
  - `.output-line.stdout`: White/normal text
  - `.output-line.stderr`: Red or orange with bold
  - `.output-line.success`: Green indicator
  - `.output-line.error`: Red indicator
- Optional: Add icons or symbols for visual distinction

**T028: Update OutputPane to apply stream-specific CSS**
- File: `src/widgets/output_pane.py` (update)
- Modify `_format_output_line()` to include CSS class
- Apply class based on `OutputLine.stream` enum
- Render different colors for stdout vs stderr
- Use Textual's text styling system

### Status Indication (T029-T031)

**T029: Add ExecutionCompleted message handling**
- File: `src/widgets/output_pane.py` (update)
- Handle ExecutionCompleted message
- Extract exit code from Execution
- Display status message at end of output

**T030: Display success indicator**
- File: `src/widgets/output_pane.py` (update)
- On exit code == 0:
  - Add "✓ Command succeeded" or similar
  - Color green
  - Timestamp of completion

**T031: Display error indicator**
- File: `src/widgets/output_pane.py` (update)
- On non-zero exit code:
  - Add "✗ Command failed with exit code X" or similar
  - Color red
  - Timestamp of completion

### Service Updates (T032)

**T032: Update CommandRunner to post ExecutionCompleted**
- File: `src/services/command_runner.py` (update)
- After execution completes, send ExecutionCompleted message
- Include final Execution object with exit code
- Should be called whether success or failure

## Dependencies

```
Phase 3 complete ✅

T027 (CSS classes) → independent
T028 (Apply classes) → uses T027
T029 (Handle completion) → independent
T030 (Success indicator) → uses T029
T031 (Error indicator) → uses T029
T032 (Runner update) → uses Phase 3 models

Execution order: 27→28, 29→30, 29→31, 32
All can run mostly in parallel with proper ordering
```

## File Checklist

Before Phase 4:
- [x] Phase 3 post-implementation doc created
- [x] All Phase 3 tests passing (14/14)
- [x] AsyncCommandRunner working

Phase 4 modifications:
- [ ] `src/styles/app.css` - CSS classes for streams
- [ ] `src/widgets/output_pane.py` - Stream-specific styling and completion handling
- [ ] `src/services/command_runner.py` - ExecutionCompleted messaging

Phase 4 validation:
- [ ] CSS classes defined and used
- [ ] stderr lines display in different color
- [ ] Success/error indicators show
- [ ] All Phase 3 tests still pass
- [ ] Ruff check passes

## Reference Materials

- **Phase 3 output_pane.py**: Current output display implementation
- **Phase 3 command_runner.py**: Current execution service
- **src/messages.py**: ExecutionComplete message definition
- **src/styles/app.css**: Existing Textual CSS

## Key Features

### Error Visualization
- ✅ Distinct stderr color (red/orange)
- ✅ Success indicator (green checkmark)
- ✅ Error indicator (red X with exit code)
- ✅ Completion status display

### Implementation Details

**CSS Strategy**:
- Use Textual's color system
- Add to existing `.output-line` class
- Create `.stdout`, `.stderr`, `.success`, `.error` variants

**Widget Updates**:
- OutputPane.add_output_line() applies correct class
- New method: format_completion_message(execution)
- Handle ExecutionComplete message

**Service Integration**:
- CommandRunner.run() already captures exit code
- Just need to post ExecutionCompleted message

## Success Criteria

✅ stderr displays in distinct color  
✅ Success indicator shows on exit code 0  
✅ Error indicator shows on non-zero exit  
✅ Completion message includes exit code  
✅ All Phase 3 tests still pass  
✅ Ruff linting passes  
✅ No breaking changes to Phase 3  

## Testing Strategy

**Manual Testing**:
1. Run command with stdout only → white text
2. Run command with stderr (e.g., `ls /nonexistent`) → red text
3. Run successful command → "✓ Command succeeded"
4. Run failing command → "✗ Command failed with exit code X"

**Automated Testing** (Phase 7):
- Test CSS class application
- Test message handling
- Test exit code extraction

## Execution Plan

1. Add CSS classes first (T027)
2. Update OutputPane styling (T028)
3. Add ExecutionCompleted handling (T029)
4. Add success/error indicators (T030-T031)
5. Update CommandRunner to post messages (T032)
6. Validate all changes work together

**Execution Time**: ~90 minutes  
**Parallelizable**: Limited - CSS and indicator tasks can overlap

## Architecture Impact

- **No new files**: Only modifications to existing widgets/services
- **Message usage**: Leverages Phase 2 message system
- **CSS expansion**: Minimal additions to existing stylesheet
- **Service layer**: Just needs to post existing message

## Known Limitations & Notes

- No error recovery UI yet (Phase 5)
- No retry mechanism (Future)
- No error log persistence (Phase 6)
- Limited to single command execution (Phase 5 adds concurrency)

## Assumptions

- Textual rendering supports color in terminal
- ExecutionCompleted message already defined (Phase 2)
- OutputPane can receive and handle messages
- CSS classes properly override defaults

