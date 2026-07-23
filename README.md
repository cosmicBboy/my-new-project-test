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
- ❓ Built-in keyboard shortcuts reference (press `?`)
- 📄 Export shortcuts as a print-friendly cheat sheet
- 🎓 Interactive tutorial for new users
- ⚙️ Fully customizable key bindings

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

### First-Time Experience

When you run the app for the first time, you'll see an interactive tutorial that guides you through the basic features. You can:
- Skip the tutorial and start using the app immediately
- Return to the tutorial anytime by pressing `Ctrl+T`

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through TODO items |
| `Tab` | Switch between list and input field |
| `Enter` | Add new TODO (when in input field) |
| `Space` | Toggle TODO completion status |
| `p` | Postpone selected TODO until tomorrow |
| `d` | Delete selected TODO |
| `?` | Show keyboard shortcuts reference |
| `c` | Customize key bindings |
| `Ctrl+E` | Export shortcuts cheat sheet |
| `Ctrl+T` | Show tutorial |
| `q` | Quit application |

**Note**: All keyboard shortcuts are customizable! Press `c` to configure your preferred key bindings.

### Keyboard Shortcuts Reference

The app includes a comprehensive help system accessible by pressing `?`:

#### Features:
- **Organized shortcuts**: All shortcuts grouped by category (Navigation, Task Management, Application, Tips)
- **Real-time search**: Type to filter shortcuts and quickly find what you need
- **Export functionality**: Click "Export Cheat Sheet" to save a print-friendly reference
- **Always up-to-date**: Shows your current key bindings (including customizations)
- **Easy to close**: Press `ESC`, `q`, or `?` again to close

### Customizing Key Bindings

Press `c` to open the key bindings customization screen:

1. **View current bindings**: See all actions and their assigned keys
2. **Modify bindings**: Click on an input field and type your desired key, then press Enter
   - Use standard key names like `space`, `ctrl+e`, `shift+a`, etc.
   - Changes are saved when you press Enter or close the screen
3. **Reset to defaults**: Click "Reset to Defaults" to restore original bindings
4. **Close**: Click "Close" or press `ESC` when done

Your custom bindings are saved to `~/.todo-tui-config.json` and persist across sessions.

### Exporting Shortcuts Cheat Sheet

Need a quick reference or want to print the shortcuts?

1. **From help screen**: Press `?`, then click "Export Cheat Sheet"
2. **Direct export**: Press `Ctrl+E` anytime
3. **File location**: Shortcuts are saved to `~/todo-tui-shortcuts.txt`
4. **Print-friendly**: Plain text format, organized by category, ready to print

The cheat sheet includes all current bindings (including your customizations) and tips for using the app.

### Tutorial

The interactive tutorial helps you get started:

- **First time**: Automatically shown when you first run the app
- **Anytime access**: Press `Ctrl+T` to show the tutorial again
- **Covers**: Adding tasks, managing tasks, essential shortcuts, and pro tips
- **Quick start**: Step-by-step guide with examples

### Basic Workflow

1. **Add a TODO**: Press `Tab` to focus the input field, type your task, and press `Enter`
2. **Complete a TODO**: Navigate to the item and press `Space`
3. **Postpone a TODO**: Navigate to the item and press `p` to postpone it until tomorrow
4. **Delete a TODO**: Navigate to the item and press `d`
5. **Get Help**: Press `?` to see all keyboard shortcuts with search
6. **Customize Keys**: Press `c` to configure your preferred bindings
7. **Export Shortcuts**: Press `Ctrl+E` to save a cheat sheet
8. **Exit**: Press `q` to quit (your data is automatically saved)

### Postponing TODOs

The postpone feature allows you to defer tasks until tomorrow:

- Press `p` on any TODO item to postpone it until tomorrow
- Postponed items are displayed with a `[postponed until YYYY-MM-DD]` indicator
- Postponed items remain visible in the list with an italic, yellow style
- Pressing `p` multiple times keeps the postpone date as tomorrow (it doesn't advance further)
- Postponed items automatically become active again after the postpone date passes

## Data Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. Configuration (including custom key bindings and tutorial status) is saved to `~/.todo-tui-config.json`. All data persists between sessions, so you can safely close and reopen the app without losing anything.

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
│   ├── basic_usage.py        # Basic usage example
│   └── help_usage.py         # Help feature demo
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
python examples/help_usage.py
```

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- The config file is located at `~/.todo-tui-config.json`
- If corrupted, you can delete them (you'll lose your TODOs and settings)
- The app will create new files on next run

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters

### Key binding conflicts

- If a key binding doesn't work, it might conflict with your terminal
- Press `c` to customize the binding to a different key
- Press "Reset to Defaults" in the customize screen if needed

### Need help?

- Press `?` inside the app to see all available shortcuts
- Press `Ctrl+T` to see the tutorial again
- Use the search feature in help to quickly find specific commands
- Export a cheat sheet with `Ctrl+E` for quick reference

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

See [SPEC.md](SPEC.md) for planned features and enhancements.

---

**Quick Win Feature**: This comprehensive keyboard shortcuts reference system was identified as a "Quick Win" in the improvements proposal - providing immediate value with relatively low implementation complexity.
