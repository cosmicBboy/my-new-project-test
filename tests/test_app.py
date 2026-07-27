"""Tests for the Textual application."""

import pytest
from datetime import date, timedelta
from pathlib import Path
from textual.widgets import Input, ListView, Button

from todo_tui.app import TodoApp, HelpScreen, CustomizeBindingsScreen, TutorialScreen
from todo_tui.models import TodoItem
from todo_tui.config import Config, DEFAULT_BINDINGS


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    return TodoApp()


@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config for testing."""
    config_path = tmp_path / "test-config.json"
    return Config(config_path)


def test_app_initialization(app):
    """Test app initializes correctly."""
    assert app.storage is not None
    assert app.config is not None
    assert isinstance(app.todos, list)


def test_app_title(app):
    """Test app has correct title."""
    assert "TODO" in app.__class__.__name__


def test_app_has_bindings(app):
    """Test app has keyboard bindings defined."""
    binding_keys = [b.key for b in app.BINDINGS]
    assert app.config.get_binding("quit") in binding_keys
    assert app.config.get_binding("toggle") in binding_keys
    assert app.config.get_binding("delete") in binding_keys
    assert app.config.get_binding("postpone") in binding_keys
    assert app.config.get_binding("help") in binding_keys
    assert app.config.get_binding("customize") in binding_keys


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
async def test_app_show_help(app):
    """Test showing the help screen."""
    async with app.run_test() as pilot:
        # Press ? to show help
        await pilot.press("question_mark")
        
        # Check that help screen is visible
        assert app.screen is not None
        assert isinstance(app.screen, HelpScreen)


@pytest.mark.asyncio
async def test_help_screen_has_shortcuts(app):
    """Test that help screen displays shortcuts."""
    async with app.run_test() as pilot:
        # Show help screen
        await pilot.press("question_mark")
        
        # Check that help screen has shortcuts
        help_screen = app.screen
        assert isinstance(help_screen, HelpScreen)
        assert len(help_screen.all_shortcuts) > 0


@pytest.mark.asyncio
async def test_help_screen_search(app):
    """Test searching shortcuts in help screen."""
    async with app.run_test() as pilot:
        # Show help screen
        await pilot.press("question_mark")
        
        help_screen = app.screen
        assert isinstance(help_screen, HelpScreen)
        
        # Get initial shortcuts count
        initial_count = len(help_screen.filtered_shortcuts)
        
        # Search for "delete"
        search_input = help_screen.query_one("#help-search", Input)
        search_input.value = "delete"
        
        # Wait for the change to process
        await pilot.pause()
        
        # Check that results are filtered
        assert len(help_screen.filtered_shortcuts) < initial_count
        assert any("delete" in s["description"].lower() for s in help_screen.filtered_shortcuts)


@pytest.mark.asyncio
async def test_help_screen_search_no_results(app):
    """Test searching with no matching shortcuts."""
    async with app.run_test() as pilot:
        # Show help screen
        await pilot.press("question_mark")
        
        help_screen = app.screen
        assert isinstance(help_screen, HelpScreen)
        
        # Search for something that doesn't exist
        search_input = help_screen.query_one("#help-search", Input)
        search_input.value = "zzzznonexistent"
        
        # Wait for the change to process
        await pilot.pause()
        
        # Check that no results are found
        assert len(help_screen.filtered_shortcuts) == 0


@pytest.mark.asyncio
async def test_help_screen_search_clear(app):
    """Test clearing search in help screen."""
    async with app.run_test() as pilot:
        # Show help screen
        await pilot.press("question_mark")
        
        help_screen = app.screen
        assert isinstance(help_screen, HelpScreen)
        
        initial_count = len(help_screen.all_shortcuts)
        
        # Search for something
        search_input = help_screen.query_one("#help-search", Input)
        search_input.value = "delete"
        await pilot.pause()
        
        # Clear search
        search_input.value = ""
        await pilot.pause()
        
        # Check that all shortcuts are shown again
        assert len(help_screen.filtered_shortcuts) == initial_count


@pytest.mark.asyncio
async def test_help_screen_close_with_escape(app):
    """Test closing help screen with escape key."""
    async with app.run_test() as pilot:
        # Show help screen
        await pilot.press("question_mark")
        
        # Verify help screen is shown
        assert isinstance(app.screen, HelpScreen)
        
        # Close with escape
        await pilot.press("escape")
        
        # Wait for the screen to dismiss
        await pilot.pause()
        
        # Check that we're back to the main screen
        assert not isinstance(app.screen, HelpScreen)


@pytest.mark.asyncio
async def test_help_screen_close_with_q(app):
    """Test closing help screen with q key."""
    async with app.run_test() as pilot:
        # Show help screen
        await pilot.press("question_mark")
        
        # Verify help screen is shown
        assert isinstance(app.screen, HelpScreen)
        
        # Close with q
        await pilot.press("q")
        
        # Wait for the screen to dismiss
        await pilot.pause()
        
        # Check that we're back to the main screen
        assert not isinstance(app.screen, HelpScreen)


@pytest.mark.asyncio
async def test_help_screen_export_button(app):
    """Test exporting cheat sheet from help screen."""
    async with app.run_test() as pilot:
        # Show help screen
        await pilot.press("question_mark")
        
        help_screen = app.screen
        assert isinstance(help_screen, HelpScreen)
        
        # Click export button using the selector
        export_button = help_screen.query_one("#export-button", Button)
        await pilot.click(Button, "#export-button")
        
        # Check that file was created
        export_path = Path.home() / "todo-tui-shortcuts.txt"
        assert export_path.exists()
        
        # Check content
        content = export_path.read_text()
        assert "Keyboard Shortcuts Cheat Sheet" in content
        assert "Navigation" in content
        assert "Task Management" in content


def test_help_screen_shortcuts_categories():
    """Test that help screen has shortcuts organized by categories."""
    config = Config()
    help_screen = HelpScreen(config)
    
    shortcuts = help_screen.all_shortcuts
    categories = set(s["category"] for s in shortcuts)
    
    # Check that we have expected categories
    assert "Navigation" in categories
    assert "Task Management" in categories
    assert "Application" in categories
    assert "Tips" in categories


def test_help_screen_shortcuts_content():
    """Test that help screen includes key shortcuts."""
    config = Config()
    help_screen = HelpScreen(config)
    
    shortcuts = help_screen.all_shortcuts
    descriptions = [s["description"].lower() for s in shortcuts]
    
    # Check that descriptions mention key actions
    assert any("toggle" in d for d in descriptions)
    assert any("delete" in d for d in descriptions)
    assert any("postpone" in d for d in descriptions)
    assert any("quit" in d for d in descriptions)
    assert any("customize" in d for d in descriptions)


@pytest.mark.asyncio
async def test_customize_bindings_screen(app):
    """Test showing the customize bindings screen."""
    async with app.run_test() as pilot:
        # Press c to show customize screen
        await pilot.press("c")
        
        # Check that customize screen is visible
        assert app.screen is not None
        assert isinstance(app.screen, CustomizeBindingsScreen)


@pytest.mark.asyncio
async def test_customize_bindings_reset(temp_config):
    """Test resetting key bindings to defaults."""
    # Change a binding
    temp_config.set_binding("quit", "ctrl+q")
    temp_config.save_bindings()
    assert temp_config.get_binding("quit") == "ctrl+q"
    
    # Reset
    temp_config.reset_bindings()
    assert temp_config.get_binding("quit") == DEFAULT_BINDINGS["quit"]


@pytest.mark.asyncio
async def test_customize_bindings_save(temp_config):
    """Test that custom bindings are saved."""
    # Set a custom binding
    temp_config.set_binding("delete", "x")
    temp_config.save_bindings()
    
    # Create a new config instance with the same path
    new_config = Config(temp_config.config_path)
    
    # Check that the binding persists
    assert new_config.get_binding("delete") == "x"


@pytest.mark.asyncio
async def test_export_shortcuts_action(app):
    """Test exporting shortcuts via action."""
    async with app.run_test() as pilot:
        # Export shortcuts
        await pilot.press("ctrl+e")
        
        # Check that file was created
        export_path = Path.home() / "todo-tui-shortcuts.txt"
        assert export_path.exists()
        
        # Check content
        content = export_path.read_text()
        assert "Keyboard Shortcuts Cheat Sheet" in content
        assert "space" in content.lower() or "toggle" in content.lower()


@pytest.mark.asyncio
async def test_tutorial_screen(app):
    """Test showing the tutorial screen."""
    async with app.run_test() as pilot:
        # Press Ctrl+T to show tutorial
        await pilot.press("ctrl+t")
        
        # Check that tutorial screen is visible
        assert app.screen is not None
        assert isinstance(app.screen, TutorialScreen)


@pytest.mark.asyncio
async def test_tutorial_screen_close(app):
    """Test closing tutorial screen with button."""
    async with app.run_test() as pilot:
        # Show tutorial
        await pilot.press("ctrl+t")
        
        tutorial_screen = app.screen
        assert isinstance(tutorial_screen, TutorialScreen)
        
        # Click close button using the selector
        close_button = tutorial_screen.query_one("#tutorial-close", Button)
        await pilot.click(Button, "#tutorial-close")
        
        # Wait for dismissal
        await pilot.pause()
        
        # Check that we're back to main screen
        assert not isinstance(app.screen, TutorialScreen)


def test_tutorial_shown_flag(temp_config):
    """Test that tutorial shown flag is saved."""
    assert temp_config.tutorial_shown is False
    
    temp_config.mark_tutorial_shown()
    assert temp_config.tutorial_shown is True
    
    # Create new config instance
    new_config = Config(temp_config.config_path)
    assert new_config.tutorial_shown is True


def test_config_default_bindings():
    """Test that default bindings are correctly defined."""
    assert DEFAULT_BINDINGS["quit"] == "q"
    assert DEFAULT_BINDINGS["toggle"] == "space"
    assert DEFAULT_BINDINGS["delete"] == "d"
    assert DEFAULT_BINDINGS["postpone"] == "p"
    assert DEFAULT_BINDINGS["help"] == "question_mark"
    assert DEFAULT_BINDINGS["customize"] == "c"
    assert DEFAULT_BINDINGS["export_shortcuts"] == "ctrl+e"
    assert DEFAULT_BINDINGS["tutorial"] == "ctrl+t"


def test_config_get_binding(temp_config):
    """Test getting a key binding."""
    assert temp_config.get_binding("quit") == "q"
    assert temp_config.get_binding("toggle") == "space"


def test_config_set_binding(temp_config):
    """Test setting a custom key binding."""
    temp_config.set_binding("quit", "ctrl+q")
    assert temp_config.get_binding("quit") == "ctrl+q"


def test_config_persistence(temp_config):
    """Test that config persists across instances."""
    # Set some custom bindings
    temp_config.set_binding("quit", "ctrl+q")
    temp_config.set_binding("delete", "x")
    temp_config.mark_tutorial_shown()
    
    # Create new config with same path
    new_config = Config(temp_config.config_path)
    
    # Check that settings persist
    assert new_config.get_binding("quit") == "ctrl+q"
    assert new_config.get_binding("delete") == "x"
    assert new_config.tutorial_shown is True
