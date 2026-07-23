"""Key binding customization overlay."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static
from textual.binding import Binding
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import Config


class KeybindingsScreen(ModalScreen):
    """Modal screen for customizing key bindings."""
    
    CSS = """
    KeybindingsScreen {
        align: center middle;
    }
    
    #keybindings-dialog {
        width: 70;
        height: auto;
        max-height: 90%;
        border: heavy #8338ec;
        background: #0f1425;
        padding: 2;
    }
    
    #keybindings-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: #ff006e;
        background: #1a1f3a;
        padding: 1;
        margin-bottom: 1;
    }
    
    #keybindings-scroll {
        width: 100%;
        height: 1fr;
        border: round #3a86ff;
        background: #0f1425;
        margin-bottom: 1;
    }
    
    #keybindings-container {
        width: 100%;
        height: auto;
        padding: 1;
    }
    
    .binding-row {
        width: 100%;
        height: auto;
        margin-bottom: 1;
        padding: 1;
        background: #1a1f3a;
        border: solid #3a86ff;
    }
    
    .binding-action {
        color: #ffbe0b;
        text-style: bold;
        margin-bottom: 1;
    }
    
    .binding-input-container {
        layout: horizontal;
        width: 100%;
        height: auto;
    }
    
    .binding-label {
        width: 15;
        color: #06ffa5;
        content-align: left middle;
    }
    
    .binding-input {
        width: 1fr;
        border: solid #06ffa5;
        background: #240046;
        color: #ff006e;
    }
    
    .binding-input:focus {
        border: heavy #ff006e;
    }
    
    #instructions {
        width: 100%;
        color: #8338ec;
        text-style: italic;
        padding: 1;
        margin-bottom: 1;
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
        min-width: 15;
    }
    
    #reset-button {
        background: #7209b7;
        color: #ffffff;
        border: solid #8338ec;
    }
    
    #reset-button:hover {
        background: #8338ec;
    }
    
    #cancel-button {
        background: #3a86ff;
        color: #ffffff;
        border: solid #8338ec;
    }
    
    #cancel-button:hover {
        background: #8338ec;
    }
    
    #save-button {
        background: #8338ec;
        color: #ffffff;
        border: heavy #ff006e;
    }
    
    #save-button:hover {
        background: #ff006e;
        border: heavy #8338ec;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]
    
    ACTIONS = {
        "quit": "Quit Application",
        "toggle": "Toggle TODO Completion",
        "delete": "Delete TODO",
        "postpone": "Postpone TODO",
        "help": "Show Help Overlay",
        "export": "Export Data",
        "import": "Import Data",
        "tutorial": "Show Tutorial",
    }
    
    def __init__(self, config: "Config"):
        """Initialize the keybindings screen.
        
        Args:
            config: The application configuration
        """
        super().__init__()
        self.config = config
        self.inputs = {}
    
    def compose(self) -> ComposeResult:
        """Compose the keybindings screen."""
        with Container(id="keybindings-dialog"):
            yield Static("⌨️  Customize Key Bindings  ⌨️", id="keybindings-title")
            
            yield Label(
                "Enter key names like: 'q', 'space', 'ctrl+s', 'question_mark', etc.",
                id="instructions"
            )
            
            with VerticalScroll(id="keybindings-scroll"):
                with Vertical(id="keybindings-container"):
                    for action, description in self.ACTIONS.items():
                        current_key = self.config.get_key(action)
                        
                        with Vertical(classes="binding-row"):
                            yield Label(description, classes="binding-action")
                            with Container(classes="binding-input-container"):
                                yield Label("Key:", classes="binding-label")
                                input_widget = Input(
                                    value=current_key,
                                    placeholder="Enter key...",
                                    id=f"input-{action}",
                                    classes="binding-input"
                                )
                                self.inputs[action] = input_widget
                                yield input_widget
            
            with Container(id="button-container"):
                yield Button("Reset to Defaults", id="reset-button", variant="default")
                yield Button("Cancel", id="cancel-button", variant="default")
                yield Button("Save Changes", id="save-button", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "save-button":
            self._save_changes()
            self.dismiss(True)
        elif event.button.id == "cancel-button":
            self.dismiss(False)
        elif event.button.id == "reset-button":
            self._reset_to_defaults()
    
    def _save_changes(self) -> None:
        """Save the modified key bindings."""
        for action, input_widget in self.inputs.items():
            key = input_widget.value.strip()
            if key:
                self.config.set_key(action, key)
    
    def _reset_to_defaults(self) -> None:
        """Reset all key bindings to defaults."""
        self.config.reset_keybindings()
        # Update input fields
        for action, input_widget in self.inputs.items():
            input_widget.value = self.config.get_key(action)
    
    def action_cancel(self) -> None:
        """Cancel and close the dialog."""
        self.dismiss(False)
