"""Key bindings configuration and persistence."""

import json
from pathlib import Path
from typing import Optional, Dict


class KeyBindings:
    """Manages customizable keyboard shortcuts with persistence.
    
    Attributes:
        storage_path: Path to the JSON file where bindings are stored
        bindings: Dictionary mapping action names to keys
    """
    
    # Default key bindings
    DEFAULT_BINDINGS = {
        "quit": "q",
        "toggle_todo": "space",
        "delete_todo": "d",
        "postpone_todo": "p",
        "show_help": "question_mark",
        "export_shortcuts": "ctrl+e",
        "customize_keys": "ctrl+k",
        "show_tutorial": "ctrl+t",
    }
    
    # Human-readable action descriptions
    ACTION_DESCRIPTIONS = {
        "quit": "Quit application",
        "toggle_todo": "Toggle TODO completion status",
        "delete_todo": "Delete selected TODO",
        "postpone_todo": "Postpone selected TODO",
        "show_help": "Show keyboard shortcuts help",
        "export_shortcuts": "Export shortcuts cheat sheet",
        "customize_keys": "Customize key bindings",
        "show_tutorial": "Show tutorial for new users",
    }
    
    # Category mapping for organizing shortcuts
    ACTION_CATEGORIES = {
        "Navigation": [],
        "TODO Management": ["toggle_todo", "delete_todo", "postpone_todo"],
        "Help & Information": ["show_help", "show_tutorial", "export_shortcuts"],
        "Application": ["quit", "customize_keys"],
    }
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize key bindings manager.
        
        Args:
            storage_path: Custom path for bindings file. Defaults to ~/.todo-tui-keys.json
        """
        if storage_path is None:
            storage_path = Path.home() / ".todo-tui-keys.json"
        self.storage_path = storage_path
        self.bindings = self._load_bindings()
    
    def _load_bindings(self) -> Dict[str, str]:
        """Load key bindings from storage.
        
        Returns:
            Dictionary of action to key mappings
        """
        if not self.storage_path.exists():
            return self.DEFAULT_BINDINGS.copy()
        
        try:
            data = json.loads(self.storage_path.read_text())
            # Merge with defaults to handle new actions
            bindings = self.DEFAULT_BINDINGS.copy()
            bindings.update(data)
            return bindings
        except (json.JSONDecodeError, IOError):
            return self.DEFAULT_BINDINGS.copy()
    
    def save_bindings(self) -> None:
        """Save current key bindings to storage."""
        self.storage_path.write_text(json.dumps(self.bindings, indent=2))
    
    def get_key(self, action: str) -> str:
        """Get the key bound to an action.
        
        Args:
            action: Action name
            
        Returns:
            Key string for the action
        """
        return self.bindings.get(action, self.DEFAULT_BINDINGS.get(action, ""))
    
    def set_key(self, action: str, key: str) -> None:
        """Set a custom key binding for an action.
        
        Args:
            action: Action name
            key: Key string to bind
        """
        self.bindings[action] = key
        self.save_bindings()
    
    def reset_to_defaults(self) -> None:
        """Reset all key bindings to defaults."""
        self.bindings = self.DEFAULT_BINDINGS.copy()
        self.save_bindings()
    
    def get_all_bindings(self) -> Dict[str, str]:
        """Get all current key bindings.
        
        Returns:
            Dictionary of all bindings
        """
        return self.bindings.copy()
    
    def get_description(self, action: str) -> str:
        """Get human-readable description for an action.
        
        Args:
            action: Action name
            
        Returns:
            Description string
        """
        return self.ACTION_DESCRIPTIONS.get(action, action)
    
    def format_key_for_display(self, key: str) -> str:
        """Format a key string for display.
        
        Args:
            key: Key string (e.g., 'ctrl+e', 'space')
            
        Returns:
            Formatted display string
        """
        replacements = {
            "question_mark": "?",
            "space": "Space",
            "ctrl": "Ctrl",
            "shift": "Shift",
            "alt": "Alt",
        }
        
        display = key
        for old, new in replacements.items():
            display = display.replace(old, new)
        
        # Capitalize first letter of simple keys
        if "+" not in display and len(display) == 1:
            display = display.upper()
        
        return display
