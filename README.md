# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- 📤 Export TODO lists to JSON or Markdown
- 📥 Import TODO lists from JSON files
- ⌨️ Keyboard-driven interface
- 🎨 Clean, modern TUI design
- 🚀 Fast and lightweight

## Requirements

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

### Using uv (recommended)

1. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-tui
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

### Development Installation

To install with development dependencies:

```bash
uv sync --extra dev
```

## Usage

### Running the App

Start the TODO TUI app:

```bash
uv run todo-tui
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through TODO items |
| `Tab` | Switch between list and input field |
| `Enter` | Add new TODO (when in input field) |
| `Space` | Toggle TODO completion status |
| `p` | Postpone selected TODO until tomorrow |
| `d` | Delete selected TODO |
| `e` | Export TODO list |
| `i` | Import TODO list |
| `q` | Quit application |

### Basic Workflow

1. **Add a TODO**: Press `Tab` to focus the input field, type your task, and press `Enter`
2. **Complete a TODO**: Navigate to the item and press `Space`
3. **Postpone a TODO**: Navigate to the item and press `p` to postpone it until tomorrow
4. **Delete a TODO**: Navigate to the item and press `d`
5. **Exit**: Press `q` to quit (your data is automatically saved)

### Postponing TODOs

The postpone feature allows you to defer tasks until tomorrow:

- Press `p` on any TODO item to postpone it until tomorrow
- Postponed items are displayed with a `[postponed until YYYY-MM-DD]` indicator
- Postponed items remain visible in the list with an italic style
- Pressing `p` multiple times keeps the postpone date as tomorrow (it doesn't advance further)
- Postponed items automatically become active again after the postpone date passes

### Export and Import

#### Exporting TODO Lists

Make your TODO lists portable by exporting them:

1. Press `e` to open the export dialog
2. Enter a filename (without extension)
3. Choose format:
   - Press `j` for JSON format (machine-readable, preserves all data)
   - Press `m` for Markdown format (human-readable, great for sharing)
4. Files are saved to `~/todo-exports/`

**Export formats:**

- **JSON**: Complete data export including all metadata (IDs, timestamps, postpone dates). Perfect for backups and importing into another instance.
- **Markdown**: Human-readable format organized by task status (Active, Postponed, Completed). Great for sharing, printing, or viewing in any text editor.

#### Importing TODO Lists

Import TODO lists from JSON files:

1. Press `i` to open the import dialog
2. Enter the path to your JSON file (supports `~` for home directory)
3. Choose import mode:
   - Press `a` to append (add to existing todos, avoiding duplicates)
   - Press `r` to replace (remove all existing todos and import new ones)
4. The import will process and display a count of imported items

**Import modes:**

- **Append**: Adds imported todos to your existing list, automatically avoiding duplicates based on todo IDs
- **Replace**: Removes all current todos and replaces them with the imported ones (use for restoring backups)

**Example workflow:**
```bash
# Export your todos
Press 'e' → enter "backup-2024-01" → press 'j'
# Creates: ~/todo-exports/backup-2024-01.json

# Import todos from a file
Press 'i' → enter "~/todo-exports/backup-2024-01.json" → press 'a'
# Appends todos from the backup file
```

## Data Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. The data persists between sessions, so you can safely close and reopen the app without losing your tasks.

Exported files are saved to `~/todo-exports/` by default.

## Development

### Running Tests

Run the test suite:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=todo_tui --cov-report=html
```

### Project Structure

```
todo-tui/
├── src/
│   └── todo_tui/
│       ├── __init__.py       # Package initialization
│       ├── app.py            # Main Textual application
│       ├── models.py         # Data models (TodoItem)
│       └── storage.py        # Persistence layer
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_storage.py       # Storage tests
│   └── test_app.py           # App tests
├── examples/
│   └── basic_usage.py        # Usage examples
├── pyproject.toml            # Project configuration
├── README.md                 # This file
└── SPEC.md                   # Design specification
```

### Code Style

The project follows:
- PEP 8 style guidelines
- Type hints throughout the codebase
- Comprehensive docstrings

## Examples

Check out the `examples/` directory for usage examples:

```bash
python examples/basic_usage.py
```

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- If corrupted, you can delete it (you'll lose your TODOs)
- The app will create a new file on next run

### Import/Export issues

- Ensure the export directory exists and is writable: `~/todo-exports/`
- For imports, verify the file path is correct and the file contains valid JSON
- Only JSON files can be imported (Markdown exports are for reading only)

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure tests pass: `uv run pytest`
5. Submit a pull request

## Documentation

- [SPEC.md](SPEC.md) - Detailed design decisions and specifications
- [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) - Planned features and enhancements
- [Textual Documentation](https://textual.textualize.io/) - Framework documentation

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral

## Roadmap

See [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for planned features and enhancements.
