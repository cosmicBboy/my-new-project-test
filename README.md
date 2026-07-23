# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- ⌨️ Comprehensive keyboard shortcuts system with 5 powerful features:
  - **Contextual help overlay** - Press `?` for instant access to all shortcuts
  - **Searchable shortcuts** - Find any command quickly with built-in search
  - **Customizable key bindings** - Personalize shortcuts to match your workflow
  - **Print-friendly cheat sheet** - Export shortcuts for offline reference
  - **In-app tutorial** - Interactive guide for first-time users
- 🎨 Clean, modern TUI design with neon cyberpunk theme
- 🚀 Fast and lightweight
- 📋 Export/Import functionality (JSON, CSV, Markdown)

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

On first launch, an interactive tutorial will guide you through the basics!

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through TODO items |
| `Tab` | Switch between list and input field |
| `Enter` | Add new TODO (when in input field) |
| `Space` | Toggle TODO completion status |
| `p` | Postpone selected TODO until tomorrow |
| `d` | Delete selected TODO |
| `?` | Show keyboard shortcuts reference (with search!) |
| `Ctrl+T` | Show interactive tutorial |
| `Ctrl+E` | Export todos |
| `Ctrl+I` | Import todos |
| `q` | Quit application |

**Tip**: Press `?` at any time to see the full keyboard shortcuts reference with search functionality!

### 🎓 Interactive Tutorial

First-time users will automatically see an interactive tutorial when launching the app. The tutorial covers:

- Adding your first TODO
- Managing tasks (complete, delete, postpone)
- Essential keyboard shortcuts
- Pro tips for productivity

You can access the tutorial anytime by pressing `Ctrl+T`.

### ⌨️ Keyboard Shortcuts Reference (Feature Highlight!)

Press `?` at any time to open the comprehensive keyboard shortcuts overlay. This feature includes:

#### 1. Contextual Help Overlay
- Beautiful modal overlay with organized sections
- Categories: Navigation, Todo Management, Data Operations, Application
- Helpful tips and best practices included
- Close with `ESC`, `q`, or `?`

#### 2. Searchable Shortcuts
- Type in the search box to instantly find any shortcut
- Search by action name, key, or description
- Real-time filtering as you type
- Clear results highlighting

#### 3. Customizable Key Bindings
- Personalize any keyboard shortcut to your preference
- Key bindings are saved automatically
- Reset to defaults anytime
- Changes persist across sessions

#### 4. Print-Friendly Cheat Sheet
- Export all shortcuts to a text file with one click
- Clean, readable format perfect for printing
- Includes all categories and tips
- Saved to `~/todo-tui-shortcuts.txt`

#### 5. First-Run Tutorial
- Interactive guide for new users
- Step-by-step instructions
- "Don't show again" option
- Can be reopened anytime with `Ctrl+T`

### Basic Workflow

1. **Add a TODO**: Press `Tab` to focus the input field, type your task, and press `Enter`
2. **Complete a TODO**: Navigate to the item and press `Space`
3. **Postpone a TODO**: Navigate to the item and press `p` to postpone it until tomorrow
4. **Delete a TODO**: Navigate to the item and press `d`
5. **Get Help**: Press `?` to see all keyboard shortcuts with search
6. **Learn More**: Press `Ctrl+T` for the interactive tutorial
7. **Export Cheat Sheet**: Open shortcuts (`?`) and click "Export Cheat Sheet"
8. **Exit**: Press `q` to quit (your data is automatically saved)

### Advanced Features

#### Searchable Shortcuts

When you press `?` to open the shortcuts reference:
1. Focus the search box at the top
2. Type your query (e.g., "delete", "postpone", "space")
3. Results update instantly as you type
4. Search matches action names, keys, and descriptions
5. Clear the search to see all shortcuts again

Example searches:
- `toggle` - Find the toggle completion shortcut
- `space` - See what the space key does
- `export` - Find data export commands
- `Navigation` - See all navigation-related shortcuts

#### Customizing Key Bindings

1. Press `?` to open shortcuts reference
2. Click "Customize Bindings" button
3. Select the action you want to rebind
4. Press the new key you want to use
5. Changes are saved automatically
6. Click "Reset to Defaults" to restore original bindings

Key bindings are stored in `~/.todo-tui-keybindings.json`

#### Exporting Cheat Sheet

1. Press `?` to open shortcuts reference
2. Click "Export Cheat Sheet" button
3. File is saved to `~/todo-tui-shortcuts.txt`
4. Open the file for a print-friendly reference

