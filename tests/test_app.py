"""Tests for the Textual application."""

import pytest
from datetime import date, timedelta
from pathlib import Path
from textual.widgets import Input, ListView, Button

from todo_tui.app import TodoApp, KeyboardShortcutsScreen, TutorialScreen
from todo_tui.models import TodoItem
from todo_tui.keybindings import KeyBindingsManager


@pytest.fixture
def app():
    """Create a TodoApp instance for testing."""
    return TodoApp()


@pytest.fixture
def keybindings_manager(tmp_path):
    """Create a KeyBindingsManager with temporary config."""
    config_path = tmp_path / "test-keybindings.json"
    return KeyBindingsManager(config_path)


def test_app_initialization(app):
    """Test app initializes correctly."""
    assert app.storage is not None
    assert isinstance(app.todos, list)
    assert app.keybindings_manager is not None


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
    assert "question_mark" in binding_keys  # help/shortcuts
    assert "ctrl+t" in binding_keys  # tutorial


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


# ===== FEATURE 1: Contextual Help Overlay =====

@pytest.mark.asyncio
async def test_show_shortcuts_screen(app):
    """Test that keyboard shortcuts screen can be opened."""
    async with app.run_test() as pilot:
        # Initially, no shortcuts screen should be visible
        assert len(app.screen_stack) == 1
        
        # Press ? to open shortcuts
        await pilot.press("question_mark")
        
        # Shortcuts screen should now be pushed onto the stack
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen_stack[-1], KeyboardShortcutsScreen)


@pytest.mark.asyncio
async def test_shortcuts_screen_has_content(app):
    """Test that shortcuts screen displays content."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        
        # Get the shortcuts screen
        shortcuts_screen = app.screen_stack[-1]
        
        # Check for key elements
        title = shortcuts_screen.query_one("#shortcuts-title")
        assert "Keyboard Shortcuts" in title.renderable
        
        content = shortcuts_screen.query_one("#shortcuts-content")
        assert content is not None
        
        search = shortcuts_screen.query_one("#shortcuts-search")
        assert search is not None


@pytest.mark.asyncio
async def test_close_shortcuts_with_escape(app):
    """Test that shortcuts screen can be closed with ESC."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        assert len(app.screen_stack) == 2
        
        # Close with escape
        await pilot.press("escape")
        
        # Should return to main screen
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_close_shortcuts_with_question_mark(app):
    """Test that shortcuts screen can be closed with ? (toggle behavior)."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        assert len(app.screen_stack) == 2
        
        # Close with question mark again
        await pilot.press("question_mark")
        
        # Should return to main screen
        assert len(app.screen_stack) == 1


# ===== FEATURE 2: Searchable Shortcuts =====

@pytest.mark.asyncio
async def test_shortcuts_search_functionality(app):
    """Test searching for shortcuts in the help overlay."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        
        shortcuts_screen = app.screen_stack[-1]
        search_input = shortcuts_screen.query_one("#shortcuts-search", Input)
        
        # Type a search query
        search_input.value = "delete"
        await pilot.pause(0.1)
        
        # Check that content was updated with search results
        content_widget = shortcuts_screen.query_one("#shortcuts-content")
        content_text = str(content_widget.renderable)
        assert "delete" in content_text.lower() or "Search Results" in content_text


@pytest.mark.asyncio
async def test_shortcuts_search_no_results(app):
    """Test searching with no matching results."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        
        shortcuts_screen = app.screen_stack[-1]
        search_input = shortcuts_screen.query_one("#shortcuts-search", Input)
        
        # Type a query that won't match anything
        search_input.value = "xyznonexistent"
        await pilot.pause(0.1)
        
        # Check that no results message is shown
        content_widget = shortcuts_screen.query_one("#shortcuts-content")
        content_text = str(content_widget.renderable)
        assert "No shortcuts found" in content_text or "xyznonexistent" in content_text


@pytest.mark.asyncio
async def test_shortcuts_search_clear(app):
    """Test clearing search shows all shortcuts again."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        
        shortcuts_screen = app.screen_stack[-1]
        search_input = shortcuts_screen.query_one("#shortcuts-search", Input)
        
        # Search for something
        search_input.value = "toggle"
        await pilot.pause(0.1)
        
        # Clear search
        search_input.value = ""
        await pilot.pause(0.1)
        
        # Check that all categories are shown again
        content_widget = shortcuts_screen.query_one("#shortcuts-content")
        content_text = str(content_widget.renderable)
        assert "Navigation" in content_text or "Todo Management" in content_text


# ===== FEATURE 3: Customizable Key Bindings =====

def test_keybindings_manager_initialization(keybindings_manager):
    """Test that key bindings manager initializes with defaults."""
    assert keybindings_manager is not None
    assert len(keybindings_manager.bindings) > 0


