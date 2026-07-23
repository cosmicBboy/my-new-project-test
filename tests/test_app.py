"""Tests for the Textual application."""

import pytest
import tempfile
from pathlib import Path
from datetime import date, timedelta
from textual.widgets import Input, ListView

from todo_tui.app import TodoApp, ExportScreen, ImportScreen
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
    assert "e" in binding_keys  # export
    assert "i" in binding_keys  # import


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
async def test_export_screen_composition():
    """Test ExportScreen modal composes correctly."""
    screen = ExportScreen()
    async with screen.run_test() as pilot:
        # Check that input widget is present
        input_widget = screen.query_one("#export-filename", Input)
        assert input_widget is not None


@pytest.mark.asyncio
async def test_export_screen_cancel():
    """Test ExportScreen can be cancelled with escape."""
    screen = ExportScreen()
    result = None
    
    async def capture_result(r):
        nonlocal result
        result = r
    
    async with screen.run_test() as pilot:
        screen.dismiss = capture_result
        await pilot.press("escape")
        assert result is None


@pytest.mark.asyncio
async def test_export_screen_json_selection():
    """Test ExportScreen JSON format selection."""
    screen = ExportScreen()
    result = None
    
    async def capture_result(r):
        nonlocal result
        result = r
    
    async with screen.run_test() as pilot:
        screen.dismiss = capture_result
        input_widget = screen.query_one("#export-filename", Input)
        input_widget.value = "test-export"
        await pilot.press("j")
        assert result == ("json", "test-export")


@pytest.mark.asyncio
async def test_export_screen_markdown_selection():
    """Test ExportScreen Markdown format selection."""
    screen = ExportScreen()
    result = None
    
    async def capture_result(r):
        nonlocal result
        result = r
    
    async with screen.run_test() as pilot:
        screen.dismiss = capture_result
        input_widget = screen.query_one("#export-filename", Input)
        input_widget.value = "test-export"
        await pilot.press("m")
        assert result == ("markdown", "test-export")


@pytest.mark.asyncio
async def test_import_screen_composition():
    """Test ImportScreen modal composes correctly."""
    screen = ImportScreen()
    async with screen.run_test() as pilot:
        # Check that input widget is present
        input_widget = screen.query_one("#import-filepath", Input)
        assert input_widget is not None


@pytest.mark.asyncio
async def test_import_screen_cancel():
    """Test ImportScreen can be cancelled with escape."""
    screen = ImportScreen()
    result = None
    
    async def capture_result(r):
        nonlocal result
        result = r
    
    async with screen.run_test() as pilot:
        screen.dismiss = capture_result
        await pilot.press("escape")
        assert result is None


@pytest.mark.asyncio
async def test_import_screen_append_selection():
    """Test ImportScreen append mode selection."""
    screen = ImportScreen()
    result = None
    
    async def capture_result(r):
        nonlocal result
        result = r
    
    async with screen.run_test() as pilot:
        screen.dismiss = capture_result
        input_widget = screen.query_one("#import-filepath", Input)
        input_widget.value = "~/test.json"
        await pilot.press("a")
        assert result == ("append", "~/test.json")


@pytest.mark.asyncio
async def test_import_screen_replace_selection():
    """Test ImportScreen replace mode selection."""
    screen = ImportScreen()
    result = None
    
    async def capture_result(r):
        nonlocal result
        result = r
    
    async with screen.run_test() as pilot:
        screen.dismiss = capture_result
        input_widget = screen.query_one("#import-filepath", Input)
        input_widget.value = "~/test.json"
        await pilot.press("r")
        assert result == ("replace", "~/test.json")


@pytest.mark.asyncio
async def test_app_export_json_integration(app):
    """Test complete export workflow with JSON format."""
    # Add some test todos
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    app.storage.save([todo1, todo2])
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Trigger export
        await pilot.press("e")
        
        # Wait for modal to appear
        await pilot.pause()
        
        # Fill in filename and select JSON
        input_widget = app.screen.query_one("#export-filename", Input)
        input_widget.value = "test-export"
        await pilot.press("j")
        
        # Check that export file was created
        export_path = Path.home() / "todo-exports" / "test-export.json"
        try:
            assert export_path.exists()
            
            # Verify content
            import json
            data = json.loads(export_path.read_text())
            assert len(data) == 2
            assert data[0]["title"] == "Task 1"
            assert data[1]["title"] == "Task 2"
        finally:
            # Cleanup
            if export_path.exists():
                export_path.unlink()


@pytest.mark.asyncio
async def test_app_export_markdown_integration(app):
    """Test complete export workflow with Markdown format."""
    # Add some test todos
    todo1 = TodoItem(title="Task 1")
    todo2 = TodoItem(title="Task 2")
    todo2.toggle_completed()
    app.storage.save([todo1, todo2])
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Trigger export
        await pilot.press("e")
        
        # Wait for modal to appear
        await pilot.pause()
        
        # Fill in filename and select Markdown
        input_widget = app.screen.query_one("#export-filename", Input)
        input_widget.value = "test-export-md"
        await pilot.press("m")
        
        # Check that export file was created
        export_path = Path.home() / "todo-exports" / "test-export-md.md"
        try:
            assert export_path.exists()
            
            # Verify content
            content = export_path.read_text()
            assert "# TODO List" in content
            assert "Task 1" in content
            assert "Task 2" in content
        finally:
            # Cleanup
            if export_path.exists():
                export_path.unlink()


@pytest.mark.asyncio
async def test_app_import_json_integration(app):
    """Test complete import workflow."""
    # Create a test import file
    import_todos = [
        TodoItem(title="Imported task 1"),
        TodoItem(title="Imported task 2"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        import json
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        async with app.run_test() as pilot:
            # Trigger import
            await pilot.press("i")
            
            # Wait for modal to appear
            await pilot.pause()
            
            # Fill in filepath and select append mode
            input_widget = app.screen.query_one("#import-filepath", Input)
            input_widget.value = str(import_path)
            await pilot.press("a")
            
            # Wait for import to complete
            await pilot.pause()
            
            # Check that todos were imported
            assert len(app.todos) == 2
            assert app.todos[0].title == "Imported task 1"
            assert app.todos[1].title == "Imported task 2"
    finally:
        # Cleanup
        if import_path.exists():
            import_path.unlink()


@pytest.mark.asyncio
async def test_app_import_replace_mode(app):
    """Test import with replace mode."""
    # Add existing todos
    existing = TodoItem(title="Existing task")
    app.storage.save([existing])
    
    # Create a test import file
    import_todos = [
        TodoItem(title="New task"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        import_path = Path(f.name)
        import json
        data = [todo.to_dict() for todo in import_todos]
        f.write(json.dumps(data, indent=2))
    
    try:
        async with app.run_test() as pilot:
            app.load_todos()
            
            # Verify existing todo
            assert len(app.todos) == 1
            assert app.todos[0].title == "Existing task"
            
            # Trigger import
            await pilot.press("i")
            
            # Wait for modal to appear
            await pilot.pause()
            
            # Fill in filepath and select replace mode
            input_widget = app.screen.query_one("#import-filepath", Input)
            input_widget.value = str(import_path)
            await pilot.press("r")
            
            # Wait for import to complete
            await pilot.pause()
            
            # Check that existing todos were replaced
            assert len(app.todos) == 1
            assert app.todos[0].title == "New task"
    finally:
        # Cleanup
        if import_path.exists():
            import_path.unlink()
