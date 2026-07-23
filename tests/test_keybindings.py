"""Tests for the keybindings customization screen."""

import pytest
import tempfile
from pathlib import Path

from todo_tui.keybindings import KeybindingsScreen
from todo_tui.config import Config


@pytest.mark.asyncio
async def test_keybindings_screen_displays():
    """Test that keybindings screen displays correctly."""
    from todo_tui.app import TodoApp
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        app = TodoApp()
        config = Config(config_path)
        
        async with app.run_test() as pilot:
            keybindings = KeybindingsScreen(config)
            app.push_screen(keybindings)
            await pilot.pause(0.1)
            
            # Check that keybindings screen is present
            assert isinstance(app.screen_stack[-1], KeybindingsScreen)
    finally:
        if config_path.exists():
            config_path.unlink()


@pytest.mark.asyncio
async def test_keybindings_has_input_fields():
    """Test that keybindings screen has input fields for actions."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        keybindings = KeybindingsScreen(config)
        
        # Check that inputs are created for each action
        assert len(keybindings.inputs) > 0
        assert "quit" in keybindings.inputs
        assert "toggle" in keybindings.inputs
        assert "delete" in keybindings.inputs
    finally:
        if config_path.exists():
            config_path.unlink()


@pytest.mark.asyncio
async def test_keybindings_save_changes():
    """Test saving modified keybindings."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        from todo_tui.app import TodoApp
        
        app = TodoApp()
        config = Config(config_path)
        
        async with app.run_test() as pilot:
            keybindings = KeybindingsScreen(config)
            app.push_screen(keybindings)
            await pilot.pause(0.1)
            
            # Modify a keybinding through the input
            quit_input = keybindings.inputs["quit"]
            quit_input.value = "ctrl+q"
            
            # Click save button
            await pilot.click("#save-button")
            await pilot.pause(0.1)
            
            # Verify the change was saved
            assert config.get_key("quit") == "ctrl+q"
    finally:
        if config_path.exists():
            config_path.unlink()


@pytest.mark.asyncio
async def test_keybindings_cancel():
    """Test canceling keybindings changes."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        from todo_tui.app import TodoApp
        
        app = TodoApp()
        config = Config(config_path)
        original_quit_key = config.get_key("quit")
        
        async with app.run_test() as pilot:
            keybindings = KeybindingsScreen(config)
            app.push_screen(keybindings)
            await pilot.pause(0.1)
            
            # Modify a keybinding
            quit_input = keybindings.inputs["quit"]
            quit_input.value = "ctrl+q"
            
            # Click cancel button
            await pilot.click("#cancel-button")
            await pilot.pause(0.1)
            
            # Verify the change was NOT saved
            assert config.get_key("quit") == original_quit_key
    finally:
        if config_path.exists():
            config_path.unlink()


@pytest.mark.asyncio
async def test_keybindings_reset_to_defaults():
    """Test resetting keybindings to defaults."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        from todo_tui.app import TodoApp
        
        app = TodoApp()
        config = Config(config_path)
        
        # Modify a keybinding first
        config.set_key("quit", "ctrl+q")
        
        async with app.run_test() as pilot:
            keybindings = KeybindingsScreen(config)
            app.push_screen(keybindings)
            await pilot.pause(0.1)
            
            # Click reset button
            await pilot.click("#reset-button")
            await pilot.pause(0.1)
            
            # Verify defaults were restored
            assert config.get_key("quit") == "q"
            
            # Verify input field was updated
            assert keybindings.inputs["quit"].value == "q"
    finally:
        if config_path.exists():
            config_path.unlink()


@pytest.mark.asyncio
async def test_keybindings_escape_key():
    """Test that escape key cancels keybindings."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        from todo_tui.app import TodoApp
        
        app = TodoApp()
        config = Config(config_path)
        
        async with app.run_test() as pilot:
            keybindings = KeybindingsScreen(config)
            app.push_screen(keybindings)
            await pilot.pause(0.1)
            
            # Press escape
            await pilot.press("escape")
            await pilot.pause(0.1)
            
            # Screen should be dismissed
            assert not isinstance(app.screen_stack[-1], KeybindingsScreen)
    finally:
        if config_path.exists():
            config_path.unlink()


@pytest.mark.asyncio
async def test_keybindings_displays_current_values():
    """Test that keybindings screen displays current config values."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        config.set_key("quit", "ctrl+q")
        config.set_key("toggle", "enter")
        
        keybindings = KeybindingsScreen(config)
        
        # Check that inputs show current values
        assert keybindings.inputs["quit"].value == "ctrl+q"
        assert keybindings.inputs["toggle"].value == "enter"
    finally:
        if config_path.exists():
            config_path.unlink()
