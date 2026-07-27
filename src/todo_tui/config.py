"""Configuration management for the TODO TUI app."""

import json
from pathlib import Path
from typing import Dict, Optional


DEFAULT_BINDINGS = {
    "quit": "q",
    "toggle": "space",
    "delete": "d",
    "postpone": "p",
    "help": "question_mark",
    "customize": "c",
    "export_shortcuts": "ctrl+e",
    "tutorial": "ctrl+t",
}


class Config:
    """Manages application configuration including key bindings.
    
    Attributes:
        config_path: Path to the configuration file
        bindings: Dictionary mapping action names to key strings
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the configuration manager.
        
        Args:
            config_path: Custom path for config file. Defaults to ~/.todo-tui-config.json
        """
        if config_path is None:
            config_path = Path.home() / ".todo-tui-config.json"
        self.config_path = config_path
        self.bindings = DEFAULT_BINDINGS.copy()
        self.tutorial_shown = False
        self._load()
    
    def _load(self) -> None:
        """Load configuration from disk."""
        if self.config_path.exists():
            try:
                data = json.loads(self.config_path.read_text())
                self.bindings.update(data.get("bindings", {}))
                self.tutorial_shown = data.get("tutorial_shown", False)
            except (json.JSONDecodeError, KeyError):
                # If config is corrupted, use defaults
                pass
    
    def save(self) -> None:
        """Save configuration to disk."""
        data = {
            "bindings": self.bindings,
            "tutorial_shown": self.tutorial_shown,
        }
        self.config_path.write_text(json.dumps(data, indent=2))
    
    def get_binding(self, action: str) -> str:
        """Get the key binding for an action.
        
        Args:
            action: The action name
            
        Returns:
            The key string bound to the action
        """
        return self.bindings.get(action, DEFAULT_BINDINGS.get(action, ""))
    
    def set_binding(self, action: str, key: str) -> None:
        """Set a key binding for an action.
        
        Args:
            action: The action name
            key: The key string to bind
        """
        self.bindings[action] = key
    
    def save_bindings(self) -> None:
        """Save only the bindings to disk."""
        self.save()
    
    def reset_bindings(self) -> None:
        """Reset all key bindings to defaults."""
        self.bindings = DEFAULT_BINDINGS.copy()
        self.save()
    
    def mark_tutorial_shown(self) -> None:
        """Mark the tutorial as having been shown."""
        self.tutorial_shown = True
        self.save()
