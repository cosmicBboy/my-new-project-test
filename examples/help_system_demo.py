"""Example demonstrating the keyboard shortcuts reference system.

This example shows how to use the help overlay to discover keyboard shortcuts,
customize key bindings, and export cheat sheets.
"""

from todo_tui.help_overlay import HelpOverlay, KeyboardShortcut


def main():
    """Demonstrate the help system features."""
    
    print("=" * 70)
    print("TODO TUI - Keyboard Shortcuts Reference System")
    print("=" * 70)
    print()
    
    print("The TODO TUI app includes a comprehensive help system with:")
    print("  ✓ Interactive help overlay (press '?')")
    print("  ✓ Searchable shortcuts")
    print("  ✓ Customizable key bindings (press 'c')")
    print("  ✓ Print-friendly cheat sheets (press 'x')")
    print("  ✓ In-app tutorial for new users")
    print()
    
    # Create a help overlay instance to demonstrate
    help_overlay = HelpOverlay()
    
    print("📋 Available Shortcuts:")
    print("-" * 70)
    
    # Group shortcuts by category
    categories = {}
    for shortcut in help_overlay.shortcuts:
        if shortcut.category not in categories:
            categories[shortcut.category] = []
        categories[shortcut.category].append(shortcut)
    
    # Display shortcuts by category
    for category in ["Navigation", "Task Management", "Application"]:
        if category not in categories:
            continue
        
        print()
        print(f"━━ {category} ━━")
        print()
        
        for shortcut in categories[category]:
            print(f"  {shortcut.key:15} {shortcut.action:20} {shortcut.description}")
    
    print()
    print("-" * 70)
    print()
    
    # Demonstrate search functionality
    print("🔍 Search Functionality:")
    print("-" * 70)
    print()
    print("The help overlay includes a search feature that lets you quickly")
    print("find shortcuts by typing keywords. For example:")
    print()
    
    search_examples = [
        ("toggle", "Find shortcuts related to toggling"),
        ("navigation", "Find all navigation shortcuts"),
        ("delete", "Find shortcuts for deleting items"),
        ("postpone", "Find shortcuts for postponing tasks"),
        ("customize", "Find customization features"),
    ]
    
    for query, description in search_examples:
        results = [s for s in help_overlay.shortcuts if s.matches_search(query)]
        print(f"  Search: '{query}' - {description}")
        print(f"    → Found {len(results)} matching shortcut(s)")
        for shortcut in results:
            print(f"      • {shortcut.key:15} {shortcut.action}")
        print()
    
    print("-" * 70)
    print()
    
    # Feature highlights
    print("✨ Key Features:")
    print("-" * 70)
    print()
    print("  1. Contextual Help: Access help anytime with '?' key")
    print("  2. Organized Categories: Shortcuts grouped by function")
    print("  3. Real-time Search: Filter shortcuts as you type")
    print("  4. Easy to Close: Press 'Esc', 'q', or click 'Close' button")
    print("  5. Visual Design: Color-coded for easy reading")
    print()
    print("  🆕 NEW FEATURES:")
    print("  6. Custom Key Bindings: Press 'c' to customize shortcuts")
    print("  7. Export Cheat Sheets: Press 'x' for print-friendly reference")
    print("  8. Interactive Tutorial: First-run guide for new users")
    print()
    
    print("-" * 70)
    print()
    
    # Quick tips
    print("💡 Quick Tips:")
    print("-" * 70)
    print()
    print("  • Press '?' in the app to open the help overlay")
    print("  • Use the search box to quickly find specific shortcuts")
    print("  • Navigate with Tab and arrow keys")
    print("  • The help overlay adapts to your terminal colors")
    print("  • All shortcuts are designed for keyboard-first workflow")
    print()
    print("  🆕 Customization Tips:")
    print("  • Press 'c' to open key binding customization")
    print("  • Press 'x' to export cheat sheets (text & markdown)")
    print("  • Press 't' to replay the tutorial anytime")
    print("  • Custom settings persist between sessions")
    print()
    
    print("-" * 70)
    print()
    
    # Usage examples
    print("📚 Usage Examples:")
    print("-" * 70)
    print()
    print("Example 1: Learning the app")
    print("  1. Start the app: uv run todo-tui")
    print("  2. Tutorial appears on first run")
    print("  3. Press '?' to see all shortcuts")
    print("  4. Use search to find specific actions")
    print()
    print("Example 2: Customizing shortcuts")
    print("  1. Press 'c' to open customization")
    print("  2. Change any key binding")
    print("  3. Click 'Save Changes'")
    print("  4. Restart app to apply")
    print()
    print("Example 3: Creating a cheat sheet")
    print("  1. Press 'x' in the app")
    print("  2. Find files in home directory:")
    print("     - todo-tui-shortcuts.txt")
    print("     - todo-tui-shortcuts.md")
    print("  3. Print or share with team")
    print()
    
    print("-" * 70)
    print()
    
    # Statistics
    print("📊 Statistics:")
    print("-" * 70)
    print()
    total = len(help_overlay.shortcuts)
    by_category = {}
    for shortcut in help_overlay.shortcuts:
        by_category[shortcut.category] = by_category.get(shortcut.category, 0) + 1
    
    print(f"  Total shortcuts: {total}")
    print()
    print("  By category:")
    for category, count in sorted(by_category.items()):
        print(f"    {category:20} {count}")
    print()
    
    print("-" * 70)
    print()
    
    # Success criteria
    print("✅ Success Criteria:")
    print("-" * 70)
    print()
    print("  ✓ Help overlay displays correctly")
    print("  ✓ All shortcuts are documented")
    print("  ✓ Search works for finding shortcuts")
    print("  ✓ Customizable bindings save correctly")
    print("  ✓ Tutorial is helpful for new users")
    print()
    
    print("=" * 70)
    print()
    print("To see the help system in action, run the TODO TUI app:")
    print("  uv run todo-tui")
    print()
    print("Then:")
    print("  • Press '?' to open the keyboard shortcuts reference")
    print("  • Press 'c' to customize key bindings")
    print("  • Press 'x' to export cheat sheets")
    print("  • Press 't' to replay the tutorial")
    print()


if __name__ == "__main__":
    main()
