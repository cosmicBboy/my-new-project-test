#!/usr/bin/env python3
"""Demonstration of customizable key bindings feature.

This script demonstrates how to customize keyboard shortcuts in the TODO TUI app,
including saving and loading custom bindings, resetting to defaults, and viewing
the effects in the help system.
"""

from pathlib import Path
from todo_tui.keybindings import KeyBindingsManager
from todo_tui.help_dialog import HelpDialog


def demo_default_bindings():
    """Demonstrate the default key bindings."""
    print("=== Default Key Bindings ===\n")
    
    manager = KeyBindingsManager()
    bindings = manager.get_all_bindings()
    
    print("Out of the box, TODO TUI uses these keyboard shortcuts:\n")
    
    action_descriptions = {
        "quit": "Quit the application",
        "help": "Show help dialog",
        "toggle": "Toggle task completion",
        "delete": "Delete selected task",
        "postpone": "Postpone task until tomorrow",
        "focus_next": "Focus next element (Tab)",
        "focus_previous": "Focus previous element (Shift+Tab)",
    }
    
    for action, key in sorted(bindings.items()):
        description = action_descriptions.get(action, action.replace("_", " ").title())
        print(f"   {action:20} → {key:20} ({description})")
    
    print()


def demo_customizing_bindings():
    """Demonstrate customizing key bindings."""
    print("=== Customizing Key Bindings ===\n")
    
    # Create a temporary manager for demo
    temp_path = Path.home() / ".demo-keybindings.json"
    manager = KeyBindingsManager(temp_path)
    
    print("You can customize any key binding to suit your preferences:\n")
    
    # Example 1: Change quit to 'x'
    print("1. Change 'quit' from 'q' to 'x':")
    print(f"   Before: quit = {manager.get_binding('quit')}")
    manager.set_binding("quit", "x")
    print(f"   After:  quit = {manager.get_binding('quit')}")
    print()
    
    # Example 2: Change toggle to 't'
    print("2. Change 'toggle' from 'space' to 't':")
    print(f"   Before: toggle = {manager.get_binding('toggle')}")
    manager.set_binding("toggle", "t")
    print(f"   After:  toggle = {manager.get_binding('toggle')}")
    print()
    
    # Example 3: Use Vim-style bindings
    print("3. Set up Vim-style navigation:")
    manager.set_binding("delete", "x")  # Vim delete
    print(f"   delete = {manager.get_binding('delete')}")
    print()
    
    # Example 4: Use Ctrl modifiers
    print("4. Use modifier keys:")
    manager.set_binding("quit", "ctrl+q")
    print(f"   quit = {manager.get_binding('quit')}")
    print()
    
    print("All changes are automatically saved to:")
    print(f"   {temp_path}")
    print()
    
    # Clean up demo file
    if temp_path.exists():
        temp_path.unlink()


def demo_persistence():
    """Demonstrate that bindings persist across sessions."""
    print("=== Persistence Across Sessions ===\n")
    
    temp_path = Path.home() / ".demo-keybindings.json"
    
    print("Key bindings are automatically saved and persist across app restarts:\n")
    
    # Session 1: Set custom bindings
    print("Session 1 - Setting custom bindings:")
    manager1 = KeyBindingsManager(temp_path)
    manager1.set_binding("quit", "x")
    manager1.set_binding("toggle", "t")
    print(f"   Set quit = x")
    print(f"   Set toggle = t")
    print(f"   Saved to {temp_path}")
    print()
    
    # Session 2: Load bindings
    print("Session 2 - Loading bindings (simulating app restart):")
    manager2 = KeyBindingsManager(temp_path)
    print(f"   quit = {manager2.get_binding('quit')} (restored!)")
    print(f"   toggle = {manager2.get_binding('toggle')} (restored!)")
    print()
    
    print("Your customizations are preserved between app sessions.")
    print()
    
    # Clean up
    if temp_path.exists():
        temp_path.unlink()


def demo_reset_to_defaults():
    """Demonstrate resetting bindings to defaults."""
    print("=== Resetting to Defaults ===\n")
    
    temp_path = Path.home() / ".demo-keybindings.json"
    manager = KeyBindingsManager(temp_path)
    
    print("If you want to undo your customizations:\n")
    
    # Customize some bindings
    print("1. Set some custom bindings:")
    manager.set_binding("quit", "x")
    manager.set_binding("toggle", "t")
    manager.set_binding("delete", "r")
    print(f"   quit = {manager.get_binding('quit')}")
    print(f"   toggle = {manager.get_binding('toggle')}")
    print(f"   delete = {manager.get_binding('delete')}")
    print()
    
    # Reset to defaults
    print("2. Reset to defaults:")
    manager.reset_to_defaults()
    print(f"   quit = {manager.get_binding('quit')} (back to default)")
    print(f"   toggle = {manager.get_binding('toggle')} (back to default)")
    print(f"   delete = {manager.get_binding('delete')} (back to default)")
    print()
    
    # Clean up
    if temp_path.exists():
        temp_path.unlink()


