"""Tests for the keybindings module."""

import pytest
from pathlib import Path
import json

from todo_tui.keybindings import KeyBindings


def test_keybindings_default_initialization():
    """Test that KeyBindings initializes with default values."""
    kb = KeyBindings()
    
    # Check default bindings
    assert kb.get_key("quit") == "q"
    assert kb.get_key("toggle_todo") == "space"
    assert kb.get_key("delete_todo") == "d"
    assert kb.get_key("postpone_todo") == "p"
    assert kb.get_key("show_help") == "question_mark"


def test_keybindings_custom_storage_path(tmp_path):
    """Test using a custom storage path."""
    storage_path = tmp_path / "custom-keys.json"
    kb = KeyBindings(storage_path)
    
    assert kb.storage_path == storage_path


def test_keybindings_set_and_get_key():
    """Test setting and getting a custom key binding."""
    kb = KeyBindings()
    
    # Set a custom binding
    kb.set_key("quit", "ctrl+q")
    
    # Verify it was set
    assert kb.get_key("quit") == "ctrl+q"


def test_keybindings_save_and_load(tmp_path):
    """Test that bindings are saved and loaded correctly."""
    storage_path = tmp_path / "test-keys.json"
    
    # Create and customize bindings
    kb1 = KeyBindings(storage_path)
    kb1.set_key("quit", "ctrl+q")
    kb1.set_key("delete_todo", "x")
    
    # Verify file was created
    assert storage_path.exists()
    
    # Load in a new instance
    kb2 = KeyBindings(storage_path)
    assert kb2.get_key("quit") == "ctrl+q"
    assert kb2.get_key("delete_todo") == "x"
    
    # Check that unchanged bindings are still default
    assert kb2.get_key("toggle_todo") == "space"


def test_keybindings_reset_to_defaults(tmp_path):
    """Test resetting all bindings to defaults."""
    storage_path = tmp_path / "test-keys.json"
    
    kb = KeyBindings(storage_path)
    
    # Customize multiple bindings
    kb.set_key("quit", "ctrl+q")
    kb.set_key("delete_todo", "x")
    kb.set_key("toggle_todo", "enter")
    
    # Reset to defaults
    kb.reset_to_defaults()
    
    # Verify all are back to defaults
    assert kb.get_key("quit") == "q"
    assert kb.get_key("delete_todo") == "d"
    assert kb.get_key("toggle_todo") == "space"
    
    # Verify defaults were persisted
    kb2 = KeyBindings(storage_path)
    assert kb2.get_key("quit") == "q"


def test_keybindings_get_all_bindings():
    """Test getting all bindings at once."""
    kb = KeyBindings()
    
    all_bindings = kb.get_all_bindings()
    
    # Check it's a dictionary
    assert isinstance(all_bindings, dict)
    
    # Check it contains expected keys
    assert "quit" in all_bindings
    assert "toggle_todo" in all_bindings
    assert "delete_todo" in all_bindings
    
    # Check it's a copy (not the original)
    all_bindings["quit"] = "modified"
    assert kb.get_key("quit") != "modified"


def test_keybindings_get_description():
    """Test getting human-readable descriptions."""
    kb = KeyBindings()
    
    # Check descriptions exist
    assert kb.get_description("quit") != ""
    assert kb.get_description("toggle_todo") != ""
    assert kb.get_description("delete_todo") != ""
    
    # Check they contain expected words
    assert "quit" in kb.get_description("quit").lower()
    assert "toggle" in kb.get_description("toggle_todo").lower()
    assert "delete" in kb.get_description("delete_todo").lower()


def test_keybindings_format_key_for_display():
    """Test formatting keys for display."""
    kb = KeyBindings()
    
    # Test special key formatting
    assert kb.format_key_for_display("question_mark") == "?"
    assert kb.format_key_for_display("space") == "Space"
    
    # Test modifier keys
    assert "Ctrl" in kb.format_key_for_display("ctrl+e")
    assert "Shift" in kb.format_key_for_display("shift+a")
    assert "Alt" in kb.format_key_for_display("alt+x")
    
    # Test single letter capitalization
    assert kb.format_key_for_display("q") == "Q"
    assert kb.format_key_for_display("d") == "D"


def test_keybindings_corrupted_file(tmp_path):
    """Test handling of corrupted storage file."""
    storage_path = tmp_path / "corrupted-keys.json"
    
    # Create corrupted file
    storage_path.write_text("not valid json {{{")
    
    # Should load defaults without crashing
    kb = KeyBindings(storage_path)
    assert kb.get_key("quit") == "q"


def test_keybindings_partial_file(tmp_path):
    """Test loading file with only some bindings."""
    storage_path = tmp_path / "partial-keys.json"
    
    # Create file with only some bindings
    partial_data = {
        "quit": "ctrl+q",
        "delete_todo": "x"
    }
    storage_path.write_text(json.dumps(partial_data))
    
    # Should merge with defaults
    kb = KeyBindings(storage_path)
    assert kb.get_key("quit") == "ctrl+q"  # From file
    assert kb.get_key("delete_todo") == "x"  # From file
    assert kb.get_key("toggle_todo") == "space"  # From defaults


def test_keybindings_action_categories():
    """Test that action categories are defined."""
    kb = KeyBindings()
    
    # Check categories exist
    assert "Navigation" in kb.ACTION_CATEGORIES
    assert "TODO Management" in kb.ACTION_CATEGORIES
    assert "Help & Information" in kb.ACTION_CATEGORIES
    assert "Application" in kb.ACTION_CATEGORIES


def test_keybindings_all_defaults_have_descriptions():
    """Test that all default bindings have descriptions."""
    kb = KeyBindings()
    
    for action in kb.DEFAULT_BINDINGS.keys():
        description = kb.get_description(action)
        assert description != ""
        assert description != action  # Should be human-readable, not just the action name


def test_keybindings_persistence_after_multiple_changes(tmp_path):
    """Test that multiple changes are all persisted."""
    storage_path = tmp_path / "test-keys.json"
    
    kb = KeyBindings(storage_path)
    
    # Make multiple changes
    changes = {
        "quit": "ctrl+q",
        "toggle_todo": "enter",
        "delete_todo": "x",
    }
    
    for action, key in changes.items():
        kb.set_key(action, key)
    
    # Load fresh instance
    kb2 = KeyBindings(storage_path)
    
    # Verify all changes persisted
    for action, key in changes.items():
        assert kb2.get_key(action) == key


def test_keybindings_nonexistent_action():
    """Test getting key for non-existent action."""
    kb = KeyBindings()
    
    # Should return empty string for unknown action
    assert kb.get_key("nonexistent_action") == ""


def test_keybindings_format_compound_keys():
    """Test formatting of complex key combinations."""
    kb = KeyBindings()
    
    # Test various combinations
    assert kb.format_key_for_display("ctrl+shift+a")
    assert kb.format_key_for_display("alt+ctrl+delete")
    
    # Verify ctrl/shift/alt are replaced with proper case
    formatted = kb.format_key_for_display("ctrl+alt+x")
    assert "Ctrl" in formatted or "ctrl" not in formatted.lower()


def test_keybindings_save_creates_valid_json(tmp_path):
    """Test that saved file is valid JSON."""
    storage_path = tmp_path / "test-keys.json"
    
    kb = KeyBindings(storage_path)
    kb.set_key("quit", "ctrl+q")
    kb.save_bindings()
    
    # Verify file contains valid JSON
    with open(storage_path) as f:
        data = json.load(f)
    
    assert isinstance(data, dict)
    assert "quit" in data
    assert data["quit"] == "ctrl+q"
