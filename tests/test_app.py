"""Tests for the Textual application."""

import pytest
from datetime import date, timedelta
from textual.widgets import Input, ListView

from todo_tui.app import TodoApp
from todo_tui.models import TodoItem
from todo_tui.themes import ThemeName, LayoutDensity, FontSize


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    return TodoApp()


def test_app_initialization(app):
    """Test app initializes correctly."""
    assert app.storage is not None
    assert app.preferences is not None
    assert isinstance(app.todos, list)


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
    assert "l" in binding_keys  # layout
    assert "f" in binding_keys  # font size


def test_app_theme_initialization(app):
    """Test app initializes with theme from preferences."""
    assert hasattr(app, "current_theme")
    assert app.current_theme in [t.value for t in ThemeName] or app.current_theme in app.custom_themes


def test_app_layout_density_initialization(app):
    """Test app initializes with layout density from preferences."""
    assert hasattr(app, "layout_density")
    assert isinstance(app.layout_density, LayoutDensity)


def test_app_font_size_initialization(app):
    """Test app initializes with font size from preferences."""
    assert hasattr(app, "font_size")
    assert isinstance(app.font_size, FontSize)


def test_app_loads_custom_themes(app):
    """Test app loads custom themes from preferences."""
    assert hasattr(app, "custom_themes")
    assert isinstance(app.custom_themes, dict)


def test_app_all_themes_registry(app):
    """Test app builds combined theme registry."""
    assert hasattr(app, "all_themes")
    # Should include built-in themes at minimum
    assert len(app.all_themes) >= 4


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
        initial_theme = app.current_theme
        
        # Cycle theme
        await pilot.press("t")
        
        # Check that theme changed
        new_theme = app.current_theme
        assert new_theme != initial_theme
        
        # Verify theme is saved in preferences
        saved_theme = app.preferences.get_theme()
        assert saved_theme == new_theme


@pytest.mark.asyncio
async def test_app_cycle_layout(app):
    """Test cycling through layout densities."""
    async with app.run_test() as pilot:
        initial_density = app.layout_density
        
        # Cycle layout
        await pilot.press("l")
        
        # Check that layout density changed
        new_density = app.layout_density
        assert new_density != initial_density
        
        # Verify layout is saved in preferences
        saved_density = app.preferences.get_layout_density()
        assert saved_density == new_density.value


@pytest.mark.asyncio
async def test_app_cycle_font_size(app):
    """Test cycling through font sizes."""
    async with app.run_test() as pilot:
        initial_size = app.font_size
        
        # Cycle font size
        await pilot.press("f")
        
        # Check that font size changed
        new_size = app.font_size
        assert new_size != initial_size
        
        # Verify font size is saved in preferences
        saved_size = app.preferences.get_font_size()
        assert saved_size == new_size.value


@pytest.mark.asyncio
async def test_app_cycle_theme_full_cycle(app):
    """Test that cycling through all themes returns to the start."""
    async with app.run_test() as pilot:
        initial_theme = app.current_theme
        num_themes = len(app.all_themes)
        
        # Cycle through all themes
        for _ in range(num_themes):
            await pilot.press("t")
        
        # Should be back to the initial theme
        assert app.current_theme == initial_theme


@pytest.mark.asyncio
async def test_app_cycle_layout_full_cycle(app):
    """Test that cycling through all layout densities returns to the start."""
    async with app.run_test() as pilot:
        initial_density = app.layout_density
        
        # Cycle through all 3 densities
        for _ in range(3):
            await pilot.press("l")
        
        # Should be back to the initial density
        assert app.layout_density == initial_density


@pytest.mark.asyncio
async def test_app_cycle_font_size_full_cycle(app):
    """Test that cycling through all font sizes returns to the start."""
    async with app.run_test() as pilot:
        initial_size = app.font_size
        
        # Cycle through all 3 sizes
        for _ in range(3):
            await pilot.press("f")
        
        # Should be back to the initial size
        assert app.font_size == initial_size


@pytest.mark.asyncio
async def test_app_preferences_persisted(app):
    """Test that preferences are persisted across actions."""
    async with app.run_test() as pilot:
        # Set theme
        await pilot.press("t")
        saved_theme = app.preferences.get_theme()
        
        # Set layout
        await pilot.press("l")
        saved_layout = app.preferences.get_layout_density()
        
        # Set font size
        await pilot.press("f")
        saved_font = app.preferences.get_font_size()
        
        # Verify all are saved
        assert saved_theme == app.current_theme
        assert saved_layout == app.layout_density.value
        assert saved_font == app.font_size.value


@pytest.mark.asyncio
async def test_app_theme_applies_immediately(app):
    """Test that theme changes apply immediately without restart."""
    async with app.run_test() as pilot:
        initial_theme = app.current_theme
        
        # Cycle theme
        await pilot.press("t")
        
        # Theme should have changed immediately
        assert app.current_theme != initial_theme
        # CSS should be updated (check that app still works)
        assert app.stylesheet is not None


@pytest.mark.asyncio
async def test_app_font_size_applies_immediately(app):
    """Test that font size changes apply immediately without restart."""
    async with app.run_test() as pilot:
        initial_size = app.font_size
        
        # Cycle font size
        await pilot.press("f")
        
        # Font size should have changed immediately
        assert app.font_size != initial_size
        # CSS class should be applied
        font_classes = [cls for cls in app.classes if cls.startswith("font-")]
        assert len(font_classes) > 0
