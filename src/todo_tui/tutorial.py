"""Tutorial overlay for new users."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from textual.binding import Binding


class TutorialScreen(ModalScreen):
    """Interactive tutorial for new users."""
    
    CSS = """
    TutorialScreen {
        align: center middle;
    }
    
    #tutorial-dialog {
        width: 70;
        height: auto;
        max-height: 90%;
        border: heavy #8338ec;
        background: #0f1425;
        padding: 2;
    }
    
    #tutorial-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: #ff006e;
        background: #1a1f3a;
        padding: 1;
        margin-bottom: 1;
    }
    
    #tutorial-content {
        width: 100%;
        height: auto;
        padding: 1 2;
        color: #06ffa5;
    }
    
    .tutorial-step {
        margin-bottom: 2;
    }
    
    .step-title {
        text-style: bold;
        color: #ffbe0b;
        margin-bottom: 1;
    }
    
    .step-content {
        color: #06ffa5;
        margin-left: 2;
    }
    
    .key-highlight {
        background: #240046;
        color: #ff006e;
        text-style: bold;
        padding: 0 1;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1;
        layout: horizontal;
    }
    
    Button {
        margin: 0 1;
        min-width: 20;
    }
    
    #skip-button {
        background: #7209b7;
        color: #ffffff;
        border: solid #8338ec;
    }
    
    #skip-button:hover {
        background: #8338ec;
    }
    
    #start-button {
        background: #8338ec;
        color: #ffffff;
        border: heavy #ff006e;
    }
    
    #start-button:hover {
        background: #ff006e;
        border: heavy #8338ec;
    }
    """
    
    BINDINGS = [
        Binding("escape", "skip", "Skip", show=False),
    ]
    
    def __init__(self):
        """Initialize the tutorial screen."""
        super().__init__()
        self.completed = False
    
    def compose(self) -> ComposeResult:
        """Compose the tutorial screen."""
        with Container(id="tutorial-dialog"):
            yield Static("🎓 Welcome to TODO TUI! 🎓", id="tutorial-title")
            
            with Vertical(id="tutorial-content"):
                yield Label("Let's get you started with a quick tour!", classes="tutorial-step")
                
                with Vertical(classes="tutorial-step"):
                    yield Label("1️⃣  Adding Tasks", classes="step-title")
                    yield Label(
                        "Press [bold #ff006e]Tab[/] to focus the input field\n"
                        "Type your task and press [bold #ff006e]Enter[/] to add it",
                        classes="step-content",
                        markup=True
                    )
                
                with Vertical(classes="tutorial-step"):
                    yield Label("2️⃣  Navigating", classes="step-title")
                    yield Label(
                        "Use [bold #ff006e]↑/↓[/] or [bold #ff006e]j/k[/] to move between tasks\n"
                        "Press [bold #ff006e]Home[/] or [bold #ff006e]End[/] to jump to first/last",
                        classes="step-content",
                        markup=True
                    )
                
                with Vertical(classes="tutorial-step"):
                    yield Label("3️⃣  Managing Tasks", classes="step-title")
                    yield Label(
                        "[bold #ff006e]Space[/] - Toggle completion status\n"
                        "[bold #ff006e]d[/] - Delete a task\n"
                        "[bold #ff006e]p[/] - Postpone until tomorrow",
                        classes="step-content",
                        markup=True
                    )
                
                with Vertical(classes="tutorial-step"):
                    yield Label("4️⃣  Getting Help", classes="step-title")
                    yield Label(
                        "Press [bold #ff006e]?[/] anytime to see all keyboard shortcuts\n"
                        "The help overlay includes a search feature!",
                        classes="step-content",
                        markup=True
                    )
                
                with Vertical(classes="tutorial-step"):
                    yield Label("5️⃣  Customization", classes="step-title")
                    yield Label(
                        "Press [bold #ff006e]c[/] to customize key bindings\n"
                        "Press [bold #ff006e]x[/] to export a shortcuts cheat sheet",
                        classes="step-content",
                        markup=True
                    )
                
                yield Label(
                    "\n💡 Your TODOs are automatically saved!\n"
                    "Press [bold #ff006e]q[/] to quit anytime.",
                    classes="tutorial-step",
                    markup=True
                )
            
            with Container(id="button-container"):
                yield Button("Skip Tutorial", id="skip-button", variant="default")
                yield Button("Start Using App", id="start-button", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "start-button":
            self.completed = True
            self.dismiss(True)
        elif event.button.id == "skip-button":
            self.completed = True
            self.dismiss(False)
    
    def action_skip(self) -> None:
        """Skip the tutorial."""
        self.completed = True
        self.dismiss(False)
