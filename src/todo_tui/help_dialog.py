"""Help dialog for displaying keyboard shortcuts."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static, Label
from textual.binding import Binding


class ShortcutItem(Static):
    """A single keyboard shortcut item."""
    
    def __init__(self, key: str, action: str, description: str) -> None:
        """Initialize the shortcut item.
        
        Args:
            key: The keyboard key(s) for the shortcut
            action: The action name
            description: Description of what the shortcut does
        """
        super().__init__()
        self.key = key
        self.action = action
        self.description = description
    
    def render(self) -> str:
        """Render the shortcut item."""
        return f"[bold cyan]{self.key:15}[/] [yellow]{self.description}[/]"


class HelpDialog(ModalScreen):
    """Modal dialog for displaying keyboard shortcuts and help."""
    
    CSS = """
    HelpDialog {
        align: center middle;
    }
    
    #help-container {
        width: 80;
        height: auto;
        max-height: 90%;
        background: $surface;
        border: heavy $primary;
        padding: 1 2;
    }
    
    #help-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 1;
    }
    
    #search-container {
        width: 100%;
        height: auto;
        padding: 1 0;
    }
    
    #search-input {
        width: 100%;
        border: round $accent;
    }
    
    #shortcuts-container {
        width: 100%;
        height: auto;
        max-height: 25;
        border: round $primary;
        padding: 1;
        margin: 1 0;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0;
    }
    
    Button {
        margin: 0 1;
    }
    
    .shortcut-section {
        width: 100%;
        text-style: bold underline;
        color: $accent;
        padding: 1 0 0 0;
    }
    
    .shortcut-item {
        width: 100%;
        padding: 0 2;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
        Binding("ctrl+e", "export_shortcuts", "Export", show=False),
        Binding("slash", "focus_search", "Search", show=False),
    ]
    
    def __init__(self, keybindings_manager=None) -> None:
        """Initialize the help dialog.
        
        Args:
            keybindings_manager: Optional KeyBindingsManager to show custom bindings
        """
        super().__init__()
        self.keybindings_manager = keybindings_manager
        self.shortcuts = self._get_shortcuts()
        self.filtered_shortcuts = self.shortcuts.copy()
    
    def _get_shortcuts(self) -> dict[str, list[tuple[str, str, str]]]:
        """Get all keyboard shortcuts organized by category.
        
        Returns:
            Dictionary mapping category names to lists of (key, action, description) tuples
        """
        # Get custom bindings if available, otherwise use defaults
        if self.keybindings_manager:
            bindings = self.keybindings_manager.get_all_bindings()
        else:
            bindings = {
                "quit": "q",
                "help": "question_mark",
                "toggle": "space",
                "delete": "d",
                "postpone": "p",
                "focus_next": "tab",
                "focus_previous": "shift+tab",
            }
        
        # Format key names for display
        def format_key(key: str) -> str:
            """Format key name for display."""
            key_map = {
                "question_mark": "?",
                "space": "Space",
                "tab": "Tab",
                "shift+tab": "Shift+Tab",
            }
            return key_map.get(key, key.upper() if len(key) == 1 else key)
        
        return {
            "Navigation": [
                ("↑ / k", "up", "Move up in the list"),
                ("↓ / j", "down", "Move down in the list"),
                (format_key(bindings.get("focus_next", "tab")), "focus_next", "Switch between list and input field"),
                (format_key(bindings.get("focus_previous", "shift+tab")), "focus_previous", "Switch backwards between elements"),
            ],
            "Task Management": [
                ("Enter", "submit", "Add new TODO (when in input field)"),
                (format_key(bindings.get("toggle", "space")), "toggle", "Toggle TODO completion status"),
                (format_key(bindings.get("delete", "d")), "delete", "Delete selected TODO"),
                (format_key(bindings.get("postpone", "p")), "postpone", "Postpone selected TODO until tomorrow"),
            ],
            "Help & Info": [
                (format_key(bindings.get("help", "?")), "help", "Show this help dialog"),
                (format_key(bindings.get("quit", "q")), "quit", "Quit application"),
            ],
            "Help Dialog": [
                ("/", "search", "Search/filter shortcuts"),
                ("Esc", "close", "Close this help dialog"),
                ("Ctrl+E", "export_shortcuts", "Export shortcuts to Markdown file"),
            ],
        }
    
    def compose(self) -> ComposeResult:
        """Compose the help dialog."""
        with Container(id="help-container"):
            yield Label("⌨️  Keyboard Shortcuts Reference  ⌨️", id="help-title")
            
            with Vertical(id="search-container"):
                yield Label("🔍 Search shortcuts:")
                yield Input(
                    placeholder="Type to filter shortcuts...",
                    id="search-input"
                )
            
            with VerticalScroll(id="shortcuts-container"):
                yield from self._render_shortcuts()
            
            with Container(id="button-container"):
                yield Button("Export to File (Ctrl+E)", variant="primary", id="export-btn")
                yield Button("Close (Esc)", variant="default", id="close-btn")
    
    def _render_shortcuts(self) -> list[Static]:
        """Render the shortcuts list based on current filter.
        
        Returns:
            List of widgets to display
        """
        widgets = []
        for category, shortcuts in self.filtered_shortcuts.items():
            if shortcuts:  # Only show category if it has shortcuts
                widgets.append(Label(category, classes="shortcut-section"))
                for key, action, description in shortcuts:
                    widgets.append(ShortcutItem(key, action, description))
        
        if not any(self.filtered_shortcuts.values()):
            widgets.append(Label("No shortcuts found matching your search.", classes="shortcut-item"))
        
        return widgets
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes.
        
        Args:
            event: The input changed event
        """
        if event.input.id == "search-input":
            search_term = event.value.lower().strip()
            
            if not search_term:
                # Show all shortcuts if search is empty
                self.filtered_shortcuts = self.shortcuts.copy()
            else:
                # Filter shortcuts based on search term
                self.filtered_shortcuts = {}
                for category, shortcuts in self.shortcuts.items():
                    filtered = [
                        (key, action, desc)
                        for key, action, desc in shortcuts
                        if (search_term in key.lower() or
                            search_term in action.lower() or
                            search_term in desc.lower())
                    ]
                    if filtered:
                        self.filtered_shortcuts[category] = filtered
            
            # Refresh the shortcuts display
            container = self.query_one("#shortcuts-container", VerticalScroll)
            container.remove_children()
            for widget in self._render_shortcuts():
                container.mount(widget)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "close-btn":
            self.dismiss()
        elif event.button.id == "export-btn":
            self.action_export_shortcuts()
    
    def action_export_shortcuts(self) -> None:
        """Export keyboard shortcuts to a Markdown file."""
        from pathlib import Path
        
        # Generate markdown content
        content = ["# TODO TUI - Keyboard Shortcuts Reference\n"]
        content.append("This document lists all available keyboard shortcuts in the TODO TUI application.\n")
        content.append(f"Generated: {self._get_current_datetime()}\n")
        
        for category, shortcuts in self.shortcuts.items():
            content.append(f"\n## {category}\n")
            content.append("| Key | Action | Description |")
            content.append("|-----|--------|-------------|")
            for key, action, description in shortcuts:
                # Escape pipe characters in content
                key_escaped = key.replace("|", "\\|")
                action_escaped = action.replace("|", "\\|")
                desc_escaped = description.replace("|", "\\|")
                content.append(f"| `{key_escaped}` | {action_escaped} | {desc_escaped} |")
        
        content.append("\n---\n")
        content.append("## Tips\n")
        content.append("- Press `?` anytime in the app to view this help\n")
        content.append("- Use `/` in the help dialog to search for specific shortcuts\n")
        content.append("- All shortcuts are case-insensitive unless specified\n")
        content.append("- Combine modifiers (Shift, Ctrl) with other keys for additional actions\n")
        
        # Save to file
        shortcuts_file = Path.home() / "todo-tui-shortcuts.md"
        try:
            shortcuts_file.write_text("\n".join(content))
            self.app.notify(
                f"Shortcuts exported to: {shortcuts_file}",
                title="Export Successful",
                timeout=5
            )
        except Exception as e:
            self.app.notify(
                f"Failed to export shortcuts: {e}",
                severity="error",
                title="Export Failed"
            )
    
    def _get_current_datetime(self) -> str:
        """Get current date and time as formatted string.
        
        Returns:
            Formatted datetime string
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def action_dismiss(self) -> None:
        """Close the help dialog."""
        self.dismiss()
    
    def action_focus_search(self) -> None:
        """Focus the search input field."""
        search_input = self.query_one("#search-input", Input)
        search_input.focus()