The cheat sheet includes:
- All keyboard shortcuts organized by category
- Clear formatting for easy reading
- Tips and best practices
- Perfect for printing or offline reference

### Postponing TODOs

The postpone feature allows you to defer tasks until tomorrow:

- Press `p` on any TODO item to postpone it until tomorrow
- Postponed items are displayed with a `[postponed until YYYY-MM-DD]` indicator
- Postponed items remain visible in the list with italic styling
- Pressing `p` multiple times keeps the postpone date as tomorrow (it doesn't advance further)
- Postponed items automatically become active again after the postpone date passes

## Data Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. The data persists between sessions, so you can safely close and reopen the app without losing your tasks.

Configuration files:
- `~/.todo-tui.json` - Your TODO items
- `~/.todo-tui-keybindings.json` - Custom key bindings
- `~/.todo-tui-tutorial-seen` - Tutorial completion marker

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

### Test Coverage

The project includes comprehensive tests for all features:
- Core TODO functionality
- Keyboard shortcuts reference with search
- Customizable key bindings
- Cheat sheet export
- Interactive tutorial
- UI interactions and workflows

### Project Structure

```
todo-tui/
├── src/
│   └── todo_tui/
│       ├── __init__.py       # Package initialization
│       ├── app.py            # Main Textual application
│       ├── models.py         # Data models (TodoItem)
│       ├── storage.py        # Persistence layer
│       └── keybindings.py    # Keyboard bindings management
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_storage.py       # Storage tests
│   ├── test_app.py           # App and UI tests
│   └── test_keybindings.py   # Key bindings tests
├── examples/
│   ├── basic_usage.py        # Basic usage examples
│   ├── advanced_usage.py     # Advanced features demo
│   └── shortcuts_demo.py     # Shortcuts feature demo
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
python examples/shortcuts_demo.py
```

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- The data file is located at `~/.todo-tui.json`
- If corrupted, you can delete it (you'll lose your TODOs)
- The app will create a new file on next run

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters

### Keyboard shortcuts not working

- Check your custom bindings: `cat ~/.todo-tui-keybindings.json`
- Reset to defaults: Open shortcuts (`?`) and click "Reset to Defaults"
- Some terminals may intercept certain key combinations

### Tutorial not showing on first run

- Delete the marker file: `rm ~/.todo-tui-tutorial-seen`
- Restart the app to see the tutorial again
- Or press `Ctrl+T` to open it manually

### Need help with keyboard shortcuts?

- Press `?` inside the app to see the complete keyboard shortcuts reference
- Use the search box to quickly find any shortcut
- Export a cheat sheet for offline reference
- The help screen shows all available commands organized by category

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
- Built-in help: Press `?` in the app for keyboard shortcuts
- Tutorial: Press `Ctrl+T` for interactive guide

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral

## Roadmap

This project implements several features from the [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md):

### ✅ Implemented (Phase 4: Polish and Ecosystem)
- **Keyboard Shortcuts Reference** (Issue #34) - All 5 features complete:
  - ✅ Contextual help overlay (`?` key)
  - ✅ Searchable keyboard shortcuts
  - ✅ Customizable key bindings
  - ✅ Print-friendly shortcuts cheat sheet
  - ✅ In-app tutorial for new users

### 🔜 Coming Soon
- Custom themes and color schemes
- Smart notifications and reminders
- Enhanced export/backup features
- Basic integrations (GitHub, Calendar)

See [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for the complete feature roadmap.

## Success Criteria (Issue #34)

All 5 success criteria are met:

- ✅ **Help overlay displays correctly** - Beautiful modal with organized sections
- ✅ **All shortcuts are documented** - Complete reference with categories and tips
- ✅ **Search works for finding shortcuts** - Real-time search with instant results
- ✅ **Customizable bindings save correctly** - Persistent JSON storage
- ✅ **Tutorial is helpful for new users** - Interactive guide with essential information

## Quick Reference Card

Print this for your desk:

```
TODO TUI - Quick Reference
==========================

Essential Shortcuts:
  ?        Help (with search!)
  Ctrl+T   Tutorial
  Tab      Switch focus
  Enter    Add TODO
  Space    Toggle complete
  p        Postpone
  d        Delete
  q        Quit

Data:
  Ctrl+E   Export
  Ctrl+I   Import

Features:
  • Auto-save to ~/.todo-tui.json
  • Search shortcuts with ?
  • Customize any key binding
  • Export cheat sheet for offline use
  • Interactive tutorial for beginners

Press ? anytime for full reference!
```
