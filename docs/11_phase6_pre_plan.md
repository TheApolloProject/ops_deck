# Phase 6 Pre-Implementation Plan: User Story 4 - Configuration

**Date**: 2025-12-28  
**Phase**: 6 of 7  
**Duration Estimate**: 50 minutes

## Overview

Phase 6 implements User Story 4: "As a DevOps engineer, I can create custom commands by editing YAML configuration, restart the app, and see them in the command palette with descriptions." This adds configuration flexibility and error handling.

## Phase Scope

| Area | Tasks | Deliverables |
|------|-------|--------------|
| UI Enhancement | T037 (1 task) | Command descriptions in palette |
| Error Handling | T038 (1 task) | Better config error messages |
| Error Display | T039 (1 task) | Startup error screen |
| Documentation | T040 (1 task) | README with config format |

**Total Tasks**: 4 tasks

## Task Breakdown

### Command Descriptions (T037)

**T037: Add command description display**
- File: `src/widgets/command_list.py` (update)
- Show command description in palette
- Display as tooltip or subtitle
- Truncate if too long
- Format: "name: description"
- Update render logic to include descriptions

### Error Messages (T038)

**T038: Improve ConfigValidationError messages**
- File: `src/services/config.py` (update)
- Add line number to error messages
- Include validation context
- Format: "Line X: {error message}"
- Show which field failed
- Provide hint for resolution

### Error Screen (T039)

**T039: Add startup error screen**
- File: `src/widgets/app.py` (update)
- Catch config errors on startup
- Display error screen instead of crashing
- Show error message clearly
- Include recovery instructions
- Exit gracefully with error code

### Documentation (T040)

**T040: Document configuration format**
- File: `README.md` (create/update)
- Command YAML format
- Configuration fields
- Example commands
- Validation rules
- Common errors

## Dependencies

```
T037 (Descriptions) → independent, CommandListPanel
T038 (Error messages) → independent, ConfigLoader
T039 (Error screen) → independent, OpsApp
T040 (Documentation) → independent, README

Can run mostly in parallel:
37, 38, 39, 40
No file conflicts, additive changes
```

## File Checklist

Before Phase 6:
- [x] Phase 5 post-implementation doc created
- [x] All Phase 5 tests passing (14/14)
- [x] Parallel execution infrastructure ready
- [x] Auto-scroll with scroll-lock working

Phase 6 modifications:
- [ ] `src/widgets/command_list.py` - Add description display
- [ ] `src/services/config.py` - Improve error messages
- [ ] `src/widgets/app.py` - Add startup error handling
- [ ] `README.md` - Configuration documentation

Phase 6 validation:
- [ ] Descriptions display in command palette
- [ ] Config errors show line numbers
- [ ] Startup error screen displays correctly
- [ ] README documents configuration
- [ ] All Phase 5 tests still pass
- [ ] Ruff check passes

## Reference Materials

- **Phase 5 command_list.py**: Current command display with spinner
- **Phase 4 config.py**: Current ConfigLoader implementation
- **Phase 5 app.py**: Current OpsApp structure
- **commands.yaml**: Example configuration file

## Key Features

### Command Descriptions
- ✅ Display description for each command
- ✅ Format: "name: description"
- ✅ Truncate long descriptions
- ✅ Visual separation in palette

### Error Messages
- ✅ Include line numbers from YAML
- ✅ Show field that failed
- ✅ Provide context
- ✅ Suggest fixes

### Error Screen
- ✅ Display on config errors
- ✅ Show error message
- ✅ No crash/traceback
- ✅ Exit gracefully

### Documentation
- ✅ Configuration format guide
- ✅ Example commands
- ✅ Field definitions
- ✅ Common errors and fixes

## Success Criteria

✅ Command descriptions display in palette  
✅ Config errors show line numbers  
✅ Invalid config shows error screen  
✅ README documents configuration  
✅ All Phase 5 tests still pass  
✅ Ruff linting passes  
✅ No breaking changes to Phase 5  

## Testing Strategy

**Manual Testing**:
1. Edit commands.yaml → add new command with description
2. Restart app → should see description in palette
3. Break YAML syntax → should show error with line number
4. Missing required field → should show specific error
5. Invalid timeout value → should show validation error

**Automated Testing** (Phase 7):
- Test error message formatting
- Test line number extraction
- Test app startup with invalid config
- Test description truncation

## Execution Plan

1. Add description display to command palette (T037)
2. Improve config error messages with line numbers (T038)
3. Add startup error screen (T039)
4. Write configuration documentation in README (T040)
5. Validate all changes work together
6. Run full test suite

**Execution Time**: ~50 minutes  
**Parallelizable**: 37, 38, 39 can run in parallel after 40

## Architecture Impact

- **No new files**: Only modifications to existing modules
- **No new models**: Reuses existing Command/Execution
- **Error handling**: Enhanced ConfigLoader error reporting
- **UI updates**: Command list shows descriptions

## Known Limitations & Notes

- Line numbers require YAML parser context
- Description truncation fixed at character limit
- Error screen doesn't auto-recover (restart needed)
- No config hot-reload (restart required)

## Assumptions

- ConfigLoader can extract line numbers from YAML
- Command descriptions already in models
- OpsApp can catch and handle startup errors
- README.md exists at repository root

## Risk Assessment

**Low Risk**:
- ✅ All changes are additive
- ✅ No existing APIs modified
- ✅ Error handling is backwards compatible
- ✅ Documentation is informational only

**Testing Coverage**:
- ✅ Manual testing for all features
- ✅ Integration tests verify no regressions
- ✅ Configuration validation tests

