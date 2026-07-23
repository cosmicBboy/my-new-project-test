"""Tests for the storage layer."""

import pytest
import tempfile
from pathlib import Path
from uuid import uuid4

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage, PreferencesStorage


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


@pytest.fixture
def temp_preferences():
    """Create a temporary preferences file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        prefs_path = Path(f.name)
    
    prefs = PreferencesStorage(prefs_path)
    yield prefs
    
    # Cleanup
    if prefs_path.exists():
        prefs_path.unlink()


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


# Preferences Storage Tests

def test_preferences_initialization(temp_preferences):
    """Test preferences storage initialization creates file."""
    assert temp_preferences.preferences_path.exists()


def test_preferences_get_set(temp_preferences):
    """Test setting and getting preferences."""
    temp_preferences.set("test_key", "test_value")
    value = temp_preferences.get("test_key")
    assert value == "test_value"


def test_preferences_get_default(temp_preferences):
    """Test getting preference with default value."""
    value = temp_preferences.get("nonexistent_key", "default_value")
    assert value == "default_value"


def test_preferences_get_theme(temp_preferences):
    """Test getting theme preference with default."""
    theme = temp_preferences.get_theme()
    assert theme == "colorful"  # Default theme


def test_preferences_set_theme(temp_preferences):
    """Test setting theme preference."""
    temp_preferences.set_theme("dark")
    theme = temp_preferences.get_theme()
    assert theme == "dark"


def test_preferences_get_layout_density(temp_preferences):
    """Test getting layout density preference with default."""
    density = temp_preferences.get_layout_density()
    assert density == "comfortable"  # Default density


def test_preferences_set_layout_density(temp_preferences):
    """Test setting layout density preference."""
    temp_preferences.set_layout_density("spacious")
    density = temp_preferences.get_layout_density()
    assert density == "spacious"


def test_preferences_get_font_size(temp_preferences):
    """Test getting font size preference with default."""
    font_size = temp_preferences.get_font_size()
    assert font_size == "medium"  # Default size


def test_preferences_set_font_size(temp_preferences):
    """Test setting font size preference."""
    temp_preferences.set_font_size("large")
    font_size = temp_preferences.get_font_size()
    assert font_size == "large"


def test_preferences_save_load(temp_preferences):
    """Test saving and loading preferences."""
    prefs = {
        "theme": "light",
        "layout_density": "compact",
        "font_size": "small",
    }
    
    temp_preferences.save(prefs)
    loaded = temp_preferences.load()
    
    assert loaded == prefs


def test_preferences_clear(temp_preferences):
    """Test clearing all preferences."""
    temp_preferences.set("key1", "value1")
    temp_preferences.set("key2", "value2")
    
    temp_preferences.clear()
    loaded = temp_preferences.load()
    
    assert loaded == {}


def test_preferences_corrupted_file():
    """Test handling of corrupted preferences file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write("invalid json {{{")
        prefs_path = Path(f.name)
    
    prefs = PreferencesStorage(prefs_path)
    
    with pytest.raises(ValueError, match="Corrupted preferences file"):
        prefs.load()
    
    # Cleanup
    prefs_path.unlink()


def test_preferences_multiple_values(temp_preferences):
    """Test setting multiple preference values."""
    temp_preferences.set("key1", "value1")
    temp_preferences.set("key2", 123)
    temp_preferences.set("key3", True)
    temp_preferences.set("key4", ["list", "value"])
    
    assert temp_preferences.get("key1") == "value1"
    assert temp_preferences.get("key2") == 123
    assert temp_preferences.get("key3") is True
    assert temp_preferences.get("key4") == ["list", "value"]


def test_preferences_overwrite(temp_preferences):
    """Test overwriting an existing preference."""
    temp_preferences.set("key", "old_value")
    temp_preferences.set("key", "new_value")
    
    assert temp_preferences.get("key") == "new_value"


def test_preferences_get_custom_themes_default(temp_preferences):
    """Test getting custom themes with default empty list."""
    themes = temp_preferences.get_custom_themes()
    assert themes == []


def test_preferences_add_custom_theme(temp_preferences):
    """Test adding a custom theme."""
    theme_data = {
        "name": "custom_theme",
        "display_name": "Custom Theme",
        "colors": {
            "background": "#111111",
            "text": "#ffffff",
        }
    }
    
    temp_preferences.add_custom_theme(theme_data)
    themes = temp_preferences.get_custom_themes()
    
    assert len(themes) == 1
    assert themes[0]["name"] == "custom_theme"
    assert themes[0]["display_name"] == "Custom Theme"


def test_preferences_add_multiple_custom_themes(temp_preferences):
    """Test adding multiple custom themes."""
    theme1 = {
        "name": "theme1",
        "display_name": "Theme 1",
        "colors": {"background": "#111111"}
    }
    theme2 = {
        "name": "theme2",
        "display_name": "Theme 2",
        "colors": {"background": "#222222"}
    }
    
    temp_preferences.add_custom_theme(theme1)
    temp_preferences.add_custom_theme(theme2)
    
    themes = temp_preferences.get_custom_themes()
    assert len(themes) == 2


def test_preferences_replace_custom_theme(temp_preferences):
    """Test that adding a theme with same name replaces the old one."""
    theme_v1 = {
        "name": "my_theme",
        "display_name": "My Theme v1",
        "colors": {"background": "#111111"}
    }
    theme_v2 = {
        "name": "my_theme",
        "display_name": "My Theme v2",
        "colors": {"background": "#222222"}
    }
    
    temp_preferences.add_custom_theme(theme_v1)
    temp_preferences.add_custom_theme(theme_v2)
    
    themes = temp_preferences.get_custom_themes()
    assert len(themes) == 1
    assert themes[0]["display_name"] == "My Theme v2"
