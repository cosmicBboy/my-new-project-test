"""Tests for the storage layer."""

import pytest
import tempfile
import json
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
    """Test exporting todos to JSON file."""
    # Create some test todos
    todos = [
        TodoItem(title="Task 1"),
        TodoItem(title="Task 2", completed=True),
        TodoItem(title="Task 3"),
    ]
    todos[1].toggle_completed()  # Set completed_at timestamp
    
    temp_storage.save(todos)
    
    # Export to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path)
        
        # Verify the export file
        assert export_path.exists()
        exported_data = json.loads(export_path.read_text())
        
        assert len(exported_data) == 3
        assert exported_data[0]["title"] == "Task 1"
        assert exported_data[1]["title"] == "Task 2"
        assert exported_data[1]["completed"] is True
        assert exported_data[2]["title"] == "Task 3"
    finally:
        if export_path.exists():
            export_path.unlink()


def test_export_markdown(temp_storage):
    """Test exporting todos to Markdown file."""
    # Create test todos with different states
    todo1 = TodoItem(title="Active task")
    todo2 = TodoItem(title="Completed task")
    todo2.toggle_completed()
    todo3 = TodoItem(title="Postponed task")
    todo3.postpone_until_tomorrow()
    
    temp_storage.save([todo1, todo2, todo3])
    
    # Export to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_markdown(export_path)
        
        # Verify the export file
        assert export_path.exists()
        content = export_path.read_text()
        
        # Check for main sections
        assert "# TODO List" in content
        assert "## Active Tasks" in content
        assert "## Postponed Tasks" in content
        assert "## Completed Tasks" in content
        
        # Check for task content
        assert "- [ ] Active task" in content
        assert "- [x] Completed task" in content
        assert "- [ ] Postponed task" in content
        
        # Check for metadata
        assert "Created:" in content
        assert "Completed:" in content
        assert "Postponed until:" in content
    finally:
        if export_path.exists():
            export_path.unlink()


def test_export_markdown_empty(temp_storage):
    """Test exporting empty todo list to Markdown."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_markdown(export_path)
        
        content = export_path.read_text()
        assert "# TODO List" in content
        assert "*No tasks found*" in content
    finally:
        if export_path.exists():
            export_path.unlink()


def test_import_json_new_file(temp_storage):
    """Test importing todos from a JSON file."""
    # Create import data
    import_todos = [
        TodoItem(title="Imported task 1"),
        TodoItem(title="Imported task 2"),
        TodoItem(title="Imported task 3"),
    ]
    
    # Create import file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        # Import (replace mode)
        count = temp_storage.import_json(import_path, replace=True)
        
        assert count == 3
        
        # Verify imported todos
        loaded = temp_storage.load()
        assert len(loaded) == 3
        assert loaded[0].title == "Imported task 1"
        assert loaded[1].title == "Imported task 2"
        assert loaded[2].title == "Imported task 3"
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_append(temp_storage):
    """Test appending imported todos to existing todos."""
    # Add existing todos
    existing_todos = [
        TodoItem(title="Existing task 1"),
        TodoItem(title="Existing task 2"),
    ]
    temp_storage.save(existing_todos)
    
    # Create import data with different IDs
    import_todos = [
        TodoItem(title="Imported task 1"),
        TodoItem(title="Imported task 2"),
    ]
    
    # Create import file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        # Import in append mode
        count = temp_storage.import_json(import_path, replace=False)
        
        assert count == 2
        
        # Verify all todos are present
        loaded = temp_storage.load()
        assert len(loaded) == 4
        titles = [todo.title for todo in loaded]
        assert "Existing task 1" in titles
        assert "Existing task 2" in titles
        assert "Imported task 1" in titles
        assert "Imported task 2" in titles
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_replace(temp_storage):
    """Test replacing existing todos with imported ones."""
    # Add existing todos
    existing_todos = [
        TodoItem(title="Existing task 1"),
        TodoItem(title="Existing task 2"),
    ]
    temp_storage.save(existing_todos)
    
    # Create import data
    import_todos = [
        TodoItem(title="Imported task 1"),
    ]
    
    # Create import file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        # Import in replace mode
        count = temp_storage.import_json(import_path, replace=True)
        
        assert count == 1
        
        # Verify only imported todos remain
        loaded = temp_storage.load()
        assert len(loaded) == 1
        assert loaded[0].title == "Imported task 1"
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_avoid_duplicates(temp_storage):
    """Test that importing doesn't create duplicates when IDs match."""
    # Create a todo
    todo = TodoItem(title="Test task")
    temp_storage.save([todo])
    
    # Create import file with the same todo (same ID)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        data = [todo.to_dict()]
        f.write(json.dumps(data, indent=2))
    
    try:
        # Import in append mode
        count = temp_storage.import_json(import_path, replace=False)
        
        assert count == 1  # Reports 1 imported
        
        # Verify no duplicates
        loaded = temp_storage.load()
        assert len(loaded) == 1  # Still only 1 todo
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_nonexistent_file(temp_storage):
    """Test importing from non-existent file raises error."""
    with pytest.raises(FileNotFoundError):
        temp_storage.import_json(Path("/nonexistent/path/todos.json"))


def test_import_json_invalid_json(temp_storage):
    """Test importing invalid JSON raises error."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        f.write("invalid json {{{")
    
    try:
        with pytest.raises(ValueError, match="Invalid JSON"):
            temp_storage.import_json(import_path)
    finally:
        if import_path.exists():
            import_path.unlink()


def test_import_json_invalid_format(temp_storage):
    """Test importing JSON with invalid todo format raises error."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        # Missing required fields
        f.write('[{"invalid": "format"}]')
    
    try:
        with pytest.raises(ValueError, match="Invalid todo data format"):
            temp_storage.import_json(import_path)
    finally:
        if import_path.exists():
            import_path.unlink()


def test_export_import_roundtrip(temp_storage):
    """Test that export and import preserve all todo data."""
    # Create todos with various states
    todo1 = TodoItem(title="Active task")
    todo2 = TodoItem(title="Completed task")
    todo2.toggle_completed()
    todo3 = TodoItem(title="Postponed task")
    todo3.postpone_until_tomorrow()
    
    original_todos = [todo1, todo2, todo3]
    temp_storage.save(original_todos)
    
    # Export
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        export_path = Path(f.name)
    
    try:
        temp_storage.export_json(export_path)
        
        # Create new storage and import
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            new_storage_path = Path(f.name)
        
        new_storage = TodoStorage(new_storage_path)
        new_storage.import_json(export_path, replace=True)
        
        # Verify all data is preserved
        imported_todos = new_storage.load()
        assert len(imported_todos) == 3
        
        # Check first todo
        assert imported_todos[0].title == "Active task"
        assert imported_todos[0].completed is False
        assert imported_todos[0].id == todo1.id
        
        # Check second todo (completed)
        assert imported_todos[1].title == "Completed task"
        assert imported_todos[1].completed is True
        assert imported_todos[1].completed_at is not None
        
        # Check third todo (postponed)
        assert imported_todos[2].title == "Postponed task"
        assert imported_todos[2].postpone_until is not None
        assert imported_todos[2].is_postponed()
        
        # Cleanup
        if new_storage_path.exists():
            new_storage_path.unlink()
    finally:
        if export_path.exists():
            export_path.unlink()
