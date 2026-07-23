"""Keyboard binding management for the TODO TUI app."""

import json
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class KeyBinding:
    """Represents a single keyboard binding."""
    action: str
    key: str
    default_key: str
    description: str
    category: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "KeyBinding":
        """Create from dictionary."""
        return cls(**data)


class KeyBindingsManager:
    """Manages customizable keyboard shortcuts."""
    
    DEFAULT_BINDINGS = {
        # Navigation
        "focus_list": KeyBinding(
            action="focus_list",
            key="tab",
            default_key="tab",
            description="Focus the TODO list",
            category="Navigation"
        ),
        "focus_input": KeyBinding(
            action="focus_input",
            key="tab",
            default_key="tab",
            description="Focus the input field",
            category="Navigation"
        ),
        
        # Todo Management
        "toggle_todo": KeyBinding(
            action="toggle_todo",
            key="space",
            default_key="space",
            description="Toggle TODO completion status",
            category="Todo Management"
        ),
        "delete_todo": KeyBinding(
            action="delete_todo",
            key="d",
            default_key="d",
            description="Delete selected TODO",
            category="Todo Management"
        ),
        "postpone_todo": KeyBinding(
            action="postpone_todo",
            key="p",
            default_key="p",
            description="Postpone selected TODO until tomorrow",
            category="Todo Management"
        ),
        "edit_todo": KeyBinding(
            action="edit_todo",
            key="e",
            default_key="e",
            description="Edit selected TODO",
            category="Todo Management"
        ),
        
        # Data Operations
        "export_data": KeyBinding(
            action="export_data",
            key="ctrl+e",
            default_key="ctrl+e",
            description="Export todos (JSON, CSV, Markdown)",
            category="Data Operations"
        ),
        "import_data": KeyBinding(
            action="import_data",
            key="ctrl+i",
            default_key="ctrl+i",
            description="Import todos from JSON file",
            category="Data Operations"
        ),
        
        # Application
        "show_shortcuts": KeyBinding(
            action="show_shortcuts",
            key="question_mark",
            default_key="question_mark",
            description="Show keyboard shortcuts reference",
            category="Application"
        ),
        "show_tutorial": KeyBinding(
            action="show_tutorial",
            key="ctrl+t",
            default_key="ctrl+t",
            description="Show tutorial for new users",
            category="Application"
        ),
        "quit": KeyBinding(
            action="quit",
            key="q",
            default_key="q",
            description="Quit application",
            category="Application"
        ),
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the key bindings manager.
        
        Args:
            config_path: Path to the configuration file
        """
        if config_path is None:
            config_path = Path.home() / ".todo-tui-keybindings.json"
        
        self.config_path = config_path
        self.bindings: Dict[str, KeyBinding] = {}
        self.load()
    
    def load(self) -> None:
        """Load key bindings from config file or use defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    self.bindings = {
                        action: KeyBinding.from_dict(binding_data)
                        for action, binding_data in data.items()
                    }
            except (json.JSONDecodeError, KeyError) as e:
                # If config is corrupted, fall back to defaults
                self.reset_to_defaults()
        else:
            self.reset_to_defaults()
    
    def save(self) -> None:
        """Save current key bindings to config file."""
        data = {
            action: binding.to_dict()
            for action, binding in self.bindings.items()
        }
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def reset_to_defaults(self) -> None:
        """Reset all key bindings to defaults."""
        self.bindings = {
            action: KeyBinding(
                action=binding.action,
                key=binding.default_key,
                default_key=binding.default_key,
                description=binding.description,
                category=binding.category
            )
            for action, binding in self.DEFAULT_BINDINGS.items()
        }
        self.save()
    
    def get_binding(self, action: str) -> Optional[KeyBinding]:
        """Get the key binding for an action.
        
        Args:
            action: The action name
            
        Returns:
            KeyBinding or None if not found
        """
        return self.bindings.get(action)
    
    def get_key(self, action: str) -> str:
        """Get the key for an action.
        
        Args:
            action: The action name
            
        Returns:
            The key string, or the default if not found
        """
        binding = self.get_binding(action)
        if binding:
            return binding.key
        return self.DEFAULT_BINDINGS.get(action, KeyBinding("", "", "", "", "")).default_key
    
    def set_binding(self, action: str, new_key: str) -> None:
        """Set a new key for an action.
        
        Args:
            action: The action name
            new_key: The new key to bind
        """
        if action in self.bindings:
            self.bindings[action].key = new_key
            self.save()
    
    def get_all_bindings(self) -> Dict[str, KeyBinding]:
        """Get all key bindings.
        
        Returns:
            Dictionary of all bindings
        """
        return self.bindings.copy()
    
    def get_bindings_by_category(self) -> Dict[str, list[KeyBinding]]:
        """Get all key bindings organized by category.
        
        Returns:
            Dictionary mapping category names to lists of bindings
        """
        categories: Dict[str, list[KeyBinding]] = {}
        for binding in self.bindings.values():
            if binding.category not in categories:
                categories[binding.category] = []
            categories[binding.category].append(binding)
        return categories
    
    def search_bindings(self, query: str) -> list[KeyBinding]:
        """Search for bindings matching a query.
        
        Args:
            query: Search query (matches action, key, or description)
            
        Returns:
            List of matching bindings
        """
        query = query.lower()
        results = []
        
        for binding in self.bindings.values():
            if (query in binding.action.lower() or
                query in binding.key.lower() or
                query in binding.description.lower() or
                query in binding.category.lower()):
                results.append(binding)
        
        return results
