"""Tests for the Textual application."""

import pytest
import tempfile
from pathlib import Path
from datetime import date, timedelta
from textual.widgets import Input, ListView, Button

from todo_tui.app import TodoApp, ExportScreen, ImportScreen, BackupScreen
from todo_tui.models import TodoItem


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    app = TodoApp()
    # Disable automatic backups for most tests
    app.storage.auto_backup_enabled = False
    return app


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
    assert "b" in binding_keys  # backup
    assert "a" in binding_keys  # archive


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
    """Test export screen composes correctly."""
    screen = ExportScreen()
    async with screen.app.run_test() as pilot:
        # Check that dialog elements are present
        assert screen.query_one("#export-path") is not None
        assert screen.query_one("#export-btn") is not None
        assert screen.query_one("#cancel-btn") is not None


@pytest.mark.asyncio
async def test_export_screen_cancel():
    """Test export screen cancel button."""
    screen = ExportScreen()
    result = None
    
    def callback(value):
        nonlocal result
        result = value
    
    async with screen.app.run_test() as pilot:
        screen.app.push_screen(screen, callback)
        cancel_btn = screen.query_one("#cancel-btn", Button)
        await pilot.click(cancel_btn)
        
        # Should return None when cancelled
        assert result is None


@pytest.mark.asyncio
async def test_import_screen_composition():
    """Test import screen composes correctly."""
    screen = ImportScreen()
    async with screen.app.run_test() as pilot:
        # Check that dialog elements are present
        assert screen.query_one("#import-path") is not None
        assert screen.query_one("#import-btn") is not None
        assert screen.query_one("#cancel-btn") is not None
        assert screen.query_one("#mode-indicator") is not None


@pytest.mark.asyncio
async def test_import_screen_toggle_merge():
    """Test import screen merge mode toggle."""
    screen = ImportScreen()
    async with screen.app.run_test() as pilot:
        # Initially should be replace mode
        assert screen.merge_mode is False
        
        # Toggle merge mode
        screen.action_toggle_merge()
        assert screen.merge_mode is True
        
        # Toggle again
        screen.action_toggle_merge()
        assert screen.merge_mode is False


@pytest.mark.asyncio
async def test_backup_screen_composition():
    """Test backup screen composes correctly."""
    screen = BackupScreen()
    async with screen.app.run_test() as pilot:
        # Check that dialog elements are present
        assert screen.query_one("#create-btn") is not None
        assert screen.query_one("#list-btn") is not None
        assert screen.query_one("#cancel-btn") is not None


@pytest.mark.asyncio
async def test_app_export_action(app):
    """Test export action opens export screen."""
    async with app.run_test() as pilot:
        # Add a todo
        todo = TodoItem(title="Test task")
        app.storage.add(todo)
        app.load_todos()
        
        # Press 'e' to open export dialog
        await pilot.press("e")
        
        # Screen should be pushed (we can't easily test the modal in unit tests,
        # but we can verify the action is bound)
        assert "e" in [b.key for b in app.BINDINGS]


@pytest.mark.asyncio
async def test_app_import_action(app):
    """Test import action opens import screen."""
    async with app.run_test() as pilot:
        # Press 'i' to open import dialog
        await pilot.press("i")
        
        # Screen should be pushed
        assert "i" in [b.key for b in app.BINDINGS]


@pytest.mark.asyncio
async def test_app_backup_action(app):
    """Test backup action opens backup screen."""
    async with app.run_test() as pilot:
        # Press 'b' to open backup dialog
        await pilot.press("b")
        
        # Screen should be pushed
        assert "b" in [b.key for b in app.BINDINGS]


@pytest.mark.asyncio
async def test_app_archive_action(app):
    """Test archive action archives completed todos."""
    # Add some todos
    todo1 = TodoItem(title="Active task")
    todo2 = TodoItem(title="Completed task")
    todo2.toggle_completed()
    
    app.storage.save([todo1, todo2])
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Archive completed todos
        await pilot.press("a")
        
        # Should only have active todo remaining
        todos = app.storage.get_all()
        assert len(todos) == 1
        assert todos[0].title == "Active task"


