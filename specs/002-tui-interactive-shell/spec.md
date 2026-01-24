# Feature Specification: TUI with Interactive Shell Commands

**Feature Branch**: `002-tui-interactive-shell`  
**Created**: 2026-01-24  
**Status**: Draft  
**Input**: User description: "convert this ops deck into a tui in which you can run interactive commands like vim, nano, etc."

## Overview

Transform the ops deck into a full TUI (Text User Interface) that allows users to run interactive shell commands directly within the TUI environment. This includes support for terminal multiplexing editors (vim, nano), interactive shells (bash, zsh), and other terminal-based tools while maintaining the ops deck's command execution capabilities.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Launch Interactive Editors (Priority: P1)

As an operator, I want to open editors like vim or nano within the TUI to edit configuration files directly, so that I can make quick changes without leaving the interface.

**Why this priority**: This is a core differentiator from the command palette dashboard. Interactive editors are essential tools for ops workflows and represent the primary new capability.

**Independent Test**: Can be fully tested by selecting an editor command from the palette, launching vim/nano, editing a file, and returning to the TUI with changes persisted.

**Acceptance Scenarios**:

1. **Given** the TUI is running and a file exists in the workspace, **When** the user selects "Edit Config (vim)" from the palette, **Then** the editor launches in full-screen mode with the file loaded.
2. **Given** vim is open within the TUI, **When** the user makes changes and exits (`:wq`), **Then** the TUI regains control with the file changes persisted.
3. **Given** nano is launched, **When** the user edits a file and saves (`Ctrl+O`), **Then** the changes are persisted and the editor exits cleanly.

---

### User Story 2 - Execute Interactive Shell Sessions (Priority: P1)

As an operator, I want to drop into a bash or zsh shell to run ad-hoc commands interactively, so that I can handle scenarios beyond predefined commands.

**Why this priority**: Interactive shell access is fundamental for ops work and provides flexibility for debugging, exploration, and custom workflows that may not be in the predefined palette.

**Independent Test**: Can be tested by launching a shell session, running commands like `ls`, `cd`, and pipes, then exiting cleanly back to the TUI.

**Acceptance Scenarios**:

1. **Given** the TUI is active, **When** the user selects "Open Shell" from the menu, **Then** a full interactive bash/zsh shell spawns with the same working context.
2. **Given** a shell session is open, **When** the user types and executes commands with pipes, redirects, or environment variables, **Then** all shell features work normally.
3. **Given** the user exits the shell (via `exit` or `Ctrl+D`), **When** the shell closes, **Then** the TUI regains focus with the correct working directory preserved.

---

### User Story 3 - Run Interactive Tools with Terminal Multiplexing (Priority: P2)

As an operator, I want to use tools like tmux, screen, or interactive debuggers within the TUI, so that I can manage multiple sessions and complex workflows.

**Why this priority**: Advanced users may need tmux/screen sessions and debuggers, which enhance the tool's capability but are not required for basic interactive shell usage.

**Independent Test**: Can be tested by launching tmux within the TUI, creating panes/windows, and managing multiple commands.

**Acceptance Scenarios**:

1. **Given** tmux is installed, **When** the user selects "Open tmux" from the palette, **Then** tmux launches and accepts keyboard input normally.
2. **Given** a tmux session is running within the TUI, **When** the user creates new windows (`Ctrl+B c`), **Then** window management works as expected.
3. **Given** the tmux session is active, **When** the user exits tmux, **Then** the TUI regains control cleanly.

---

### User Story 4 - Maintain Command Palette with Interactive Enhancements (Priority: P2)

As an operator, I want to continue using the existing command palette for predefined commands while also having access to interactive shells, so that I get the best of both structured and ad-hoc workflows.

**Why this priority**: This ensures the new interactive shell feature integrates seamlessly with the existing dashboard without breaking current workflows.

**Independent Test**: Can be tested by executing a predefined command from the palette, then launching an interactive shell, and confirming both work independently.

**Acceptance Scenarios**:

1. **Given** the TUI displays the command palette, **When** the user selects a predefined command, **Then** the command executes as before with output displayed in the output window.
2. **Given** a command has completed, **When** the user selects "Open Shell" while still viewing command output, **Then** the shell launches without losing the previous output history.
3. **Given** the shell session ends, **When** the user returns to the palette, **Then** they can select and run new commands normally.

---

### Edge Cases

- What happens when a user kills a shell with `kill -9` or force-exits without cleanup?
- How does the TUI handle Ctrl+C when multiple processes are running?
- What happens if an interactive editor crashes or becomes unresponsive?
- How are environment variables and working directory state managed across multiple shell sessions?
- What happens when a user tries to run a non-interactive editor (sed, awk) as if it were interactive?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support launching interactive editors (vim, nano, emacs, etc.) as full-screen overlays that capture all keyboard input and terminal output.
- **FR-002**: System MUST support spawning bash/zsh shells with the same environment variables, working directory, and PATH as the parent TUI process.
- **FR-003**: System MUST preserve the terminal state (working directory, environment variables) when returning from an interactive session to the palette.
- **FR-004**: System MUST handle keyboard signals (Ctrl+C, Ctrl+Z, Ctrl+D) correctly and pass them to the running interactive process.
- **FR-005**: System MUST ensure the TUI terminal is restored to a clean state after any interactive session exits or crashes.
- **FR-006**: System MUST support predefined palette commands that launch interactive sessions (e.g., "Edit Config in Vim").
- **FR-007**: System MUST stream stdin/stdout/stderr from interactive sessions live to provide responsive interaction, logging only errors and exceptions to a debug log.
- **FR-008**: System MUST support detecting when an interactive process is ready to accept input before returning control to the user.
- **FR-009**: System MUST restore the TUI interface cleanly if an interactive process leaves the terminal in an unexpected state.

### Key Entities

- **Interactive Session**: Represents a running editor, shell, or other interactive tool with active TTY control.
- **Shell Environment**: Captures working directory, environment variables, and process context to maintain state across sessions.
- **Terminal State**: Includes cursor position, color palette, and terminal mode (raw vs. cooked) for restoration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can launch vim and edit a file, saving changes, and return to the TUI in under 30 seconds (round-trip).
- **SC-002**: Users can spawn an interactive shell and run 10 sequential commands with correct output in under 5 seconds total execution time.
- **SC-003**: The TUI terminal is fully restored (colors, cursor, input mode) to its pre-interactive state 100% of the time.
- **SC-004**: Keyboard signals (Ctrl+C, Ctrl+D) work correctly in 95% of interactive sessions without crashes or hung processes.
- **SC-005**: Users can return from an interactive editor with working directory and environment variables unchanged from before the session.

## Assumptions

- The TUI is built with a terminal library that supports raw mode and signal handling (e.g., Python's curses or similar).
- Operators have bash/zsh and common editors (vim, nano) installed in their environment.
- The ops deck runs on Unix-like systems (Linux, macOS) where TTY control is supported.
- Interactive sessions inherit the parent TUI's terminal size (rows/cols) and handle resize events appropriately.
- Users understand basic shell navigation and editor controls (no custom keybinding support beyond system defaults initially).

## Constraints & Open Questions

- **Terminal Support**: Only Unix-like systems with TTY support are in scope; Windows support is out of scope initially.
- **Nested TUIs**: Running another ops deck TUI instance within an interactive session is not supported; the system will block nested TUI launches to prevent confusion and resource exhaustion.
- **Session Logging**: Interactive session input/output is not logged by default. Users can enable logging on a per-session basis when creating an interactive session. All enabled logs are written to a configurable log directory.

## Glossary

- **TUI**: Text User Interface—a graphical interface rendered in the terminal using characters.
- **TTY**: Terminal device that manages keyboard input and screen output.
- **Raw Mode**: Terminal mode where each keystroke is sent directly to the application (vs. line-buffered mode).
- **Palette**: The menu of predefined commands available in the command palette.
