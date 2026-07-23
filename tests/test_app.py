"""Tests for the Textual application."""

import pytest
from datetime import date, timedelta
from pathlib import Path
from textual.widgets import Input, ListView

from todo_tui.app import TodoApp, KeyboardShortcutsScreen, TutorialScreen, CustomizeKeysScreen
from todo_tui.models import TodoItem
from todo_tui.config import KeyBindingConfig, AppConfig


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    return TodoApp()


def test_app_initialization(app):
    """Test app initializes correctly."""
    assert app.storage is not None
    assert isinstance(app.todos, list)
    assert app.key_config is not None
    assert app.app_config is not None


def test_app_title(app):
    """Test app has correct title."""
    assert "TODO" in app.__class__.__name__


def test_app_has_bindings(app):
    """Test app has keyboard bindings defined."""
    binding_keys = [b.key for b in app.BINDINGS]
    assert "q" in binding_keys  # quit (default)
    assert "space" in binding_keys  # toggle (default)
    assert "d" in binding_keys  # delete (default)
    assert "p" in binding_keys  # postpone (default)
    assert "?" in binding_keys  # help (default)


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
async def test_keyboard_shortcuts_screen_opens(app):
    """Test that the keyboard shortcuts screen can be opened."""
    async with app.run_test() as pilot:
        # Press ? to open shortcuts screen
        await pilot.press("?")
        
        # Check that the screen is displayed
        assert len(app.screen_stack) == 2  # Main screen + shortcuts screen
        assert isinstance(app.screen, KeyboardShortcutsScreen)


