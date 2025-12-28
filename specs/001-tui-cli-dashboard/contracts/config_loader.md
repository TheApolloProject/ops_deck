# Contract: ConfigLoader

**Layer**: Configuration  
**Location**: `src/services/config_loader.py`

## Interface

```python
from pathlib import Path
from src.models.command import Command, AppConfig

class ConfigLoader:
    """Load and validate application configuration from YAML files."""
    
    def load(self, path: Path) -> AppConfig:
        """
        Load configuration from a YAML file.
        
        Args:
            path: Path to the YAML configuration file
            
        Returns:
            Validated AppConfig with list of commands
            
        Raises:
            FileNotFoundError: If config file does not exist
            ConfigValidationError: If config format is invalid
        """
        ...
    
    def load_default(self) -> AppConfig:
        """
        Load configuration from default locations.
        
        Search order:
        1. ./commands.yaml (current directory)
        2. ~/.opsdeck/commands.yaml (user home)
        
        Returns:
            Validated AppConfig from first found location
            
        Raises:
            ConfigNotFoundError: If no config file found in any location
            ConfigValidationError: If found config is invalid
        """
        ...
```

## Exceptions

```python
class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass

class ConfigNotFoundError(ConfigError):
    """No configuration file found in any search location."""
    searched_paths: list[Path]

class ConfigValidationError(ConfigError):
    """Configuration file has invalid format or content."""
    message: str
    line: int | None  # Line number if available
    field: str | None  # Field name if applicable
```

## Behavior Contracts

| Scenario | Expected Behavior |
|----------|-------------------|
| Valid YAML with all required fields | Returns AppConfig |
| Missing `commands` key | Raises ConfigValidationError |
| Empty commands list | Raises ConfigValidationError |
| Command missing `name` | Raises ConfigValidationError with field="name" |
| Command missing `command` | Raises ConfigValidationError with field="command" |
| YAML syntax error | Raises ConfigValidationError with line number |
| File not found | Raises FileNotFoundError or ConfigNotFoundError |
| Non-readable file | Raises PermissionError |

## Usage Example

```python
loader = ConfigLoader()
try:
    config = loader.load_default()
    print(f"Loaded {len(config.commands)} commands")
except ConfigNotFoundError as e:
    print(f"No config found. Searched: {e.searched_paths}")
    sys.exit(1)
except ConfigValidationError as e:
    print(f"Invalid config: {e.message}")
    sys.exit(1)
```
