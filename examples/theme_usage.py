#!/usr/bin/env python3
"""Theme customization examples for the TODO TUI app.

This script demonstrates how to work with themes programmatically,
including creating custom themes and managing theme configuration.
"""

import tempfile
from pathlib import Path

from todo_tui.themes import (
    Theme,
    ThemePreset,
    FontSize,
    Layout,
    ColorScheme,
    get_theme_by_preset,
    get_all_themes,
    generate_css,
)
from todo_tui.config import Config


def example_built_in_themes():
    """Demonstrate all built-in themes."""
    print("=== Built-in Themes ===")
    print()
    
    themes = get_all_themes()
    for theme in themes:
        print(f"Theme: {theme.name}")
        print(f"  Preset: {theme.preset.value}")
        print(f"  Background: {theme.colors.background}")
        print(f"  Foreground: {theme.colors.foreground}")
        print(f"  Primary: {theme.colors.primary}")
        print(f"  Font Size: {theme.font_size.value}")
        print(f"  Layout: {theme.layout.value}")
        print()


def example_get_theme_by_preset():
    """Demonstrate getting a specific theme."""
    print("=== Getting Specific Themes ===")
    print()
    
    # Get dark theme
    dark = get_theme_by_preset(ThemePreset.DARK)
    print(f"Dark Theme: {dark.name}")
    print(f"  Background: {dark.colors.background}")
    print()
    
    # Get light theme
    light = get_theme_by_preset(ThemePreset.LIGHT)
    print(f"Light Theme: {light.name}")
    print(f"  Background: {light.colors.background}")
    print()
    
    # Get high contrast theme
    high_contrast = get_theme_by_preset(ThemePreset.HIGH_CONTRAST)
    print(f"High Contrast Theme: {high_contrast.name}")
    print(f"  Background: {high_contrast.colors.background}")
    print()


def example_custom_color_scheme():
    """Demonstrate creating a custom color scheme."""
    print("=== Custom Color Scheme ===")
    print()
    
    # Create a custom "Ocean" theme
    ocean_colors = ColorScheme(
        background="#001f3f",  # Deep blue
        foreground="#7fdbff",  # Light cyan
        primary="#0074d9",     # Blue
        secondary="#39cccc",   # Teal
        accent="#2ecc40",      # Green
        success="#2ecc40",     # Green
        warning="#ff851b",     # Orange
        error="#ff4136",       # Red
        border="#0074d9",
        highlight_bg="#0074d9",
        highlight_fg="#ffffff",
        header_bg="#001f3f",
        footer_bg="#001f3f",
        input_bg="#002a52",
        input_border="#0074d9",
        completed_text="#39cccc",
        postponed_text="#ff851b",
        postponed_bg="#003d66",
    )
    
    ocean_theme = Theme(
        name="Ocean",
        preset=ThemePreset.DARK,  # Base it on dark theme
        colors=ocean_colors,
        font_size=FontSize.MEDIUM,
        layout=Layout.COMFORTABLE,
    )
    
    print(f"Custom Theme: {ocean_theme.name}")
    print(f"  Background: {ocean_theme.colors.background}")
    print(f"  Foreground: {ocean_theme.colors.foreground}")
    print(f"  Primary: {ocean_theme.colors.primary}")
    print()
    
    # Generate CSS for custom theme
    css = generate_css(ocean_theme)
    print("Generated CSS (first 300 characters):")
    print(css[:300] + "...")
    print()


def example_theme_configuration():
    """Demonstrate theme configuration management."""
    print("=== Theme Configuration ===")
    print()
    
    # Create temporary config for demonstration
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        # Create config
        config = Config(config_path)
        print(f"Default theme: {config.theme.name}")
        print()
        
        # Change to light theme
        light_theme = get_theme_by_preset(ThemePreset.LIGHT)
        config.save_theme(light_theme)
        print(f"Saved theme: {light_theme.name}")
        print()
        
        # Load config again to verify persistence
        config2 = Config(config_path)
        print(f"Loaded theme: {config2.theme.name}")
        print()
        
        # Cycle through themes
        print("Cycling through themes:")
        for i in range(5):
            theme = config2.cycle_theme()
            print(f"  {i+1}. {theme.name}")
        print()
        
    finally:
        # Cleanup
        if config_path.exists():
            config_path.unlink()


