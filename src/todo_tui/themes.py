"""Theme definitions and management for the TODO TUI app."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Any


class ThemeName(str, Enum):
    """Available theme names."""
    DARK = "dark"
    LIGHT = "light"
    HIGH_CONTRAST = "high_contrast"
    COLORFUL = "colorful"


class LayoutDensity(str, Enum):
    """Layout density options."""
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    SPACIOUS = "spacious"


class FontSize(str, Enum):
    """Font size options."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass
class Theme:
    """Represents a visual theme for the app.
    
    Attributes:
        name: Unique identifier for the theme
        display_name: Human-readable name
        css: CSS string for the theme
    """
    name: str
    display_name: str
    css: str


def get_base_css() -> str:
    """Get base CSS that includes font size definitions.
    
    Returns:
        Base CSS string with font size classes
    """
    return """
    /* Font size classes */
    .font-small Screen {
        text-size: 14px;
    }
    
    .font-small Header {
        text-size: 16px;
    }
    
    .font-small Footer {
        text-size: 14px;
    }
    
    .font-small ListView > ListItem {
        text-size: 14px;
    }
    
    .font-medium Screen {
        text-size: 16px;
    }
    
    .font-medium Header {
        text-size: 18px;
    }
    
    .font-medium Footer {
        text-size: 16px;
    }
    
    .font-medium ListView > ListItem {
        text-size: 16px;
    }
    
    .font-large Screen {
        text-size: 18px;
    }
    
    .font-large Header {
        text-size: 20px;
    }
    
    .font-large Footer {
        text-size: 18px;
    }
    
    .font-large ListView > ListItem {
        text-size: 18px;
    }
    """


