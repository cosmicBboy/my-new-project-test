"""Tests for the Textual application."""

import pytest
from datetime import date, timedelta
from textual.widgets import Input, ListView

from todo_tui.app import TodoApp, DescriptionScreen, DescriptionViewScreen
from todo_tui.models import TodoItem


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    return TodoApp()


def test_app_initialization(app):
    """Test app initializes correctly."""
    assert app.storage is not None
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
    assert "v" in binding_keys  # view description
    assert "n" in binding_keys  # edit description


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
async def test_description_screen_creation():
    """Test that description screen can be created."""
    todo = TodoItem(title="Test task", description="Initial description")
    screen = DescriptionScreen(todo)
    
    assert screen.todo == todo


@pytest.mark.asyncio
async def test_description_screen_displays_existing_description():
    """Test that description screen shows existing description."""
    todo = TodoItem(title="Test task", description="Existing description")
    screen = DescriptionScreen(todo)
    
    app = TodoApp()
    async with app.run_test():
        app.push_screen(screen)
        await app._animator.wait_for_idle()
        
        # Verify textarea contains existing description
        from textual.widgets import TextArea
        textarea = screen.query_one("#description-textarea", TextArea)
        assert textarea.text == "Existing description"


@pytest.mark.asyncio
async def test_description_screen_handles_empty_description():
    """Test that description screen handles todos without description."""
    todo = TodoItem(title="Test task")
    screen = DescriptionScreen(todo)
    
    app = TodoApp()
    async with app.run_test():
        app.push_screen(screen)
        await app._animator.wait_for_idle()
        
        # Verify textarea is empty
        from textual.widgets import TextArea
        textarea = screen.query_one("#description-textarea", TextArea)
        assert textarea.text == ""


@pytest.mark.asyncio
async def test_description_view_screen_creation():
    """Test that description view screen can be created."""
    todo = TodoItem(title="Test task", description="View this description")
    screen = DescriptionViewScreen(todo)
    
    assert screen.todo == todo


@pytest.mark.asyncio
async def test_description_view_screen_renders_markdown_headings():
    """Test that description view renders markdown headings."""
    description = "# Heading 1\n## Heading 2\n### Heading 3"
    todo = TodoItem(title="Test task", description=description)
    screen = DescriptionViewScreen(todo)
    
    rendered = screen._render_markdown()
    
    # Check that headings are formatted
    assert "[bold #ff006e]Heading 1[/]" in rendered
    assert "[bold #ff006e]Heading 2[/]" in rendered
    assert "[bold #ff006e]Heading 3[/]" in rendered


@pytest.mark.asyncio
async def test_description_view_screen_renders_lists():
    """Test that description view renders lists with color."""
    description = "- Item 1\n- Item 2\n* Item 3"
    todo = TodoItem(title="Test task", description=description)
    screen = DescriptionViewScreen(todo)
    
    rendered = screen._render_markdown()
    
    # Check that list items are colored
    assert "[#ffbe0b]- Item 1[/]" in rendered
    assert "[#ffbe0b]- Item 2[/]" in rendered
    assert "[#ffbe0b]* Item 3[/]" in rendered


@pytest.mark.asyncio
async def test_description_view_screen_renders_links():
    """Test that description view renders links as clickable."""
    description = "Check this: https://github.com/example/repo"
    todo = TodoItem(title="Test task", description=description)
    screen = DescriptionViewScreen(todo)
    
    rendered = screen._render_markdown()
    
    # Check that links are formatted
    assert "https://github.com/example/repo" in rendered
    assert "[link=" in rendered
    assert "[#3a86ff underline]" in rendered


@pytest.mark.asyncio
async def test_description_view_screen_renders_code():
    """Test that description view renders inline code."""
    description = "Run `npm install` to install dependencies"
    todo = TodoItem(title="Test task", description=description)
    screen = DescriptionViewScreen(todo)
    
    rendered = screen._render_markdown()
    
    # Check that code is formatted
    assert "[#06ffa5 italic]" in rendered


@pytest.mark.asyncio
async def test_description_view_screen_handles_empty_description():
    """Test that description view handles empty descriptions."""
    todo = TodoItem(title="Test task")
    screen = DescriptionViewScreen(todo)
    
    rendered = screen._render_markdown()
    
    # Should show a message about no description
    assert "No description" in rendered or "dim" in rendered.lower()


@pytest.mark.asyncio
async def test_todo_item_with_description_shows_indicator():
    """Test that todos with descriptions show [+] indicator."""
    todo = TodoItem(title="Test task", description="Has description")
    
    assert str(todo) == "[ ] Test task [+]"


@pytest.mark.asyncio
async def test_todo_item_without_description_no_indicator():
    """Test that todos without descriptions don't show [+] indicator."""
    todo = TodoItem(title="Test task")
    
    assert str(todo) == "[ ] Test task"


@pytest.mark.asyncio
async def test_storage_persists_description():
    """Test that descriptions are saved and loaded correctly."""
    from todo_tui.storage import TodoStorage
    import tempfile
    from pathlib import Path
    
    # Use a temporary file for storage
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    
    try:
        storage = TodoStorage(temp_path)
        
        # Create and save a todo with description
        todo = TodoItem(title="Test task", description="My detailed notes")
        storage.add(todo)
        
        # Load todos and verify description persists
        loaded_todos = storage.get_all()
        assert len(loaded_todos) == 1
        assert loaded_todos[0].description == "My detailed notes"
        assert loaded_todos[0].has_description() is True
    finally:
        # Clean up
        temp_path.unlink()


@pytest.mark.asyncio
async def test_storage_handles_multiline_description():
    """Test that multi-line descriptions are saved and loaded correctly."""
    from todo_tui.storage import TodoStorage
    import tempfile
    from pathlib import Path
    
    description = """Line 1
Line 2
Line 3"""
    
    # Use a temporary file for storage
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    
    try:
        storage = TodoStorage(temp_path)
        
        # Create and save a todo with multi-line description
        todo = TodoItem(title="Test task", description=description)
        storage.add(todo)
        
        # Load todos and verify multi-line description persists
        loaded_todos = storage.get_all()
        assert len(loaded_todos) == 1
        assert loaded_todos[0].description == description
        assert "\n" in loaded_todos[0].description
    finally:
        # Clean up
        temp_path.unlink()
