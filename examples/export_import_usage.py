#!/usr/bin/env python3
"""Export and import usage examples for the TODO TUI app.

This script demonstrates how to programmatically export and import
TODO lists in different formats.
"""

import tempfile
from pathlib import Path
from datetime import datetime

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


def create_sample_todos():
    """Create a sample set of todos for demonstration."""
    todos = []
    
    # Active task
    todo1 = TodoItem(title="Write project documentation")
    todos.append(todo1)
    
    # Completed task
    todo2 = TodoItem(title="Set up development environment")
    todo2.toggle_completed()
    todos.append(todo2)
    
    # Postponed task
    todo3 = TodoItem(title="Review code changes")
    todo3.postpone_until_tomorrow()
    todos.append(todo3)
    
    # Another active task
    todo4 = TodoItem(title="Deploy to production")
    todos.append(todo4)
    
    # Completed task
    todo5 = TodoItem(title="Fix critical bug")
    todo5.toggle_completed()
    todos.append(todo5)
    
    return todos


def example_export_json():
    """Demonstrate exporting todos to JSON format."""
    print("=== Export to JSON Example ===\n")
    
    # Create temporary storage
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        # Set up storage with sample todos
        storage = TodoStorage(storage_path)
        todos = create_sample_todos()
        storage.save(todos)
        
        print(f"Created {len(todos)} sample todos")
        for todo in todos:
            print(f"  - {todo}")
        print()
        
        # Export to JSON
        export_path = Path(tempfile.gettempdir()) / "todos-export.json"
        storage.export_json(export_path)
        
        print(f"✅ Exported to: {export_path}")
        print(f"File size: {export_path.stat().st_size} bytes")
        print()
        
        # Show a snippet of the exported JSON
        content = export_path.read_text()
        lines = content.split('\n')[:10]
        print("First 10 lines of exported JSON:")
        for line in lines:
            print(f"  {line}")
        print("  ...")
        print()
        
        # Cleanup
        export_path.unlink()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_export_markdown():
    """Demonstrate exporting todos to Markdown format."""
    print("=== Export to Markdown Example ===\n")
    
    # Create temporary storage
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        # Set up storage with sample todos
        storage = TodoStorage(storage_path)
        todos = create_sample_todos()
        storage.save(todos)
        
        print(f"Created {len(todos)} sample todos")
        print()
        
        # Export to Markdown
        export_path = Path(tempfile.gettempdir()) / "todos-export.md"
        storage.export_markdown(export_path)
        
        print(f"✅ Exported to: {export_path}")
        print(f"File size: {export_path.stat().st_size} bytes")
        print()
        
        # Show the exported Markdown
        content = export_path.read_text()
        print("Exported Markdown content:")
        print("-" * 60)
        print(content)
        print("-" * 60)
        print()
        
        # Cleanup
        export_path.unlink()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_import_json_append():
    """Demonstrate importing todos in append mode."""
    print("=== Import JSON (Append Mode) Example ===\n")
    
    # Create storage with existing todos
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        
        # Add some existing todos
        existing = [
            TodoItem(title="Existing task 1"),
            TodoItem(title="Existing task 2"),
        ]
        storage.save(existing)
        print(f"Existing todos: {len(existing)}")
        for todo in existing:
            print(f"  - {todo}")
        print()
        
        # Create import file with new todos
        import_todos = [
            TodoItem(title="Imported task 1"),
            TodoItem(title="Imported task 2"),
            TodoItem(title="Imported task 3"),
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            import_path = Path(f.name)
        
        import_storage = TodoStorage(import_path)
        import_storage.save(import_todos)
        
        print(f"Import file contains: {len(import_todos)} todos")
        for todo in import_todos:
            print(f"  - {todo}")
        print()
        
        # Import in append mode
        count = storage.import_json(import_path, replace=False)
        print(f"✅ Imported {count} todos in append mode")
        print()
        
        # Show final state
        all_todos = storage.get_all()
        print(f"Total todos after import: {len(all_todos)}")
        for todo in all_todos:
            print(f"  - {todo}")
        print()
        
        # Cleanup
        import_path.unlink()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_import_json_replace():
    """Demonstrate importing todos in replace mode."""
    print("=== Import JSON (Replace Mode) Example ===\n")
    
    # Create storage with existing todos
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        
        # Add some existing todos
        existing = [
            TodoItem(title="Old task 1"),
            TodoItem(title="Old task 2"),
            TodoItem(title="Old task 3"),
        ]
        storage.save(existing)
        print(f"Existing todos: {len(existing)}")
        for todo in existing:
            print(f"  - {todo}")
        print()
        
        # Create import file with new todos
        import_todos = [
            TodoItem(title="New task 1"),
            TodoItem(title="New task 2"),
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            import_path = Path(f.name)
        
        import_storage = TodoStorage(import_path)
        import_storage.save(import_todos)
        
        print(f"Import file contains: {len(import_todos)} todos")
        for todo in import_todos:
            print(f"  - {todo}")
        print()
        
        # Import in replace mode
        count = storage.import_json(import_path, replace=True)
        print(f"✅ Imported {count} todos in replace mode")
        print()
        
        # Show final state
        all_todos = storage.get_all()
        print(f"Total todos after import: {len(all_todos)}")
        print("(Old todos were replaced)")
        for todo in all_todos:
            print(f"  - {todo}")
        print()
        
        # Cleanup
        import_path.unlink()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_backup_restore_workflow():
    """Demonstrate a complete backup and restore workflow."""
    print("=== Backup and Restore Workflow Example ===\n")
    
    # Create original storage
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        original_path = Path(f.name)
    
    try:
        print("Step 1: Create original todo list")
        original_storage = TodoStorage(original_path)
        original_todos = create_sample_todos()
        original_storage.save(original_todos)
        
        print(f"  Created {len(original_todos)} todos")
        print()
        
        # Create backup
        backup_path = Path(tempfile.gettempdir()) / f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        print(f"Step 2: Create backup at {backup_path}")
        original_storage.export_json(backup_path)
        print(f"  ✅ Backup created ({backup_path.stat().st_size} bytes)")
        print()
        
        # Simulate data loss (clear storage)
        print("Step 3: Simulate data loss")
        original_storage.clear()
        print(f"  Todos remaining: {len(original_storage.get_all())}")
        print()
        
        # Restore from backup
        print("Step 4: Restore from backup")
        count = original_storage.import_json(backup_path, replace=True)
        print(f"  ✅ Restored {count} todos")
        print()
        
        # Verify restoration
        restored_todos = original_storage.get_all()
        print(f"Step 5: Verify restoration")
        print(f"  Restored todos: {len(restored_todos)}")
        for todo in restored_todos:
            print(f"    - {todo}")
        print()
        
        # Check data integrity
        print("Step 6: Verify data integrity")
        all_match = True
        for orig, rest in zip(original_todos, restored_todos):
            if orig.id != rest.id or orig.title != rest.title:
                all_match = False
                break
        
        if all_match:
            print("  ✅ All data restored correctly!")
        else:
            print("  ❌ Data mismatch detected")
        print()
        
        # Cleanup
        backup_path.unlink()
        
    finally:
        if original_path.exists():
            original_path.unlink()


def example_cross_instance_sharing():
    """Demonstrate sharing todos between different instances."""
    print("=== Cross-Instance Sharing Example ===\n")
    
    # Create two separate storage instances (simulating different users/machines)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        alice_path = Path(f.name)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        bob_path = Path(f.name)
    
    try:
        # Alice creates some todos
        print("Alice's todos:")
        alice_storage = TodoStorage(alice_path)
        alice_todos = [
            TodoItem(title="Review Bob's code"),
            TodoItem(title="Update project documentation"),
            TodoItem(title="Fix merge conflicts"),
        ]
        alice_storage.save(alice_todos)
        for todo in alice_todos:
            print(f"  - {todo}")
        print()
        
        # Alice exports to share with Bob
        shared_path = Path(tempfile.gettempdir()) / "shared-todos.json"
        alice_storage.export_json(shared_path)
        print(f"✅ Alice exported todos to: {shared_path}")
        print()
        
        # Bob has his own todos
        print("Bob's existing todos:")
        bob_storage = TodoStorage(bob_path)
        bob_todos = [
            TodoItem(title="Implement new feature"),
            TodoItem(title="Write unit tests"),
        ]
        bob_storage.save(bob_todos)
        for todo in bob_todos:
            print(f"  - {todo}")
        print()
        
        # Bob imports Alice's todos (append mode)
        print("Bob imports Alice's todos...")
        count = bob_storage.import_json(shared_path, replace=False)
        print(f"✅ Bob imported {count} todos")
        print()
        
        # Show Bob's combined todo list
        print("Bob's combined todo list:")
        bob_all_todos = bob_storage.get_all()
        for todo in bob_all_todos:
            print(f"  - {todo}")
        print()
        
        print("Result: Both Alice and Bob now have a shared set of tasks!")
        print()
        
        # Cleanup
        shared_path.unlink()
        
    finally:
        if alice_path.exists():
            alice_path.unlink()
        if bob_path.exists():
            bob_path.unlink()


def main():
    """Run all export/import examples."""
    print("TODO TUI App - Export/Import Usage Examples")
    print("=" * 60)
    print()
    
    example_export_json()
    print()
    
    example_export_markdown()
    print()
    
    example_import_json_append()
    print()
    
    example_import_json_replace()
    print()
    
    example_backup_restore_workflow()
    print()
    
    example_cross_instance_sharing()
    print()
    
    print("=" * 60)
    print("Examples complete!")
    print()
    print("Key takeaways:")
    print("  • Export to JSON for full data backup/sharing")
    print("  • Export to Markdown for human-readable format")
    print("  • Import with 'append' to merge todos")
    print("  • Import with 'replace' to restore backups")
    print("  • Use exports to share todos between users/machines")
    print()
    print("In the TUI app:")
    print("  • Press 'e' to export")
    print("  • Press 'i' to import")


if __name__ == "__main__":
    main()
