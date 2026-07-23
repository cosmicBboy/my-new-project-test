"""Tests for the storage layer."""

import pytest
import tempfile
import csv
import time
from pathlib import Path
from uuid import uuid4
from datetime import date, timedelta, datetime

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    storage = TodoStorage(storage_path, auto_backup_enabled=False)
    yield storage
    
    # Cleanup
    if storage_path.exists():
        storage_path.unlink()


@pytest.fixture
def temp_storage_with_auto_backup():
    """Create a temporary storage file with auto-backup enabled for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        backup_dir = Path(tmpdir)
        storage = TodoStorage(storage_path, auto_backup_enabled=True)
        # Override backup directory for testing
        storage._backup_dir = backup_dir
        
        # Patch list_backups and create_backup to use test directory
        original_create_backup = storage.create_backup
        original_list_backups = storage.list_backups
        
        def create_backup_wrapper(backup_dir_arg=None):
            return original_create_backup(backup_dir if backup_dir_arg is None else backup_dir_arg)
        
        def list_backups_wrapper(backup_dir_arg=None):
            return original_list_backups(backup_dir if backup_dir_arg is None else backup_dir_arg)
        
        storage.create_backup = create_backup_wrapper
        storage.list_backups = list_backups_wrapper
        
        yield storage, backup_dir
    
    # Cleanup
    if storage_path.exists():
        storage_path.unlink()


def test_storage_initialization(temp_storage):
    """Test storage initialization creates file."""
    assert temp_storage.storage_path.exists()


def test_storage_add_and_load(temp_storage):
    """Test adding and loading todos."""
    todo = TodoItem(title="Test task")
    temp_storage.add(todo)
    
    todos = temp_storage.load()
    assert len(todos) == 1
    assert todos[0].title == "Test task"
    assert todos[0].id == todo.id


def test_storage_save_and_load_multiple(temp_storage):
    """Test saving and loading multiple todos."""
    todos = [
        TodoItem(title="Task 1"),
        TodoItem(title="Task 2"),
        TodoItem(title="Task 3"),
    ]
    
    temp_storage.save(todos)
    loaded = temp_storage.load()
    
    assert len(loaded) == 3
    assert [t.title for t in loaded] == ["Task 1", "Task 2", "Task 3"]


def test_storage_update(temp_storage):
    """Test updating a todo."""
    todo = TodoItem(title="Test task")
    temp_storage.add(todo)
    
    # Update the todo
    todo.toggle_completed()
    temp_storage.update(todo)
    
    # Verify update
    loaded = temp_storage.load()
    assert len(loaded) == 1
    assert loaded[0].completed is True


def test_storage_update_nonexistent(temp_storage):
    """Test updating a non-existent todo raises error."""
    todo = TodoItem(title="Test task")
    
    with pytest.raises(ValueError, match="not found"):
        temp_storage.update(todo)


def test_storage_delete(temp_storage):
    """Test deleting a todo."""
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    
    temp_storage.add(todo1)
    temp_storage.add(todo2)
    
    # Delete first todo
    temp_storage.delete(todo1.id)
    
    loaded = temp_storage.load()
    assert len(loaded) == 1
    assert loaded[0].title == "Task 2"


def test_storage_delete_nonexistent(temp_storage):
    """Test deleting a non-existent todo raises error."""
    with pytest.raises(ValueError, match="not found"):
        temp_storage.delete(uuid4())


def test_storage_get_all(temp_storage):
    """Test getting all todos."""
    todos = [
        TodoItem(title="Task 1"),
        TodoItem(title="Task 2"),
    ]
    
    temp_storage.save(todos)
    all_todos = temp_storage.get_all()
    
    assert len(all_todos) == 2
    assert all_todos[0].title == "Task 1"
    assert all_todos[1].title == "Task 2"


def test_storage_clear(temp_storage):
    """Test clearing all todos."""
    todos = [
        TodoItem(title="Task 1"),
        TodoItem(title="Task 2"),
    ]
    
    temp_storage.save(todos)
    temp_storage.clear()
    
    loaded = temp_storage.load()
    assert len(loaded) == 0


def test_storage_corrupted_file():
    """Test handling of corrupted storage file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write("invalid json content {{{")
        storage_path = Path(f.name)
    
    storage = TodoStorage(storage_path, auto_backup_enabled=False)
    
    with pytest.raises(ValueError, match="Corrupted storage file"):
        storage.load()
    
    # Cleanup
    storage_path.unlink()


