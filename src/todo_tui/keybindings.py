"""Customizable key bindings management."""

import json
from pathlib import Path
from typing import Dict, Optional


class KeyBindingsManager:
    """Manages customizable key bindings for the application.
    
    Attributes:
        bindings_path: Path to the JSON file where key bindings are stored
        bindings: Dictionary mapping action names to key strings
    """
    
    # Default key bindings
    DEFAULT_BINDINGS = {
        "quit": "q",
        "help": "question_mark",
        "toggle": "space",
        "delete": "d",
        "postpone": "p",
        "focus_next": "tab",
        "focus_previous": "shift+tab",
    }
    
    def __init__(self, bindings_path: Optional[Path] = None):
        """Initialize the key bindings manager.
        
        Args:
            bindings_path: Custom path for bindings file. Defaults to ~/.todo-tui-keybindings.json
        """
        if bindings_path is None:
            bindings_path = Path.home() / ".todo-tui-keybindings.json"
        self.bindings_path = bindings_path
        self.bindings = self._load_bindings()
    
    def _load_bindings(self) -> Dict[str, str]:
        """Load key bindings from file or return defaults.
        
        Returns:
            Dictionary mapping action names to key strings
        """
        if not self.bindings_path.exists():
            return self.DEFAULT_BINDINGS.copy()
        
        try:
            data = json.loads(self.bindings_path.read_text())
            # Merge with defaults to ensure all actions have bindings
            bindings = self.DEFAULT_BINDINGS.copy()
            bindings.update(data)
            return bindings
        except (json.JSONDecodeError, Exception):
            # If file is corrupted, return defaults
            return self.DEFAULT_BINDINGS.copy()
    
    def save_bindings(self) -> None:
        """Save current key bindings to file."""
        try:
            self.bindings_path.write_text(json.dumps(self.bindings, indent=2))
        except Exception as e:
            raise ValueError(f"Failed to save key bindings: {e}")
    
    def set_binding(self, action: str, key: str) -> None:
        """Set a key binding for an action.
        
        Args:
            action: The action name (e.g., "quit", "toggle")
            key: The key string (e.g., "q", "space", "ctrl+s")
        """
        self.bindings[action] = key
        self.save_bindings()
    
    def get_binding(self, action: str) -> Optional[str]:
        """Get the key binding for an action.
        
        Args:
            action: The action name
            
        Returns:
            The key string, or None if not found
        """
        return self.bindings.get(action)
    
    def reset_to_defaults(self) -> None:
        """Reset all key bindings to defaults."""
        self.bindings = self.DEFAULT_BINDINGS.copy()
        self.save_bindings()
    
    def get_all_bindings(self) -> Dict[str, str]:
        """Get all current key bindings.
        
        Returns:
            Dictionary of all action-to-key mappings
        """
        return self.bindings.copy()
