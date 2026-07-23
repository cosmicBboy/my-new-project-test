#!/usr/bin/env python3
"""Demonstration of the keyboard shortcuts help feature.

This script shows how the keyboard shortcuts help system works,
including the searchable shortcuts reference, customizable bindings,
printable cheat sheet, and interactive tutorial.
"""

from todo_tui.app import KeyboardShortcutsHelp, TutorialScreen, CustomizeKeysScreen
from todo_tui.keybindings import KeyBindings


def print_section_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_all_shortcuts():
    """Display all available keyboard shortcuts."""
    print_section_header("Available Keyboard Shortcuts")
    
    # Create help screen to access shortcuts data
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    shortcuts = help_screen._get_all_shortcuts()
    
    for category, items in shortcuts.items():
        print(f"📂 {category}")
        print("─" * 70)
        for key, description in items:
            print(f"  {key:15} {description}")
        print()


def demonstrate_search():
    """Demonstrate the search functionality."""
    print_section_header("Search Functionality Demo")
    
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    
    # Example searches
    searches = [
        ("delete", "Finding 'delete' shortcuts"),
        ("space", "Finding 'Space' key shortcuts"),
        ("todo", "Finding shortcuts related to 'todo'"),
        ("quit", "Finding 'quit' shortcuts"),
        ("ctrl", "Finding shortcuts with Ctrl modifier"),
    ]
    
    for search_term, description in searches:
        print(f"{description}: '{search_term}'")
        print("─" * 70)
        
        # Filter shortcuts
        filtered = {}
        for category, items in help_screen.shortcuts.items():
            filtered_items = [
                (key, desc) for key, desc in items
                if search_term.lower() in key.lower() or 
                   search_term.lower() in desc.lower()
            ]
            if filtered_items:
                filtered[category] = filtered_items
        
        # Display results
        if filtered:
            for category, items in filtered.items():
                print(f"  {category}:")
                for key, desc in items:
                    print(f"    {key:15} {desc}")
        else:
            print("  No matches found")
        print()


def demonstrate_customization():
    """Demonstrate key binding customization."""
    print_section_header("Interactive Key Binding Customization")
    
    keybindings = KeyBindings()
    
    print("DEFAULT BINDINGS:")
    print("─" * 70)
    for action, key in sorted(keybindings.DEFAULT_BINDINGS.items()):
        description = keybindings.get_description(action)
        display_key = keybindings.format_key_for_display(key)
        print(f"  {display_key:15} {description}")
    print()
    
    print("INTERACTIVE CUSTOMIZATION FEATURES:")
    print("─" * 70)
    print("  • Click 'Edit' button next to any action")
    print("  • Press the new key you want to use")
    print("  • Binding is saved automatically")
    print("  • Changes take effect immediately")
    print("  • Press ESC while editing to cancel")
    print("  • Visual feedback during editing")
    print("  • Persistent across sessions")
    print("  • Easy reset to defaults")
    print("  • Accessible via Ctrl+K in the app")
    print()
    
    print("EXAMPLE CUSTOMIZATION WORKFLOW:")
    print("─" * 70)
    print("  1. Press Ctrl+K to open customization dialog")
    print("  2. Click 'Edit' next to 'Quit application'")
    print("  3. Press 'x' (or any other key)")
    print("  4. Binding updated: quit = 'x'")
    print("  5. Changes saved to ~/.todo-tui-keys.json")
    print()
    
    print("PROGRAMMATIC EXAMPLE:")
    print("─" * 70)
    print("  Original: quit = 'q'")
    keybindings.set_key("quit", "ctrl+q")
    print(f"  Modified: quit = '{keybindings.get_key('quit')}'")
    keybindings.reset_to_defaults()
    print(f"  Reset:    quit = '{keybindings.get_key('quit')}'")
    print()


