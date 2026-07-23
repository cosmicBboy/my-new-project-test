"""Main Textual application for the TODO TUI app."""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, Button
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


class ExportScreen(ModalScreen[tuple[str, str]]):
    """Modal screen for exporting TODO items."""
    
    CSS = """
    ExportScreen {
        align: center middle;
    }
    
    #export-dialog {
        width: 60;
        height: auto;
        border: thick #8338ec;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #export-dialog Static {
        margin: 1 0;
        color: #06ffa5;
    }
    
    #export-dialog Input {
        margin: 1 0;
        border: solid #06ffa5;
        background: #0f1425;
    }
    
    #export-buttons {
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    
    #export-buttons Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the export dialog."""
        with Container(id="export-dialog"):
            yield Static("📤 Export TODO Items", classes="dialog-title")
            yield Static("Enter export path (e.g., ~/todos.json):")
            yield Input(placeholder="~/todos-export.json", id="export-path")
            yield Static("Format will be auto-detected from extension")
            yield Static("Supported: .json, .csv, .md, .html")
            with Horizontal(id="export-buttons"):
                yield Button("Export", variant="primary", id="export-btn")
                yield Button("Cancel", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "export-btn":
            path_input = self.query_one("#export-path", Input)
            path_str = path_input.value.strip()
            if path_str:
                # Detect format from extension
                path = Path(path_str).expanduser()
                ext = path.suffix.lower()
                if ext in ('.json', '.csv', '.md', '.html'):
                    format_map = {'.json': 'json', '.csv': 'csv', '.md': 'markdown', '.html': 'html'}
                    self.dismiss((path_str, format_map.get(ext, 'json')))
                else:
                    self.app.notify("Unsupported file extension. Use .json, .csv, .md, or .html", severity="error")
        else:
            self.action_cancel()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "export-path":
            self.query_one("#export-btn", Button).press()
    
    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)


