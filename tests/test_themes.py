"""Tests for the theme system."""

import pytest
from todo_tui.themes import (
    Theme,
    ThemePreset,
    FontSize,
    Layout,
    ColorScheme,
    get_theme_by_preset,
    get_all_themes,
    generate_css,
    DARK_THEME,
    LIGHT_THEME,
    HIGH_CONTRAST_THEME,
    COLORFUL_THEME,
    CYBERPUNK_THEME,
)


def test_color_scheme_defaults():
    """Test ColorScheme has reasonable defaults."""
    colors = ColorScheme()
    assert colors.background is not None
    assert colors.foreground is not None
    assert colors.primary is not None
    assert colors.secondary is not None


def test_theme_creation():
    """Test creating a Theme instance."""
    theme = Theme(
        name="Test Theme",
        preset=ThemePreset.DARK,
        colors=ColorScheme(),
        font_size=FontSize.MEDIUM,
        layout=Layout.COMFORTABLE,
    )
    assert theme.name == "Test Theme"
    assert theme.preset == ThemePreset.DARK
    assert theme.font_size == FontSize.MEDIUM
    assert theme.layout == Layout.COMFORTABLE


def test_theme_serialization():
    """Test theme can be serialized and deserialized."""
    original = Theme(
        name="Test",
        preset=ThemePreset.LIGHT,
        font_size=FontSize.LARGE,
        layout=Layout.SPACIOUS,
    )
    
    # Serialize
    data = original.to_dict()
    assert data["name"] == "Test"
    assert data["preset"] == "light"
    assert data["font_size"] == "large"
    assert data["layout"] == "spacious"
    
    # Deserialize
    restored = Theme.from_dict(data)
    assert restored.preset == ThemePreset.LIGHT
    assert restored.font_size == FontSize.LARGE
    assert restored.layout == Layout.SPACIOUS


def test_get_theme_by_preset():
    """Test retrieving themes by preset."""
    dark = get_theme_by_preset(ThemePreset.DARK)
    assert dark == DARK_THEME
    assert dark.name == "Dark"
    
    light = get_theme_by_preset(ThemePreset.LIGHT)
    assert light == LIGHT_THEME
    assert light.name == "Light"
    
    high_contrast = get_theme_by_preset(ThemePreset.HIGH_CONTRAST)
    assert high_contrast == HIGH_CONTRAST_THEME
    assert high_contrast.name == "High Contrast"
    
    colorful = get_theme_by_preset(ThemePreset.COLORFUL)
    assert colorful == COLORFUL_THEME
    assert colorful.name == "Colorful"
    
    cyberpunk = get_theme_by_preset(ThemePreset.CYBERPUNK)
    assert cyberpunk == CYBERPUNK_THEME
    assert cyberpunk.name == "Cyberpunk"


def test_get_all_themes():
    """Test getting all available themes."""
    themes = get_all_themes()
    assert len(themes) == 5
    theme_names = [t.name for t in themes]
    assert "Dark" in theme_names
    assert "Light" in theme_names
    assert "High Contrast" in theme_names
    assert "Colorful" in theme_names
    assert "Cyberpunk" in theme_names


def test_generate_css_dark_theme():
    """Test CSS generation for dark theme."""
    css = generate_css(DARK_THEME)
    assert "#1e1e1e" in css  # Dark background
    assert "#d4d4d4" in css  # Light foreground
    assert "background:" in css
    assert "color:" in css
    assert "border:" in css


def test_generate_css_light_theme():
    """Test CSS generation for light theme."""
    css = generate_css(LIGHT_THEME)
    assert "#ffffff" in css  # Light background
    assert "#24292f" in css  # Dark foreground
    assert "background:" in css
    assert "color:" in css


def test_generate_css_high_contrast_theme():
    """Test CSS generation for high contrast theme."""
    css = generate_css(HIGH_CONTRAST_THEME)
    assert "#000000" in css  # Black background
    assert "#ffffff" in css  # White foreground
    assert "#00ffff" in css  # Cyan
    assert "#ffff00" in css  # Yellow


def test_generate_css_compact_layout():
    """Test CSS generation with compact layout."""
    theme = Theme(
        name="Test",
        preset=ThemePreset.DARK,
        layout=Layout.COMPACT,
    )
    css = generate_css(theme)
    # Compact layout should have minimal padding
    assert "padding: 0" in css or "padding: 0 1" in css


