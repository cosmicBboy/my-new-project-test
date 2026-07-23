"""Tests for the configuration module."""

import json
import pytest
import tempfile
from pathlib import Path

from todo_tui.config import KeyBindingConfig, AppConfig


@pytest.fixture
def temp_key_config():
    """Create a KeyBindingConfig with a temporary file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    yield KeyBindingConfig(config_path)
    if config_path.exists():
        config_path.unlink()


@pytest.fixture
def temp_app_config():
    """Create an AppConfig with a temporary file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    yield AppConfig(config_path)
    if config_path.exists():
        config_path.unlink()


class TestKeyBindingConfig:
    """Tests for KeyBindingConfig class."""
    
    def test_init_with_defaults(self, temp_key_config):
        """Test initialization loads default bindings."""
        assert temp_key_config.get_binding("quit") == "q"
        assert temp_key_config.get_binding("toggle_todo") == "space"
        assert temp_key_config.get_binding("delete_todo") == "d"
    
    def test_get_binding(self, temp_key_config):
        """Test getting a binding."""
        assert temp_key_config.get_binding("quit") == "q"
        assert temp_key_config.get_binding("nonexistent") == ""
    
    def test_set_binding(self, temp_key_config):
        """Test setting a binding."""
        temp_key_config.set_binding("quit", "ctrl+q")
        assert temp_key_config.get_binding("quit") == "ctrl+q"
    
    def test_set_binding_invalid_action(self, temp_key_config):
        """Test setting binding for non-existent action does nothing."""
        temp_key_config.set_binding("invalid_action", "x")
        assert temp_key_config.get_binding("invalid_action") == ""
    
    def test_save_and_load_bindings(self, temp_key_config):
        """Test saving and loading bindings."""
        # Modify a binding
        temp_key_config.set_binding("quit", "ctrl+q")
        temp_key_config.save_bindings()
        
        # Create new config with same path
        new_config = KeyBindingConfig(temp_key_config.config_path)
        assert new_config.get_binding("quit") == "ctrl+q"
    
    def test_reset_to_defaults(self, temp_key_config):
        """Test resetting bindings to defaults."""
        temp_key_config.set_binding("quit", "ctrl+q")
        temp_key_config.reset_to_defaults()
        assert temp_key_config.get_binding("quit") == "q"
    
    def test_get_all_bindings(self, temp_key_config):
        """Test getting all bindings."""
        all_bindings = temp_key_config.get_all_bindings()
        assert isinstance(all_bindings, dict)
        assert "quit" in all_bindings
        assert "toggle_todo" in all_bindings
        assert all_bindings["quit"] == "q"
    
    def test_corrupted_file_loads_defaults(self, temp_key_config):
        """Test that corrupted config file loads defaults."""
        # Write invalid JSON
        with open(temp_key_config.config_path, 'w') as f:
            f.write("invalid json {{{")
        
        # Create new config - should load defaults
        new_config = KeyBindingConfig(temp_key_config.config_path)
        assert new_config.get_binding("quit") == "q"
    
    def test_save_bindings_creates_file(self):
        """Test that save_bindings creates file if it doesn't exist."""
        with tempfile.NamedTemporaryFile(delete=True) as f:
            config_path = Path(f.name)
        
        # File should not exist now
        assert not config_path.exists()
        
        config = KeyBindingConfig(config_path)
        config.save_bindings()
        
        # File should now exist
        assert config_path.exists()
        
        # Cleanup
        config_path.unlink()


class TestAppConfig:
    """Tests for AppConfig class."""
    
    def test_init_with_defaults(self, temp_app_config):
        """Test initialization with default values."""
        assert temp_app_config.get("first_run") is True
        assert temp_app_config.get("tutorial_completed") is False
    
    def test_get_with_default(self, temp_app_config):
        """Test getting value with default."""
        assert temp_app_config.get("nonexistent", "default") == "default"
    
    def test_set_value(self, temp_app_config):
        """Test setting a value."""
        temp_app_config.set("test_key", "test_value")
        assert temp_app_config.get("test_key") == "test_value"
    
    def test_save_and_load_config(self, temp_app_config):
        """Test saving and loading configuration."""
        temp_app_config.set("test_key", "test_value")
        temp_app_config.save_config()
        
        # Create new config with same path
        new_config = AppConfig(temp_app_config.config_path)
        assert new_config.get("test_key") == "test_value"
    
    def test_is_first_run(self, temp_app_config):
        """Test is_first_run method."""
        assert temp_app_config.is_first_run() is True
        
        temp_app_config.set("first_run", False)
        assert temp_app_config.is_first_run() is False
    
    def test_mark_tutorial_completed(self, temp_app_config):
        """Test marking tutorial as completed."""
        temp_app_config.mark_tutorial_completed()
        
        assert temp_app_config.get("first_run") is False
        assert temp_app_config.get("tutorial_completed") is True
        
        # Should be saved to file
        new_config = AppConfig(temp_app_config.config_path)
        assert new_config.get("first_run") is False
        assert new_config.get("tutorial_completed") is True
    
    def test_corrupted_file_loads_defaults(self, temp_app_config):
        """Test that corrupted config file loads defaults."""
        # Write invalid JSON
        with open(temp_app_config.config_path, 'w') as f:
            f.write("invalid json {{{")
        
        # Create new config - should load defaults
        new_config = AppConfig(temp_app_config.config_path)
        assert new_config.get("first_run") is True
