"""Persistence layer for TODO items and user preferences."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import UUID

from .models import TodoItem


class TodoStorage:
    """Handles reading and writing TODO items to disk.
    
    Attributes:
        storage_path: Path to the JSON file where TODOs are stored
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize the storage handler.
        
        Args:
            storage_path: Custom path for storage file. Defaults to ~/.todo-tui.json
        """
        if storage_path is None:
            storage_path = Path.home() / ".todo-tui.json"
        self.storage_path = storage_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create the storage file if it doesn't exist."""
        if not self.storage_path.exists():
            self.storage_path.write_text("[]")
    
    def load(self) -> List[TodoItem]:
        """Load all TODO items from storage.
        
        Returns:
            List of TodoItem objects
            
        Raises:
            ValueError: If the storage file is corrupted
        """
        try:
            data = json.loads(self.storage_path.read_text())
            return [TodoItem.from_dict(item) for item in data]
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted storage file: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid data format in storage: {e}")
    
    def save(self, todos: List[TodoItem]) -> None:
        """Save all TODO items to storage.
        
        Args:
            todos: List of TodoItem objects to save
        """
        data = [todo.to_dict() for todo in todos]
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def add(self, todo: TodoItem) -> None:
        """Add a new TODO item to storage.
        
        Args:
            todo: TodoItem to add
        """
        todos = self.load()
        todos.append(todo)
        self.save(todos)
    
    def update(self, todo: TodoItem) -> None:
        """Update an existing TODO item in storage.
        
        Args:
            todo: TodoItem with updated data
            
        Raises:
            ValueError: If the TODO item doesn't exist
        """
        todos = self.load()
        for i, existing_todo in enumerate(todos):
            if existing_todo.id == todo.id:
                todos[i] = todo
                self.save(todos)
                return
        raise ValueError(f"Todo with id {todo.id} not found")
    
    def delete(self, todo_id: UUID) -> None:
        """Delete a TODO item from storage.
        
        Args:
            todo_id: UUID of the TODO item to delete
            
        Raises:
            ValueError: If the TODO item doesn't exist
        """
        todos = self.load()
        original_length = len(todos)
        todos = [todo for todo in todos if todo.id != todo_id]
        if len(todos) == original_length:
            raise ValueError(f"Todo with id {todo_id} not found")
        self.save(todos)
    
    def get_all(self) -> List[TodoItem]:
        """Get all TODO items.
        
        Returns:
            List of all TodoItem objects
        """
        return self.load()
    
    def clear(self) -> None:
        """Remove all TODO items from storage."""
        self.save([])


class PreferencesStorage:
    """Handles reading and writing user preferences to disk.
    
    Attributes:
        preferences_path: Path to the JSON file where preferences are stored
    """
    
    def __init__(self, preferences_path: Optional[Path] = None):
        """Initialize the preferences storage handler.
        
        Args:
            preferences_path: Custom path for preferences file. 
                            Defaults to ~/.todo-tui-preferences.json
        """
        if preferences_path is None:
            preferences_path = Path.home() / ".todo-tui-preferences.json"
        self.preferences_path = preferences_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create the preferences file if it doesn't exist."""
        if not self.preferences_path.exists():
            self.preferences_path.write_text("{}")
    
    def load(self) -> Dict[str, Any]:
        """Load user preferences from storage.
        
        Returns:
            Dictionary of preference keys and values
            
        Raises:
            ValueError: If the preferences file is corrupted
        """
        try:
            data = json.loads(self.preferences_path.read_text())
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted preferences file: {e}")
    
    def save(self, preferences: Dict[str, Any]) -> None:
        """Save user preferences to storage.
        
        Args:
            preferences: Dictionary of preference keys and values
        """
        self.preferences_path.write_text(json.dumps(preferences, indent=2))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a preference value.
        
        Args:
            key: Preference key
            default: Default value if key doesn't exist
            
        Returns:
            Preference value or default
        """
        preferences = self.load()
        return preferences.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a preference value.
        
        Args:
            key: Preference key
            value: Preference value
        """
        preferences = self.load()
        preferences[key] = value
        self.save(preferences)
    
    def get_theme(self) -> str:
        """Get the current theme preference.
        
        Returns:
            Theme name, defaults to 'colorful'
        """
        return self.get("theme", "colorful")
    
    def set_theme(self, theme_name: str) -> None:
        """Set the current theme preference.
        
        Args:
            theme_name: Name of the theme
        """
        self.set("theme", theme_name)
    
    def get_layout_density(self) -> str:
        """Get the layout density preference.
        
        Returns:
            Layout density, defaults to 'comfortable'
        """
        return self.get("layout_density", "comfortable")
    
    def set_layout_density(self, density: str) -> None:
        """Set the layout density preference.
        
        Args:
            density: Layout density setting
        """
        self.set("layout_density", density)
    
    def get_font_size(self) -> str:
        """Get the font size preference.
        
        Returns:
            Font size, defaults to 'medium'
        """
        return self.get("font_size", "medium")
    
    def set_font_size(self, size: str) -> None:
        """Set the font size preference.
        
        Args:
            size: Font size setting
        """
        self.set("font_size", size)
    
    def get_custom_themes(self) -> List[Dict[str, Any]]:
        """Get list of custom themes.
        
        Returns:
            List of custom theme dictionaries
        """
        return self.get("custom_themes", [])
    
    def add_custom_theme(self, theme_data: Dict[str, Any]) -> None:
        """Add a custom theme.
        
        Args:
            theme_data: Dictionary with theme data (name, display_name, colors)
        """
        custom_themes = self.get_custom_themes()
        # Remove existing theme with same name
        custom_themes = [t for t in custom_themes if t.get("name") != theme_data.get("name")]
        custom_themes.append(theme_data)
        self.set("custom_themes", custom_themes)
    
    def clear(self) -> None:
        """Clear all preferences."""
        self.save({})
