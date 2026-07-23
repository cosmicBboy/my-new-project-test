"""Theme system for the TODO TUI app.

Provides customizable themes with different color schemes, font sizes, and layouts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ThemePreset(Enum):
    """Available theme presets."""
    DARK = "dark"
    LIGHT = "light"
    HIGH_CONTRAST = "high_contrast"
    COLORFUL = "colorful"
    CYBERPUNK = "cyberpunk"


class FontSize(Enum):
    """Font size options."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Layout(Enum):
    """Layout spacing options."""
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    SPACIOUS = "spacious"


@dataclass
class ColorScheme:
    """Color scheme for a theme.
    
    Attributes:
        background: Main background color
        foreground: Main text color
        primary: Primary accent color
        secondary: Secondary accent color
        accent: Additional accent color
        success: Success state color (completed items)
        warning: Warning state color (postponed items)
        error: Error state color
        border: Border color
        highlight_bg: Highlighted item background
        highlight_fg: Highlighted item foreground
        header_bg: Header background (gradient or solid)
        footer_bg: Footer background (gradient or solid)
        input_bg: Input field background
        input_border: Input field border
        completed_text: Completed todo text color
        postponed_text: Postponed todo text color
        postponed_bg: Postponed todo background
    """
    background: str = "#0a0e27"
    foreground: str = "#06ffa5"
    primary: str = "#ff006e"
    secondary: str = "#8338ec"
    accent: str = "#3a86ff"
    success: str = "#06ffa5"
    warning: str = "#ffbe0b"
    error: str = "#ff006e"
    border: str = "#ff006e"
    highlight_bg: str = "linear-gradient(90deg, #8338ec 0%, #3a86ff 100%)"
    highlight_fg: str = "#ffffff"
    header_bg: str = "linear-gradient(90deg, #ff006e 0%, #8338ec 50%, #3a86ff 100%)"
    footer_bg: str = "linear-gradient(90deg, #3a86ff 0%, #8338ec 50%, #ff006e 100%)"
    input_bg: str = "#1a1f3a"
    input_border: str = "#06ffa5"
    completed_text: str = "#7209b7"
    postponed_text: str = "#ffbe0b"
    postponed_bg: str = "#3a0f51"


