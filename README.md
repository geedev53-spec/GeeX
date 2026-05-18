# GeeX OS

> **The Futuristic Terminal Enhancement Framework for Android Termux**

Transform your Termux terminal into a next-generation cyberpunk command center with animated dashboards, smart prompts, AI assistance, and beautiful visual effects.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/geexos/GeeX-OS)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Termux](https://img.shields.io/badge/Termux-supported-orange.svg)](https://termux.dev)

---

## Features

- **Animated Startup** - BIOS-style boot sequence with cyberpunk loading
- **Interactive Dashboard** - Real-time system monitoring with CPU/RAM graphs
- **Smart Prompt** - Powerline-style prompt with git, battery, CPU, RAM info
- **6 Beautiful Themes** - Cyberpunk, Matrix, Ocean, Neon, Minimal, Hackerman
- **AI Assistant** - Smart command suggestions and contextual tips
- **Plugin System** - Extensible plugin architecture with 8 built-in plugins
- **System Monitor** - Live CPU, memory, storage, battery, network monitoring
- **Benchmark** - Device performance testing
- **Terminal Effects** - Matrix rain, glitch effects, neon glow, scanlines
- **Auto-Completion** - Smart command completion
- **Full Uninstall** - Clean removal with backup restore
- **Auto-Update** - Check and install updates from GitHub

---

## Quick Install (Termux)

```bash
# Install dependencies
pkg update && pkg install git python -y

# Clone repository
cd $HOME
git clone https://github.com/yourusername/GeeX-OS.git

# Run installer
cd GeeX-OS
chmod +x setup.sh
./setup.sh
```

## Quick Install (Linux)

```bash
# Install dependencies
sudo apt update && sudo apt install git python3 python3-pip -y

# Clone repository
cd $HOME
git clone https://github.com/yourusername/GeeX-OS.git

# Run installer
cd GeeX-OS
chmod +x setup.sh
./setup.sh
```

## One-Liner Install (Curl)

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/GeeX-OS/main/setup.sh | bash
```

---

## Commands

| Command | Description |
|---------|-------------|
| `geex info` | System information |
| `geex dashboard` | Interactive system dashboard |
| `geex monitor` | Live system monitor |
| `geex sysfetch` | Beautiful system info display |
| `geex benchmark` | Performance benchmark |
| `geex doctor` | Diagnose issues |
| `geex cpu` | CPU info and monitoring |
| `geex memory` | Memory/RAM information |
| `geex storage` | Storage/disk information |
| `geex battery` | Battery status |
| `geex network` | Network tools |
| `geex theme` | Theme manager |
| `geex plugins` | Plugin manager |
| `geex config` | Configuration editor |
| `geex backup` | Backup configuration |
| `geex restore` | Restore from backup |
| `geex clean` | Clean cache and temp files |
| `geex update` | Check for updates |
| `geex ai` | AI assistant |
| `geex help` | Show all commands |

### Shortcuts

| Shortcut | Command |
|----------|---------|
| `gxx` | `geex` |
| `gxinfo` | `geex info` |
| `gxdash` | `geex dashboard` |
| `gxmon` | `geex monitor` |
| `gxfetch` | `geex sysfetch` |

---

## Themes

### Available Themes

| Theme | Style |
|-------|-------|
| `cyberpunk` | Neon blue cyberpunk (default) |
| `matrix` | Green Matrix rain style |
| `ocean` | Deep blue ocean |
| `neon` | Vibrant neon colors |
| `minimal` | Clean minimal design |
| `hackerman` | Classic hacker green |

### Switch Theme

```bash
geex theme <name>
# Example:
geex theme matrix
```

---

## Plugins

### Built-in Plugins

| Plugin | Description |
|--------|-------------|
| `ai_assistant` | Smart suggestions |
| `cyberclock` | Digital clock |
| `weather` | Weather info (wttr.in) |
| `network_scanner` | Port scanning |
| `terminal_games` | Mini games |
| `productivity` | Pomodoro timer |
| `filesystem` | File management |
| `animations` | Extra animations |

### Manage Plugins

```bash
geex plugins list
geex plugins enable <name>
geex plugins disable <name>
```

---

## Uninstall

```bash
# Run uninstaller
geex-uninstall

# Or manually
python3 ~/.geex/os/uninstall.py
```

---

## Troubleshooting

### Run diagnostics

```bash
geex doctor
```

### Common issues

**Import errors?**
```bash
pip3 install --user -r requirements.txt
```

**Shell hooks not working?**
```bash
source ~/.bashrc  # or ~/.zshrc
```

**Slow animations?**
```bash
geex config low_resource_mode true
```

---

## Project Structure

```
GeeX/
├── geex.py              # Main entry point
├── launcher.py          # Command dispatcher
├── installer.py         # Python installer
├── uninstall.py         # Uninstaller
├── updater.py           # Update checker
├── setup.sh             # One-click setup script
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── LICENSE              # MIT License
└── geex/
    ├── core/            # Core modules
    │   ├── config.py    # Configuration manager
    │   ├── theme.py     # Theme engine
    │   ├── animations.py # Animation engine
    │   ├── startup.py   # Startup sequence
    │   ├── shell.py     # Shell integration
    │   ├── dashboard.py # System dashboard
    │   ├── systeminfo.py # System info collector
    │   ├── prompt.py    # Smart prompt builder
    │   └── ...
    ├── ui/              # UI components
    ├── commands/        # CLI commands
    ├── plugins/         # Plugin modules
    ├── assets/          # Assets (banners, themes)
    └── data/            # Configuration files
```

---

## Requirements

- Python 3.7+
- Bash or Zsh shell
- Linux or Android (Termux)

### Python Packages

- `rich` - Terminal formatting
- `psutil` - System monitoring
- `colorama` - Cross-platform colors
- `pyfiglet` - ASCII art
- `prompt_toolkit` - Interactive prompts
- `pygments` - Syntax highlighting
- See `requirements.txt` for full list

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

---

<p align="center">
  <strong>Made with 💙 for the Termux community</strong><br>
  GeeX OS v2.0.0 | 2025
</p>