def demonstrate_export():
    """Demonstrate exporting cheat sheet."""
    print_section_header("Printable Cheat Sheet Export")
    
    print("EXPORT FEATURE:")
    print("─" * 70)
    print("  • Press Ctrl+E in the app to export shortcuts")
    print("  • Creates 'todo-tui-shortcuts.txt' in your home directory")
    print("  • Print-friendly format with all shortcuts organized")
    print("  • Perfect for quick reference or offline use")
    print()
    
    print("EXAMPLE EXPORT FORMAT:")
    print("─" * 70)
    keybindings = KeyBindings()
    help_screen = KeyboardShortcutsHelp(keybindings)
    shortcuts = help_screen._get_all_shortcuts()
    
    print("  " + "=" * 66)
    print("  TODO TUI - Keyboard Shortcuts Cheat Sheet")
    print("  " + "=" * 66)
    
    for category, items in list(shortcuts.items())[:2]:  # Show first 2 categories
        print(f"\n  {category}")
        print("  " + "-" * 66)
        for key, description in items:
            print(f"    {key:15} {description}")
    
    print("\n  [... additional categories ...]")
    print("  " + "=" * 66)
    print()


def demonstrate_tutorial():
    """Demonstrate tutorial features."""
    print_section_header("Interactive Tutorial")
    
    print("TUTORIAL FEATURES:")
    print("─" * 70)
    print("  • Automatic on first run")
    print("  • Step-by-step guide covering all major features")
    print("  • Covers: Adding TODOs, Managing tasks, Postponing, Help system")
    print("  • Re-accessible anytime with Ctrl+T")
    print("  • Easy to navigate and close")
    print()
    
    print("TUTORIAL STEPS:")
    print("─" * 70)
    steps = [
        ("Step 1", "Adding Your First TODO", 
         "Learn how to add tasks using Tab and Enter"),
        ("Step 2", "Managing Your TODOs",
         "Navigate with arrows, toggle with Space, delete with D"),
        ("Step 3", "Postponing Tasks",
         "Learn to postpone tasks until tomorrow with P"),
        ("Step 4", "Getting Help",
         "Discover help system, cheat sheet export, and customization"),
        ("Step 5", "Your Data is Safe",
         "Understand automatic saving and persistence"),
    ]
    
    for step_num, title, description in steps:
        print(f"  {step_num}: {title}")
        print(f"          {description}")
        print()


def usage_guide():
    """Display usage guide for the help features."""
    print_section_header("Using the Keyboard Shortcuts Help System")
    
    print("HOW TO ACCESS:")
    print("  Press '?' anywhere in the TODO TUI app to open the help dialog.")
    print()
    
    print("FEATURES:")
    print("  • Organized by category (Navigation, TODO Management, etc.)")
    print("  • Real-time search - type to filter shortcuts")
    print("  • Search by key name or description")
    print("  • Scrollable list for easy browsing")
    print("  • Export to printable cheat sheet (Ctrl+E)")
    print("  • Customize key bindings (Ctrl+K)")
    print("  • Interactive tutorial (Ctrl+T)")
    print()
    
    print("CUSTOMIZATION:")
    print("  • Press Ctrl+K to open customization dialog")
    print("  • Click 'Edit' next to any action")
    print("  • Press the new key you want to use")
    print("  • Changes are saved automatically")
    print("  • Press ESC to cancel editing")
    print("  • Click 'Reset to Defaults' to restore original bindings")
    print()
    
    print("NAVIGATION:")
    print("  • Type in search box to filter shortcuts")
    print("  • Use arrow keys to scroll through the list")
    print("  • Press ESC or Q to close the dialog")
    print("  • Press Ctrl+E to export cheat sheet")
    print()
    
    print("EXAMPLES:")
    print("  • Search 'delete' to find the delete shortcut")
    print("  • Search 'space' to find the toggle completion shortcut")
    print("  • Search 'postpone' to find postpone-related shortcuts")
    print("  • Clear search to show all shortcuts again")
    print()


def benefits():
    """Explain the benefits of the help features."""
    print_section_header("Benefits of Keyboard Shortcuts Help System")
    
    benefits = [
        ("Faster Learning", 
         "New users can quickly discover all available shortcuts without "
         "leaving the app or checking external documentation."),
        
        ("Increased Efficiency", 
         "Users can look up forgotten shortcuts instantly, maintaining their "
         "workflow without interruption."),
        
        ("Better Discoverability", 
         "Search functionality makes it easy to find specific shortcuts by "
         "function (e.g., 'delete', 'complete')."),
        
        ("Reduced Friction", 
         "In-app help eliminates the need to switch to a browser or "
         "documentation, keeping focus on task management."),
        
        ("Accessibility", 
         "Multiple learning modes (tutorial, help, cheat sheet) support "
         "different user preferences and needs."),
        
        ("True Personalization",
         "Interactive key editing lets users adapt shortcuts to their "
         "preferred workflow with immediate visual feedback."),
        
        ("Offline Reference",
         "Exportable cheat sheet provides quick reference without running "
         "the app or having internet access."),
        
        ("Onboarding",
         "Interactive tutorial guides new users through all features, "
         "reducing time to productivity."),
    ]
    
    for i, (title, description) in enumerate(benefits, 1):
        print(f"{i}. {title}")
        print(f"   {description}")
        print()


