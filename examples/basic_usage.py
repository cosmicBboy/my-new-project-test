#!/usr/bin/env python3
"""Basic usage examples for the TODO TUI app.

This script demonstrates how to use the TODO TUI app programmatically,
including working with the storage layer and models.
"""

import tempfile
from pathlib import Path

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage
from todo_tui.app import TodoApp


def example_models():
    """Demonstrate working with TodoItem models."""
    print("=== TodoItem Model Example ===")
    
    # Create a new todo
    todo = TodoItem(title="Learn Python Textual")
    print(f"Created: {todo}")
    print(f"ID: {todo.id}")
    print(f"Created at: {todo.created_at}")
    print()
    
    # Toggle completion
    todo.toggle_completed()
    print(f"After completion: {todo}")
    print(f"Completed at: {todo.completed_at}")
    print()
    
    # Serialize to dict
    data = todo.to_dict()
    print(f"Serialized: {data}")
    print()
    
    # Deserialize from dict
    restored = TodoItem.from_dict(data)
    print(f"Restored: {restored}")
    print()


def example_storage():
    """Demonstrate working with TodoStorage."""
    print("=== TodoStorage Example ===")
    
    # Create a temporary storage file for this example
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        print(f"Storage file: {storage_path}")
        print()
        
        # Add some todos
        todos = [
            TodoItem(title="Write documentation"),
            TodoItem(title="Add unit tests"),
            TodoItem(title="Review pull requests"),
        ]
        
        for todo in todos:
            storage.add(todo)
            print(f"Added: {todo}")
        print()
        
        # Load all todos
        loaded = storage.get_all()
        print(f"Loaded {len(loaded)} todos:")
        for todo in loaded:
            print(f"  - {todo}")
        print()
        
        # Complete the first todo
        first_todo = loaded[0]
        first_todo.toggle_completed()
        storage.update(first_todo)
        print(f"Updated: {first_todo}")
        print()
        
        # Delete the last todo
        last_todo = loaded[-1]
        storage.delete(last_todo.id)
        print(f"Deleted: {last_todo}")
        print()
        
        # Show final state
        remaining = storage.get_all()
        print(f"Final state ({len(remaining)} todos):")
        for todo in remaining:
            print(f"  - {todo}")
        print()
        
    finally:
        # Cleanup
        if storage_path.exists():
            storage_path.unlink()


def example_app_info():
    """Display information about running the app."""
    print("=== Running the TODO TUI App ===")
    print()
    print("To run the interactive TUI application, use:")
    print("  uv run todo-tui")
    print()
    print("Or in Python code:")
    print("  from todo_tui.app import TodoApp")
    print("  app = TodoApp()")
    print("  app.run()")
    print()
    print("Keyboard shortcuts:")
    print("  ↑/↓     : Navigate todos")
    print("  Tab     : Switch between list and input")
    print("  Enter   : Add new todo (when in input)")
    print("  Space   : Toggle completion")
    print("  d       : Delete todo")
    print("  q       : Quit")
    print()
    print("Data is stored at: ~/.todo-tui.json")
    print()


def main():
    """Run all examples."""
    print("TODO TUI App - Usage Examples")
    print("=" * 50)
    print()
    
    example_models()
    print()
    
    example_storage()
    print()
    
    example_app_info()
    
    print("=" * 50)
    print("Examples complete!")
    print()
    print("Run 'uv run todo-tui' to start the interactive app.")


if __name__ == "__main__":
    main()
