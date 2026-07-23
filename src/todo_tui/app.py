"""Main Textual application for the TODO TUI app."""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label
from textual.message import Message
from textual.screen import ModalScreen

from .models import TodoItem
from .storage import TodoStorage


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


class ExportScreen(ModalScreen):
    """Modal screen for exporting todos."""
    
    CSS = """
    ExportScreen {
        align: center middle;
    }
    
    #export-dialog {
        width: 60;
        height: auto;
        border: heavy #ff006e;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #export-dialog Static {
        color: #06ffa5;
        text-align: center;
        margin-bottom: 1;
    }
    
    #export-dialog Input {
        margin: 1 0;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose the export dialog."""
        with Container(id="export-dialog"):
            yield Static("💾 Export TODO List 💾")
            yield Static("Enter filename (without extension):")
            yield Input(placeholder="my-todos", id="export-filename")
            yield Static("\nFormat: [j]son or [m]arkdown")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle filename submission."""
        if event.input.id == "export-filename":
            filename = event.value.strip() or "todos-export"
            self.dismiss(filename)
    
    def on_key(self, event) -> None:
        """Handle key presses for format selection."""
        if event.key == "j":
            input_widget = self.query_one("#export-filename", Input)
            filename = input_widget.value.strip() or "todos-export"
            self.dismiss(("json", filename))
        elif event.key == "m":
            input_widget = self.query_one("#export-filename", Input)
            filename = input_widget.value.strip() or "todos-export"
            self.dismiss(("markdown", filename))
        elif event.key == "escape":
            self.dismiss(None)


class ImportScreen(ModalScreen):
    """Modal screen for importing todos."""
    
    CSS = """
    ImportScreen {
        align: center middle;
    }
    
    #import-dialog {
        width: 60;
        height: auto;
        border: heavy #ff006e;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #import-dialog Static {
        color: #06ffa5;
        text-align: center;
        margin-bottom: 1;
    }
    
    #import-dialog Input {
        margin: 1 0;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose the import dialog."""
        with Container(id="import-dialog"):
            yield Static("📥 Import TODO List 📥")
            yield Static("Enter path to JSON file:")
            yield Input(placeholder="path/to/todos.json", id="import-filepath")
            yield Static("\n[r]eplace all or [a]ppend to existing")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle filepath submission."""
        if event.input.id == "import-filepath":
            filepath = event.value.strip()
            if filepath:
                self.dismiss(filepath)
    
    def on_key(self, event) -> None:
        """Handle key presses for mode selection."""
        if event.key == "r":
            input_widget = self.query_one("#import-filepath", Input)
            filepath = input_widget.value.strip()
            if filepath:
                self.dismiss(("replace", filepath))
        elif event.key == "a":
            input_widget = self.query_one("#import-filepath", Input)
            filepath = input_widget.value.strip()
            if filepath:
                self.dismiss(("append", filepath))
        elif event.key == "escape":
            self.dismiss(None)


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
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("space", "toggle_todo", "Toggle", show=True),
        Binding("d", "delete_todo", "Delete", show=True),
        Binding("p", "postpone_todo", "Postpone", show=True),
        Binding("e", "export_todos", "Export", show=True),
        Binding("i", "import_todos", "Import", show=True),
    ]
    
    def __init__(self):
        """Initialize the TODO app."""
        super().__init__()
        self.storage = TodoStorage()
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
    
    def action_export_todos(self) -> None:
        """Export todos to a file."""
        def handle_export(result):
            if result is None:
                return
            
            try:
                if isinstance(result, tuple):
                    format_type, filename = result
                else:
                    # Default to JSON if only filename provided
                    format_type = "json"
                    filename = result
                
                # Determine export path
                export_dir = Path.home() / "todo-exports"
                export_dir.mkdir(exist_ok=True)
                
                if format_type == "json":
                    export_path = export_dir / f"{filename}.json"
                    self.storage.export_json(export_path)
                    self.notify(f"✅ Exported to {export_path}", timeout=3)
                elif format_type == "markdown":
                    export_path = export_dir / f"{filename}.md"
                    self.storage.export_markdown(export_path)
                    self.notify(f"✅ Exported to {export_path}", timeout=3)
                else:
                    self.notify("Invalid format selected", severity="error")
            except Exception as e:
                self.notify(f"❌ Export failed: {e}", severity="error", timeout=5)
        
        self.push_screen(ExportScreen(), handle_export)
    
    def action_import_todos(self) -> None:
        """Import todos from a file."""
        def handle_import(result):
            if result is None:
                return
            
            try:
                if isinstance(result, tuple):
                    mode, filepath = result
                    replace = (mode == "replace")
                else:
                    # Default to append if only filepath provided
                    filepath = result
                    replace = False
                
                import_path = Path(filepath).expanduser()
                count = self.storage.import_json(import_path, replace=replace)
                
                # Reload todos
                self.load_todos()
                
                mode_text = "replaced with" if replace else "imported"
                self.notify(f"✅ {count} todo(s) {mode_text}", timeout=3)
            except FileNotFoundError:
                self.notify(f"❌ File not found: {filepath}", severity="error", timeout=5)
            except ValueError as e:
                self.notify(f"❌ Import failed: {e}", severity="error", timeout=5)
            except Exception as e:
                self.notify(f"❌ Unexpected error: {e}", severity="error", timeout=5)
        
        self.push_screen(ImportScreen(), handle_import)


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