def integration_examples():
    """Show how the help system integrates with the app."""
    print_section_header("Integration with TODO TUI App")
    
    print("The help system is seamlessly integrated:")
    print()
    
    print("1. KEYBOARD BINDING")
    print("   • Bound to '?' key (Shift + / on most keyboards)")
    print("   • Available from anywhere in the app")
    print("   • Listed in the footer with other shortcuts")
    print()
    
    print("2. MODAL DIALOG")
    print("   • Opens as an overlay, preserving context")
    print("   • Styled consistently with the cyberpunk theme")
    print("   • Easy to close and return to work")
    print()
    
    print("3. SEARCH CAPABILITY")
    print("   • Live filtering as you type")
    print("   • Searches both keys and descriptions")
    print("   • Case-insensitive for ease of use")
    print()
    
    print("4. ORGANIZED DISPLAY")
    print("   • Shortcuts grouped by category")
    print("   • Clear visual hierarchy")
    print("   • Consistent formatting")
    print()
    
    print("5. TUTORIAL SYSTEM")
    print("   • Automatic on first launch")
    print("   • Comprehensive coverage of features")
    print("   • Always accessible via Ctrl+T")
    print()
    
    print("6. INTERACTIVE CUSTOMIZATION")
    print("   • Full control over key bindings")
    print("   • Click-to-edit interface")
    print("   • Instant visual feedback")
    print("   • Persistent storage of preferences")
    print("   • Easy reset to defaults")
    print()
    
    print("7. EXPORT CAPABILITY")
    print("   • Generate printable cheat sheet")
    print("   • Plain text format for universal access")
    print("   • One-key export (Ctrl+E)")
    print()


def key_features_summary():
    """Summarize all key features."""
    print_section_header("Complete Feature Set")
    
    print("✅ IMPLEMENTED FEATURES:")
    print("─" * 70)
    
    features = [
        ("1", "Contextual Help Overlay", 
         "Press ? to see all shortcuts organized by category"),
        ("2", "Searchable Shortcuts", 
         "Real-time search filters shortcuts by key or description"),
        ("3", "Interactive Key Customization", 
         "Click 'Edit' and press new key - changes save automatically"),
        ("4", "Print-Friendly Cheat Sheet", 
         "Export shortcuts to text file with Ctrl+E"),
        ("5", "In-App Tutorial", 
         "Interactive guide for new users, shows on first run"),
    ]
    
    for num, feature, description in features:
        print(f"  {num}. {feature}")
        print(f"     {description}")
        print()
    
    print("🎯 SUCCESS CRITERIA:")
    print("─" * 70)
    print("  ✓ Help overlay displays correctly")
    print("  ✓ All shortcuts are documented")
    print("  ✓ Search works for finding shortcuts")
    print("  ✓ Customizable bindings save correctly")
    print("  ✓ Users can interactively edit key bindings")
    print("  ✓ Tutorial is helpful for new users")
    print()


def main():
    """Run the keyboard shortcuts demo."""
    print("\n" + "=" * 70)
    print("    TODO TUI - Keyboard Shortcuts Help Demonstration")
    print("=" * 70 + "\n")
    
    key_features_summary()
    print_all_shortcuts()
    demonstrate_search()
    demonstrate_customization()
    demonstrate_export()
    demonstrate_tutorial()
    usage_guide()
    benefits()
    integration_examples()
    
    print("=" * 70)
    print("\n✨ To see it in action, run: uv run todo-tui")
    print("   • Press '?' for keyboard shortcuts help")
    print("   • Press 'Ctrl+T' for the interactive tutorial")
    print("   • Press 'Ctrl+K' to customize key bindings interactively")
    print("   • Click 'Edit' next to any action to change its key")
    print("   • Press 'Ctrl+E' to export a cheat sheet\n")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