def test_keybindings_get_binding(keybindings_manager):
    """Test getting a specific key binding."""
    binding = keybindings_manager.get_binding("toggle_todo")
    assert binding is not None
    assert binding.action == "toggle_todo"
    assert binding.key == "space"


def test_keybindings_set_binding(keybindings_manager):
    """Test setting a custom key binding."""
    keybindings_manager.set_binding("toggle_todo", "t")
    binding = keybindings_manager.get_binding("toggle_todo")
    assert binding.key == "t"


def test_keybindings_reset_to_defaults(keybindings_manager):
    """Test resetting key bindings to defaults."""
    # Modify a binding
    keybindings_manager.set_binding("toggle_todo", "x")
    assert keybindings_manager.get_key("toggle_todo") == "x"
    
    # Reset
    keybindings_manager.reset_to_defaults()
    assert keybindings_manager.get_key("toggle_todo") == "space"


def test_keybindings_search(keybindings_manager):
    """Test searching for key bindings."""
    results = keybindings_manager.search_bindings("toggle")
    assert len(results) > 0
    assert any("toggle" in r.action.lower() or "toggle" in r.description.lower() for r in results)


def test_keybindings_search_no_results(keybindings_manager):
    """Test searching with no matches."""
    results = keybindings_manager.search_bindings("xyznonexistent")
    assert len(results) == 0


def test_keybindings_get_by_category(keybindings_manager):
    """Test getting bindings organized by category."""
    categories = keybindings_manager.get_bindings_by_category()
    assert len(categories) > 0
    assert "Navigation" in categories or "Todo Management" in categories


def test_keybindings_persistence(tmp_path):
    """Test that key bindings are persisted to file."""
    config_path = tmp_path / "keybindings.json"
    
    # Create manager and set a custom binding
    manager1 = KeyBindingsManager(config_path)
    manager1.set_binding("toggle_todo", "t")
    
    # Create a new manager instance (should load from file)
    manager2 = KeyBindingsManager(config_path)
    assert manager2.get_key("toggle_todo") == "t"


