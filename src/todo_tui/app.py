"""Main Textual application for the TODO TUI app."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label
from textual.message import Message

from .models import TodoItem
from .storage import TodoStorage, PreferencesStorage
from .themes import (
    THEMES, 
    ThemeName, 
    LayoutDensity, 
    FontSize, 
    get_layout_padding, 
    get_layout_margin,
    get_font_size_class,
    get_base_css,
    load_custom_theme,
)


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
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("space", "toggle_todo", "Toggle", show=True),
        Binding("d", "delete_todo", "Delete", show=True),
        Binding("p", "postpone_todo", "Postpone", show=True),
        Binding("t", "cycle_theme", "Theme", show=True),
        Binding("l", "cycle_layout", "Layout", show=True),
        Binding("f", "cycle_font_size", "Font", show=True),
    ]
    
    def __init__(self):
        """Initialize the TODO app."""
        super().__init__()
        self.storage = TodoStorage()
        self.preferences = PreferencesStorage()
        self.todos: list[TodoItem] = []
        
        # Load preferences
        self.current_theme = self.preferences.get_theme()
        self.layout_density = LayoutDensity(self.preferences.get_layout_density())
        self.font_size = FontSize(self.preferences.get_font_size())
        
        # Load custom themes
        self.custom_themes = {}
        for theme_data in self.preferences.get_custom_themes():
            theme = load_custom_theme(theme_data)
            if theme:
                self.custom_themes[theme.name] = theme
        
        # Build combined theme registry
        self.all_themes = {**THEMES, **self.custom_themes}
    
    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        yield Header()
        with Container(id="todo-container"):
            yield ListView(id="todo-list")
            with Vertical(id="input-container"):
                yield Static(self._get_input_label())
                yield Input(placeholder="Enter a new task...", id="todo-input")
        yield Footer()
    
    def _get_input_label(self) -> str:
        """Get the input label based on current theme."""
        if self.current_theme == ThemeName.COLORFUL:
            return "✨ Add new TODO ✨"
        return "Add new TODO:"
    
    def on_mount(self) -> None:
        """Load todos when the app starts."""
        self.title = self._get_title()
        self.load_todos()
        self._apply_layout_density()
        self._apply_theme()
        self._apply_font_size()
    
    def _get_title(self) -> str:
        """Get the app title based on current theme."""
        if self.current_theme == ThemeName.COLORFUL:
            return "✨ TODO TUI App ✨"
        return "TODO TUI App"
    
    def _apply_theme(self) -> None:
        """Apply the current theme's CSS immediately."""
        theme = self.all_themes.get(self.current_theme)
        if theme:
            # Combine base CSS (font sizes) with theme CSS
            combined_css = get_base_css() + "\n" + theme.css
            # Parse the CSS to apply it immediately
            self.stylesheet.parse(combined_css)
            self.refresh(layout=True)
    
    def _apply_layout_density(self) -> None:
        """Apply the current layout density settings."""
        # Get padding and margin values
        padding = get_layout_padding(self.layout_density)
        margin = get_layout_margin(self.layout_density)
        
        # Update list styles
        list_view = self.query_one("#todo-list", ListView)
        for item in list_view.children:
            if isinstance(item, TodoListItem):
                item.styles.padding = (0, padding)
        
        # Update input container
        input_container = self.query_one("#input-container")
        input_container.styles.padding = padding
    
    def _apply_font_size(self) -> None:
        """Apply the current font size by adding CSS class to screen."""
        # Remove all font size classes first
        for size in FontSize:
            self.remove_class(get_font_size_class(size))
        
        # Add current font size class
        self.add_class(get_font_size_class(self.font_size))
    
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
        
        # Reapply layout density
        self._apply_layout_density()
    
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
    
    def action_cycle_theme(self) -> None:
        """Cycle through available themes."""
        theme_names = list(self.all_themes.keys())
        current_index = theme_names.index(self.current_theme) if self.current_theme in theme_names else 0
        next_index = (current_index + 1) % len(theme_names)
        self.current_theme = theme_names[next_index]
        
        # Save preference
        self.preferences.set_theme(self.current_theme)
        
        # Apply new theme immediately
        self._apply_theme()
        
        # Update title if needed
        self.title = self._get_title()
        
        # Update input label
        input_container = self.query_one("#input-container")
        static = input_container.query_one(Static)
        static.update(self._get_input_label())
        
        # Display notification
        theme = self.all_themes[self.current_theme]
        self.notify(f"Theme: {theme.display_name}", timeout=2)
    
    def action_cycle_layout(self) -> None:
        """Cycle through layout density options."""
        densities = [LayoutDensity.COMPACT, LayoutDensity.COMFORTABLE, LayoutDensity.SPACIOUS]
        current_index = densities.index(self.layout_density)
        next_index = (current_index + 1) % len(densities)
        self.layout_density = densities[next_index]
        
        # Save preference
        self.preferences.set_layout_density(self.layout_density.value)
        
        # Apply new layout
        self._apply_layout_density()
        
        # Display name
        display_names = {
            LayoutDensity.COMPACT: "Compact",
            LayoutDensity.COMFORTABLE: "Comfortable",
            LayoutDensity.SPACIOUS: "Spacious",
        }
        self.notify(f"Layout: {display_names[self.layout_density]}", timeout=2)
    
    def action_cycle_font_size(self) -> None:
        """Cycle through font size options."""
        sizes = [FontSize.SMALL, FontSize.MEDIUM, FontSize.LARGE]
        current_index = sizes.index(self.font_size)
        next_index = (current_index + 1) % len(sizes)
        self.font_size = sizes[next_index]
        
        # Save preference
        self.preferences.set_font_size(self.font_size.value)
        
        # Apply new font size immediately
        self._apply_font_size()
        
        # Display name
        display_names = {
            FontSize.SMALL: "Small",
            FontSize.MEDIUM: "Medium",
            FontSize.LARGE: "Large",
        }
        self.notify(f"Font Size: {display_names[self.font_size]}", timeout=2)


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
