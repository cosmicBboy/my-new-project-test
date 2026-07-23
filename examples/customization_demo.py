"""Example demonstrating customization features.

This example shows how to work with configuration, custom key bindings,
and cheat sheet export.
"""

import tempfile
from pathlib import Path

from todo_tui.config import Config
from todo_tui.help_overlay import HelpOverlay
from todo_tui.cheatsheet import CheatSheetGenerator, export_cheat_sheet


def demo_config_management():
    """Demonstrate configuration management."""
    print("=" * 70)
    print("Configuration Management Demo")
    print("=" * 70)
    print()
    
    # Create a temporary config for demo
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        # Initialize config
        config = Config(config_path)
        
        print("Default Key Bindings:")
        print("-" * 70)
        for action in ["quit", "toggle", "delete", "postpone", "help"]:
            key = config.get_key(action)
            print(f"  {action:15} → {key}")
        print()
        
        # Customize key bindings
        print("Customizing Key Bindings:")
        print("-" * 70)
        config.set_key("quit", "ctrl+q")
        config.set_key("toggle", "enter")
        config.set_key("help", "f1")
        print("  Changed 'quit' to 'ctrl+q'")
        print("  Changed 'toggle' to 'enter'")
        print("  Changed 'help' to 'f1'")
        print()
        
        # Display updated bindings
        print("Updated Key Bindings:")
        print("-" * 70)
        for action in ["quit", "toggle", "delete", "postpone", "help"]:
            key = config.get_key(action)
            print(f"  {action:15} → {key}")
        print()
        
        # Reset to defaults
        print("Resetting to Defaults:")
        print("-" * 70)
        config.reset_keybindings()
        print("  All bindings reset!")
        print()
        
        # Display reset bindings
        print("Reset Key Bindings:")
        print("-" * 70)
        for action in ["quit", "toggle", "delete", "postpone", "help"]:
            key = config.get_key(action)
            print(f"  {action:15} → {key}")
        print()
        
    finally:
        if config_path.exists():
            config_path.unlink()


def demo_tutorial_status():
    """Demonstrate tutorial status management."""
    print("=" * 70)
    print("Tutorial Status Demo")
    print("=" * 70)
    print()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        print("Initial Tutorial Status:")
        print(f"  Completed: {config.tutorial_completed}")
        print()
        
        print("Marking tutorial as completed...")
        config.mark_tutorial_completed()
        print(f"  Completed: {config.tutorial_completed}")
        print()
        
        print("Resetting tutorial (to show again)...")
        config.reset_tutorial()
        print(f"  Completed: {config.tutorial_completed}")
        print()
        
    finally:
        if config_path.exists():
            config_path.unlink()


