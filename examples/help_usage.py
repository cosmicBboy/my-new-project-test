"""Example demonstrating the keyboard shortcuts help and customization features.

This example shows how the comprehensive help system works in the TODO TUI app,
including the help screen, customizable bindings, tutorial, and cheat sheet export.

Key features demonstrated:
- Opening the help screen with '?'
- Searching for specific shortcuts
- Organized categories of shortcuts
- Customizing key bindings with 'c'
- Exporting shortcuts cheat sheet with Ctrl+E
- Interactive tutorial with Ctrl+T
- Closing screens with ESC or q

To run this example:
    python examples/help_usage.py

Then try the following:
1. Press '?' to see the help screen
   - Try searching for shortcuts
   - Click "Export Cheat Sheet" button
2. Press 'c' to customize key bindings
   - Try changing a binding
   - Click "Reset to Defaults" to restore
3. Press Ctrl+T to see the tutorial
4. Press Ctrl+E to export shortcuts directly
"""

from todo_tui.app import TodoApp
from todo_tui.models import TodoItem


def main():
    """Run the TODO app with sample data to demonstrate help features."""
    app = TodoApp()
    
    # Add sample todos to make the app more interesting
    sample_todos = [
        "Press '?' to see all keyboard shortcuts",
        "Press 'c' to customize your key bindings",
        "Press Ctrl+E to export a shortcuts cheat sheet",
        "Press Ctrl+T to see the interactive tutorial",
        "Use search in help screen to find commands",
        "Navigate with arrow keys",
        "Toggle completion with Space",
        "Postpone tasks with 'p' until tomorrow",
        "Delete tasks with 'd'",
        "All your changes are saved automatically!",
    ]
    
    for title in sample_todos:
        todo = TodoItem(title=title)
        app.storage.add(todo)
    
    # Display welcome message
    print("🎯 TODO TUI App - Complete Help System Demo")
    print("=" * 70)
    print("\nThis demo showcases the comprehensive keyboard shortcuts system:")
    print()
    print("📚 Help & Reference:")
    print("  • Press '?' - Open keyboard shortcuts reference")
    print("    - Search shortcuts in real-time")
    print("    - Export as print-friendly cheat sheet")
    print()
    print("⚙️  Customization:")
    print("  • Press 'c' - Customize key bindings")
    print("    - Change any shortcut to your preference")
    print("    - Press Enter to save a binding")
    print("    - Reset to defaults anytime")
    print()
    print("📄 Export:")
    print("  • Press Ctrl+E - Export shortcuts to ~/todo-tui-shortcuts.txt")
    print("    - Plain text format")
    print("    - Ready to print")
    print()
    print("🎓 Tutorial:")
    print("  • Press Ctrl+T - Show interactive tutorial")
    print("    - Step-by-step guide for new users")
    print("    - Access anytime you need a refresher")
    print()
    print("💡 Tips:")
    print("  • All shortcuts show your current bindings")
    print("  • Customizations are saved automatically")
    print("  • Press ESC to close any modal screen")
    print("  • Press 'q' on main screen to quit")
    print()
    print("=" * 70)
    print("\n🚀 Starting app with sample TODOs...\n")
    
    app.run()


if __name__ == "__main__":
    main()
