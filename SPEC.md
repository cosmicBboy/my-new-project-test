# TODO TUI App Specification

## Overview
A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the Textual framework.

## Design Decisions

### Technology Stack

#### Python Version
- **Decision**: Python 3.11+
- **Rationale**: 
  - Modern type hints and performance improvements
  - Wide adoption and stable
  - Good balance between cutting-edge and stability

#### TUI Framework
- **Decision**: Textual (https://textual.textualize.io/)
- **Rationale**:
  - Modern, actively maintained Python TUI framework
  - Rich terminal rendering capabilities
  - Reactive and component-based architecture
  - Excellent documentation and examples
  - Built-in widgets for common UI patterns

#### Package Management
- **Decision**: uv with pyproject.toml
- **Rationale**:
  - Modern Python packaging standard (PEP 621)
  - Fast and reliable dependency resolution
  - Single source of truth for project metadata
  - Better than legacy setup.py approach

#### Data Storage
- **Decision**: JSON file-based storage
- **Rationale**:
  - Simple and sufficient for a TODO app
  - Human-readable format
  - No external database dependencies
  - Easy to backup and version control
  - Stored in user's home directory (~/.todo-tui.json)

#### Testing Framework
- **Decision**: pytest with pytest-asyncio
- **Rationale**:
  - Industry standard for Python testing
  - Excellent fixture system
  - Good async support needed for Textual
  - Clear and concise test syntax

### Architecture

#### Project Structure
```
todo-tui/
├── src/
│   └── todo_tui/
│       ├── __init__.py
│       ├── app.py          # Main Textual application
│       ├── models.py       # Data models
│       └── storage.py      # Persistence layer
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_app.py
├── examples/
│   └── basic_usage.py      # Standalone usage example
├── pyproject.toml
├── README.md
├── SPEC.md                 # This file
└── .python-version
```

#### Component Design

##### Models (`models.py`)
- **TodoItem**: Core data model
  - `id`: Unique identifier (UUID)
  - `title`: Task description
  - `completed`: Boolean status
  - `created_at`: Timestamp
  - `completed_at`: Optional timestamp
- Uses dataclasses for clean, typed data structures
- Immutable where appropriate

##### Storage (`storage.py`)
- **TodoStorage**: Handles persistence
  - `load()`: Read todos from JSON file
  - `save()`: Write todos to JSON file
  - `add()`: Add new todo
  - `update()`: Update existing todo
  - `delete()`: Remove todo
  - `get_all()`: Retrieve all todos
- Error handling for file I/O
- Automatic file creation if not exists

##### App (`app.py`)
- **TodoApp**: Main Textual application
  - Display list of todos
  - Input widget for adding new todos
  - Keyboard shortcuts for actions
  - Status bar with help text
- **TodoList**: Custom widget for displaying todos
  - Scrollable list
  - Visual distinction between completed/pending
  - Selection and interaction

### User Interface

#### Layout
```
┌─────────────────────────────────────┐
│ TODO TUI App                        │
├─────────────────────────────────────┤
│ [ ] Buy groceries                   │
│ [✓] Write documentation             │
│ [ ] Review pull requests            │
│                                     │
│                                     │
├─────────────────────────────────────┤
│ Add: [                            ] │
├─────────────────────────────────────┤
│ Enter: Add | Space: Toggle | d: Del │
└─────────────────────────────────────┘
```

#### Keyboard Shortcuts
- **Enter**: Add new todo (when in input field)
- **↑/↓**: Navigate todo list
- **Space**: Toggle todo completion status
- **d**: Delete selected todo
- **q**: Quit application

### Features

#### MVP (Minimum Viable Product)
1. Add new TODO items
2. Mark items as complete/incomplete
3. Delete items
4. Persist data between sessions
5. Basic keyboard navigation

#### Future Enhancements (Not in MVP)
- Edit existing todos
- Categories/tags
- Due dates
- Priority levels
- Search/filter
- Export to different formats
- Undo/redo
- Multiple todo lists

### Testing Strategy

#### Unit Tests
- **Models**: Test data structure creation, validation
- **Storage**: Test CRUD operations, file handling
- **App**: Test component initialization and basic interactions

#### Coverage Goals
- Aim for >80% code coverage
- Focus on business logic and data handling
- UI testing kept simple (Textual provides its own testing utilities)

### Error Handling

1. **File I/O Errors**: Graceful handling with user feedback
2. **Invalid Data**: Validation and clear error messages
3. **Storage Corruption**: Fallback to empty todo list with warning

### Documentation

#### README.md
- Installation instructions using uv
- Quick start guide
- Usage examples
- Keyboard shortcuts reference
- Troubleshooting

#### Code Documentation
- Docstrings for all public classes and methods
- Type hints throughout
- Inline comments for complex logic

### Development Workflow

1. **Setup**: `uv sync` to install dependencies
2. **Run**: `uv run todo-tui` to start the app
3. **Test**: `uv run pytest` to run tests
4. **Format**: Follow PEP 8 style guidelines

## Dependencies

### Runtime
- **textual** (>=0.47.0): TUI framework

### Development
- **pytest** (>=7.4.0): Testing framework
- **pytest-asyncio** (>=0.21.0): Async test support

## Versioning

- Start at 0.1.0 (development version)
- Follow semantic versioning (semver.org)
- Major.Minor.Patch format

## License

- To be determined by project owner

## Success Criteria

1. ✅ Functional TODO app with TUI
2. ✅ Data persists between sessions
3. ✅ Unit tests with good coverage
4. ✅ Clear documentation
5. ✅ Modern Python practices (uv, pyproject.toml, type hints)
6. ✅ Keyboard-driven interface
7. ✅ Clean, maintainable code