"""Configuration management for the TODO TUI app."""

import json
from pathlib import Path
from typing import Optional, Dict


class Config:
    """Manages application configuration and custom key bindings.
    
    Attributes:
        config_path: Path to the JSON configuration file
        keybindings: Dictionary mapping actions to key combinations
        tutorial_completed: Whether the user has completed the tutorial
    """
    
    DEFAULT_KEYBINDINGS = {
        "quit": "q",
        "toggle": "space",
        "delete": "d",
        "postpone": "p",
        "help": "question_mark",
        "export": "e",
        "import": "i",
        "tutorial": "t",
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the configuration manager.
        
        Args:
            config_path: Custom path for config file. Defaults to ~/.todo-tui-config.json
        """
        if config_path is None:
            config_path = Path.home() / ".todo-tui-config.json"
        self.config_path = config_path
        self.keybindings: Dict[str, str] = {}
        self.tutorial_completed: bool = False
        self._load()
    
    def _load(self) -> None:
        """Load configuration from file."""
        if not self.config_path.exists():
            self._create_default()
            return
        
        try:
            data = json.loads(self.config_path.read_text())
            self.keybindings = data.get("keybindings", self.DEFAULT_KEYBINDINGS.copy())
            self.tutorial_completed = data.get("tutorial_completed", False)
        except (json.JSONDecodeError, KeyError):
            self._create_default()
    
    def _create_default(self) -> None:
        """Create default configuration."""
        self.keybindings = self.DEFAULT_KEYBINDINGS.copy()
        self.tutorial_completed = False
        self._save()
    
    def _save(self) -> None:
        """Save configuration to file."""
        data = {
            "keybindings": self.keybindings,
            "tutorial_completed": self.tutorial_completed,
        }
        self.config_path.write_text(json.dumps(data, indent=2))
    
    def get_key(self, action: str) -> str:
        """Get the key binding for an action.
        
        Args:
            action: The action name
            
        Returns:
            The key combination assigned to the action
        """
        return self.keybindings.get(action, self.DEFAULT_KEYBINDINGS.get(action, ""))
    
    def set_key(self, action: str, key: str) -> None:
        """Set a custom key binding for an action.
        
        Args:
            action: The action name
            key: The key combination to bind
        """
        self.keybindings[action] = key
        self._save()
    
    def reset_keybindings(self) -> None:
        """Reset all keybindings to defaults."""
        self.keybindings = self.DEFAULT_KEYBINDINGS.copy()
        self._save()
    
    def mark_tutorial_completed(self) -> None:
        """Mark the tutorial as completed."""
        self.tutorial_completed = True
        self._save()
    
    def reset_tutorial(self) -> None:
        """Reset tutorial status (for testing or re-running)."""
        self.tutorial_completed = False
        self._save()