# Define built-in themes
THEMES: Dict[str, Theme] = {
    ThemeName.DARK: Theme(
        name=ThemeName.DARK,
        display_name="Dark",
        css="""
        Screen {
            background: #1e1e2e;
        }
        
        Header {
            background: #313244;
            color: #cdd6f4;
            text-style: bold;
        }
        
        #todo-container {
            height: 100%;
            border: heavy #45475a;
            background: #1e1e2e;
        }
        
        #todo-list {
            height: 1fr;
            border: round #45475a;
            margin: 1;
            background: #181825;
        }
        
        #input-container {
            height: auto;
            padding: 1;
            background: #313244;
            border: solid #45475a;
        }
        
        Input {
            margin: 0 1;
            border: solid #89b4fa;
            background: #1e1e2e;
            color: #cdd6f4;
        }
        
        Input:focus {
            border: heavy #89b4fa;
            background: #313244;
        }
        
        Input > .input--placeholder {
            color: #6c7086;
            text-style: italic;
        }
        
        Static {
            color: #89b4fa;
            text-style: bold;
        }
        
        ListView {
            height: 100%;
            background: #181825;
        }
        
        ListView > ListItem {
            background: #1e1e2e;
            color: #cdd6f4;
            padding: 0 2;
        }
        
        ListView > ListItem:hover {
            background: #313244;
            color: #cdd6f4;
        }
        
        ListView > ListItem.--highlight {
            background: #45475a;
            color: #cdd6f4;
            text-style: bold;
        }
        
        .dim {
            color: #6c7086;
            text-style: dim strikethrough;
        }
        
        .postponed {
            color: #f9e2af;
            text-style: italic bold;
            background: #313244;
        }
        
        Footer {
            background: #313244;
            color: #cdd6f4;
        }
        
        Footer > .footer--key {
            background: #89b4fa;
            color: #1e1e2e;
            text-style: bold;
        }
        
        Footer > .footer--description {
            color: #cdd6f4;
            text-style: italic;
        }
        """
    ),
    
    ThemeName.LIGHT: Theme(
        name=ThemeName.LIGHT,
        display_name="Light",
        css="""
        Screen {
            background: #eff1f5;
        }
        
        Header {
            background: #dce0e8;
            color: #4c4f69;
            text-style: bold;
        }
        
        #todo-container {
            height: 100%;
            border: heavy #9ca0b0;
            background: #eff1f5;
        }
        
        #todo-list {
            height: 1fr;
            border: round #9ca0b0;
            margin: 1;
            background: #e6e9ef;
        }
        
        #input-container {
            height: auto;
            padding: 1;
            background: #dce0e8;
            border: solid #9ca0b0;
        }
        
        Input {
            margin: 0 1;
            border: solid #1e66f5;
            background: #eff1f5;
            color: #4c4f69;
        }
        
        Input:focus {
            border: heavy #1e66f5;
            background: #dce0e8;
        }
        
        Input > .input--placeholder {
            color: #9ca0b0;
            text-style: italic;
        }
        
        Static {
            color: #1e66f5;
            text-style: bold;
        }
        
        ListView {
            height: 100%;
            background: #e6e9ef;
        }
        
        ListView > ListItem {
            background: #eff1f5;
            color: #4c4f69;
            padding: 0 2;
        }
        
        ListView > ListItem:hover {
            background: #dce0e8;
            color: #4c4f69;
        }
        
        ListView > ListItem.--highlight {
            background: #9ca0b0;
            color: #4c4f69;
            text-style: bold;
        }
        
        .dim {
            color: #9ca0b0;
            text-style: dim strikethrough;
        }
        
        .postponed {
            color: #df8e1d;
            text-style: italic bold;
            background: #dce0e8;
        }
        
        Footer {
            background: #dce0e8;
            color: #4c4f69;
        }
        
        Footer > .footer--key {
            background: #1e66f5;
            color: #eff1f5;
            text-style: bold;
        }
        
        Footer > .footer--description {
            color: #4c4f69;
            text-style: italic;
        }
        """
    ),
    
    ThemeName.HIGH_CONTRAST: Theme(
        name=ThemeName.HIGH_CONTRAST,
        display_name="High Contrast",
        css="""
        Screen {
            background: #000000;
        }
        
        Header {
            background: #ffffff;
            color: #000000;
            text-style: bold;
        }
        
        #todo-container {
            height: 100%;
            border: heavy #ffffff;
            background: #000000;
        }
        
        #todo-list {
            height: 1fr;
            border: round #ffffff;
            margin: 1;
            background: #000000;
        }
        
        #input-container {
            height: auto;
            padding: 1;
            background: #000000;
            border: solid #ffffff;
        }
        
        Input {
            margin: 0 1;
            border: solid #ffffff;
            background: #000000;
            color: #ffffff;
        }
        
        Input:focus {
            border: heavy #ffff00;
            background: #000000;
        }
        
        Input > .input--placeholder {
            color: #808080;
            text-style: italic;
        }
        
        Static {
            color: #ffffff;
            text-style: bold;
        }
        
        ListView {
            height: 100%;
            background: #000000;
        }
        
        ListView > ListItem {
            background: #000000;
            color: #ffffff;
            padding: 0 2;
        }
        
        ListView > ListItem:hover {
            background: #333333;
            color: #ffffff;
        }
        
        ListView > ListItem.--highlight {
            background: #ffffff;
            color: #000000;
            text-style: bold;
        }
        
        .dim {
            color: #808080;
            text-style: dim strikethrough;
        }
        
        .postponed {
            color: #ffff00;
            text-style: italic bold;
            background: #333333;
        }
        
        Footer {
            background: #ffffff;
            color: #000000;
        }
        
        Footer > .footer--key {
            background: #000000;
            color: #ffffff;
            text-style: bold;
        }
        
        Footer > .footer--description {
            color: #000000;
            text-style: italic;
        }
        """
    ),
    
    ThemeName.COLORFUL: Theme(
        name=ThemeName.COLORFUL,
        display_name="Colorful (Cyberpunk)",
        css="""
        Screen {
            background: #0a0e27;
        }
        
        Header {
            background: linear-gradient(90deg, #ff006e 0%, #8338ec 50%, #3a86ff 100%);
            color: #ffffff;
            text-style: bold;
        }
        
        #todo-container {
            height: 100%;
            border: heavy #ff006e;
            background: #1a1f3a;
        }
        
        #todo-list {
            height: 1fr;
            border: round #3a86ff;
            margin: 1;
            background: #0f1425;
        }
        
        #input-container {
            height: auto;
            padding: 1;
            background: linear-gradient(135deg, #240046 0%, #10002b 100%);
            border: solid #8338ec;
        }
        
        Input {
            margin: 0 1;
            border: solid #06ffa5;
            background: #1a1f3a;
            color: #06ffa5;
        }
        
        Input:focus {
            border: heavy #ff006e;
            background: #240046;
        }
        
        Input > .input--placeholder {
            color: #7209b7;
            text-style: italic;
        }
        
        Static {
            color: #ff006e;
            text-style: bold;
        }
        
        ListView {
            height: 100%;
            background: #0f1425;
        }
        
        ListView > ListItem {
            background: #1a1f3a;
            color: #06ffa5;
            padding: 0 2;
        }
        
        ListView > ListItem:hover {
            background: #240046;
            color: #ffbe0b;
        }
        
        ListView > ListItem.--highlight {
            background: linear-gradient(90deg, #8338ec 0%, #3a86ff 100%);
            color: #ffffff;
            text-style: bold;
        }
        
        .dim {
            color: #7209b7;
            text-style: dim strikethrough;
        }
        
        .postponed {
            color: #ffbe0b;
            text-style: italic bold;
            background: #3a0f51;
        }
        
        Footer {
            background: linear-gradient(90deg, #3a86ff 0%, #8338ec 50%, #ff006e 100%);
            color: #ffffff;
        }
        
        Footer > .footer--key {
            background: #06ffa5;
            color: #0a0e27;
            text-style: bold;
        }
        
        Footer > .footer--description {
            color: #ffffff;
            text-style: italic;
        }
        """
    ),
}


