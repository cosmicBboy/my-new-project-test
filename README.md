# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 💾 Automatic persistence (data saved between sessions)
- ⌨️ Keyboard-driven interface
- 🎨 Customizable themes with 5 built-in presets
- 🔤 Adjustable font sizes (small, medium, large)
- 📐 Layout options (compact, comfortable, spacious)
- ♿ High contrast mode for accessibility
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

#### Basic Operations
| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through TODO items |
| `Tab` | Switch between list and input field |
| `Enter` | Add new TODO (when in input field) |
| `Space` | Toggle TODO completion status |
| `p` | Postpone selected TODO until tomorrow |
| `d` | Delete selected TODO |
| `q` | Quit application |

#### Customization
| Key | Action |
|-----|--------|
| `t` | Cycle through themes |
| `f` | Cycle through font sizes |
| `l` | Cycle through layout spacing |

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

## Themes

The app includes 5 beautiful built-in themes that you can switch between instantly:

### Available Themes

1. **Cyberpunk** (Default) - Neon colors with hot pink, cyan, and purple accents
2. **Dark** - Professional dark theme with soft, muted colors
3. **Light** - Clean light theme perfect for bright environments
4. **High Contrast** - Maximum contrast with pure black/white for accessibility
5. **Colorful** - Vibrant theme with gradients and pastel accents

### Theme Customization

- Press `t` to cycle through themes
- Press `f` to cycle through font sizes (small, medium, large)
- Press `l` to cycle through layouts (compact, comfortable, spacious)
- Your preferences are automatically saved and restored on next launch

### Theme Examples

**Dark Theme**: Professional and easy on the eyes
```
Background: #1e1e1e | Foreground: #d4d4d4
Perfect for long coding sessions
```

**Light Theme**: Clean and bright
```
Background: #ffffff | Foreground: #24292f
Ideal for well-lit environments
```

**High Contrast**: Maximum visibility
```
Background: #000000 | Foreground: #ffffff
Designed for accessibility and outdoor use
```

## Data Storage

### TODO Items
TODO items are automatically saved to `~/.todo-tui.json` in your home directory. The data persists between sessions, so you can safely close and reopen the app without losing your tasks.

### Theme Preferences
Theme and customization preferences are saved to `~/.todo-tui-config.json`. This includes:
- Selected theme preset
- Font size preference
- Layout spacing preference

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
│       ├── themes.py         # Theme system and presets
│       └── config.py         # Configuration management
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_storage.py       # Storage tests
│   ├── test_app.py           # App tests
│   ├── test_themes.py        # Theme tests
│   └── test_config.py        # Config tests
├── examples/
│   ├── basic_usage.py        # Basic usage examples
│   ├── advanced_usage.py     # Advanced features
│   └── theme_usage.py        # Theme customization examples
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
# Basic usage and models
python examples/basic_usage.py

# Theme customization
python examples/theme_usage.py

# Advanced features
python examples/advanced_usage.py
```

## Accessibility

The app is designed with accessibility in mind:

- **High Contrast Theme**: Pure black and white colors for maximum visibility
- **Keyboard-Only Navigation**: No mouse required
- **Clear Visual Indicators**: Status symbols and color coding
- **Adjustable Layouts**: Choose spacing that works for you
- **Screen Reader Compatible**: Textual framework supports screen readers

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- TODO data file: `~/.todo-tui.json`
- Config file: `~/.todo-tui-config.json`
- If corrupted, you can delete them (you'll lose your data/preferences)
- The app will create new files on next run

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters
- Some themes may look different depending on terminal color support

### Theme not displaying correctly

- Some terminal emulators have limited color support
- Try the High Contrast theme if colors aren't showing
- Modern terminals like iTerm2, Windows Terminal, or Alacritty work best

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure tests pass: `uv run pytest`
5. Submit a pull request

## Documentation

- [SPEC.md](SPEC.md) - Detailed design decisions and specifications
- [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) - Feature roadmap
- [Textual Documentation](https://textual.textualize.io/) - Framework documentation

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral
- Theme system inspired by popular code editors and terminals

## Roadmap

See [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for planned features and enhancements, including:

- ✅ **Customizable Themes** (Completed in Phase 4)
- Tags and categories
- Priority levels
- Due dates and time tracking
- Advanced search and filtering
- And much more!

## Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the examples in the `examples/` directory
3. Open an issue on GitHub with details about your environment and the problem
