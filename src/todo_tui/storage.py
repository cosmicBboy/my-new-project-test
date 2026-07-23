"""Persistence layer for TODO items."""

import json
from pathlib import Path
from typing import List, Optional
from uuid import UUID
from datetime import datetime

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
    
    def export_json(self, export_path: Path) -> None:
        """Export all TODO items to a JSON file.
        
        Args:
            export_path: Path where the JSON file should be saved
        """
        todos = self.load()
        data = [todo.to_dict() for todo in todos]
        export_path.write_text(json.dumps(data, indent=2))
    
    def export_markdown(self, export_path: Path) -> None:
        """Export all TODO items to a Markdown file.
        
        Args:
            export_path: Path where the Markdown file should be saved
        """
        todos = self.load()
        
        # Group todos by status
        active_todos = [t for t in todos if not t.completed and not t.is_postponed()]
        postponed_todos = [t for t in todos if t.is_postponed() and not t.completed]
        completed_todos = [t for t in todos if t.completed]
        
        lines = []
        lines.append("# TODO List")
        lines.append(f"\n*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        if active_todos:
            lines.append("## Active Tasks\n")
            for todo in active_todos:
                lines.append(f"- [ ] {todo.title}")
                lines.append(f"  - Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                if todo.postpone_until:
                    lines.append(f"  - Postponed until: {todo.postpone_until}")
                lines.append("")
        
        if postponed_todos:
            lines.append("## Postponed Tasks\n")
            for todo in postponed_todos:
                lines.append(f"- [ ] {todo.title}")
                lines.append(f"  - Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                lines.append(f"  - Postponed until: {todo.postpone_until}")
                lines.append("")
        
        if completed_todos:
            lines.append("## Completed Tasks\n")
            for todo in completed_todos:
                lines.append(f"- [x] {todo.title}")
                lines.append(f"  - Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                if todo.completed_at:
                    lines.append(f"  - Completed: {todo.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
                lines.append("")
        
        if not todos:
            lines.append("*No tasks found*\n")
        
        export_path.write_text("\n".join(lines))
    
    def import_json(self, import_path: Path, replace: bool = False) -> int:
        """Import TODO items from a JSON file.
        
        Args:
            import_path: Path to the JSON file to import
            replace: If True, replace all existing todos. If False, append to existing todos.
            
        Returns:
            Number of todos imported
            
        Raises:
            ValueError: If the import file is invalid
            FileNotFoundError: If the import file doesn't exist
        """
        if not import_path.exists():
            raise FileNotFoundError(f"Import file not found: {import_path}")
        
        try:
            data = json.loads(import_path.read_text())
            imported_todos = [TodoItem.from_dict(item) for item in data]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid todo data format: {e}")
        
        if replace:
            self.save(imported_todos)
        else:
            existing_todos = self.load()
            # Avoid duplicates by ID
            existing_ids = {todo.id for todo in existing_todos}
            new_todos = [todo for todo in imported_todos if todo.id not in existing_ids]
            self.save(existing_todos + new_todos)
        
        return len(imported_todos)