def test_auto_backup_on_initialization(temp_storage_with_auto_backup):
    """Test that automatic backup is created on initialization if needed."""
    storage, backup_dir = temp_storage_with_auto_backup
    
    # Add some todos
    todos = [TodoItem(title="Task 1"), TodoItem(title="Task 2")]
    storage.save(todos)
    
    # Check if backups were created
    backups = list(backup_dir.glob("todo-backup-*.json"))
    assert len(backups) >= 1


def test_auto_backup_after_many_operations(temp_storage_with_auto_backup):
    """Test that automatic backup is created after many operations."""
    storage, backup_dir = temp_storage_with_auto_backup
    
    # Perform many operations
    for i in range(60):
        storage.add(TodoItem(title=f"Task {i}"))
    
    # Should have created automatic backup(s)
    backups = list(backup_dir.glob("todo-backup-*.json"))
    assert len(backups) >= 1


def test_auto_backup_on_shutdown(temp_storage_with_auto_backup):
    """Test that automatic backup is created on shutdown if there were operations."""
    storage, backup_dir = temp_storage_with_auto_backup
    
    # Clear any existing backups
    for backup in backup_dir.glob("todo-backup-*.json"):
        backup.unlink()
    
    # Perform some operations
    storage.add(TodoItem(title="Task 1"))
    storage.add(TodoItem(title="Task 2"))
    
    # Call shutdown
    storage.shutdown()
    
    # Should have created a backup
    backups = list(backup_dir.glob("todo-backup-*.json"))
    assert len(backups) >= 1


