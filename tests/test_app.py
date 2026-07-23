"""Tests for the Textual application."""

import pytest
from datetime import date, timedelta
from textual.widgets import Input, ListView, Button
from pathlib import Path

from todo_tui.app import TodoApp, KeyboardShortcutsHelp, TutorialScreen, CustomizeKeysScreen
from todo_tui.models import TodoItem
from todo_tui.keybindings import KeyBindings


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    return TodoApp()


def test_app_initialization(app):
    """Test app initializes correctly."""
    assert app.storage is not None
    assert isinstance(app.todos, list)
    assert app.keybindings is not None


def test_app_title(app):
    """Test app has correct title."""
    assert "TODO" in app.__class__.__name__


def test_app_has_bindings(app):
    """Test app has keyboard bindings defined."""
    binding_keys = [b.key for b in app.BINDINGS]
    assert app.keybindings.get_key("quit") in binding_keys
    assert app.keybindings.get_key("toggle_todo") in binding_keys
    assert app.keybindings.get_key("delete_todo") in binding_keys
    assert app.keybindings.get_key("postpone_todo") in binding_keys
    assert app.keybindings.get_key("show_help") in binding_keys


@pytest.mark.asyncio
async def test_app_compose(app):
    """Test app composition includes required widgets."""
    async with app.run_test() as pilot:
        # Check that key widgets are present
        assert app.query_one("#todo-list") is not None
        assert app.query_one("#todo-input") is not None


@pytest.mark.asyncio
async def test_app_add_todo(app):
    """Test adding a todo through the input."""
    async with app.run_test() as pilot:
        # Get the input widget
        input_widget = app.query_one("#todo-input", Input)
        
        # Simulate entering text and submitting
        input_widget.value = "Test task"
        await pilot.press("enter")
        
        # Check that todo was added
        assert len(app.todos) == 1
        assert app.todos[0].title == "Test task"


@pytest.mark.asyncio
async def test_app_add_empty_todo(app):
    """Test that empty todos are not added."""
    async with app.run_test() as pilot:
        input_widget = app.query_one("#todo-input", Input)
        
        # Try to add empty todo
        input_widget.value = "   "
        await pilot.press("enter")
        
        # Check that no todo was added
        assert len(app.todos) == 0


@pytest.mark.asyncio
async def test_app_toggle_todo(app):
    """Test toggling a todo's completion status."""
    # Add a todo first
    todo = TodoItem(title="Test task")
    app.storage.add(todo)
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Get the list view and select first item
        list_view = app.query_one("#todo-list", ListView)
        list_view.index = 0
        
        # Toggle the todo
        await pilot.press("space")
        
        # Check that todo was toggled
        todos = app.storage.get_all()
        assert todos[0].completed is True


@pytest.mark.asyncio
async def test_app_delete_todo(app):
    """Test deleting a todo."""
    # Add a todo first
    todo = TodoItem(title="Test task")
    app.storage.add(todo)
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Get the list view and select first item
        list_view = app.query_one("#todo-list", ListView)
        list_view.index = 0
        
        # Delete the todo
        await pilot.press("d")
        
        # Check that todo was deleted
        assert len(app.todos) == 0
        todos = app.storage.get_all()
        assert len(todos) == 0


@pytest.mark.asyncio
async def test_app_postpone_todo(app):
    """Test postponing a todo until tomorrow."""
    # Add a todo first
    todo = TodoItem(title="Test task")
    app.storage.add(todo)
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Get the list view and select first item
        list_view = app.query_one("#todo-list", ListView)
        list_view.index = 0
        
        # Postpone the todo
        await pilot.press("p")
        
        # Check that todo was postponed
        todos = app.storage.get_all()
        assert todos[0].postpone_until is not None
        assert todos[0].postpone_until == date.today() + timedelta(days=1)
        assert todos[0].is_postponed() is True


