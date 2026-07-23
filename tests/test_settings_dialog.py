"""Tests for the settings dialog."""

import pytest
from textual.widgets import Button, Input

from todo_tui.settings_dialog import SettingsDialog, BindingEditor
from todo_tui.keybindings import KeyBindingsManager
from todo_tui.app import TodoApp


@pytest.fixture
def keybindings_manager(tmp_path):
    """Create a KeyBindingsManager for testing."""
    bindings_path = tmp_path / "test-keybindings.json"
    return KeyBindingsManager(bindings_path)


@pytest.fixture
def settings_dialog(keybindings_manager):
    """Create a SettingsDialog instance for testing."""
    return SettingsDialog(keybindings_manager)


def test_binding_editor_initialization():
    """Test BindingEditor widget initialization."""
    editor = BindingEditor("quit", "q", "Quit application")
    
    assert editor.action == "quit"
    assert editor.key == "q"
    assert editor.description == "Quit application"


@pytest.mark.asyncio
async def test_binding_editor_composition():
    """Test BindingEditor composes correctly."""
    app = TodoApp()
    async with app.run_test():
        editor = BindingEditor("quit", "q", "Quit application")
        
        # Mount the editor
        await app.mount(editor)
        
        # Should have input widget
        input_widget = editor.query_one(Input)
        assert input_widget.value == "q"


def test_settings_dialog_initialization(settings_dialog, keybindings_manager):
    """Test settings dialog initializes correctly."""
    assert settings_dialog is not None
    assert settings_dialog.keybindings_manager == keybindings_manager


@pytest.mark.asyncio
async def test_settings_dialog_composition(settings_dialog):
    """Test settings dialog composes correctly."""
    app = TodoApp()
    async with app.run_test():
        app.push_screen(settings_dialog)
        
        # Check that key widgets are present
        assert settings_dialog.query_one("#settings-title") is not None
        assert settings_dialog.query_one("#settings-content") is not None
        assert settings_dialog.query_one("#save-btn") is not None
        assert settings_dialog.query_one("#reset-btn") is not None
        assert settings_dialog.query_one("#cancel-btn") is not None


@pytest.mark.asyncio
async def test_settings_dialog_shows_all_bindings(settings_dialog, keybindings_manager):
    """Test that settings dialog shows all key bindings."""
    app = TodoApp()
    async with app.run_test():
        app.push_screen(settings_dialog)
        
        bindings = keybindings_manager.get_all_bindings()
        
        # Check that input exists for each binding
        for action in bindings.keys():
            input_id = f"binding-{action}"
            try:
                input_widget = settings_dialog.query_one(f"#{input_id}", Input)
                assert input_widget is not None
            except Exception:
                pytest.fail(f"Input for action '{action}' not found")


@pytest.mark.asyncio
async def test_settings_dialog_save_button(settings_dialog, keybindings_manager):
    """Test saving custom bindings."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        # Change a binding
        quit_input = settings_dialog.query_one("#binding-quit", Input)
        quit_input.value = "x"
        
        # Click save button
        await pilot.click(Button, "#save-btn")
        await pilot.pause()
        
        # Verify binding was saved
        assert keybindings_manager.get_binding("quit") == "x"


@pytest.mark.asyncio
async def test_settings_dialog_cancel_button(settings_dialog, keybindings_manager):
    """Test cancel button doesn't save changes."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        original_quit = keybindings_manager.get_binding("quit")
        
        # Change a binding
        quit_input = settings_dialog.query_one("#binding-quit", Input)
        quit_input.value = "x"
        
        # Click cancel button
        await pilot.click(Button, "#cancel-btn")
        await pilot.pause()
        
        # Verify binding was NOT saved
        assert keybindings_manager.get_binding("quit") == original_quit


@pytest.mark.asyncio
async def test_settings_dialog_reset_button(settings_dialog, keybindings_manager):
    """Test reset button restores defaults."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        # Set a custom binding first
        keybindings_manager.set_binding("quit", "x")
        
        # Click reset button
        await pilot.click(Button, "#reset-btn")
        await pilot.pause()
        
        # Verify binding was reset
        assert keybindings_manager.get_binding("quit") == "q"


@pytest.mark.asyncio
async def test_settings_dialog_escape_binding(settings_dialog):
    """Test escape key binding cancels dialog."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        # Press escape
        await pilot.press("escape")
        await pilot.pause()
        
        # Should dismiss without errors


