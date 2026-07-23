"""Main Textual application for the TODO TUI app."""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label
from textual.message import Message
from textual.screen import Screen, ModalScreen

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


class ExportScreen(ModalScreen[str]):
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
        padding: 2;
    }
    
    #export-dialog Static {
        color: #06ffa5;
        margin-bottom: 1;
    }
    
    #export-dialog Input {
        margin-bottom: 1;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
    }
    
    #export-dialog Input:focus {
        border: heavy #ff006e;
    }
    
    .export-help {
        color: #7209b7;
        text-style: italic;
        margin-bottom: 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the export dialog."""
        with Container(id="export-dialog"):
            yield Static("📤 Export TODO Items")
            yield Static("Enter export path:", classes="export-help")
            yield Input(
                placeholder="e.g., ~/todos.json or ~/todos.csv or ~/todos.md",
                id="export-path"
            )
            yield Static("Formats: .json, .csv, .md", classes="export-help")
            yield Static("Press Enter to export, Esc to cancel", classes="export-help")
    
    def on_mount(self) -> None:
        """Focus the input when mounted."""
        self.query_one("#export-path", Input).focus()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle export path submission."""
        if event.input.id == "export-path":
            path = event.value.strip()
            if path:
                self.dismiss(path)
    
    def action_cancel(self) -> None:
        """Cancel the export."""
        self.dismiss(None)


class ImportScreen(ModalScreen[tuple[str, bool]]):
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
        padding: 2;
    }
    
    #import-dialog Static {
        color: #06ffa5;
        margin-bottom: 1;
    }
    
    #import-dialog Input {
        margin-bottom: 1;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
    }
    
    #import-dialog Input:focus {
        border: heavy #ff006e;
    }
    
    .import-help {
        color: #7209b7;
        text-style: italic;
        margin-bottom: 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+m", "toggle_merge", "Toggle Merge"),
    ]
    
    def __init__(self):
        """Initialize the import screen."""
        super().__init__()
        self.merge_mode = False
    
    def compose(self) -> ComposeResult:
        """Compose the import dialog."""
        with Container(id="import-dialog"):
            yield Static("📥 Import TODO Items")
            yield Static("Enter import path (JSON only):", classes="import-help")
            yield Input(
                placeholder="e.g., ~/todos.json",
                id="import-path"
            )
            yield Static("Press Enter to import, Esc to cancel", classes="import-help")
            yield Static("Ctrl+M: Toggle merge mode", classes="import-help", id="merge-indicator")
    
    def on_mount(self) -> None:
        """Focus the input when mounted."""
        self.query_one("#import-path", Input).focus()
        self._update_merge_indicator()
    
    def _update_merge_indicator(self) -> None:
        """Update the merge mode indicator."""
        indicator = self.query_one("#merge-indicator", Static)
        if self.merge_mode:
            indicator.update("Mode: MERGE with existing todos (Ctrl+M to toggle)")
        else:
            indicator.update("Mode: REPLACE all todos (Ctrl+M to toggle)")
    
    def action_toggle_merge(self) -> None:
        """Toggle merge mode."""
        self.merge_mode = not self.merge_mode
        self._update_merge_indicator()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle import path submission."""
        if event.input.id == "import-path":
            path = event.value.strip()
            if path:
                self.dismiss((path, self.merge_mode))
    
    def action_cancel(self) -> None:
        """Cancel the import."""
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
        """Show the export dialog."""
        self.push_screen(ExportScreen(), self._handle_export)
    
    def _handle_export(self, export_path: str | None) -> None:
        """Handle the export operation.
        
        Args:
            export_path: Path to export to, or None if cancelled
        """
        if export_path is None:
            return
        
        try:
            # Expand user home directory
            path = Path(export_path).expanduser()
            
            # Determine format from extension
            suffix = path.suffix.lower()
            
            if suffix == '.json':
                self.storage.export_json(path)
                self.notify(f"✅ Exported to {path} (JSON format)", timeout=3)
            elif suffix == '.csv':
                self.storage.export_csv(path)
                self.notify(f"✅ Exported to {path} (CSV format)", timeout=3)
            elif suffix == '.md':
                self.storage.export_markdown(path)
                self.notify(f"✅ Exported to {path} (Markdown format)", timeout=3)
            else:
                self.notify(f"❌ Unsupported format: {suffix}. Use .json, .csv, or .md", severity="error")
        except Exception as e:
            self.notify(f"❌ Export failed: {e}", severity="error")
    
    def action_import_todos(self) -> None:
        """Show the import dialog."""
        self.push_screen(ImportScreen(), self._handle_import)
    
    def _handle_import(self, result: tuple[str, bool] | None) -> None:
        """Handle the import operation.
        
        Args:
            result: Tuple of (import_path, merge_mode), or None if cancelled
        """
        if result is None:
            return
        
        import_path, merge_mode = result
        
        try:
            # Expand user home directory
            path = Path(import_path).expanduser()
            
            # Import the todos
            imported_todos = self.storage.import_json(path, merge=merge_mode)
            
            # Reload todos and refresh display
            self.load_todos()
            
            mode_str = "merged" if merge_mode else "replaced"
            count = len(imported_todos)
            self.notify(f"✅ Imported {count} todo(s) from {path} ({mode_str})", timeout=3)
        except FileNotFoundError:
            self.notify(f"❌ File not found: {import_path}", severity="error")
        except ValueError as e:
            self.notify(f"❌ Import failed: {e}", severity="error")
        except Exception as e:
            self.notify(f"❌ Import failed: {e}", severity="error")


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
