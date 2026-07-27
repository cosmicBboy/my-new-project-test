# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- ⌨️ Keyboard-driven interface with **customizable key bindings**
- 🎨 Clean, modern TUI design
- 🚀 Fast and lightweight
- ❓ Interactive help system with searchable keyboard shortcuts
- 📄 Export shortcuts reference to Markdown
- 🎓 **In-app tutorial for new users**
- ⚙️ **Customizable settings** with persistent storage

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

On first launch, you'll see an interactive tutorial that walks you through all the features!

### Keyboard Shortcuts

The app uses intuitive keyboard shortcuts (which you can customize!):

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through TODO items |
| `Tab` | Switch between list and input field |
| `Enter` | Add new TODO (when in input field) |
| `Space` | Toggle TODO completion status |
| `p` | Postpone selected TODO until tomorrow |
| `d` | Delete selected TODO |
| `?` | Show keyboard shortcuts help (with search!) |
| `q` | Quit application |

#### Help Dialog Shortcuts

When the help dialog is open (`?`):

| Key | Action |
|-----|--------|
| `/` | Focus search box to filter shortcuts |
| `Ctrl+E` | Export shortcuts to Markdown file |
| `Esc` | Close help dialog |

> **Tip**: Press `?` anytime to open the interactive help dialog. You can search shortcuts using `/`, and even export them to a Markdown file for reference!

### Customizable Key Bindings

**NEW!** You can now customize keyboard shortcuts to match your preferences:

1. Key bindings are automatically saved to `~/.todo-tui-keybindings.json`
2. Customize bindings programmatically (see examples below)
3. Reset to defaults anytime
4. All customizations persist across app restarts

### Tutorial for New Users

**NEW!** First-time users are greeted with an interactive tutorial that covers:

- 📝 Adding and managing tasks
- ✓ Marking tasks as complete
- ⏰ Postponing tasks
- ❓ Using the help system
- 💡 Pro tips for power users

The tutorial only shows once. To see it again, delete `~/.todo-tui-tutorial-shown`.

### Basic Workflow

1. **First Run**: Follow the interactive tutorial to learn the basics
2. **Add a TODO**: Press `Tab` to focus the input field, type your task, and press `Enter`
3. **Complete a TODO**: Navigate to the item and press `Space`
4. **Postpone a TODO**: Navigate to the item and press `p` to postpone it until tomorrow
5. **Delete a TODO**: Navigate to the item and press `d`
6. **Get Help**: Press `?` to view all keyboard shortcuts with descriptions
7. **Customize**: Modify key bindings to suit your workflow
8. **Exit**: Press `q` to quit (your data is automatically saved)

### Help System

The app includes a comprehensive help system accessible by pressing `?`:

- **Searchable Shortcuts**: Press `/` or type in the search box to filter shortcuts by key, action, or description
- **Categorized Reference**: Shortcuts organized by category (Navigation, Task Management, etc.)
- **Export to File**: Press `Ctrl+E` in the help dialog to export all shortcuts to `~/todo-tui-shortcuts.md`
- **Print-Friendly**: The exported Markdown file is formatted for easy printing or sharing
- **Shows Custom Bindings**: The help system reflects your customized key bindings

### Postponing TODOs

The postpone feature allows you to defer tasks until tomorrow:

- Press `p` on any TODO item to postpone it until tomorrow
- Postponed items are displayed with a `[postponed until YYYY-MM-DD]` indicator
- Postponed items remain visible in the list with an italic style
- Pressing `p` multiple times keeps the postpone date as tomorrow (it doesn't advance further)
- Postponed items automatically become active again after the postpone date passes

## Data Storage

- **TODO items**: Automatically saved to `~/.todo-tui.json`
- **Key bindings**: Saved to `~/.todo-tui-keybindings.json`
- **Tutorial flag**: `~/.todo-tui-tutorial-shown` (tracks first run)

All data persists between sessions, so you can safely close and reopen the app.

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

Run specific test files:

```bash
uv run pytest tests/test_keybindings.py
uv run pytest tests/test_tutorial.py
uv run pytest tests/test_settings_dialog.py
```

### Project Structure

```
todo-tui/
├── src/
│   └── todo_tui/
│       ├── __init__.py           # Package initialization
│       ├── app.py                # Main Textual application
│       ├── models.py             # Data models (TodoItem)
│       ├── storage.py            # Persistence layer
│       ├── keybindings.py        # Key bindings management
│       ├── help_dialog.py        # Keyboard shortcuts help dialog
│       ├── tutorial.py           # Tutorial screen for new users
│       └── settings_dialog.py    # Settings dialog for customization
├── tests/
│   ├── test_models.py            # Model tests
│   ├── test_storage.py           # Storage tests
│   ├── test_app.py               # App tests
│   ├── test_help_dialog.py       # Help dialog tests
│   ├── test_keybindings.py       # Key bindings tests
│   ├── test_tutorial.py          # Tutorial tests
│   └── test_settings_dialog.py   # Settings dialog tests
├── examples/
│   ├── basic_usage.py            # Basic usage examples
│   ├── advanced_usage.py         # Advanced usage examples
│   ├── help_system_demo.py       # Help system demonstration
│   └── custom_keybindings.py     # Key binding customization examples
├── pyproject.toml                # Project configuration
├── README.md                     # This file
└── SPEC.md                       # Design specification
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
python examples/advanced_usage.py
python examples/help_system_demo.py
python examples/custom_keybindings.py
```

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- If corrupted, you can delete it (you'll lose your TODOs)
- The app will create a new file on next run

### Key binding issues

- Key bindings are stored in `~/.todo-tui-keybindings.json`
- Delete this file to reset to defaults
- See `examples/custom_keybindings.py` for customization examples

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters

### Tutorial not showing

- The tutorial only shows on first launch
- Delete `~/.todo-tui-tutorial-shown` to see it again
- Or run `python examples/custom_keybindings.py` to see tutorial demo

### Help system not showing

- Ensure you're pressing `Shift+/` (question mark) to open help
- Try pressing `?` with or without Shift depending on your keyboard layout
- The help dialog opens as a modal overlay
- Press `/` inside the help dialog to search for shortcuts
- Press `Ctrl+E` inside the help dialog to export shortcuts

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
- Keyboard Shortcuts - Press `?` in the app or export to Markdown

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral

## Roadmap

See [SPEC.md](SPEC.md) and [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for planned features and enhancements.

## Recent Updates

### Version 2.0 - Keyboard Shortcuts Reference

- ✨ **Interactive Tutorial**: New users get a guided tour
- ⌨️ **Customizable Key Bindings**: Personalize shortcuts to your liking
- 💾 **Persistent Settings**: All customizations save automatically
- 📖 **Enhanced Help System**: Now shows your custom bindings
- 🔍 **Searchable Shortcuts**: Find any command instantly
- 📄 **Export Reference**: Create printable cheat sheets
