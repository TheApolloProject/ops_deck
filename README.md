# Ops Deck - CLI Command Dashboard TUI

A modern terminal user interface (TUI) dashboard for managing and executing CLI commands with real-time output streaming.

## Overview

**Ops Deck** is a Python-based TUI application built with [Textual](https://textual.textualize.io/) that enables DevOps engineers to:

- ✅ Execute CLI commands from a curated list
- ✅ View real-time command output (stdout/stderr)
- ✅ Manage command configuration via YAML
- ✅ Track execution status and timing
- ✅ Handle timeouts and errors gracefully
- ⏳ Implement responsive multi-execution UI (Phase 5)
- ⏳ Load dynamic configurations (Phase 6)

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip or poetry

### Installation

```bash
# Clone repository
cd /home/sthe/ops_deck

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Ops Deck (loads commands from commands.yaml in current directory)
ops-deck

# Or run directly with Python
python3 -m src.app
```

**Keyboard Controls:**
- **Q**: Quit the application
- **Up/Down**: Navigate command list
- **Enter**: Execute selected command
- **Mouse**: Click commands and scroll output

**Navigation Tips:**
- When an error screen is shown, press Q to exit
- When viewing output, use scroll-lock to prevent auto-scroll
- Command descriptions appear in the left panel

## Project Structure

```
ops_deck/
├── src/                          # Source code
│   ├── models/                   # Pydantic data models
│   │   ├── command.py           # Command configuration
│   │   ├── execution.py         # Execution tracking
│   │   ├── output.py            # Output line model
│   │   ├── config.py            # App configuration
│   │   └── __init__.py
│   ├── services/                # Business logic
│   │   ├── command_runner.py    # Async command execution
│   │   ├── config.py            # Configuration loading
│   │   └── __init__.py
│   ├── widgets/                 # Textual UI components
│   │   ├── app.py              # Main application
│   │   ├── command_list.py     # Command selection widget
│   │   ├── output_pane.py      # Output display widget
│   │   └── __init__.py
│   ├── styles/                  # Textual CSS
│   │   └── app.css             # Application styling
│   ├── exceptions.py            # Custom exception classes
│   ├── messages.py              # Textual message definitions
│   └── __init__.py
├── tests/                        # Test suite
│   ├── unit/                    # Unit tests
│   │   └── test_command_runner.py
│   ├── integration/             # Integration tests
│   │   └── test_app.py
│   ├── conftest.py              # Shared pytest fixtures
│   └── __init__.py
├── docs/                         # Phase documentation
├── commands.yaml                 # Example command configuration
├── pyproject.toml               # Python package metadata
├── ruff.toml                    # Linter configuration
└── README.md
```

## Architecture

### Core Components

#### Data Models (Pydantic)
- **Command**: CLI command configuration with timeout, environment variables
- **Execution**: Single command execution run with status tracking
- **OutputLine**: Output stream line with timestamp and stream type (stdout/stderr)
- **AppConfig**: Global application settings (theme, refresh rate, logging)

#### Services
- **ConfigLoader**: Load and validate YAML configuration files
- **AsyncCommandRunner**: Execute commands asynchronously with output streaming

#### Textual Widgets
- **OpsApp**: Main application container with key bindings
- **CommandListPanel**: Navigate and select commands
- **OutputPane**: Display real-time command output

#### Message System
- **CommandOutput**: Streaming output lines
- **StatusUpdate**: Execution status changes
- **ExecutionComplete**: Finished execution notification
- **CommandStarted**: Execution initiation
- **ExecutionError**: Execution failures

## Features

### Phase 1: Setup ✅ COMPLETE
- [x] Project structure initialization
- [x] Dependency management (pyproject.toml)
- [x] Virtual environment setup
- [x] Linting configuration (ruff)
- [x] Testing framework setup (pytest)

### Phase 2: Foundational ✅ COMPLETE
- [x] Pydantic data models
- [x] Exception hierarchy
- [x] Configuration service
- [x] Textual message system
- [x] Base CSS layout

### Phase 3: User Story 1 MVP ✅ COMPLETE
- [x] Async command execution
- [x] Real-time output streaming
- [x] Command selection widget
- [x] Output display widget
- [x] Main application widget
- [x] Unit tests (6/6 passing)
- [x] Integration tests (8/8 passing)

### Phase 4: User Story 2 Error Handling ✅ COMPLETE
- [x] Error message display
- [x] Status bar implementation
- [x] Exit code handling
- [x] Execution metadata display
- [x] Error recovery UI

### Phase 5: User Story 3 Responsiveness ✅ COMPLETE
- [x] Responsive grid layout
- [x] Concurrent command execution
- [x] Execution tracking with running indicators
- [x] Auto-scroll with scroll-lock detection
- [x] Command execution headers with timestamps

### Phase 6: User Story 4 Configuration ✅ COMPLETE
- [x] Dynamic configuration loading
- [x] Enhanced error messages with field context
- [x] Startup error screen
- [x] Configuration documentation

### Phase 7: Polish ⏳ PENDING
- [ ] Complete type checking (mypy)
- [ ] Comprehensive logging
- [ ] Full documentation
- [ ] Performance optimization
- [ ] End-to-end tests

## Development

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest -v

# Run specific test file
pytest tests/unit/test_command_runner.py -v

# Run with coverage
pytest --cov=src tests/

# Run with asyncio debugging
pytest -v -s
```

### Code Quality

```bash
# Activate virtual environment
source .venv/bin/activate

# Lint code
ruff check src/

# Auto-fix linting issues
ruff check src/ --fix

# Type checking
mypy src/
```

### Configuration

Edit `commands.yaml` to add your custom commands:

```yaml
commands:
  - name: "list_files"
    command: "ls -la /tmp"
    description: "List files in /tmp"
    tags: ["filesystem"]
    timeout: 10
    env: {}

  - name: "check_disk"
    command: "df -h"
    description: "Check disk usage"
    tags: ["system"]
    timeout: 5

app:
  theme: "dark"
  refresh_rate: 1.0
  log_level: "INFO"
  command_timeout: 300
  max_output_lines: 10000
  auto_scroll: true
```

### Configuration Format

#### Commands Section

The `commands` section is a list of CLI command configurations. Each command has the following fields:

**Required Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier for the command (used internally) |
| `command` | string | The shell command to execute (bash compatible) |
| `description` | string | Human-readable description shown in the UI |

**Optional Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `tags` | list[string] | `[]` | Category tags for organizing commands |
| `timeout` | integer | app-level timeout | Execution timeout in seconds (0 = no timeout) |
| `env` | object | `{}` | Environment variables as key-value pairs |

**Example Command Definition:**

```yaml
commands:
  - name: "deploy_prod"
    command: "bash scripts/deploy.sh --env=production"
    description: "Deploy to production environment"
    tags: ["deployment", "production"]
    timeout: 600  # 10 minutes
    env:
      DEPLOY_ENV: "production"
      DEBUG: "false"
```

**Field Validation Rules:**

- `name`: Must be non-empty, max 100 characters
- `command`: Must be non-empty, max 1000 characters
- `description`: Must be non-empty, max 500 characters
- `timeout`: Must be non-negative integer (0 = unlimited)
- `tags`: List of strings, each max 50 characters
- `env`: Object with string keys and string values

#### App Configuration Section

The `app` section configures global application settings:

**Optional Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `theme` | string | `"dark"` | Textual theme name (dark, light, nord, etc.) |
| `refresh_rate` | float | `1.0` | UI refresh rate in Hz (updates per second) |
| `log_level` | string | `"INFO"` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `command_timeout` | integer | `300` | Default timeout for all commands in seconds |
| `max_output_lines` | integer | `10000` | Maximum output lines to keep in memory |
| `auto_scroll` | boolean | `true` | Auto-scroll output to latest line |

**Example App Configuration:**

```yaml
app:
  theme: "nord"
  refresh_rate: 2.0  # Update UI twice per second
  log_level: "DEBUG"
  command_timeout: 600  # 10 minute default
  max_output_lines: 50000
  auto_scroll: false  # Disable auto-scroll
```

### Configuration Loading and Error Handling

#### Valid Configuration

When the application starts, it loads `commands.yaml` from the current directory. If the file is valid, the app displays your commands in the command palette.

#### Configuration Errors

If the configuration is invalid, the app shows an error screen with:
- **Error Title**: The type of error (Configuration Error, YAML Parse Error, etc.)
- **Error Message**: Details about what went wrong
- **Field Context**: For validation errors, which field caused the problem
- **Suggestions**: Hints for optional fields in commands and app config

**Press Q to exit** the error screen.

#### Common Configuration Issues

**Missing commands.yaml:**
```
Configuration File Not Found
Could not find commands.yaml
Create a commands.yaml file in the current directory.
```

**Invalid YAML syntax:**
```
YAML Parse Error at line 5: Unexpected character ':'
Check your commands.yaml file for syntax errors.
```

**Missing required field:**
```
Configuration Error: Command 1 missing required field 'name'
Optional fields: tags, timeout, env
```

**Invalid field type:**
```
Configuration Error: timeout must be integer, got string
Check your commands.yaml file for type errors.
```

**Invalid timeout value:**
```
Configuration Error: timeout must be >= 0, got -10
Check your commands.yaml file for values.
```

#### Validation Rules Applied

1. **YAML Syntax**: Must be valid YAML format
2. **Command Structure**: Each command must have required fields
3. **Field Types**: Fields must match expected types
4. **Field Ranges**: Numeric fields must be within valid ranges
5. **Field Lengths**: Strings must not exceed maximum length
6. **Special Characters**: Command strings may contain shell metacharacters

### Complete Configuration Example

```yaml
# Ops Deck Configuration

# List of available commands
commands:
  # System monitoring commands
  - name: "system_stats"
    command: "uname -a && uptime && free -h"
    description: "Display system information and uptime"
    tags: ["system", "monitoring"]
    timeout: 5

  - name: "process_list"
    command: "ps aux | head -20"
    description: "List top 20 running processes"
    tags: ["system", "monitoring"]
    timeout: 10

  # Git operations
  - name: "git_status"
    command: "git status"
    description: "Show git repository status"
    tags: ["git"]
    timeout: 10

  - name: "git_log"
    command: "git log --oneline -10"
    description: "Show last 10 commits"
    tags: ["git"]
    timeout: 10

  # Deployment commands
  - name: "deploy_staging"
    command: "bash scripts/deploy.sh staging"
    description: "Deploy to staging environment"
    tags: ["deployment"]
    timeout: 300
    env:
      ENV: "staging"
      DEBUG: "false"

  - name: "deploy_prod"
    command: "bash scripts/deploy.sh production"
    description: "Deploy to production environment"
    tags: ["deployment"]
    timeout: 600
    env:
      ENV: "production"
      DEBUG: "false"

  # Database commands
  - name: "db_backup"
    command: "mysqldump -u root mydb > backup.sql"
    description: "Backup database to file"
    tags: ["database", "backup"]
    timeout: 900

  - name: "db_restore"
    command: "mysql -u root mydb < backup.sql"
    description: "Restore database from backup"
    tags: ["database", "backup"]
    timeout: 900

# Global application configuration
app:
  # UI Theme
  theme: "dark"

  # Refresh rate in Hz (updates per second)
  refresh_rate: 2.0

  # Logging level
  log_level: "INFO"

  # Default timeout for all commands (seconds)
  # Command-level timeout overrides this value
  command_timeout: 300

  # Maximum output lines to keep in memory
  # Older lines are discarded when exceeded
  max_output_lines: 10000

  # Auto-scroll output to latest line when new output appears
  auto_scroll: true
```

### Troubleshooting Configuration

**Q: My commands don't appear in the app**
- A: Check that your `commands.yaml` file is in the current directory where you run `ops-deck`
- A: Verify YAML syntax is valid (use a YAML validator)
- A: Check that each command has required fields (name, command, description)

**Q: I get a "Configuration Error" on startup**
- A: Check error screen for specific field and error type
- A: Verify field types match expected types (string, integer, list, object)
- A: Ensure required fields are present in each command

**Q: Commands timeout unexpectedly**
- A: Increase the `timeout` value for individual commands
- A: Or increase the global `command_timeout` in the app config
- A: Use `timeout: 0` to disable timeout for a specific command

**Q: Output is cut off**
- A: Increase `max_output_lines` in app config
- A: Default is 10,000 lines; set higher for verbose commands
- A: Press Q and check error messages if app crashes with large output



## Dependencies

### Core
- **textual** - Modern TUI framework
- **pydantic** - Data validation and settings management
- **pyyaml** - YAML configuration parsing

### Development
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **ruff** - Fast Python linter
- **mypy** - Static type checker

## Documentation

See the [docs/](docs/) directory for detailed phase implementation reports:

- [Phase 1: Setup](docs/01_phase1_pre_plan.md)
- [Phase 2: Foundational](docs/03_phase2_pre_plan.md)
- [Phase 3: User Story 1 MVP](docs/05_phase3_pre_plan.md)
- [Progress Summary](docs/PROGRESS.md)

## Testing

### Test Structure

```
tests/
├── unit/                          # Unit tests (services, models)
├── integration/                   # Integration tests (widgets, workflows)
└── conftest.py                   # Shared fixtures
```

### Current Test Coverage

- **Unit Tests**: 6 passing
  - CommandRunner execution
  - Output streaming
  - Timeout handling
  - Error detection

- **Integration Tests**: 8 passing
  - Configuration loading
  - Widget initialization
  - Widget navigation
  - Message passing

## Performance

- Async command execution prevents UI blocking
- Streaming output callbacks for real-time display
- Configurable output line buffering (default 10,000 lines)
- Efficient CSS-based layout system

## Known Limitations

- CSS layout defined but not yet integrated into running app (Phase 6)
- Message handlers not yet connected to widgets (Phase 4)
- Single command execution at a time (Phase 5)
- No persistent command history (Phase 6)
- No command editing/creation UI (Future)

## Troubleshooting

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Linting Errors
```bash
# Auto-fix most issues
ruff check src/ --fix

# Check remaining issues
ruff check src/
```

### Test Failures
```bash
# Run with verbose output
pytest -vv --tb=long

# Run specific test
pytest tests/unit/test_command_runner.py::test_simple_echo_command -v
```

## Contributing

1. Follow PEP 604 type hint style (Python 3.10+)
2. Ensure ruff linting passes
3. Add tests for new features
4. Update phase documentation
5. Maintain 100% test pass rate

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check [Phase Documentation](docs/PROGRESS.md)
2. Review test cases for usage examples
3. Check docstrings in source code

---

**Last Updated**: 2025-12-28  
**Status**: In Active Development (Phases 1-6 Complete, Phase 7 Pending)  
**Target Completion**: Phase 7 - Polish  
**Test Status**: 14/14 tests passing ✅  
**Linting Status**: 0 errors with ruff ✅