def test_auto_backup_disabled():
    """Test that automatic backup can be disabled."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path, auto_backup_enabled=False)
        
        # Perform many operations
        for i in range(60):
            storage.add(TodoItem(title=f"Task {i}"))
        
        # Get default backup directory
        backup_dir = Path.home() / ".todo-tui-backups"
        
        # Should not have created any backups (or only pre-existing ones)
        backups_before = len(list(backup_dir.glob("todo-backup-*.json"))) if backup_dir.exists() else 0
        
        storage.shutdown()
        
        # Should not have created new backups
        backups_after = len(list(backup_dir.glob("todo-backup-*.json"))) if backup_dir.exists() else 0
        assert backups_after == backups_before
    finally:
        storage_path.unlink()


def test_export_json(temp_storage):
    """Test exporting todos to JSON format."""
    # Create test todos
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    
    temp_storage.save([todo1, todo2])
    
    # Export to JSON
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path)
        
        # Verify export
        import json
        data = json.loads(export_path.read_text())
        assert len(data) == 2
        assert data[0]['title'] == "Task 1"
        assert data[0]['completed'] is False
        assert data[1]['title'] == "Task 2"
        assert data[1]['completed'] is True
    finally:
        export_path.unlink()


def test_export_csv(temp_storage):
    """Test exporting todos to CSV format."""
    # Create test todos
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    
    temp_storage.save([todo1, todo2])
    
    # Export to CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_csv(export_path)
        
        # Verify export
        with open(export_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 2
            assert rows[0]['title'] == "Task 1"
            assert rows[0]['completed'] == 'False'
            assert rows[1]['title'] == "Task 2"
            assert rows[1]['completed'] == 'True'
    finally:
        export_path.unlink()


def test_export_markdown(temp_storage):
    """Test exporting todos to Markdown format."""
    # Create test todos
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    
    temp_storage.save([todo1, todo2])
    
    # Export to Markdown
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_markdown(export_path)
        
        # Verify export
        content = export_path.read_text()
        assert "# TODO List" in content
        assert "## Active Tasks" in content
        assert "- [ ] Task 1" in content
        assert "## Completed Tasks" in content
        assert "- [x] Task 2" in content
    finally:
        export_path.unlink()


def test_export_html(temp_storage):
    """Test exporting todos to HTML format."""
    # Create test todos
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    
    temp_storage.save([todo1, todo2])
    
    # Export to HTML
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_html(export_path)
        
        # Verify export
        content = export_path.read_text()
        assert "<!DOCTYPE html>" in content
        assert "<title>TODO List</title>" in content
        assert "Active Tasks" in content
        assert "Task 1" in content
        assert "Completed Tasks" in content
        assert "Task 2" in content
    finally:
        export_path.unlink()


def test_export_with_format_detection(temp_storage):
    """Test export with automatic format detection."""
    todo = TodoItem(title="Test task")
    temp_storage.save([todo])
    
    # Test JSON export
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json_path = Path(f.name)
    
    try:
        temp_storage.export(json_path, format='json')
        assert json_path.exists()
        assert "Test task" in json_path.read_text()
    finally:
        json_path.unlink()


def test_export_unsupported_format(temp_storage):
    """Test export with unsupported format raises error."""
    todo = TodoItem(title="Test task")
    temp_storage.save([todo])
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        export_path = Path(f.name)
    
    try:
        with pytest.raises(ValueError, match="Unsupported export format"):
            temp_storage.export(export_path, format='txt')
    finally:
        export_path.unlink()


def test_import_json_replace(temp_storage):
    """Test importing todos with replace mode."""
    # Create some existing todos
    existing = [TodoItem(title="Existing 1"), TodoItem(title="Existing 2")]
    temp_storage.save(existing)
    
    # Create import data
    import_todos = [TodoItem(title="Imported 1"), TodoItem(title="Imported 2")]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
    
    try:
        # Save import data
        import json
        data = [todo.to_dict() for todo in import_todos]
        import_path.write_text(json.dumps(data))
        
        # Import with replace mode
        result = temp_storage.import_json(import_path, merge=False)
        
        # Verify replace
        loaded = temp_storage.load()
        assert len(loaded) == 2
        assert loaded[0].title == "Imported 1"
        assert loaded[1].title == "Imported 2"
        assert len(result) == 2
    finally:
        import_path.unlink()


def test_import_json_merge(temp_storage):
    """Test importing todos with merge mode."""
    # Create some existing todos
    existing = [TodoItem(title="Existing 1"), TodoItem(title="Existing 2")]
    temp_storage.save(existing)
    
    # Create import data with one duplicate ID and one new
    import_todos = [
        existing[0],  # Duplicate - should be skipped
        TodoItem(title="New task")  # New - should be added
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
    
    try:
        # Save import data
        import json
        data = [todo.to_dict() for todo in import_todos]
        import_path.write_text(json.dumps(data))
        
        # Import with merge mode
        result = temp_storage.import_json(import_path, merge=True)
        
        # Verify merge - should have 3 todos (2 existing + 1 new)
        loaded = temp_storage.load()
        assert len(loaded) == 3
        assert len(result) == 1  # Only 1 new todo added
        assert result[0].title == "New task"
    finally:
        import_path.unlink()


def test_import_json_missing_file(temp_storage):
    """Test importing from missing file raises error."""
    with pytest.raises(FileNotFoundError):
        temp_storage.import_json(Path("/nonexistent/file.json"))


def test_import_json_invalid_format(temp_storage):
    """Test importing invalid JSON raises error."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        f.write("invalid json {{{")
    
    try:
        with pytest.raises(ValueError, match="Invalid JSON"):
            temp_storage.import_json(import_path)
    finally:
        import_path.unlink()


def test_create_backup(temp_storage):
    """Test creating a backup."""
    # Create some todos
    todos = [TodoItem(title="Task 1"), TodoItem(title="Task 2")]
    temp_storage.save(todos)
    
    # Create backup in temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        backup_dir = Path(tmpdir)
        backup_path = temp_storage.create_backup(backup_dir)
        
        # Verify backup was created
        assert backup_path.exists()
        assert backup_path.parent == backup_dir
        assert "todo-backup-" in backup_path.name
        
        # Verify backup content
        import json
        data = json.loads(backup_path.read_text())
        assert len(data) == 2
        assert data[0]['title'] == "Task 1"


def test_restore_backup(temp_storage):
    """Test restoring from a backup."""
    # Create initial todos
    original_todos = [TodoItem(title="Original 1"), TodoItem(title="Original 2")]
    temp_storage.save(original_todos)
    
    # Create a backup
    with tempfile.TemporaryDirectory() as tmpdir:
        backup_dir = Path(tmpdir)
        backup_path = temp_storage.create_backup(backup_dir)
        
        # Modify current todos
        temp_storage.clear()
        temp_storage.add(TodoItem(title="New task"))
        
        # Restore from backup
        temp_storage.restore_backup(backup_path)
        
        # Verify restoration
        loaded = temp_storage.load()
        assert len(loaded) == 2
        assert loaded[0].title == "Original 1"
        assert loaded[1].title == "Original 2"


def test_restore_backup_invalid_file(temp_storage):
    """Test restoring from invalid backup raises error."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        backup_path = Path(f.name)
        f.write("invalid json")
    
    try:
        with pytest.raises(ValueError, match="Invalid backup file"):
            temp_storage.restore_backup(backup_path)
    finally:
        backup_path.unlink()


def test_list_backups(temp_storage):
    """Test listing backups."""
    with tempfile.TemporaryDirectory() as tmpdir:
        backup_dir = Path(tmpdir)
        
        # Create multiple backups
        temp_storage.save([TodoItem(title="Task 1")])
        backup1 = temp_storage.create_backup(backup_dir)
        
        temp_storage.save([TodoItem(title="Task 2")])
        backup2 = temp_storage.create_backup(backup_dir)
        
        # List backups
        backups = temp_storage.list_backups(backup_dir)
        
        # Verify list
        assert len(backups) >= 2
        assert backup2 in backups
        assert backup1 in backups
        # Should be sorted newest first
        assert backups[0] == backup2


def test_list_backups_empty_directory(temp_storage):
    """Test listing backups in empty directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        backup_dir = Path(tmpdir)
        backups = temp_storage.list_backups(backup_dir)
        assert backups == []


def test_archive_completed(temp_storage):
    """Test archiving completed todos."""
    # Create mixed todos
    todo1 = TodoItem(title="Active 1")
    todo2 = TodoItem(title="Completed 1")
    todo2.toggle_completed()
    todo3 = TodoItem(title="Active 2")
    todo4 = TodoItem(title="Completed 2")
    todo4.toggle_completed()
    
    temp_storage.save([todo1, todo2, todo3, todo4])
    
    # Archive completed todos
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        archive_path = Path(f.name)
    
    try:
        count = temp_storage.archive_completed(archive_path)
        
        # Verify archive count
        assert count == 2
        
        # Verify only active todos remain
        active_todos = temp_storage.load()
        assert len(active_todos) == 2
        assert all(not t.completed for t in active_todos)
        
        # Verify archive contains completed todos
        archived = temp_storage.load_archive(archive_path)
        assert len(archived) == 2
        assert all(t.completed for t in archived)
    finally:
        archive_path.unlink()


def test_archive_completed_no_completed_todos(temp_storage):
    """Test archiving when no completed todos exist."""
    # Create only active todos
    todos = [TodoItem(title="Active 1"), TodoItem(title="Active 2")]
    temp_storage.save(todos)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        archive_path = Path(f.name)
    
    try:
        count = temp_storage.archive_completed(archive_path)
        
        # Verify nothing was archived
        assert count == 0
        
        # Verify all todos still in storage
        loaded = temp_storage.load()
        assert len(loaded) == 2
    finally:
        if archive_path.exists():
            archive_path.unlink()


def test_archive_completed_merge_with_existing(temp_storage):
    """Test archiving merges with existing archive."""
    # Create initial completed todos and archive them
    todo1 = TodoItem(title="Completed 1")
    todo1.toggle_completed()
    temp_storage.save([todo1])
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        archive_path = Path(f.name)
    
    try:
        # First archive
        temp_storage.archive_completed(archive_path)
        
        # Create more completed todos
        todo2 = TodoItem(title="Completed 2")
        todo2.toggle_completed()
        temp_storage.save([todo2])
        
        # Archive again
        count = temp_storage.archive_completed(archive_path)
        assert count == 1
        
        # Verify archive contains both
        archived = temp_storage.load_archive(archive_path)
        assert len(archived) == 2
    finally:
        archive_path.unlink()


def test_load_archive_nonexistent(temp_storage):
    """Test loading non-existent archive returns empty list."""
    archived = temp_storage.load_archive(Path("/nonexistent/archive.json"))
    assert archived == []


def test_export_import_roundtrip(temp_storage):
    """Test full export-import roundtrip preserves data."""
    # Create diverse todos
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    todo3 = TodoItem(title="Task 3")
    todo3.postpone_until_tomorrow()
    
    original_todos = [todo1, todo2, todo3]
    temp_storage.save(original_todos)
    
    # Export
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path, original_todos)
        
        # Clear storage
        temp_storage.clear()
        
        # Import
        temp_storage.import_json(export_path, merge=False)
        
        # Verify all data preserved
        imported = temp_storage.load()
        assert len(imported) == 3
        
        # Find corresponding todos by title
        imported_dict = {t.title: t for t in imported}
        
        assert not imported_dict["Task 1"].completed
        assert imported_dict["Task 2"].completed
        assert imported_dict["Task 3"].is_postponed()
    finally:
        export_path.unlink()
