"""Tests for the storage layer."""

import pytest
import tempfile
import json
from pathlib import Path
from uuid import uuid4

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    # Create a temporary backup directory
    backup_dir = Path(tempfile.mkdtemp())
    
    storage = TodoStorage(storage_path, enable_auto_backup=True, backup_dir=backup_dir)
    yield storage
    
    # Cleanup
    if storage_path.exists():
        storage_path.unlink()
    
    # Cleanup backup directory
    if backup_dir.exists():
        for file in backup_dir.glob("*"):
            file.unlink()
        backup_dir.rmdir()


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
    
    backup_dir = Path(tempfile.mkdtemp())
    storage = TodoStorage(storage_path, backup_dir=backup_dir)
    
    with pytest.raises(ValueError, match="Corrupted storage file"):
        storage.load()
    
    # Cleanup
    storage_path.unlink()
    if backup_dir.exists():
        backup_dir.rmdir()


def test_automatic_backup_on_save(temp_storage):
    """Test that automatic backups are created on save."""
    todos = [TodoItem(title="Task 1")]
    temp_storage.save(todos)
    
    # Check that a backup was created
    backups = list(temp_storage.backup_dir.glob("todo-backup-*.json"))
    assert len(backups) >= 1


def test_backup_cleanup(temp_storage):
    """Test that old backups are cleaned up."""
    # Create 15 backups
    for i in range(15):
        todos = [TodoItem(title=f"Task {i}")]
        temp_storage.save(todos)
    
    # Should keep only 10 most recent
    backups = list(temp_storage.backup_dir.glob("todo-backup-*.json"))
    assert len(backups) == 10


def test_export_json(temp_storage):
    """Test exporting todos to JSON format."""
    todos = [
        TodoItem(title="Task 1"),
        TodoItem(title="Task 2"),
    ]
    temp_storage.save(todos)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path)
        
        # Verify export
        assert export_path.exists()
        data = json.loads(export_path.read_text())
        assert len(data) == 2
        assert data[0]['title'] == "Task 1"
        assert data[1]['title'] == "Task 2"
    finally:
        if export_path.exists():
            export_path.unlink()


def test_export_csv(temp_storage):
    """Test exporting todos to CSV format."""
    todos = [
        TodoItem(title="Task 1"),
        TodoItem(title="Task 2"),
    ]
    todos[0].toggle_completed()
    temp_storage.save(todos)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_csv(export_path)
        
        # Verify export
        assert export_path.exists()
        content = export_path.read_text()
        assert 'Task 1' in content
        assert 'Task 2' in content
        assert 'ID,Title,Completed,Created At,Completed At,Postponed Until' in content
    finally:
        if export_path.exists():
            export_path.unlink()


def test_export_markdown(temp_storage):
    """Test exporting todos to Markdown format."""
    todos = [
        TodoItem(title="Active Task"),
        TodoItem(title="Completed Task"),
    ]
    todos[1].toggle_completed()
    temp_storage.save(todos)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_markdown(export_path)
        
        # Verify export
        assert export_path.exists()
        content = export_path.read_text()
        assert '# TODO List' in content
        assert '## Active Tasks' in content
        assert '## Completed Tasks' in content
        assert '- [ ] Active Task' in content
        assert '- [x] Completed Task' in content
    finally:
        if export_path.exists():
            export_path.unlink()


def test_export_html(temp_storage):
    """Test exporting todos to HTML format."""
    todos = [
        TodoItem(title="Task 1"),
        TodoItem(title="Task 2"),
    ]
    temp_storage.save(todos)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_html(export_path)
        
        # Verify export
        assert export_path.exists()
        content = export_path.read_text()
        assert '<!DOCTYPE html>' in content
        assert '<h1>📝 TODO List</h1>' in content
        assert 'Task 1' in content
        assert 'Task 2' in content
    finally:
        if export_path.exists():
            export_path.unlink()


def test_export_with_format_detection(temp_storage):
    """Test export with automatic format detection."""
    todos = [TodoItem(title="Task 1")]
    temp_storage.save(todos)
    
    formats = [
        ('test.json', 'json'),
        ('test.csv', 'csv'),
        ('test.md', 'markdown'),
        ('test.html', 'html'),
    ]
    
    for filename, format in formats:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=Path(filename).suffix) as f:
            export_path = Path(f.name)
        
        try:
            temp_storage.export(export_path, format)
            assert export_path.exists()
        finally:
            if export_path.exists():
                export_path.unlink()


