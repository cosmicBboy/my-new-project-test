"""Example demonstrating rich task descriptions feature.

This example shows how to:
1. Create todos with detailed descriptions
2. Use markdown formatting in descriptions
3. Add links and code snippets
4. Work with multi-line notes
"""

from todo_tui.models import TodoItem
from todo_tui.storage import TodoStorage
from pathlib import Path
import tempfile


def main():
    """Demonstrate rich description features."""
    
    # Use a temporary storage file for this demo
    temp_dir = tempfile.mkdtemp()
    storage_path = Path(temp_dir) / "demo_todos.json"
    storage = TodoStorage(storage_path)
    
    print("=== Rich Task Descriptions Demo ===\n")
    
    # Example 1: Simple description
    print("1. Creating a todo with a simple description...")
    todo1 = TodoItem(
        title="Update documentation",
        description="Add examples for the new API endpoints."
    )
    storage.add(todo1)
    print(f"   Created: {todo1}")
    print(f"   Has description: {todo1.has_description()}")
    print()
    
    # Example 2: Multi-line description with markdown
    print("2. Creating a todo with markdown-formatted description...")
    todo2 = TodoItem(
        title="Review pull request #234",
        description="""# Code Review Checklist

## Security
- Check input validation
- Review authentication logic
- Verify authorization checks

## Quality
- Test coverage > 80%
- No code duplication
- Follow style guide

## Documentation
- API docs updated
- README reflects changes
- Examples provided

## Links
PR: https://github.com/team/repo/pull/234
Docs: https://docs.example.com/api
"""
    )
    storage.add(todo2)
    print(f"   Created: {todo2}")
    print("   Description preview:")
    for line in todo2.description.split('\n')[:5]:
        print(f"     {line}")
    print("     ...")
    print()
    
    # Example 3: Description with code snippets
    print("3. Creating a todo with code snippets...")
    todo3 = TodoItem(
        title="Fix authentication bug",
        description="""Found an issue in the login flow.

The problem is in `auth.py` line 42:
`if user.password == password:`

This should use proper password hashing:
`if verify_password(password, user.password_hash):`

Steps to fix:
1. Update the comparison logic
2. Add unit tests
3. Update integration tests
"""
    )
    storage.add(todo3)
    print(f"   Created: {todo3}")
    print()
    
    # Example 4: Description with links and references
    print("4. Creating a todo with external references...")
    todo4 = TodoItem(
        title="Research GraphQL implementation",
        description="""# Research Task

## Resources
- GraphQL Spec: https://spec.graphql.org/
- Apollo Server: https://www.apollographql.com/docs/apollo-server/
- Best Practices: https://graphql.org/learn/best-practices/

## Questions to Answer
- Should we use Apollo or custom implementation?
- How to handle authentication?
- What's the migration path from REST?

## Timeline
Spend 2-3 hours researching, then write up findings.
"""
    )
    storage.add(todo4)
    print(f"   Created: {todo4}")
    print()
    
    # Example 5: Task with checklist in description
    print("5. Creating a todo with a subtask checklist...")
    todo5 = TodoItem(
        title="Prepare for product launch",
        description="""# Launch Preparation

## Marketing
- [ ] Write press release
- [ ] Update website
- [ ] Schedule social media posts
- [ ] Contact tech bloggers

## Technical
- [ ] Deploy to production
- [ ] Set up monitoring
- [ ] Configure CDN
- [ ] Test payment system

## Legal
- [ ] Review terms of service
- [ ] Privacy policy updated
- [ ] Cookie consent implemented
"""
    )
    storage.add(todo5)
    print(f"   Created: {todo5}")
    print()
    
    # Display all todos
    print("\n=== Summary ===")
    print(f"Total todos created: {len(storage.get_all())}")
    print("\nAll todos:")
    for i, todo in enumerate(storage.get_all(), 1):
        desc_info = f" ({len(todo.description)} chars)" if todo.has_description() else ""
        print(f"  {i}. {todo.title}{desc_info}")
    
    # Show serialization
    print("\n=== Storage Format ===")
    print(f"Data saved to: {storage_path}")
    print("\nExample serialized todo:")
    import json
    print(json.dumps(todo2.to_dict(), indent=2))
    
    # Demonstrate retrieval
    print("\n=== Retrieval ===")
    loaded_todos = storage.get_all()
    print(f"Loaded {len(loaded_todos)} todos from storage")
    
    # Verify descriptions are preserved
    print("\nVerifying description integrity:")
    for todo in loaded_todos:
        if todo.has_description():
            lines = todo.description.count('\n') + 1
            print(f"  ✓ '{todo.title}' - {lines} lines, {len(todo.description)} chars")
    
    print("\n=== Demo Complete ===")
    print("\nIn the actual app:")
    print("  - Press 'n' to add/edit descriptions")
    print("  - Press 'v' to view formatted descriptions")
    print("  - TODOs with descriptions show a [+] indicator")
    print("  - Markdown is rendered with colors and formatting")
    print("\nTry running: uv run todo-tui")


if __name__ == "__main__":
    main()
