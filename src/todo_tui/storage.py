"""Persistence layer for TODO items."""

import json
import csv
import shutil
from pathlib import Path
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from .models import TodoItem


class TodoStorage:
    """Handles reading and writing TODO items to disk.
    
    Attributes:
        storage_path: Path to the JSON file where TODOs are stored
        auto_backup_enabled: Whether automatic backups are enabled
        auto_backup_interval_hours: Hours between automatic backups
        _last_backup_time: Timestamp of last automatic backup
        _operations_since_backup: Counter for operations since last backup
    """
    
    def __init__(self, storage_path: Optional[Path] = None, auto_backup_enabled: bool = True):
        """Initialize the storage handler.
        
        Args:
            storage_path: Custom path for storage file. Defaults to ~/.todo-tui.json
            auto_backup_enabled: Whether to enable automatic backups (default: True)
        """
        if storage_path is None:
            storage_path = Path.home() / ".todo-tui.json"
        self.storage_path = storage_path
        self.auto_backup_enabled = auto_backup_enabled
        self.auto_backup_interval_hours = 24  # Create backup once per day
        self._last_backup_time: Optional[datetime] = None
        self._operations_since_backup = 0
        self._ensure_file_exists()
        
        # Check if we need an automatic backup on initialization
        if self.auto_backup_enabled:
            self._check_and_create_auto_backup()
    
    def _ensure_file_exists(self) -> None:
        """Create the storage file if it doesn't exist."""
        if not self.storage_path.exists():
            self.storage_path.write_text("[]")
    
    def _check_and_create_auto_backup(self) -> None:
        """Check if automatic backup is needed and create one if so.
        
        Creates a backup if:
        1. No backup has been created yet in this session, AND
        2. Last backup is older than auto_backup_interval_hours, OR
        3. More than 50 operations have been performed since last backup
        """
        should_backup = False
        
        # Get the most recent backup
        backups = self.list_backups()
        
        if not backups:
            # No backups exist, create one
            should_backup = True
        elif self._last_backup_time is None:
            # First check in this session - check if last backup is old
            last_backup = backups[0]
            last_backup_time = datetime.fromtimestamp(last_backup.stat().st_mtime)
            time_since_backup = datetime.now() - last_backup_time
            
            if time_since_backup > timedelta(hours=self.auto_backup_interval_hours):
                should_backup = True
            
            self._last_backup_time = last_backup_time
        elif self._operations_since_backup >= 50:
            # Many operations since last backup - create a new one
            should_backup = True
        
        if should_backup:
            try:
                self.create_backup()
                self._last_backup_time = datetime.now()
                self._operations_since_backup = 0
            except Exception:
                # Silently fail on backup errors - don't interrupt normal operation
                pass
    
    def _increment_operation_counter(self) -> None:
        """Increment the operations counter and check if backup is needed."""
        if not self.auto_backup_enabled:
            return
        
        self._operations_since_backup += 1
        
        # Check if we should create a backup based on operation count
        if self._operations_since_backup >= 50:
            self._check_and_create_auto_backup()
    
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
        self._increment_operation_counter()
    
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
    
    def export_json(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to JSON format.
        
        Args:
            export_path: Path to save the JSON file
            todos: List of todos to export (defaults to all todos)
        """
        if todos is None:
            todos = self.load()
        
        data = [todo.to_dict() for todo in todos]
        export_path.write_text(json.dumps(data, indent=2))
    
    def export_csv(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to CSV format.
        
        Args:
            export_path: Path to save the CSV file
            todos: List of todos to export (defaults to all todos)
        """
        if todos is None:
            todos = self.load()
        
        with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'completed', 'created_at', 'completed_at', 'postpone_until']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for todo in todos:
                writer.writerow(todo.to_dict())
    
    def export_markdown(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to Markdown format.
        
        Args:
            export_path: Path to save the Markdown file
            todos: List of todos to export (defaults to all todos)
        """
        if todos is None:
            todos = self.load()
        
        lines = ["# TODO List\n"]
        
        # Separate active and completed todos
        active_todos = [t for t in todos if not t.completed]
        completed_todos = [t for t in todos if t.completed]
        
        if active_todos:
            lines.append("\n## Active Tasks\n")
            for todo in active_todos:
                postponed = f" *(postponed until {todo.postpone_until})*" if todo.is_postponed() else ""
                lines.append(f"- [ ] {todo.title}{postponed}\n")
        
        if completed_todos:
            lines.append("\n## Completed Tasks\n")
            for todo in completed_todos:
                completed_date = f" *(completed {todo.completed_at.strftime('%Y-%m-%d')})*" if todo.completed_at else ""
                lines.append(f"- [x] {todo.title}{completed_date}\n")
        
        export_path.write_text(''.join(lines))
    
    def export_html(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to HTML format.
        
        Args:
            export_path: Path to save the HTML file
            todos: List of todos to export (defaults to all todos)
        """
        if todos is None:
            todos = self.load()
        
        # Separate active and completed todos
        active_todos = [t for t in todos if not t.completed]
        completed_todos = [t for t in todos if t.completed]
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>TODO List</title>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }',
            '        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }',
            '        h2 { color: #666; margin-top: 30px; }',
            '        ul { list-style-type: none; padding: 0; }',
            '        li { padding: 10px; margin: 5px 0; background: #f8f9fa; border-left: 3px solid #007bff; }',
            '        li.completed { background: #e9ecef; border-left-color: #28a745; text-decoration: line-through; color: #666; }',
            '        li.postponed { background: #fff3cd; border-left-color: #ffc107; }',
            '        .checkbox { font-weight: bold; margin-right: 10px; }',
            '        .meta { font-size: 0.85em; color: #666; margin-left: 20px; font-style: italic; }',
            '    </style>',
            '</head>',
            '<body>',
            '    <h1>TODO List</h1>',
        ]
        
        if active_todos:
            html_parts.append('    <h2>Active Tasks</h2>')
            html_parts.append('    <ul>')
            for todo in active_todos:
                postponed_class = ' class="postponed"' if todo.is_postponed() else ''
                postponed_text = f'<span class="meta">postponed until {todo.postpone_until}</span>' if todo.is_postponed() else ''
                html_parts.append(f'        <li{postponed_class}>')
                html_parts.append(f'            <span class="checkbox">☐</span>{todo.title}')
                if postponed_text:
                    html_parts.append(f'            {postponed_text}')
                html_parts.append('        </li>')
            html_parts.append('    </ul>')
        
        if completed_todos:
            html_parts.append('    <h2>Completed Tasks</h2>')
            html_parts.append('    <ul>')
            for todo in completed_todos:
                completed_date = f'<span class="meta">completed {todo.completed_at.strftime("%Y-%m-%d")}</span>' if todo.completed_at else ''
                html_parts.append('        <li class="completed">')
                html_parts.append(f'            <span class="checkbox">☑</span>{todo.title}')
                if completed_date:
                    html_parts.append(f'            {completed_date}')
                html_parts.append('        </li>')
            html_parts.append('    </ul>')
        
        html_parts.extend([
            '</body>',
            '</html>',
        ])
        
        export_path.write_text('\n'.join(html_parts))
    
    def export(self, export_path: Path, format: str = 'json', todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to specified format.
        
        Args:
            export_path: Path to save the export file
            format: Export format ('json', 'csv', 'markdown', 'html')
            todos: List of todos to export (defaults to all todos)
            
        Raises:
            ValueError: If format is not supported
        """
        format = format.lower()
        if format == 'json':
            self.export_json(export_path, todos)
        elif format == 'csv':
            self.export_csv(export_path, todos)
        elif format in ('markdown', 'md'):
            self.export_markdown(export_path, todos)
        elif format == 'html':
            self.export_html(export_path, todos)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def import_json(self, import_path: Path, merge: bool = False) -> List[TodoItem]:
        """Import TODO items from JSON file.
        
        Args:
            import_path: Path to the JSON file to import
            merge: If True, merge with existing todos. If False, replace all todos.
            
        Returns:
            List of imported TodoItem objects
            
        Raises:
            FileNotFoundError: If import file doesn't exist
            ValueError: If import file is invalid or corrupted
        """
        if not import_path.exists():
            raise FileNotFoundError(f"Import file not found: {import_path}")
        
        try:
            data = json.loads(import_path.read_text())
            imported_todos = [TodoItem.from_dict(item) for item in data]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid data format: {e}")
        
        if merge:
            # Merge with existing todos, avoiding duplicates by ID
            existing_todos = self.load()
            existing_ids = {todo.id for todo in existing_todos}
            
            new_todos = [todo for todo in imported_todos if todo.id not in existing_ids]
            all_todos = existing_todos + new_todos
            self.save(all_todos)
            return new_todos
        else:
            # Replace all todos
            self.save(imported_todos)
            return imported_todos
    
    def create_backup(self, backup_dir: Optional[Path] = None) -> Path:
        """Create a backup of the current TODO storage.
        
        Args:
            backup_dir: Directory to store backups (defaults to ~/.todo-tui-backups/)
            
        Returns:
            Path to the created backup file
        """
        if backup_dir is None:
            backup_dir = Path.home() / ".todo-tui-backups"
        
        backup_dir.mkdir(exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"todo-backup-{timestamp}.json"
        
        # Copy current storage to backup
        if self.storage_path.exists():
            shutil.copy2(self.storage_path, backup_path)
        
        return backup_path
    
    def restore_backup(self, backup_path: Path) -> None:
        """Restore TODO items from a backup file.
        
        Args:
            backup_path: Path to the backup file
            
        Raises:
            FileNotFoundError: If backup file doesn't exist
            ValueError: If backup file is invalid
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        # Validate backup before restoring
        try:
            data = json.loads(backup_path.read_text())
            todos = [TodoItem.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid backup file: {e}")
        
        # Create a backup of current state before restoring
        self.create_backup()
        
        # Restore from backup
        self.save(todos)
    
    def list_backups(self, backup_dir: Optional[Path] = None) -> List[Path]:
        """List all available backup files.
        
        Args:
            backup_dir: Directory containing backups (defaults to ~/.todo-tui-backups/)
            
        Returns:
            List of backup file paths, sorted by creation time (newest first)
        """
        if backup_dir is None:
            backup_dir = Path.home() / ".todo-tui-backups"
        
        if not backup_dir.exists():
            return []
        
        backups = list(backup_dir.glob("todo-backup-*.json"))
        return sorted(backups, key=lambda p: p.stat().st_mtime, reverse=True)
    
    def archive_completed(self, archive_path: Optional[Path] = None) -> int:
        """Archive completed TODO items to a separate file and remove them from storage.
        
        Args:
            archive_path: Path to archive file (defaults to ~/.todo-tui-archive.json)
            
        Returns:
            Number of items archived
        """
        if archive_path is None:
            archive_path = Path.home() / ".todo-tui-archive.json"
        
        # Load current todos
        todos = self.load()
        
        # Separate completed and active todos
        completed_todos = [t for t in todos if t.completed]
        active_todos = [t for t in todos if not t.completed]
        
        if not completed_todos:
            return 0
        
        # Load existing archive
        archived_todos = []
        if archive_path.exists():
            try:
                data = json.loads(archive_path.read_text())
                archived_todos = [TodoItem.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                # If archive is corrupted, start fresh
                archived_todos = []
        
        # Add completed todos to archive
        archived_todos.extend(completed_todos)
        
        # Save archive
        data = [todo.to_dict() for todo in archived_todos]
        archive_path.write_text(json.dumps(data, indent=2))
        
        # Save only active todos to main storage
        self.save(active_todos)
        
        return len(completed_todos)
    
    def load_archive(self, archive_path: Optional[Path] = None) -> List[TodoItem]:
        """Load archived TODO items.
        
        Args:
            archive_path: Path to archive file (defaults to ~/.todo-tui-archive.json)
            
        Returns:
            List of archived TodoItem objects
        """
        if archive_path is None:
            archive_path = Path.home() / ".todo-tui-archive.json"
        
        if not archive_path.exists():
            return []
        
        try:
            data = json.loads(archive_path.read_text())
            return [TodoItem.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def shutdown(self) -> None:
        """Perform cleanup operations when shutting down.
        
        Creates a final automatic backup if needed.
        """
        if self.auto_backup_enabled and self._operations_since_backup > 0:
            self._check_and_create_auto_backup()
