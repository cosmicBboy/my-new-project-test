"""Persistence layer for TODO items."""

import json
from pathlib import Path
from typing import List, Optional
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
