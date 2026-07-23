"""Help overlay for displaying keyboard shortcuts."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static
from textual.binding import Binding


class KeyboardShortcut:
    """Represents a keyboard shortcut with metadata."""
    
    def __init__(
        self,
        key: str,
        action: str,
        description: str,
        category: str = "General"
    ):
        """Initialize a keyboard shortcut.
        
        Args:
            key: The key or key combination
            action: The action name
            description: Detailed description of what the shortcut does
            category: Category for grouping shortcuts
        """
        self.key = key
        self.action = action
        self.description = description
        self.category = category
    
    def matches_search(self, query: str) -> bool:
        """Check if this shortcut matches a search query.
        
        Args:
            query: The search query
            
        Returns:
            True if the shortcut matches the query
        """
        query_lower = query.lower()
        return (
            query_lower in self.key.lower()
            or query_lower in self.action.lower()
            or query_lower in self.description.lower()
            or query_lower in self.category.lower()
        )


class HelpOverlay(ModalScreen):
    """Modal overlay displaying keyboard shortcuts."""
    
    CSS = """
    HelpOverlay {
        align: center middle;
    }
    
    #help-dialog {
        width: 80;
        height: auto;
        max-height: 90%;
        border: heavy #8338ec;
        background: #0f1425;
        padding: 1 2;
    }
    
    #help-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: #ff006e;
        background: #1a1f3a;
        padding: 1;
        margin-bottom: 1;
    }
    
    #search-container {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    
    #search-label {
        color: #06ffa5;
        text-style: bold;
        margin-bottom: 1;
    }
    
    #search-input {
        width: 100%;
        border: solid #06ffa5;
        background: #1a1f3a;
        color: #06ffa5;
    }
    
    #search-input:focus {
        border: heavy #ff006e;
        background: #240046;
    }
    
    #shortcuts-scroll {
        width: 100%;
        height: 1fr;
        border: round #3a86ff;
        background: #0f1425;
        margin-bottom: 1;
    }
    
    #shortcuts-container {
        width: 100%;
        height: auto;
        padding: 1;
    }
    
    .category-header {
        width: 100%;
        text-style: bold;
        color: #8338ec;
        background: #1a1f3a;
        padding: 1;
        margin-top: 1;
        margin-bottom: 1;
    }
    
    .shortcut-row {
        width: 100%;
        height: auto;
        padding: 0 1;
        margin-bottom: 1;
    }
    
    .shortcut-key {
        width: 15;
        text-style: bold;
        color: #ff006e;
        background: #240046;
        padding: 0 1;
        border: solid #ff006e;
    }
    
    .shortcut-action {
        width: 20;
        color: #ffbe0b;
        padding: 0 1;
    }
    
    .shortcut-description {
        color: #06ffa5;
        padding: 0 1;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1;
    }
    
    #close-button {
        min-width: 20;
        background: #8338ec;
        color: #ffffff;
        border: heavy #ff006e;
    }
    
    #close-button:hover {
        background: #ff006e;
        border: heavy #8338ec;
    }
    
    .no-results {
        width: 100%;
        content-align: center middle;
        color: #ffbe0b;
        text-style: italic;
        padding: 2;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
        Binding("q", "dismiss", "Close", show=False),
    ]
    
    def __init__(self):
        """Initialize the help overlay."""
        super().__init__()
        self.shortcuts = self._get_shortcuts()
        self.search_query = ""
    
    def _get_shortcuts(self) -> list[KeyboardShortcut]:
        """Get all keyboard shortcuts.
        
        Returns:
            List of keyboard shortcuts
        """
        return [
            # Navigation
            KeyboardShortcut(
                "↑ / k",
                "Move Up",
                "Navigate to the previous TODO item in the list",
                "Navigation"
            ),
            KeyboardShortcut(
                "↓ / j",
                "Move Down",
                "Navigate to the next TODO item in the list",
                "Navigation"
            ),
            KeyboardShortcut(
                "Home",
                "First Item",
                "Jump to the first TODO item in the list",
                "Navigation"
            ),
            KeyboardShortcut(
                "End",
                "Last Item",
                "Jump to the last TODO item in the list",
                "Navigation"
            ),
            KeyboardShortcut(
                "Tab",
                "Switch Focus",
                "Switch between the TODO list and the input field",
                "Navigation"
            ),
            
            # Task Management
            KeyboardShortcut(
                "Enter",
                "Add TODO",
                "Add a new TODO item (when input field is focused)",
                "Task Management"
            ),
            KeyboardShortcut(
                "Space",
                "Toggle",
                "Toggle completion status of the selected TODO item",
                "Task Management"
            ),
            KeyboardShortcut(
                "d",
                "Delete",
                "Delete the selected TODO item permanently",
                "Task Management"
            ),
            KeyboardShortcut(
                "p",
                "Postpone",
                "Postpone the selected TODO item until tomorrow",
                "Task Management"
            ),
            KeyboardShortcut(
                "e",
                "Export",
                "Export TODO items to a file",
                "Task Management"
            ),
            KeyboardShortcut(
                "i",
                "Import",
                "Import TODO items from a file",
                "Task Management"
            ),
            
            # Application
            KeyboardShortcut(
                "?",
                "Help",
                "Show this help overlay with all keyboard shortcuts",
                "Application"
            ),
            KeyboardShortcut(
                "c",
                "Customize Keys",
                "Customize keyboard bindings",
                "Application"
            ),
            KeyboardShortcut(
                "x",
                "Export Cheat Sheet",
                "Export shortcuts to a print-friendly cheat sheet",
                "Application"
            ),
            KeyboardShortcut(
                "t",
                "Tutorial",
                "Show the tutorial for new users",
                "Application"
            ),
            KeyboardShortcut(
                "q",
                "Quit",
                "Exit the application (data is automatically saved)",
                "Application"
            ),
            KeyboardShortcut(
                "Esc",
                "Close Dialog",
                "Close the current dialog or help overlay",
                "Application"
            ),
        ]
    
    def compose(self) -> ComposeResult:
        """Compose the help overlay."""
        with Container(id="help-dialog"):
            yield Static("⌨️  Keyboard Shortcuts Reference  ⌨️", id="help-title")
            
            with Container(id="search-container"):
                yield Label("🔍 Search shortcuts:", id="search-label")
                yield Input(
                    placeholder="Type to search...",
                    id="search-input"
                )
            
            with VerticalScroll(id="shortcuts-scroll"):
                yield Container(id="shortcuts-container")
            
            with Container(id="button-container"):
                yield Button("Close (Esc)", id="close-button", variant="primary")
    
    def on_mount(self) -> None:
        """Handle mount event."""
        self._refresh_shortcuts()
        # Focus the search input
        self.query_one("#search-input", Input).focus()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes.
        
        Args:
            event: The input changed event
        """
        if event.input.id == "search-input":
            self.search_query = event.value
            self._refresh_shortcuts()
    
    def _refresh_shortcuts(self) -> None:
        """Refresh the shortcuts display based on search query."""
        container = self.query_one("#shortcuts-container", Container)
        container.remove_children()
        
        # Filter shortcuts based on search query
        if self.search_query:
            filtered = [
                s for s in self.shortcuts
                if s.matches_search(self.search_query)
            ]
        else:
            filtered = self.shortcuts
        
        if not filtered:
            container.mount(Label("No shortcuts found matching your search.", classes="no-results"))
            return
        
        # Group by category
        categories = {}
        for shortcut in filtered:
            if shortcut.category not in categories:
                categories[shortcut.category] = []
            categories[shortcut.category].append(shortcut)
        
        # Display shortcuts by category
        for category in ["Navigation", "Task Management", "Application"]:
            if category not in categories:
                continue
            
            container.mount(Label(f"━━ {category} ━━", classes="category-header"))
            
            for shortcut in categories[category]:
                with container:
                    with Vertical(classes="shortcut-row"):
                        row_text = f"[bold #ff006e]{shortcut.key:15}[/] "
                        row_text += f"[#ffbe0b]{shortcut.action:20}[/] "
                        row_text += f"[#06ffa5]{shortcut.description}[/]"
                        container.mount(Label(row_text))
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "close-button":
            self.dismiss()
    
    def action_dismiss(self) -> None:
        """Dismiss the help overlay."""
        self.dismiss()