@pytest.mark.asyncio
async def test_app_postpone_multiple_times(app):
    """Test postponing a todo multiple times.
    
    Each postpone sets the date to tomorrow from today,
    not progressively advancing.
    """
    # Add a todo first
    todo = TodoItem(title="Test task")
    app.storage.add(todo)
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Get the list view and select first item
        list_view = app.query_one("#todo-list", ListView)
        list_view.index = 0
        
        # Postpone the todo twice
        await pilot.press("p")
        await pilot.press("p")
        
        # Check that todo is still postponed to tomorrow (not day after tomorrow)
        todos = app.storage.get_all()
        assert todos[0].postpone_until == date.today() + timedelta(days=1)


@pytest.mark.asyncio
async def test_app_postponed_todo_displayed(app):
    """Test that postponed todos are displayed with indicator."""
    # Add and postpone a todo
    todo = TodoItem(title="Test task")
    todo.postpone_until_tomorrow()
    app.storage.add(todo)
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Check that todo is in the list
        assert len(app.todos) == 1
        assert app.todos[0].is_postponed() is True


@pytest.mark.asyncio
async def test_show_help_dialog(app):
    """Test showing the keyboard shortcuts help dialog."""
    async with app.run_test() as pilot:
        # Press ? to show help
        await pilot.press("question_mark")
        
        # Wait for screen to be pushed
        await pilot.pause()
        
        # Check that help screen is displayed
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen, KeyboardShortcutsHelp)


@pytest.mark.asyncio
async def test_help_dialog_displays_shortcuts():
    """Test that help dialog displays all shortcut categories."""
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    
    async with help_screen.run_test() as pilot:
        # Check that key sections are present
        shortcuts = help_screen.shortcuts
        assert "Navigation" in shortcuts
        assert "TODO Management" in shortcuts
        assert "Help & Information" in shortcuts
        assert "Application" in shortcuts


@pytest.mark.asyncio
async def test_help_dialog_search():
    """Test searching in the help dialog."""
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    
    async with help_screen.run_test() as pilot:
        # Get the search input
        search_input = help_screen.query_one("#help-search", Input)
        
        # Search for "delete"
        search_input.value = "delete"
        await pilot.pause()
        
        # Check that filtered shortcuts only contain matching items
        assert "TODO Management" in help_screen.filtered_shortcuts
        
        # Check that the matching shortcut exists
        found_delete = False
        for category, items in help_screen.filtered_shortcuts.items():
            for key, desc in items:
                if "delete" in desc.lower():
                    found_delete = True
                    break
        assert found_delete


@pytest.mark.asyncio
async def test_help_dialog_search_by_key():
    """Test searching help dialog by key name."""
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    
    async with help_screen.run_test() as pilot:
        # Get the search input
        search_input = help_screen.query_one("#help-search", Input)
        
        # Search for "space"
        search_input.value = "space"
        await pilot.pause()
        
        # Check that filtered shortcuts contain Space key
        found_space = False
        for category, items in help_screen.filtered_shortcuts.items():
            for key, desc in items:
                if "space" in key.lower():
                    found_space = True
                    break
        assert found_space


@pytest.mark.asyncio
async def test_help_dialog_search_no_results():
    """Test searching with no matching results."""
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    
    async with help_screen.run_test() as pilot:
        # Get the search input
        search_input = help_screen.query_one("#help-search", Input)
        
        # Search for something that doesn't exist
        search_input.value = "xyzabc123"
        await pilot.pause()
        
        # Check that filtered shortcuts is empty
        assert len(help_screen.filtered_shortcuts) == 0


@pytest.mark.asyncio
async def test_help_dialog_search_clear():
    """Test clearing search returns all shortcuts."""
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    
    async with help_screen.run_test() as pilot:
        # Get the search input
        search_input = help_screen.query_one("#help-search", Input)
        
        # Search for something
        search_input.value = "delete"
        await pilot.pause()
        
        # Clear the search
        search_input.value = ""
        await pilot.pause()
        
        # Check that all shortcuts are shown again
        assert len(help_screen.filtered_shortcuts) == len(help_screen.shortcuts)


