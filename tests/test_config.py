"""Tests for configuration management."""

import json
import pytest
import tempfile
from pathlib import Path

from todo_tui.config import Config
from todo_tui.themes import (
    Theme,
    ThemePreset,
    FontSize,
    Layout,
    get_theme_by_preset,
)


@pytest.fixture
def temp_config_path():
    """Create a temporary config file path."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        path = Path(f.name)
    yield path
    # Cleanup
    if path.exists():
        path.unlink()


def test_config_initialization(temp_config_path):
    """Test Config initializes with default theme."""
    config = Config(temp_config_path)
    assert config.config_path == temp_config_path
    assert config.theme is not None
    assert isinstance(config.theme, Theme)


def test_config_default_theme(temp_config_path):
    """Test Config uses Cyberpunk theme as default."""
    config = Config(temp_config_path)
    assert config.theme.preset == ThemePreset.CYBERPUNK


def test_config_save_and_load_theme(temp_config_path):
    """Test saving and loading theme configuration."""
    config = Config(temp_config_path)
    
    # Change to light theme
    light_theme = get_theme_by_preset(ThemePreset.LIGHT)
    config.save_theme(light_theme)
    
    # Create new config instance to test loading
    config2 = Config(temp_config_path)
    assert config2.theme.preset == ThemePreset.LIGHT


def test_config_save_theme_with_font_size(temp_config_path):
    """Test saving theme with font size."""
    config = Config(temp_config_path)
    
    theme = get_theme_by_preset(ThemePreset.DARK)
    theme.font_size = FontSize.LARGE
    config.save_theme(theme)
    
    # Load and verify
    config2 = Config(temp_config_path)
    assert config2.theme.font_size == FontSize.LARGE


def test_config_save_theme_with_layout(temp_config_path):
    """Test saving theme with layout."""
    config = Config(temp_config_path)
    
    theme = get_theme_by_preset(ThemePreset.COLORFUL)
    theme.layout = Layout.SPACIOUS
    config.save_theme(theme)
    
    # Load and verify
    config2 = Config(temp_config_path)
    assert config2.theme.layout == Layout.SPACIOUS


def test_config_cycle_theme(temp_config_path):
    """Test cycling through themes."""
    config = Config(temp_config_path)
    
    # Start with Cyberpunk (default)
    assert config.theme.preset == ThemePreset.CYBERPUNK
    
    # Cycle through all themes
    themes_seen = [config.theme.preset]
    for _ in range(4):  # Cycle 4 more times to see all 5 themes
        new_theme = config.cycle_theme()
        themes_seen.append(new_theme.preset)
    
    # Should have seen all 5 themes
    assert len(set(themes_seen)) == 5
    
    # Should cycle back to first theme
    assert themes_seen[-1] != themes_seen[0]  # After 4 cycles, different from start


def test_config_cycle_theme_preserves_settings(temp_config_path):
    """Test that cycling themes preserves font size and layout."""
    config = Config(temp_config_path)
    
    # Set custom font size and layout
    config.set_font_size(FontSize.LARGE)
    config.set_layout(Layout.COMPACT)
    
    # Cycle theme
    config.cycle_theme()
    
    # Check settings are preserved
    assert config.theme.font_size == FontSize.LARGE
    assert config.theme.layout == Layout.COMPACT


def test_config_set_font_size(temp_config_path):
    """Test setting font size."""
    config = Config(temp_config_path)
    
    config.set_font_size(FontSize.SMALL)
    assert config.theme.font_size == FontSize.SMALL
    
    # Verify it's saved
    config2 = Config(temp_config_path)
    assert config2.theme.font_size == FontSize.SMALL


def test_config_set_layout(temp_config_path):
    """Test setting layout."""
    config = Config(temp_config_path)
    
    config.set_layout(Layout.SPACIOUS)
    assert config.theme.layout == Layout.SPACIOUS
    
    # Verify it's saved
    config2 = Config(temp_config_path)
    assert config2.theme.layout == Layout.SPACIOUS


def test_config_cycle_font_size(temp_config_path):
    """Test cycling through font sizes."""
    config = Config(temp_config_path)
    
    # Start with default (medium)
    assert config.theme.font_size == FontSize.MEDIUM
    
    # Cycle to large
    size = config.cycle_font_size()
    assert size == FontSize.LARGE
    assert config.theme.font_size == FontSize.LARGE
    
    # Cycle to small
    size = config.cycle_font_size()
    assert size == FontSize.SMALL
    assert config.theme.font_size == FontSize.SMALL
    
    # Cycle back to medium
    size = config.cycle_font_size()
    assert size == FontSize.MEDIUM
    assert config.theme.font_size == FontSize.MEDIUM


def test_config_cycle_layout(temp_config_path):
    """Test cycling through layouts."""
    config = Config(temp_config_path)
    
    # Start with default (comfortable)
    assert config.theme.layout == Layout.COMFORTABLE
    
    # Cycle to spacious
    layout = config.cycle_layout()
    assert layout == Layout.SPACIOUS
    assert config.theme.layout == Layout.SPACIOUS
    
    # Cycle to compact
    layout = config.cycle_layout()
    assert layout == Layout.COMPACT
    assert config.theme.layout == Layout.COMPACT
    
    # Cycle back to comfortable
    layout = config.cycle_layout()
    assert layout == Layout.COMFORTABLE
    assert config.theme.layout == Layout.COMFORTABLE


def test_config_handles_corrupted_file(temp_config_path):
    """Test Config handles corrupted config file gracefully."""
    # Write invalid JSON
    temp_config_path.write_text("not valid json {")
    
    # Should not raise, should use default theme
    config = Config(temp_config_path)
    assert config.theme.preset == ThemePreset.CYBERPUNK


def test_config_handles_missing_theme_data(temp_config_path):
    """Test Config handles missing theme data in config file."""
    # Write config without theme data
    temp_config_path.write_text(json.dumps({"other_setting": "value"}))
    
    # Should not raise, should use default theme
    config = Config(temp_config_path)
    assert config.theme.preset == ThemePreset.CYBERPUNK


def test_config_preserves_other_settings(temp_config_path):
    """Test that saving theme preserves other config settings."""
    # Write config with other settings
    initial_data = {
        "other_setting": "value",
        "another_setting": 42,
    }
    temp_config_path.write_text(json.dumps(initial_data))
    
    # Load config and save a theme
    config = Config(temp_config_path)
    config.save_theme(get_theme_by_preset(ThemePreset.LIGHT))
    
    # Check that other settings are preserved
    data = json.loads(temp_config_path.read_text())
    assert data["other_setting"] == "value"
    assert data["another_setting"] == 42
    assert "theme" in data


def test_config_updates_existing_theme(temp_config_path):
    """Test that saving theme updates existing theme config."""
    # Save initial theme
    config = Config(temp_config_path)
    config.save_theme(get_theme_by_preset(ThemePreset.DARK))
    
    # Save different theme
    config.save_theme(get_theme_by_preset(ThemePreset.LIGHT))
    
    # Verify only one theme config exists
    data = json.loads(temp_config_path.read_text())
    assert data["theme"]["preset"] == "light"


def test_config_default_path():
    """Test Config uses default path when none provided."""
    config = Config()
    expected_path = Path.home() / ".todo-tui-config.json"
    assert config.config_path == expected_path
