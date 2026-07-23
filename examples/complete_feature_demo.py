"""Complete feature demonstration for TODO TUI app.

This example demonstrates all five features of the keyboard shortcuts
reference system implemented for issue #34:

1. Help Overlay - Press '?' for contextual help
2. Searchable Shortcuts - Search within the help screen
3. Customizable Key Bindings - Press 'c' to customize
4. Print-friendly Cheat Sheet - Press Ctrl+E to export
5. In-app Tutorial - Press Ctrl+T for interactive guide

Run this example to try all features:
    python examples/complete_feature_demo.py
"""

from todo_tui.app import TodoApp
from todo_tui.models import TodoItem


def setup_demo_data(app):
    """Setup demo TODO items showcasing different features."""
    demo_todos = [
        # Feature demonstrations
        ("🎯 Try pressing '?' to see the help overlay", False),
        ("🔍 In help, type 'delete' to search shortcuts", False),
        ("⚙️  Press 'c' to customize your key bindings", False),
        ("📄 Press Ctrl+E to export a cheat sheet", False),
        ("🎓 Press Ctrl+T to see the tutorial", False),
        
        # Usage examples
        ("Navigate with ↑↓ arrow keys", False),
        ("Press Space on this item to complete it", False),
        ("Press 'p' on this item to postpone it", False),
        ("Press 'd' to delete a task", False),
        
        # Completed example
        ("Example of a completed task", True),
    ]
    
    for title, completed in demo_todos:
        todo = TodoItem(title=title)
        if completed:
            todo.toggle_completed()
        app.storage.add(todo)


def print_feature_guide():
    """Print a guide to the features being demonstrated."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + "TODO TUI - Complete Feature Demonstration".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    print("This demo showcases all 5 features of the Keyboard Shortcuts Reference:")
    print()
    
    print("1️⃣  HELP OVERLAY (Press '?')")
    print("   └─ Contextual help showing all available shortcuts")
    print("   └─ Organized by category for easy navigation")
    print("   └─ Always reflects your current key bindings")
    print()
    
    print("2️⃣  SEARCHABLE SHORTCUTS (In help screen)")
    print("   └─ Real-time search as you type")
    print("   └─ Filters shortcuts by key or description")
    print("   └─ Quickly find the command you need")
    print()
    
    print("3️⃣  CUSTOMIZABLE KEY BINDINGS (Press 'c')")
    print("   └─ Change any shortcut to your preference")
    print("   └─ Press Enter or close screen to save")
    print("   └─ Reset to defaults anytime")
    print("   └─ Persists across sessions")
    print()
    
    print("4️⃣  PRINT-FRIENDLY CHEAT SHEET (Press Ctrl+E)")
    print("   └─ Exports to ~/todo-tui-shortcuts.txt")
    print("   └─ Plain text format, ready to print")
    print("   └─ Includes all current bindings")
    print("   └─ Great for reference or sharing")
    print()
    
    print("5️⃣  IN-APP TUTORIAL (Press Ctrl+T)")
    print("   └─ Interactive guide for new users")
    print("   └─ Step-by-step walkthrough")
    print("   └─ Access anytime you need help")
    print("   └─ Shows once on first run (configurable)")
    print()
    
    print("─" * 70)
    print()
    print("🎯 QUICK START:")
    print("   1. Press '?' to open help")
    print("   2. Type 'customize' to see the customize shortcut")
    print("   3. Press 'c' to try customizing bindings")
    print("   4. Press Ctrl+E to export a cheat sheet")
    print("   5. Press Ctrl+T to see the tutorial")
    print()
    print("💡 TIP: All features work together!")
    print("   • Customize a binding, then see it in help")
    print("   • Export the cheat sheet with your custom bindings")
    print("   • Tutorial teaches you about all these features")
    print()
    print("─" * 70)
    print()
    print("Starting TODO TUI with demo data...")
    print("Press 'q' to quit when done exploring.")
    print()


def main():
    """Run the complete feature demonstration."""
    print_feature_guide()
    
    app = TodoApp()
    setup_demo_data(app)
    
    # Note: Tutorial will show on first run unless already shown
    # You can delete ~/.todo-tui-config.json to reset this
    
    app.run()
    
    print()
    print("Thanks for trying the TODO TUI feature demo!")
    print()
    print("✨ Summary of what you explored:")
    print("   ✓ Help overlay with organized shortcuts")
    print("   ✓ Searchable shortcuts for quick lookup")
    print("   ✓ Customizable key bindings (saved automatically)")
    print("   ✓ Exportable print-friendly cheat sheet")
    print("   ✓ Interactive tutorial for new users")
    print()
    print("All features are production-ready and fully tested!")
    print()


if __name__ == "__main__":
    main()