@dataclass
class Theme:
    """Complete theme configuration.
    
    Attributes:
        name: Theme display name
        preset: Theme preset type
        colors: Color scheme
        font_size: Font size setting
        layout: Layout spacing setting
    """
    name: str
    preset: ThemePreset
    colors: ColorScheme = field(default_factory=ColorScheme)
    font_size: FontSize = FontSize.MEDIUM
    layout: Layout = Layout.COMFORTABLE
    
    def to_dict(self) -> dict:
        """Convert theme to dictionary for serialization."""
        return {
            "name": self.name,
            "preset": self.preset.value,
            "font_size": self.font_size.value,
            "layout": self.layout.value,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Theme":
        """Create theme from dictionary."""
        preset = ThemePreset(data["preset"])
        theme = get_theme_by_preset(preset)
        theme.font_size = FontSize(data.get("font_size", "medium"))
        theme.layout = Layout(data.get("layout", "comfortable"))
        return theme


# Built-in theme definitions

DARK_THEME = Theme(
    name="Dark",
    preset=ThemePreset.DARK,
    colors=ColorScheme(
        background="#1e1e1e",
        foreground="#d4d4d4",
        primary="#569cd6",
        secondary="#4ec9b0",
        accent="#c586c0",
        success="#4ec9b0",
        warning="#dcdcaa",
        error="#f48771",
        border="#3e3e3e",
        highlight_bg="#264f78",
        highlight_fg="#ffffff",
        header_bg="#2d2d30",
        footer_bg="#2d2d30",
        input_bg="#252526",
        input_border="#3e3e3e",
        completed_text="#6a9955",
        postponed_text="#dcdcaa",
        postponed_bg="#3a3a2a",
    ),
)

LIGHT_THEME = Theme(
    name="Light",
    preset=ThemePreset.LIGHT,
    colors=ColorScheme(
        background="#ffffff",
        foreground="#24292f",
        primary="#0969da",
        secondary="#8250df",
        accent="#1f883d",
        success="#1f883d",
        warning="#bf8700",
        error="#cf222e",
        border="#d0d7de",
        highlight_bg="#ddf4ff",
        highlight_fg="#24292f",
        header_bg="#f6f8fa",
        footer_bg="#f6f8fa",
        input_bg="#ffffff",
        input_border="#d0d7de",
        completed_text="#57606a",
        postponed_text="#9a6700",
        postponed_bg="#fff8c5",
    ),
)

HIGH_CONTRAST_THEME = Theme(
    name="High Contrast",
    preset=ThemePreset.HIGH_CONTRAST,
    colors=ColorScheme(
        background="#000000",
        foreground="#ffffff",
        primary="#00ffff",
        secondary="#ffff00",
        accent="#ff00ff",
        success="#00ff00",
        warning="#ffff00",
        error="#ff0000",
        border="#ffffff",
        highlight_bg="#ffffff",
        highlight_fg="#000000",
        header_bg="#000000",
        footer_bg="#000000",
        input_bg="#000000",
        input_border="#00ffff",
        completed_text="#00ff00",
        postponed_text="#ffff00",
        postponed_bg="#333300",
    ),
)

COLORFUL_THEME = Theme(
    name="Colorful",
    preset=ThemePreset.COLORFUL,
    colors=ColorScheme(
        background="#2d1b2e",
        foreground="#f8f0e3",
        primary="#ff6b9d",
        secondary="#c79fef",
        accent="#00d9ff",
        success="#a8e6cf",
        warning="#ffd93d",
        error="#ff6b6b",
        border="#ff6b9d",
        highlight_bg="linear-gradient(90deg, #ff6b9d 0%, #c79fef 100%)",
        highlight_fg="#ffffff",
        header_bg="linear-gradient(90deg, #ff6b9d 0%, #c79fef 50%, #00d9ff 100%)",
        footer_bg="linear-gradient(90deg, #00d9ff 0%, #c79fef 50%, #ff6b9d 100%)",
        input_bg="#3d2a3e",
        input_border="#c79fef",
        completed_text="#a8e6cf",
        postponed_text="#ffd93d",
        postponed_bg="#4a3a2e",
    ),
)

CYBERPUNK_THEME = Theme(
    name="Cyberpunk",
    preset=ThemePreset.CYBERPUNK,
    colors=ColorScheme(
        background="#0a0e27",
        foreground="#06ffa5",
        primary="#ff006e",
        secondary="#8338ec",
        accent="#3a86ff",
        success="#06ffa5",
        warning="#ffbe0b",
        error="#ff006e",
        border="#ff006e",
        highlight_bg="linear-gradient(90deg, #8338ec 0%, #3a86ff 100%)",
        highlight_fg="#ffffff",
        header_bg="linear-gradient(90deg, #ff006e 0%, #8338ec 50%, #3a86ff 100%)",
        footer_bg="linear-gradient(90deg, #3a86ff 0%, #8338ec 50%, #ff006e 100%)",
        input_bg="#1a1f3a",
        input_border="#06ffa5",
        completed_text="#7209b7",
        postponed_text="#ffbe0b",
        postponed_bg="#3a0f51",
    ),
)

# Theme registry
THEMES = {
    ThemePreset.DARK: DARK_THEME,
    ThemePreset.LIGHT: LIGHT_THEME,
    ThemePreset.HIGH_CONTRAST: HIGH_CONTRAST_THEME,
    ThemePreset.COLORFUL: COLORFUL_THEME,
    ThemePreset.CYBERPUNK: CYBERPUNK_THEME,
}


def get_theme_by_preset(preset: ThemePreset) -> Theme:
    """Get a theme by its preset.
    
    Args:
        preset: Theme preset to retrieve
        
    Returns:
        Theme instance
    """
    return THEMES[preset]


def get_all_themes() -> list[Theme]:
    """Get all available themes.
    
    Returns:
        List of all theme instances
    """
    return list(THEMES.values())


def generate_css(theme: Theme) -> str:
    """Generate CSS string for a theme.
    
    Args:
        theme: Theme to generate CSS for
        
    Returns:
        CSS string
    """
    colors = theme.colors
    
    # Layout spacing based on layout setting
    padding = {
        Layout.COMPACT: "0",
        Layout.COMFORTABLE: "1",
        Layout.SPACIOUS: "2",
    }[theme.layout]
    
    margin = {
        Layout.COMPACT: "0",
        Layout.COMFORTABLE: "1",
        Layout.SPACIOUS: "1 2",
    }[theme.layout]
    
    list_item_padding = {
        Layout.COMPACT: "0 1",
        Layout.COMFORTABLE: "0 2",
        Layout.SPACIOUS: "1 2",
    }[theme.layout]
    
    # Font size is handled by terminal/system settings, not CSS
    # We use the layout spacing to give a sense of size
    
    css = f"""
    Screen {{
        background: {colors.background};
    }}
    
    Header {{
        background: {colors.header_bg};
        color: {colors.highlight_fg};
        text-style: bold;
    }}
    
    #todo-container {{
        height: 100%;
        border: heavy {colors.border};
        background: {colors.background};
    }}
    
    #todo-list {{
        height: 1fr;
        border: round {colors.primary};
        margin: {margin};
        background: {colors.background};
    }}
    
    #input-container {{
        height: auto;
        padding: {padding};
        background: {colors.input_bg};
        border: solid {colors.secondary};
    }}
    
    Input {{
        margin: 0 1;
        border: solid {colors.input_border};
        background: {colors.input_bg};
        color: {colors.foreground};
    }}
    
    Input:focus {{
        border: heavy {colors.primary};
        background: {colors.input_bg};
    }}
    
    Input > .input--placeholder {{
        color: {colors.secondary};
        text-style: italic;
    }}
    
    Static {{
        color: {colors.primary};
        text-style: bold;
    }}
    
    ListView {{
        height: 100%;
        background: {colors.background};
    }}
    
    ListView > ListItem {{
        background: {colors.background};
        color: {colors.foreground};
        padding: {list_item_padding};
    }}
    
    ListView > ListItem:hover {{
        background: {colors.secondary};
        color: {colors.highlight_fg};
    }}
    
    ListView > ListItem.--highlight {{
        background: {colors.highlight_bg};
        color: {colors.highlight_fg};
        text-style: bold;
    }}
    
    .dim {{
        color: {colors.completed_text};
        text-style: dim strikethrough;
    }}
    
    .postponed {{
        color: {colors.postponed_text};
        text-style: italic bold;
        background: {colors.postponed_bg};
    }}
    
    Footer {{
        background: {colors.footer_bg};
        color: {colors.highlight_fg};
    }}
    
    Footer > .footer--key {{
        background: {colors.success};
        color: {colors.background};
        text-style: bold;
    }}
    
    Footer > .footer--description {{
        color: {colors.highlight_fg};
        text-style: italic;
    }}
    """
    
    return css