def test_generate_css_comfortable_layout():
    """Test CSS generation with comfortable layout."""
    theme = Theme(
        name="Test",
        preset=ThemePreset.DARK,
        layout=Layout.COMFORTABLE,
    )
    css = generate_css(theme)
    # Comfortable layout should have moderate padding
    assert "padding: 1" in css or "padding: 0 2" in css


def test_generate_css_spacious_layout():
    """Test CSS generation with spacious layout."""
    theme = Theme(
        name="Test",
        preset=ThemePreset.DARK,
        layout=Layout.SPACIOUS,
    )
    css = generate_css(theme)
    # Spacious layout should have more padding
    assert "padding: 2" in css or "padding: 1 2" in css


def test_generate_css_includes_all_selectors():
    """Test that generated CSS includes all required selectors."""
    css = generate_css(DARK_THEME)
    
    # Check for key selectors
    assert "Screen {" in css
    assert "Header {" in css
    assert "Footer {" in css
    assert "#todo-container {" in css
    assert "#todo-list {" in css
    assert "#input-container {" in css
    assert "Input {" in css
    assert "ListView {" in css
    assert "ListItem {" in css
    assert ".dim {" in css
    assert ".postponed {" in css


def test_dark_theme_properties():
    """Test dark theme has expected properties."""
    assert DARK_THEME.preset == ThemePreset.DARK
    assert DARK_THEME.colors.background == "#1e1e1e"
    assert DARK_THEME.colors.foreground == "#d4d4d4"


def test_light_theme_properties():
    """Test light theme has expected properties."""
    assert LIGHT_THEME.preset == ThemePreset.LIGHT
    assert LIGHT_THEME.colors.background == "#ffffff"
    assert LIGHT_THEME.colors.foreground == "#24292f"


def test_high_contrast_theme_properties():
    """Test high contrast theme has expected properties."""
    assert HIGH_CONTRAST_THEME.preset == ThemePreset.HIGH_CONTRAST
    assert HIGH_CONTRAST_THEME.colors.background == "#000000"
    assert HIGH_CONTRAST_THEME.colors.foreground == "#ffffff"


def test_colorful_theme_properties():
    """Test colorful theme has expected properties."""
    assert COLORFUL_THEME.preset == ThemePreset.COLORFUL
    assert COLORFUL_THEME.colors.background == "#2d1b2e"
    assert COLORFUL_THEME.colors.foreground == "#f8f0e3"


def test_cyberpunk_theme_properties():
    """Test cyberpunk theme has expected properties."""
    assert CYBERPUNK_THEME.preset == ThemePreset.CYBERPUNK
    assert CYBERPUNK_THEME.colors.background == "#0a0e27"
    assert CYBERPUNK_THEME.colors.foreground == "#06ffa5"


def test_theme_enum_values():
    """Test ThemePreset enum has expected values."""
    assert ThemePreset.DARK.value == "dark"
    assert ThemePreset.LIGHT.value == "light"
    assert ThemePreset.HIGH_CONTRAST.value == "high_contrast"
    assert ThemePreset.COLORFUL.value == "colorful"
    assert ThemePreset.CYBERPUNK.value == "cyberpunk"


def test_font_size_enum_values():
    """Test FontSize enum has expected values."""
    assert FontSize.SMALL.value == "small"
    assert FontSize.MEDIUM.value == "medium"
    assert FontSize.LARGE.value == "large"


def test_layout_enum_values():
    """Test Layout enum has expected values."""
    assert Layout.COMPACT.value == "compact"
    assert Layout.COMFORTABLE.value == "comfortable"
    assert Layout.SPACIOUS.value == "spacious"


def test_custom_color_scheme():
    """Test creating a custom color scheme."""
    custom_colors = ColorScheme(
        background="#123456",
        foreground="#abcdef",
        primary="#ff0000",
        secondary="#00ff00",
        accent="#0000ff",
    )
    
    theme = Theme(
        name="Custom",
        preset=ThemePreset.DARK,
        colors=custom_colors,
    )
    
    css = generate_css(theme)
    assert "#123456" in css
    assert "#abcdef" in css
    assert "#ff0000" in css
    assert "#00ff00" in css
    assert "#0000ff" in css
