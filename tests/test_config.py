"""Tests for configuration management."""

import pytest
from pathlib import Path

from todo_tui.config import Config, DEFAULT_BINDINGS


@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config for testing."""
    config_path = tmp_path / "test-config.json"
    return Config(config_path)


def test_config_initialization(temp_config):
    """Test config initializes with default bindings."""
    assert temp_config.bindings == DEFAULT_BINDINGS
    assert temp_config.tutorial_shown is False


def test_config_get_binding(temp_config):
    """Test getting a key binding."""
    assert temp_config.get_binding("quit") == "q"
    assert temp_config.get_binding("toggle") == "space"
    assert temp_config.get_binding("delete") == "d"
    assert temp_config.get_binding("postpone") == "p"


def test_config_get_binding_nonexistent(temp_config):
    """Test getting a non-existent binding returns empty string."""
    assert temp_config.get_binding("nonexistent") == ""


def test_config_set_binding(temp_config):
    """Test setting a custom key binding."""
    temp_config.set_binding("quit", "ctrl+q")
    assert temp_config.get_binding("quit") == "ctrl+q"


def test_config_set_multiple_bindings(temp_config):
    """Test setting multiple custom bindings."""
    temp_config.set_binding("quit", "ctrl+q")
    temp_config.set_binding("delete", "x")
    temp_config.set_binding("toggle", "t")
    
    assert temp_config.get_binding("quit") == "ctrl+q"
    assert temp_config.get_binding("delete") == "x"
    assert temp_config.get_binding("toggle") == "t"


def test_config_reset_bindings(temp_config):
    """Test resetting bindings to defaults."""
    # Change some bindings
    temp_config.set_binding("quit", "ctrl+q")
    temp_config.set_binding("delete", "x")
    
    # Reset
    temp_config.reset_bindings()
    
    # Check that defaults are restored
    assert temp_config.get_binding("quit") == DEFAULT_BINDINGS["quit"]
    assert temp_config.get_binding("delete") == DEFAULT_BINDINGS["delete"]


def test_config_mark_tutorial_shown(temp_config):
    """Test marking tutorial as shown."""
    assert temp_config.tutorial_shown is False
    
    temp_config.mark_tutorial_shown()
    assert temp_config.tutorial_shown is True


def test_config_persistence(temp_config):
    """Test that configuration persists across instances."""
    # Set some values
    temp_config.set_binding("quit", "ctrl+q")
    temp_config.set_binding("delete", "x")
    temp_config.mark_tutorial_shown()
    
    # Create a new config instance with the same path
    new_config = Config(temp_config.config_path)
    
    # Check that values persist
    assert new_config.get_binding("quit") == "ctrl+q"
    assert new_config.get_binding("delete") == "x"
    assert new_config.tutorial_shown is True


def test_config_save_and_load(temp_config):
    """Test explicit save and load."""
    # Modify config
    temp_config.set_binding("toggle", "t")
    temp_config.mark_tutorial_shown()
    temp_config.save()
    
    # Load in new instance
    new_config = Config(temp_config.config_path)
    
    assert new_config.get_binding("toggle") == "t"
    assert new_config.tutorial_shown is True


def test_config_corrupted_file(tmp_path):
    """Test that corrupted config file falls back to defaults."""
    config_path = tmp_path / "corrupted-config.json"
    config_path.write_text("{ this is not valid json }")
    
    config = Config(config_path)
    
    # Should fall back to defaults
    assert config.bindings == DEFAULT_BINDINGS
    assert config.tutorial_shown is False


def test_config_partial_config(tmp_path):
    """Test that partial config merges with defaults."""
    config_path = tmp_path / "partial-config.json"
    config_path.write_text('{"bindings": {"quit": "ctrl+q"}, "tutorial_shown": true}')
    
    config = Config(config_path)
    
    # Custom binding should be loaded
    assert config.get_binding("quit") == "ctrl+q"
    # Other bindings should be defaults
    assert config.get_binding("toggle") == DEFAULT_BINDINGS["toggle"]
    # Tutorial flag should be loaded
    assert config.tutorial_shown is True


def test_default_bindings_complete():
    """Test that all expected default bindings exist."""
    expected_actions = [
        "quit", "toggle", "delete", "postpone",
        "help", "customize", "export_shortcuts", "tutorial"
    ]
    
    for action in expected_actions:
        assert action in DEFAULT_BINDINGS
        assert DEFAULT_BINDINGS[action]  # Not empty


def test_default_bindings_values():
    """Test specific default binding values."""
    assert DEFAULT_BINDINGS["quit"] == "q"
    assert DEFAULT_BINDINGS["toggle"] == "space"
    assert DEFAULT_BINDINGS["delete"] == "d"
    assert DEFAULT_BINDINGS["postpone"] == "p"
    assert DEFAULT_BINDINGS["help"] == "question_mark"
    assert DEFAULT_BINDINGS["customize"] == "c"
    assert DEFAULT_BINDINGS["export_shortcuts"] == "ctrl+e"
    assert DEFAULT_BINDINGS["tutorial"] == "ctrl+t"
