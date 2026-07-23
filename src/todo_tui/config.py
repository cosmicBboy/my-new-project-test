"""Configuration management for the TODO TUI app.

Handles loading and saving user preferences including theme settings.
"""

import json
from pathlib import Path
from typing import Optional

from .themes import Theme, ThemePreset, FontSize, Layout, get_theme_by_preset


class Config:
    """Manages application configuration and preferences.
    
    Attributes:
        config_path: Path to the configuration file
        theme: Currently selected theme
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Custom path for config file. Defaults to ~/.todo-tui-config.json
        """
        if config_path is None:
            config_path = Path.home() / ".todo-tui-config.json"
        self.config_path = config_path
        self.theme = self._load_theme()
    
    def _load_theme(self) -> Theme:
        """Load theme from configuration file.
        
        Returns:
            Theme instance (default if config doesn't exist)
        """
        if not self.config_path.exists():
            # Return default theme (Cyberpunk to maintain current appearance)
            return get_theme_by_preset(ThemePreset.CYBERPUNK)
        
        try:
            data = json.loads(self.config_path.read_text())
            theme_data = data.get("theme", {})
            return Theme.from_dict(theme_data)
        except (json.JSONDecodeError, KeyError, ValueError):
            # If config is corrupted, return default theme
            return get_theme_by_preset(ThemePreset.CYBERPUNK)
    
    def save_theme(self, theme: Theme) -> None:
        """Save theme to configuration file.
        
        Args:
            theme: Theme to save
        """
        self.theme = theme
        
        # Load existing config or create new one
        if self.config_path.exists():
            try:
                data = json.loads(self.config_path.read_text())
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}
        
        # Update theme section
        data["theme"] = theme.to_dict()
        
        # Save to file
        self.config_path.write_text(json.dumps(data, indent=2))
    
    def cycle_theme(self) -> Theme:
        """Cycle to the next theme in the list.
        
        Returns:
            The new theme
        """
        presets = list(ThemePreset)
        current_index = presets.index(self.theme.preset)
        next_index = (current_index + 1) % len(presets)
        new_theme = get_theme_by_preset(presets[next_index])
        
        # Preserve font size and layout settings
        new_theme.font_size = self.theme.font_size
        new_theme.layout = self.theme.layout
        
        self.save_theme(new_theme)
        return new_theme
    
    def set_font_size(self, font_size: FontSize) -> None:
        """Set font size preference.
        
        Args:
            font_size: Font size to set
        """
        self.theme.font_size = font_size
        self.save_theme(self.theme)
    
    def set_layout(self, layout: Layout) -> None:
        """Set layout spacing preference.
        
        Args:
            layout: Layout to set
        """
        self.theme.layout = layout
        self.save_theme(self.theme)
    
    def cycle_font_size(self) -> FontSize:
        """Cycle to the next font size.
        
        Returns:
            The new font size
        """
        sizes = list(FontSize)
        current_index = sizes.index(self.theme.font_size)
        next_index = (current_index + 1) % len(sizes)
        new_size = sizes[next_index]
        self.set_font_size(new_size)
        return new_size
    
    def cycle_layout(self) -> Layout:
        """Cycle to the next layout.
        
        Returns:
            The new layout
        """
        layouts = list(Layout)
        current_index = layouts.index(self.theme.layout)
        next_index = (current_index + 1) % len(layouts)
        new_layout = layouts[next_index]
        self.set_layout(new_layout)
        return new_layout
