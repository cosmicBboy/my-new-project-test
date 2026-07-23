"""Persistence layer for TODO items."""

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Literal
from uuid import UUID

from .models import TodoItem


ExportFormat = Literal["json", "csv", "markdown", "html"]
ImportMode = Literal["replace", "merge"]


class TodoStorage:
    """Handles reading and writing TODO items to disk.
    
    Attributes:
        storage_path: Path to the JSON file where TODOs are stored
        backup_dir: Directory where automatic backups are stored
        enable_auto_backup: Whether to create automatic backups on save
    """
    
    def __init__(
        self,
        storage_path: Optional[Path] = None,
        enable_auto_backup: bool = True,
        backup_dir: Optional[Path] = None,
    ):
        """Initialize the storage handler.
        
        Args:
            storage_path: Custom path for storage file. Defaults to ~/.todo-tui.json
            enable_auto_backup: Whether to enable automatic backups. Defaults to True
            backup_dir: Directory for backups. Defaults to ~/.todo-tui-backups/
        """
        if storage_path is None:
            storage_path = Path.home() / ".todo-tui.json"
        self.storage_path = storage_path
        self.enable_auto_backup = enable_auto_backup
        
        if backup_dir is None:
            backup_dir = Path.home() / ".todo-tui-backups"
        self.backup_dir = backup_dir
        
        self._ensure_file_exists()
        if self.enable_auto_backup:
            self._ensure_backup_dir_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create the storage file if it doesn't exist."""
        if not self.storage_path.exists():
            self.storage_path.write_text("[]")
    
    def _ensure_backup_dir_exists(self) -> None:
        """Create the backup directory if it doesn't exist."""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_backup(self) -> Optional[Path]:
        """Create a backup of the current storage file.
        
        Returns:
            Path to the backup file, or None if backup creation failed
        """
        if not self.enable_auto_backup or not self.storage_path.exists():
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"todo-backup-{timestamp}.json"
            shutil.copy2(self.storage_path, backup_path)
            
            # Keep only the last 10 backups
            self._cleanup_old_backups(keep=10)
            
            return backup_path
        except Exception:
            # Don't fail the main operation if backup fails
            return None
    
    def _cleanup_old_backups(self, keep: int = 10) -> None:
        """Remove old backup files, keeping only the most recent ones.
        
        Args:
            keep: Number of most recent backups to keep
        """
        if not self.backup_dir.exists():
            return
        
        backups = sorted(
            self.backup_dir.glob("todo-backup-*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        
        # Delete old backups
        for backup in backups[keep:]:
            try:
                backup.unlink()
            except Exception:
                pass
    
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
        # Create backup before saving
        self._create_backup()
        
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
    
    def archive_completed(self) -> tuple[int, Path]:
        """Archive completed TODO items to a separate file.
        
        Removes all completed items from the main storage and saves them
        to an archive file with a timestamp.
        
        Returns:
            Tuple of (number of items archived, path to archive file)
        """
        todos = self.load()
        completed = [todo for todo in todos if todo.completed]
        active = [todo for todo in todos if not todo.completed]
        
        if not completed:
            return (0, None)
        
        # Save active todos back to main storage
        self.save(active)
        
        # Save completed todos to archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = self.backup_dir / f"todo-archive-{timestamp}.json"
        self._ensure_backup_dir_exists()
        
        archive_data = [todo.to_dict() for todo in completed]
        archive_path.write_text(json.dumps(archive_data, indent=2))
        
        return (len(completed), archive_path)
    
    def export_json(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to JSON format.
        
        Args:
            export_path: Path where the JSON file will be saved
            todos: List of todos to export. If None, exports all todos
        """
        if todos is None:
            todos = self.load()
        
        data = [todo.to_dict() for todo in todos]
        export_path.expanduser().write_text(json.dumps(data, indent=2))
    
    def export_csv(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to CSV format.
        
        Args:
            export_path: Path where the CSV file will be saved
            todos: List of todos to export. If None, exports all todos
        """
        if todos is None:
            todos = self.load()
        
        export_path = export_path.expanduser()
        with export_path.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Title', 'Completed', 'Created At', 'Completed At', 'Postponed Until'])
            
            for todo in todos:
                writer.writerow([
                    str(todo.id),
                    todo.title,
                    'Yes' if todo.completed else 'No',
                    todo.created_at.isoformat(),
                    todo.completed_at.isoformat() if todo.completed_at else '',
                    todo.postpone_until.isoformat() if todo.postpone_until else '',
                ])
    
    def export_markdown(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to Markdown format.
        
        Args:
            export_path: Path where the Markdown file will be saved
            todos: List of todos to export. If None, exports all todos
        """
        if todos is None:
            todos = self.load()
        
        lines = ['# TODO List\n\n']
        
        # Separate active and completed todos
        active_todos = [t for t in todos if not t.completed]
        completed_todos = [t for t in todos if t.completed]
        
        if active_todos:
            lines.append('## Active Tasks\n\n')
            for todo in active_todos:
                checkbox = '- [ ]'
                postponed = f' *(postponed until {todo.postpone_until})*' if todo.is_postponed() else ''
                lines.append(f'{checkbox} {todo.title}{postponed}\n')
            lines.append('\n')
        
        if completed_todos:
            lines.append('## Completed Tasks\n\n')
            for todo in completed_todos:
                checkbox = '- [x]'
                completed_date = f' *(completed {todo.completed_at.date()})*' if todo.completed_at else ''
                lines.append(f'{checkbox} {todo.title}{completed_date}\n')
        
        export_path.expanduser().write_text(''.join(lines))
    
    def export_html(self, export_path: Path, todos: Optional[List[TodoItem]] = None) -> None:
        """Export TODO items to HTML format.
        
        Args:
            export_path: Path where the HTML file will be saved
            todos: List of todos to export. If None, exports all todos
        """
        if todos is None:
            todos = self.load()
        
        # Separate active and completed todos
        active_todos = [t for t in todos if not t.completed]
        completed_todos = [t for t in todos if t.completed]
        
        html = ['<!DOCTYPE html>']
        html.append('<html lang="en">')
        html.append('<head>')
        html.append('    <meta charset="UTF-8">')
        html.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html.append('    <title>TODO List</title>')
        html.append('    <style>')
        html.append('        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }')
        html.append('        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }')
        html.append('        h2 { color: #555; margin-top: 30px; }')
        html.append('        ul { list-style: none; padding: 0; }')
        html.append('        li { padding: 10px; margin: 5px 0; background: #f9f9f9; border-left: 4px solid #4CAF50; }')
        html.append('        li.completed { background: #e8f5e9; border-left-color: #81C784; text-decoration: line-through; color: #666; }')
        html.append('        li.postponed { background: #fff3e0; border-left-color: #FFB74D; }')
        html.append('        .checkbox { display: inline-block; width: 20px; height: 20px; border: 2px solid #4CAF50; margin-right: 10px; vertical-align: middle; }')
        html.append('        .checkbox.checked { background: #4CAF50; }')
        html.append('        .checkbox.checked::after { content: "✓"; color: white; font-weight: bold; display: block; text-align: center; line-height: 16px; }')
        html.append('        .meta { font-size: 0.85em; color: #999; font-style: italic; margin-left: 30px; }')
        html.append('    </style>')
        html.append('</head>')
        html.append('<body>')
        html.append('    <h1>📝 TODO List</h1>')
        
        if active_todos:
            html.append('    <h2>Active Tasks</h2>')
            html.append('    <ul>')
            for todo in active_todos:
                li_class = 'postponed' if todo.is_postponed() else ''
                html.append(f'        <li class="{li_class}">')
                html.append('            <span class="checkbox"></span>')
                html.append(f'            {todo.title}')
                if todo.is_postponed():
                    html.append(f'            <div class="meta">Postponed until {todo.postpone_until}</div>')
                html.append('        </li>')
            html.append('    </ul>')
        
        if completed_todos:
            html.append('    <h2>Completed Tasks</h2>')
            html.append('    <ul>')
            for todo in completed_todos:
                html.append('        <li class="completed">')
                html.append('            <span class="checkbox checked"></span>')
                html.append(f'            {todo.title}')
                if todo.completed_at:
                    html.append(f'            <div class="meta">Completed on {todo.completed_at.date()}</div>')
                html.append('        </li>')
            html.append('    </ul>')
        
        html.append('</body>')
        html.append('</html>')
        
        export_path.expanduser().write_text('\n'.join(html))
    
    def export(
        self,
        export_path: Path,
        format: ExportFormat = "json",
        todos: Optional[List[TodoItem]] = None,
    ) -> None:
        """Export TODO items to the specified format.
        
        Args:
            export_path: Path where the file will be saved
            format: Export format (json, csv, markdown, html)
            todos: List of todos to export. If None, exports all todos
            
        Raises:
            ValueError: If the format is not supported
        """
        export_methods = {
            "json": self.export_json,
            "csv": self.export_csv,
            "markdown": self.export_markdown,
            "html": self.export_html,
        }
        
        if format not in export_methods:
            raise ValueError(f"Unsupported export format: {format}")
        
        export_methods[format](export_path, todos)
    
    def import_json(self, import_path: Path, mode: ImportMode = "merge") -> int:
        """Import TODO items from a JSON file.
        
        Args:
            import_path: Path to the JSON file to import
            mode: Import mode - 'replace' replaces all existing todos,
                  'merge' adds imported todos to existing ones (skips duplicates)
            
        Returns:
            Number of todos imported
            
        Raises:
            FileNotFoundError: If the import file doesn't exist
            ValueError: If the JSON file is invalid or corrupted
        """
        import_path = import_path.expanduser()
        
        if not import_path.exists():
            raise FileNotFoundError(f"Import file not found: {import_path}")
        
        try:
            data = json.loads(import_path.read_text())
            imported_todos = [TodoItem.from_dict(item) for item in data]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid data format in import file: {e}")
        
        if mode == "replace":
            self.save(imported_todos)
            return len(imported_todos)
        else:  # merge mode
            existing_todos = self.load()
            existing_ids = {todo.id for todo in existing_todos}
            
            # Only add todos that don't already exist
            new_todos = [todo for todo in imported_todos if todo.id not in existing_ids]
            all_todos = existing_todos + new_todos
            
            self.save(all_todos)
            return len(new_todos)