def example_font_size_and_layout():
    """Demonstrate font size and layout options."""
    print("=== Font Size and Layout Options ===")
    print()
    
    # Create temporary config
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        # Show default settings
        print(f"Default font size: {config.theme.font_size.value}")
        print(f"Default layout: {config.theme.layout.value}")
        print()
        
        # Cycle font sizes
        print("Cycling font sizes:")
        for i in range(3):
            size = config.cycle_font_size()
            print(f"  {i+1}. {size.value}")
        print()
        
        # Cycle layouts
        print("Cycling layouts:")
        for i in range(3):
            layout = config.cycle_layout()
            print(f"  {i+1}. {layout.value}")
        print()
        
        # Set specific font size
        config.set_font_size(FontSize.LARGE)
        print(f"Set font size to: {config.theme.font_size.value}")
        print()
        
        # Set specific layout
        config.set_layout(Layout.SPACIOUS)
        print(f"Set layout to: {config.theme.layout.value}")
        print()
        
    finally:
        # Cleanup
        if config_path.exists():
            config_path.unlink()


def example_css_generation():
    """Demonstrate CSS generation for different layouts."""
    print("=== CSS Generation for Layouts ===")
    print()
    
    theme = get_theme_by_preset(ThemePreset.COLORFUL)
    
    # Generate CSS for different layouts
    layouts = [Layout.COMPACT, Layout.COMFORTABLE, Layout.SPACIOUS]
    
    for layout in layouts:
        theme.layout = layout
        css = generate_css(theme)
        
        print(f"Layout: {layout.value}")
        # Find and show padding settings in CSS
        lines = [line.strip() for line in css.split('\n') if 'padding:' in line]
        for line in lines[:3]:  # Show first 3 padding declarations
            print(f"  {line}")
        print()


def example_theme_switching_in_app():
    """Display information about theme switching in the app."""
    print("=== Theme Switching in the App ===")
    print()
    print("When running the interactive app (uv run todo-tui), you can:")
    print()
    print("  t       : Cycle through themes (Dark → Light → High Contrast → Colorful → Cyberpunk)")
    print("  f       : Cycle through font sizes (Medium → Large → Small)")
    print("  l       : Cycle through layouts (Comfortable → Spacious → Compact)")
    print()
    print("Your theme preferences are automatically saved to:")
    print("  ~/.todo-tui-config.json")
    print()
    print("Available themes:")
    print("  - Dark: Professional dark theme with soft colors")
    print("  - Light: Clean light theme for bright environments")
    print("  - High Contrast: Maximum contrast for accessibility")
    print("  - Colorful: Vibrant theme with gradient accents")
    print("  - Cyberpunk: Neon theme with hot pink and cyan (default)")
    print()


def example_accessibility_features():
    """Demonstrate accessibility features."""
    print("=== Accessibility Features ===")
    print()
    
    print("High Contrast Theme:")
    high_contrast = get_theme_by_preset(ThemePreset.HIGH_CONTRAST)
    print(f"  Background: {high_contrast.colors.background} (Pure black)")
    print(f"  Foreground: {high_contrast.colors.foreground} (Pure white)")
    print(f"  Border: {high_contrast.colors.border} (Pure white)")
    print(f"  Success: {high_contrast.colors.success} (Pure green)")
    print(f"  Warning: {high_contrast.colors.warning} (Pure yellow)")
    print(f"  Error: {high_contrast.colors.error} (Pure red)")
    print()
    print("This theme provides maximum contrast for users with")
    print("visual impairments or those working in bright environments.")
    print()
    
    print("Layout Options for Readability:")
    print("  - Compact: Minimal spacing, more content visible")
    print("  - Comfortable: Balanced spacing (default)")
    print("  - Spacious: Maximum spacing, easier to read")
    print()


def main():
    """Run all examples."""
    print("TODO TUI App - Theme Customization Examples")
    print("=" * 60)
    print()
    
    example_built_in_themes()
    print()
    
    example_get_theme_by_preset()
    print()
    
    example_custom_color_scheme()
    print()
    
    example_theme_configuration()
    print()
    
    example_font_size_and_layout()
    print()
    
    example_css_generation()
    print()
    
    example_theme_switching_in_app()
    print()
    
    example_accessibility_features()
    
    print("=" * 60)
    print("Examples complete!")
    print()
    print("Run 'uv run todo-tui' and press 't' to try different themes!")


if __name__ == "__main__":
    main()
