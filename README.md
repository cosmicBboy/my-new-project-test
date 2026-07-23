# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- ⌨️ Keyboard-driven interface with fully customizable shortcuts
- ❓ Built-in keyboard shortcuts help (press `?`)
- 🔍 Searchable shortcuts reference
- 📄 Export printable cheat sheet
- 🎓 Interactive tutorial for new users
- ⚙️ Fully customizable key bindings with interactive editing
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

On first run, an interactive tutorial will guide you through the basics!

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
| `Ctrl+T` | Show interactive tutorial |
| `Ctrl+E` | Export printable cheat sheet |
| `Ctrl+K` | Customize key bindings |
| `q` | Quit application |

**Note:** All keyboard shortcuts are fully customizable! Press `Ctrl+K` and click "Edit" next to any action to change its key binding.

### Basic Workflow

1. **Add a TODO**: Press `Tab` to focus the input field, type your task, and press `Enter`
2. **Complete a TODO**: Navigate to the item and press `Space`
3. **Postpone a TODO**: Navigate to the item and press `p` to postpone it until tomorrow
4. **Delete a TODO**: Navigate to the item and press `d`
5. **Get Help**: Press `?` to view all keyboard shortcuts with search
6. **Exit**: Press `q` to quit (your data is automatically saved)

### Interactive Tutorial

First-time users will automatically see a comprehensive tutorial covering:

- Adding your first TODO
- Managing TODOs (complete, reopen, delete)
- Postponing tasks for later
- Using the help system
- Understanding data persistence

You can always access the tutorial again by pressing `Ctrl+T`.

### Keyboard Shortcuts Help

The app includes a comprehensive keyboard shortcuts help system:

- **Access**: Press `?` anywhere in the app to open the help dialog
- **Search**: Type in the search box to filter shortcuts by key or description
- **Navigate**: Use arrow keys or scroll through the shortcuts list
- **Export**: Press `Ctrl+E` to save a printable cheat sheet to your home directory
- **Close**: Press `Esc` or `q` to close the help dialog

The help dialog organizes shortcuts into categories:
- **Navigation**: Moving through the interface
- **TODO Management**: Creating, editing, and managing tasks
- **Help & Information**: Accessing help and documentation
- **Application**: App-level controls

### Customizable Key Bindings

Personalize your workflow by customizing keyboard shortcuts:

1. Press `Ctrl+K` to open the key bindings dialog
2. Click "Edit" next to any action you want to customize
3. Press the new key you want to use for that action
4. The binding is saved automatically and takes effect immediately
5. Press "Reset to Defaults" to restore original key bindings
6. All changes are persisted to `~/.todo-tui-keys.json`

**Features:**
- **Interactive Editing**: Click "Edit" and press your desired key
- **Visual Feedback**: Editing mode is clearly highlighted
- **Cancel Option**: Press `Esc` while editing to cancel
- **Instant Save**: Changes are automatically saved to disk
- **Reset Capability**: Easy return to default bindings

### Printable Cheat Sheet

Export a text file with all keyboard shortcuts:

1. Press `Ctrl+E` anywhere in the app
2. A file `todo-tui-shortcuts.txt` is saved to your home directory
3. Print or keep it handy for quick reference
4. Perfect for offline use or sharing with team members

### Postponing TODOs

The postpone feature allows you to defer tasks until tomorrow:

- Press `p` on any TODO item to postpone it until tomorrow
- Postponed items are displayed with a `[postponed until YYYY-MM-DD]` indicator
- Postponed items remain visible in the list with an italic style
- Pressing `p` multiple times keeps the postpone date as tomorrow (it doesn't advance further)
- Postponed items automatically become active again after the postpone date passes

## Data Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. Custom key bindings are saved to `~/.todo-tui-keys.json`. The data persists between sessions, so you can safely close and reopen the app without losing your tasks or preferences.

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
│       └── keybindings.py    # Key bindings management
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_storage.py       # Storage tests
│   ├── test_app.py           # App tests
│   └── test_keybindings.py   # Key bindings tests
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
python examples/keyboard_shortcuts_demo.py
```

## Feature Highlights

### 1. Comprehensive Help System

- **Contextual Help**: Press `?` for instant access to all shortcuts
- **Smart Search**: Find shortcuts by key name or function
- **Always Available**: Help is never more than one keypress away

### 2. Learning Made Easy

- **Interactive Tutorial**: Step-by-step guide for new users
- **Automatic on First Run**: Tutorial shows automatically
- **Re-accessible**: Press `Ctrl+T` to view tutorial again

### 3. Full Customization

- **Interactive Key Editing**: Click "Edit" and press your desired key
- **Instant Feedback**: Changes apply immediately
- **Persistent Settings**: All customizations saved automatically
- **Easy Reset**: One-click return to defaults
- **No Manual Config**: No need to edit JSON files manually

### 4. Export & Share

- **Printable Cheat Sheet**: Export shortcuts to text file
- **Offline Reference**: Keep cheat sheet handy without running the app
- **Team Sharing**: Share shortcuts with colleagues

### 5. Discoverability

All features are designed to be discoverable:
- Footer shows common shortcuts
- Help system is prominently featured
- Tutorial covers all major features
- Search makes finding specific shortcuts easy
- Interactive editing makes customization intuitive

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- The key bindings file is at `~/.todo-tui-keys.json`
- If corrupted, you can delete them (you'll lose your data/settings)
- The app will create new files on next run

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters

### Help dialog not appearing

- Ensure you're pressing `Shift + /` (which produces `?`)
- Try pressing it from different parts of the interface
- Check that your terminal properly handles the `?` key

### Custom key bindings not working

- Check `~/.todo-tui-keys.json` exists and is valid JSON
- Try resetting to defaults with `Ctrl+K` → "Reset to Defaults"
- Restart the app after changing bindings

### Can't customize a key binding

- Make sure you click the "Edit" button first
- When in edit mode, press the key you want to use
- Press `Esc` to cancel if you change your mind
- Some keys like `Enter` and `Tab` cannot be rebound

### Tutorial keeps appearing

- The tutorial shows only once (on first run)
- A marker file `~/.todo-tui-tutorial-shown` tracks this
- Delete this file to see the tutorial again

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

**Quick Start**: Run `uv run todo-tui` and follow the interactive tutorial! 🚀
