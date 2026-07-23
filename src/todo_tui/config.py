"""Configuration management for the TODO TUI app."""

import json
from pathlib import Path
from typing import Any


class KeyBindingConfig:
    """Manage customizable key bindings."""
    
    DEFAULT_BINDINGS = {
        "quit": "q",
        "toggle_todo": "space",
        "delete_todo": "d",
        "postpone_todo": "p",
        "show_shortcuts": "?",
        "export_cheatsheet": "ctrl+h",
        "customize_keys": "ctrl+k",
        "show_tutorial": "ctrl+t",
    }
    
    def __init__(self, config_path: Path | None = None):
        """Initialize the key binding configuration.
        
        Args:
            config_path: Path to the configuration file. Defaults to ~/.todo-tui-keybindings.json
        """
        if config_path is None:
            config_path = Path.home() / ".todo-tui-keybindings.json"
        self.config_path = config_path
        self.bindings = self._load_bindings()
    
    def _load_bindings(self) -> dict[str, str]:
        """Load key bindings from file or return defaults.
        
        Returns:
            Dictionary mapping action names to key bindings
        """
        if not self.config_path.exists():
            return self.DEFAULT_BINDINGS.copy()
        
        try:
            with open(self.config_path, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults to handle new actions
                bindings = self.DEFAULT_BINDINGS.copy()
                bindings.update(loaded)
                return bindings
        except (json.JSONDecodeError, IOError):
            return self.DEFAULT_BINDINGS.copy()
    
    def save_bindings(self) -> None:
        """Save current key bindings to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.bindings, f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save key bindings: {e}")
    
    def get_binding(self, action: str) -> str:
        """Get the key binding for an action.
        
        Args:
            action: The action name
            
        Returns:
            The key binding string
        """
        return self.bindings.get(action, self.DEFAULT_BINDINGS.get(action, ""))
    
    def set_binding(self, action: str, key: str) -> None:
        """Set a key binding for an action.
        
        Args:
            action: The action name
            key: The key binding string
        """
        if action in self.DEFAULT_BINDINGS:
            self.bindings[action] = key
    
    def reset_to_defaults(self) -> None:
        """Reset all bindings to defaults."""
        self.bindings = self.DEFAULT_BINDINGS.copy()
    
    def get_all_bindings(self) -> dict[str, str]:
        """Get all current bindings.
        
        Returns:
            Dictionary of all action-to-key mappings
        """
        return self.bindings.copy()


class AppConfig:
    """Manage application configuration."""
    
    def __init__(self, config_path: Path | None = None):
        """Initialize the app configuration.
        
        Args:
            config_path: Path to the configuration file. Defaults to ~/.todo-tui-config.json
        """
        if config_path is None:
            config_path = Path.home() / ".todo-tui-config.json"
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict[str, Any]:
        """Load configuration from file or return defaults.
        
        Returns:
            Configuration dictionary
        """
        defaults = {
            "first_run": True,
            "tutorial_completed": False,
        }
        
        if not self.config_path.exists():
            return defaults
        
        try:
            with open(self.config_path, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults
                config = defaults.copy()
                config.update(loaded)
                return config
        except (json.JSONDecodeError, IOError):
            return defaults
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
    
    def is_first_run(self) -> bool:
        """Check if this is the first time the app is being run.
        
        Returns:
            True if first run, False otherwise
        """
        return self.config.get("first_run", True)
    
    def mark_tutorial_completed(self) -> None:
        """Mark the tutorial as completed."""
        self.config["first_run"] = False
        self.config["tutorial_completed"] = True
        self.save_config()
