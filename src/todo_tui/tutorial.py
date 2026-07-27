"""Tutorial screen for new users."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from textual.binding import Binding


class TutorialScreen(ModalScreen):
    """Interactive tutorial for new users."""
    
    CSS = """
    TutorialScreen {
        align: center middle;
    }
    
    #tutorial-container {
        width: 90;
        height: auto;
        max-height: 95%;
        background: $surface;
        border: heavy $primary;
        padding: 1 2;
    }
    
    #tutorial-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 1;
        text-style: bold;
    }
    
    #tutorial-content {
        width: 100%;
        height: auto;
        max-height: 35;
        border: round $primary;
        padding: 1 2;
        margin: 1 0;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0;
    }
    
    Button {
        margin: 0 1;
    }
    
    .tutorial-section {
        width: 100%;
        text-style: bold underline;
        color: $accent;
        padding: 1 0;
    }
    
    .tutorial-step {
        width: 100%;
        padding: 0 2 1 2;
    }
    
    .tutorial-tip {
        width: 100%;
        padding: 0 2 1 2;
        color: $warning;
        text-style: italic;
    }
    """
    
    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=False),
        Binding("enter", "dismiss", "Close", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the tutorial screen."""
        with Container(id="tutorial-container"):
            yield Label("🎓 Welcome to TODO TUI! 🎓", id="tutorial-title")
            
            with VerticalScroll(id="tutorial-content"):
                yield from self._render_tutorial_content()
            
            with Container(id="button-container"):
                yield Button("Got it! Let's start (Enter)", variant="primary", id="start-btn")
    
    def _render_tutorial_content(self) -> list[Static]:
        """Render the tutorial content.
        
        Returns:
            List of widgets for the tutorial
        """
        widgets = []
        
        # Introduction
        widgets.append(Label("Getting Started", classes="tutorial-section"))
        widgets.append(Label(
            "TODO TUI is a keyboard-driven task manager. Here's what you need to know:",
            classes="tutorial-step"
        ))
        
        # Basic usage
        widgets.append(Label("📝 Adding Tasks", classes="tutorial-section"))
        widgets.append(Label(
            "• Press Tab to focus the input field at the bottom",
            classes="tutorial-step"
        ))
        widgets.append(Label(
            "• Type your task and press Enter to add it",
            classes="tutorial-step"
        ))
        widgets.append(Label(
            "• Press Tab again to return to the task list",
            classes="tutorial-step"
        ))
        
        # Task management
        widgets.append(Label("✓ Managing Tasks", classes="tutorial-section"))
        widgets.append(Label(
            "• Use ↑/↓ (or j/k) to navigate through your tasks",
            classes="tutorial-step"
        ))
        widgets.append(Label(
            "• Press Space to mark a task as complete/incomplete",
            classes="tutorial-step"
        ))
        widgets.append(Label(
            "• Press d to delete the selected task",
            classes="tutorial-step"
        ))
        widgets.append(Label(
            "• Press p to postpone a task until tomorrow",
            classes="tutorial-step"
        ))
        
        # Help system
        widgets.append(Label("❓ Getting Help", classes="tutorial-section"))
        widgets.append(Label(
            "• Press ? to open the keyboard shortcuts reference",
            classes="tutorial-step"
        ))
        widgets.append(Label(
            "• In the help dialog, press / to search for shortcuts",
            classes="tutorial-step"
        ))
        widgets.append(Label(
            "• Press Ctrl+E in help to export shortcuts to a file",
            classes="tutorial-step"
        ))
        
        # Tips
        widgets.append(Label("💡 Pro Tips", classes="tutorial-section"))
        widgets.append(Label(
            "🔸 All your tasks are automatically saved",
            classes="tutorial-tip"
        ))
        widgets.append(Label(
            "🔸 You can customize key bindings in the settings (coming soon!)",
            classes="tutorial-tip"
        ))
        widgets.append(Label(
            "🔸 Postponed tasks remain visible with a special indicator",
            classes="tutorial-tip"
        ))
        widgets.append(Label(
            "🔸 Press q anytime to quit the application",
            classes="tutorial-tip"
        ))
        
        # Final message
        widgets.append(Label("", classes="tutorial-step"))
        widgets.append(Label(
            "Ready to get organized? Press Enter or click the button below to start!",
            classes="tutorial-section"
        ))
        
        return widgets
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "start-btn":
            self.dismiss()
    
    def action_dismiss(self) -> None:
        """Close the tutorial screen."""
        self.dismiss()
