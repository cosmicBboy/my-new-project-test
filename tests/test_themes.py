"""Tests for the themes module."""

import pytest
from todo_tui.themes import (
    THEMES,
    ThemeName,
    LayoutDensity,
    FontSize,
    Theme,
    get_layout_padding,
    get_layout_margin,
    get_font_size_class,
    get_base_css,
    create_custom_theme,
    load_custom_theme,
)


def test_all_themes_defined():
    """Test that all theme names have corresponding theme definitions."""
    for theme_name in ThemeName:
        assert theme_name in THEMES
        assert isinstance(THEMES[theme_name], Theme)


def test_theme_structure():
    """Test that each theme has required attributes."""
    for theme in THEMES.values():
        assert hasattr(theme, "name")
        assert hasattr(theme, "display_name")
        assert hasattr(theme, "css")
        assert isinstance(theme.name, str)
        assert isinstance(theme.display_name, str)
        assert isinstance(theme.css, str)
        assert len(theme.css) > 0


def test_dark_theme():
    """Test dark theme has correct attributes."""
    dark_theme = THEMES[ThemeName.DARK]
    assert dark_theme.name == ThemeName.DARK
    assert dark_theme.display_name == "Dark"
    assert "#1e1e2e" in dark_theme.css  # Background color
    assert "Screen" in dark_theme.css
    assert "ListView" in dark_theme.css


def test_light_theme():
    """Test light theme has correct attributes."""
    light_theme = THEMES[ThemeName.LIGHT]
    assert light_theme.name == ThemeName.LIGHT
    assert light_theme.display_name == "Light"
    assert "#eff1f5" in light_theme.css  # Background color
    assert "Screen" in light_theme.css


def test_high_contrast_theme():
    """Test high contrast theme has correct attributes."""
    hc_theme = THEMES[ThemeName.HIGH_CONTRAST]
    assert hc_theme.name == ThemeName.HIGH_CONTRAST
    assert hc_theme.display_name == "High Contrast"
    assert "#000000" in hc_theme.css  # Black
    assert "#ffffff" in hc_theme.css  # White


def test_colorful_theme():
    """Test colorful theme has correct attributes."""
    colorful_theme = THEMES[ThemeName.COLORFUL]
    assert colorful_theme.name == ThemeName.COLORFUL
    assert colorful_theme.display_name == "Colorful (Cyberpunk)"
    assert "gradient" in colorful_theme.css.lower()


def test_theme_css_includes_required_elements():
    """Test that each theme includes CSS for required UI elements."""
    required_elements = [
        "Screen",
        "#todo-container",
        "#todo-list",
        "#input-container",
        "Input",
        "ListView",
        "Header",
        "Footer",
    ]
    
    for theme in THEMES.values():
        for element in required_elements:
            assert element in theme.css, f"Theme {theme.name} missing CSS for {element}"


def test_layout_padding_compact():
    """Test compact layout padding."""
    padding = get_layout_padding(LayoutDensity.COMPACT)
    assert padding == 0


def test_layout_padding_comfortable():
    """Test comfortable layout padding."""
    padding = get_layout_padding(LayoutDensity.COMFORTABLE)
    assert padding == 1


def test_layout_padding_spacious():
    """Test spacious layout padding."""
    padding = get_layout_padding(LayoutDensity.SPACIOUS)
    assert padding == 2


def test_layout_margin_compact():
    """Test compact layout margin."""
    margin = get_layout_margin(LayoutDensity.COMPACT)
    assert margin == 0


def test_layout_margin_comfortable():
    """Test comfortable layout margin."""
    margin = get_layout_margin(LayoutDensity.COMFORTABLE)
    assert margin == 1


def test_layout_margin_spacious():
    """Test spacious layout margin."""
    margin = get_layout_margin(LayoutDensity.SPACIOUS)
    assert margin == 2


def test_font_size_class_small():
    """Test small font size class."""
    css_class = get_font_size_class(FontSize.SMALL)
    assert css_class == "font-small"


def test_font_size_class_medium():
    """Test medium font size class."""
    css_class = get_font_size_class(FontSize.MEDIUM)
    assert css_class == "font-medium"


def test_font_size_class_large():
    """Test large font size class."""
    css_class = get_font_size_class(FontSize.LARGE)
    assert css_class == "font-large"


def test_theme_name_enum():
    """Test ThemeName enum values."""
    assert ThemeName.DARK == "dark"
    assert ThemeName.LIGHT == "light"
    assert ThemeName.HIGH_CONTRAST == "high_contrast"
    assert ThemeName.COLORFUL == "colorful"