@pytest.mark.asyncio
async def test_help_dialog_close_with_escape(app):
    """Test closing help dialog with Escape key."""
    async with app.run_test() as pilot:
        # Open help dialog
        await pilot.press("question_mark")
        await pilot.pause()
        
        # Check help is open
        assert len(app.screen_stack) == 2
        
        # Close with Escape
        await pilot.press("escape")
        await pilot.pause()
        
        # Check help is closed
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_help_dialog_close_with_q(app):
    """Test closing help dialog with Q key."""
    async with app.run_test() as pilot:
        # Open help dialog
        await pilot.press("question_mark")
        await pilot.pause()
        
        # Check help is open
        assert len(app.screen_stack) == 2
        
        # Close with Q
        await pilot.press("q")
        await pilot.pause()
        
        # Check help is closed
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_help_contains_all_main_shortcuts():
    """Test that help includes all main app shortcuts."""
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    
    # Get all shortcuts as a flat list
    all_shortcuts = []
    for category, items in help_screen.shortcuts.items():
        all_shortcuts.extend(items)
    
    # Check for key shortcuts
    shortcut_keys = [key for key, _ in all_shortcuts]
    shortcut_text = " ".join(shortcut_keys)
    
    # Check main shortcuts are present (key names may vary)
    assert any("space" in s.lower() or "Space" in s for s in shortcut_keys)
    assert any("d" in s.lower() or "D" in s for s in shortcut_keys)
    assert any("p" in s.lower() or "P" in s for s in shortcut_keys)
    assert any("q" in s.lower() or "Q" in s for s in shortcut_keys)


@pytest.mark.asyncio
async def test_show_tutorial(app):
    """Test showing the tutorial screen."""
    async with app.run_test() as pilot:
        # Press Ctrl+T to show tutorial
        await pilot.press("ctrl+t")
        await pilot.pause()
        
        # Check that tutorial screen is displayed
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen, TutorialScreen)


@pytest.mark.asyncio
async def test_tutorial_screen_compose():
    """Test that tutorial screen composes correctly."""
    tutorial = TutorialScreen()
    
    async with tutorial.run_test() as pilot:
        # Check that tutorial content is present
        title = tutorial.query_one("#tutorial-title")
        assert title is not None
        assert "Tutorial" in title.render() or "Welcome" in title.render()


@pytest.mark.asyncio
async def test_tutorial_close_button():
    """Test closing tutorial with button."""
    tutorial = TutorialScreen()
    
    async with tutorial.run_test() as pilot:
        # Find and click close button
        close_button = tutorial.query_one("#close-tutorial")
        close_button.press()
        await pilot.pause()


@pytest.mark.asyncio
async def test_customize_keys_screen(app):
    """Test showing the customize keys screen."""
    async with app.run_test() as pilot:
        # Press Ctrl+K to show customize keys
        await pilot.press("ctrl+k")
        await pilot.pause()
        
        # Check that customize screen is displayed
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen, CustomizeKeysScreen)


@pytest.mark.asyncio
async def test_customize_keys_displays_bindings():
    """Test that customize keys screen displays current bindings."""
    keybindings = KeyBindings()
    customize = CustomizeKeysScreen(keybindings)
    
    async with customize.run_test() as pilot:
        # Check that content is present
        content = customize.query_one("#customize-content")
        assert content is not None
        
        # Check that edit buttons are present for each binding
        for action in keybindings.get_all_bindings().keys():
            edit_button = customize.query_one(f"#edit-{action}", Button)
            assert edit_button is not None


@pytest.mark.asyncio
async def test_customize_keys_edit_binding():
    """Test editing a key binding interactively."""
    keybindings = KeyBindings()
    customize = CustomizeKeysScreen(keybindings)
    
    async with customize.run_test() as pilot:
        # Click edit button for quit action
        edit_button = customize.query_one("#edit-quit", Button)
        edit_button.press()
        await pilot.pause()
        
        # Check that we're in editing mode
        assert customize.editing_action == "quit"
        
        # Simulate pressing a new key
        await pilot.press("x")
        await pilot.pause()
        
        # Check that binding was updated
        assert keybindings.get_key("quit") == "x"


