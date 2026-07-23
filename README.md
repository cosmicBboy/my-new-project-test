# TODO TUI App

A simple, interactive TODO list application with a Text User Interface (TUI) built using Python and the [Textual](https://textual.textualize.io/) framework.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📝 Add, complete, and delete TODO items
- ⏰ Postpone TODO items until tomorrow
- 🎨 **Customizable themes** (4 built-in + custom theme creation)
- 📐 **Layout density options** (compact, comfortable, spacious)
- 🔤 **Font size adjustment** (small, medium, large)
- ⚡ **Instant customization** - all changes apply immediately, no restart needed!
- 💾 Automatic persistence (data and preferences saved between sessions)
- ⌨️ Keyboard-driven interface
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

#### Customization (All apply instantly!)
| Key | Action |
|-----|--------|
| `t` | Cycle through themes |
| `l` | Cycle through layout densities |
| `f` | Cycle through font sizes |

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

### Customizing the Appearance

#### Themes

The app includes four built-in themes that you can cycle through by pressing `t`:

1. **Dark** (Catppuccin Mocha)
   - Soft, warm dark theme with muted colors
   - Easy on the eyes for long sessions
   - Great for low-light environments

2. **Light** (Catppuccin Latte)
   - Clean, bright theme for daytime use
   - High readability in well-lit rooms
   - Professional appearance

3. **High Contrast**
   - Maximum contrast for accessibility
   - Black and white design
   - Excellent for users with visual impairments
   - Clear yellow focus indicators

4. **Colorful** (Cyberpunk) - *Default*
   - Vibrant neon colors with gradients
   - Futuristic aesthetic
   - High visual impact

**✨ NEW**: Theme changes now apply **instantly** - no restart needed!

#### Creating Custom Themes

You can create your own custom themes programmatically:

```python
from todo_tui.themes import create_custom_theme
from todo_tui.storage import PreferencesStorage

# Create a custom theme
my_theme = create_custom_theme(
    name="my_ocean",
    display_name="Ocean Theme",
    colors={
        "background": "#1a1d29",
        "surface": "#252936",
        "text": "#e0e0e0",
        "text_dim": "#707070",
        "accent": "#4a9eff",
        "border": "#3a3d49",
        "completed": "#909090",
        "postponed": "#ffaa00",
    }
)

# Save it to preferences
prefs = PreferencesStorage()
prefs.add_custom_theme({
    "name": my_theme.name,
    "display_name": my_theme.display_name,
    "colors": {
        "background": "#1a1d29",
        "surface": "#252936",
        "text": "#e0e0e0",
        "accent": "#4a9eff",
        # ... other colors
    }
})
```

Your custom themes will then be available in the theme cycle (press `t`) along with the built-in themes.

#### Layout Density

Adjust the spacing of UI elements by pressing `l`:

- **Compact**: Minimal spacing, more items visible
- **Comfortable**: Balanced spacing (default)
- **Spacious**: Maximum spacing, easier to read

Layout changes take effect **immediately**.

#### Font Size

Cycle through font size options by pressing `f`:

- **Small**: Compact text, more content visible
- **Medium**: Standard size (default)
- **Large**: Larger text for better readability

**✨ NEW**: Font size changes now apply **instantly** - no restart needed!

#### Preference Persistence

All your customization preferences are automatically saved to `~/.todo-tui-preferences.json` and persist across sessions:
- Current theme selection
- Layout density
- Font size
- Custom themes you've created

## Data Storage

TODO items are automatically saved to `~/.todo-tui.json` in your home directory. The data persists between sessions, so you can safely close and reopen the app without losing your tasks.

User preferences (theme, layout, font size, custom themes) are saved to `~/.todo-tui-preferences.json`.

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
│       └── themes.py         # Theme definitions & custom theme creation
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_storage.py       # Storage tests
│   ├── test_app.py           # App tests
│   └── test_themes.py        # Theme tests
├── examples/
│   ├── basic_usage.py        # Basic usage examples
│   └── themes_demo.py        # Theme customization demo
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
# Basic usage example
python examples/basic_usage.py

# Theme customization demo (including custom theme creation)
python examples/themes_demo.py
```

## Accessibility

The app is designed with accessibility in mind:

- **Keyboard-only navigation**: No mouse required
- **High contrast theme**: Optimized for users with visual impairments
- **Customizable font sizes**: Adjust text size for better readability
- **Layout density options**: Choose spacing that works best for you
- **Screen reader friendly**: Works with terminal screen readers
- **Instant feedback**: All customization changes apply immediately

## What's New

### ✨ Version 2.0 - Enhanced Customization

- **Custom theme creation**: Design your own themes with custom color palettes
- **Instant theme switching**: Theme changes apply immediately without restart
- **Instant font size changes**: Font size adjustments apply immediately
- **Smooth transitions**: Seamless theme and font changes while using the app
- **Custom theme persistence**: Your custom themes are saved and reloaded

All customization features now provide instant visual feedback!

## Troubleshooting

### App won't start

- Ensure Python 3.11+ is installed: `python --version`
- Try reinstalling dependencies: `uv sync --reinstall`

### Data file issues

- TODO data is stored at `~/.todo-tui.json`
- Preferences are stored at `~/.todo-tui-preferences.json`
- If corrupted, you can delete these files (you'll lose your data)
- The app will create new files on next run

### Terminal display issues

- Ensure your terminal supports Unicode characters
- Try a different terminal emulator if problems persist
- Minimum terminal size: 80x24 characters
- Some themes use gradients which may not display correctly in all terminals

### Theme not applying

- Theme changes now apply instantly - no restart needed!
- Ensure you're using a terminal that supports 24-bit color (true color)
- Try a different theme if colors don't display correctly

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure tests pass: `uv run pytest`
5. Submit a pull request

## Documentation

- [SPEC.md](SPEC.md) - Detailed design decisions and specifications
- [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) - Planned enhancements
- [Textual Documentation](https://textual.textualize.io/) - Framework documentation

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Managed with [uv](https://github.com/astral-sh/uv) by Astral
- Dark and Light themes inspired by [Catppuccin](https://github.com/catppuccin/catppuccin)

## Roadmap

See [IMPROVEMENTS_PROPOSAL.md](IMPROVEMENTS_PROPOSAL.md) for planned features and enhancements.

---

**Latest**: 🎨 Create custom themes! Theme and font changes apply instantly! Press `t`, `l`, or `f` to try them out.
