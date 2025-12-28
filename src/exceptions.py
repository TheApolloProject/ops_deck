"""Custom exceptions for Ops Deck."""


class OpsError(Exception):
    """Base exception for all Ops Deck errors."""


class ConfigError(OpsError):
    """Raised when configuration is invalid or cannot be loaded."""


class ExecutionError(OpsError):
    """Raised when command execution fails."""


class TimeoutError(OpsError):
    """Raised when command execution times out."""


class ValidationError(OpsError):
    """Raised when data validation fails."""


class NotFoundError(OpsError):
    """Raised when a resource is not found."""
