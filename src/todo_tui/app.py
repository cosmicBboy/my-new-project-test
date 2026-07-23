"""Main Textual application for the TODO TUI app."""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, Button
from textual.message import Message
from textual.screen import ModalScreen

from .models import TodoItem
from .storage import TodoStorage
from .config import KeyBindingConfig, AppConfig


class TodoListItem(ListItem):
    """A single TODO item in the list."""
    
    def __init__(self, todo: TodoItem) -> None:
        """Initialize the list item.
        
        Args:
            todo: The TodoItem to display
        """
        super().__init__()
        self.todo = todo
        self._update_display()
    
    def _update_display(self) -> None:
        """Update the display text based on todo state."""
        status = "✓" if self.todo.completed else " "
        style = "dim" if self.todo.completed else ""
        
        # Add postponed indicator
        postponed = ""
        if self.todo.is_postponed():
            postponed = f" [postponed until {self.todo.postpone_until}]"
            style = "postponed"
        
        self._label = Label(f"[{status}] {self.todo.title}{postponed}")
        if style:
            self._label.add_class(style)
    
    def compose(self) -> ComposeResult:
        """Compose the list item."""
        yield self._label


class ShortcutItem(Static):
    """A single shortcut item in the help overlay."""
    
    def __init__(self, key: str, description: str) -> None:
        """Initialize the shortcut item.
        
        Args:
            key: The keyboard key(s)
            description: Description of what the key does
        """
        super().__init__()
        self.key = key
        self.description = description
        self.key_text = key
        self.desc_text = description
    
    def render(self) -> str:
        """Render the shortcut item."""
        return f"[bold cyan]{self.key:20}[/] [dim white]{self.description}[/]"


class TutorialScreen(ModalScreen):
    """Modal screen displaying an interactive tutorial for new users."""
    
    CSS = """
    TutorialScreen {
        align: center middle;
    }
    
    #tutorial-dialog {
        width: 90;
        height: auto;
        max-height: 95%;
        background: $panel;
        border: heavy $accent;
        padding: 2;
    }
    
    #tutorial-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }
    
    #tutorial-content {
        width: 100%;
        height: auto;
        max-height: 35;
        padding: 1;
    }
    
    .tutorial-section {
        width: 100%;
        margin: 1 0;
    }
    
    .tutorial-heading {
        text-style: bold;
        color: $success;
    }
    
    #tutorial-footer {
        width: 100%;
        content-align: center middle;
        padding: 1 0 0 0;
    }
    
    #tutorial-button {
        margin: 1 1 0 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
        Binding("enter", "dismiss", "Close", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the tutorial dialog."""
        with Container(id="tutorial-dialog"):
            yield Static("🎓 Welcome to TODO TUI App!", id="tutorial-title")
            with VerticalScroll(id="tutorial-content"):
                yield Static("", classes="tutorial-section")
                yield Static("Let's get you started with the basics:", classes="tutorial-heading")
                yield Static("", classes="tutorial-section")
                
                yield Static("📝 Adding TODOs:", classes="tutorial-heading")
                yield Static(
                    "Press [bold]Tab[/] to focus the input field at the bottom.\n"
                    "Type your task and press [bold]Enter[/] to add it to the list.",
                    classes="tutorial-section"
                )
                
                yield Static("🎯 Managing TODOs:", classes="tutorial-heading")
                yield Static(
                    "• Use [bold]↑[/] and [bold]↓[/] (or [bold]j[/]/[bold]k[/]) to navigate\n"
                    "• Press [bold]Space[/] to toggle completion status\n"
                    "• Press [bold]d[/] to delete a TODO\n"
                    "• Press [bold]p[/] to postpone until tomorrow",
                    classes="tutorial-section"
                )
                
                yield Static("❓ Getting Help:", classes="tutorial-heading")
                yield Static(
                    "Press [bold]?[/] at any time to view all keyboard shortcuts.\n"
                    "Use the search box to quickly find specific commands.",
                    classes="tutorial-section"
                )
                
                yield Static("⚙️ Customization:", classes="tutorial-heading")
                yield Static(
                    "• Press [bold]Ctrl+K[/] to customize keyboard shortcuts\n"
                    "• Press [bold]Ctrl+H[/] to export a cheat sheet\n"
                    "• Press [bold]Ctrl+T[/] to view this tutorial again",
                    classes="tutorial-section"
                )
                
                yield Static("💾 Auto-Save:", classes="tutorial-heading")
                yield Static(
                    "Your TODOs are automatically saved to ~/.todo-tui.json\n"
                    "Press [bold]q[/] to quit - your data is always safe!",
                    classes="tutorial-section"
                )
                
                yield Static("", classes="tutorial-section")
                yield Static(
                    "💡 Tip: Start by pressing Tab and adding your first TODO!",
                    classes="tutorial-section"
                )
            
            with Container(id="tutorial-footer"):
                yield Button("Got it! Let's start!", id="tutorial-button", variant="success")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "tutorial-button":
            self.dismiss(True)
    
    def action_dismiss(self) -> None:
        """Close the tutorial dialog."""
        self.dismiss(True)


