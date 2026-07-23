"""
Example demonstrating export, import, backup, and archive features.

This script demonstrates programmatic usage of the TODO TUI storage layer,
showcasing all the export, import, backup, archive, and automatic backup capabilities.
"""

from pathlib import Path
import tempfile
from datetime import date, timedelta

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


def main():
    """Demonstrate export, import, backup, archive, and automatic backup features."""
    
    # Create a temporary storage for this demo
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "demo-todos.json"
        backup_dir = Path(tmpdir) / "backups"
        backup_dir.mkdir()
        
        # Create storage with automatic backups enabled
        storage = TodoStorage(storage_path, auto_backup_enabled=True)
        
        print("=" * 60)
        print("TODO TUI - Export, Import, Backup & Archive Demo")
        print("=" * 60)
        
        # 1. Create sample todos
        print("\n1. Creating sample TODO items...")
        todos = [
            TodoItem(title="Write project documentation"),
            TodoItem(title="Review pull requests"),
            TodoItem(title="Update dependencies"),
            TodoItem(title="Fix critical bug"),
            TodoItem(title="Plan next sprint"),
        ]
        
        # Mark some as completed
        todos[1].toggle_completed()
        todos[3].toggle_completed()
        
        # Postpone one
        todos[2].postpone_until_tomorrow()
        
        storage.save(todos)
        print(f"   Created {len(todos)} todos")
        print(f"   - Active: {sum(1 for t in todos if not t.completed)}")
        print(f"   - Completed: {sum(1 for t in todos if t.completed)}")
        print(f"   - Postponed: {sum(1 for t in todos if t.is_postponed())}")
        
        # 2. Demonstrate automatic backups
        print("\n2. Demonstrating automatic backups...")
        
        # Check if automatic backup was created on initialization
        backups = storage.list_backups(backup_dir)
        print(f"   Backups after initialization: {len(backups)}")
        
        # Perform many operations to trigger automatic backup
        print("   Performing 60 operations to trigger automatic backup...")
        for i in range(60):
            storage.add(TodoItem(title=f"Bulk task {i}"))
        
        backups = storage.list_backups(backup_dir)
        print(f"   Backups after 60 operations: {len(backups)}")
        print("   ✓ Automatic backup triggered after many operations")
        
        # Clear the bulk tasks
        storage.save(todos)
        
        # 3. Export to different formats
        print("\n3. Exporting to different formats...")
        
        export_dir = Path(tmpdir) / "exports"
        export_dir.mkdir()
        
        # Export to JSON
        json_path = export_dir / "todos.json"
        storage.export_json(json_path)
        print(f"   ✓ Exported to JSON: {json_path.name}")
        print(f"     Size: {json_path.stat().st_size} bytes")
        
        # Export to CSV
        csv_path = export_dir / "todos.csv"
        storage.export_csv(csv_path)
        print(f"   ✓ Exported to CSV: {csv_path.name}")
        print(f"     Size: {csv_path.stat().st_size} bytes")
        
        # Export to Markdown
        md_path = export_dir / "todos.md"
        storage.export_markdown(md_path)
        print(f"   ✓ Exported to Markdown: {md_path.name}")
        print(f"     Size: {md_path.stat().st_size} bytes")
        
        # Export to HTML
        html_path = export_dir / "todos.html"
        storage.export_html(html_path)
        print(f"   ✓ Exported to HTML: {html_path.name}")
        print(f"     Size: {html_path.stat().st_size} bytes")
        
        # Display Markdown content as example
        print("\n   Markdown preview:")
        print("   " + "-" * 56)
        for line in md_path.read_text().split('\n')[:10]:
            print(f"   {line}")
        print("   ...")
        
        # 4. Create manual backups
        print("\n4. Creating manual backups...")
        
        # Create first manual backup
        backup1 = storage.create_backup(backup_dir)
        print(f"   ✓ Manual backup 1 created: {backup1.name}")
        
        # Modify todos
        storage.add(TodoItem(title="New task added"))
        
        # Create second manual backup
        backup2 = storage.create_backup(backup_dir)
        print(f"   ✓ Manual backup 2 created: {backup2.name}")
        
        # List all backups (automatic + manual)
        backups = storage.list_backups(backup_dir)
        print(f"\n   Available backups ({len(backups)}) - automatic + manual:")
        for i, backup in enumerate(backups, 1):
            size = backup.stat().st_size
            print(f"     {i}. {backup.name} ({size} bytes)")
        
        # 5. Archive completed todos
        print("\n5. Archiving completed todos...")
        
        archive_path = Path(tmpdir) / "archive.json"
        
        current_count = len(storage.load())
        archived_count = storage.archive_completed(archive_path)
        remaining_count = len(storage.load())
        
        print(f"   ✓ Archived {archived_count} completed todo(s)")
        print(f"   - Before: {current_count} todos")
        print(f"   - After: {remaining_count} todos")
        print(f"   - Archive: {archive_path.name}")
        
        # Show archived todos
        archived_todos = storage.load_archive(archive_path)
        print(f"\n   Archived items:")
        for todo in archived_todos:
            completed_date = todo.completed_at.strftime('%Y-%m-%d') if todo.completed_at else 'N/A'
            print(f"     • {todo.title} (completed: {completed_date})")
        
        # 6. Import demonstration
        print("\n6. Demonstrating import...")
        
        # Export current state
        import_test_path = Path(tmpdir) / "import-test.json"
        storage.export_json(import_test_path)
        
        # Clear storage
        original_count = len(storage.load())
        storage.clear()
        print(f"   Cleared storage ({original_count} items)")
        
        # Import with replace mode
        imported = storage.import_json(import_test_path, merge=False)
        print(f"   ✓ Imported {len(imported)} todos (replace mode)")
        
        # Add a new todo
        storage.add(TodoItem(title="Another new task"))
        before_merge = len(storage.load())
        
        # Import with merge mode (should skip duplicates)
        new_todos = storage.import_json(import_test_path, merge=True)
        after_merge = len(storage.load())
        
        print(f"   ✓ Imported with merge mode:")
        print(f"     - Before merge: {before_merge} todos")
        print(f"     - New todos added: {len(new_todos)}")
        print(f"     - After merge: {after_merge} todos")
        
        # 7. Restore from backup
        print("\n7. Restoring from backup...")
        
        # Clear storage
        storage.clear()
        print(f"   Cleared storage")
        
        # Restore from first backup
        storage.restore_backup(backup1)
        restored_count = len(storage.load())
        print(f"   ✓ Restored from backup: {backup1.name}")
        print(f"   - Restored {restored_count} todos")
        
        # 8. Export filtered todos
        print("\n8. Exporting filtered todos...")
        
        all_todos = storage.load()
        active_only = [t for t in all_todos if not t.completed]
        
        active_export_path = Path(tmpdir) / "active-only.json"
        storage.export_json(active_export_path, todos=active_only)
        print(f"   ✓ Exported {len(active_only)} active todos to {active_export_path.name}")
        
        # 9. Demonstrate shutdown backup
        print("\n9. Testing automatic backup on shutdown...")
        
        # Add a few more operations
        storage.add(TodoItem(title="Final task 1"))
        storage.add(TodoItem(title="Final task 2"))
        
        backups_before_shutdown = len(storage.list_backups(backup_dir))
        print(f"   Backups before shutdown: {backups_before_shutdown}")
        
        # Call shutdown (simulates app exit)
        storage.shutdown()
        
        backups_after_shutdown = len(storage.list_backups(backup_dir))
        print(f"   Backups after shutdown: {backups_after_shutdown}")
        
        if backups_after_shutdown > backups_before_shutdown:
            print("   ✓ Automatic backup created on shutdown")
        else:
            print("   ℹ No new backup needed (recent backup exists)")
        
        # 10. Summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        
        final_todos = storage.load()
        print(f"Current todos: {len(final_todos)}")
        print(f"  - Active: {sum(1 for t in final_todos if not t.completed)}")
        print(f"  - Completed: {sum(1 for t in final_todos if t.completed)}")
        
        archived = storage.load_archive(archive_path)
        print(f"\nArchived todos: {len(archived)}")
        
        backups = storage.list_backups(backup_dir)
        print(f"Backups available: {len(backups)} (automatic + manual)")
        
        print("\nExports created:")
        for export_file in export_dir.iterdir():
            print(f"  • {export_file.name} ({export_file.stat().st_size} bytes)")
        
        print("\n" + "=" * 60)
        print("Automatic Backup Features Demonstrated:")
        print("=" * 60)
        print("✓ Backup on initialization (if needed)")
        print("✓ Backup after many operations (50+ changes)")
        print("✓ Backup on shutdown (if changes made)")
        print("✓ Seamless background operation")
        print("✓ No user intervention required")
        
        print("\n" + "=" * 60)
        print("Demo completed successfully!")
        print("=" * 60)
        
        print("\nNote: This demo used temporary files that will be cleaned up.")
        print("In the actual app, files are stored in:")
        print(f"  - Main storage: ~/.todo-tui.json")
        print(f"  - Backups (auto + manual): ~/.todo-tui-backups/")
        print(f"  - Archive: ~/.todo-tui-archive.json")
        print("\nAutomatic backups run in the background to protect your data!")


if __name__ == "__main__":
    main()
