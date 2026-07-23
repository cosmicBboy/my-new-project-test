"""Tests for the storage layer."""

import pytest
import tempfile
import json
import csv
from pathlib import Path
from uuid import uuid4
from datetime import datetime, date, timedelta

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    storage = TodoStorage(storage_path)
    yield storage
    
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
    
    storage = TodoStorage(storage_path)
    
    with pytest.raises(ValueError, match="Corrupted storage file"):
        storage.load()
    
    # Cleanup
    storage_path.unlink()


def test_export_json(temp_storage):
    """Test exporting todos to JSON format."""
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    
    todos = [todo1, todo2]
    temp_storage.save(todos)
    
    # Export to JSON
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
        assert data[1]['completed'] is True
    finally:
        export_path.unlink()


def test_export_json_with_custom_todos(temp_storage):
    """Test exporting a custom list of todos to JSON."""
    # Add some todos to storage
    temp_storage.add(TodoItem(title="Stored task"))
    
    # Export a different set of todos
    custom_todos = [TodoItem(title="Custom task 1"), TodoItem(title="Custom task 2")]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path, todos=custom_todos)
        
        # Verify only custom todos were exported
        data = json.loads(export_path.read_text())
        assert len(data) == 2
        assert data[0]['title'] == "Custom task 1"
        assert data[1]['title'] == "Custom task 2"
    finally:
        export_path.unlink()


def test_export_csv(temp_storage):
    """Test exporting todos to CSV format."""
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    
    todos = [todo1, todo2]
    temp_storage.save(todos)
    
    # Export to CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_csv(export_path)
        
        # Verify export
        assert export_path.exists()
        with export_path.open('r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Check header
        assert rows[0] == ['id', 'title', 'completed', 'created_at', 'completed_at', 'postpone_until']
        
        # Check data
        assert len(rows) == 3  # header + 2 todos
        assert rows[1][1] == "Task 1"
        assert rows[1][2] == "False"
        assert rows[2][1] == "Task 2"
        assert rows[2][2] == "True"
    finally:
        export_path.unlink()


def test_export_markdown(temp_storage):
    """Test exporting todos to Markdown format."""
    now = datetime.now()
    
    todos = [
        TodoItem(title="Active task 1", created_at=now),
        TodoItem(title="Active task 2", created_at=now),
        TodoItem(title="Completed task", created_at=now),
    ]
    # Mark the completed task as completed
    todos[2].toggle_completed()
    
    # Add a postponed task
    postponed = TodoItem(title="Postponed task", created_at=now)
    postponed.postpone_until_tomorrow()
    todos.append(postponed)
    
    temp_storage.save(todos)
    
    # Export to Markdown
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_markdown(export_path)
        
        # Verify export
        assert export_path.exists()
        content = export_path.read_text()
        
        # Check headers
        assert "# TODO List" in content
        assert "## Active Tasks" in content
        assert "## Completed Tasks" in content
        
        # Check active tasks
        assert "- [ ] Active task 1" in content
        assert "- [ ] Active task 2" in content
        assert "- [ ] Postponed task" in content
        assert "postponed until" in content
        
        # Check completed tasks
        assert "- [x] Completed task" in content
    finally:
        export_path.unlink()


def test_import_json_replace(temp_storage):
    """Test importing todos from JSON (replace mode)."""
    # Add existing todos
    temp_storage.add(TodoItem(title="Existing task"))
    
    # Create import file
    import_todos = [
        TodoItem(title="Imported task 1"),
        TodoItem(title="Imported task 2"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        # Import (replace mode)
        imported = temp_storage.import_json(export_path, merge=False)
        
        # Verify import replaced existing todos
        assert len(imported) == 2
        all_todos = temp_storage.load()
        assert len(all_todos) == 2
        assert all_todos[0].title == "Imported task 1"
        assert all_todos[1].title == "Imported task 2"
    finally:
        export_path.unlink()


def test_import_json_merge(temp_storage):
    """Test importing todos from JSON (merge mode)."""
    # Add existing todos
    existing = TodoItem(title="Existing task")
    temp_storage.add(existing)
    
    # Create import file with new todos
    import_todos = [
        TodoItem(title="Imported task 1"),
        TodoItem(title="Imported task 2"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        # Import (merge mode)
        imported = temp_storage.import_json(export_path, merge=True)
        
        # Verify import merged with existing todos
        assert len(imported) == 2  # Only new todos returned
        all_todos = temp_storage.load()
        assert len(all_todos) == 3  # 1 existing + 2 imported
        titles = {todo.title for todo in all_todos}
        assert titles == {"Existing task", "Imported task 1", "Imported task 2"}
    finally:
        export_path.unlink()


def test_import_json_merge_skip_duplicates(temp_storage):
    """Test importing todos with duplicate IDs in merge mode."""
    # Add existing todo
    existing = TodoItem(title="Existing task")
    temp_storage.add(existing)
    
    # Create import file with same ID and a new one
    import_todos = [
        existing,  # Duplicate ID
        TodoItem(title="New task"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        # Import (merge mode)
        imported = temp_storage.import_json(export_path, merge=True)
        
        # Verify only new todo was added
        assert len(imported) == 1
        assert imported[0].title == "New task"
        
        all_todos = temp_storage.load()
        assert len(all_todos) == 2
    finally:
        export_path.unlink()


def test_import_json_file_not_found(temp_storage):
    """Test importing from non-existent file raises error."""
    with pytest.raises(FileNotFoundError):
        temp_storage.import_json(Path("/nonexistent/path.json"))


def test_import_json_invalid_json(temp_storage):
    """Test importing invalid JSON raises error."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
        f.write("invalid json {{{")
    
    try:
        with pytest.raises(ValueError, match="Invalid JSON file"):
            temp_storage.import_json(export_path)
    finally:
        export_path.unlink()


def test_import_json_invalid_format(temp_storage):
    """Test importing JSON with invalid format raises error."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
        # Valid JSON but missing required fields
        f.write('[{"title": "Task", "missing_id": true}]')
    
    try:
        with pytest.raises(ValueError, match="Invalid data format"):
            temp_storage.import_json(export_path)
    finally:
        export_path.unlink()


def test_export_import_roundtrip(temp_storage):
    """Test that export and import preserve all data."""
    # Create todos with various states
    todos = [
        TodoItem(title="Simple task"),
        TodoItem(title="Completed task"),
    ]
    # Mark the second task as completed (this sets completed_at)
    todos[1].toggle_completed()
    
    postponed = TodoItem(title="Postponed task")
    postponed.postpone_until_tomorrow()
    todos.append(postponed)
    
    temp_storage.save(todos)
    
    # Export to JSON
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path)
        
        # Create new storage and import
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            import_storage_path = Path(f.name)
        
        try:
            import_storage = TodoStorage(import_storage_path)
            import_storage.import_json(export_path, merge=False)
            
            # Verify all data preserved
            imported_todos = import_storage.load()
            assert len(imported_todos) == 3
            
            # Check simple task
            assert imported_todos[0].title == "Simple task"
            assert imported_todos[0].completed is False
            
            # Check completed task
            assert imported_todos[1].title == "Completed task"
            assert imported_todos[1].completed is True
            assert imported_todos[1].completed_at is not None
            
            # Check postponed task
            assert imported_todos[2].title == "Postponed task"
            assert imported_todos[2].is_postponed()
            assert imported_todos[2].postpone_until is not None
        finally:
            if import_storage_path.exists():
                import_storage_path.unlink()
    finally:
        export_path.unlink()
