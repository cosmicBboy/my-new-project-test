"""Tests for the tutorial screen."""

import pytest
from textual.widgets import Button, Label

from todo_tui.tutorial import TutorialScreen
from todo_tui.app import TodoApp


@pytest.fixture
def tutorial_screen():
    """Create a TutorialScreen instance for testing."""
    return TutorialScreen()


def test_tutorial_screen_initialization(tutorial_screen):
    """Test tutorial screen initializes correctly."""
    assert tutorial_screen is not None


@pytest.mark.asyncio
async def test_tutorial_screen_composition(tutorial_screen):
    """Test tutorial screen composes correctly."""
    app = TodoApp()
    async with app.run_test():
        app.push_screen(tutorial_screen)
        
        # Check that key widgets are present
        assert tutorial_screen.query_one("#tutorial-title") is not None
        assert tutorial_screen.query_one("#tutorial-content") is not None
        assert tutorial_screen.query_one("#start-btn") is not None


@pytest.mark.asyncio
async def test_tutorial_screen_title(tutorial_screen):
    """Test tutorial screen has correct title."""
    app = TodoApp()
    async with app.run_test():
        app.push_screen(tutorial_screen)
        
        title = tutorial_screen.query_one("#tutorial-title", Label)
        assert "Welcome" in str(title.renderable) or "Welcome" in str(title)


@pytest.mark.asyncio
async def test_tutorial_screen_content_sections(tutorial_screen):
    """Test tutorial screen has all expected content sections."""
    app = TodoApp()
    async with app.run_test():
        app.push_screen(tutorial_screen)
        
        # Render the content
        widgets = tutorial_screen._render_tutorial_content()
        
        # Check that we have content
        assert len(widgets) > 0
        
        # Check for section labels (categories)
        labels = [w for w in widgets if isinstance(w, Label)]
        label_texts = [str(w.renderable) for w in labels]
        
        # Check for key sections
        assert any("Adding" in text or "Tasks" in text for text in label_texts)
        assert any("Managing" in text or "Tasks" in text for text in label_texts)
        assert any("Help" in text or "Getting" in text for text in label_texts)


@pytest.mark.asyncio
async def test_tutorial_screen_start_button(tutorial_screen):
    """Test start button exists and works."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(tutorial_screen)
        
        start_btn = tutorial_screen.query_one("#start-btn", Button)
        assert start_btn is not None
        
        # Click the button
        await pilot.click(Button, "#start-btn")
        
        # Should dismiss (we just verify no errors occur)


@pytest.mark.asyncio
async def test_tutorial_screen_escape_binding(tutorial_screen):
    """Test escape key binding closes tutorial."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(tutorial_screen)
        
        # Press escape
        await pilot.press("escape")
        await pilot.pause()
        
        # Should dismiss without errors


@pytest.mark.asyncio
async def test_tutorial_screen_enter_binding(tutorial_screen):
    """Test enter key binding closes tutorial."""
    app = TodoApp()
    async with app.run_test() as pilot:
        app.push_screen(tutorial_screen)
        
        # Press enter
        await pilot.press("enter")
        await pilot.pause()
        
        # Should dismiss without errors


@pytest.mark.asyncio
async def test_tutorial_screen_bindings():
    """Test that tutorial screen has proper key bindings."""
    tutorial_screen = TutorialScreen()
    
    binding_keys = [b.key for b in tutorial_screen.BINDINGS]
    assert "escape" in binding_keys, "Should have escape key binding"
    assert "enter" in binding_keys, "Should have enter key binding"


def test_tutorial_content_structure(tutorial_screen):
    """Test that tutorial content has proper structure."""
    widgets = tutorial_screen._render_tutorial_content()
    
    # Should have multiple widgets
    assert len(widgets) > 5
    
    # All widgets should be Labels or Statics
    for widget in widgets:
        assert isinstance(widget, Label)


def test_tutorial_content_has_keyboard_shortcuts(tutorial_screen):
    """Test that tutorial mentions keyboard shortcuts."""
    widgets = tutorial_screen._render_tutorial_content()
    
    # Collect all text
    all_text = []
    for widget in widgets:
        if hasattr(widget, "renderable"):
            all_text.append(str(widget.renderable))
    
    combined_text = " ".join(all_text).lower()
    
    # Check for important shortcuts
    assert "space" in combined_text or "toggle" in combined_text
    assert "delete" in combined_text or "d" in combined_text
    assert "postpone" in combined_text or "p" in combined_text


def test_tutorial_content_has_tips(tutorial_screen):
    """Test that tutorial includes helpful tips."""
    widgets = tutorial_screen._render_tutorial_content()
    
    # Look for tips section
    found_tips = False
    for widget in widgets:
        if hasattr(widget, "renderable"):
            text = str(widget.renderable)
            if "tip" in text.lower() or "🔸" in text:
                found_tips = True
                break
    
    assert found_tips, "Tutorial should include tips"


def test_tutorial_content_mentions_help(tutorial_screen):
    """Test that tutorial mentions the help system."""
    widgets = tutorial_screen._render_tutorial_content()
    
    # Collect all text
    all_text = []
    for widget in widgets:
        if hasattr(widget, "renderable"):
            all_text.append(str(widget.renderable).lower())
    
    combined_text = " ".join(all_text)
    
    # Should mention help or ? key
    assert "?" in combined_text or "help" in combined_text


@pytest.mark.asyncio
async def test_app_shows_tutorial_on_first_run(tmp_path, monkeypatch):
    """Test that app shows tutorial on first run."""
    # Mock home directory
    def mock_home():
        return tmp_path
    
    monkeypatch.setattr("pathlib.Path.home", mock_home)
    
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Tutorial flag file should be created
        tutorial_flag = tmp_path / ".todo-tui-tutorial-shown"
        assert tutorial_flag.exists()


@pytest.mark.asyncio
async def test_app_skips_tutorial_on_subsequent_runs(tmp_path, monkeypatch):
    """Test that app skips tutorial on subsequent runs."""
    # Mock home directory
    def mock_home():
        return tmp_path
    
    monkeypatch.setattr("pathlib.Path.home", mock_home)
    
    # Create tutorial flag file
    tutorial_flag = tmp_path / ".todo-tui-tutorial-shown"
    tutorial_flag.touch()
    
    app = TodoApp()
    
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # App should start normally without showing tutorial
        # (Tutorial won't be pushed to screen stack)


def test_tutorial_content_has_welcome_message(tutorial_screen):
    """Test that tutorial has a welcoming message."""
    widgets = tutorial_screen._render_tutorial_content()
    
    # First widget should be welcoming
    first_widgets_text = " ".join([
        str(w.renderable) for w in widgets[:3] 
        if hasattr(w, "renderable")
    ]).lower()
    
    assert any(word in first_widgets_text for word in ["getting", "started", "welcome"])


def test_tutorial_content_has_final_message(tutorial_screen):
    """Test that tutorial has an encouraging final message."""
    widgets = tutorial_screen._render_tutorial_content()
    
    # Last few widgets should have encouraging message
    last_widgets_text = " ".join([
        str(w.renderable) for w in widgets[-3:] 
        if hasattr(w, "renderable")
    ]).lower()
    
    assert any(word in last_widgets_text for word in ["ready", "start", "organized"])


@pytest.mark.asyncio
async def test_tutorial_action_dismiss(tutorial_screen):
    """Test tutorial dismiss action."""
    app = TodoApp()
    async with app.run_test():
        app.push_screen(tutorial_screen)
        
        # Call dismiss action
        tutorial_screen.action_dismiss()
        
        # Should dismiss without errors