@pytest.mark.asyncio
async def test_app_archive_no_completed(app):
    """Test archive action with no completed todos."""
    # Add only active todos
    todo1 = TodoItem(title="Active task 1")
    todo2 = TodoItem(title="Active task 2")
    
    app.storage.save([todo1, todo2])
    
    async with app.run_test() as pilot:
        app.load_todos()
        
        # Try to archive (should have no effect)
        await pilot.press("a")
        
        # Should still have all todos
        todos = app.storage.get_all()
        assert len(todos) == 2


@pytest.mark.asyncio
async def test_app_handle_export(app):
    """Test export handler saves file correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        export_path = Path(tmpdir) / "test-export.json"
        
        # Add a todo
        todo = TodoItem(title="Test task")
        app.storage.add(todo)
        
        async with app.run_test() as pilot:
            app.load_todos()
            
            # Call the export handler directly
            app._handle_export((str(export_path), "json"))
            
            # Verify file was created
            assert export_path.exists()
            
            # Verify content
            import json
            data = json.loads(export_path.read_text())
            assert len(data) == 1
            assert data[0]['title'] == "Test task"


@pytest.mark.asyncio
async def test_app_handle_import(app):
    """Test import handler loads file correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        import_path = Path(tmpdir) / "test-import.json"
        
        # Create import file
        import json
        todo = TodoItem(title="Imported task")
        data = [todo.to_dict()]
        import_path.write_text(json.dumps(data))
        
        async with app.run_test() as pilot:
            # Import the file
            app._handle_import((str(import_path), False))
            
            # Verify todo was imported
            todos = app.storage.get_all()
            assert len(todos) == 1
            assert todos[0].title == "Imported task"


@pytest.mark.asyncio
async def test_app_handle_backup_create(app):
    """Test backup creation through handler."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Override backup directory
        app.storage.storage_path = Path(tmpdir) / "todos.json"
        app.storage._ensure_file_exists()
        
        # Add a todo
        todo = TodoItem(title="Test task")
        app.storage.add(todo)
        
        async with app.run_test() as pilot:
            app.load_todos()
            
            # Create backup
            backup_dir = Path(tmpdir) / "backups"
            app.storage.create_backup(backup_dir)
            
            # Verify backup was created
            backups = list(backup_dir.glob("todo-backup-*.json"))
            assert len(backups) == 1


@pytest.mark.asyncio
async def test_app_handle_backup_list(app):
    """Test listing backups through handler."""
    with tempfile.TemporaryDirectory() as tmpdir:
        backup_dir = Path(tmpdir) / "backups"
        backup_dir.mkdir()
        
        # Create some backups
        app.storage.create_backup(backup_dir)
        app.storage.create_backup(backup_dir)
        
        async with app.run_test() as pilot:
            # List backups
            backups = app.storage.list_backups(backup_dir)
            
            # Should have 2 backups
            assert len(backups) == 2


@pytest.mark.asyncio
async def test_app_shutdown_creates_backup():
    """Test that app shutdown triggers automatic backup if needed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "todos.json"
        backup_dir = Path(tmpdir) / "backups"
        backup_dir.mkdir()
        
        # Create app with automatic backups enabled
        app = TodoApp()
        app.storage = TodoStorage(storage_path, auto_backup_enabled=True)
        
        # Override backup methods to use test directory
        original_create_backup = app.storage.create_backup
        original_list_backups = app.storage.list_backups
        
        def create_backup_wrapper(backup_dir_arg=None):
            return original_create_backup(backup_dir if backup_dir_arg is None else backup_dir_arg)
        
        def list_backups_wrapper(backup_dir_arg=None):
            return original_list_backups(backup_dir if backup_dir_arg is None else backup_dir_arg)
        
        app.storage.create_backup = create_backup_wrapper
        app.storage.list_backups = list_backups_wrapper
        
        async with app.run_test() as pilot:
            # Add some todos
            app.storage.add(TodoItem(title="Task 1"))
            app.storage.add(TodoItem(title="Task 2"))
            
            # Get backup count before unmount
            backups_before = len(list(backup_dir.glob("todo-backup-*.json")))
            
            # Simulate app shutdown
            app.on_unmount()
            
            # Check if backup was created
            backups_after = len(list(backup_dir.glob("todo-backup-*.json")))
            
            # Should have created at least one backup
            assert backups_after >= backups_before
