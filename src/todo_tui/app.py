"""Main Textual application for the TODO TUI app."""

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, Button
from textual.screen import ModalScreen
from textual.message import Message

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


class ExportScreen(ModalScreen[tuple[Path, str]]):
    """Modal screen for exporting TODO items."""
    
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
        margin: 1 0;
    }
    
    #export-dialog Input {
        margin: 0 0 1 0;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
    }
    
    #export-dialog Button {
        margin: 0 1;
    }
    
    #export-buttons {
        width: 100%;
        height: auto;
        align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the export dialog."""
        with Container(id="export-dialog"):
            yield Static("📤 Export TODO List")
            yield Static("Enter export path (with extension: .json, .csv, .md, .html):")
            yield Input(placeholder="~/my-todos.json", id="export-path")
            with Horizontal(id="export-buttons"):
                yield Button("Export", variant="success", id="export-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")
    
    def on_mount(self) -> None:
        """Focus the input when mounted."""
        self.query_one("#export-path", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "export-btn":
            self._do_export()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "export-path":
            self._do_export()
    
    def _do_export(self) -> None:
        """Process the export."""
        path_input = self.query_one("#export-path", Input)
        path_str = path_input.value.strip()
        
        if not path_str:
            self.app.notify("Please enter a path", severity="warning")
            return
        
        path = Path(path_str).expanduser()
        
        # Determine format from extension
        ext = path.suffix.lower()
        format_map = {
            '.json': 'json',
            '.csv': 'csv',
            '.md': 'markdown',
            '.markdown': 'markdown',
            '.html': 'html',
            '.htm': 'html',
        }
        
        if ext not in format_map:
            self.app.notify("Unsupported file extension. Use .json, .csv, .md, or .html", severity="error")
            return
        
        self.dismiss((path, format_map[ext]))
    
    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)


class ImportScreen(ModalScreen[tuple[Path, str]]):
    """Modal screen for importing TODO items."""
    
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
        margin: 1 0;
    }
    
    #import-dialog Input {
        margin: 0 0 1 0;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
    }
    
    #import-dialog Button {
        margin: 0 1;
    }
    
    #import-buttons {
        width: 100%;
        height: auto;
        align: center middle;
    }
    
    #mode-info {
        color: #ffbe0b;
        text-style: italic;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
        Binding("ctrl+m", "toggle_mode", "Toggle Mode", show=True),
    ]
    
    def __init__(self):
        """Initialize the import screen."""
        super().__init__()
        self.mode = "merge"  # Default mode
    
    def compose(self) -> ComposeResult:
        """Compose the import dialog."""
        with Container(id="import-dialog"):
            yield Static("📥 Import TODO List")
            yield Static("Enter path to JSON file to import:")
            yield Input(placeholder="~/my-todos.json", id="import-path")
            yield Static(f"Mode: {self.mode} (Ctrl+M to toggle)", id="mode-info")
            with Horizontal(id="import-buttons"):
                yield Button("Import", variant="success", id="import-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")
    
    def on_mount(self) -> None:
        """Focus the input when mounted."""
        self.query_one("#import-path", Input).focus()
    
    def action_toggle_mode(self) -> None:
        """Toggle between merge and replace mode."""
        self.mode = "replace" if self.mode == "merge" else "merge"
        mode_label = self.query_one("#mode-info", Static)
        mode_label.update(f"Mode: {self.mode} (Ctrl+M to toggle)")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "import-btn":
            self._do_import()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "import-path":
            self._do_import()
    
    def _do_import(self) -> None:
        """Process the import."""
        path_input = self.query_one("#import-path", Input)
        path_str = path_input.value.strip()
        
        if not path_str:
            self.app.notify("Please enter a path", severity="warning")
            return
        
        path = Path(path_str).expanduser()
        
        if not path.suffix.lower() == '.json':
            self.app.notify("Only JSON files are supported for import", severity="error")
            return
        
        self.dismiss((path, self.mode))
    
    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)


class ArchiveConfirmScreen(ModalScreen[bool]):
    """Modal screen for confirming archive operation."""
    
    CSS = """
    ArchiveConfirmScreen {
        align: center middle;
    }
    
    #archive-dialog {
        width: 60;
        height: auto;
        border: heavy #ff006e;
        background: #1a1f3a;
        padding: 1 2;
    }
    
    #archive-dialog Static {
        color: #06ffa5;
        margin: 1 0;
    }
    
    #archive-dialog Button {
        margin: 0 1;
    }
    
    #archive-buttons {
        width: 100%;
        height: auto;
        align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]
    
    def __init__(self, completed_count: int):
        """Initialize the archive confirmation screen.
        
        Args:
            completed_count: Number of completed todos to archive
        """
        super().__init__()
        self.completed_count = completed_count
    
    def compose(self) -> ComposeResult:
        """Compose the archive confirmation dialog."""
        with Container(id="archive-dialog"):
            yield Static("📦 Archive Completed Tasks")
            yield Static(
                f"This will move {self.completed_count} completed task(s) "
                f"to an archive file and remove them from the main list."
            )
            yield Static("Do you want to continue?")
            with Horizontal(id="archive-buttons"):
                yield Button("Archive", variant="success", id="archive-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(False)
        elif event.button.id == "archive-btn":
            self.dismiss(True)
    
    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(False)


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
        margin: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("space", "toggle_todo", "Toggle", show=True),
        Binding("d", "delete_todo", "Delete", show=True),
        Binding("p", "postpone_todo", "Postpone", show=True),
        Binding("e", "export_todos", "Export", show=True),
        Binding("i", "import_todos", "Import", show=True),
        Binding("a", "archive_completed", "Archive", show=True),
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
        def handle_export(result: tuple[Path, str] | None) -> None:
            if result is None:
                return
            
            path, format = result
            try:
                self.storage.export(path, format)
                self.notify(f"Exported to {path} ({format} format)", timeout=3)
            except Exception as e:
                self.notify(f"Export failed: {e}", severity="error")
        
        self.push_screen(ExportScreen(), handle_export)
    
    def action_import_todos(self) -> None:
        """Show the import dialog."""
        def handle_import(result: tuple[Path, str] | None) -> None:
            if result is None:
                return
            
            path, mode = result
            try:
                count = self.storage.import_json(path, mode)
                self.load_todos()  # Reload todos
                
                if mode == "replace":
                    self.notify(f"Replaced all todos with {count} items from {path}", timeout=3)
                else:
                    self.notify(f"Imported {count} new items from {path}", timeout=3)
            except FileNotFoundError:
                self.notify(f"File not found: {path}", severity="error")
            except ValueError as e:
                self.notify(f"Import failed: {e}", severity="error")
            except Exception as e:
                self.notify(f"Unexpected error: {e}", severity="error")
        
        self.push_screen(ImportScreen(), handle_import)
    
    def action_archive_completed(self) -> None:
        """Archive completed todos."""
        # Count completed todos
        completed_count = sum(1 for todo in self.todos if todo.completed)
        
        if completed_count == 0:
            self.notify("No completed tasks to archive", timeout=2)
            return
        
        def handle_archive(confirmed: bool) -> None:
            if not confirmed:
                return
            
            try:
                count, archive_path = self.storage.archive_completed()
                self.load_todos()  # Reload todos
                self.notify(
                    f"Archived {count} completed task(s) to {archive_path.name}",
                    timeout=3
                )
            except Exception as e:
                self.notify(f"Archive failed: {e}", severity="error")
        
        self.push_screen(ArchiveConfirmScreen(completed_count), handle_archive)


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
