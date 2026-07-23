"""Main Textual application for the TODO TUI app."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, Button
from textual.message import Message
from textual.screen import ModalScreen
from pathlib import Path

from .models import TodoItem
from .storage import TodoStorage
from .config import Config, DEFAULT_BINDINGS


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


class TutorialScreen(ModalScreen):
    """Modal screen displaying an interactive tutorial for new users."""
    
    CSS = """
    TutorialScreen {
        align: center middle;
    }
    
    #tutorial-container {
        width: 90;
        height: auto;
        max-height: 95%;
        background: #1a1f3a;
        border: heavy #ff006e;
        padding: 1 2;
    }
    
    #tutorial-title {
        width: 100%;
        text-align: center;
        color: #ff006e;
        text-style: bold;
        padding: 1 0;
        background: #240046;
        content-align: center middle;
    }
    
    #tutorial-content {
        width: 100%;
        height: auto;
        max-height: 35;
        background: #0f1425;
        border: solid #8338ec;
        padding: 1 2;
    }
    
    .tutorial-section {
        padding: 1 0;
    }
    
    .tutorial-heading {
        color: #8338ec;
        text-style: bold;
        padding: 1 0 0 0;
    }
    
    .tutorial-text {
        color: #06ffa5;
    }
    
    .tutorial-tip {
        color: #ffbe0b;
        text-style: italic;
    }
    
    #tutorial-button-container {
        width: 100%;
        height: auto;
        padding: 1 0;
        align: center middle;
    }
    
    Button {
        margin: 0 1;
        background: #8338ec;
        color: #ffffff;
    }
    
    Button:hover {
        background: #ff006e;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the tutorial screen layout."""
        with Container(id="tutorial-container"):
            yield Static("🎓 Welcome to TODO TUI! 🎓", id="tutorial-title")
            with VerticalScroll(id="tutorial-content"):
                yield Static("Getting Started", classes="tutorial-heading")
                yield Static(
                    "Welcome! This quick tutorial will help you get started with TODO TUI.",
                    classes="tutorial-text tutorial-section"
                )
                
                yield Static("📝 Adding Tasks", classes="tutorial-heading")
                yield Static(
                    "• Press Tab to focus the input field at the bottom\n"
                    "• Type your task and press Enter to add it\n"
                    "• Your task appears in the list above",
                    classes="tutorial-text tutorial-section"
                )
                
                yield Static("✅ Managing Tasks", classes="tutorial-heading")
                yield Static(
                    "• Use ↑/↓ arrow keys to navigate your tasks\n"
                    "• Press Space to mark a task complete/incomplete\n"
                    "• Press 'd' to delete the selected task\n"
                    "• Press 'p' to postpone a task until tomorrow",
                    classes="tutorial-text tutorial-section"
                )
                
                yield Static("🔑 Essential Shortcuts", classes="tutorial-heading")
                yield Static(
                    "• Press '?' anytime to see all keyboard shortcuts\n"
                    "• Press 'c' to customize your key bindings\n"
                    "• Press Ctrl+E to export shortcuts as a cheat sheet\n"
                    "• Press 'q' to quit (your data saves automatically)",
                    classes="tutorial-text tutorial-section"
                )
                
                yield Static("💡 Pro Tips", classes="tutorial-heading")
                yield Static(
                    "• Completed tasks show with a checkmark and dim style\n"
                    "• Postponed tasks appear in yellow with a date indicator\n"
                    "• All data is saved automatically to ~/.todo-tui.json\n"
                    "• Search in the help screen (?) to find shortcuts quickly",
                    classes="tutorial-tip tutorial-section"
                )
                
                yield Static("🎯 You're Ready!", classes="tutorial-heading")
                yield Static(
                    "That's all you need to know! Start adding tasks and press '?' if you need help.",
                    classes="tutorial-text tutorial-section"
                )
            
            with Horizontal(id="tutorial-button-container"):
                yield Button("Got it! Let's start", id="tutorial-close", variant="primary")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "tutorial-close":
            self.dismiss()


class CustomizeBindingsScreen(ModalScreen):
    """Modal screen for customizing key bindings."""
    
    CSS = """
    CustomizeBindingsScreen {
        align: center middle;
    }
    
    #customize-container {
        width: 80;
        height: auto;
        max-height: 90%;
        background: #1a1f3a;
        border: heavy #ff006e;
        padding: 1 2;
    }
    
    #customize-title {
        width: 100%;
        text-align: center;
        color: #ff006e;
        text-style: bold;
        padding: 1 0;
        background: #240046;
    }
    
    #customize-content {
        width: 100%;
        height: auto;
        max-height: 30;
        background: #0f1425;
        border: solid #8338ec;
        padding: 1 2;
    }
    
    .customize-row {
        padding: 0 0 1 0;
    }
    
    .customize-label {
        color: #06ffa5;
        text-style: bold;
    }
    
    .customize-current {
        color: #8338ec;
    }
    
    #customize-button-container {
        width: 100%;
        height: auto;
        padding: 1 0;
        align: center middle;
    }
    
    Button {
        margin: 0 1;
    }
    
    #reset-button {
        background: #ffbe0b;
        color: #0a0e27;
    }
    
    #reset-button:hover {
        background: #ff006e;
        color: #ffffff;
    }
    
    #close-button {
        background: #8338ec;
        color: #ffffff;
    }
    
    #close-button:hover {
        background: #06ffa5;
        color: #0a0e27;
    }
    
    .customize-info {
        color: #ffbe0b;
        text-style: italic;
        padding: 1 0;
        text-align: center;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
    ]
    
    def __init__(self, config: Config):
        """Initialize the customize bindings screen.
        
        Args:
            config: The application configuration object
        """
        super().__init__()
        self.config = config
        self.selected_action: Optional[str] = None
        self.action_inputs: Dict[str, Input] = {}
        # Track pending changes before saving
        self.pending_changes: Dict[str, str] = {}
    
    def compose(self) -> ComposeResult:
        """Compose the customize screen layout."""
        with Container(id="customize-container"):
            yield Static("⚙️  Customize Key Bindings  ⚙️", id="customize-title")
            yield Static(
                "Click in a field and press your desired key. Use standard names like 'space', 'ctrl+e', etc.",
                classes="customize-info"
            )
            with VerticalScroll(id="customize-content"):
                for action, default_key in DEFAULT_BINDINGS.items():
                    current_key = self.config.get_binding(action)
                    action_name = action.replace("_", " ").title()
                    
                    with Vertical(classes="customize-row"):
                        yield Static(f"{action_name}:", classes="customize-label")
                        input_widget = Input(
                            value=current_key,
                            placeholder=f"Default: {default_key}",
                            id=f"binding-{action}"
                        )
                        self.action_inputs[action] = input_widget
                        yield input_widget
            
            with Horizontal(id="customize-button-container"):
                yield Button("Reset to Defaults", id="reset-button")
                yield Button("Close", id="close-button", variant="primary")
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes to track pending bindings.
        
        Args:
            event: The input change event
        """
        # Find which action this input corresponds to
        for action, input_widget in self.action_inputs.items():
            if input_widget == event.input:
                new_key = event.value.strip()
                if new_key:
                    # Store the pending change but don't save yet
                    self.pending_changes[action] = new_key
                break
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission to save bindings.
        
        Args:
            event: The input submit event
        """
        # Find which action this input corresponds to
        for action, input_widget in self.action_inputs.items():
            if input_widget == event.input:
                new_key = event.value.strip()
                if new_key:
                    self.config.set_binding(action, new_key)
                    self.config.save_bindings()
                    self.notify(f"Updated {action.replace('_', ' ')} binding", timeout=2)
                break
    
    def on_screen_resume(self) -> None:
        """Save any pending changes when screen is dismissed."""
        # Save all pending changes when closing
        for action, key in self.pending_changes.items():
            if key.strip():  # Only save non-empty keys
                self.config.set_binding(action, key)
        
        if self.pending_changes:
            self.config.save_bindings()
        
        self.pending_changes.clear()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.
        
        Args:
            event: The button press event
        """
        if event.button.id == "reset-button":
            self.config.reset_bindings()
            # Update all input fields
            for action, input_widget in self.action_inputs.items():
                input_widget.value = self.config.get_binding(action)
            self.pending_changes.clear()
            self.notify("Key bindings reset to defaults", timeout=2)
        elif event.button.id == "close-button":
            # Save pending changes before closing
            for action, key in self.pending_changes.items():
                if key.strip():  # Only save non-empty keys
                    self.config.set_binding(action, key)
            
            if self.pending_changes:
                self.config.save_bindings()
            
            self.dismiss()


class HelpScreen(ModalScreen):
    """Modal screen displaying keyboard shortcuts and help information."""
    
    CSS = """
    HelpScreen {
        align: center middle;
    }
    
    #help-container {
        width: 80;
        height: auto;
        max-height: 90%;
        background: #1a1f3a;
        border: heavy #ff006e;
        padding: 1 2;
    }
    
    #help-title {
        width: 100%;
        text-align: center;
        color: #ff006e;
        text-style: bold;
        padding: 1 0;
        background: #240046;
    }
    
    #help-search-container {
        width: 100%;
        height: auto;
        padding: 1 0;
    }
    
    #help-search {
        width: 100%;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
    }
    
    #help-search:focus {
        border: heavy #ff006e;
    }
    
    #help-content {
        width: 100%;
        height: auto;
        max-height: 30;
        background: #0f1425;
        border: solid #8338ec;
        padding: 1 2;
    }
    
    .help-section-title {
        color: #8338ec;
        text-style: bold;
        padding-top: 1;
    }
    
    .help-shortcut {
        color: #06ffa5;
        text-style: bold;
    }
    
    .help-description {
        color: #ffffff;
    }
    
    #help-button-container {
        width: 100%;
        height: auto;
        padding: 1 0;
        align: center middle;
    }
    
    Button {
        margin: 0 1;
        background: #8338ec;
        color: #ffffff;
    }
    
    Button:hover {
        background: #ff006e;
    }
    
    .help-footer {
        width: 100%;
        text-align: center;
        color: #ffbe0b;
        text-style: italic;
        padding: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("escape,q,question_mark", "dismiss", "Close", show=True),
    ]
    
    def __init__(self, config: Config):
        """Initialize the help screen.
        
        Args:
            config: The application configuration object
        """
        super().__init__()
        self.config = config
        self.all_shortcuts = self._get_all_shortcuts()
        self.filtered_shortcuts = self.all_shortcuts.copy()
    
    def _get_all_shortcuts(self) -> list[dict]:
        """Get all keyboard shortcuts organized by category.
        
        Returns:
            List of shortcut dictionaries with category, key, and description
        """
        return [
            # Navigation
            {"category": "Navigation", "key": "↑ / ↓", "description": "Move selection up/down in the list"},
            {"category": "Navigation", "key": "Tab", "description": "Switch between list and input field"},
            {"category": "Navigation", "key": "Shift+Tab", "description": "Switch backwards between elements"},
            
            # Task Management
            {"category": "Task Management", "key": self.config.get_binding("toggle"), "description": "Toggle TODO completion status"},
            {"category": "Task Management", "key": self.config.get_binding("delete"), "description": "Delete selected TODO"},
            {"category": "Task Management", "key": self.config.get_binding("postpone"), "description": "Postpone selected TODO until tomorrow"},
            {"category": "Task Management", "key": "Enter", "description": "Add new TODO (when in input field)"},
            
            # Application
            {"category": "Application", "key": self.config.get_binding("quit"), "description": "Quit application (data auto-saved)"},
            {"category": "Application", "key": self.config.get_binding("help"), "description": "Show this help screen"},
            {"category": "Application", "key": self.config.get_binding("customize"), "description": "Customize key bindings"},
            {"category": "Application", "key": self.config.get_binding("export_shortcuts"), "description": "Export shortcuts cheat sheet"},
            {"category": "Application", "key": self.config.get_binding("tutorial"), "description": "Show tutorial"},
            
            # Tips
            {"category": "Tips", "key": "", "description": "• TODOs are automatically saved to ~/.todo-tui.json"},
            {"category": "Tips", "key": "", "description": "• Postponed items show with yellow text and indicator"},
            {"category": "Tips", "key": "", "description": "• Completed items appear dimmed with strikethrough"},
            {"category": "Tips", "key": "", "description": "• Search shortcuts below to find specific actions"},
            {"category": "Tips", "key": "", "description": "• Customize all key bindings to your preference"},
        ]
    
    def compose(self) -> ComposeResult:
        """Compose the help screen layout."""
        with Container(id="help-container"):
            yield Static("⌨️  Keyboard Shortcuts Reference  ⌨️", id="help-title")
            with Vertical(id="help-search-container"):
                yield Static("🔍 Search shortcuts:", classes="help-section-title")
                yield Input(placeholder="Type to filter shortcuts...", id="help-search")
            with VerticalScroll(id="help-content"):
                yield from self._render_shortcuts(self.filtered_shortcuts)
            
            with Horizontal(id="help-button-container"):
                yield Button("Export Cheat Sheet", id="export-button")
                yield Button("Close", id="close-button", variant="primary")
            
            yield Static("Press ESC, q, or ? to close", classes="help-footer")
    
    def _render_shortcuts(self, shortcuts: list[dict]) -> list[Static]:
        """Render shortcuts grouped by category.
        
        Args:
            shortcuts: List of shortcut dictionaries
            
        Returns:
            List of Static widgets to display
        """
        widgets = []
        current_category = None
        
        for shortcut in shortcuts:
            category = shortcut["category"]
            key = shortcut["key"]
            description = shortcut["description"]
            
            # Add category header if it's a new category
            if category != current_category:
                if current_category is not None:
                    widgets.append(Static(""))  # Blank line between categories
                widgets.append(Static(f"═══ {category} ═══", classes="help-section-title"))
                current_category = category
            
            # Add shortcut item
            if key:  # Only show key-description pairs, skip tips without keys
                shortcut_text = f"  [{key}]".ljust(20) + description
                widgets.append(Static(shortcut_text, classes="help-description"))
            else:
                # For tips without keys, just show the description
                widgets.append(Static(f"  {description}", classes="help-description"))
        
        if not widgets:
            widgets.append(Static("No shortcuts found matching your search.", classes="help-description"))
        
        return widgets
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes.
        
        Args:
            event: The input change event
        """
        if event.input.id == "help-search":
            search_term = event.value.lower().strip()
            
            if not search_term:
                self.filtered_shortcuts = self.all_shortcuts.copy()
            else:
                # Filter shortcuts by search term (search in key and description)
                self.filtered_shortcuts = [
                    s for s in self.all_shortcuts
                    if search_term in s["key"].lower() or search_term in s["description"].lower()
                ]
            
            # Refresh the content
            self._refresh_content()
    
    def _refresh_content(self) -> None:
        """Refresh the help content display."""
        content = self.query_one("#help-content", VerticalScroll)
        content.remove_children()
        for widget in self._render_shortcuts(self.filtered_shortcuts):
            content.mount(widget)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.
        
        Args:
            event: The button press event
        """
        if event.button.id == "export-button":
            self._export_cheat_sheet()
        elif event.button.id == "close-button":
            self.dismiss()
    
    def _export_cheat_sheet(self) -> None:
        """Export shortcuts as a print-friendly cheat sheet."""
        try:
            export_path = Path.home() / "todo-tui-shortcuts.txt"
            
            # Build the cheat sheet content
            lines = [
                "=" * 70,
                "TODO TUI - Keyboard Shortcuts Cheat Sheet".center(70),
                "=" * 70,
                "",
            ]
            
            current_category = None
            for shortcut in self.all_shortcuts:
                category = shortcut["category"]
                key = shortcut["key"]
                description = shortcut["description"]
                
                # Add category header
                if category != current_category:
                    if current_category is not None:
                        lines.append("")  # Blank line between categories
                    lines.append(f"{category}")
                    lines.append("-" * 70)
                    current_category = category
                
                # Add shortcut
                if key:
                    lines.append(f"  {key:20s} {description}")
                else:
                    lines.append(f"  {description}")
            
            lines.extend([
                "",
                "=" * 70,
                f"Generated by TODO TUI | Save this file for quick reference",
                "=" * 70,
            ])
            
            export_path.write_text("\n".join(lines))
            self.notify(f"Cheat sheet exported to {export_path}", timeout=3)
        except Exception as e:
            self.notify(f"Error exporting cheat sheet: {e}", severity="error", timeout=3)


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
    """
    
    def __init__(self):
        """Initialize the TODO app."""
        super().__init__()
        self.storage = TodoStorage()
        self.config = Config()
        self.todos: list[TodoItem] = []
        self._setup_bindings()
    
    def _setup_bindings(self) -> None:
        """Setup dynamic bindings based on configuration."""
        self.BINDINGS = [
            Binding(self.config.get_binding("quit"), "quit", "Quit", priority=True),
            Binding(self.config.get_binding("toggle"), "toggle_todo", "Toggle", show=True),
            Binding(self.config.get_binding("delete"), "delete_todo", "Delete", show=True),
            Binding(self.config.get_binding("postpone"), "postpone_todo", "Postpone", show=True),
            Binding(self.config.get_binding("help"), "show_help", "Help", show=True),
            Binding(self.config.get_binding("customize"), "customize_bindings", "Customize", show=True),
            Binding(self.config.get_binding("export_shortcuts"), "export_shortcuts", "Export", show=False),
            Binding(self.config.get_binding("tutorial"), "show_tutorial", "Tutorial", show=False),
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
        
        # Show tutorial for first-time users
        if not self.config.tutorial_shown:
            self.call_after_refresh(self._show_first_time_tutorial)
    
    def _show_first_time_tutorial(self) -> None:
        """Show the tutorial for first-time users."""
        self.config.mark_tutorial_shown()
        self.push_screen(TutorialScreen())
    
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
    
    def action_show_help(self) -> None:
        """Show the keyboard shortcuts help screen."""
        self.push_screen(HelpScreen(self.config))
    
    def action_customize_bindings(self) -> None:
        """Show the customize key bindings screen."""
        self.push_screen(CustomizeBindingsScreen(self.config))
    
    def action_export_shortcuts(self) -> None:
        """Export shortcuts cheat sheet."""
        try:
            export_path = Path.home() / "todo-tui-shortcuts.txt"
            
            # Build the cheat sheet content
            lines = [
                "=" * 70,
                "TODO TUI - Keyboard Shortcuts Cheat Sheet".center(70),
                "=" * 70,
                "",
                "Navigation",
                "-" * 70,
                "  ↑ / ↓              Move selection up/down in the list",
                "  Tab                Switch between list and input field",
                "  Shift+Tab          Switch backwards between elements",
                "",
                "Task Management",
                "-" * 70,
                f"  {self.config.get_binding('toggle'):20s} Toggle TODO completion status",
                f"  {self.config.get_binding('delete'):20s} Delete selected TODO",
                f"  {self.config.get_binding('postpone'):20s} Postpone selected TODO until tomorrow",
                "  Enter              Add new TODO (when in input field)",
                "",
                "Application",
                "-" * 70,
                f"  {self.config.get_binding('quit'):20s} Quit application (data auto-saved)",
                f"  {self.config.get_binding('help'):20s} Show help screen",
                f"  {self.config.get_binding('customize'):20s} Customize key bindings",
                f"  {self.config.get_binding('export_shortcuts'):20s} Export shortcuts cheat sheet",
                f"  {self.config.get_binding('tutorial'):20s} Show tutorial",
                "",
                "Tips",
                "-" * 70,
                "  • TODOs are automatically saved to ~/.todo-tui.json",
                "  • Postponed items show with yellow text and indicator",
                "  • Completed items appear dimmed with strikethrough",
                "  • Search shortcuts below to find specific actions",
                "  • Customize all key bindings to your preference",
                "",
                "=" * 70,
                "Generated by TODO TUI | Save this file for quick reference",
                "=" * 70,
            ]
            
            export_path.write_text("\n".join(lines))
            self.notify(f"Cheat sheet exported to {export_path}", timeout=3)
        except Exception as e:
            self.notify(f"Error exporting cheat sheet: {e}", severity="error", timeout=3)
    
    def action_show_tutorial(self) -> None:
        """Show the interactive tutorial."""
        self.push_screen(TutorialScreen())
