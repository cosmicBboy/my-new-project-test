# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- 🔄 Automatic backups on every save
- 📤 Export to multiple formats (JSON, CSV, Markdown, HTML)
- 📥 Import from JSON files with merge/replace modes
- 📦 Archive completed todos to keep your list clean
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
| `a` | Archive completed todos |
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

### Export and Backup Features

#### Exporting TODOs

Press `e` to open the export dialog. You can export your TODO list to multiple formats:

**Supported formats:**
- **JSON** (`.json`): Full data export preserving all metadata (IDs, timestamps, postpone dates)
- **CSV** (`.csv`): Spreadsheet-compatible format for use in Excel, Google Sheets, etc.
- **Markdown** (`.md`): Human-readable checklist format for documentation and sharing
- **HTML** (`.html`): Styled web page with checkboxes and completion status

**How to export:**
1. Press `e` to open the export dialog
2. Enter the export path with the desired extension (e.g., `~/my-todos.json`, `~/export.csv`)
3. Press `Enter` or click "Export"
4. The file will be created with all your todos in the specified format

**Format comparison:**
- **JSON**: Best for backups and data portability between devices
- **CSV**: Best for data analysis, spreadsheets, or importing into other tools
- **Markdown**: Best for sharing with others or including in documentation
- **HTML**: Best for viewing in a web browser or printing

#### Importing TODOs

Press `i` to open the import dialog. You can import todos from JSON files:

**Import modes:**
- **Merge mode** (default): Adds imported todos to your existing list, skipping duplicates
- **Replace mode**: Replaces all your current todos with the imported ones

**How to import:**
1. Press `i` to open the import dialog
2. Enter the path to the JSON file to import (e.g., `~/my-todos.json`)
3. Press `Ctrl+M` to toggle between merge and replace mode
4. Press `Enter` or click "Import"

**Tips:**
- Only JSON files can be imported to ensure data integrity
- In merge mode, todos with the same ID will be skipped
- In replace mode, all existing todos will be lost (backup first!)
- Path expansion is supported (e.g., `~` for home directory)

#### Archiving Completed TODOs

Press `a` to archive completed todos. This moves all completed tasks to an archive file and removes them from your main list.

**Benefits:**
- Keeps your active list focused and manageable
- Preserves completed todos for future reference
- Improves app performance with large todo lists
- Creates a historical record of your accomplishments

**How to archive:**
1. Press `a` to open the archive confirmation dialog
2. Review the number of completed tasks to be archived
3. Confirm to proceed or cancel
4. Archived todos are saved to `~/.todo-tui-backups/todo-archive-TIMESTAMP.json`

#### Automatic Backups

The app automatically creates backups every time you save changes:

- Backups are stored in `~/.todo-tui-backups/`
- Backup files are named `todo-backup-TIMESTAMP.json`
- The 10 most recent backups are kept automatically
- Older backups are cleaned up to save disk space
- Backups preserve all your data in JSON format

**Restoring from backup:**
1. Navigate to `~/.todo-tui-backups/`
2. Find the backup file you want to restore
3. Copy it to `~/.todo-tui.json` (replacing the current file)
4. Restart the app

Or use the import feature:
1. Press `i` to import
2. Enter the path to the backup file
3. Choose replace mode (`Ctrl+M`)
4. Import the backup

## Data Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. The data persists between sessions, so you can safely close and reopen the app without losing your tasks.

**Storage locations:**
- **Main storage**: `~/.todo-tui.json`
- **Backups**: `~/.todo-tui-backups/todo-backup-*.json`
- **Archives**: `~/.todo-tui-backups/todo-archive-*.json`

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
- If corrupted, restore from a backup in `~/.todo-tui-backups/`
- Or delete it (you'll lose your TODOs) and the app will create a new file

### Export/Import issues

- **Export fails**: Check that you have write permissions in the target directory
- **Import fails**: Ensure the file is valid JSON and contains properly formatted todos
- **Path not found**: Use absolute paths or paths starting with `~` for home directory
- **Wrong format**: Check the file extension matches the desired format

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters

## Use Cases

### Backup and Restore
Export your todos to JSON for a complete backup, then import them on another device or after a system restore.

### Data Migration
Moving to a new computer? Export your todos and import them on the new machine.

### Sharing with Team
Export to Markdown or HTML to share your task list with team members who don't use the app.

### Data Analysis
Export to CSV to analyze your productivity patterns in a spreadsheet.

### Documentation
Export to Markdown to include your task list in project documentation.

### Regular Maintenance
Use the archive feature weekly or monthly to keep your list focused on active tasks.

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
