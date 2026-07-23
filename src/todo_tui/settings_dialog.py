"""Settings dialog for customizing key bindings."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static, Input
from textual.binding import Binding


class BindingEditor(Static):
    """A single key binding editor row."""
    
    def __init__(self, action: str, key: str, description: str) -> None:
        """Initialize the binding editor.
        
        Args:
            action: The action name
            key: Current key binding
            description: Description of the action
        """
        super().__init__()
        self.action = action
        self.key = key
        self.description = description
    
    def compose(self) -> ComposeResult:
        """Compose the binding editor."""
        with Horizontal():
            yield Label(f"{self.description}:", classes="binding-label")
            yield Input(value=self.key, placeholder="Enter key...", 
                       id=f"binding-{self.action}", classes="binding-input")


class SettingsDialog(ModalScreen):
    """Modal dialog for customizing settings."""
    
    CSS = """
    SettingsDialog {
        align: center middle;
    }
    
    #settings-container {
        width: 80;
        height: auto;
        max-height: 90%;
        background: $surface;
        border: heavy $primary;
        padding: 1 2;
    }
    
    #settings-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 1;
    }
    
    #settings-content {
        width: 100%;
        height: auto;
        max-height: 25;
        border: round $primary;
        padding: 1;
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
    
    .section-label {
        width: 100%;
        text-style: bold underline;
        color: $accent;
        padding: 1 0;
    }
    
    .binding-label {
        width: 30;
        padding: 0 1;
    }
    
    .binding-input {
        width: 1fr;
    }
    
    Horizontal {
        width: 100%;
        height: auto;
        padding: 0 0 1 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]
    
    ACTION_DESCRIPTIONS = {
        "quit": "Quit application",
        "help": "Show help dialog",
        "toggle": "Toggle task completion",
        "delete": "Delete selected task",
        "postpone": "Postpone task",
        "focus_next": "Focus next element",
        "focus_previous": "Focus previous element",
    }
    
    def __init__(self, keybindings_manager) -> None:
        """Initialize the settings dialog.
        
        Args:
            keybindings_manager: The KeyBindingsManager instance
        """
        super().__init__()
        self.keybindings_manager = keybindings_manager
    
    def compose(self) -> ComposeResult:
        """Compose the settings dialog."""
        with Container(id="settings-container"):
            yield Label("⚙️  Settings - Key Bindings  ⚙️", id="settings-title")
            
            with VerticalScroll(id="settings-content"):
                yield Label("Customize Keyboard Shortcuts", classes="section-label")
                yield Label("Enter the key you want to use for each action:", classes="binding-label")
                yield Label("", classes="binding-label")  # Spacer
                
                bindings = self.keybindings_manager.get_all_bindings()
                for action, key in sorted(bindings.items()):
                    description = self.ACTION_DESCRIPTIONS.get(action, action.replace("_", " ").title())
                    yield BindingEditor(action, key, description)
            
            with Container(id="button-container"):
                yield Button("Save Changes", variant="primary", id="save-btn")
                yield Button("Reset to Defaults", variant="warning", id="reset-btn")
                yield Button("Cancel (Esc)", variant="default", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses.
        
        Args:
            event: The button pressed event
        """
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "save-btn":
            self._save_bindings()
        elif event.button.id == "reset-btn":
            self._reset_bindings()
    
    def _save_bindings(self) -> None:
        """Save the customized key bindings."""
        try:
            # Collect all binding inputs
            for action in self.keybindings_manager.get_all_bindings().keys():
                input_id = f"binding-{action}"
                try:
                    input_widget = self.query_one(f"#{input_id}", Input)
                    new_key = input_widget.value.strip()
                    if new_key:
                        self.keybindings_manager.set_binding(action, new_key)
                except Exception:
                    continue  # Skip if input not found
            
            self.app.notify("Key bindings saved successfully!", title="Settings Saved", timeout=3)
            self.dismiss(True)
        except Exception as e:
            self.app.notify(
                f"Failed to save key bindings: {e}",
                severity="error",
                title="Save Failed"
            )
    
    def _reset_bindings(self) -> None:
        """Reset key bindings to defaults."""
        try:
            self.keybindings_manager.reset_to_defaults()
            
            # Update input fields with default values
            for action, key in self.keybindings_manager.get_all_bindings().items():
                input_id = f"binding-{action}"
                try:
                    input_widget = self.query_one(f"#{input_id}", Input)
                    input_widget.value = key
                except Exception:
                    continue
            
            self.app.notify("Key bindings reset to defaults", title="Reset Complete", timeout=3)
        except Exception as e:
            self.app.notify(
                f"Failed to reset key bindings: {e}",
                severity="error",
                title="Reset Failed"
            )
    
    def action_cancel(self) -> None:
        """Cancel and close the dialog."""
        self.dismiss(None)
