# Quickstart: TUI CLI Dashboard

**Feature**: 001-tui-cli-dashboard  
**Date**: 2025-12-28  
**Purpose**: Get the application running for development and testing

## Prerequisites

- Python 3.10 or higher
- pip or uv package manager

## Setup

### 1. Create Virtual Environment

```bash
cd /home/sthe/ops_deck
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install textual pyyaml pydantic
```

Or with development dependencies:

```bash
pip install textual pyyaml pydantic pytest pytest-asyncio ruff mypy
```

### 3. Create Configuration File

Create `commands.yaml` in the project root:

```yaml
commands:
  - name: "Check Disk Space"
    command: "df -h"
    description: "Display disk usage in human-readable format"
  
  - name: "Git Status"
    command: "git status"
    description: "Show working tree status"
  
  - name: "List Files"
    command: "ls -la"
    description: "List all files in current directory"
  
  - name: "System Info"
    command: "uname -a"
    description: "Display system information"
  
  - name: "Network Test"
    command: "ping -c 3 localhost"
    description: "Test network with 3 pings to localhost"
```

### 4. Run the Application

```bash
python -m src.app
```

Or create an entry point:

```bash
# After implementing src/app.py with App class
textual run src.app:OpsDeckApp
```

## Development Commands

### Run Tests

```bash
pytest tests/ -v
```

### Run Tests with Async Support

```bash
pytest tests/ -v --asyncio-mode=auto
```

### Lint Code

```bash
ruff check src/ tests/
```

### Type Check

```bash
mypy src/ --strict
```

### Run Textual Console (Debug Mode)

```bash
textual console
# In another terminal:
textual run src.app:OpsDeckApp --dev
```

## Validation Checklist

After implementation, verify these work:

- [ ] `python -m src.app` launches without errors
- [ ] Command palette displays all commands from config
- [ ] Selecting a command shows output in real-time
- [ ] stderr appears in different color than stdout
- [ ] UI remains scrollable during long commands
- [ ] Invalid config file produces clear error message
- [ ] Exit code indicator shows success (0) vs failure (non-zero)

## Project Structure Reference

```
ops_deck/
├── src/
│   ├── __init__.py
│   ├── app.py                 # Main Textual App
│   ├── models/
│   │   ├── __init__.py
│   │   ├── command.py         # Command, AppConfig
│   │   └── execution.py       # Execution, OutputLine
│   ├── services/
│   │   ├── __init__.py
│   │   ├── config_loader.py   # ConfigLoader
│   │   └── runner.py          # CommandRunner
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── command_palette.py # Sidebar widget
│   │   └── output_view.py     # Output display widget
│   └── styles/
│       └── app.tcss           # Textual CSS
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── commands.yaml              # User configuration
├── pyproject.toml
└── specs/                     # Feature specifications
```

## Troubleshooting

### "No module named 'src'"

Ensure you're running from the project root and the virtual environment is activated.

### "Config file not found"

Create `commands.yaml` in the current directory or `~/.opsdeck/commands.yaml`.

### "Textual not rendering correctly"

Ensure your terminal supports 256 colors. Try: `export TERM=xterm-256color`

### UI appears frozen

This indicates a blocking call in the main loop. Check that all subprocess execution uses `asyncio` and Textual workers.