def demo_help_system_integration():
    """Demonstrate how custom bindings appear in help system."""
    print("=== Help System Integration ===\n")
    
    temp_path = Path.home() / ".demo-keybindings.json"
    manager = KeyBindingsManager(temp_path)
    
    print("The help system automatically reflects your custom bindings:\n")
    
    # Set custom bindings
    print("1. Customize some bindings:")
    manager.set_binding("quit", "x")
    manager.set_binding("toggle", "t")
    print(f"   quit = x")
    print(f"   toggle = t")
    print()
    
    # Create help dialog with custom bindings
    print("2. Help dialog shows your custom bindings:")
    help_dialog = HelpDialog(manager)
    
    # Show shortcuts from help
    print("   Help & Info shortcuts:")
    for category, shortcuts in help_dialog.shortcuts.items():
        if "Help" in category or "Info" in category:
            for key, action, description in shortcuts:
                if "quit" in action.lower():
                    print(f"      {key:15} → {description}")
    
    print()
    print("   Task Management shortcuts:")
    for category, shortcuts in help_dialog.shortcuts.items():
        if "Task" in category:
            for key, action, description in shortcuts:
                if "toggle" in action.lower():
                    print(f"      {key:15} → {description}")
    
    print()
    print("When you export shortcuts or search in help, your custom")
    print("bindings are shown everywhere!")
    print()
    
    # Clean up
    if temp_path.exists():
        temp_path.unlink()


def demo_common_configurations():
    """Show some common key binding configurations."""
    print("=== Common Configurations ===\n")
    
    configs = {
        "Vim-Style": {
            "delete": "x",
            "quit": "q",
            "help": "question_mark",
        },
        "Emacs-Style": {
            "quit": "ctrl+x_ctrl+c",
            "delete": "ctrl+d",
            "help": "ctrl+h",
        },
        "Windows-Style": {
            "quit": "alt+f4",
            "delete": "delete",
            "help": "f1",
        },
        "Minimalist": {
            "quit": "q",
            "toggle": "enter",
            "delete": "backspace",
            "help": "question_mark",
        },
    }
    
    print("Popular key binding configurations:\n")
    
    for config_name, bindings in configs.items():
        print(f"📋 {config_name}:")
        for action, key in bindings.items():
            print(f"   {action:20} = {key}")
        print()


def demo_programmatic_setup():
    """Demonstrate programmatic key binding setup."""
    print("=== Programmatic Setup ===\n")
    
    print("You can set up custom bindings in code:\n")
    
    print("```python")
    print("from todo_tui.keybindings import KeyBindingsManager")
    print()
    print("# Create manager")
    print("manager = KeyBindingsManager()")
    print()
    print("# Configure Vim-style bindings")
    print("manager.set_binding('delete', 'x')")
    print("manager.set_binding('quit', 'q')")
    print("manager.set_binding('toggle', 'enter')")
    print()
    print("# Changes are saved automatically")
    print("```")
    print()


def demo_validation_tips():
    """Provide tips for choosing good key bindings."""
    print("=== Tips for Choosing Key Bindings ===\n")
    
    tips = [
        ("Use Mnemonic Keys", 
         "Choose keys that relate to the action (d for delete, q for quit)"),
        
        ("Avoid Conflicts", 
         "Don't override important system shortcuts like Ctrl+C"),
        
        ("Consider Your Workflow", 
         "Put frequently-used actions on easy-to-reach keys"),
        
        ("Test Before Committing", 
         "Try your bindings for a day before making them permanent"),
        
        ("Document Your Setup", 
         "Export your shortcuts to Markdown for reference"),
        
        ("Start Small", 
         "Customize 1-2 bindings at a time, not everything at once"),
    ]
    
    for tip, explanation in tips:
        print(f"💡 {tip}")
        print(f"   {explanation}")
        print()


def main():
    """Run all key bindings demonstrations."""
    print("=" * 70)
    print("TODO TUI App - Customizable Key Bindings Demonstration")
    print("=" * 70)
    print()
    
    demo_default_bindings()
    demo_customizing_bindings()
    demo_persistence()
    demo_reset_to_defaults()
    demo_help_system_integration()
    demo_common_configurations()
    demo_programmatic_setup()
    demo_validation_tips()
    
    print("=" * 70)
    print("Key Bindings Demo Complete!")
    print("=" * 70)
    print()
    print("To customize your own bindings:")
    print("  1. Run the app: uv run todo-tui")
    print("  2. Bindings are stored in: ~/.todo-tui-keybindings.json")
    print("  3. Or use the KeyBindingsManager API (see examples above)")
    print()
    print("Your customizations will persist across all app sessions!")
    print()


if __name__ == "__main__":
    main()
