"""Main Textual application for the TODO TUI app."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, Button
from textual.message import Message
from textual.screen import ModalScreen
from pathlib import Path
from datetime import datetime

from .models import TodoItem
from .storage import TodoStorage
from .keybindings import KeyBindingsManager


class TutorialScreen(ModalScreen):
    """Modal screen for first-time user tutorial."""
    
    CSS = """
    TutorialScreen {
        align: center middle;
    }
    
    #tutorial-dialog {
        width: 90;
        height: auto;
        max-height: 95%;
        border: heavy #06ffa5;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #tutorial-title {
        text-align: center;
        text-style: bold;
        color: #06ffa5;
        background: linear-gradient(90deg, #8338ec 0%, #3a86ff 100%);
        padding: 1;
        margin-bottom: 1;
    }
    
    #tutorial-content {
        height: auto;
        max-height: 35;
        border: round #3a86ff;
        padding: 1 2;
        background: #0f1425;
        margin-bottom: 1;
    }
    
    #tutorial-buttons {
        height: auto;
        align: center middle;
        padding: 1;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("escape,q", "dismiss", "Close", show=False),
    ]
    
    def __init__(self, is_first_run: bool = False):
        """Initialize the tutorial screen.
        
        Args:
            is_first_run: Whether this is the first run of the app
        """
        super().__init__()
        self.is_first_run = is_first_run
    
    def compose(self) -> ComposeResult:
        """Compose the tutorial screen."""
        with Container(id="tutorial-dialog"):
            yield Static("🎓 Welcome to TODO TUI!", id="tutorial-title")
            with VerticalScroll(id="tutorial-content"):
                yield Static(self._get_tutorial_content())
            with Horizontal(id="tutorial-buttons"):
                yield Button("Got it!", id="tutorial-done", variant="success")
                if self.is_first_run:
                    yield Button("Don't show again", id="tutorial-skip", variant="default")
    
    def _get_tutorial_content(self) -> str:
        """Generate the tutorial content."""
        content = []
        
        content.append("[bold #06ffa5]👋 Welcome![/]")
        content.append("")
        content.append("TODO TUI is a keyboard-driven task management app.")
        content.append("Let's get you started with a quick tutorial!")
        content.append("")
        
        content.append("[bold #ffbe0b]📝 Adding Your First TODO[/]")
        content.append("  1. Press [#06ffa5]Tab[/] to focus the input field")
        content.append("  2. Type your task (e.g., 'Buy groceries')")
        content.append("  3. Press [#06ffa5]Enter[/] to add it to your list")
        content.append("")
        
        content.append("[bold #ffbe0b]✅ Managing TODOs[/]")
        content.append("  • Use [#06ffa5]↑/↓[/] to navigate through your list")
        content.append("  • Press [#06ffa5]Space[/] to mark a task as complete")
        content.append("  • Press [#06ffa5]d[/] to delete a task")
        content.append("  • Press [#06ffa5]p[/] to postpone until tomorrow")
        content.append("")
        
        content.append("[bold #ffbe0b]⌨️  Essential Shortcuts[/]")
        content.append("  • [#06ffa5]?[/] - Show all keyboard shortcuts (your best friend!)")
        content.append("  • [#06ffa5]Ctrl+E[/] - Export your todos")
        content.append("  • [#06ffa5]Ctrl+I[/] - Import todos from file")
        content.append("  • [#06ffa5]q[/] - Quit (your data is auto-saved)")
        content.append("")
        
        content.append("[bold #ffbe0b]💡 Pro Tips[/]")
        content.append("  • Everything is auto-saved to [#8ecae6]~/.todo-tui.json[/]")
        content.append("  • Press [#06ffa5]?[/] anytime to search for shortcuts")
        content.append("  • Customize key bindings in the shortcuts screen")
        content.append("  • Export a cheat sheet for offline reference")
        content.append("")
        
        content.append("[bold #06ffa5]Ready to be productive! 🚀[/]")
        content.append("")
        content.append("Remember: Press [#06ffa5]?[/] anytime to see all shortcuts!")
        
        return "\n".join(content)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "tutorial-done":
            self.dismiss()
        elif event.button.id == "tutorial-skip":
            # Mark tutorial as seen
            self._mark_tutorial_seen()
            self.dismiss()
    
    def _mark_tutorial_seen(self) -> None:
        """Mark the tutorial as seen so it doesn't show on next run."""
        marker_file = Path.home() / ".todo-tui-tutorial-seen"
        marker_file.touch()
    
    def action_dismiss(self) -> None:
        """Dismiss the tutorial screen."""
        self.app.pop_screen()


