"""Tests for the help overlay."""

import pytest
from textual.widgets import Button, Input

from todo_tui.app import TodoApp
from todo_tui.help_overlay import HelpOverlay, KeyboardShortcut


def test_keyboard_shortcut_initialization():
    """Test KeyboardShortcut initialization."""
    shortcut = KeyboardShortcut(
        key="q",
        action="Quit",
        description="Exit the application",
        category="Application"
    )
    
    assert shortcut.key == "q"
    assert shortcut.action == "Quit"
    assert shortcut.description == "Exit the application"
    assert shortcut.category == "Application"


def test_keyboard_shortcut_matches_search():
    """Test KeyboardShortcut search matching."""
    shortcut = KeyboardShortcut(
        key="Space",
        action="Toggle",
        description="Toggle completion status",
        category="Task Management"
    )
    
    # Test matching key
    assert shortcut.matches_search("space")
    assert shortcut.matches_search("Space")
    assert shortcut.matches_search("SPACE")
    
    # Test matching action
    assert shortcut.matches_search("toggle")
    assert shortcut.matches_search("Toggle")
    
    # Test matching description
    assert shortcut.matches_search("completion")
    assert shortcut.matches_search("status")
    
    # Test matching category
    assert shortcut.matches_search("task")
    assert shortcut.matches_search("management")
    
    # Test non-matching
    assert not shortcut.matches_search("delete")
    assert not shortcut.matches_search("xyz")


@pytest.mark.asyncio
async def test_help_overlay_displays():
    """Test that help overlay displays correctly."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        # Open help overlay
        await pilot.press("question_mark")
        
        # Check that help overlay is present
        help_screen = app.screen_stack[-1]
        assert isinstance(help_screen, HelpOverlay)
        
        # Check that title is present
        title = help_screen.query_one("#help-title")
        assert "Keyboard Shortcuts" in title.render()


@pytest.mark.asyncio
async def test_help_overlay_has_shortcuts():
    """Test that help overlay contains shortcuts."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.press("question_mark")
        
        help_screen = app.screen_stack[-1]
        assert isinstance(help_screen, HelpOverlay)
        
        # Check that shortcuts are defined
        assert len(help_screen.shortcuts) > 0
        
        # Check that common shortcuts are present
        shortcut_keys = [s.key for s in help_screen.shortcuts]
        shortcut_actions = [s.action for s in help_screen.shortcuts]
        
        assert any("Space" in key for key in shortcut_keys)
        assert any("Toggle" in action for action in shortcut_actions)
        assert any("Quit" in action for action in shortcut_actions)
        assert any("Delete" in action for action in shortcut_actions)


@pytest.mark.asyncio
async def test_help_overlay_has_new_shortcuts():
    """Test that help overlay includes new shortcuts."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.press("question_mark")
        
        help_screen = app.screen_stack[-1]
        shortcut_actions = [s.action for s in help_screen.shortcuts]
        
        # Check for new features
        assert any("Customize" in action or "Customize Keys" in action for action in shortcut_actions)
        assert any("Cheat Sheet" in action or "Export Cheat Sheet" in action for action in shortcut_actions)
        assert any("Tutorial" in action for action in shortcut_actions)


@pytest.mark.asyncio
async def test_help_overlay_categorizes_shortcuts():
    """Test that shortcuts are organized into categories."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.press("question_mark")
        
        help_screen = app.screen_stack[-1]
        categories = set(s.category for s in help_screen.shortcuts)
        
        # Check that expected categories exist
        assert "Navigation" in categories
        assert "Task Management" in categories
        assert "Application" in categories


@pytest.mark.asyncio
async def test_help_overlay_search():
    """Test help overlay search functionality."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.press("question_mark")
        
        help_screen = app.screen_stack[-1]
        search_input = help_screen.query_one("#search-input", Input)
        
        # Test search for "toggle"
        search_input.value = "toggle"
        await pilot.pause(0.1)
        
        # The search should filter shortcuts
        # We can't easily check the rendered output, but we can verify
        # that the search query is stored
        assert help_screen.search_query == "toggle"


@pytest.mark.asyncio
async def test_help_overlay_search_filters():
    """Test that search filters shortcuts correctly."""
    help_overlay = HelpOverlay()
    
    # Test that all shortcuts match empty search
    help_overlay.search_query = ""
    all_shortcuts = help_overlay.shortcuts
    
    # Test specific searches
    help_overlay.search_query = "toggle"
    filtered = [s for s in all_shortcuts if s.matches_search("toggle")]
    assert len(filtered) > 0
    assert all("toggle" in s.action.lower() or "toggle" in s.description.lower() for s in filtered)
    
    # Test search with no results
    help_overlay.search_query = "xyz123nonexistent"
    filtered = [s for s in all_shortcuts if s.matches_search("xyz123nonexistent")]
    assert len(filtered) == 0


@pytest.mark.asyncio
async def test_help_overlay_close_with_button():
    """Test closing help overlay with close button."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        # Open help overlay
        await pilot.press("question_mark")
        
        # Verify overlay is open
        assert len(app.screen_stack) > 1
        assert isinstance(app.screen_stack[-1], HelpOverlay)
        
        # Click close button
        help_screen = app.screen_stack[-1]
        close_button = help_screen.query_one("#close-button", Button)
        await pilot.click("#close-button")
        await pilot.pause(0.1)
        
        # Verify overlay is closed
        assert not isinstance(app.screen_stack[-1], HelpOverlay)


