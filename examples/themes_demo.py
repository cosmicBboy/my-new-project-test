"""
Example demonstrating the themes and customization features.

This example shows how to:
1. Use built-in themes (dark, light, high contrast, colorful)
2. Create custom themes with your own color palette
3. Switch themes using keyboard shortcuts
4. Adjust layout density (compact, comfortable, spacious)
5. Change font sizes (small, medium, large)
6. Persist preferences across sessions
"""

from pathlib import Path
import tempfile
from todo_tui.storage import PreferencesStorage
from todo_tui.themes import (
    THEMES, 
    ThemeName, 
    LayoutDensity, 
    FontSize,
    create_custom_theme,
)


def main():
    """Demonstrate themes and customization features."""
    
    # Create a temporary preferences file for this demo
    temp_dir = Path(tempfile.mkdtemp())
    prefs_file = temp_dir / "demo-preferences.json"
    
    # Initialize preferences storage
    prefs = PreferencesStorage(prefs_file)
    
    print("🎨 TODO TUI App - Themes and Customization Demo\n")
    print("=" * 60)
    
    # 1. Show available built-in themes
    print("\n📋 Built-in Themes:")
    print("-" * 60)
    for theme_name, theme in THEMES.items():
        print(f"  • {theme.display_name:20} (key: {theme.name})")
    
    # 2. Demonstrate custom theme creation
    print("\n🎨 Creating Custom Themes:")
    print("-" * 60)
    print("You can create your own themes with custom color palettes!\n")
    
    # Create a custom blue theme
    custom_blue = create_custom_theme(
        name="custom_blue",
        display_name="Ocean Blue",
        colors={
            "background": "#1a1d29",
            "surface": "#252936",
            "text": "#e0e0e0",
            "text_dim": "#707070",
            "accent": "#4a9eff",
            "border": "#3a3d49",
            "completed": "#909090",
            "postponed": "#ffaa00",
        }
    )
    print(f"  Created: {custom_blue.display_name}")
    print(f"  Colors: Ocean blue accent with dark background")
    
    # Create a custom green theme
    custom_green = create_custom_theme(
        name="custom_green",
        display_name="Forest Green",
        colors={
            "background": "#1a2617",
            "surface": "#2a3627",
            "text": "#d4e4d4",
            "text_dim": "#6a7a6a",
            "accent": "#4a9e4a",
            "border": "#3a4a3a",
            "completed": "#7a8a7a",
            "postponed": "#d4a44a",
        }
    )
    print(f"  Created: {custom_green.display_name}")
    print(f"  Colors: Nature-inspired green tones")
    
    # Save custom themes to preferences
    prefs.add_custom_theme({
        "name": custom_blue.name,
        "display_name": custom_blue.display_name,
        "colors": {
            "background": "#1a1d29",
            "surface": "#252936",
            "text": "#e0e0e0",
            "accent": "#4a9eff",
        }
    })
    print(f"\n  ✓ Custom theme saved to preferences")
    
    # 3. Demonstrate theme switching
    print("\n🔄 Theme Switching:")
    print("-" * 60)
    print("In the app, press 't' to cycle through themes:")
    print("  • Theme changes apply IMMEDIATELY")
    print("  • No restart required!")
    
    current_theme = prefs.get_theme()
    print(f"\n  Current theme: {current_theme}")
    
    # Cycle to next theme
    all_themes = list(THEMES.keys())
    current_index = all_themes.index(current_theme) if current_theme in all_themes else 0
    next_index = (current_index + 1) % len(all_themes)
    next_theme = all_themes[next_index]
    
    prefs.set_theme(next_theme)
    print(f"  Next theme: {next_theme}")
    print(f"  → Saved to: {prefs_file}")
    
    # 4. Layout density options
    print("\n📐 Layout Density Options:")
    print("-" * 60)
    print("In the app, press 'l' to cycle through layouts:")
    for density in LayoutDensity:
        print(f"  • {density.value.capitalize():15} - ", end="")
        if density == LayoutDensity.COMPACT:
            print("Minimal spacing, more items visible")
        elif density == LayoutDensity.COMFORTABLE:
            print("Balanced spacing (default)")
        else:
            print("Maximum spacing, easier to read")
    
    current_density = prefs.get_layout_density()
    print(f"\n  Current layout: {current_density}")
    print("  → Changes apply instantly")
    
    # 5. Font size options
    print("\n🔤 Font Size Options:")
    print("-" * 60)
    print("In the app, press 'f' to cycle through font sizes:")
    for size in FontSize:
        print(f"  • {size.value.capitalize():10} - ", end="")
        if size == FontSize.SMALL:
            print("Compact text, more content visible")
        elif size == FontSize.MEDIUM:
            print("Standard size (default)")
        else:
            print("Larger text for better readability")
    
    current_font = prefs.get_font_size()
    print(f"\n  Current font size: {current_font}")
    print("  → Changes apply IMMEDIATELY (no restart!)")
    
    # 6. Show keyboard shortcuts
    print("\n⌨️  Keyboard Shortcuts for Customization:")
    print("-" * 60)
    print("  t - Cycle through themes (instant)")
    print("  l - Cycle through layout densities (instant)")
    print("  f - Cycle through font sizes (instant)")
    print("  q - Quit application")
    
    # 7. Theme descriptions
    print("\n🎨 Theme Descriptions:")
    print("-" * 60)
    print("\n  Dark (Catppuccin Mocha)")
    print("  • Soft, warm dark theme with muted colors")
    print("  • Easy on the eyes for long sessions")
    print("  • Great for low-light environments")
    
    print("\n  Light (Catppuccin Latte)")
    print("  • Clean, bright theme for daytime use")
    print("  • High readability in well-lit rooms")
    print("  • Professional appearance")
    
    print("\n  High Contrast")
    print("  • Maximum contrast for accessibility")
    print("  • Black and white design")
    print("  • Excellent for users with visual impairments")
    print("  • Clear focus indicators (yellow)")
    
    print("\n  Colorful (Cyberpunk)")
    print("  • Vibrant neon colors with gradients")
    print("  • Futuristic aesthetic")
    print("  • High visual impact")
    print("  • Fun and energetic")
    
    # 8. Custom theme guide
    print("\n🛠️  Creating Custom Themes:")
    print("-" * 60)
    print("You can create themes programmatically:")
    print("""
    from todo_tui.themes import create_custom_theme
    
    my_theme = create_custom_theme(
        name="my_theme",
        display_name="My Custom Theme",
        colors={
            "background": "#your_color",
            "surface": "#your_color",
            "text": "#your_color",
            "text_dim": "#your_color",
            "accent": "#your_color",
            "border": "#your_color",
            "completed": "#your_color",
            "postponed": "#your_color",
        }
    )
    
    # Save to preferences
    prefs.add_custom_theme({
        "name": my_theme.name,
        "display_name": my_theme.display_name,
        "colors": {...}
    })
    """)
    
    # 9. Persistence example
    print("\n💾 Preference Persistence:")
    print("-" * 60)
    print("All preferences are automatically saved to:")
    print(f"  {Path.home() / '.todo-tui-preferences.json'}")
    print("\nYour customizations persist across sessions:")
    print("  • Current theme")
    print("  • Layout density")
    print("  • Font size")
    print("  • Custom themes you've created")
    
    # 10. What's NEW
    print("\n✨ What's New in This Version:")
    print("-" * 60)
    print("  ✓ Custom theme creation - design your own look!")
    print("  ✓ Instant theme switching - no restart needed")
    print("  ✓ Instant font size changes - see changes immediately")
    print("  ✓ Smooth transitions between themes")
    print("  ✓ Save and load custom themes")
    
    # 11. Customization tips
    print("\n💡 Tips:")
    print("-" * 60)
    print("  1. Try different themes to find what works best for you")
    print("  2. Use High Contrast theme for better accessibility")
    print("  3. Adjust layout density based on your screen size")
    print("  4. Compact layout shows more todos at once")
    print("  5. Spacious layout is easier on the eyes")
    print("  6. All changes now apply instantly!")
    print("  7. Create custom themes with your favorite colors")
    print("  8. Share your custom theme color palettes with others")
    
    # 12. Example workflow
    print("\n🚀 Example Workflow:")
    print("-" * 60)
    print("  1. Start the app with: uv run todo-tui")
    print("  2. Press 't' to try different themes - instant preview!")
    print("  3. Press 'l' to adjust spacing")
    print("  4. Press 'f' to change font size - see it immediately")
    print("  5. All preferences saved automatically")
    print("  6. Create custom themes in Python if desired")
    
    # Clean up demo file
    prefs_file.unlink()
    temp_dir.rmdir()
    
    print("\n" + "=" * 60)
    print("\nDemo complete! Start the app to try these features yourself.")
    print("Run: uv run todo-tui\n")


if __name__ == "__main__":
    main()
