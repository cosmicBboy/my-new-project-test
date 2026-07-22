#!/usr/bin/env python3
"""Advanced usage examples for the TODO TUI app.

This script demonstrates advanced features and patterns for working with
the TODO app programmatically, including batch operations, filtering,
date queries, and storage manipulation.
"""

import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage


def example_batch_operations():
    """Demonstrate batch operations on todos."""
    print("=== Batch Operations Example ===")
    
    # Create a temporary storage file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        
        # Batch create multiple todos
        print("Creating multiple todos in batch...")
        todo_titles = [
            "Write unit tests",
            "Update documentation",
            "Review pull requests",
            "Refactor storage layer",
            "Add CI/CD pipeline",
            "Deploy to production",
        ]
        
        todos = [TodoItem(title=title) for title in todo_titles]
        for todo in todos:
            storage.add(todo)
        print(f"Created {len(todos)} todos")
        print()
        
        # Batch complete multiple todos
        print("Marking first 3 todos as complete...")
        all_todos = storage.get_all()
        for i in range(3):
            all_todos[i].toggle_completed()
            storage.update(all_todos[i])
        print(f"Completed {3} todos")
        print()
        
        # Display status
        all_todos = storage.get_all()
        completed = sum(1 for t in all_todos if t.completed)
        incomplete = len(all_todos) - completed
        print(f"Status: {completed} completed, {incomplete} incomplete")
        print()
        
        # Batch delete completed todos
        print("Deleting all completed todos...")
        todos_to_delete = [t for t in all_todos if t.completed]
        for todo in todos_to_delete:
            storage.delete(todo.id)
        print(f"Deleted {len(todos_to_delete)} completed todos")
        print()
        
        # Show remaining todos
        remaining = storage.get_all()
        print(f"Remaining todos: {len(remaining)}")
        for todo in remaining:
            print(f"  - {todo.title}")
        print()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_filtering_and_queries():
    """Demonstrate filtering and querying todos."""
    print("=== Filtering and Queries Example ===")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        
        # Create todos with different states
        todos = [
            TodoItem(title="Fix critical bug"),
            TodoItem(title="Add new feature"),
            TodoItem(title="Write tests"),
            TodoItem(title="Update README"),
            TodoItem(title="Code review"),
        ]
        
        # Mark some as completed
        todos[0].toggle_completed()
        todos[2].toggle_completed()
        todos[4].toggle_completed()
        
        for todo in todos:
            storage.add(todo)
        
        # Filter by completion status
        all_todos = storage.get_all()
        completed = [t for t in all_todos if t.completed]
        incomplete = [t for t in all_todos if not t.completed]
        
        print(f"Completed todos ({len(completed)}):")
        for todo in completed:
            print(f"  ✓ {todo.title}")
        print()
        
        print(f"Incomplete todos ({len(incomplete)}):")
        for todo in incomplete:
            print(f"  ☐ {todo.title}")
        print()
        
        # Search by title
        search_term = "test"
        matching = [t for t in all_todos if search_term.lower() in t.title.lower()]
        print(f"Todos matching '{search_term}': {len(matching)}")
        for todo in matching:
            print(f"  - {todo.title}")
        print()
        
        # Find todos by keyword
        keywords = ["bug", "feature", "test"]
        for keyword in keywords:
            matches = [t for t in all_todos if keyword.lower() in t.title.lower()]
            if matches:
                print(f"Todos with '{keyword}': {', '.join(t.title for t in matches)}")
        print()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_date_queries():
    """Demonstrate date-based queries and filtering."""
    print("=== Date-Based Queries Example ===")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        
        # Create todos with different timestamps
        now = datetime.now()
        
        # Simulate todos from different times
        old_todo = TodoItem(title="Old task")
        old_todo.created_at = now - timedelta(days=7)
        
        recent_todo = TodoItem(title="Recent task")
        recent_todo.created_at = now - timedelta(hours=2)
        
        new_todo = TodoItem(title="Brand new task")
        
        # Add a completed todo from yesterday
        completed_todo = TodoItem(title="Completed yesterday")
        completed_todo.created_at = now - timedelta(days=1)
        completed_todo.toggle_completed()
        
        for todo in [old_todo, recent_todo, new_todo, completed_todo]:
            storage.add(todo)
        
        all_todos = storage.get_all()
        
        # Find todos created today
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_todos = [t for t in all_todos if t.created_at >= today_start]
        print(f"Todos created today: {len(today_todos)}")
        for todo in today_todos:
            print(f"  - {todo.title} (created at {todo.created_at.strftime('%H:%M')})")
        print()
        
        # Find todos from last week
        week_ago = now - timedelta(days=7)
        week_todos = [t for t in all_todos if t.created_at >= week_ago]
        print(f"Todos from last 7 days: {len(week_todos)}")
        for todo in week_todos:
            days_ago = (now - todo.created_at).days
            print(f"  - {todo.title} ({days_ago} days ago)")
        print()
        
        # Find todos completed in last 24 hours
        day_ago = now - timedelta(days=1)
        recently_completed = [
            t for t in all_todos 
            if t.completed and t.completed_at and t.completed_at >= day_ago
        ]
        print(f"Completed in last 24 hours: {len(recently_completed)}")
        for todo in recently_completed:
            print(f"  ✓ {todo.title}")
        print()
        
        # Sort todos by creation date
        sorted_todos = sorted(all_todos, key=lambda t: t.created_at, reverse=True)
        print("Todos sorted by creation date (newest first):")
        for todo in sorted_todos:
            age = now - todo.created_at
            if age.days > 0:
                age_str = f"{age.days} days ago"
            elif age.seconds > 3600:
                age_str = f"{age.seconds // 3600} hours ago"
            else:
                age_str = f"{age.seconds // 60} minutes ago"
            print(f"  - {todo.title} ({age_str})")
        print()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_storage_migration():
    """Demonstrate migrating data between storage files."""
    print("=== Storage Migration Example ===")
    
    # Create source and destination storage files
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        source_path = Path(f.name)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        dest_path = Path(f.name)
    
    try:
        # Populate source storage
        source = TodoStorage(source_path)
        print(f"Source: {source_path}")
        print(f"Destination: {dest_path}")
        print()
        
        todos = [
            TodoItem(title="Task 1"),
            TodoItem(title="Task 2"),
            TodoItem(title="Task 3"),
        ]
        todos[0].toggle_completed()
        
        for todo in todos:
            source.add(todo)
        
        print(f"Source contains {len(source.get_all())} todos")
        print()
        
        # Migrate only incomplete todos
        dest = TodoStorage(dest_path)
        source_todos = source.get_all()
        incomplete_todos = [t for t in source_todos if not t.completed]
        
        print(f"Migrating {len(incomplete_todos)} incomplete todos...")
        for todo in incomplete_todos:
            dest.add(todo)
        
        print(f"Destination now contains {len(dest.get_all())} todos")
        print()
        
        # Verify migration
        print("Migrated todos:")
        for todo in dest.get_all():
            print(f"  - {todo.title} (ID: {todo.id})")
        print()
        
        # Create a backup
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            backup_path = Path(f.name)
        
        print(f"Creating backup at {backup_path}")
        import shutil
        shutil.copy(source_path, backup_path)
        
        backup_storage = TodoStorage(backup_path)
        print(f"Backup contains {len(backup_storage.get_all())} todos")
        print()
        
        if backup_path.exists():
            backup_path.unlink()
        
    finally:
        for path in [source_path, dest_path]:
            if path.exists():
                path.unlink()