def test_layout_density_enum():
    """Test LayoutDensity enum values."""
    assert LayoutDensity.COMPACT == "compact"
    assert LayoutDensity.COMFORTABLE == "comfortable"
    assert LayoutDensity.SPACIOUS == "spacious"


def test_font_size_enum():
    """Test FontSize enum values."""
    assert FontSize.SMALL == "small"
    assert FontSize.MEDIUM == "medium"
    assert FontSize.LARGE == "large"


def test_themes_count():
    """Test that we have exactly 4 themes."""
    assert len(THEMES) == 4


def test_theme_css_no_syntax_errors():
    """Test that theme CSS doesn't have obvious syntax errors."""
    for theme in THEMES.values():
        # Check for balanced braces
        assert theme.css.count("{") == theme.css.count("}")
        # Check for some content between braces
        assert "{" in theme.css and "}" in theme.css


def test_get_base_css():
    """Test that base CSS includes font size definitions."""
    base_css = get_base_css()
    assert "font-small" in base_css
    assert "font-medium" in base_css
    assert "font-large" in base_css
    assert "text-size" in base_css


def test_base_css_includes_all_sizes():
    """Test base CSS includes all font size variants."""
    base_css = get_base_css()
    for size in FontSize:
        assert f"font-{size.value}" in base_css


def test_create_custom_theme_basic():
    """Test creating a basic custom theme."""
    theme = create_custom_theme(
        name="test_theme",
        display_name="Test Theme",
        colors={
            "background": "#111111",
            "text": "#ffffff",
        }
    )
    
    assert theme.name == "test_theme"
    assert theme.display_name == "Test Theme"
    assert "#111111" in theme.css
    assert "#ffffff" in theme.css


def test_create_custom_theme_all_colors():
    """Test creating a custom theme with all color options."""
    colors = {
        "background": "#1a1d29",
        "surface": "#252936",
        "text": "#e0e0e0",
        "text_dim": "#707070",
        "accent": "#4a9eff",
        "border": "#3a3d49",
        "completed": "#909090",
        "postponed": "#ffaa00",
    }
    
    theme = create_custom_theme(
        name="custom_blue",
        display_name="Custom Blue",
        colors=colors
    )
    
    assert theme.name == "custom_blue"
    assert theme.display_name == "Custom Blue"
    
    # Check all colors are in CSS
    for color_value in colors.values():
        assert color_value in theme.css


def test_create_custom_theme_with_defaults():
    """Test that custom theme fills in defaults for missing colors."""
    theme = create_custom_theme(
        name="minimal",
        display_name="Minimal",
        colors={"background": "#000000"}  # Only one color
    )
    
    # Should still generate valid CSS
    assert "Screen" in theme.css
    assert "Header" in theme.css
    assert "Footer" in theme.css
    assert "#000000" in theme.css


def test_create_custom_theme_css_structure():
    """Test that custom theme generates proper CSS structure."""
    theme = create_custom_theme(
        name="test",
        display_name="Test",
        colors={"background": "#111111"}
    )
    
    # Check for required CSS elements
    required_elements = [
        "Screen",
        "Header",
        "#todo-container",
        "#todo-list",
        "Input",
        "ListView",
        "Footer",
    ]
    
    for element in required_elements:
        assert element in theme.css


def test_load_custom_theme_valid():
    """Test loading a valid custom theme from data."""
    theme_data = {
        "name": "loaded_theme",
        "display_name": "Loaded Theme",
        "colors": {
            "background": "#222222",
            "text": "#eeeeee",
        }
    }
    
    theme = load_custom_theme(theme_data)
    
    assert theme is not None
    assert theme.name == "loaded_theme"
    assert theme.display_name == "Loaded Theme"
    assert "#222222" in theme.css


def test_load_custom_theme_invalid():
    """Test loading invalid custom theme returns None."""
    # Missing required keys
    theme_data = {"name": "incomplete"}
    
    theme = load_custom_theme(theme_data)
    assert theme is None


def test_load_custom_theme_empty():
    """Test loading empty theme data returns None."""
    theme = load_custom_theme({})
    assert theme is None


def test_custom_theme_instance_of_theme():
    """Test that custom theme is instance of Theme."""
    theme = create_custom_theme(
        name="test",
        display_name="Test",
        colors={}
    )
    
    assert isinstance(theme, Theme)


def test_custom_theme_unique_names():
    """Test that custom themes can have unique names."""
    theme1 = create_custom_theme(
        name="theme_1",
        display_name="Theme 1",
        colors={"background": "#111111"}
    )
    
    theme2 = create_custom_theme(
        name="theme_2",
        display_name="Theme 2",
        colors={"background": "#222222"}
    )
    
    assert theme1.name != theme2.name
    assert theme1.display_name != theme2.display_name