class KeyboardShortcutsScreen(ModalScreen):
    """Modal screen displaying keyboard shortcuts reference with search."""
    
    CSS = """
    KeyboardShortcutsScreen {
        align: center middle;
    }
    
    #shortcuts-dialog {
        width: 85;
        height: auto;
        max-height: 95%;
        border: heavy #ff006e;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #shortcuts-title {
        text-align: center;
        text-style: bold;
        color: #ff006e;
        background: linear-gradient(90deg, #8338ec 0%, #3a86ff 100%);
        padding: 1;
        margin-bottom: 1;
    }
    
    #shortcuts-search-container {
        height: auto;
        padding: 0 1;
        margin-bottom: 1;
    }
    
    #shortcuts-search {
        border: solid #06ffa5;
        background: #0f1425;
        margin: 0;
    }
    
    #shortcuts-content {
        height: auto;
        max-height: 30;
        border: round #3a86ff;
        padding: 1 2;
        background: #0f1425;
        margin-bottom: 1;
    }
    
    #shortcuts-actions {
        height: auto;
        align: center middle;
        padding: 1;
        margin-top: 1;
    }
    
    .action-button {
        margin: 0 1;
    }
    
    #shortcuts-footer {
        text-align: center;
        color: #7209b7;
        text-style: italic;
        padding: 1;
    }
    
    .shortcut-row {
        color: #ffffff;
        margin-bottom: 0;
    }
    
    .shortcut-key {
        color: #ffbe0b;
        text-style: bold;
    }
    
    .no-results {
        color: #ff006e;
        text-style: italic;
        text-align: center;
        padding: 2;
    }
    """
    
    BINDINGS = [
        Binding("escape,question_mark", "dismiss", "Close", show=False),
    ]
    
    def __init__(self, keybindings_manager: KeyBindingsManager):
        """Initialize the shortcuts screen.
        
        Args:
            keybindings_manager: The key bindings manager
        """
        super().__init__()
        self.keybindings_manager = keybindings_manager
        self.search_query = ""
    
    def compose(self) -> ComposeResult:
        """Compose the shortcuts reference screen."""
        with Container(id="shortcuts-dialog"):
            yield Static("⌨️  Keyboard Shortcuts Reference", id="shortcuts-title")
            with Vertical(id="shortcuts-search-container"):
                yield Input(
                    placeholder="🔍 Search shortcuts (action, key, or description)...",
                    id="shortcuts-search"
                )
            with VerticalScroll(id="shortcuts-content"):
                yield Static(self._get_shortcuts_content())
            with Horizontal(id="shortcuts-actions"):
                yield Button("Export Cheat Sheet", id="export-cheat", variant="primary", classes="action-button")
                yield Button("Customize Bindings", id="customize-bindings", variant="default", classes="action-button")
                yield Button("Reset to Defaults", id="reset-bindings", variant="warning", classes="action-button")
            yield Static("Press ESC or ? to close | Type to search", id="shortcuts-footer")
    
    def _get_shortcuts_content(self, search_query: str = "") -> str:
        """Generate the shortcuts reference content.
        
        Args:
            search_query: Optional search query to filter shortcuts
            
        Returns:
            Formatted content string
        """
        content = []
        
        if search_query:
            # Search mode
            results = self.keybindings_manager.search_bindings(search_query)
            if results:
                content.append(f"[bold #06ffa5]Search Results for '{search_query}' ({len(results)} found)[/]")
                content.append("")
                for binding in results:
                    content.append(f"  [#ffbe0b]{binding.key}[/] → {binding.description}")
                    content.append(f"     [dim]Category: {binding.category}[/]")
                    content.append("")
            else:
                content.append(f"[#ff006e]No shortcuts found matching '{search_query}'[/]")
                content.append("")
                content.append("[dim]Try searching for:[/]")
                content.append("  • Action names (toggle, delete, postpone)")
                content.append("  • Keys (space, q, tab)")
                content.append("  • Categories (Navigation, Todo, Application)")
        else:
            # Show all shortcuts organized by category
            categories = self.keybindings_manager.get_bindings_by_category()
            
            for category, bindings in sorted(categories.items()):
                content.append(f"[bold #06ffa5]{category}[/]")
                for binding in bindings:
                    key_display = binding.key.replace("_", " ").title()
                    content.append(f"  [#ffbe0b]{key_display}[/] → {binding.description}")
                content.append("")
            
            # Add tips section
            content.append("[bold #06ffa5]💡 Tips[/]")
            content.append("  • All todos are automatically saved")
            content.append("  • Postponed items show until date indicator")
            content.append("  • Completed items appear with strikethrough")
            content.append("  • Data is stored in ~/.todo-tui.json")
            content.append("  • Use search above to quickly find any shortcut")
            content.append("  • Export cheat sheet for offline reference")
            content.append("  • Customize any key binding to your preference")
        
        return "\n".join(content)
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if event.input.id == "shortcuts-search":
            self.search_query = event.value.strip()
            content_widget = self.query_one("#shortcuts-content")
            content_widget.query_one(Static).update(
                self._get_shortcuts_content(self.search_query)
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "export-cheat":
            self._export_cheat_sheet()
        elif event.button.id == "customize-bindings":
            self.app.notify("Key binding customization coming in next update!", timeout=3)
        elif event.button.id == "reset-bindings":
            self.keybindings_manager.reset_to_defaults()
            self.app.notify("Key bindings reset to defaults", timeout=2)
            # Refresh the display
            content_widget = self.query_one("#shortcuts-content")
            content_widget.query_one(Static).update(
                self._get_shortcuts_content(self.search_query)
            )
    
    def _export_cheat_sheet(self) -> None:
        """Export keyboard shortcuts as a text file."""
        output_file = Path.home() / "todo-tui-shortcuts.txt"
        
        try:
            with open(output_file, "w") as f:
                f.write("=" * 70 + "\n")
                f.write("TODO TUI - Keyboard Shortcuts Cheat Sheet\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                categories = self.keybindings_manager.get_bindings_by_category()
                
                for category, bindings in sorted(categories.items()):
                    f.write(f"\n{category}\n")
                    f.write("-" * len(category) + "\n\n")
                    
                    for binding in bindings:
                        key_display = binding.key.replace("_", " ").title()
                        f.write(f"  {key_display:20} {binding.description}\n")
                
                f.write("\n\n" + "=" * 70 + "\n")
                f.write("Tips:\n")
                f.write("=" * 70 + "\n\n")
                f.write("• All todos are automatically saved to ~/.todo-tui.json\n")
                f.write("• Postponed items show until date indicator\n")
                f.write("• Completed items appear with strikethrough\n")
                f.write("• Press '?' anytime to see shortcuts in-app\n")
                f.write("• You can customize key bindings in the shortcuts screen\n\n")
            
            self.app.notify(f"Cheat sheet exported to {output_file}", timeout=4, severity="information")
        except Exception as e:
            self.app.notify(f"Error exporting cheat sheet: {e}", severity="error")
    
    def action_dismiss(self) -> None:
        """Dismiss the shortcuts screen."""
        self.app.pop_screen()


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
        border: solid #3a86ff;
        background: #1a1f3a;
        color: #06ffa5;
    }
    
    Button:hover {
        background: #240046;
        border: heavy #ff006e;
        color: #ffffff;
    }
    
    Button.-primary {
        background: #3a86ff;
        color: #ffffff;
        border: heavy #06ffa5;
    }
    
    Button.-success {
        background: #06ffa5;
        color: #0a0e27;
        border: heavy #06ffa5;
    }
    
    Button.-warning {
        background: #ffbe0b;
        color: #0a0e27;
        border: heavy #ff006e;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("space", "toggle_todo", "Toggle", show=True),
        Binding("d", "delete_todo", "Delete", show=True),
        Binding("p", "postpone_todo", "Postpone", show=True),
        Binding("question_mark", "show_shortcuts", "Help", show=True),
        Binding("ctrl+t", "show_tutorial", "Tutorial", show=False),
    ]
    
    def __init__(self):
        """Initialize the TODO app."""
        super().__init__()
        self.storage = TodoStorage()
        self.keybindings_manager = KeyBindingsManager()
        self.todos: list[TodoItem] = []
    
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
        if self._is_first_run():
            self.push_screen(TutorialScreen(is_first_run=True))
    
    def _is_first_run(self) -> bool:
        """Check if this is the first run of the app.
        
        Returns:
            True if first run, False otherwise
        """
        marker_file = Path.home() / ".todo-tui-tutorial-seen"
        return not marker_file.exists()
    
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
        """Show the keyboard shortcuts reference screen."""
        self.push_screen(KeyboardShortcutsScreen(self.keybindings_manager))
    
    def action_show_tutorial(self) -> None:
        """Show the tutorial screen."""
        self.push_screen(TutorialScreen(is_first_run=False))


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