@pytest.mark.asyncio
async def test_shortcuts_reset_button(app):
    """Test the reset to defaults button in shortcuts screen."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        
        shortcuts_screen = app.screen_stack[-1]
        
        # Modify a binding
        app.keybindings_manager.set_binding("toggle_todo", "x")
        
        # Find and click reset button
        reset_button = shortcuts_screen.query_one("#reset-bindings", Button)
        await reset_button.press()
        await pilot.pause(0.1)
        
        # Check that binding was reset
        assert app.keybindings_manager.get_key("toggle_todo") == "space"


# ===== FEATURE 4: Print-Friendly Cheat Sheet =====

@pytest.mark.asyncio
async def test_export_cheat_sheet(app, tmp_path):
    """Test exporting keyboard shortcuts to a text file."""
    async with app.run_test() as pilot:
        # Open shortcuts screen
        await pilot.press("question_mark")
        
        shortcuts_screen = app.screen_stack[-1]
        
        # Find and click export button
        export_button = shortcuts_screen.query_one("#export-cheat", Button)
        await export_button.press()
        await pilot.pause(0.1)
        
        # Check that file was created
        cheat_sheet_path = Path.home() / "todo-tui-shortcuts.txt"
        assert cheat_sheet_path.exists()
        
        # Check content
        content = cheat_sheet_path.read_text()
        assert "Keyboard Shortcuts Cheat Sheet" in content
        assert "Navigation" in content or "Todo Management" in content
        
        # Cleanup
        cheat_sheet_path.unlink()


def test_cheat_sheet_content_format(keybindings_manager, tmp_path):
    """Test that cheat sheet has proper format."""
    # This is a unit test for the export logic
    output_file = tmp_path / "test-shortcuts.txt"
    
    with open(output_file, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("TODO TUI - Keyboard Shortcuts Cheat Sheet\n")
        f.write("=" * 70 + "\n\n")
        
        categories = keybindings_manager.get_bindings_by_category()
        for category, bindings in sorted(categories.items()):
            f.write(f"\n{category}\n")
            f.write("-" * len(category) + "\n\n")
            for binding in bindings:
                key_display = binding.key.replace("_", " ").title()
                f.write(f"  {key_display:20} {binding.description}\n")
    
    content = output_file.read_text()
    assert "Keyboard Shortcuts Cheat Sheet" in content
    assert "=" * 70 in content
    assert len(content) > 100  # Should have substantial content


# ===== FEATURE 5: In-App Tutorial =====

@pytest.mark.asyncio
async def test_show_tutorial_screen(app):
    """Test that tutorial screen can be opened."""
    async with app.run_test() as pilot:
        # Open tutorial with keyboard shortcut
        await pilot.press("ctrl+t")
        
        # Tutorial screen should be pushed onto the stack
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen_stack[-1], TutorialScreen)


@pytest.mark.asyncio
async def test_tutorial_screen_has_content(app):
    """Test that tutorial screen displays content."""
    async with app.run_test() as pilot:
        # Open tutorial screen
        await pilot.press("ctrl+t")
        
        tutorial_screen = app.screen_stack[-1]
        
        # Check for key elements
        title = tutorial_screen.query_one("#tutorial-title")
        assert "Welcome" in title.renderable or "Tutorial" in title.renderable
        
        content = tutorial_screen.query_one("#tutorial-content")
        assert content is not None


@pytest.mark.asyncio
async def test_tutorial_close_button(app):
    """Test closing tutorial with button."""
    async with app.run_test() as pilot:
        # Open tutorial screen
        await pilot.press("ctrl+t")
        assert len(app.screen_stack) == 2
        
        tutorial_screen = app.screen_stack[-1]
        
        # Find and click done button
        done_button = tutorial_screen.query_one("#tutorial-done", Button)
        await done_button.press()
        await pilot.pause(0.1)
        
        # Should return to main screen
        assert len(app.screen_stack) == 1


@pytest.mark.asyncio
async def test_tutorial_escape_key(app):
    """Test closing tutorial with escape key."""
    async with app.run_test() as pilot:
        # Open tutorial screen
        await pilot.press("ctrl+t")
        assert len(app.screen_stack) == 2
        
        # Close with escape
        await pilot.press("escape")
        
        # Should return to main screen
        assert len(app.screen_stack) == 1


def test_tutorial_first_run_detection(app, tmp_path, monkeypatch):
    """Test that first run is detected correctly."""
    # Mock the home directory
    test_home = tmp_path / "home"
    test_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: test_home)
    
    # First run - marker file doesn't exist
    assert app._is_first_run() is True
    
    # Create marker file
    marker = test_home / ".todo-tui-tutorial-seen"
    marker.touch()
    
    # Not first run anymore
    assert app._is_first_run() is False


@pytest.mark.asyncio
async def test_tutorial_skip_button_creates_marker(app, tmp_path):
    """Test that skip button creates marker file."""
    async with app.run_test() as pilot:
        # Open tutorial with first_run=True
        tutorial_screen = TutorialScreen(is_first_run=True)
        app.push_screen(tutorial_screen)
        await pilot.pause(0.1)
        
        # Find and click skip button
        skip_button = tutorial_screen.query_one("#tutorial-skip", Button)
        await skip_button.press()
        await pilot.pause(0.1)
        
        # Check that marker file was created
        marker_file = Path.home() / ".todo-tui-tutorial-seen"
        assert marker_file.exists()
        
        # Cleanup
        marker_file.unlink()


@pytest.mark.asyncio
async def test_tutorial_content_sections(app):
    """Test that tutorial has all important sections."""
    async with app.run_test() as pilot:
        # Open tutorial screen
        await pilot.press("ctrl+t")
        
        tutorial_screen = app.screen_stack[-1]
        content_widget = tutorial_screen.query_one("#tutorial-content")
        
        # Get the text content
        static_widget = content_widget.query_one(Static)
        content = str(static_widget.renderable)
        
        # Check for essential sections
        assert "Adding" in content or "TODO" in content
        assert "Managing" in content or "shortcuts" in content.lower()
        assert "Tips" in content or "Pro" in content


# ===== Integration Tests =====

@pytest.mark.asyncio
async def test_full_workflow_with_shortcuts_reference(app):
    """Test complete workflow including shortcuts reference."""
    async with app.run_test() as pilot:
        # Add a todo
        input_widget = app.query_one("#todo-input", Input)
        input_widget.value = "Learn keyboard shortcuts"
        await pilot.press("enter")
        
        # Open shortcuts to learn how to toggle
        await pilot.press("question_mark")
        assert len(app.screen_stack) == 2
        
        # Search for toggle
        shortcuts_screen = app.screen_stack[-1]
        search_input = shortcuts_screen.query_one("#shortcuts-search", Input)
        search_input.value = "toggle"
        await pilot.pause(0.1)
        
        # Close shortcuts
        await pilot.press("escape")
        assert len(app.screen_stack) == 1
        
        # Use what we learned - toggle the todo
        list_view = app.query_one("#todo-list", ListView)
        list_view.index = 0
        await pilot.press("space")
        
        # Verify todo was completed
        assert app.todos[0].completed is True


@pytest.mark.asyncio
async def test_shortcuts_and_tutorial_integration(app):
    """Test using both shortcuts reference and tutorial."""
    async with app.run_test() as pilot:
        # Open tutorial
        await pilot.press("ctrl+t")
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen_stack[-1], TutorialScreen)
        
        # Close tutorial
        await pilot.press("escape")
        assert len(app.screen_stack) == 1
        
        # Open shortcuts
        await pilot.press("question_mark")
        assert len(app.screen_stack) == 2
        assert isinstance(app.screen_stack[-1], KeyboardShortcutsScreen)
        
        # Close shortcuts
        await pilot.press("escape")
        assert len(app.screen_stack) == 1
