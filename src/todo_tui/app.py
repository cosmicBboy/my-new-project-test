"""Main Textual application for the TODO TUI app."""

from typing import Optional
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, Button
from textual.screen import Screen, ModalScreen
from textual.message import Message
from textual.events import Key
from pathlib import Path

from .models import TodoItem
from .storage import TodoStorage
from .keybindings import KeyBindings


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
    """Interactive tutorial for new users."""
    
    CSS = """
    TutorialScreen {
        align: center middle;
    }
    
    #tutorial-dialog {
        width: 90;
        height: auto;
        max-height: 95%;
        background: #1a1f3a;
        border: heavy #ffbe0b;
        padding: 1 2;
    }
    
    #tutorial-title {
        width: 100%;
        content-align: center middle;
        color: #ffbe0b;
        text-style: bold;
        padding: 0 0 1 0;
    }
    
    #tutorial-content {
        width: 100%;
        height: auto;
        max-height: 35;
        padding: 1;
    }
    
    .tutorial-step {
        width: 100%;
        margin: 0 0 2 0;
        padding: 1;
        border: solid #8338ec;
        background: #0f1425;
    }
    
    .step-number {
        color: #ff006e;
        text-style: bold;
    }
    
    .step-title {
        color: #06ffa5;
        text-style: bold;
        margin: 0 0 1 0;
    }
    
    .step-content {
        color: #3a86ff;
        margin: 0 0 0 2;
    }
    
    .tutorial-footer {
        width: 100%;
        content-align: center middle;
        margin: 1 0 0 0;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the tutorial dialog."""
        with Container(id="tutorial-dialog"):
            yield Static("🎓 Welcome to TODO TUI - Quick Start Tutorial", id="tutorial-title")
            with VerticalScroll(id="tutorial-content"):
                yield Static(
                    "[bold]Step 1:[/bold] Adding Your First TODO",
                    classes="tutorial-step step-title",
                    markup=True
                )
                yield Static(
                    "• Press [bold]Tab[/bold] to focus the input field at the bottom\n"
                    "• Type your task (e.g., 'Buy groceries')\n"
                    "• Press [bold]Enter[/bold] to add it to your list\n"
                    "• Your TODO appears in the list above!",
                    classes="tutorial-step step-content",
                    markup=True
                )
                
                yield Static(
                    "[bold]Step 2:[/bold] Managing Your TODOs",
                    classes="tutorial-step step-title",
                    markup=True
                )
                yield Static(
                    "• Use [bold]↑[/bold] and [bold]↓[/bold] arrow keys to navigate\n"
                    "• Press [bold]Space[/bold] to mark a TODO as complete (or reopen it)\n"
                    "• Completed TODOs show a ✓ and appear dimmed\n"
                    "• Press [bold]d[/bold] to delete a TODO you no longer need",
                    classes="tutorial-step step-content",
                    markup=True
                )
                
                yield Static(
                    "[bold]Step 3:[/bold] Postponing Tasks",
                    classes="tutorial-step step-title",
                    markup=True
                )
                yield Static(
                    "• Select a TODO with arrow keys\n"
                    "• Press [bold]p[/bold] to postpone it until tomorrow\n"
                    "• Postponed TODOs show when they'll become active\n"
                    "• Great for tasks you can't do today!",
                    classes="tutorial-step step-content",
                    markup=True
                )
                
                yield Static(
                    "[bold]Step 4:[/bold] Getting Help",
                    classes="tutorial-step step-title",
                    markup=True
                )
                yield Static(
                    "• Press [bold]?[/bold] anytime to see all keyboard shortcuts\n"
                    "• Use the search box to find specific shortcuts\n"
                    "• Press [bold]Ctrl+E[/bold] to export a printable cheat sheet\n"
                    "• Press [bold]Ctrl+K[/bold] to customize key bindings",
                    classes="tutorial-step step-content",
                    markup=True
                )
                
                yield Static(
                    "[bold]Step 5:[/bold] Your Data is Safe",
                    classes="tutorial-step step-title",
                    markup=True
                )
                yield Static(
                    "• All TODOs are automatically saved to disk\n"
                    "• Close the app anytime with [bold]q[/bold]\n"
                    "• Your tasks will be here when you return\n"
                    "• Data is stored in your home directory",
                    classes="tutorial-step step-content",
                    markup=True
                )
                
                yield Static(
                    "🎉 [bold]You're Ready![/bold] Press ESC or the button below to start.",
                    classes="tutorial-step",
                    markup=True
                )
            
            with Horizontal(classes="tutorial-footer"):
                yield Button("Close Tutorial", variant="primary", id="close-tutorial")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "close-tutorial":
            self.dismiss()
    
    def action_dismiss(self) -> None:
        """Close the tutorial."""
        self.dismiss()