class ImportScreen(ModalScreen[tuple[str, bool]]):
    """Modal screen for importing TODO items."""
    
    CSS = """
    ImportScreen {
        align: center middle;
    }
    
    #import-dialog {
        width: 60;
        height: auto;
        border: thick #8338ec;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #import-dialog Static {
        margin: 1 0;
        color: #06ffa5;
    }
    
    #import-dialog Input {
        margin: 1 0;
        border: solid #06ffa5;
        background: #0f1425;
    }
    
    #import-buttons {
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    
    #import-buttons Button {
        margin: 0 1;
    }
    
    .merge-indicator {
        color: #ffbe0b;
        text-style: bold;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
        Binding("ctrl+m", "toggle_merge", "Toggle Merge", show=True),
    ]
    
    def __init__(self) -> None:
        """Initialize the import screen."""
        super().__init__()
        self.merge_mode = False
    
    def compose(self) -> ComposeResult:
        """Compose the import dialog."""
        with Container(id="import-dialog"):
            yield Static("📥 Import TODO Items", classes="dialog-title")
            yield Static("Enter import path (must be .json):")
            yield Input(placeholder="~/todos-import.json", id="import-path")
            yield Static("Mode: Replace All", id="mode-indicator", classes="merge-indicator")
            yield Static("(Press Ctrl+M to toggle merge mode)")
            with Horizontal(id="import-buttons"):
                yield Button("Import", variant="primary", id="import-btn")
                yield Button("Cancel", id="cancel-btn")
    
    def action_toggle_merge(self) -> None:
        """Toggle merge mode."""
        self.merge_mode = not self.merge_mode
        mode_text = "Mode: Merge (keep existing)" if self.merge_mode else "Mode: Replace All"
        self.query_one("#mode-indicator", Static).update(mode_text)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "import-btn":
            path_input = self.query_one("#import-path", Input)
            path_str = path_input.value.strip()
            if path_str:
                self.dismiss((path_str, self.merge_mode))
        else:
            self.action_cancel()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "import-path":
            self.query_one("#import-btn", Button).press()
    
    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)


class BackupScreen(ModalScreen[str]):
    """Modal screen for backup operations."""
    
    CSS = """
    BackupScreen {
        align: center middle;
    }
    
    #backup-dialog {
        width: 60;
        height: auto;
        border: thick #8338ec;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #backup-dialog Static {
        margin: 1 0;
        color: #06ffa5;
    }
    
    #backup-buttons {
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    
    #backup-buttons Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the backup dialog."""
        with Container(id="backup-dialog"):
            yield Static("💾 Backup Operations", classes="dialog-title")
            yield Static("Choose an action:")
            with Horizontal(id="backup-buttons"):
                yield Button("Create Backup", variant="primary", id="create-btn")
                yield Button("List Backups", id="list-btn")
                yield Button("Cancel", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "create-btn":
            self.dismiss("create")
        elif event.button.id == "list-btn":
            self.dismiss("list")
        else:
            self.action_cancel()
    
    def action_cancel(self) -> None:
        """Cancel the dialog."""
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
    
    Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("space", "toggle_todo", "Toggle", show=True),
        Binding("d", "delete_todo", "Delete", show=True),
        Binding("p", "postpone_todo", "Postpone", show=True),
        Binding("e", "export", "Export", show=True),
        Binding("i", "import_todos", "Import", show=True),
        Binding("b", "backup", "Backup", show=True),
        Binding("a", "archive", "Archive", show=True),
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
        
        # Notify user if automatic backup was created on startup
        backups = self.storage.list_backups()
        if backups:
            # Check if we have recent automatic backups
            self.notify("💾 Automatic backups enabled (backups created daily)", timeout=3)
    
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
    
    def action_export(self) -> None:
        """Open export dialog."""
        self.push_screen(ExportScreen(), self._handle_export)
    
    def _handle_export(self, result: tuple[str, str] | None) -> None:
        """Handle export dialog result."""
        if result is None:
            return
        
        path_str, format = result
        path = Path(path_str).expanduser()
        
        try:
            # Create parent directory if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export todos
            self.storage.export(path, format=format, todos=self.todos)
            self.notify(f"✅ Exported {len(self.todos)} todos to {path}", timeout=3)
        except Exception as e:
            self.notify(f"Export failed: {e}", severity="error")
    
    def action_import_todos(self) -> None:
        """Open import dialog."""
        self.push_screen(ImportScreen(), self._handle_import)
    
    def _handle_import(self, result: tuple[str, bool] | None) -> None:
        """Handle import dialog result."""
        if result is None:
            return
        
        path_str, merge = result
        path = Path(path_str).expanduser()
        
        try:
            imported_todos = self.storage.import_json(path, merge=merge)
            self.load_todos()
            
            mode = "merged" if merge else "imported"
            self.notify(f"✅ Successfully {mode} {len(imported_todos)} todos", timeout=3)
        except FileNotFoundError:
            self.notify(f"File not found: {path}", severity="error")
        except ValueError as e:
            self.notify(f"Import failed: {e}", severity="error")
        except Exception as e:
            self.notify(f"Import error: {e}", severity="error")
    
    def action_backup(self) -> None:
        """Open backup dialog."""
        self.push_screen(BackupScreen(), self._handle_backup)
    
    def _handle_backup(self, action: str | None) -> None:
        """Handle backup dialog result."""
        if action is None:
            return
        
        if action == "create":
            try:
                backup_path = self.storage.create_backup()
                self.notify(f"✅ Backup created: {backup_path}", timeout=3)
            except Exception as e:
                self.notify(f"Backup failed: {e}", severity="error")
        
        elif action == "list":
            try:
                backups = self.storage.list_backups()
                if backups:
                    backup_list = "\n".join([f"  • {b.name}" for b in backups[:5]])
                    self.notify(f"Recent backups:\n{backup_list}", timeout=5)
                else:
                    self.notify("No backups found", timeout=3)
            except Exception as e:
                self.notify(f"Error listing backups: {e}", severity="error")
    
    def action_archive(self) -> None:
        """Archive completed todos."""
        try:
            count = self.storage.archive_completed()
            if count > 0:
                self.load_todos()
                self.notify(f"✅ Archived {count} completed todo(s)", timeout=3)
            else:
                self.notify("No completed todos to archive", timeout=2)
        except Exception as e:
            self.notify(f"Archive failed: {e}", severity="error")
    
    def on_unmount(self) -> None:
        """Cleanup when app is shutting down."""
        # Create final automatic backup if needed
        self.storage.shutdown()


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
