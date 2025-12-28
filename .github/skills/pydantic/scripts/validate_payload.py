"""
validate_payload.py
--------------------

Purpose:
    Validate JSON-like input using a supplied Pydantic model and return
    formatted results or structured errors.

Usage:
    This script is used when the user needs quick validation checks for
    payloads or wants to reproduce a ValidationError.

Notes:
    Replace placeholder sections with full implementations when integrating.
"""

from typing import Any, Type
from pydantic import BaseModel, ValidationError

def validate_data(model: Type[BaseModel], data: Any) -> dict:
    try:
        instance = model.model_validate(data)
        return {"success": True, "data": instance.model_dump()}
    except ValidationError as e:
        return {"success": False, "errors": e.errors()}
