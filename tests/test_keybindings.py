"""Tests for the key bindings manager."""

import pytest
import json
from pathlib import Path

from todo_tui.keybindings import KeyBindingsManager


@pytest.fixture
def tmp_bindings_path(tmp_path):
    """Create a temporary path for bindings file."""
    return tmp_path / "test-keybindings.json"


@pytest.fixture
def keybindings_manager(tmp_bindings_path):
    """Create a KeyBindingsManager with temporary storage."""
    return KeyBindingsManager(tmp_bindings_path)


def test_keybindings_manager_initialization(keybindings_manager):
    """Test that KeyBindingsManager initializes with defaults."""
    bindings = keybindings_manager.get_all_bindings()
    
    assert bindings is not None
    assert len(bindings) > 0
    
    # Check that all default actions exist
    assert "quit" in bindings
    assert "help" in bindings
    assert "toggle" in bindings
    assert "delete" in bindings
    assert "postpone" in bindings


def test_keybindings_manager_default_bindings():
    """Test default bindings are correct."""
    assert KeyBindingsManager.DEFAULT_BINDINGS["quit"] == "q"
    assert KeyBindingsManager.DEFAULT_BINDINGS["help"] == "question_mark"
    assert KeyBindingsManager.DEFAULT_BINDINGS["toggle"] == "space"
    assert KeyBindingsManager.DEFAULT_BINDINGS["delete"] == "d"
    assert KeyBindingsManager.DEFAULT_BINDINGS["postpone"] == "p"


def test_set_binding(keybindings_manager, tmp_bindings_path):
    """Test setting a custom binding."""
    keybindings_manager.set_binding("quit", "x")
    
    assert keybindings_manager.get_binding("quit") == "x"
    
    # Verify it was saved to file
    assert tmp_bindings_path.exists()
    data = json.loads(tmp_bindings_path.read_text())
    assert data["quit"] == "x"


def test_get_binding(keybindings_manager):
    """Test getting a binding."""
    binding = keybindings_manager.get_binding("quit")
    assert binding == "q"
    
    # Test non-existent binding
    binding = keybindings_manager.get_binding("nonexistent")
    assert binding is None


def test_get_all_bindings(keybindings_manager):
    """Test getting all bindings."""
    bindings = keybindings_manager.get_all_bindings()
    
    assert isinstance(bindings, dict)
    assert len(bindings) == len(KeyBindingsManager.DEFAULT_BINDINGS)
    
    # Verify it's a copy, not the original
    bindings["quit"] = "modified"
    assert keybindings_manager.get_binding("quit") == "q"


def test_save_bindings(keybindings_manager, tmp_bindings_path):
    """Test saving bindings to file."""
    keybindings_manager.bindings["quit"] = "x"
    keybindings_manager.bindings["toggle"] = "t"
    
    keybindings_manager.save_bindings()
    
    assert tmp_bindings_path.exists()
    data = json.loads(tmp_bindings_path.read_text())
    assert data["quit"] == "x"
    assert data["toggle"] == "t"


def test_load_bindings_from_file(tmp_bindings_path):
    """Test loading bindings from existing file."""
    # Create a file with custom bindings
    custom_bindings = {
        "quit": "x",
        "toggle": "t",
    }
    tmp_bindings_path.write_text(json.dumps(custom_bindings))
    
    # Load the manager
    manager = KeyBindingsManager(tmp_bindings_path)
    
    # Should have custom bindings merged with defaults
    assert manager.get_binding("quit") == "x"
    assert manager.get_binding("toggle") == "t"
    assert manager.get_binding("delete") == "d"  # Default preserved


def test_load_bindings_corrupted_file(tmp_bindings_path):
    """Test loading bindings when file is corrupted."""
    # Create a corrupted file
    tmp_bindings_path.write_text("not valid json {{{")
    
    # Should fall back to defaults without error
    manager = KeyBindingsManager(tmp_bindings_path)
    bindings = manager.get_all_bindings()
    
    assert bindings == KeyBindingsManager.DEFAULT_BINDINGS


def test_reset_to_defaults(keybindings_manager, tmp_bindings_path):
    """Test resetting bindings to defaults."""
    # Set some custom bindings
    keybindings_manager.set_binding("quit", "x")
    keybindings_manager.set_binding("toggle", "t")
    
    assert keybindings_manager.get_binding("quit") == "x"
    
    # Reset to defaults
    keybindings_manager.reset_to_defaults()
    
    assert keybindings_manager.get_binding("quit") == "q"
    assert keybindings_manager.get_binding("toggle") == "space"
    
    # Verify file was updated
    data = json.loads(tmp_bindings_path.read_text())
    assert data == KeyBindingsManager.DEFAULT_BINDINGS


def test_persistence_across_instances(tmp_bindings_path):
    """Test that bindings persist across manager instances."""
    # Create first manager and set custom bindings
    manager1 = KeyBindingsManager(tmp_bindings_path)
    manager1.set_binding("quit", "x")
    manager1.set_binding("toggle", "t")
    
    # Create second manager
    manager2 = KeyBindingsManager(tmp_bindings_path)
    
    # Should have the custom bindings
    assert manager2.get_binding("quit") == "x"
    assert manager2.get_binding("toggle") == "t"


def test_save_bindings_failure(keybindings_manager, monkeypatch):
    """Test handling of save failures."""
    def mock_write_text(*args, **kwargs):
        raise PermissionError("Cannot write to file")
    
    monkeypatch.setattr(Path, "write_text", mock_write_text)
    
    with pytest.raises(ValueError, match="Failed to save key bindings"):
        keybindings_manager.save_bindings()


def test_multiple_bindings_changes(keybindings_manager):
    """Test making multiple binding changes."""
    changes = {
        "quit": "x",
        "toggle": "t",
        "delete": "r",
        "postpone": "s",
    }
    
    for action, key in changes.items():
        keybindings_manager.set_binding(action, key)
    
    # Verify all changes
    for action, expected_key in changes.items():
        assert keybindings_manager.get_binding(action) == expected_key


def test_keybindings_with_modifiers(keybindings_manager):
    """Test setting bindings with modifier keys."""
    keybindings_manager.set_binding("quit", "ctrl+q")
    keybindings_manager.set_binding("toggle", "shift+space")
    
    assert keybindings_manager.get_binding("quit") == "ctrl+q"
    assert keybindings_manager.get_binding("toggle") == "shift+space"


def test_keybindings_empty_file(tmp_bindings_path):
    """Test loading from an empty bindings file."""
    # Create empty file
    tmp_bindings_path.write_text("{}")
    
    manager = KeyBindingsManager(tmp_bindings_path)
    
    # Should fall back to defaults
    assert manager.get_all_bindings() == KeyBindingsManager.DEFAULT_BINDINGS


def test_keybindings_partial_file(tmp_bindings_path):
    """Test loading from a file with only some bindings."""
    # Create file with partial bindings
    partial = {"quit": "x"}
    tmp_bindings_path.write_text(json.dumps(partial))
    
    manager = KeyBindingsManager(tmp_bindings_path)
    
    # Should have custom quit and default others
    assert manager.get_binding("quit") == "x"
    assert manager.get_binding("toggle") == "space"
    assert manager.get_binding("delete") == "d"
