# Internal Contracts: TUI CLI Dashboard

**Feature**: 001-tui-cli-dashboard  
**Date**: 2025-12-28  
**Purpose**: Define interfaces between architectural layers (Runner, UI, Config)

This is a TUI application without external APIs. Contracts define internal service interfaces to enforce Constitution Principle I (Separation of Concerns).

## Contract Index

| Contract | Layer | Purpose |
|----------|-------|---------|
| [ConfigLoader](config_loader.md) | Configuration | Load and validate YAML config |
| [CommandRunner](command_runner.md) | Runner | Execute commands and stream output |
| [Messages](messages.md) | Communication | Textual messages between components |
