# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- ⌨️ Keyboard-driven interface
- 🎨 Clean, modern TUI design
- 🚀 Fast and lightweight
- ❓ Interactive keyboard shortcuts help (press `?`)
- 🎓 Built-in tutorial for new users
- ⚙️ Customizable key bindings with persistence
- 📄 Export keyboard shortcuts cheat sheet

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

### First-Time Setup

When you run the app for the first time, you'll see an interactive tutorial that walks you through the basic features. You can:

- Skip the tutorial by pressing `Escape`
- View it again anytime by pressing `Ctrl+T`

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through TODO items |
| `Tab` | Switch between list and input field |
| `Enter` | Add new TODO (when in input field) |
| `Space` | Toggle TODO completion status |
| `p` | Postpone selected TODO until tomorrow |
| `d` | Delete selected TODO |
| `?` | Show keyboard shortcuts help |
| `Ctrl+T` | Show welcome tutorial |
| `Ctrl+K` | View current key bindings |
| `Ctrl+H` | Export shortcuts cheat sheet |
| `q` | Quit application |

**💡 Tips**: 
- Press `?` at any time to see an interactive keyboard shortcuts reference with search functionality!
- Press `Ctrl+H` to export a print-friendly cheat sheet to `~/todo-tui-shortcuts.txt`
- Customize key bindings by editing `~/.todo-tui-keybindings.json`

### Basic Workflow

1. **First Launch**: Review the welcome tutorial to learn the basics
2. **Add a TODO**: Press `Tab` to focus the input field, type your task, and press `Enter`
3. **Complete a TODO**: Navigate to the item and press `Space`
4. **Postpone a TODO**: Navigate to the item and press `p` to postpone it until tomorrow
5. **Delete a TODO**: Navigate to the item and press `d`
6. **Get Help**: Press `?` to view all keyboard shortcuts and search for specific commands
7. **Exit**: Press `q` to quit (your data is automatically saved)

### Keyboard Shortcuts Help

The app includes an interactive help overlay that can be accessed by pressing `?`:

- **Search**: Type to filter shortcuts by key or description
- **Browse**: Shortcuts are organized by category for easy navigation
- **Close**: Press `Escape`, `q`, or `?` again to close the help overlay

This feature makes it easy to discover and learn all available keyboard shortcuts without leaving the app or consulting external documentation.

### Customizing Key Bindings

You can customize keyboard shortcuts to match your preferences:

1. **View Current Bindings**: Press `Ctrl+K` to see all current key bindings
2. **Edit Configuration**: Manually edit `~/.todo-tui-keybindings.json`
3. **Example Configuration**:
   ```json
   {
     "quit": "ctrl+q",
     "toggle_todo": "t",
     "delete_todo": "x",
     "postpone_todo": "s",
     "show_shortcuts": "h",
     "export_cheatsheet": "ctrl+e",
     "customize_keys": "ctrl+k",
     "show_tutorial": "ctrl+t"
   }
   ```
4. **Reset to Defaults**: Delete the config file to restore default bindings

Your custom bindings are automatically reflected in:
- The interactive help overlay (`?`)
- The exported cheat sheet (`Ctrl+H`)
- The footer bar

### Exporting Keyboard Shortcuts

Create a print-friendly cheat sheet of all keyboard shortcuts:

1. Press `Ctrl+H` in the app
2. A text file is created at `~/todo-tui-shortcuts.txt`
3. Open and print the file for offline reference

The exported cheat sheet includes:
- All keyboard shortcuts organized by category
- Your current custom key bindings
- Configuration file locations
- Instructions for customization

### Postponing TODOs

The postpone feature allows you to defer tasks until tomorrow:

- Press `p` on any TODO item to postpone it until tomorrow
- Postponed items are displayed with a `[postponed until YYYY-MM-DD]` indicator
- Postponed items remain visible in the list with an italic style
- Pressing `p` multiple times keeps the postpone date as tomorrow (it doesn't advance further)
- Postponed items automatically become active again after the postpone date passes

## Data Storage

The app uses several files for data persistence:

- **TODOs**: `~/.todo-tui.json` - Your TODO items
- **Key Bindings**: `~/.todo-tui-keybindings.json` - Custom keyboard shortcuts
- **App Config**: `~/.todo-tui-config.json` - Application settings (tutorial status, etc.)

All data persists between sessions, so you can safely close and reopen the app without losing anything.

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
│       ├── storage.py        # Persistence layer
│       └── config.py         # Configuration management
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_storage.py       # Storage tests
│   ├── test_app.py           # App tests
│   └── test_config.py        # Config tests
├── examples/
│   ├── basic_usage.py        # Basic usage examples
│   ├── advanced_usage.py     # Advanced usage examples
│   └── keyboard_shortcuts_demo.py  # Shortcuts feature demo
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
python examples/advanced_usage.py
python examples/keyboard_shortcuts_demo.py
```

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- If corrupted, you can delete it (you'll lose your TODOs)
- The app will create a new file on next run

### Key bindings not working

- Check your custom bindings file: `~/.todo-tui-keybindings.json`
- Ensure the JSON syntax is valid
- Delete the file to reset to defaults
- Press `Ctrl+K` to view current bindings

### Tutorial not showing

- Delete `~/.todo-tui-config.json` to reset first-run status
- Or press `Ctrl+T` to manually show the tutorial

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
- [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) - Future enhancements roadmap
- [Textual Documentation](https://textual.textualize.io/) - Framework documentation

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral

## Roadmap

See [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for planned features and enhancements.

---

## Quick Reference

### Essential Commands
- **Add TODO**: `Tab` → type → `Enter`
- **Complete**: `Space`
- **Delete**: `d`
- **Help**: `?`
- **Tutorial**: `Ctrl+T`
- **Quit**: `q`

### Files
- TODOs: `~/.todo-tui.json`
- Key Bindings: `~/.todo-tui-keybindings.json`
- Config: `~/.todo-tui-config.json`
- Exported Cheat Sheet: `~/todo-tui-shortcuts.txt`