def example_error_handling():
    """Demonstrate error handling and recovery."""
    print("=== Error Handling Example ===")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        
        # Try to update non-existent todo
        print("Attempting to update non-existent todo...")
        fake_todo = TodoItem(title="Ghost task")
        fake_todo.id = uuid4()  # Random ID that doesn't exist
        
        try:
            storage.update(fake_todo)
        except ValueError as e:
            print(f"  Error caught: {e}")
        print()
        
        # Try to delete non-existent todo
        print("Attempting to delete non-existent todo...")
        try:
            storage.delete(uuid4())
        except ValueError as e:
            print(f"  Error caught: {e}")
        print()
        
        # Corrupt the storage file and handle it
        print("Simulating corrupted storage file...")
        storage_path.write_text("invalid json {{{")
        
        try:
            corrupted_storage = TodoStorage(storage_path)
            corrupted_storage.load()
        except ValueError as e:
            print(f"  Error caught: {e}")
            print("  Recovering by recreating file...")
            storage_path.write_text("[]")
            recovered_storage = TodoStorage(storage_path)
            print(f"  Recovered: storage now has {len(recovered_storage.get_all())} todos")
        print()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_statistics_and_reporting():
    """Demonstrate generating statistics and reports."""
    print("=== Statistics and Reporting Example ===")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_path = Path(f.name)
    
    try:
        storage = TodoStorage(storage_path)
        
        # Create a variety of todos
        todos = [
            TodoItem(title="High priority: Fix security issue"),
            TodoItem(title="Medium priority: Add feature"),
            TodoItem(title="Low priority: Update docs"),
            TodoItem(title="High priority: Performance optimization"),
            TodoItem(title="Medium priority: Refactor code"),
        ]
        
        # Set creation times
        now = datetime.now()
        todos[0].created_at = now - timedelta(days=5)
        todos[1].created_at = now - timedelta(days=3)
        todos[2].created_at = now - timedelta(days=2)
        todos[3].created_at = now - timedelta(hours=12)
        todos[4].created_at = now - timedelta(hours=1)
        
        # Complete some
        todos[0].toggle_completed()
        todos[2].toggle_completed()
        
        for todo in todos:
            storage.add(todo)
        
        all_todos = storage.get_all()
        
        # Generate statistics
        print("Todo Statistics Report")
        print("=" * 50)
        print()
        
        total = len(all_todos)
        completed = sum(1 for t in all_todos if t.completed)
        incomplete = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        print(f"Total todos:        {total}")
        print(f"Completed:          {completed}")
        print(f"Incomplete:         {incomplete}")
        print(f"Completion rate:    {completion_rate:.1f}%")
        print()
        
        # Priority breakdown
        high_priority = [t for t in all_todos if "high priority" in t.title.lower()]
        medium_priority = [t for t in all_todos if "medium priority" in t.title.lower()]
        low_priority = [t for t in all_todos if "low priority" in t.title.lower()]
        
        print("Priority Breakdown:")
        print(f"  High:   {len(high_priority)} ({sum(1 for t in high_priority if t.completed)} completed)")
        print(f"  Medium: {len(medium_priority)} ({sum(1 for t in medium_priority if t.completed)} completed)")
        print(f"  Low:    {len(low_priority)} ({sum(1 for t in low_priority if t.completed)} completed)")
        print()
        
        # Age analysis
        ages = [(now - t.created_at).days for t in all_todos]
        avg_age = sum(ages) / len(ages) if ages else 0
        oldest_age = max(ages) if ages else 0
        newest_age = min(ages) if ages else 0
        
        print("Age Analysis:")
        print(f"  Average age:  {avg_age:.1f} days")
        print(f"  Oldest todo:  {oldest_age} days")
        print(f"  Newest todo:  {newest_age} days")
        print()
        
        # Time to completion
        completed_todos = [t for t in all_todos if t.completed and t.completed_at]
        if completed_todos:
            completion_times = [
                (t.completed_at - t.created_at).total_seconds() / 3600 
                for t in completed_todos
            ]
            avg_completion = sum(completion_times) / len(completion_times)
            print(f"Average time to completion: {avg_completion:.1f} hours")
        print()
        
    finally:
        if storage_path.exists():
            storage_path.unlink()


