"""
tool_examples.py

Collection of reusable example tools for LangChain agents.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

from langchain.tools import tool


@tool
def sqrt(value: float) -> float:
    """Return the square root of a non-negative float."""
    if value < 0:
        raise ValueError("sqrt requires a non-negative value.")
    return math.sqrt(value)


@tool
def current_utc_time(_: str = "") -> str:
    """
    Return the current UTC time in ISO 8601 format.

    Input is ignored but kept for compatibility with tool-calling models.
    """
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TodoItem:
    title: str
    done: bool = False


TODO_LIST: List[TodoItem] = []


@tool
def add_todo(title: str) -> str:
    """Add a todo item with a given title, and return a JSON summary of the list."""
    item = TodoItem(title=title)
    TODO_LIST.append(item)
    return json.dumps([todo.__dict__ for todo in TODO_LIST])


@tool
def list_todos(_: str = "") -> str:
    """Return the current todo list as JSON."""
    return json.dumps([todo.__dict__ for todo in TODO_LIST])
