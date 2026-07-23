"""Tests for the Textual application."""

import pytest
from datetime import date, timedelta
from textual.widgets import Input, ListView

from todo_tui.app import TodoApp
from todo_tui.models import TodoItem
from todo_tui.themes import ThemePreset


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    return TodoApp()


def test_app_initialization(app):
    """Test app initializes correctly."""
    assert app.storage is not None
    assert app.config is not None
    assert isinstance(app.todos, list)


def test_app_has_theme(app):
    """Test app has a theme configured."""
    assert app.config.theme is not None
    assert app.config.theme.preset in ThemePreset


def test_app_css_property(app):
    """Test app CSS property generates valid CSS."""
    css = app.CSS
    assert isinstance(css, str)
    assert len(css) > 0
    assert "background:" in css
    assert "color:" in css


def test_app_title(app):
    """Test app has correct title."""
    assert "TODO" in app.__class__.__name__


def test_app_has_bindings(app):
    """Test app has keyboard bindings defined."""
    binding_keys = [b.key for b in app.BINDINGS]
    assert "q" in binding_keys  # quit
    assert "space" in binding_keys  # toggle
    assert "d" in binding_keys  # delete
    assert "p" in binding_keys  # postpone
    assert "t" in binding_keys  # theme
    assert "f" in binding_keys  # font size
    assert "l" in binding_keys  # layout


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
async def test_app_cycle_theme(app):
    """Test cycling through themes."""
    async with app.run_test() as pilot:
        original_theme = app.config.theme.preset
        
        # Cycle theme
        await pilot.press("t")
        
        # Check that theme changed
        new_theme = app.config.theme.preset
        assert new_theme != original_theme


@pytest.mark.asyncio
async def test_app_cycle_font_size(app):
    """Test cycling through font sizes."""
    async with app.run_test() as pilot:
        original_size = app.config.theme.font_size
        
        # Cycle font size
        await pilot.press("f")
        
        # Check that font size changed
        new_size = app.config.theme.font_size
        assert new_size != original_size


@pytest.mark.asyncio
async def test_app_cycle_layout(app):
    """Test cycling through layouts."""
    async with app.run_test() as pilot:
        original_layout = app.config.theme.layout
        
        # Cycle layout
        await pilot.press("l")
        
        # Check that layout changed
        new_layout = app.config.theme.layout
        assert new_layout != original_layout


@pytest.mark.asyncio
async def test_app_title_includes_theme(app):
    """Test app title includes current theme name."""
    async with app.run_test() as pilot:
        # Title should include theme name
        assert app.config.theme.name in app.title
        
        # Cycle theme and check title updates
        await pilot.press("t")
        assert app.config.theme.name in app.title
