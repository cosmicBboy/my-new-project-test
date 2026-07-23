"""Tests for the keybindings module."""

import pytest
import json
from pathlib import Path

from todo_tui.keybindings import KeyBinding, KeyBindingsManager


def test_keybinding_creation():
    """Test creating a KeyBinding instance."""
    binding = KeyBinding(
        action="test_action",
        key="t",
        default_key="t",
        description="Test action",
        category="Test"
    )
    
    assert binding.action == "test_action"
    assert binding.key == "t"
    assert binding.default_key == "t"
    assert binding.description == "Test action"
    assert binding.category == "Test"


def test_keybinding_to_dict():
    """Test converting KeyBinding to dictionary."""
    binding = KeyBinding(
        action="test_action",
        key="t",
        default_key="t",
        description="Test action",
        category="Test"
    )
    
    data = binding.to_dict()
    assert isinstance(data, dict)
    assert data["action"] == "test_action"
    assert data["key"] == "t"


def test_keybinding_from_dict():
    """Test creating KeyBinding from dictionary."""
    data = {
        "action": "test_action",
        "key": "t",
        "default_key": "t",
        "description": "Test action",
        "category": "Test"
    }
    
    binding = KeyBinding.from_dict(data)
    assert binding.action == "test_action"
    assert binding.key == "t"
    assert binding.description == "Test action"


@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config path."""
    return tmp_path / "test-keybindings.json"


def test_keybindings_manager_initialization(temp_config):
    """Test KeyBindingsManager initialization."""
    manager = KeyBindingsManager(temp_config)
    
    assert manager is not None
    assert manager.config_path == temp_config
    assert len(manager.bindings) > 0


def test_keybindings_manager_defaults(temp_config):
    """Test that manager starts with default bindings."""
    manager = KeyBindingsManager(temp_config)
    
    # Check that some default bindings exist
    assert manager.get_binding("toggle_todo") is not None
    assert manager.get_binding("delete_todo") is not None
    assert manager.get_binding("quit") is not None


def test_keybindings_manager_get_binding(temp_config):
    """Test getting a specific binding."""
    manager = KeyBindingsManager(temp_config)
    
    binding = manager.get_binding("toggle_todo")
    assert binding is not None
    assert binding.action == "toggle_todo"
    assert binding.key == "space"
    assert binding.default_key == "space"


def test_keybindings_manager_get_nonexistent_binding(temp_config):
    """Test getting a binding that doesn't exist."""
    manager = KeyBindingsManager(temp_config)
    
    binding = manager.get_binding("nonexistent_action")
    assert binding is None


def test_keybindings_manager_get_key(temp_config):
    """Test getting the key for an action."""
    manager = KeyBindingsManager(temp_config)
    
    key = manager.get_key("toggle_todo")
    assert key == "space"


def test_keybindings_manager_set_binding(temp_config):
    """Test setting a custom key binding."""
    manager = KeyBindingsManager(temp_config)
    
    # Set a custom key
    manager.set_binding("toggle_todo", "t")
    
    # Verify it was changed
    binding = manager.get_binding("toggle_todo")
    assert binding.key == "t"
    assert binding.default_key == "space"  # Default should remain unchanged


def test_keybindings_manager_set_multiple_bindings(temp_config):
    """Test setting multiple custom bindings."""
    manager = KeyBindingsManager(temp_config)
    
    manager.set_binding("toggle_todo", "t")
    manager.set_binding("delete_todo", "x")
    manager.set_binding("postpone_todo", "s")
    
    assert manager.get_key("toggle_todo") == "t"
    assert manager.get_key("delete_todo") == "x"
    assert manager.get_key("postpone_todo") == "s"


def test_keybindings_manager_reset_to_defaults(temp_config):
    """Test resetting all bindings to defaults."""
    manager = KeyBindingsManager(temp_config)
    
    # Modify some bindings
    manager.set_binding("toggle_todo", "t")
    manager.set_binding("delete_todo", "x")
    
    assert manager.get_key("toggle_todo") == "t"
    
    # Reset to defaults
    manager.reset_to_defaults()
    
    # Verify defaults are restored
    assert manager.get_key("toggle_todo") == "space"
    assert manager.get_key("delete_todo") == "d"


def test_keybindings_manager_save_and_load(temp_config):
    """Test saving and loading bindings from file."""
    # Create manager and set custom bindings
    manager1 = KeyBindingsManager(temp_config)
    manager1.set_binding("toggle_todo", "t")
    manager1.set_binding("delete_todo", "x")
    
    # Create a new manager instance (should load from file)
    manager2 = KeyBindingsManager(temp_config)
    
    # Verify loaded bindings match
    assert manager2.get_key("toggle_todo") == "t"
    assert manager2.get_key("delete_todo") == "x"


def test_keybindings_manager_corrupted_config(temp_config):
    """Test handling of corrupted config file."""
    # Create a corrupted config file
    with open(temp_config, "w") as f:
        f.write("{ invalid json }")
    
    # Manager should fall back to defaults
    manager = KeyBindingsManager(temp_config)
    
    assert manager.get_key("toggle_todo") == "space"
    assert len(manager.bindings) > 0


def test_keybindings_manager_get_all_bindings(temp_config):
    """Test getting all bindings."""
    manager = KeyBindingsManager(temp_config)
    
    all_bindings = manager.get_all_bindings()
    
    assert isinstance(all_bindings, dict)
    assert len(all_bindings) > 0
    assert "toggle_todo" in all_bindings
    assert "delete_todo" in all_bindings