def test_export_unsupported_format(temp_storage):
    """Test that unsupported formats raise an error."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        export_path = Path(f.name)
    
    try:
        with pytest.raises(ValueError, match="Unsupported export format"):
            temp_storage.export(export_path, "txt")
    finally:
        if export_path.exists():
            export_path.unlink()


def test_import_json_replace_mode(temp_storage):
    """Test importing todos in replace mode."""
    # Create initial todos
    initial_todos = [TodoItem(title="Original Task")]
    temp_storage.save(initial_todos)
    
    # Create import file
    import_todos = [
        TodoItem(title="Imported Task 1"),
        TodoItem(title="Imported Task 2"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data))
    
    try:
        # Import in replace mode
        count = temp_storage.import_json(import_path, mode="replace")
        
        assert count == 2
        loaded = temp_storage.load()
        assert len(loaded) == 2
        assert loaded[0].title == "Imported Task 1"
        assert loaded[1].title == "Imported Task 2"
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_merge_mode(temp_storage):
    """Test importing todos in merge mode."""
    # Create initial todos
    initial_todos = [TodoItem(title="Original Task")]
    temp_storage.save(initial_todos)
    
    # Create import file
    import_todos = [
        TodoItem(title="Imported Task 1"),
        TodoItem(title="Imported Task 2"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data))
    
    try:
        # Import in merge mode
        count = temp_storage.import_json(import_path, mode="merge")
        
        assert count == 2
        loaded = temp_storage.load()
        assert len(loaded) == 3
        titles = [t.title for t in loaded]
        assert "Original Task" in titles
        assert "Imported Task 1" in titles
        assert "Imported Task 2" in titles
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_merge_mode_skips_duplicates(temp_storage):
    """Test that merge mode skips duplicate IDs."""
    # Create a todo
    todo = TodoItem(title="Original Task")
    temp_storage.save([todo])
    
    # Try to import the same todo
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        data = [todo.to_dict()]
        f.write(json.dumps(data))
    
    try:
        # Import in merge mode
        count = temp_storage.import_json(import_path, mode="merge")
        
        # Should not import duplicate
        assert count == 0
        loaded = temp_storage.load()
        assert len(loaded) == 1
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_missing_file(temp_storage):
    """Test importing from non-existent file."""
    with pytest.raises(FileNotFoundError):
        temp_storage.import_json(Path("/nonexistent/file.json"))


def test_import_json_invalid_json(temp_storage):
    """Test importing invalid JSON."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        f.write("invalid json {{{")
    
    try:
        with pytest.raises(ValueError, match="Invalid JSON"):
            temp_storage.import_json(import_path)
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_invalid_data_format(temp_storage):
    """Test importing JSON with invalid data format."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        # Missing required fields
        f.write('[{"title": "Task"}]')
    
    try:
        with pytest.raises(ValueError, match="Invalid data format"):
            temp_storage.import_json(import_path)
    finally:
        if import_path.exists():
            import_path.unlink()


def test_archive_completed(temp_storage):
    """Test archiving completed todos."""
    todos = [
        TodoItem(title="Active Task 1"),
        TodoItem(title="Completed Task 1"),
        TodoItem(title="Active Task 2"),
        TodoItem(title="Completed Task 2"),
    ]
    todos[1].toggle_completed()
    todos[3].toggle_completed()
    temp_storage.save(todos)
    
    # Archive completed
    count, archive_path = temp_storage.archive_completed()
    
    assert count == 2
    assert archive_path is not None
    assert archive_path.exists()
    
    # Verify active todos remain
    remaining = temp_storage.load()
    assert len(remaining) == 2
    assert all(not t.completed for t in remaining)
    
    # Verify archive file contains completed todos
    archive_data = json.loads(archive_path.read_text())
    assert len(archive_data) == 2
    assert all(item['completed'] for item in archive_data)
    
    # Cleanup
    if archive_path.exists():
        archive_path.unlink()


def test_archive_completed_no_completed_todos(temp_storage):
    """Test archiving when there are no completed todos."""
    todos = [TodoItem(title="Active Task")]
    temp_storage.save(todos)
    
    count, archive_path = temp_storage.archive_completed()
    
    assert count == 0
    assert archive_path is None
    
    # Verify all todos remain
    remaining = temp_storage.load()
    assert len(remaining) == 1


def test_roundtrip_export_import(temp_storage):
    """Test full export and import roundtrip."""
    # Create todos with various states
    todos = [
        TodoItem(title="Active Task"),
        TodoItem(title="Completed Task"),
        TodoItem(title="Postponed Task"),
    ]
    todos[1].toggle_completed()
    todos[2].postpone_until_tomorrow()
    temp_storage.save(todos)
    
    # Export
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path)
        
        # Clear storage
        temp_storage.clear()
        assert len(temp_storage.load()) == 0
        
        # Import
        count = temp_storage.import_json(export_path, mode="replace")
        
        # Verify
        assert count == 3
        loaded = temp_storage.load()
        assert len(loaded) == 3
        
        # Check that all data is preserved
        titles = {t.title for t in loaded}
        assert "Active Task" in titles
        assert "Completed Task" in titles
        assert "Postponed Task" in titles
        
        # Check states
        completed = [t for t in loaded if t.completed]
        assert len(completed) == 1
        assert completed[0].title == "Completed Task"
        
        postponed = [t for t in loaded if t.is_postponed()]
        assert len(postponed) == 1
        assert postponed[0].title == "Postponed Task"
    finally:
        if export_path.exists():
            export_path.unlink()


def test_disable_auto_backup():
    """Test that backups can be disabled."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    backup_dir = Path(tempfile.mkdtemp())
    
    try:
        storage = TodoStorage(storage_path, enable_auto_backup=False, backup_dir=backup_dir)
        todos = [TodoItem(title="Task 1")]
        storage.save(todos)
        
        # No backups should be created
        backups = list(backup_dir.glob("todo-backup-*.json"))
        assert len(backups) == 0
    finally:
        if storage_path.exists():
            storage_path.unlink()
        if backup_dir.exists():
            for file in backup_dir.glob("*"):
                file.unlink()
            backup_dir.rmdir()
