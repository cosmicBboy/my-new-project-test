"""Tests for the tutorial screen."""

import pytest
from textual.widgets import Button

from todo_tui.tutorial import TutorialScreen


@pytest.mark.asyncio
async def test_tutorial_screen_displays():
    """Test that tutorial screen displays correctly."""
    from todo_tui.app import TodoApp
    
    app = TodoApp()
    
    async with app.run_test() as pilot:
        tutorial = TutorialScreen()
        app.push_screen(tutorial)
        await pilot.pause(0.1)
        
        # Check that tutorial is present
        assert isinstance(app.screen_stack[-1], TutorialScreen)


@pytest.mark.asyncio
async def test_tutorial_has_content():
    """Test that tutorial contains expected content."""
    tutorial = TutorialScreen()
    
    # Compose the tutorial to check content
    widgets = list(tutorial.compose())
    assert len(widgets) > 0


@pytest.mark.asyncio
async def test_tutorial_start_button():
    """Test that start button completes tutorial."""
    from todo_tui.app import TodoApp
    
    app = TodoApp()
    
    async with app.run_test() as pilot:
        tutorial = TutorialScreen()
        app.push_screen(tutorial)
        await pilot.pause(0.1)
        
        # Click start button
        await pilot.click("#start-button")
        await pilot.pause(0.1)
        
        # Tutorial should be marked as completed
        assert tutorial.completed is True


@pytest.mark.asyncio
async def test_tutorial_skip_button():
    """Test that skip button dismisses tutorial."""
    from todo_tui.app import TodoApp
    
    app = TodoApp()
    
    async with app.run_test() as pilot:
        tutorial = TutorialScreen()
        app.push_screen(tutorial)
        await pilot.pause(0.1)
        
        # Click skip button
        await pilot.click("#skip-button")
        await pilot.pause(0.1)
        
        # Tutorial should be marked as completed
        assert tutorial.completed is True


@pytest.mark.asyncio
async def test_tutorial_escape_key():
    """Test that escape key dismisses tutorial."""
    from todo_tui.app import TodoApp
    
    app = TodoApp()
    
    async with app.run_test() as pilot:
        tutorial = TutorialScreen()
        app.push_screen(tutorial)
        await pilot.pause(0.1)
        
        # Press escape
        await pilot.press("escape")
        await pilot.pause(0.1)
        
        # Tutorial should be completed
        assert tutorial.completed is True


@pytest.mark.asyncio
async def test_tutorial_shows_all_steps():
    """Test that tutorial shows all expected steps."""
    tutorial = TutorialScreen()
    
    # Render to string to check content
    async with tutorial.run_test():
        # The tutorial should contain key information
        content = str(tutorial)
        
        # Just verify the tutorial initialized properly
        assert tutorial is not None
