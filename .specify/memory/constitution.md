<!--
## Sync Impact Report

Version change: N/A → 1.0.0 (Initial ratification)

### Modified Principles
- N/A (Initial version)

### Added Sections
- Core Principles (5 principles)
- Technology Stack
- Quality Gates
- Governance

### Removed Sections
- N/A (Initial version)

### Templates Requiring Updates
- ✅ plan-template.md - Constitution Check section compatible
- ✅ spec-template.md - User scenarios align with UI responsiveness requirements
- ✅ tasks-template.md - Phase structure supports async/TUI development workflow

### Follow-up TODOs
- None
-->

# Ops Deck Constitution

## Core Principles

### I. Separation of Concerns (NON-NEGOTIABLE)

All code MUST adhere to SOLID design principles with clear architectural boundaries:

- **Runner Layer**: Command execution logic MUST be isolated in dedicated service modules; subprocess management handled exclusively via `asyncio.create_subprocess_shell`
- **UI Layer**: Textual widgets and layouts MUST contain no business logic; UI components only handle rendering and user event delegation
- **Configuration Layer**: Command definitions MUST be externalized to YAML/JSON configuration files; no hardcoded commands in source code
- **Data Flow**: Strict unidirectional flow: User Input → Worker → Output Capture → UI Update

**Rationale**: Clear separation enables independent testing, easier maintenance, and prevents coupling between subprocess management and UI rendering.

### II. Non-Blocking Async-First

The application MUST remain responsive at all times:

- All subprocess execution MUST use `asyncio` workers; blocking calls are forbidden in the main event loop
- Output streaming MUST be line-by-line to enable real-time UI updates
- Long-running commands MUST NOT freeze scrolling, clicking, or other UI interactions
- Workers MUST use Textual's worker pattern for background task management

**Rationale**: A frozen UI defeats the purpose of a dashboard controller; users must always be able to cancel, scroll, or switch commands.

### III. Observable Output Streams

All command output MUST be clearly distinguishable and debuggable:

- `stdout` and `stderr` MUST be captured separately and rendered with distinct visual styling (e.g., different colors)
- Non-zero exit codes MUST trigger explicit error indication in the UI
- Output display MUST support both streaming (live) and completed (scrollable history) modes
- All command executions MUST log: command string, start time, exit code, duration

**Rationale**: Operators need to quickly distinguish successful output from errors; mixed streams cause confusion during incident response.

### IV. Configuration-Driven Commands

Command definitions MUST be externalized and user-editable:

- Commands MUST be defined in a structured configuration file (YAML or JSON)
- Each command entry MUST include: `name` (display label), `command` (shell string), `description` (optional help text)
- Configuration MUST be validated at application startup; malformed configs MUST prevent launch with clear error messages
- Adding new commands MUST NOT require code changes

**Rationale**: End users should customize their dashboard without modifying Python source; this enables team-specific deployments.

### V. Simplicity & YAGNI

Start simple, add complexity only when proven necessary:

- Initial implementation MUST cover core features only: Command Palette, Output Window, Non-Blocking Execution
- Abstractions MUST be justified by concrete use cases, not speculative needs
- Dependencies MUST be minimal: Python 3.10+, Textual, asyncio (stdlib)
- Features not in the spec MUST NOT be implemented without explicit approval

**Rationale**: TUI applications grow complex quickly; aggressive scope control prevents feature creep and maintains focus on the core operator experience.

## Technology Stack

The following technology choices are mandated for this project:

| Component | Requirement | Flexibility |
|-----------|-------------|-------------|
| Language | Python 3.10+ | MUST use; type hints encouraged |
| TUI Framework | Textual (by Textualize) | MUST use; no alternatives |
| Async Runtime | asyncio (stdlib) | MUST use for subprocess management |
| Config Format | YAML or JSON | Either acceptable; pick one and be consistent |
| Testing | pytest | Recommended; async tests via pytest-asyncio |

## Quality Gates

All contributions MUST pass these gates before merge:

1. **Lint Gate**: Code MUST pass configured linter (ruff or flake8) with zero errors
2. **Type Gate**: Code SHOULD pass mypy in strict mode (warnings acceptable for initial phases)
3. **Test Gate**: All existing tests MUST pass; new features SHOULD include tests
4. **UI Responsiveness Gate**: Manual verification that UI remains interactive during command execution
5. **Configuration Validation Gate**: Application MUST start successfully with example config

## Governance

This constitution supersedes all other development practices for the Ops Deck project:

- All pull requests MUST be reviewed for constitution compliance
- Violations require documented justification in the PR description
- Amendments to this constitution require:
  1. Written proposal with rationale
  2. Version increment following semantic versioning (MAJOR.MINOR.PATCH)
  3. Update to Last Amended date
- Constitution version follows: MAJOR (principle changes), MINOR (new sections), PATCH (clarifications)

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