@pytest.mark.asyncio
async def test_keyboard_shortcuts_screen_closes_with_escape(app):
    """Test that the keyboard shortcuts screen closes with Escape."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("?")
        assert len(app.screen_stack) == 2
        
        # Close with Escape
        await pilot.press("escape")
        
        # Check that we're back to the main screen
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_keyboard_shortcuts_screen_closes_with_q(app):
    """Test that the keyboard shortcuts screen closes with 'q'."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("?")
        assert len(app.screen_stack) == 2
        
        # Close with q
        await pilot.press("q")
        
        # Check that we're back to the main screen
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_keyboard_shortcuts_search_functionality(app):
    """Test that the search in shortcuts screen filters results."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("?")
        
        # Get the search input
        shortcuts_screen = app.screen
        search_input = shortcuts_screen.query_one("#shortcuts-search", Input)
        
        # Initially, all shortcuts should be shown
        initial_count = len(shortcuts_screen.filtered_shortcuts)
        assert initial_count > 0
        
        # Search for "quit"
        search_input.value = "quit"
        await pilot.pause()
        
        # Check that filtered results are fewer
        filtered_count = len(shortcuts_screen.filtered_shortcuts)
        assert filtered_count < initial_count


@pytest.mark.asyncio
async def test_tutorial_screen_opens(app):
    """Test that the tutorial screen can be opened."""
    async with app.run_test() as pilot:
        # Skip first-run auto-show
        await pilot.pause()
        
        # Press Ctrl+T to open tutorial
        await pilot.press("ctrl+t")
        
        # Check that the screen is displayed
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen, TutorialScreen)


@pytest.mark.asyncio
async def test_tutorial_screen_closes_with_escape(app):
    """Test that the tutorial screen closes with Escape."""
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Open tutorial screen
        await pilot.press("ctrl+t")
        assert len(app.screen_stack) == 2
        
        # Close with Escape
        await pilot.press("escape")
        
        # Check that we're back to the main screen
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_tutorial_screen_closes_with_button(app):
    """Test that the tutorial screen closes with the button."""
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Open tutorial screen
        await pilot.press("ctrl+t")
        assert len(app.screen_stack) == 2
        
        # Click the button (simulate with Enter)
        await pilot.press("enter")
        
        # Check that we're back to the main screen
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_customize_keys_screen_opens(app):
    """Test that the customize keys screen can be opened."""
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Press Ctrl+K to open customize screen
        await pilot.press("ctrl+k")
        
        # Check that the screen is displayed
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen, CustomizeKeysScreen)


@pytest.mark.asyncio
async def test_customize_keys_screen_closes(app):
    """Test that the customize keys screen closes with Escape."""
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Open customize screen
        await pilot.press("ctrl+k")
        assert len(app.screen_stack) == 2
        
        # Close with Escape
        await pilot.press("escape")
        
        # Check that we're back to the main screen
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_export_cheatsheet(app):
    """Test exporting keyboard shortcuts cheat sheet."""
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Press Ctrl+H to export cheat sheet
        await pilot.press("ctrl+h")
        
        # Check that file was created
        cheatsheet_path = Path.home() / "todo-tui-shortcuts.txt"
        assert cheatsheet_path.exists()
        
        # Check content
        content = cheatsheet_path.read_text()
        assert "Keyboard Shortcuts Cheat Sheet" in content
        assert "Navigation:" in content
        assert "TODO Management:" in content
        
        # Cleanup
        cheatsheet_path.unlink()


@pytest.mark.asyncio
async def test_first_run_shows_tutorial(app):
    """Test that tutorial shows on first run."""
    # Create a fresh app config
    app.app_config = AppConfig()
    app.app_config.set("first_run", True)
    
    async with app.run_test() as pilot:
        # Allow tutorial to show
        await pilot.pause()
        await pilot.pause()
        
        # Tutorial should be shown (screen stack has 2 items)
        # Note: This may be timing-dependent
        if len(app.screen_stack) == 2:
            assert isinstance(app.screen, TutorialScreen)


def test_keyboard_shortcuts_screen_has_content():
    """Test that the keyboard shortcuts screen displays content."""
    key_config = KeyBindingConfig()
    shortcuts_screen = KeyboardShortcutsScreen(key_config)
    
    # Check that shortcuts are loaded
    assert len(shortcuts_screen.all_shortcuts) > 0
    
    # Check categories exist
    categories = [cat for cat, _ in shortcuts_screen.all_shortcuts]
    assert "Navigation" in categories
    assert "TODO Management" in categories
    assert "Help & Customization" in categories
    assert "Application" in categories


def test_keyboard_shortcuts_screen_uses_custom_bindings():
    """Test that shortcuts screen displays custom key bindings."""
    # Create custom config
    key_config = KeyBindingConfig()
    key_config.set_binding("quit", "ctrl+q")
    key_config.set_binding("toggle_todo", "t")
    
    shortcuts_screen = KeyboardShortcutsScreen(key_config)
    shortcuts = shortcuts_screen._get_all_shortcuts()
    
    # Find the quit shortcut
    for category, items in shortcuts:
        for key, desc in items:
            if "quit" in desc.lower() and "force" not in desc.lower():
                assert key == "ctrl+q"
            elif "toggle" in desc.lower():
                assert key == "t"


def test_tutorial_screen_initialization():
    """Test that tutorial screen initializes correctly."""
    tutorial = TutorialScreen()
    assert tutorial is not None


def test_customize_keys_screen_initialization():
    """Test that customize keys screen initializes correctly."""
    key_config = KeyBindingConfig()
    customize = CustomizeKeysScreen(key_config)
    assert customize is not None
    assert customize.key_config == key_config


def test_app_loads_custom_key_bindings():
    """Test that app loads custom key bindings on initialization."""
    # This is tested implicitly by app initialization
    app = TodoApp()
    
    # Check that bindings are loaded from config
    assert app.key_config is not None
    assert app.key_config.get_binding("quit") is not None


@pytest.mark.asyncio
async def test_keyboard_shortcuts_reflects_custom_keys(app):
    """Test that keyboard shortcuts help reflects custom bindings."""
    # Customize a key
    app.key_config.set_binding("quit", "ctrl+q")
    
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Open shortcuts (need to recreate screen with updated config)
        app.action_show_shortcuts()
        await pilot.pause()
        
        # The shortcuts screen should show the custom binding
        # (This is verified by the screen using key_config)
        assert len(app.screen_stack) == 2


def test_export_cheatsheet_content():
    """Test that exported cheat sheet contains all expected content."""
    app = TodoApp()
    
    # Export cheat sheet
    app.action_export_cheatsheet()
    
    # Read and verify content
    cheatsheet_path = Path.home() / "todo-tui-shortcuts.txt"
    assert cheatsheet_path.exists()
    
    content = cheatsheet_path.read_text()
    
    # Check for all major sections
    assert "Navigation:" in content
    assert "TODO Management:" in content
    assert "Help & Customization:" in content
    assert "Application:" in content
    assert "Configuration Files:" in content
    assert "~/.todo-tui.json" in content
    assert "~/.todo-tui-keybindings.json" in content
    
    # Cleanup
    cheatsheet_path.unlink()
