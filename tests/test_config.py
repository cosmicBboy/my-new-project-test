"""Tests for configuration management."""

import pytest
import tempfile
from pathlib import Path

from todo_tui.config import Config


def test_config_initialization():
    """Test Config initialization with default values."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        assert config.config_path == config_path
        assert config.keybindings is not None
        assert isinstance(config.keybindings, dict)
        assert config.tutorial_completed is False
    finally:
        if config_path.exists():
            config_path.unlink()


def test_config_default_keybindings():
    """Test that default keybindings are loaded."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        assert config.get_key("quit") == "q"
        assert config.get_key("toggle") == "space"
        assert config.get_key("delete") == "d"
        assert config.get_key("postpone") == "p"
        assert config.get_key("help") == "question_mark"
    finally:
        if config_path.exists():
            config_path.unlink()


def test_config_set_key():
    """Test setting a custom key binding."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        config.set_key("quit", "ctrl+q")
        assert config.get_key("quit") == "ctrl+q"
        
        # Verify persistence
        config2 = Config(config_path)
        assert config2.get_key("quit") == "ctrl+q"
    finally:
        if config_path.exists():
            config_path.unlink()


def test_config_reset_keybindings():
    """Test resetting keybindings to defaults."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        # Modify a key
        config.set_key("quit", "ctrl+q")
        assert config.get_key("quit") == "ctrl+q"
        
        # Reset
        config.reset_keybindings()
        assert config.get_key("quit") == "q"
    finally:
        if config_path.exists():
            config_path.unlink()


def test_config_tutorial_completed():
    """Test marking tutorial as completed."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        assert config.tutorial_completed is False
        
        config.mark_tutorial_completed()
        assert config.tutorial_completed is True
        
        # Verify persistence
        config2 = Config(config_path)
        assert config2.tutorial_completed is True
    finally:
        if config_path.exists():
            config_path.unlink()


def test_config_reset_tutorial():
    """Test resetting tutorial status."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        config.mark_tutorial_completed()
        assert config.tutorial_completed is True
        
        config.reset_tutorial()
        assert config.tutorial_completed is False
    finally:
        if config_path.exists():
            config_path.unlink()


def test_config_persistence():
    """Test that configuration persists across instances."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        # First instance
        config1 = Config(config_path)
        config1.set_key("quit", "escape")
        config1.set_key("toggle", "enter")
        config1.mark_tutorial_completed()
        
        # Second instance
        config2 = Config(config_path)
        assert config2.get_key("quit") == "escape"
        assert config2.get_key("toggle") == "enter"
        assert config2.tutorial_completed is True
    finally:
        if config_path.exists():
            config_path.unlink()


def test_config_get_nonexistent_key():
    """Test getting a key that doesn't exist."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        result = config.get_key("nonexistent")
        assert result == ""  # Should return empty string for unknown keys
    finally:
        if config_path.exists():
            config_path.unlink()
