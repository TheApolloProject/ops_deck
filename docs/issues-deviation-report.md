# Issues and Specification Deviation Report

**Project**: Ops Deck - TUI CLI Dashboard  
**Report Date**: January 4, 2026  
**Spec Reference**: `/specs/001-tui-cli-dashboard/`  
**Issues Analyzed**: 11 distinct issues across 24 files in `/issues/`

---

## Executive Summary

This report analyzes all documented issues encountered during the implementation of the TUI CLI Dashboard and maps each to specific deviations from the original specifications, tasks, and research documentation. The issues fall into **four major categories**:

| Category | Issues | Root Cause Pattern |
|----------|--------|-------------------|
| Environment Setup | #001-#003 | Documentation gaps and platform-specific assumptions |
| CSS/Styling | #004-#008 | Wrong file extension, syntax errors, and framework misunderstanding |
| Theme System | #008-#010 | Incorrect Textual API usage |
| Command Execution | #011 | Empty implementation and worker misconfiguration |

---

## Issue Analysis by Category

### Category 1: Environment Setup Issues (#001-#003)

#### Issue #001: Python Command Not Found

**Error**: `bash: python: command not found`

**Specification Reference**:
- [quickstart.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/quickstart.md#L64): Documents `python -m src.app` as the run command

**Deviation Analysis**:
| What the Spec Said | What Was Actually Needed | 
|-------------------|-------------------------|
| "Run with `python -m src.app`" | Modern Linux systems require `python3` explicitly |

**Root Cause**: Documentation assumed `python` symlink exists, which is not true on modern Debian/Ubuntu systems where Python 2 has been deprecated.

**Preventive Measure Missing**: The quickstart should have specified `python3` or included a system check.

---

#### Issue #002: Missing Textual Module

**Error**: `ModuleNotFoundError: No module named 'textual'`

**Specification Reference**:
- [quickstart.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/quickstart.md#L24-L32): Lists installation commands
- [plan.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/plan.md#L12-L13): Lists primary dependencies

**Deviation Analysis**:
| Spec Said | Actual Implementation |
|-----------|----------------------|
| "Install with `pip install textual pyyaml pydantic`" | Dependencies were not installed before running |

**Root Cause**: User attempted to run application before completing the setup steps. The error message assumed the user would know to install dependencies.

**Task Deviation**: [tasks.md T002](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/tasks.md#L23) marks `pyproject.toml` creation as complete but doesn't enforce installation verification.

---

#### Issue #003: Externally Managed Environment (PEP 668)

**Error**: `error: externally-managed-environment`

**Specification Reference**:
- [quickstart.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/quickstart.md#L14-L20): Virtual environment setup instructions

**Deviation Analysis**:
| Spec Said | What Happened |
|-----------|--------------|
| Create venv with `python3 -m venv .venv` | User environment may have been created with restricted Python |

**Root Cause**: The spec didn't account for PEP 668 restrictions in Debian-managed Python 3.12+ installations. The `python3-full` package may not have been installed.

**Missing from Spec**: No mention of `python3-full` requirement or troubleshooting steps for PEP 668.

---

### Category 2: CSS and Styling Issues (#004-#008)

#### Issue #004: CSS File Not Found

**Error**: CSS file path could not be resolved

**Specification Reference**:
- [plan.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/plan.md#L74): Specifies `src/styles/app.tcss`
- [research.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md#L153): Shows examples using `.tcss` extension

**Deviation Analysis**:
| Spec Said | What Was Implemented |
|-----------|---------------------|
| `src/styles/app.tcss` | Likely `src/styles/app.css` or path mismatch |

**Root Cause**: The CSS file was either created with wrong extension or the app referenced the wrong path.

**Task Reference**: [T016](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/tasks.md#L48) correctly specifies `.tcss` extension.

---

#### Issue #005: Invalid CSS Syntax - Python Docstring

**Error**: `Expected selector or end of file (found '"""Base CSS layout...')`

**Specification Reference**:
- [research.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md#L153-L191): Shows proper CSS comment syntax with `/* */`

**Deviation Analysis**:
| Spec Said | What Was Implemented |
|-----------|---------------------|
| CSS comments use `/* ... */` | File started with Python docstring `"""..."""` |

**Root Cause**: **Copy-paste error** or **incorrect file creation**. The CSS file was started as if it were a Python file, using Python docstring syntax instead of CSS comment syntax.

**Critical Deviation**: This represents a fundamental misunderstanding of file formats. The spec clearly shows CSS syntax in research.md, but implementation used Python syntax.

---

#### Issue #006: CSS Variable Reference Errors

**Error**: `reference to undefined variable '$muted'`

**Specification Reference**:
- [research.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md#L176-L190): Shows valid Textual CSS variables

**Valid Variables Listed in Spec**:
```css
$surface, $text, $error, $success, $primary
```

**Deviation Analysis**:
| Spec Variables | Variables Used in Implementation |
|----------------|--------------------------------|
| `$text`, `$text-muted` (not in spec) | `$muted` (invented, non-existent) |
| `$accent` (implicit) | `$info` (invented, non-existent) |

**Root Cause**: Implementation invented CSS variables that don't exist in Textual's theme system. The spec's research.md showed example variables, but the implementation used different names.

**5 Occurrences**:
- Line 34: `#subtitle { color: $muted; }` → should be `$text-muted`
- Line 75: `#output-header { color: $muted; }` → should be `$text-muted`
- Line 108: `.output-line.info { color: $info; }` → should be `$accent`
- Line 145: `#status-indicator .status-item.idle { color: $muted; }` → should be `$text-muted`
- Line 155: `#help-bar { color: $muted; }` → should be `$text-muted`

---

#### Issue #007: Invalid Border Syntax

**Error**: `border: solid $text 50%;` - Invalid opacity parameter

**Specification Reference**:
- [research.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md#L167): Shows `border-right: solid $primary;`

**Deviation Analysis**:
| Spec Pattern | Implementation |
|--------------|---------------|
| `border: solid $primary;` | `border: solid $text 50%;` with opacity |

**Root Cause**: Implementation attempted to use CSS opacity syntax (`50%`) which is **not supported by Textual's CSS parser**. Standard web CSS knowledge was incorrectly applied to Textual CSS.

**2 Occurrences**:
- Line 94: `#output-container`
- Line 234: `Modal > Container > Static`

---

#### Issue #008: CSS Code Quality Issues

**Identified Issues**:
1. Incomplete border declarations (missing color)
2. Duplicated styling patterns
3. Hardcoded magic numbers
4. Missing hover/focus states
5. Accessibility concern with `text-style: blink`

**Specification Reference**:
- [spec.md FR-007](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/spec.md#L92): "System MUST remain responsive"

**Deviation from Quality Standards**:
The spec's Constitution Check in [plan.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/plan.md#L26-L32) emphasizes:
- **Principle V: Simplicity & YAGNI**

The CSS implementation contains:
- Magic numbers without documentation (lines 46, 218: hardcoded widths)
- Duplicate selectors that violate DRY (lines 110 vs 123)
- Accessibility-problematic `blink` text style (line 162)

---

### Category 3: Theme System Issues (#008-#010)

#### Issue #008 (Theme): InvalidThemeError - Theme 'dark' Not Registered

**Error**: `InvalidThemeError: Theme 'dark' has not been registered`

**Specification Reference**:
- [research.md §1](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md#L19-L43): Documents Textual worker pattern but **does not document theme system**

**Deviation Analysis**:
| What Resolution Was | What Spec Said About Themes |
|--------------------|---------------------------|
| Textual requires `App.register_theme()` before setting themes | **Nothing** - Theme configuration not covered in spec |

**Root Cause**: **Spec gap**. The specification documents Textual's worker pattern, CSS layout, and configuration loading, but **completely omits the theme registration system**. Implementation attempted to set themes without understanding Textual's registration requirement.

---

#### Issue #009: AttributeError - 'theme_names' Not Found

**Error**: `AttributeError: 'OpsApp' object has no attribute 'theme_names'`

**Specification Reference**: None - this was an attempted fix for Issue #008

**Deviation Analysis**:
This issue was a **cascading failure** from Issue #008. The fix attempted to use a non-existent `self.theme_names` attribute to validate themes before setting them.

**Root Cause**: Incorrect assumption about Textual's API based on incomplete framework knowledge.

---

#### Issue #010: Theme Fallback Also Fails

**Error**: Even fallback to `'dark'` theme raises `InvalidThemeError`

**Specification Reference**: None - theme system undocumented

**Deviation Analysis**:
| Attempted Solution | Why It Failed |
|-------------------|--------------|
| Try theme → catch error → fallback to 'dark' | 'dark' is also not registered by default |

**Root Cause**: **Fundamental misunderstanding of Textual's theme system**. Built-in themes like 'dark' are not automatically available and must be explicitly registered or the theme setting should be skipped entirely.

**Missing from Research**: [research.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md) researched 5 topics but theme handling was not one of them.

---

### Category 4: Command Execution Issues (#011)

#### Issue #011: Command Execution Not Triggered + Worker Configuration Error

**Errors**:
1. Pressing Enter on a command does nothing
2. `WorkerError: Request to run a non-async function as an async worker`

**Specification Reference**:
- [spec.md FR-002](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/spec.md#L87): "System MUST execute the selected command as a shell subprocess"
- [research.md §1](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md#L29-L41): Shows `@work` decorator pattern with `exclusive=False`
- [tasks.md T024](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/tasks.md#L69): "Implement App.on_command_selected handler to start worker"
- [tasks.md T025](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/tasks.md#L70): "Implement @work decorated execute_command worker"

**Deviation Analysis**:

| Task Requirement | Actual Implementation |
|-----------------|----------------------|
| T024: `action_execute` should run command | `action_execute()` method was **empty** |
| T025: Use `@work(exclusive=False)` async pattern | Used sync function without `thread=True` |

**Detailed Root Cause**:

1. **Empty Implementation**: The `action_execute` method that should trigger command execution was implemented as an empty stub:
   ```python
   async def action_execute(self) -> None:
       pass  # ← Nothing here!
   ```

2. **Worker Configuration**: When implementation was added, it used:
   ```python
   self.run_worker(run_command)  # ❌ sync function without thread=True
   ```
   Instead of what the spec researched:
   ```python
   self.run_worker(run_command, thread=True)  # ✅ correct for sync functions
   ```

**Spec vs Implementation Comparison**:

| research.md Pattern | Actual Implementation |
|--------------------|-----------------------|
| `@work(exclusive=False)` on async method | `run_worker()` call on sync function |
| `async def run_command(...):` | `def run_command():` (sync) |
| Returns `AsyncIterator` | Uses `asyncio.run()` inside sync function |

**This was the most critical issue** - it made the core functionality (FR-002: execute commands) completely non-functional despite all 47 tasks being marked complete in tasks.md.

---

## Root Cause Summary

### Pattern 1: Documentation-Reality Mismatch

| Document | Issue | Gap |
|----------|-------|-----|
| quickstart.md | #001 | Assumed `python` symlink exists |
| quickstart.md | #003 | Didn't mention PEP 668 or `python3-full` |
| research.md | #008-#010 | No research on theme system |

### Pattern 2: Framework Misunderstanding

| Framework Aspect | Expected | Implemented |
|-----------------|----------|-------------|
| CSS file extension | `.tcss` | `.css` or file path wrong |
| CSS comment syntax | `/* */` | `""" """` (Python) |
| CSS variables | `$text-muted`, `$accent` | `$muted`, `$info` (non-existent) |
| Border syntax | `border: type color;` | `border: type color opacity%;` |
| Theme system | Registration required | Direct assignment attempted |
| Worker pattern | `thread=True` for sync | Called without parameter |

### Pattern 3: Incomplete Implementation

| Task | Status in tasks.md | Actual State |
|------|-------------------|--------------|
| T024: `on_command_selected` handler | ✅ Complete | Empty method |
| T025: `@work` decorated worker | ✅ Complete | Missing `thread=True` |
| T045: Quickstart validation | ✅ Complete | Core feature not working |

---

## Deviation Matrix: Spec Requirements → Issues

| Requirement | Spec Reference | Issue(s) | Deviation |
|-------------|---------------|----------|-----------|
| FR-002: Execute selected command | spec.md:87 | #011 | Empty action method |
| FR-003: Stream output real-time | spec.md:88 | #011 | Worker error prevents execution |
| FR-005: Distinct stdout/stderr | spec.md:90 | #006 | Wrong CSS variables |
| FR-007: Remain responsive | spec.md:92 | #011 | Worker config error |
| SC-001: Execute within 3 seconds | spec.md:118 | #011 | Cannot execute at all |
| Research §1: Textual workers | research.md:21 | #011 | Pattern not followed |
| Research §4: CSS layout | research.md:153 | #005-#007 | Syntax errors |
| T016: CSS layout | tasks.md:48 | #004-#008 | Multiple CSS issues |

---

## Impact Assessment

### Blocking Issues (Prevented Application Launch)

| Issue # | Severity | Resolution Required |
|---------|----------|-------------------|
| #002 | HIGH | Install dependencies |
| #003 | HIGH | Fix venv with python3-full |
| #005 | HIGH | Fix CSS comment syntax |
| #006 | HIGH | Fix variable references |
| #007 | HIGH | Fix border syntax |
| #008-#010 | HIGH | Remove theme setting |
| #011 | CRITICAL | Implement command execution |

### Non-Blocking Issues (Quality/UX)

| Issue # | Severity | Impact |
|---------|----------|-------|
| #001 | MEDIUM | Documentation improvement |
| #008 (CSS quality) | LOW | Code maintainability |

---

## Lessons Learned

### 1. Testing Gap
**Finding**: All 47 tasks were marked complete in [tasks.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/tasks.md), including T045 ("Run quickstart.md validation checklist"), yet the core functionality was broken.

**Lesson**: Task completion checkboxes don't guarantee working code. The validation checklist in quickstart.md (lines 108-118) should have caught Issue #011.

### 2. Research Completeness
**Finding**: [research.md](file:///home/sthe/ops_deck/specs/001-tui-cli-dashboard/research.md) researched 5 topics but missed the theme system entirely.

**Lesson**: Research should cover ALL framework APIs being used, not just the "interesting" ones.

### 3. Textual CSS Is Not Standard CSS
**Finding**: Issues #005, #006, and #007 all stem from treating Textual CSS like standard web CSS.

**Lesson**: Framework-specific variants (TCSS, JSX, etc.) require their own documentation review.

### 4. Environment Assumptions
**Finding**: Issues #001 and #003 assume a standard Python environment that doesn't exist on modern Debian-based systems.

**Lesson**: Quickstart documentation should be tested on fresh systems.

---

## Recommendations

### Immediate Fixes Applied

| Issue | Fix Applied |
|-------|------------|
| #005 | Changed `"""` to `/*` at file start |
| #006 | Replaced `$muted` → `$text-muted`, `$info` → `$accent` |
| #007 | Removed `50%` from border declarations |
| #008-#010 | Removed theme setting, use Textual defaults |
| #011 | Added `thread=True` to `run_worker()` call |

### Documentation Updates Needed

1. **quickstart.md**: Use `python3` instead of `python`
2. **quickstart.md**: Add PEP 668 troubleshooting section
3. **research.md**: Add section on Textual theme system (or note it's not being used)
4. **tasks.md**: Add integration test task before marking T045 complete

### Process Improvements

1. **Run validation checklist ACTUALLY** - Don't just mark checkboxes
2. **Test commands before documenting them** - Especially `python -m src.app`
3. **Research framework APIs completely** - Not just the parts that seem relevant
4. **Use framework-specific linting** - Textual CSS linter if available

---

## Appendix: Issue File Index

| File | Category | Status |
|------|----------|--------|
| 001-python-command-not-found.md | Environment | Resolved |
| 002-missing-textual-module.md | Environment | Resolved |
| 003-externally-managed-environment.md | Environment | Resolved |
| 004-css-file-not-found.md | CSS | Resolved |
| 005-invalid-css-syntax.md | CSS | Resolved |
| 006-css-variable-reference-errors.md | CSS | Resolved |
| 007-invalid-border-syntax.md | CSS | Resolved |
| 007-border-syntax-FINAL-RESOLUTION.md | CSS | Documentation |
| 008-app-css-review-issues.md | CSS Quality | Open |
| 008-invalid-theme-error.md | Theme | Resolved |
| 009-theme-names-attribute-error.md | Theme | Resolved |
| 010-theme-not-registered-fallback-also-fails.md | Theme | Resolved |
| 010-widget-rendering-error.md | Rendering | Related |
| 011-command-execution-not-triggered.md | Execution | Resolved |
| 011-worker-configuration-error.md | Execution | Resolved |
| 011-*.md (7 files) | Execution | Documentation |

---

*Report generated from analysis of `/issues/` and `/specs/001-tui-cli-dashboard/`*
