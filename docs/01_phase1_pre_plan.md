# Phase 1 Pre-Implementation Plan: Setup

**Date**: 2025-12-28  
**Phase**: 1 of 7  
**Duration**: ~30 minutes  
**Priority**: CRITICAL (blocks all other phases)

## Objectives

Setup the complete project directory structure, dependencies, and development tools required for phases 2-7.

## Tasks

| ID | Task | Parallel | Est. Time |
|----|----|----------|-----------|
| T001 | Create project directory structure | No | 5 min |
| T002 | Create pyproject.toml with dependencies | No | 5 min |
| T003 | Create src/__init__.py | Yes | 2 min |
| T004 | Create tests/__init__.py and conftest.py | Yes | 3 min |
| T005 | Configure ruff.toml | Yes | 3 min |
| T006 | Create example commands.yaml | No | 5 min |

## Directory Structure to Create

```
src/
├── __init__.py
├── models/
│   └── __init__.py
├── services/
│   └── __init__.py
├── widgets/
│   └── __init__.py
└── styles/
    └── __init__.py

tests/
├── __init__.py
├── unit/
└── integration/
```

## Dependencies to Install

- **textual**: TUI framework
- **pyyaml**: YAML configuration parsing
- **pydantic**: Data validation
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **ruff**: Code linting/formatting
- **mypy**: Type checking

## Key Files to Create

1. **pyproject.toml**: Package metadata and dependencies
2. **ruff.toml**: Linter configuration
3. **commands.yaml**: Example configuration with sample commands
4. **tests/conftest.py**: Shared test fixtures and configuration

## Success Criteria

- [ ] All directories created per plan.md structure
- [ ] `pip install -e .` succeeds without errors
- [ ] `ruff check src/` runs without errors
- [ ] `python -m pytest --collect-only` discovers test directories
- [ ] `commands.yaml` loads and displays 5+ example commands

## Dependencies

None - Phase 1 is standalone and has no predecessors.

## Next Phase

Phase 2 (Foundational) depends on Phase 1 completion. All foundation models and services require the project structure and dependencies.
