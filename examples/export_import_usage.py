"""Example demonstrating export and import functionality.

This example shows how to:
1. Create TODO items programmatically
2. Export to different formats (JSON, CSV, Markdown)
3. Import from JSON files
4. Use merge vs replace modes
"""

from pathlib import Path
from datetime import datetime, timedelta
import tempfile

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


def main():
    """Demonstrate export and import functionality."""
    
    # Create a temporary storage for the demo
    temp_dir = Path(tempfile.mkdtemp())
    storage = TodoStorage(temp_dir / "demo.json")
    
    print("=" * 60)
    print("TODO TUI - Export/Import Demo")
    print("=" * 60)
    print()
    
    # Step 1: Create some sample todos
    print("Step 1: Creating sample TODO items...")
    todos = [
        TodoItem(title="Write documentation"),
        TodoItem(title="Add unit tests"),
        TodoItem(title="Review pull requests"),
        TodoItem(title="Deploy to production"),
    ]
    
    # Mark some as completed
    todos[0].toggle_completed()
    todos[2].toggle_completed()
    
    # Postpone one
    todos[3].postpone_until_tomorrow()
    
    # Save to storage
    storage.save(todos)
    print(f"✓ Created {len(todos)} TODO items")
    print()
    
    # Step 2: Export to JSON
    print("Step 2: Exporting to JSON...")
    json_path = temp_dir / "todos.json"
    storage.export_json(json_path)
    print(f"✓ Exported to: {json_path}")
    print(f"  File size: {json_path.stat().st_size} bytes")
    print()
    
    # Step 3: Export to CSV
    print("Step 3: Exporting to CSV...")
    csv_path = temp_dir / "todos.csv"
    storage.export_csv(csv_path)
    print(f"✓ Exported to: {csv_path}")
    print(f"  File size: {csv_path.stat().st_size} bytes")
    print()
    
    # Step 4: Export to Markdown
    print("Step 4: Exporting to Markdown...")
    md_path = temp_dir / "todos.md"
    storage.export_markdown(md_path)
    print(f"✓ Exported to: {md_path}")
    print(f"  File size: {md_path.stat().st_size} bytes")
    print()
    
    # Display Markdown content
    print("Markdown preview:")
    print("-" * 60)
    print(md_path.read_text())
    print("-" * 60)
    print()
    
    # Step 5: Import with REPLACE mode
    print("Step 5: Testing REPLACE mode import...")
    new_storage = TodoStorage(temp_dir / "new_storage.json")
    new_storage.add(TodoItem(title="Existing task"))
    print(f"  Before import: {len(new_storage.load())} todo(s)")
    
    imported = new_storage.import_json(json_path, merge=False)
    print(f"  After import: {len(new_storage.load())} todo(s)")
    print(f"✓ Replaced all todos with {len(imported)} imported items")
    print()
    
    # Step 6: Import with MERGE mode
    print("Step 6: Testing MERGE mode import...")
    merge_storage = TodoStorage(temp_dir / "merge_storage.json")
    merge_storage.add(TodoItem(title="Original task 1"))
    merge_storage.add(TodoItem(title="Original task 2"))
    print(f"  Before import: {len(merge_storage.load())} todo(s)")
    
    imported = merge_storage.import_json(json_path, merge=True)
    all_todos = merge_storage.load()
    print(f"  After import: {len(all_todos)} todo(s)")
    print(f"✓ Added {len(imported)} new items (kept existing ones)")
    print()
    
    # Step 7: Export specific todos (filtered)
    print("Step 7: Exporting only completed tasks...")
    completed_todos = [t for t in todos if t.completed]
    completed_path = temp_dir / "completed.json"
    storage.export_json(completed_path, todos=completed_todos)
    print(f"✓ Exported {len(completed_todos)} completed todo(s)")
    print()
    
    # Step 8: Show all exported files
    print("Summary of exported files:")
    print("-" * 60)
    for file_path in temp_dir.glob("*.json"):
        print(f"  📄 {file_path.name}: {file_path.stat().st_size} bytes")
    for file_path in temp_dir.glob("*.csv"):
        print(f"  📄 {file_path.name}: {file_path.stat().st_size} bytes")
    for file_path in temp_dir.glob("*.md"):
        print(f"  📄 {file_path.name}: {file_path.stat().st_size} bytes")
    print("-" * 60)
    print()
    
    # Step 9: Demonstrate error handling
    print("Step 9: Demonstrating error handling...")
    
    try:
        storage.import_json(Path("/nonexistent/file.json"))
    except FileNotFoundError:
        print("✓ Correctly handles missing file error")
    
    try:
        invalid_json = temp_dir / "invalid.json"
        invalid_json.write_text("not valid json {{{")
        storage.import_json(invalid_json)
    except ValueError:
        print("✓ Correctly handles invalid JSON error")
    
    print()
    
    # Cleanup
    print("Cleaning up temporary files...")
    import shutil
    shutil.rmtree(temp_dir)
    print("✓ Done!")
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    print()
    print("To use export/import in the app:")
    print("  - Press 'e' to export")
    print("  - Press 'i' to import")
    print("  - Ctrl+M to toggle merge mode when importing")


if __name__ == "__main__":
    main()