def test_keybindings_manager_get_bindings_by_category(temp_config):
    """Test getting bindings organized by category."""
    manager = KeyBindingsManager(temp_config)
    
    categories = manager.get_bindings_by_category()
    
    assert isinstance(categories, dict)
    assert len(categories) > 0
    
    # Check that expected categories exist
    assert "Navigation" in categories or "Todo Management" in categories
    
    # Check that each category has bindings
    for category, bindings in categories.items():
        assert isinstance(bindings, list)
        assert len(bindings) > 0
        assert all(isinstance(b, KeyBinding) for b in bindings)


def test_keybindings_manager_search_bindings(temp_config):
    """Test searching for bindings."""
    manager = KeyBindingsManager(temp_config)
    
    # Search by action
    results = manager.search_bindings("toggle")
    assert len(results) > 0
    assert any("toggle" in r.action.lower() for r in results)
    
    # Search by key
    results = manager.search_bindings("space")
    assert len(results) > 0
    assert any("space" in r.key.lower() for r in results)
    
    # Search by description
    results = manager.search_bindings("completion")
    assert len(results) > 0


def test_keybindings_manager_search_case_insensitive(temp_config):
    """Test that search is case-insensitive."""
    manager = KeyBindingsManager(temp_config)
    
    results_lower = manager.search_bindings("toggle")
    results_upper = manager.search_bindings("TOGGLE")
    results_mixed = manager.search_bindings("ToGgLe")
    
    # All should return the same results
    assert len(results_lower) == len(results_upper) == len(results_mixed)


def test_keybindings_manager_search_no_results(temp_config):
    """Test search with no matching results."""
    manager = KeyBindingsManager(temp_config)
    
    results = manager.search_bindings("xyznonexistent")
    assert len(results) == 0


def test_keybindings_manager_search_multiple_matches(temp_config):
    """Test search that matches multiple bindings."""
    manager = KeyBindingsManager(temp_config)
    
    # Search for common term
    results = manager.search_bindings("todo")
    
    # Should match multiple actions related to todos
    assert len(results) >= 2


def test_keybindings_manager_search_by_category(temp_config):
    """Test searching by category name."""
    manager = KeyBindingsManager(temp_config)
    
    results = manager.search_bindings("Navigation")
    
    assert len(results) > 0
    assert all(r.category == "Navigation" for r in results)


def test_keybindings_default_bindings_structure():
    """Test that default bindings have expected structure."""
    from todo_tui.keybindings import KeyBindingsManager
    
    defaults = KeyBindingsManager.DEFAULT_BINDINGS
    
    assert isinstance(defaults, dict)
    assert len(defaults) > 0
    
    # Check that all defaults have required fields
    for action, binding in defaults.items():
        assert isinstance(binding, KeyBinding)
        assert binding.action == action
        assert binding.key == binding.default_key
        assert len(binding.description) > 0
        assert len(binding.category) > 0


def test_keybindings_default_actions_exist():
    """Test that expected default actions exist."""
    from todo_tui.keybindings import KeyBindingsManager
    
    defaults = KeyBindingsManager.DEFAULT_BINDINGS
    
    expected_actions = [
        "toggle_todo",
        "delete_todo",
        "postpone_todo",
        "show_shortcuts",
        "quit"
    ]
    
    for action in expected_actions:
        assert action in defaults, f"Expected action '{action}' not in defaults"


def test_keybindings_categories_exist():
    """Test that expected categories exist."""
    from todo_tui.keybindings import KeyBindingsManager
    
    defaults = KeyBindingsManager.DEFAULT_BINDINGS
    categories = {binding.category for binding in defaults.values()}
    
    expected_categories = [
        "Navigation",
        "Todo Management",
        "Application"
    ]
    
    for category in expected_categories:
        assert category in categories, f"Expected category '{category}' not found"


def test_keybindings_persistence_format(temp_config):
    """Test that saved config has correct JSON format."""
    manager = KeyBindingsManager(temp_config)
    manager.set_binding("toggle_todo", "t")
    
    # Read the saved file
    with open(temp_config, "r") as f:
        data = json.load(f)
    
    assert isinstance(data, dict)
    assert "toggle_todo" in data
    assert data["toggle_todo"]["key"] == "t"
    assert data["toggle_todo"]["action"] == "toggle_todo"


def test_keybindings_no_key_conflicts():
    """Test that default bindings don't have key conflicts."""
    from todo_tui.keybindings import KeyBindingsManager
    
    defaults = KeyBindingsManager.DEFAULT_BINDINGS
    
    # Build a mapping of keys to actions
    key_to_actions = {}
    for action, binding in defaults.items():
        key = binding.key
        if key not in key_to_actions:
            key_to_actions[key] = []
        key_to_actions[key].append(action)
    
    # Check for conflicts (same key used for different non-navigation actions)
    # Note: Tab is shared between focus_list and focus_input which is OK
    for key, actions in key_to_actions.items():
        if len(actions) > 1:
            # Multiple actions with same key should be related (e.g., both focus actions)
            action_names = [a for a in actions]
            # Allow focus_list and focus_input to share Tab
            if not all("focus" in a for a in action_names):
                pytest.fail(f"Key '{key}' is bound to multiple unrelated actions: {actions}")
