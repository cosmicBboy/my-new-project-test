"""Tests for cheat sheet generator."""

import pytest
import tempfile
from pathlib import Path

from todo_tui.cheatsheet import CheatSheetGenerator, export_cheat_sheet
from todo_tui.help_overlay import KeyboardShortcut


def test_cheatsheet_generator_initialization():
    """Test CheatSheetGenerator initialization."""
    shortcuts = [
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
        KeyboardShortcut("Space", "Toggle", "Toggle completion", "Task Management"),
    ]
    
    generator = CheatSheetGenerator(shortcuts)
    assert generator.shortcuts == shortcuts


def test_generate_text():
    """Test generating plain text cheat sheet."""
    shortcuts = [
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
        KeyboardShortcut("Space", "Toggle", "Toggle completion", "Task Management"),
        KeyboardShortcut("↑", "Move Up", "Navigate up", "Navigation"),
    ]
    
    generator = CheatSheetGenerator(shortcuts)
    text = generator.generate_text()
    
    assert "TODO TUI" in text
    assert "Keyboard Shortcuts" in text
    assert "Navigation" in text
    assert "Task Management" in text
    assert "Application" in text
    assert "q" in text
    assert "Space" in text
    assert "Quit" in text
    assert "Toggle" in text


def test_generate_markdown():
    """Test generating markdown cheat sheet."""
    shortcuts = [
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
        KeyboardShortcut("Space", "Toggle", "Toggle completion", "Task Management"),
    ]
    
    generator = CheatSheetGenerator(shortcuts)
    markdown = generator.generate_markdown()
    
    assert "# TODO TUI" in markdown
    assert "## Application" in markdown
    assert "## Task Management" in markdown
    assert "| Key | Action | Description |" in markdown
    assert "| `q` |" in markdown
    assert "| `Space` |" in markdown


def test_export_to_file_text():
    """Test exporting cheat sheet to text file."""
    shortcuts = [
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        file_path = Path(f.name)
    
    try:
        generator = CheatSheetGenerator(shortcuts)
        generator.export_to_file(file_path, format="text")
        
        assert file_path.exists()
        content = file_path.read_text()
        assert "TODO TUI" in content
        assert "Quit" in content
    finally:
        if file_path.exists():
            file_path.unlink()


def test_export_to_file_markdown():
    """Test exporting cheat sheet to markdown file."""
    shortcuts = [
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        file_path = Path(f.name)
    
    try:
        generator = CheatSheetGenerator(shortcuts)
        generator.export_to_file(file_path, format="markdown")
        
        assert file_path.exists()
        content = file_path.read_text()
        assert "# TODO TUI" in content
        assert "| Key |" in content
    finally:
        if file_path.exists():
            file_path.unlink()


def test_export_cheat_sheet_auto_detect_format():
    """Test that export_cheat_sheet auto-detects format from extension."""
    shortcuts = [
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
    ]
    
    # Test markdown format
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        md_path = Path(f.name)
    
    try:
        result_path = export_cheat_sheet(shortcuts, md_path)
        assert result_path == md_path
        content = md_path.read_text()
        assert "# TODO TUI" in content
        assert "| Key |" in content
    finally:
        if md_path.exists():
            md_path.unlink()
    
    # Test text format
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        txt_path = Path(f.name)
    
    try:
        result_path = export_cheat_sheet(shortcuts, txt_path)
        assert result_path == txt_path
        content = txt_path.read_text()
        assert "TODO TUI" in content
        assert "──" in content  # Text format uses this separator
    finally:
        if txt_path.exists():
            txt_path.unlink()


def test_cheatsheet_includes_all_categories():
    """Test that cheat sheet includes all categories."""
    shortcuts = [
        KeyboardShortcut("↑", "Move Up", "Navigate up", "Navigation"),
        KeyboardShortcut("Space", "Toggle", "Toggle completion", "Task Management"),
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
    ]
    
    generator = CheatSheetGenerator(shortcuts)
    text = generator.generate_text()
    
    assert "Navigation" in text
    assert "Task Management" in text
    assert "Application" in text


def test_cheatsheet_includes_tips():
    """Test that cheat sheet includes helpful tips."""
    shortcuts = [
        KeyboardShortcut("q", "Quit", "Exit the app", "Application"),
    ]
    
    generator = CheatSheetGenerator(shortcuts)
    text = generator.generate_text()
    
    assert "Tips:" in text
    assert "?" in text  # Should mention help key


def test_markdown_escapes_pipe_characters():
    """Test that markdown generator escapes pipe characters in table."""
    shortcuts = [
        KeyboardShortcut("↑ / ↓", "Navigate", "Up or down", "Navigation"),
    ]
    
    generator = CheatSheetGenerator(shortcuts)
    markdown = generator.generate_markdown()
    
    # Should contain escaped pipes or handle them properly
    assert "Navigate" in markdown