def example_multi_storage():
    """Demonstrate working with multiple storage files."""
    print("=== Multiple Storage Files Example ===")
    
    # Create storage files for different projects
    storage_files = {}
    try:
        for project in ["work", "personal", "learning"]:
            f = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
            storage_files[project] = Path(f.name)
            f.close()
        
        # Create separate storages
        work_storage = TodoStorage(storage_files["work"])
        personal_storage = TodoStorage(storage_files["personal"])
        learning_storage = TodoStorage(storage_files["learning"])
        
        # Populate each storage
        work_todos = [
            TodoItem(title="Finish quarterly report"),
            TodoItem(title="Team meeting prep"),
        ]
        for todo in work_todos:
            work_storage.add(todo)
        
        personal_todos = [
            TodoItem(title="Grocery shopping"),
            TodoItem(title="Pay bills"),
        ]
        for todo in personal_todos:
            personal_storage.add(todo)
        
        learning_todos = [
            TodoItem(title="Complete Python course"),
            TodoItem(title="Read design patterns book"),
        ]
        for todo in learning_todos:
            learning_storage.add(todo)
        
        # Display all projects
        print("Work todos:")
        for todo in work_storage.get_all():
            print(f"  - {todo.title}")
        print()
        
        print("Personal todos:")
        for todo in personal_storage.get_all():
            print(f"  - {todo.title}")
        print()
        
        print("Learning todos:")
        for todo in learning_storage.get_all():
            print(f"  - {todo.title}")
        print()
        
        # Aggregate view
        all_projects = [
            ("Work", work_storage),
            ("Personal", personal_storage),
            ("Learning", learning_storage),
        ]
        
        print("Summary across all projects:")
        total_todos = 0
        for name, storage in all_projects:
            count = len(storage.get_all())
            total_todos += count
            print(f"  {name}: {count} todos")
        print(f"  Total: {total_todos} todos")
        print()
        
    finally:
        for path in storage_files.values():
            if path.exists():
                path.unlink()


def main():
    """Run all advanced examples."""
    print("TODO TUI App - Advanced Usage Examples")
    print("=" * 50)
    print()
    
    example_batch_operations()
    print()
    
    example_filtering_and_queries()
    print()
    
    example_date_queries()
    print()
    
    example_storage_migration()
    print()
    
    example_error_handling()
    print()
    
    example_statistics_and_reporting()
    print()
    
    example_multi_storage()
    print()
    
    print("=" * 50)
    print("Advanced examples complete!")
    print()
    print("These examples demonstrate:")
    print("  ✓ Batch operations (create, update, delete)")
    print("  ✓ Filtering and searching todos")
    print("  ✓ Date-based queries and analysis")
    print("  ✓ Storage migration and backup")
    print("  ✓ Error handling and recovery")
    print("  ✓ Statistics and reporting")
    print("  ✓ Multiple storage files")
    print()
    print("See examples/basic_usage.py for basic usage.")


if __name__ == "__main__":
    main()
