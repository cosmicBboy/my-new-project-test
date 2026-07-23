# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- ⌨️ Keyboard-driven interface with **customizable key bindings**
- ❓ Built-in keyboard shortcuts reference (press `?`)
- 🔍 Searchable help overlay
- 📄 **Export print-friendly cheat sheets** (text and markdown)
- 🎓 **Interactive tutorial for new users**
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

### First Run Experience

When you first launch the app, you'll be greeted with an **interactive tutorial** that walks you through:
- Adding and managing tasks
- Navigating the interface
- Using keyboard shortcuts
- Customizing the app

You can skip the tutorial or replay it anytime by pressing `t`.

### Keyboard Shortcuts

Press `?` at any time to see the complete keyboard shortcuts reference with search functionality!

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through TODO items |
| `Tab` | Switch between list and input field |
| `Enter` | Add new TODO (when in input field) |
| `Space` | Toggle TODO completion status |
| `p` | Postpone selected TODO until tomorrow |
| `d` | Delete selected TODO |
| `?` | Show keyboard shortcuts reference |
| `c` | **Customize key bindings** |
| `x` | **Export shortcuts cheat sheet** |
| `t` | Show tutorial |
| `q` | Quit application |

### Customizing Key Bindings

The app allows you to customize keyboard shortcuts to match your preferences:

1. Press `c` to open the key bindings customization screen
2. Edit any key binding by typing in the input field
3. Use key names like: `q`, `space`, `ctrl+s`, `question_mark`, etc.
4. Click "Save Changes" to apply (requires app restart)
5. Click "Reset to Defaults" to restore original bindings

Your custom key bindings are saved to `~/.todo-tui-config.json`.

### Print-Friendly Cheat Sheet

Generate a reference document you can print or keep on hand:

1. Press `x` in the app to export cheat sheets
2. Two files are created in your home directory:
   - `todo-tui-shortcuts.txt` - Plain text format
   - `todo-tui-shortcuts.md` - Markdown format

These cheat sheets include all keyboard shortcuts organized by category, perfect for quick reference or sharing with others.

### Basic Workflow

1. **Add a TODO**: Press `Tab` to focus the input field, type your task, and press `Enter`
2. **Complete a TODO**: Navigate to the item and press `Space`
3. **Postpone a TODO**: Navigate to the item and press `p` to postpone it until tomorrow
4. **Delete a TODO**: Navigate to the item and press `d`
5. **Get Help**: Press `?` to see all keyboard shortcuts with search functionality
6. **Customize**: Press `c` to customize key bindings to your preference
7. **Exit**: Press `q` to quit (your data is automatically saved)

### Keyboard Shortcuts Reference

The app includes a comprehensive, searchable keyboard shortcuts reference that you can access at any time by pressing `?`. This help overlay features:

- **Contextual Help**: All available shortcuts organized by category (Navigation, Task Management, Application)
- **Search Functionality**: Type to filter shortcuts by key, action, description, or category
- **Easy Navigation**: Use `Tab` to move between elements, `Esc` or `q` to close
- **Visual Design**: Color-coded shortcuts matching the app's theme

The help overlay is designed to make learning the app intuitive and improve your productivity.

### Postponing TODOs

The postpone feature allows you to defer tasks until tomorrow:

- Press `p` on any TODO item to postpone it until tomorrow
- Postponed items are displayed with a `[postponed until YYYY-MM-DD]` indicator
- Postponed items remain visible in the list with an italic style
- Pressing `p` multiple times keeps the postpone date as tomorrow (it doesn't advance further)
- Postponed items automatically become active again after the postpone date passes

## Data Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. Configuration and custom key bindings are saved to `~/.todo-tui-config.json`. The data persists between sessions, so you can safely close and reopen the app without losing your tasks or settings.

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
│       ├── __init__.py         # Package initialization
│       ├── app.py              # Main Textual application
│       ├── models.py           # Data models (TodoItem)
│       ├── storage.py          # Persistence layer
│       ├── config.py           # Configuration management
│       ├── help_overlay.py     # Keyboard shortcuts reference
│       ├── tutorial.py         # Interactive tutorial
│       ├── keybindings.py      # Key binding customization
│       └── cheatsheet.py       # Cheat sheet generator
├── tests/
│   ├── test_models.py          # Model tests
│   ├── test_storage.py         # Storage tests
│   ├── test_app.py             # App tests
│   ├── test_config.py          # Configuration tests
│   ├── test_help_overlay.py    # Help overlay tests
│   ├── test_tutorial.py        # Tutorial tests
│   ├── test_keybindings.py     # Keybindings tests
│   └── test_cheatsheet.py      # Cheat sheet tests
├── examples/
│   ├── basic_usage.py          # Usage examples
│   ├── advanced_usage.py       # Advanced examples
│   └── help_system_demo.py     # Help system demo
├── pyproject.toml              # Project configuration
├── README.md                   # This file
└── SPEC.md                     # Design specification
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
```

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- Configuration file is at `~/.todo-tui-config.json`
- If corrupted, you can delete them (you'll lose your TODOs and settings)
- The app will create new files on next run

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters

### Help overlay not showing

- Make sure you're pressing `Shift+?` (the question mark key)
- If using a non-US keyboard layout, try the key that produces `?`
- The overlay should appear immediately when the key is pressed

### Custom key bindings not working

- Key bindings require an app restart to take effect
- Check `~/.todo-tui-config.json` for proper JSON syntax
- Use standard key names: `q`, `space`, `ctrl+s`, `question_mark`, etc.
- Click "Reset to Defaults" in the customization screen if needed

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure tests pass: `uv run pytest`
5. Submit a pull request

## Documentation

- [SPEC.md](SPEC.md) - Detailed design decisions and specifications
- [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) - Planned enhancements and features
- [Textual Documentation](https://textual.textualize.io/) - Framework documentation

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral

## Roadmap

See [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for planned features and enhancements, including:
- Tags and categories
- Priority levels
- Due dates
- Advanced search
- Pomodoro timer integration
- And much more!