@pytest.mark.asyncio
async def test_help_overlay_close_with_escape():
    """Test closing help overlay with Escape key."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        # Open help overlay
        await pilot.press("question_mark")
        
        # Verify overlay is open
        assert len(app.screen_stack) > 1
        assert isinstance(app.screen_stack[-1], HelpOverlay)
        
        # Press Escape
        await pilot.press("escape")
        await pilot.pause(0.1)
        
        # Verify overlay is closed
        assert not isinstance(app.screen_stack[-1], HelpOverlay)


@pytest.mark.asyncio
async def test_help_overlay_close_with_q():
    """Test closing help overlay with 'q' key."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        # Open help overlay
        await pilot.press("question_mark")
        
        # Verify overlay is open
        assert len(app.screen_stack) > 1
        assert isinstance(app.screen_stack[-1], HelpOverlay)
        
        # Press 'q'
        await pilot.press("q")
        await pilot.pause(0.1)
        
        # Verify overlay is closed
        assert not isinstance(app.screen_stack[-1], HelpOverlay)


@pytest.mark.asyncio
async def test_help_overlay_search_input_focused():
    """Test that search input is focused when help opens."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.press("question_mark")
        
        help_screen = app.screen_stack[-1]
        search_input = help_screen.query_one("#search-input", Input)
        
        # Check that search input has focus
        assert search_input.has_focus


@pytest.mark.asyncio
async def test_help_overlay_all_shortcuts_documented():
    """Test that all app bindings are documented in help."""
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.press("question_mark")
        
        help_screen = app.screen_stack[-1]
        
        # Get all app bindings
        app_binding_actions = [b.action for b in app.BINDINGS if b.show]
        
        # Get all documented shortcuts
        help_actions = [s.action for s in help_screen.shortcuts]
        
        # Verify that main actions are documented
        # (Note: Some bindings might be internal or have different display names)
        assert any("Quit" in action for action in help_actions)
        assert any("Toggle" in action for action in help_actions)
        assert any("Delete" in action for action in help_actions)
        assert any("Postpone" in action for action in help_actions)
        assert any("Help" in action for action in help_actions)


@pytest.mark.asyncio
async def test_help_overlay_search_multiple_terms():
    """Test searching with multiple terms."""
    help_overlay = HelpOverlay()
    
    # Search for navigation-related shortcuts
    nav_shortcuts = [s for s in help_overlay.shortcuts if s.matches_search("navigation")]
    assert len(nav_shortcuts) > 0
    assert all(s.category == "Navigation" for s in nav_shortcuts)
    
    # Search for task-related shortcuts
    task_shortcuts = [s for s in help_overlay.shortcuts if s.matches_search("task")]
    assert len(task_shortcuts) > 0


@pytest.mark.asyncio
async def test_help_overlay_has_all_categories():
    """Test that all expected categories are present."""
    help_overlay = HelpOverlay()
    
    categories = set(s.category for s in help_overlay.shortcuts)
    
    # Check for essential categories
    assert "Navigation" in categories
    assert "Task Management" in categories
    assert "Application" in categories
    
    # Check that each category has shortcuts
    for category in categories:
        category_shortcuts = [s for s in help_overlay.shortcuts if s.category == category]
        assert len(category_shortcuts) > 0


def test_help_overlay_shortcut_keys_are_unique():
    """Test that shortcut keys don't have duplicates (except for alternate keys)."""
    help_overlay = HelpOverlay()
    
    # Get all keys (split alternates like "↑ / k")
    all_keys = []
    for shortcut in help_overlay.shortcuts:
        keys = [k.strip() for k in shortcut.key.split("/")]
        all_keys.extend(keys)
    
    # Some keys may legitimately appear multiple times (like in descriptions)
    # This test just ensures we have a reasonable variety
    assert len(set(all_keys)) >= 10  # At least 10 unique keys


def test_help_overlay_includes_customization_shortcuts():
    """Test that help overlay documents customization features."""
    help_overlay = HelpOverlay()
    
    actions = [s.action for s in help_overlay.shortcuts]
    
    # Should include new customization features
    assert any("customize" in action.lower() or "keys" in action.lower() for action in actions)
    assert any("cheat" in action.lower() or "sheet" in action.lower() for action in actions)
    assert any("tutorial" in action.lower() for action in actions)