@pytest.mark.asyncio
async def test_settings_dialog_bindings():
    """Test that settings dialog has proper key bindings."""
    keybindings_manager = KeyBindingsManager()
    settings_dialog = SettingsDialog(keybindings_manager)
    
    binding_keys = [b.key for b in settings_dialog.BINDINGS]
    assert "escape" in binding_keys, "Should have escape key binding"


def test_settings_dialog_action_descriptions():
    """Test that action descriptions are defined."""
    assert len(SettingsDialog.ACTION_DESCRIPTIONS) > 0
    
    # Check key actions have descriptions
    assert "quit" in SettingsDialog.ACTION_DESCRIPTIONS
    assert "toggle" in SettingsDialog.ACTION_DESCRIPTIONS
    assert "delete" in SettingsDialog.ACTION_DESCRIPTIONS


@pytest.mark.asyncio
async def test_settings_dialog_save_multiple_bindings(settings_dialog, keybindings_manager):
    """Test saving multiple custom bindings at once."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        # Change multiple bindings
        quit_input = settings_dialog.query_one("#binding-quit", Input)
        quit_input.value = "x"
        
        toggle_input = settings_dialog.query_one("#binding-toggle", Input)
        toggle_input.value = "t"
        
        delete_input = settings_dialog.query_one("#binding-delete", Input)
        delete_input.value = "r"
        
        # Click save button
        await pilot.click(Button, "#save-btn")
        await pilot.pause()
        
        # Verify all bindings were saved
        assert keybindings_manager.get_binding("quit") == "x"
        assert keybindings_manager.get_binding("toggle") == "t"
        assert keybindings_manager.get_binding("delete") == "r"


@pytest.mark.asyncio
async def test_settings_dialog_reset_updates_inputs(settings_dialog, keybindings_manager):
    """Test that reset button updates input fields."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        # Set custom bindings
        keybindings_manager.set_binding("quit", "x")
        keybindings_manager.set_binding("toggle", "t")
        
        # Change input values manually
        quit_input = settings_dialog.query_one("#binding-quit", Input)
        quit_input.value = "x"
        
        # Click reset button
        settings_dialog._reset_bindings()
        await pilot.pause()
        
        # Input should be updated to default
        assert quit_input.value == "q"


@pytest.mark.asyncio
async def test_settings_dialog_save_empty_binding(settings_dialog, keybindings_manager):
    """Test that empty bindings are not saved."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        original_quit = keybindings_manager.get_binding("quit")
        
        # Clear a binding
        quit_input = settings_dialog.query_one("#binding-quit", Input)
        quit_input.value = ""
        
        # Click save button
        settings_dialog._save_bindings()
        await pilot.pause()
        
        # Original binding should be preserved
        assert keybindings_manager.get_binding("quit") == original_quit


@pytest.mark.asyncio
async def test_settings_dialog_action_cancel(settings_dialog):
    """Test cancel action."""
    app = TodoApp()
    async with app.run_test():
        app.push_screen(settings_dialog)
        
        # Call cancel action
        settings_dialog.action_cancel()
        
        # Should dismiss without errors


def test_settings_dialog_with_custom_bindings(keybindings_manager):
    """Test settings dialog with pre-existing custom bindings."""
    keybindings_manager.set_binding("quit", "x")
    keybindings_manager.set_binding("toggle", "t")
    
    settings_dialog = SettingsDialog(keybindings_manager)
    
    # Dialog should have the manager
    assert settings_dialog.keybindings_manager == keybindings_manager


@pytest.mark.asyncio
async def test_settings_dialog_notification_on_save(settings_dialog):
    """Test that save shows a notification."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        # Change a binding
        quit_input = settings_dialog.query_one("#binding-quit", Input)
        quit_input.value = "x"
        
        # Save
        settings_dialog._save_bindings()
        await pilot.pause()
        
        # Should show notification (we just verify no errors)


@pytest.mark.asyncio
async def test_settings_dialog_notification_on_reset(settings_dialog):
    """Test that reset shows a notification."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(settings_dialog)
        
        # Reset
        settings_dialog._reset_bindings()
        await pilot.pause()
        
        # Should show notification (we just verify no errors)