def demo_cheat_sheet_export():
    """Demonstrate cheat sheet export."""
    print("=" * 70)
    print("Cheat Sheet Export Demo")
    print("=" * 70)
    print()
    
    # Get shortcuts from help overlay
    help_overlay = HelpOverlay()
    shortcuts = help_overlay.shortcuts
    
    print(f"Found {len(shortcuts)} keyboard shortcuts")
    print()
    
    # Generate text version
    print("Generating Text Cheat Sheet:")
    print("-" * 70)
    generator = CheatSheetGenerator(shortcuts)
    text = generator.generate_text()
    
    # Show first few lines
    lines = text.split('\n')[:15]
    for line in lines:
        print(line)
    print("...")
    print(f"(Full text: {len(text.split(chr(10)))} lines)")
    print()
    
    # Generate markdown version
    print("Generating Markdown Cheat Sheet:")
    print("-" * 70)
    markdown = generator.generate_markdown()
    
    # Show first few lines
    lines = markdown.split('\n')[:15]
    for line in lines:
        print(line)
    print("...")
    print(f"(Full markdown: {len(markdown.split(chr(10)))} lines)")
    print()
    
    # Export to files
    print("Exporting Cheat Sheets:")
    print("-" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Export text
        text_path = tmp_path / "shortcuts.txt"
        export_cheat_sheet(shortcuts, text_path)
        print(f"  Text:     {text_path.name} ({text_path.stat().st_size} bytes)")
        
        # Export markdown
        md_path = tmp_path / "shortcuts.md"
        export_cheat_sheet(shortcuts, md_path)
        print(f"  Markdown: {md_path.name} ({md_path.stat().st_size} bytes)")
        print()


def demo_shortcuts_reference():
    """Demonstrate shortcuts reference features."""
    print("=" * 70)
    print("Shortcuts Reference Demo")
    print("=" * 70)
    print()
    
    help_overlay = HelpOverlay()
    
    # Show categories
    categories = {}
    for shortcut in help_overlay.shortcuts:
        if shortcut.category not in categories:
            categories[shortcut.category] = []
        categories[shortcut.category].append(shortcut)
    
    print("Shortcut Categories:")
    print("-" * 70)
    for category, shortcuts in categories.items():
        print(f"  {category:20} {len(shortcuts)} shortcuts")
    print()
    
    # Demo search functionality
    print("Search Functionality Demo:")
    print("-" * 70)
    
    search_terms = ["toggle", "delete", "navigation", "postpone"]
    for term in search_terms:
        matches = [s for s in help_overlay.shortcuts if s.matches_search(term)]
        print(f"  Search '{term:12}' → {len(matches)} matches")
        for shortcut in matches[:2]:  # Show first 2
            print(f"    • {shortcut.key:15} {shortcut.action}")
        if len(matches) > 2:
            print(f"    ... and {len(matches) - 2} more")
        print()


def demo_customization_workflow():
    """Demonstrate a complete customization workflow."""
    print("=" * 70)
    print("Complete Customization Workflow")
    print("=" * 70)
    print()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        print("Step 1: User starts app for first time")
        print(f"  Tutorial completed: {config.tutorial_completed}")
        print()
        
        print("Step 2: User completes tutorial")
        config.mark_tutorial_completed()
        print(f"  Tutorial completed: {config.tutorial_completed}")
        print()
        
        print("Step 3: User customizes key bindings")
        print("  User prefers Vim-style bindings...")
        config.set_key("quit", "shift+z_shift+z")  # :wq equivalent
        config.set_key("delete", "d_d")  # dd to delete
        print("  Bindings saved!")
        print()
        
        print("Step 4: User exports cheat sheet")
        help_overlay = HelpOverlay()
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "my-shortcuts.md"
            export_cheat_sheet(help_overlay.shortcuts, tmp_path)
            print(f"  Cheat sheet exported: {tmp_path.name}")
            print(f"  Size: {tmp_path.stat().st_size} bytes")
        print()
        
        print("Step 5: User shares config with colleague")
        print(f"  Config file: {config_path}")
        print("  Colleague can copy this file to use same settings!")
        print()
        
    finally:
        if config_path.exists():
            config_path.unlink()


def main():
    """Run all customization demos."""
    print()
    print("TODO TUI - Customization Features Demo")
    print("=" * 70)
    print()
    print("This demo shows the new customization features:")
    print("  • Custom key bindings")
    print("  • Configuration management")
    print("  • Tutorial status tracking")
    print("  • Cheat sheet export")
    print()
    print("Press '?' in the app to access the help overlay")
    print("Press 'c' in the app to customize key bindings")
    print("Press 'x' in the app to export cheat sheets")
    print("Press 't' in the app to replay the tutorial")
    print()
    
    demo_config_management()
    print()
    
    demo_tutorial_status()
    print()
    
    demo_cheat_sheet_export()
    print()
    
    demo_shortcuts_reference()
    print()
    
    demo_customization_workflow()
    print()
    
    print("=" * 70)
    print("Customization features demo complete!")
    print()
    print("To try these features in the app:")
    print("  1. Run: uv run todo-tui")
    print("  2. Press '?' for help")
    print("  3. Press 'c' to customize keys")
    print("  4. Press 'x' to export cheat sheets")
    print("  5. Press 't' to replay tutorial")
    print()


if __name__ == "__main__":
    main()
