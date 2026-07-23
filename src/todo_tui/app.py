"""Main Textual application for the TODO TUI app."""

from typing import Dict, Optional
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label, Button, TextArea
from textual.screen import Screen, ModalScreen
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
        
        # Add description indicator
        has_desc = " [+]" if self.todo.has_description() else ""
        
        self._label = Label(f"[{status}] {self.todo.title}{postponed}{has_desc}")
        if style:
            self._label.add_class(style)
    
    def compose(self) -> ComposeResult:
        """Compose the list item."""
        yield self._label


class DescriptionScreen(ModalScreen[Optional[str]]):
    """Modal screen for viewing and editing task descriptions."""
    
    CSS = """
    DescriptionScreen {
        align: center middle;
    }
    
    #description-dialog {
        width: 80;
        height: 24;
        border: heavy #8338ec;
        background: #1a1f3a;
        padding: 1;
    }
    
    #description-title {
        color: #ff006e;
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
    }
    
    #description-textarea {
        height: 1fr;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
        margin: 1 0;
    }
    
    #description-buttons {
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    
    Button {
        margin: 0 1;
        background: #8338ec;
        color: #ffffff;
        border: solid #06ffa5;
    }
    
    Button:hover {
        background: #ff006e;
        border: heavy #ffbe0b;
    }
    
    Button:focus {
        background: #3a86ff;
        border: heavy #06ffa5;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
        Binding("ctrl+s", "save", "Save", show=True),
    ]
    
    def __init__(self, todo: TodoItem) -> None:
        """Initialize the description screen.
        
        Args:
            todo: The TodoItem to edit description for
        """
        super().__init__()
        self.todo = todo
    
    def compose(self) -> ComposeResult:
        """Compose the description screen."""
        with Container(id="description-dialog"):
            yield Static(f"📝 Edit Description: {self.todo.title}", id="description-title")
            
            # Create textarea with existing description or empty
            initial_text = self.todo.description if self.todo.description else ""
            yield TextArea(initial_text, id="description-textarea")
            
            with Container(id="description-buttons"):
                yield Button("Save [Ctrl+S]", variant="primary", id="save-btn")
                yield Button("Cancel [ESC]", variant="default", id="cancel-btn")
    
    def on_mount(self) -> None:
        """Focus the textarea when the screen is mounted."""
        textarea = self.query_one("#description-textarea", TextArea)
        textarea.focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "save-btn":
            self.action_save()
        elif event.button.id == "cancel-btn":
            self.action_cancel()
    
    def action_save(self) -> None:
        """Save the description and close the screen."""
        textarea = self.query_one("#description-textarea", TextArea)
        description = textarea.text.strip()
        # Return the description (or None if empty)
        self.dismiss(description if description else None)
    
    def action_cancel(self) -> None:
        """Cancel and close the screen without saving."""
        self.dismiss(None)


class DescriptionViewScreen(ModalScreen[bool]):
    """Modal screen for viewing task description with markdown rendering."""
    
    CSS = """
    DescriptionViewScreen {
        align: center middle;
    }
    
    #view-dialog {
        width: 80;
        height: 24;
        border: heavy #8338ec;
        background: #1a1f3a;
        padding: 1;
    }
    
    #view-title {
        color: #ff006e;
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
    }
    
    #view-content {
        height: 1fr;
        border: solid #06ffa5;
        background: #0f1425;
        color: #06ffa5;
        margin: 1 0;
        padding: 1;
    }
    
    #view-buttons {
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    
    .markdown-heading {
        color: #ff006e;
        text-style: bold;
    }
    
    .markdown-link {
        color: #3a86ff;
        text-style: underline;
    }
    
    .markdown-list {
        color: #ffbe0b;
    }
    
    .markdown-code {
        color: #06ffa5;
        text-style: italic;
    }
    """
    
    BINDINGS = [
        Binding("escape", "close", "Close", priority=True),
        Binding("e", "edit", "Edit", show=True),
    ]
    
    def __init__(self, todo: TodoItem) -> None:
        """Initialize the description view screen.
        
        Args:
            todo: The TodoItem to view description for
        """
        super().__init__()
        self.todo = todo
    
    def compose(self) -> ComposeResult:
        """Compose the description view screen."""
        with Container(id="view-dialog"):
            yield Static(f"📖 Description: {self.todo.title}", id="view-title")
            
            with ScrollableContainer(id="view-content"):
                yield Static(self._render_markdown(), markup=True)
            
            with Container(id="view-buttons"):
                yield Button("Edit [E]", variant="primary", id="edit-btn")
                yield Button("Close [ESC]", variant="default", id="close-btn")
    
    def _render_markdown(self) -> str:
        """Render the description with basic markdown support.
        
        Returns:
            Formatted text with markup
        """
        if not self.todo.description:
            return "[dim]No description available[/dim]"
        
        lines = self.todo.description.split("\n")
        rendered_lines = []
        
        for line in lines:
            # Handle headings
            if line.startswith("# "):
                rendered_lines.append(f"[bold #ff006e]{line[2:]}[/]")
            elif line.startswith("## "):
                rendered_lines.append(f"[bold #ff006e]{line[3:]}[/]")
            elif line.startswith("### "):
                rendered_lines.append(f"[bold #ff006e]{line[4:]}[/]")
            # Handle lists
            elif line.strip().startswith("- ") or line.strip().startswith("* "):
                rendered_lines.append(f"[#ffbe0b]{line}[/]")
            # Handle links (basic pattern)
            elif "http://" in line or "https://" in line:
                # Simple link detection
                parts = []
                for word in line.split():
                    if word.startswith("http://") or word.startswith("https://"):
                        parts.append(f"[link={word}][#3a86ff underline]{word}[/][/]")
                    else:
                        parts.append(word)
                rendered_lines.append(" ".join(parts))
            # Handle code blocks (inline)
            elif "`" in line:
                # Replace backticks with italic green
                formatted = line.replace("`", "[#06ffa5 italic]", 1)
                # Replace closing backtick
                if "`" in formatted:
                    formatted = formatted.replace("`", "[/]", 1)
                rendered_lines.append(formatted)
            else:
                rendered_lines.append(line)
        
        return "\n".join(rendered_lines)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "edit-btn":
            self.action_edit()
        elif event.button.id == "close-btn":
            self.action_close()
    
    def action_edit(self) -> None:
        """Open edit mode."""
        self.dismiss(True)  # Signal to edit
    
    def action_close(self) -> None:
        """Close the view without editing."""
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
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("space", "toggle_todo", "Toggle", show=True),
        Binding("d", "delete_todo", "Delete", show=True),
        Binding("p", "postpone_todo", "Postpone", show=True),
        Binding("v", "view_description", "View Desc", show=True),
        Binding("n", "edit_description", "Add/Edit Note", show=True),
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
    
    async def action_view_description(self) -> None:
        """View the description of the selected todo."""
        list_view = self.query_one("#todo-list", ListView)
        if list_view.index is not None and 0 <= list_view.index < len(self.todos):
            todo = self.todos[list_view.index]
            
            if not todo.has_description():
                self.notify("No description. Press 'n' to add one.", timeout=2)
                return
            
            # Show view screen
            should_edit = await self.push_screen_wait(DescriptionViewScreen(todo))
            
            # If user pressed edit, open edit screen
            if should_edit:
                await self._edit_description(list_view.index)
    
    async def action_edit_description(self) -> None:
        """Edit the description of the selected todo."""
        list_view = self.query_one("#todo-list", ListView)
        if list_view.index is not None and 0 <= list_view.index < len(self.todos):
            await self._edit_description(list_view.index)
    
    async def _edit_description(self, index: int) -> None:
        """Helper method to edit description at given index.
        
        Args:
            index: Index of the todo in the list
        """
        todo = self.todos[index]
        list_view = self.query_one("#todo-list", ListView)
        
        # Show edit screen
        new_description = await self.push_screen_wait(DescriptionScreen(todo))
        
        # If user saved (returned a value), update the todo
        if new_description is not None:
            todo.description = new_description if new_description else None
            try:
                self.storage.update(todo)
                self._refresh_list()
                # Restore selection
                list_view.index = index
                if new_description:
                    self.notify("Description saved", timeout=2)
                else:
                    self.notify("Description cleared", timeout=2)
            except Exception as e:
                self.notify(f"Error updating description: {e}", severity="error")


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