@pytest.mark.asyncio
async def test_customize_keys_cancel_editing():
    """Test canceling key binding editing with escape."""
    keybindings = KeyBindings()
    original_key = keybindings.get_key("quit")
    customize = CustomizeKeysScreen(keybindings)
    
    async with customize.run_test() as pilot:
        # Start editing
        edit_button = customize.query_one("#edit-quit", Button)
        edit_button.press()
        await pilot.pause()
        
        assert customize.editing_action == "quit"
        
        # Cancel with escape
        await pilot.press("escape")
        await pilot.pause()
        
        # Check that editing was cancelled
        assert customize.editing_action is None
        
        # Check that binding was NOT changed
        assert keybindings.get_key("quit") == original_key


@pytest.mark.asyncio
async def test_customize_keys_reset():
    """Test resetting key bindings to defaults."""
    keybindings = KeyBindings()
    # Modify a binding
    keybindings.set_key("quit", "ctrl+q")
    
    customize = CustomizeKeysScreen(keybindings)
    
    async with customize.run_test() as pilot:
        # Click reset button
        reset_button = customize.query_one("#reset-keys")
        reset_button.press()
        await pilot.pause()
        
        # Check that bindings were reset
        assert keybindings.get_key("quit") == "q"


@pytest.mark.asyncio
async def test_customize_keys_saves_to_file(tmp_path):
    """Test that customized bindings are persisted to file."""
    storage_path = tmp_path / "test-keys.json"
    keybindings = KeyBindings(storage_path)
    customize = CustomizeKeysScreen(keybindings)
    
    async with customize.run_test() as pilot:
        # Edit a binding
        edit_button = customize.query_one("#edit-quit", Button)
        edit_button.press()
        await pilot.pause()
        
        await pilot.press("x")
        await pilot.pause()
        
        # Verify file was updated
        assert storage_path.exists()
        
        # Load in new instance to verify persistence
        keybindings2 = KeyBindings(storage_path)
        assert keybindings2.get_key("quit") == "x"


@pytest.mark.asyncio
async def test_export_shortcuts(app, tmp_path):
    """Test exporting shortcuts cheat sheet."""
    async with app.run_test() as pilot:
        # Trigger export
        await pilot.press("ctrl+e")
        await pilot.pause()
        
        # Check that file was created
        cheat_sheet_path = Path.home() / "todo-tui-shortcuts.txt"
        assert cheat_sheet_path.exists()
        
        # Check content
        content = cheat_sheet_path.read_text()
        assert "Keyboard Shortcuts Cheat Sheet" in content
        assert "Navigation" in content
        assert "TODO Management" in content
        
        # Cleanup
        cheat_sheet_path.unlink()


def test_keybindings_initialization():
    """Test KeyBindings class initialization."""
    kb = KeyBindings()
    assert kb.get_key("quit") == "q"
    assert kb.get_key("toggle_todo") == "space"
    assert kb.get_key("delete_todo") == "d"


def test_keybindings_set_key():
    """Test setting a custom key binding."""
    kb = KeyBindings()
    kb.set_key("quit", "ctrl+q")
    assert kb.get_key("quit") == "ctrl+q"


def test_keybindings_reset_to_defaults():
    """Test resetting bindings to defaults."""
    kb = KeyBindings()
    kb.set_key("quit", "ctrl+q")
    kb.reset_to_defaults()
    assert kb.get_key("quit") == "q"


def test_keybindings_format_key_for_display():
    """Test formatting key names for display."""
    kb = KeyBindings()
    assert kb.format_key_for_display("question_mark") == "?"
    assert kb.format_key_for_display("space") == "Space"
    assert "Ctrl" in kb.format_key_for_display("ctrl+e")


def test_keybindings_persistence(tmp_path):
    """Test that key bindings are persisted to disk."""
    storage_path = tmp_path / "test-keys.json"
    
    # Create and modify bindings
    kb1 = KeyBindings(storage_path)
    kb1.set_key("quit", "ctrl+q")
    
    # Load bindings in new instance
    kb2 = KeyBindings(storage_path)
    assert kb2.get_key("quit") == "ctrl+q"


def test_keybindings_get_description():
    """Test getting action descriptions."""
    kb = KeyBindings()
    assert "Quit" in kb.get_description("quit")
    assert "Toggle" in kb.get_description("toggle_todo")
    assert "Delete" in kb.get_description("delete_todo")