def get_layout_padding(density: LayoutDensity) -> int:
    """Get padding value for layout density.
    
    Args:
        density: The layout density setting
        
    Returns:
        Padding value in spaces
    """
    padding_map = {
        LayoutDensity.COMPACT: 0,
        LayoutDensity.COMFORTABLE: 1,
        LayoutDensity.SPACIOUS: 2,
    }
    return padding_map.get(density, 1)


def get_layout_margin(density: LayoutDensity) -> int:
    """Get margin value for layout density.
    
    Args:
        density: The layout density setting
        
    Returns:
        Margin value in spaces
    """
    margin_map = {
        LayoutDensity.COMPACT: 0,
        LayoutDensity.COMFORTABLE: 1,
        LayoutDensity.SPACIOUS: 2,
    }
    return margin_map.get(density, 1)


def get_font_size_class(size: FontSize) -> str:
    """Get CSS class modifier for font size.
    
    Args:
        size: The font size setting
        
    Returns:
        CSS class name suffix
    """
    return f"font-{size.value}"


def create_custom_theme(name: str, display_name: str, colors: Dict[str, str]) -> Theme:
    """Create a custom theme from a color palette.
    
    Args:
        name: Unique identifier for the theme
        display_name: Human-readable name
        colors: Dictionary of color keys to hex values. Supported keys:
            - background: Main background color
            - surface: Secondary background (containers)
            - text: Primary text color
            - text_dim: Dimmed/secondary text color
            - accent: Accent/highlight color
            - border: Border color
            - completed: Color for completed items
            - postponed: Color for postponed items
            
    Returns:
        Theme object with generated CSS
        
    Example:
        >>> theme = create_custom_theme(
        ...     name="custom_blue",
        ...     display_name="Custom Blue",
        ...     colors={
        ...         "background": "#1a1d29",
        ...         "surface": "#252936",
        ...         "text": "#e0e0e0",
        ...         "text_dim": "#707070",
        ...         "accent": "#4a9eff",
        ...         "border": "#3a3d49",
        ...         "completed": "#909090",
        ...         "postponed": "#ffaa00",
        ...     }
        ... )
    """
    # Set defaults for any missing colors
    defaults = {
        "background": "#1e1e2e",
        "surface": "#313244",
        "text": "#cdd6f4",
        "text_dim": "#6c7086",
        "accent": "#89b4fa",
        "border": "#45475a",
        "completed": "#6c7086",
        "postponed": "#f9e2af",
    }
    
    # Merge with defaults
    colors = {**defaults, **colors}
    
    # Generate CSS from color palette
    css = f"""
    Screen {{
        background: {colors['background']};
    }}
    
    Header {{
        background: {colors['surface']};
        color: {colors['text']};
        text-style: bold;
    }}
    
    #todo-container {{
        height: 100%;
        border: heavy {colors['border']};
        background: {colors['background']};
    }}
    
    #todo-list {{
        height: 1fr;
        border: round {colors['border']};
        margin: 1;
        background: {colors['background']};
    }}
    
    #input-container {{
        height: auto;
        padding: 1;
        background: {colors['surface']};
        border: solid {colors['border']};
    }}
    
    Input {{
        margin: 0 1;
        border: solid {colors['accent']};
        background: {colors['background']};
        color: {colors['text']};
    }}
    
    Input:focus {{
        border: heavy {colors['accent']};
        background: {colors['surface']};
    }}
    
    Input > .input--placeholder {{
        color: {colors['text_dim']};
        text-style: italic;
    }}
    
    Static {{
        color: {colors['accent']};
        text-style: bold;
    }}
    
    ListView {{
        height: 100%;
        background: {colors['background']};
    }}
    
    ListView > ListItem {{
        background: {colors['background']};
        color: {colors['text']};
        padding: 0 2;
    }}
    
    ListView > ListItem:hover {{
        background: {colors['surface']};
        color: {colors['text']};
    }}
    
    ListView > ListItem.--highlight {{
        background: {colors['border']};
        color: {colors['text']};
        text-style: bold;
    }}
    
    .dim {{
        color: {colors['completed']};
        text-style: dim strikethrough;
    }}
    
    .postponed {{
        color: {colors['postponed']};
        text-style: italic bold;
        background: {colors['surface']};
    }}
    
    Footer {{
        background: {colors['surface']};
        color: {colors['text']};
    }}
    
    Footer > .footer--key {{
        background: {colors['accent']};
        color: {colors['background']};
        text-style: bold;
    }}
    
    Footer > .footer--description {{
        color: {colors['text']};
        text-style: italic;
    }}
    """
    
    return Theme(name=name, display_name=display_name, css=css)


def load_custom_theme(theme_data: Dict[str, Any]) -> Optional[Theme]:
    """Load a custom theme from saved data.
    
    Args:
        theme_data: Dictionary with theme data including name, display_name, and colors
        
    Returns:
        Theme object or None if invalid
    """
    try:
        return create_custom_theme(
            name=theme_data["name"],
            display_name=theme_data["display_name"],
            colors=theme_data["colors"]
        )
    except KeyError:
        return None