class CustomizeKeysScreen(ModalScreen):
    """Modal screen for customizing key bindings."""
    
    CSS = """
    CustomizeKeysScreen {
        align: center middle;
    }
    
    #customize-dialog {
        width: 80;
        height: auto;
        max-height: 90%;
        background: $panel;
        border: heavy $primary;
        padding: 2;
    }
    
    #customize-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }
    
    #customize-content {
        width: 100%;
        height: auto;
        max-height: 30;
        padding: 1;
    }
    
    .key-binding-item {
        width: 100%;
        margin: 0 0 1 0;
    }
    
    #customize-footer {
        width: 100%;
        content-align: center middle;
        padding: 1 0 0 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
    ]
    
    def __init__(self, key_config: KeyBindingConfig) -> None:
        """Initialize the customize keys screen.
        
        Args:
            key_config: The key binding configuration
        """
        super().__init__()
        self.key_config = key_config
    
    def compose(self) -> ComposeResult:
        """Compose the customize dialog."""
        with Container(id="customize-dialog"):
            yield Static("⚙️ Customize Keyboard Shortcuts", id="customize-title")
            with VerticalScroll(id="customize-content"):
                bindings = self.key_config.get_all_bindings()
                action_names = {
                    "quit": "Quit Application",
                    "toggle_todo": "Toggle TODO Completion",
                    "delete_todo": "Delete TODO",
                    "postpone_todo": "Postpone TODO",
                    "show_shortcuts": "Show Shortcuts Help",
                    "export_cheatsheet": "Export Cheat Sheet",
                    "customize_keys": "Customize Keys",
                    "show_tutorial": "Show Tutorial",
                }
                
                for action, key in bindings.items():
                    name = action_names.get(action, action.replace("_", " ").title())
                    yield Static(
                        f"[bold cyan]{name:30}[/] [dim white]→[/] [bold yellow]{key}[/]",
                        classes="key-binding-item"
                    )
                
                yield Static("", classes="key-binding-item")
                yield Static(
                    "[dim]To customize bindings, edit: ~/.todo-tui-keybindings.json[/]",
                    classes="key-binding-item"
                )
                yield Static(
                    "[dim]Example: {\"quit\": \"ctrl+q\", \"toggle_todo\": \"t\"}[/]",
                    classes="key-binding-item"
                )
            
            with Container(id="customize-footer"):
                yield Static(
                    "Press [bold]Escape[/] to close",
                    id="customize-footer"
                )
    
    def action_dismiss(self) -> None:
        """Close the customize dialog."""
        self.dismiss()


class KeyboardShortcutsScreen(ModalScreen):
    """Modal screen displaying keyboard shortcuts help."""
    
    CSS = """
    KeyboardShortcutsScreen {
        align: center middle;
    }
    
    #shortcuts-dialog {
        width: 80;
        height: auto;
        max-height: 90%;
        background: $panel;
        border: heavy $primary;
        padding: 1 2;
    }
    
    #shortcuts-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }
    
    #shortcuts-search {
        width: 100%;
        margin: 0 0 1 0;
    }
    
    #shortcuts-list {
        width: 100%;
        height: auto;
        max-height: 30;
        border: round $primary;
        padding: 1;
        background: $boost;
    }
    
    .shortcut-category {
        width: 100%;
        text-style: bold;
        color: $success;
        margin: 1 0 0 0;
    }
    
    #shortcuts-footer {
        width: 100%;
        content-align: center middle;
        text-style: dim;
        padding: 1 0 0 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
        Binding("q", "dismiss", "Close", show=False),
        Binding("?", "dismiss", "Close", show=False),
    ]
    
    def __init__(self, key_config: KeyBindingConfig) -> None:
        """Initialize the keyboard shortcuts screen.
        
        Args:
            key_config: The key binding configuration
        """
        super().__init__()
        self.key_config = key_config
        self.all_shortcuts = self._get_all_shortcuts()
        self.filtered_shortcuts = self.all_shortcuts.copy()
    
    def _get_all_shortcuts(self) -> list[tuple[str, list[tuple[str, str]]]]:
        """Get all keyboard shortcuts organized by category.
        
        Returns:
            List of tuples: (category_name, [(key, description), ...])
        """
        return [
            ("Navigation", [
                ("↑ / k", "Move up in the TODO list"),
                ("↓ / j", "Move down in the TODO list"),
                ("Tab", "Switch between TODO list and input field"),
                ("Shift+Tab", "Switch backwards between widgets"),
                ("Home", "Jump to first TODO"),
                ("End", "Jump to last TODO"),
            ]),
            ("TODO Management", [
                ("Enter", "Add new TODO (when in input field)"),
                (self.key_config.get_binding("toggle_todo"), "Toggle TODO completion status"),
                (self.key_config.get_binding("delete_todo"), "Delete selected TODO"),
                (self.key_config.get_binding("postpone_todo"), "Postpone TODO until tomorrow"),
            ]),
            ("Help & Customization", [
                (self.key_config.get_binding("show_shortcuts"), "Show this keyboard shortcuts help"),
                (self.key_config.get_binding("show_tutorial"), "Show welcome tutorial"),
                (self.key_config.get_binding("customize_keys"), "Customize key bindings"),
                (self.key_config.get_binding("export_cheatsheet"), "Export shortcuts cheat sheet"),
            ]),
            ("Application", [
                (self.key_config.get_binding("quit"), "Quit application"),
                ("Ctrl+C", "Force quit application"),
            ]),
        ]
    
    def compose(self) -> ComposeResult:
        """Compose the shortcuts dialog."""
        with Container(id="shortcuts-dialog"):
            yield Static("⌨️  Keyboard Shortcuts Reference", id="shortcuts-title")
            yield Input(placeholder="Search shortcuts...", id="shortcuts-search")
            with VerticalScroll(id="shortcuts-list"):
                yield from self._render_shortcuts(self.filtered_shortcuts)
            yield Static(
                "Press [bold]Escape[/], [bold]q[/], or [bold]?[/] to close",
                id="shortcuts-footer"
            )
    
    def _render_shortcuts(self, shortcuts: list[tuple[str, list[tuple[str, str]]]]) -> list[Static]:
        """Render shortcuts as widgets.
        
        Args:
            shortcuts: List of (category, shortcuts) tuples
            
        Returns:
            List of Static widgets
        """
        widgets = []
        for category, items in shortcuts:
            if items:  # Only show categories with items
                widgets.append(Static(f"📋 {category}", classes="shortcut-category"))
                for key, description in items:
                    widgets.append(ShortcutItem(key, description))
        
        if not widgets:
            widgets.append(Static("[dim]No shortcuts found matching your search.[/]"))
        
        return widgets
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes.
        
        Args:
            event: The input change event
        """
        search_term = event.value.lower().strip()
        
        if not search_term:
            self.filtered_shortcuts = self.all_shortcuts.copy()
        else:
            # Filter shortcuts based on search term
            self.filtered_shortcuts = []
            for category, items in self.all_shortcuts:
                filtered_items = [
                    (key, desc) for key, desc in items
                    if search_term in key.lower() or search_term in desc.lower()
                ]
                if filtered_items:
                    self.filtered_shortcuts.append((category, filtered_items))
        
        # Update the display
        shortcuts_list = self.query_one("#shortcuts-list", VerticalScroll)
        shortcuts_list.remove_children()
        shortcuts_list.mount_all(self._render_shortcuts(self.filtered_shortcuts))
    
    def action_dismiss(self) -> None:
        """Close the shortcuts dialog."""
        self.dismiss()


class TodoApp(App):
    """A Textual app for managing TODO items."""
    
    CSS = """
    /* 🎨 Vibrant Neon Cyberpunk Theme 🎨 */
    
    Screen {
        background: #0a0e27;  /* Deep midnight blue */
    }
    
    Header {
        background: linear-gradient(90deg, #ff006e 0%, #8338ec 50%, #3a86ff 100%);
        color: #ffffff;
        text-style: bold;
    }
    
    #todo-container {
        height: 100%;
        border: heavy #ff006e;  /* Hot pink border */
        background: #1a1f3a;  /* Slightly lighter midnight */
    }
    
    #todo-list {
        height: 1fr;
        border: round #3a86ff;  /* Electric blue border */
        margin: 1;
        background: #0f1425;  /* Very dark blue-black */
    }
    
    #input-container {
        height: auto;
        padding: 1;
        background: linear-gradient(135deg, #240046 0%, #10002b 100%);  /* Deep purple gradient */
        border: solid #8338ec;  /* Purple border */
    }
    
    Input {
        margin: 0 1;
        border: solid #06ffa5;  /* Neon green border */
        background: #1a1f3a;
        color: #06ffa5;  /* Neon green text */
    }
    
    Input:focus {
        border: heavy #ff006e;  /* Hot pink when focused */
        background: #240046;
    }
    
    Input > .input--placeholder {
        color: #7209b7;  /* Purple placeholder */
        text-style: italic;
    }
    
    Static {
        color: #ff006e;  /* Hot pink labels */
        text-style: bold;
    }
    
    ListView {
        height: 100%;
        background: #0f1425;
    }
    
    ListView > ListItem {
        background: #1a1f3a;
        color: #06ffa5;  /* Neon green text */
        padding: 0 2;
    }
    
    ListView > ListItem:hover {
        background: #240046;  /* Purple hover */
        color: #ffbe0b;  /* Golden yellow on hover */
    }
    
    ListView > ListItem.--highlight {
        background: linear-gradient(90deg, #8338ec 0%, #3a86ff 100%);  /* Purple to blue gradient */
        color: #ffffff;
        text-style: bold;
    }
    
    .dim {
        color: #7209b7;  /* Purple for completed */
        text-style: dim strikethrough;
    }
    
    .postponed {
        color: #ffbe0b;  /* Golden yellow for postponed */
        text-style: italic bold;
        background: #3a0f51;  /* Dark purple background */
    }
    
    Footer {
        background: linear-gradient(90deg, #3a86ff 0%, #8338ec 50%, #ff006e 100%);
        color: #ffffff;
    }
    
    Footer > .footer--key {
        background: #06ffa5;  /* Neon green key backgrounds */
        color: #0a0e27;  /* Dark text */
        text-style: bold;
    }
    
    Footer > .footer--description {
        color: #ffffff;
        text-style: italic;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    def __init__(self):
        """Initialize the TODO app."""
        super().__init__()
        self.storage = TodoStorage()
        self.todos: list[TodoItem] = []
        self.key_config = KeyBindingConfig()
        self.app_config = AppConfig()
        
        # Set up dynamic bindings from config
        self.BINDINGS = [
            Binding(self.key_config.get_binding("quit"), "quit", "Quit", priority=True),
            Binding(self.key_config.get_binding("toggle_todo"), "toggle_todo", "Toggle", show=True),
            Binding(self.key_config.get_binding("delete_todo"), "delete_todo", "Delete", show=True),
            Binding(self.key_config.get_binding("postpone_todo"), "postpone_todo", "Postpone", show=True),
            Binding(self.key_config.get_binding("show_shortcuts"), "show_shortcuts", "Help", show=True),
            Binding(self.key_config.get_binding("export_cheatsheet"), "export_cheatsheet", "Export", show=False),
            Binding(self.key_config.get_binding("customize_keys"), "customize_keys", "Customize", show=False),
            Binding(self.key_config.get_binding("show_tutorial"), "show_tutorial", "Tutorial", show=False),
        ]
    
    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        yield Header()
        with Container(id="todo-container"):
            yield ListView(id="todo-list")
            with Vertical(id="input-container"):
                yield Static("✨ Add new TODO ✨")
                yield Input(placeholder="Enter a new task...", id="todo-input")
        yield Footer()
    
    def on_mount(self) -> None:
        """Load todos when the app starts."""
        self.title = "✨ TODO TUI App ✨"
        self.load_todos()
        
        # Show tutorial on first run
        if self.app_config.is_first_run():
            self.call_after_refresh(self._show_first_run_tutorial)
    
    def _show_first_run_tutorial(self) -> None:
        """Show tutorial for first-time users."""
        def handle_tutorial_result(completed: bool | None) -> None:
            if completed:
                self.app_config.mark_tutorial_completed()
        
        self.push_screen(TutorialScreen(), handle_tutorial_result)
    
    def load_todos(self) -> None:
        """Load todos from storage and display them."""
        try:
            self.todos = self.storage.get_all()
            self._refresh_list()
        except ValueError as e:
            self.notify(f"Error loading todos: {e}", severity="error")
            self.todos = []
    
    def _refresh_list(self) -> None:
        """Refresh the todo list display."""
        list_view = self.query_one("#todo-list", ListView)
        list_view.clear()
        for todo in self.todos:
            # Show all todos, including postponed ones
            list_view.append(TodoListItem(todo))
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle new todo submission.
        
        Args:
            event: The input submission event
        """
        if event.input.id == "todo-input":
            title = event.value.strip()
            if title:
                todo = TodoItem(title=title)
                try:
                    self.storage.add(todo)
                    self.todos.append(todo)
                    self._refresh_list()
                    event.input.value = ""
                    self.notify(f"Added: {title}", timeout=2)
                except Exception as e:
                    self.notify(f"Error adding todo: {e}", severity="error")
    
    def action_toggle_todo(self) -> None:
        """Toggle the completion status of the selected todo."""
        list_view = self.query_one("#todo-list", ListView)
        if list_view.index is not None and 0 <= list_view.index < len(self.todos):
            todo = self.todos[list_view.index]
            todo.toggle_completed()
            try:
                self.storage.update(todo)
                self._refresh_list()
                # Restore selection
                list_view.index = list_view.index
                status = "completed" if todo.completed else "reopened"
                self.notify(f"Todo {status}", timeout=2)
            except Exception as e:
                self.notify(f"Error updating todo: {e}", severity="error")
    
    def action_delete_todo(self) -> None:
        """Delete the selected todo."""
        list_view = self.query_one("#todo-list", ListView)
        if list_view.index is not None and 0 <= list_view.index < len(self.todos):
            todo = self.todos[list_view.index]
            try:
                self.storage.delete(todo.id)
                self.todos.pop(list_view.index)
                self._refresh_list()
                self.notify(f"Deleted: {todo.title}", timeout=2)
            except Exception as e:
                self.notify(f"Error deleting todo: {e}", severity="error")
    
    def action_postpone_todo(self) -> None:
        """Postpone the selected todo until tomorrow."""
        list_view = self.query_one("#todo-list", ListView)
        if list_view.index is not None and 0 <= list_view.index < len(self.todos):
            todo = self.todos[list_view.index]
            todo.postpone_until_tomorrow()
            try:
                self.storage.update(todo)
                self._refresh_list()
                # Restore selection
                list_view.index = list_view.index
                self.notify(f"Postponed until {todo.postpone_until}", timeout=2)
            except Exception as e:
                self.notify(f"Error postponing todo: {e}", severity="error")
    
    def action_show_shortcuts(self) -> None:
        """Show the keyboard shortcuts help overlay."""
        self.push_screen(KeyboardShortcutsScreen(self.key_config))
    
    def action_show_tutorial(self) -> None:
        """Show the welcome tutorial."""
        def handle_tutorial_result(completed: bool | None) -> None:
            if completed:
                self.notify("Tutorial completed!", timeout=2)
        
        self.push_screen(TutorialScreen(), handle_tutorial_result)
    
    def action_customize_keys(self) -> None:
        """Show the customize key bindings screen."""
        self.push_screen(CustomizeKeysScreen(self.key_config))
    
    def action_export_cheatsheet(self) -> None:
        """Export keyboard shortcuts to a text file."""
        try:
            cheatsheet_path = Path.home() / "todo-tui-shortcuts.txt"
            
            content = []
            content.append("=" * 70)
            content.append("TODO TUI App - Keyboard Shortcuts Cheat Sheet")
            content.append("=" * 70)
            content.append("")
            
            # Get all shortcuts
            shortcuts = [
                ("Navigation", [
                    ("↑ / k", "Move up in the TODO list"),
                    ("↓ / j", "Move down in the TODO list"),
                    ("Tab", "Switch between TODO list and input field"),
                    ("Shift+Tab", "Switch backwards between widgets"),
                    ("Home", "Jump to first TODO"),
                    ("End", "Jump to last TODO"),
                ]),
                ("TODO Management", [
                    ("Enter", "Add new TODO (when in input field)"),
                    (self.key_config.get_binding("toggle_todo"), "Toggle TODO completion status"),
                    (self.key_config.get_binding("delete_todo"), "Delete selected TODO"),
                    (self.key_config.get_binding("postpone_todo"), "Postpone TODO until tomorrow"),
                ]),
                ("Help & Customization", [
                    (self.key_config.get_binding("show_shortcuts"), "Show keyboard shortcuts help"),
                    (self.key_config.get_binding("show_tutorial"), "Show welcome tutorial"),
                    (self.key_config.get_binding("customize_keys"), "Customize key bindings"),
                    (self.key_config.get_binding("export_cheatsheet"), "Export shortcuts cheat sheet"),
                ]),
                ("Application", [
                    (self.key_config.get_binding("quit"), "Quit application"),
                    ("Ctrl+C", "Force quit application"),
                ]),
            ]
            
            for category, items in shortcuts:
                content.append(f"{category}:")
                content.append("-" * 70)
                for key, description in items:
                    content.append(f"  {key:20} {description}")
                content.append("")
            
            content.append("=" * 70)
            content.append("Configuration Files:")
            content.append("-" * 70)
            content.append(f"  TODOs:        ~/.todo-tui.json")
            content.append(f"  Key Bindings: ~/.todo-tui-keybindings.json")
            content.append(f"  App Config:   ~/.todo-tui-config.json")
            content.append("")
            content.append("To customize key bindings, edit ~/.todo-tui-keybindings.json")
            content.append('Example: {"quit": "ctrl+q", "toggle_todo": "t"}')
            content.append("")
            content.append("=" * 70)
            content.append(f"Generated by TODO TUI App")
            content.append("=" * 70)
            
            with open(cheatsheet_path, 'w') as f:
                f.write('\n'.join(content))
            
            self.notify(f"Cheat sheet exported to: {cheatsheet_path}", timeout=5)
        except Exception as e:
            self.notify(f"Error exporting cheat sheet: {e}", severity="error")


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
