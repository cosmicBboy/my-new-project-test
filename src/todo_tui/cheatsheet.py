"""Print-friendly cheat sheet generator."""

from pathlib import Path
from datetime import datetime
from typing import List
from .help_overlay import KeyboardShortcut


class CheatSheetGenerator:
    """Generates print-friendly keyboard shortcut cheat sheets."""
    
    def __init__(self, shortcuts: List[KeyboardShortcut]):
        """Initialize the generator.
        
        Args:
            shortcuts: List of keyboard shortcuts to include
        """
        self.shortcuts = shortcuts
    
    def generate_text(self) -> str:
        """Generate a plain text cheat sheet.
        
        Returns:
            Plain text cheat sheet
        """
        lines = []
        lines.append("=" * 70)
        lines.append("TODO TUI - Keyboard Shortcuts Cheat Sheet")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Group by category
        categories = {}
        for shortcut in self.shortcuts:
            if shortcut.category not in categories:
                categories[shortcut.category] = []
            categories[shortcut.category].append(shortcut)
        
        # Display shortcuts by category
        for category in ["Navigation", "Task Management", "Application"]:
            if category not in categories:
                continue
            
            lines.append("")
            lines.append(f"── {category} " + "─" * (68 - len(category) - 4))
            lines.append("")
            
            for shortcut in categories[category]:
                lines.append(f"  {shortcut.key:15} {shortcut.action:20} {shortcut.description}")
        
        lines.append("")
        lines.append("=" * 70)
        lines.append("")
        lines.append("Tips:")
        lines.append("  • Press '?' in the app for interactive help with search")
        lines.append("  • Press 'c' to customize key bindings")
        lines.append("  • Press 't' to replay the tutorial")
        lines.append("  • All changes are automatically saved")
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def generate_markdown(self) -> str:
        """Generate a Markdown cheat sheet.
        
        Returns:
            Markdown formatted cheat sheet
        """
        lines = []
        lines.append("# TODO TUI - Keyboard Shortcuts Cheat Sheet")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Group by category
        categories = {}
        for shortcut in self.shortcuts:
            if shortcut.category not in categories:
                categories[shortcut.category] = []
            categories[shortcut.category].append(shortcut)
        
        # Display shortcuts by category
        for category in ["Navigation", "Task Management", "Application"]:
            if category not in categories:
                continue
            
            lines.append(f"## {category}")
            lines.append("")
            lines.append("| Key | Action | Description |")
            lines.append("|-----|--------|-------------|")
            
            for shortcut in categories[category]:
                key = shortcut.key.replace("|", "\\|")
                action = shortcut.action.replace("|", "\\|")
                description = shortcut.description.replace("|", "\\|")
                lines.append(f"| `{key}` | **{action}** | {description} |")
            
            lines.append("")
        
        lines.append("## Tips")
        lines.append("")
        lines.append("- Press `?` in the app for interactive help with search")
        lines.append("- Press `c` to customize key bindings")
        lines.append("- Press `t` to replay the tutorial")
        lines.append("- All changes are automatically saved")
        lines.append("")
        
        return "\n".join(lines)
    
    def export_to_file(self, file_path: Path, format: str = "text") -> None:
        """Export cheat sheet to a file.
        
        Args:
            file_path: Path to save the file
            format: Output format ('text' or 'markdown')
        """
        if format == "markdown":
            content = self.generate_markdown()
        else:
            content = self.generate_text()
        
        file_path.write_text(content)


def export_cheat_sheet(shortcuts: List[KeyboardShortcut], output_path: Path = None) -> Path:
    """Export a cheat sheet to a file.
    
    Args:
        shortcuts: List of keyboard shortcuts
        output_path: Optional output path, defaults to home directory
        
    Returns:
        Path to the exported file
    """
    if output_path is None:
        output_path = Path.home() / "todo-tui-shortcuts.txt"
    
    generator = CheatSheetGenerator(shortcuts)
    
    # Determine format from file extension
    if output_path.suffix in [".md", ".markdown"]:
        format = "markdown"
    else:
        format = "text"
    
    generator.export_to_file(output_path, format)
    return output_path