class CustomizeKeysScreen(ModalScreen):
    """Screen for customizing key bindings with interactive editing."""
    
    CSS = """
    CustomizeKeysScreen {
        align: center middle;
    }
    
    #customize-dialog {
        width: 80;
        height: auto;
        max-height: 90%;
        background: #1a1f3a;
        border: heavy #06ffa5;
        padding: 1 2;
    }
    
    #customize-title {
        width: 100%;
        content-align: center middle;
        color: #06ffa5;
        text-style: bold;
        padding: 0 0 1 0;
    }
    
    #customize-content {
        width: 100%;
        height: auto;
        max-height: 30;
        border: solid #8338ec;
        background: #0f1425;
        padding: 1;
    }
    
    .binding-row {
        width: 100%;
        height: auto;
        margin: 0 0 1 0;
        padding: 1;
        background: #1a1f3a;
        border: solid #3a86ff;
    }
    
    .binding-row.editing {
        border: heavy #ff006e;
        background: #240046;
    }
    
    .binding-description {
        color: #3a86ff;
        text-style: bold;
        margin: 0 0 0 0;
    }
    
    .binding-key-display {
        color: #ff006e;
        text-style: bold;
        margin: 0 0 1 0;
    }
    
    .binding-buttons {
        width: 100%;
        height: auto;
    }
    
    .binding-input {
        width: 100%;
        margin: 0 0 1 0;
    }
    
    .customize-footer {
        width: 100%;
        content-align: center middle;
        margin: 1 0 0 0;
    }
    
    .info-text {
        color: #ffbe0b;
        text-style: italic;
        margin: 1 0;
    }
    
    Button {
        margin: 0 1;
    }
    
    Button.edit-button {
        margin: 0 0 0 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
    ]
    
    def __init__(self, keybindings: KeyBindings) -> None:
        """Initialize the customize keys screen.
        
        Args:
            keybindings: KeyBindings instance to manage
        """
        super().__init__()
        self.keybindings = keybindings
        self.editing_action: Optional[str] = None
    
    def compose(self) -> ComposeResult:
        """Compose the customize dialog."""
        with Container(id="customize-dialog"):
            yield Static("⚙️  Customize Key Bindings  ⚙️", id="customize-title")
            yield Static(
                "Click 'Edit' to change a key binding, then press the new key:",
                classes="info-text"
            )
            with VerticalScroll(id="customize-content"):
                for action, key in sorted(self.keybindings.get_all_bindings().items()):
                    yield from self._create_binding_row(action, key)
            
            yield Static(
                "💡 Tip: Your custom bindings are saved automatically",
                classes="info-text"
            )
            
            with Horizontal(classes="customize-footer"):
                yield Button("Reset to Defaults", variant="warning", id="reset-keys")
                yield Button("Close", variant="primary", id="close-customize")
    
    def _create_binding_row(self, action: str, key: str):
        """Create widgets for a single binding row.
        
        Args:
            action: Action name
            key: Current key binding
            
        Yields:
            Widgets for the binding row
        """
        description = self.keybindings.get_description(action)
        display_key = self.keybindings.format_key_for_display(key)
        
        with Container(classes="binding-row", id=f"row-{action}"):
            yield Static(description, classes="binding-description")
            yield Static(
                f"Current key: [bold]{display_key}[/bold]",
                classes="binding-key-display",
                markup=True,
                id=f"display-{action}"
            )
            with Horizontal(classes="binding-buttons"):
                yield Button("Edit", classes="edit-button", id=f"edit-{action}")
                yield Input(
                    placeholder="Press a key...",
                    classes="binding-input hidden",
                    id=f"input-{action}",
                    disabled=True
                )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        button_id = event.button.id
        
        if button_id == "reset-keys":
            self.keybindings.reset_to_defaults()
            self.app.notify("Key bindings reset to defaults", timeout=3)
            self.dismiss(True)  # Signal to refresh
        elif button_id == "close-customize":
            self.dismiss()
        elif button_id and button_id.startswith("edit-"):
            action = button_id[5:]  # Remove "edit-" prefix
            self._start_editing(action)
    
    def _start_editing(self, action: str) -> None:
        """Start editing a key binding.
        
        Args:
            action: Action to edit
        """
        # Cancel any previous editing
        if self.editing_action:
            self._cancel_editing(self.editing_action)
        
        self.editing_action = action
        
        # Hide the edit button and show the input
        try:
            edit_button = self.query_one(f"#edit-{action}", Button)
            edit_button.disabled = True
            edit_button.display = False
            
            input_widget = self.query_one(f"#input-{action}", Input)
            input_widget.disabled = False
            input_widget.remove_class("hidden")
            input_widget.focus()
            
            # Highlight the row
            row = self.query_one(f"#row-{action}")
            row.add_class("editing")
            
            self.app.notify(f"Press the new key for '{self.keybindings.get_description(action)}'", timeout=5)
        except Exception:
            pass
    
    def _cancel_editing(self, action: str) -> None:
        """Cancel editing a key binding.
        
        Args:
            action: Action being edited
        """
        try:
            edit_button = self.query_one(f"#edit-{action}", Button)
            edit_button.disabled = False
            edit_button.display = True
            
            input_widget = self.query_one(f"#input-{action}", Input)
            input_widget.disabled = True
            input_widget.add_class("hidden")
            input_widget.value = ""
            
            row = self.query_one(f"#row-{action}")
            row.remove_class("editing")
        except Exception:
            pass
    
    def _save_binding(self, action: str, new_key: str) -> None:
        """Save a new key binding.
        
        Args:
            action: Action to bind
            new_key: New key string
        """
        # Save the binding
        self.keybindings.set_key(action, new_key)
        
        # Update display
        display_key = self.keybindings.format_key_for_display(new_key)
        try:
            display = self.query_one(f"#display-{action}", Static)
            display.update(f"Current key: [bold]{display_key}[/bold]")
        except Exception:
            pass
        
        # Cancel editing mode
        self._cancel_editing(action)
        self.editing_action = None
        
        self.app.notify(f"Saved: {self.keybindings.get_description(action)} = {display_key}", timeout=3)
    
    def on_key(self, event: Key) -> None:
        """Handle key press during editing.
        
        Args:
            event: Key event
        """
        if self.editing_action:
            # Convert the key event to our key string format
            key_str = event.key
            
            # Cancel on escape
            if key_str == "escape":
                self._cancel_editing(self.editing_action)
                self.editing_action = None
                self.app.notify("Editing cancelled", timeout=2)
                return
            
            # Ignore certain keys that shouldn't be bound
            if key_str in ["enter", "tab"]:
                return
            
            # Save the new binding
            self._save_binding(self.editing_action, key_str)
            event.prevent_default()
            event.stop()
    
    def action_dismiss(self) -> None:
        """Close the dialog."""
        self.dismiss()


class KeyboardShortcutsHelp(ModalScreen):
    """Modal screen displaying keyboard shortcuts help."""
    
    CSS = """
    KeyboardShortcutsHelp {
        align: center middle;
    }
    
    #help-dialog {
        width: 80;
        height: auto;
        max-height: 90%;
        background: #1a1f3a;
        border: heavy #ff006e;
        padding: 1 2;
    }
    
    #help-title {
        width: 100%;
        content-align: center middle;
        color: #ff006e;
        text-style: bold;
        padding: 0 0 1 0;
    }
    
    #help-search {
        width: 100%;
        margin: 0 0 1 0;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
    }
    
    #help-search:focus {
        border: heavy #ff006e;
        background: #240046;
    }
    
    #help-content {
        width: 100%;
        height: auto;
        max-height: 30;
        border: solid #8338ec;
        background: #0f1425;
        padding: 1;
    }
    
    .help-section {
        width: 100%;
        margin: 0 0 1 0;
    }
    
    .help-section-title {
        color: #ffbe0b;
        text-style: bold;
        margin: 0 0 1 0;
    }
    
    .help-shortcut {
        margin: 0 0 0 2;
        color: #06ffa5;
    }
    
    .help-key {
        color: #ff006e;
        text-style: bold;
    }
    
    .help-description {
        color: #3a86ff;
    }
    
    .help-footer {
        width: 100%;
        content-align: center middle;
        color: #7209b7;
        text-style: italic;
        margin: 1 0 0 0;
    }
    
    .hidden {
        display: none;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
        Binding("q", "dismiss", "Close", show=False),
    ]
    
    def __init__(self, keybindings: KeyBindings) -> None:
        """Initialize the help screen.
        
        Args:
            keybindings: KeyBindings instance for current bindings
        """
        super().__init__()
        self.keybindings = keybindings
        self.shortcuts = self._get_all_shortcuts()
        self.filtered_shortcuts = self.shortcuts.copy()
    
    def _get_all_shortcuts(self) -> dict:
        """Get all keyboard shortcuts organized by category.
        
        Returns:
            Dictionary of shortcuts organized by category
        """
        bindings = self.keybindings.get_all_bindings()
        
        shortcuts = {
            "Navigation": [
                ("↑ / ↓", "Navigate through TODO items"),
                ("Tab", "Switch between list and input field"),
                ("Enter", "Add new TODO (when in input field)"),
            ],
            "TODO Management": [
                (self.keybindings.format_key_for_display(bindings["toggle_todo"]), 
                 "Toggle TODO completion status"),
                (self.keybindings.format_key_for_display(bindings["delete_todo"]), 
                 "Delete selected TODO"),
                (self.keybindings.format_key_for_display(bindings["postpone_todo"]), 
                 "Postpone selected TODO until tomorrow"),
            ],
            "Help & Information": [
                (self.keybindings.format_key_for_display(bindings["show_help"]), 
                 "Show this keyboard shortcuts help"),
                (self.keybindings.format_key_for_display(bindings["show_tutorial"]), 
                 "Show interactive tutorial"),
                (self.keybindings.format_key_for_display(bindings["export_shortcuts"]), 
                 "Export printable cheat sheet"),
            ],
            "Application": [
                (self.keybindings.format_key_for_display(bindings["quit"]), 
                 "Quit application"),
                (self.keybindings.format_key_for_display(bindings["customize_keys"]), 
                 "Customize key bindings"),
                ("Esc", "Close dialogs and modals"),
            ],
        }
        return shortcuts
    
    def compose(self) -> ComposeResult:
        """Compose the help dialog."""
        with Container(id="help-dialog"):
            yield Static("⌨️  Keyboard Shortcuts Reference  ⌨️", id="help-title")
            yield Input(
                placeholder="Search shortcuts...",
                id="help-search"
            )
            with VerticalScroll(id="help-content"):
                yield from self._render_shortcuts(self.filtered_shortcuts)
            yield Static(
                "Press ESC or Q to close | Type to search | Ctrl+E to export",
                classes="help-footer"
            )
    
    def _render_shortcuts(self, shortcuts: dict) -> list:
        """Render shortcuts content.
        
        Args:
            shortcuts: Dictionary of shortcuts to render
            
        Returns:
            List of widgets to display
        """
        widgets = []
        for category, items in shortcuts.items():
            # Section title
            widgets.append(
                Static(f"━━ {category} ━━", classes="help-section help-section-title")
            )
            # Shortcuts in this category
            for key, description in items:
                widgets.append(
                    Static(
                        f"[bold]{key:12}[/bold]  {description}",
                        classes="help-section help-shortcut",
                        markup=True
                    )
                )
        return widgets
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes.
        
        Args:
            event: The input change event
        """
        if event.input.id == "help-search":
            search_term = event.value.lower().strip()
            
            if not search_term:
                self.filtered_shortcuts = self.shortcuts.copy()
            else:
                # Filter shortcuts based on search term
                self.filtered_shortcuts = {}
                for category, items in self.shortcuts.items():
                    filtered_items = [
                        (key, desc) for key, desc in items
                        if search_term in key.lower() or search_term in desc.lower()
                    ]
                    if filtered_items:
                        self.filtered_shortcuts[category] = filtered_items
            
            # Re-render the shortcuts
            content = self.query_one("#help-content", VerticalScroll)
            content.remove_children()
            content.mount_all(self._render_shortcuts(self.filtered_shortcuts))
    
    def action_dismiss(self) -> None:
        """Close the help dialog."""
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
        background: #8338ec;
        color: #ffffff;
        border: solid #06ffa5;
    }
    
    Button:hover {
        background: #ff006e;
        border: heavy #ffbe0b;
    }
    
    Button.primary {
        background: #06ffa5;
        color: #0a0e27;
    }
    
    Button.warning {
        background: #ffbe0b;
        color: #0a0e27;
    }
    
    .hidden {
        display: none;
    }
    """
    
    def __init__(self):
        """Initialize the TODO app."""
        super().__init__()
        self.storage = TodoStorage()
        self.keybindings = KeyBindings()
        self.todos: list[TodoItem] = []
        self._update_bindings()
    
    def _update_bindings(self) -> None:
        """Update app bindings from keybindings configuration."""
        self.BINDINGS = [
            Binding(self.keybindings.get_key("quit"), "quit", "Quit", priority=True),
            Binding(self.keybindings.get_key("toggle_todo"), "toggle_todo", "Toggle", show=True),
            Binding(self.keybindings.get_key("delete_todo"), "delete_todo", "Delete", show=True),
            Binding(self.keybindings.get_key("postpone_todo"), "postpone_todo", "Postpone", show=True),
            Binding(self.keybindings.get_key("show_help"), "show_help", "Help", show=True),
            Binding(self.keybindings.get_key("export_shortcuts"), "export_shortcuts", "Export", show=False),
            Binding(self.keybindings.get_key("customize_keys"), "customize_keys", "Keys", show=False),
            Binding(self.keybindings.get_key("show_tutorial"), "show_tutorial", "Tutorial", show=False),
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
        self._check_first_run()
    
    def _check_first_run(self) -> None:
        """Check if this is the first run and show tutorial."""
        tutorial_marker = Path.home() / ".todo-tui-tutorial-shown"
        if not tutorial_marker.exists():
            # Show tutorial on first run
            self.set_timer(0.5, lambda: self.action_show_tutorial())
            tutorial_marker.touch()
    
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
        """Show the keyboard shortcuts help dialog."""
        self.push_screen(KeyboardShortcutsHelp(self.keybindings))
    
    def action_show_tutorial(self) -> None:
        """Show the interactive tutorial."""
        self.push_screen(TutorialScreen())
    
    def action_customize_keys(self) -> None:
        """Show the key bindings customization dialog."""
        def handle_result(refresh: Optional[bool]) -> None:
            if refresh:
                self._update_bindings()
        
        self.push_screen(CustomizeKeysScreen(self.keybindings), handle_result)
    
    def action_export_shortcuts(self) -> None:
        """Export a printable keyboard shortcuts cheat sheet."""
        try:
            cheat_sheet_path = Path.home() / "todo-tui-shortcuts.txt"
            
            content = []
            content.append("=" * 70)
            content.append("TODO TUI - Keyboard Shortcuts Cheat Sheet")
            content.append("=" * 70)
            content.append("")
            
            # Get shortcuts from help
            help_screen = KeyboardShortcutsHelp(self.keybindings)
            shortcuts = help_screen._get_all_shortcuts()
            
            for category, items in shortcuts.items():
                content.append(f"\n{category}")
                content.append("-" * 70)
                for key, description in items:
                    content.append(f"  {key:15} {description}")
            
            content.append("\n" + "=" * 70)
            content.append("Generated by TODO TUI App")
            content.append(f"Save this file for quick reference!")
            content.append("=" * 70)
            
            cheat_sheet_path.write_text("\n".join(content))
            self.notify(f"Cheat sheet exported to: {cheat_sheet_path}", timeout=5)
            
        except Exception as e:
            self.notify(f"Error exporting cheat sheet: {e}", severity="error")


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
