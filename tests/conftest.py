"""Shared test fixtures and configuration."""

import pytest


@pytest.fixture
def sample_command():
    """Fixture providing a sample command for testing."""
    return {
        "name": "Test Command",
        "command": "echo 'test'",
        "description": "A test command"
    }


@pytest.fixture
def valid_config():
    """Fixture providing a valid configuration structure."""
    return {
        "commands": [
            {
                "name": "Check Disk Space",
                "command": "df -h",
                "description": "Display disk usage"
            },
            {
                "name": "Git Status",
                "command": "git status",
                "description": "Show working tree status"
            }
        ]
    }
