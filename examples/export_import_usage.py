"""Example demonstrating export, import, and backup features.

This example shows how to:
1. Create and manage TODO items programmatically
2. Export to different formats (JSON, CSV, Markdown, HTML)
3. Import from JSON files
4. Archive completed todos
5. Work with backups
"""

from pathlib import Path
import tempfile
from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


def main():
    """Demonstrate export, import, and backup features."""
    
    # Create a temporary storage for this example
    temp_dir = Path(tempfile.mkdtemp())
    storage_path = temp_dir / "example-todos.json"
    backup_dir = temp_dir / "backups"
    
    print("📝 TODO Export, Import, and Backup Example\n")
    print(f"Using temporary directory: {temp_dir}\n")
    
    # Initialize storage with automatic backups enabled
    storage = TodoStorage(
        storage_path=storage_path,
        enable_auto_backup=True,
        backup_dir=backup_dir
    )
    
    # ========== Part 1: Creating and Managing TODOs ==========
    print("=" * 60)
    print("Part 1: Creating TODOs")
    print("=" * 60)
    
    todos = [
        TodoItem(title="Write project documentation"),
        TodoItem(title="Review pull requests"),
        TodoItem(title="Update dependencies"),
        TodoItem(title="Deploy to production"),
        TodoItem(title="Team meeting notes"),
    ]
    
    # Mark some as completed
    todos[1].toggle_completed()
    todos[4].toggle_completed()
    
    # Postpone one
    todos[3].postpone_until_tomorrow()
    
    # Save todos (this creates an automatic backup)
    storage.save(todos)
    
    print(f"Created {len(todos)} todos")
    print(f"Completed: {sum(1 for t in todos if t.completed)}")
    print(f"Postponed: {sum(1 for t in todos if t.is_postponed())}")
    
    # Check that backup was created
    backups = list(backup_dir.glob("todo-backup-*.json"))
    print(f"Automatic backup created: {len(backups)} backup(s) found\n")
    
    # ========== Part 2: Exporting to Different Formats ==========
    print("=" * 60)
    print("Part 2: Exporting to Different Formats")
    print("=" * 60)
    
    # Export to JSON (full data preservation)
    json_export = temp_dir / "todos-export.json"
    storage.export_json(json_export)
    print(f"✓ Exported to JSON: {json_export}")
    print(f"  Size: {json_export.stat().st_size} bytes")
    
    # Export to CSV (spreadsheet compatible)
    csv_export = temp_dir / "todos-export.csv"
    storage.export_csv(csv_export)
    print(f"✓ Exported to CSV: {csv_export}")
    print(f"  Size: {csv_export.stat().st_size} bytes")
    
    # Export to Markdown (human-readable)
    md_export = temp_dir / "todos-export.md"
    storage.export_markdown(md_export)
    print(f"✓ Exported to Markdown: {md_export}")
    print(f"  Size: {md_export.stat().st_size} bytes")
    
    # Export to HTML (web page)
    html_export = temp_dir / "todos-export.html"
    storage.export_html(html_export)
    print(f"✓ Exported to HTML: {html_export}")
    print(f"  Size: {html_export.stat().st_size} bytes")
    
    print("\nPreview of Markdown export:")
    print("-" * 60)
    print(md_export.read_text()[:300] + "...")
    print("-" * 60)
    print()
    
    # ========== Part 3: Import with Merge Mode ==========
    print("=" * 60)
    print("Part 3: Importing with Merge Mode")
    print("=" * 60)
    
    # Create new todos and save them
    new_todo = TodoItem(title="New task after export")
    current_todos = storage.load()
    current_todos.append(new_todo)
    storage.save(current_todos)
    
    print(f"Added 1 new todo. Total todos now: {len(current_todos)}")
    
    # Import the previous export in merge mode
    imported_count = storage.import_json(json_export, mode="merge")
    
    print(f"Imported {imported_count} new todos in merge mode")
    
    all_todos = storage.load()
    print(f"Total todos after merge: {len(all_todos)}")
    print("(Duplicates were skipped based on ID)\n")
    
    # ========== Part 4: Import with Replace Mode ==========
    print("=" * 60)
    print("Part 4: Importing with Replace Mode")
    print("=" * 60)
    
    print(f"Current todos: {len(storage.load())}")
    
    # Import in replace mode (this will replace all current todos)
    imported_count = storage.import_json(json_export, mode="replace")
    
    print(f"Imported {imported_count} todos in replace mode")
    print(f"Total todos after replace: {len(storage.load())}")
    print("(All previous todos were replaced)\n")
    
    # ========== Part 5: Archiving Completed TODOs ==========
    print("=" * 60)
    print("Part 5: Archiving Completed TODOs")
    print("=" * 60)
    
    todos_before = storage.load()
    completed_before = sum(1 for t in todos_before if t.completed)
    active_before = sum(1 for t in todos_before if not t.completed)
    
    print(f"Before archiving:")
    print(f"  Total: {len(todos_before)}")
    print(f"  Active: {active_before}")
    print(f"  Completed: {completed_before}")
    
    # Archive completed todos
    archived_count, archive_path = storage.archive_completed()
    
    print(f"\nArchived {archived_count} completed todo(s)")
    print(f"Archive file: {archive_path.name}")
    
    todos_after = storage.load()
    print(f"\nAfter archiving:")
    print(f"  Total: {len(todos_after)}")
    print(f"  Active: {len(todos_after)}")
    print(f"  Completed: 0")
    
    # Show archive file size
    if archive_path:
        print(f"\nArchive file size: {archive_path.stat().st_size} bytes")
    
    print()
    
    # ========== Part 6: Working with Backups ==========
    print("=" * 60)
    print("Part 6: Automatic Backups")
    print("=" * 60)
    
    backups = sorted(backup_dir.glob("todo-backup-*.json"))
    print(f"Total backups created: {len(backups)}")
    
    if backups:
        print("\nMost recent backups:")
        for backup in backups[-3:]:  # Show last 3
            size = backup.stat().st_size
            print(f"  {backup.name} ({size} bytes)")
    
    print(f"\nBackups are automatically created on every save")
    print(f"Old backups are cleaned up (keeping last 10)")
    print()
    
    # ========== Part 7: Exporting Filtered TODOs ==========
    print("=" * 60)
    print("Part 7: Exporting Filtered TODOs")
    print("=" * 60)
    
    # Create some more todos with different states
    mixed_todos = [
        TodoItem(title="Active task 1"),
        TodoItem(title="Active task 2"),
        TodoItem(title="Completed task 1"),
        TodoItem(title="Completed task 2"),
    ]
    mixed_todos[2].toggle_completed()
    mixed_todos[3].toggle_completed()
    storage.save(mixed_todos)
    
    # Export only active todos
    active_only = [t for t in storage.load() if not t.completed]
    active_export = temp_dir / "active-only.json"
    storage.export_json(active_export, todos=active_only)
    
    print(f"Exported {len(active_only)} active todos to: {active_export.name}")
    
    # Export only completed todos
    completed_only = [t for t in storage.load() if t.completed]
    completed_export = temp_dir / "completed-only.json"
    storage.export_json(completed_export, todos=completed_only)
    
    print(f"Exported {len(completed_only)} completed todos to: {completed_export.name}")
    print()
    
    # ========== Summary ==========
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    print("\n✓ Export formats supported:")
    print("  - JSON: Full data with all metadata")
    print("  - CSV: Spreadsheet-compatible format")
    print("  - Markdown: Human-readable checklists")
    print("  - HTML: Styled web pages")
    
    print("\n✓ Import modes:")
    print("  - Merge: Adds to existing todos (skips duplicates)")
    print("  - Replace: Replaces all todos with imported ones")
    
    print("\n✓ Archive feature:")
    print("  - Moves completed todos to archive file")
    print("  - Keeps main list focused on active tasks")
    print("  - Preserves completed todos for reference")
    
    print("\n✓ Automatic backups:")
    print("  - Created on every save operation")
    print("  - Stored in backup directory")
    print("  - Old backups automatically cleaned up")
    
    print(f"\n📁 All files created in: {temp_dir}")
    print("   (This is a temporary directory for demonstration)")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
