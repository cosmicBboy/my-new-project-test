# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- 🤖 **Automatic backups** (created daily and after every 50 operations)
- 📤 Export to multiple formats (JSON, CSV, Markdown, HTML)
- 📥 Import from JSON files
- 🔄 Manual backups on-demand
- 📦 Archive completed todos
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
| `e` | Export TODO items |
| `i` | Import TODO items |
| `b` | Backup operations |
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

### Automatic Backups

**Your data is automatically protected** with intelligent backup functionality:

#### How Automatic Backups Work

The app creates automatic backups in the following situations:

1. **On Startup**: If no backup exists or the last backup is older than 24 hours
2. **After Many Operations**: Automatically after every 50 add/update/delete operations
3. **On Exit**: When you quit the app (if changes were made since last backup)

**Backup Location**: `~/.todo-tui-backups/`

**Backup Format**: `todo-backup-YYYYMMDD_HHMMSS.json`

#### Benefits of Automatic Backups

- ✅ **Zero effort required** - Backups happen automatically in the background
- ✅ **Protection against data loss** - Recover from accidental deletions or corruption
- ✅ **Version history** - Multiple timestamped backups let you go back in time
- ✅ **Performance friendly** - Backups are created intelligently, not after every single change
- ✅ **Non-intrusive** - Backup failures don't interrupt your workflow

#### Disabling Automatic Backups

If you prefer manual control, automatic backups can be disabled programmatically when creating a `TodoStorage` instance:

```python
storage = TodoStorage(auto_backup_enabled=False)
```

### Export and Import

#### Exporting TODOs

Press `e` to open the export dialog:

1. Enter the export path (e.g., `~/todos.json`, `~/todos.csv`)
2. Format is auto-detected from file extension
3. Press Enter or click "Export"

**Supported formats:**
- **JSON** (`.json`): Full data export with all metadata (IDs, timestamps, postpone dates)
- **CSV** (`.csv`): Spreadsheet-compatible format for Excel, Google Sheets, etc.
- **Markdown** (`.md`): Human-readable checklist format
- **HTML** (`.html`): Styled web page format

**Use cases:**
- Backup your data
- Share your task list with others
- Import into spreadsheet applications
- Generate documentation

#### Importing TODOs

Press `i` to open the import dialog:

1. Enter the import path (must be `.json`)
2. Choose import mode:
   - **Replace mode** (default): Replaces all existing todos
   - **Merge mode** (Ctrl+M): Adds imported todos, skipping duplicates
3. Press Enter or click "Import"

**Import modes:**
- **Replace**: Completely replaces your current todos with imported ones
- **Merge**: Adds imported todos to existing ones, using UUID-based deduplication

### Manual Backup and Restore

Press `b` to access backup operations:

#### Creating Manual Backups

- Select "Create Backup" to create a timestamped backup on-demand
- Use this before major changes or experiments
- Manual backups are saved to the same location as automatic backups

#### Listing Backups

- Select "List Backups" to view recent backups
- Shows the 5 most recent backups (both automatic and manual)
- Backups are sorted by creation time (newest first)

**Backup best practices:**
- Automatic backups handle day-to-day protection
- Create manual backups before major changes or experiments
- Keep important backups in cloud storage or external drives
- Old backups can be safely deleted to save space

### Archiving Completed TODOs

Press `a` to archive all completed todos:

- Moves completed todos to `~/.todo-tui-archive.json`
- Removes them from your active list
- Preserves all data for historical reference
- Improves performance with large todo lists

**When to archive:**
- After completing a major project
- Weekly or monthly cleanup
- When your list gets too long
- Before starting a new phase of work

## Data Storage

### Main Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. The data persists between sessions, so you can safely close and reopen the app without losing your tasks.

### Automatic Backups

Automatic backups are created regularly and stored in `~/.todo-tui-backups/`. Each backup is timestamped for easy identification. The app maintains multiple backup versions, allowing you to recover from mistakes or data corruption.

**Automatic backup schedule:**
- Daily (when you start the app after 24+ hours)
- After every 50 operations (add, update, delete)
- On app exit (if changes were made)

### Manual Backups

Manual backups can be created on-demand via the 'b' key and are stored in the same location as automatic backups.

### Archive

Completed todos can be archived to `~/.todo-tui-archive.json`, keeping your main list clean while preserving historical data.

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
│       └── storage.py        # Persistence layer with auto-backup
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_storage.py       # Storage tests (including auto-backup)
│   └── test_app.py           # App tests
├── examples/
│   ├── basic_usage.py        # Basic usage examples
│   └── export_backup_usage.py # Export & backup examples
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
python examples/export_backup_usage.py
```

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- Automatic backups are in `~/.todo-tui-backups/`
- If main file is corrupted, restore from the most recent backup
- Or delete it (you'll lose your TODOs) - the app will create a new file on next run

### Export/Import issues

- **Export fails**: Ensure the target directory exists and you have write permissions
- **Import fails**: Verify the file is valid JSON and follows the correct format
- **Merge not working**: Check that imported todos have unique IDs

### Backup issues

- Automatic backups are stored in `~/.todo-tui-backups/`
- Manual backups go to the same location
- Ensure you have write permissions to your home directory
- Old backups can be manually deleted to save space
- Backup failures are silent and won't interrupt normal operation

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
- [Textual Documentation](https://textual.textualize.io/) - Framework documentation

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral

## Roadmap

See [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for planned features and enhancements.

## Feature Highlights

### Export Formats Comparison

| Format | Use Case | Preserves Metadata | Human Readable |
|--------|----------|-------------------|----------------|
| JSON | Backup, data portability | ✅ Full | ❌ No |
| CSV | Spreadsheet import | ⚠️ Partial | ⚠️ Moderate |
| Markdown | Documentation, sharing | ❌ Minimal | ✅ Yes |
| HTML | Web publishing | ⚠️ Partial | ✅ Yes |

### Data Safety Features

1. **Automatic Backups**: Background backups created daily, after many operations, and on exit
2. **Manual Backups**: Create backups on-demand before major changes
3. **Archive System**: Preserve completed tasks without cluttering your active list
4. **Import/Export**: Move data between devices or users
5. **Corruption Recovery**: Restore from automatic or manual backups if main storage is corrupted

### Backup System Comparison

| Feature | Automatic Backups | Manual Backups |
|---------|------------------|----------------|
| Frequency | Daily + every 50 ops + on exit | On-demand (via 'b' key) |
| User Action Required | None | User presses 'b' → Create Backup |
| Use Case | Day-to-day protection | Before major changes |
| Storage Location | ~/.todo-tui-backups/ | ~/.todo-tui-backups/ |
| Can be Disabled | Yes (programmatically) | Always available |

### Performance Tips

- Archive completed todos regularly to keep your list fast
- Use export to clean up old data while keeping a backup
- Merge mode import is slower than replace mode for large datasets
- Automatic backups are optimized to minimize performance impact
- Old backups can be safely deleted to save disk space
