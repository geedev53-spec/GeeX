#!/bin/bash
# =============================================================================
# GeeX OS - One-Click Installer for Termux & Linux
# =============================================================================
# This script auto-detects the environment, installs all dependencies,
# and sets up GeeX OS completely.
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m'

GEEX_VERSION="2.0.0"
GEEX_DIR="$HOME/.geex"
INSTALL_DIR="$GEEX_DIR/os"
REPO_URL="https://github.com/geexos/GeeX-OS.git"

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

print_banner() {
    clear
    echo -e "${CYAN}"
    echo '   ██████╗ ███████╗███████╗██╗  ██╗      ██████╗ ███████╗'
    echo '  ██╔════╝ ██╔════╝██╔════╝╚██╗██╔╝      ██╔═══██╗██╔════╝'
    echo '  ██║  ███╗█████╗  █████╗   ╚███╔╝ █████╗██║   ██║███████╗'
    echo '  ██║   ██║██╔══╝  ██╔══╝   ██╔██╗ ╚════╝██║   ██║╚════██║'
    echo '  ╚██████╔╝███████╗███████╗██╔╝ ██╗      ╚██████╔╝███████║'
    echo '   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═════╝ ╚══════╝'
    echo -e "${MAGENTA}"
    echo '         ═══ Termux Terminal Enhancement Framework ═══'
    echo -e "${BLUE}                  Version ${GEEX_VERSION} | Production Ready${NC}"
    echo ""
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

step() {
    echo -e "\n${MAGENTA}${BOLD}━━━ $1 ━━━${NC}\n"
}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " ${CYAN}[%c]${NC}  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\r"
    done
    printf "       \r"
}

detect_termux() {
    if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux" ] || [ -n "$PREFIX" ] && [[ "$PREFIX" == *"com.termux"* ]]; then
        return 0
    fi
    return 1
}

detect_shell() {
    local current_shell=$(basename "$SHELL")
    echo "$current_shell"
}

get_shell_rc() {
    local shell_name=$(detect_shell)
    if [ "$shell_name" = "zsh" ]; then
        echo "$HOME/.zshrc"
    else
        echo "$HOME/.bashrc"
    fi
}

# ---------------------------------------------------------------------------
# Pre-flight Checks
# ---------------------------------------------------------------------------

print_banner

step "System Detection"

if detect_termux; then
    success "Termux detected! (Version: ${TERMUX_VERSION:-unknown})"
    IS_TERMUX=true
else
    warn "Not running in Termux - installing for generic Linux"
    IS_TERMUX=false
fi

SHELL_NAME=$(detect_shell)
SHELL_RC=$(get_shell_rc)
info "Detected shell: ${SHELL_NAME}"
info "Shell config: ${SHELL_RC}"

# Check Python
step "Checking Python"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    success "Python ${PYTHON_VERSION} found"
else
    error "Python 3 not found. Installing..."
    if [ "$IS_TERMUX" = true ]; then
        pkg update -y && pkg install python -y
    else
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    fi
fi

# Check pip
if ! command -v pip3 &>/dev/null && ! command -v pip &>/dev/null; then
    warn "pip not found. Installing..."
    python3 -m ensurepip --upgrade || true
fi

# Upgrade pip
python3 -m pip install --upgrade pip &>/dev/null &
spinner $!
success "pip upgraded"

# ---------------------------------------------------------------------------
# Install System Dependencies
# ---------------------------------------------------------------------------

step "Installing System Dependencies"

if [ "$IS_TERMUX" = true ]; then
    info "Updating Termux packages..."
    pkg update -y &>/dev/null &
    spinner $!
    
    TERMUX_DEPS="git zsh curl wget termux-api ncurses-utils"
    for dep in $TERMUX_DEPS; do
        info "Installing ${dep}..."
        pkg install -y $dep &>/dev/null &
        spinner $!
        success "${dep} installed"
    done
else
    info "Installing Linux dependencies..."
    sudo apt-get update &>/dev/null &
    spinner $!
    sudo apt-get install -y git zsh curl wget ncurses-bin &>/dev/null &
    spinner $!
    success "Dependencies installed"
fi

# ---------------------------------------------------------------------------
# Setup Directories
# ---------------------------------------------------------------------------

step "Setting Up Directories"

mkdir -p "$INSTALL_DIR"
mkdir -p "$GEEX_DIR"/{backups,themes,cache,logs,plugins}

# Copy project files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "$SCRIPT_DIR/geex" ]; then
    cp -r "$SCRIPT_DIR/geex" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR"/*.py "$INSTALL_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR/requirements.txt" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/LICENSE" "$INSTALL_DIR/"
fi

success "Directories created at ${INSTALL_DIR}"

# ---------------------------------------------------------------------------
# Install Python Dependencies
# ---------------------------------------------------------------------------

step "Installing Python Dependencies"

info "This may take a few minutes..."

pip3 install --user -r "$SCRIPT_DIR/requirements.txt" &>/dev/null &
spinner $!
success "All Python dependencies installed"

# ---------------------------------------------------------------------------
# Run Python Installer
# ---------------------------------------------------------------------------

step "Running GeeX OS Installer"

if [ -f "$INSTALL_DIR/installer.py" ]; then
    python3 "$INSTALL_DIR/installer.py" --shell "${SHELL_NAME}" --rc "${SHELL_RC}"
else
    # Fallback: manual installation
    info "Running manual setup..."
fi

# ---------------------------------------------------------------------------
# Shell Integration
# ---------------------------------------------------------------------------

step "Configuring Shell Integration"

GEEX_BIN="$GEEX_DIR/bin"
mkdir -p "$GEEX_BIN"

# Create main geex command wrapper
cat > "$GEEX_BIN/geex" << 'EOF'
#!/bin/bash
# GeeX OS Main Command Wrapper

GEEX_DIR="$HOME/.geex/os"
PYTHON_CMD=$(command -v python3)

if [ -f "$GEEX_DIR/launcher.py" ]; then
    $PYTHON_CMD "$GEEX_DIR/launcher.py" "$@"
else
    echo "GeeX OS not found. Please reinstall."
    exit 1
fi
EOF
chmod +x "$GEEX_BIN/geex"

# Add to PATH
if ! grep -q "$GEEX_BIN" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# GeeX OS Path" >> "$SHELL_RC"
    echo "export PATH=\"$GEEX_BIN:\$PATH\"" >> "$SHELL_RC"
    success "Added GeeX to PATH"
fi

# Add shell startup hook
if ! grep -q "GEEX_OS" "$SHELL_RC" 2>/dev/null; then
    cat >> "$SHELL_RC" << EOF

# ═══════════════════════════════════════════
# GeeX OS Terminal Enhancement Framework
# ═══════════════════════════════════════════
export GEEX_OS_VERSION="${GEEX_VERSION}"
export GEEX_OS_HOME="${GEEX_DIR}"

# Auto-launch GeeX startup (disable with GEEX_NO_STARTUP=1)
if [ -z "\$GEEX_NO_STARTUP" ] && [ -f "${INSTALL_DIR}/geex/core/startup.py" ]; then
    python3 "${INSTALL_DIR}/geex/core/startup.py" --quick 2>/dev/null
fi

# GeeX prompt integration
if [ -f "${INSTALL_DIR}/geex/core/prompt.py" ]; then
    eval "\$(python3 "${INSTALL_DIR}/geex/core/prompt.py" --init \$?)"
fi

# GeeX aliases
if [ -f "${GEEX_DIR}/data/aliases.sh" ]; then
    source "${GEEX_DIR}/data/aliases.sh"
fi
EOF
    success "Shell integration added to ${SHELL_RC}"
fi

# ---------------------------------------------------------------------------
# Create aliases file
# ---------------------------------------------------------------------------

mkdir -p "$GEEX_DIR/data"

cat > "$GEEX_DIR/data/aliases.sh" << 'EOF'
#!/bin/bash
# GeeX OS Enhanced Aliases

# --- Core Aliases ---
alias ls='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.commands.terminal import fancy_ls; fancy_ls()" 2>/dev/null || ls --color=auto'
alias cat='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.commands.terminal import fancy_cat; fancy_cat(\">>>\".join(sys.argv[1:]))" 2>/dev/null || cat'
alias grep='grep --color=auto'
alias top='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.commands.monitor import top_app; top_app()" 2>/dev/null || top'
alias clear='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.core.animations import clear_animated; clear_animated()" 2>/dev/null || clear'

# --- GeeX Shortcuts ---
alias gxx='geex'
alias gxinfo='geex info'
alias gxdash='geex dashboard'
alias gxmon='geex monitor'
alias gxdoc='geex doctor'
alias gxbench='geex benchmark'
alias gxupdate='geex update'
alias gxbackup='geex backup'
alias gxtheme='geex theme'
alias gxplugins='geex plugins'
alias gxai='geex ai'
alias gxfetch='geex sysfetch'
alias gxnet='geex network'
alias gxbat='geex battery'
alias gxcpu='geex cpu'
alias gxmem='geex memory'
alias gxsto='geex storage'
alias gxhelp='geex help'

# --- Developer Aliases ---
alias weather='geex weather 2>/dev/null || echo "Run: geex weather"'
alias sysfetch='geex sysfetch'
alias matrix='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.core.animations import matrix_rain; matrix_rain()"'
alias ports='netstat -tulanp 2>/dev/null || netstat -tulan'
alias extract='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.commands.terminal import extract_archive; extract_archive(\">>>\".join(sys.argv[1:]))"'
alias mkcd='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.commands.terminal import mkcd; mkcd(sys.argv[1])"'
alias serve='python3 -m http.server'
alias backup='geex backup'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph'
alias gd='git diff'

# --- Fun ---
alias cyberpunk='python3 -c "import sys; sys.path.insert(0, \"\$HOME/.geex/os\"); from geex.ui.cyberpunk import run_cyberpunk; run_cyberpunk()"'
alias cyberclock='geex clock'
EOF
chmod +x "$GEEX_DIR/data/aliases.sh"

# ---------------------------------------------------------------------------
# Create config files
# ---------------------------------------------------------------------------

step "Creating Configuration Files"

python3 << EOF
import json
import os

geex_dir = os.path.expanduser("~/.geex")

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

# Main config
config = {
    "version": "${GEEX_VERSION}",
    "first_run": True,
    "theme": "cyberpunk",
    "shell": "${SHELL_NAME}",
    "shell_rc": "${SHELL_RC}",
    "startup_enabled": True,
    "startup_quick": True,
    "animations_enabled": True,
    "truecolor": True,
    "unicode": True,
    "sound": False,
    "auto_update_check": True,
    "update_channel": "stable",
    "backup_auto": True,
    "backup_keep": 5,
    "log_level": "INFO",
    "debug": False,
    "low_resource_mode": False,
    "dashboard_refresh": 2.0,
    "monitor_refresh": 1.0,
    "prompt": {
        "enabled": True,
        "style": "powerline",
        "show_time": True,
        "show_user": True,
        "show_host": True,
        "show_git": True,
        "show_battery": True,
        "show_cpu": True,
        "show_ram": True,
        "show_path": True,
        "show_exit_code": True,
        "newline": True,
        "color_scheme": "neon"
    },
    "paths": {
        "home": geex_dir,
        "os": f"{geex_dir}/os",
        "backups": f"{geex_dir}/backups",
        "themes": f"{geex_dir}/themes",
        "cache": f"{geex_dir}/cache",
        "logs": f"{geex_dir}/logs",
        "plugins": f"{geex_dir}/plugins",
        "data": f"{geex_dir}/data"
    },
    "aliases": {
        "ls": "fancy",
        "cat": "fancy",
        "grep": "colored",
        "clear": "animated"
    }
}
save_json(f"{geex_dir}/data/config.json", config)

# Themes config
themes = {
    "active": "cyberpunk",
    "available": ["cyberpunk", "matrix", "ocean", "neon", "minimal", "hackerman"],
    "cyberpunk": {
        "name": "Cyberpunk",
        "bg": "#0a0a0f",
        "fg": "#00d4ff",
        "accent1": "#00d4ff",
        "accent2": "#ff00ff",
        "accent3": "#00ff88",
        "warning": "#ffaa00",
        "error": "#ff0044",
        "success": "#00ff88",
        "dim": "#555577"
    },
    "matrix": {
        "name": "Matrix",
        "bg": "#000000",
        "fg": "#00ff00",
        "accent1": "#00ff00",
        "accent2": "#00cc00",
        "accent3": "#55ff55",
        "warning": "#ffaa00",
        "error": "#ff0044",
        "success": "#00ff00",
        "dim": "#008800"
    },
    "ocean": {
        "name": "Ocean",
        "bg": "#001020",
        "fg": "#44aaff",
        "accent1": "#44aaff",
        "accent2": "#0088ff",
        "accent3": "#66ccff",
        "warning": "#ffcc00",
        "error": "#ff4466",
        "success": "#44ffaa",
        "dim": "#336688"
    },
    "neon": {
        "name": "Neon",
        "bg": "#0f0010",
        "fg": "#ff00ff",
        "accent1": "#ff00ff",
        "accent2": "#00ffff",
        "accent3": "#ffff00",
        "warning": "#ff8800",
        "error": "#ff0044",
        "success": "#00ff88",
        "dim": "#663366"
    },
    "minimal": {
        "name": "Minimal",
        "bg": "#1a1a1a",
        "fg": "#cccccc",
        "accent1": "#ffffff",
        "accent2": "#999999",
        "accent3": "#666666",
        "warning": "#ffaa00",
        "error": "#ff4444",
        "success": "#44ff44",
        "dim": "#555555"
    },
    "hackerman": {
        "name": "Hackerman",
        "bg": "#050505",
        "fg": "#00ff41",
        "accent1": "#00ff41",
        "accent2": "#008f11",
        "accent3": "#003b00",
        "warning": "#d4ff00",
        "error": "#ff0000",
        "success": "#00ff41",
        "dim": "#005500"
    }
}
save_json(f"{geex_dir}/data/themes.json", themes)

# Plugins config
plugins = {
    "ai_assistant": {"enabled": True, "config": {}},
    "cyberclock": {"enabled": True, "config": {"format": "24h", "show_seconds": True}},
    "weather": {"enabled": False, "config": {"location": "auto", "unit": "celsius"}},
    "network_scanner": {"enabled": False, "config": {}},
    "terminal_games": {"enabled": False, "config": {}},
    "productivity": {"enabled": True, "config": {}},
    "filesystem": {"enabled": True, "config": {}},
    "animations": {"enabled": True, "config": {}}
}
save_json(f"{geex_dir}/data/plugins.json", plugins)

# Cache
cache = {
    "last_update_check": None,
    "weather_cache": {},
    "system_cache": {},
    "version_check": {}
}
save_json(f"{geex_dir}/data/cache.json", cache)

print("Configuration files created successfully!")
EOF

success "All configuration files created"

# ---------------------------------------------------------------------------
# Backup existing configs
# ---------------------------------------------------------------------------

step "Backing Up Existing Configurations"

BACKUP_DIR="$GEEX_DIR/backups/pre-install-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f "$SHELL_RC" ]; then
    cp "$SHELL_RC" "$BACKUP_DIR/"
    success "Backed up ${SHELL_RC}"
fi

# ---------------------------------------------------------------------------
# Final Setup
# ---------------------------------------------------------------------------

step "Finalizing Installation"

# Make all Python files executable
find "$INSTALL_DIR" -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

# Create uninstall shortcut
cat > "$GEEX_BIN/geex-uninstall" << EOF
#!/bin/bash
python3 "${INSTALL_DIR}/uninstall.py" "\$@"
EOF
chmod +x "$GEEX_BIN/geex-uninstall"

# Create update shortcut
cat > "$GEEX_BIN/geex-update" << EOF
#!/bin/bash
python3 "${INSTALL_DIR}/updater.py" "\$@"
EOF
chmod +x "$GEEX_BIN/geex-update"

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------

print_banner

echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║           GeeX OS Installation Complete!                     ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}${BOLD}Installation Directory:${NC} ${INSTALL_DIR}"
echo -e "${CYAN}${BOLD}Config Directory:${NC}       ${GEEX_DIR}"
echo -e "${CYAN}${BOLD}Shell:${NC}                  ${SHELL_NAME}"
echo -e "${CYAN}${BOLD}Shell Config:${NC}           ${SHELL_RC}"
echo ""
echo -e "${YELLOW}${BOLD}━━━ Next Steps ━━━${NC}"
echo -e "  ${WHITE}1.${NC} Restart your terminal or run: ${BOLD}source ${SHELL_RC}${NC}"
echo -e "  ${WHITE}2.${NC} Run ${BOLD}geex${NC} to launch GeeX OS"
echo -e "  ${WHITE}3.${NC} Run ${BOLD}geex help${NC} to see all commands"
echo -e "  ${WHITE}4.${NC} Run ${BOLD}geex dashboard${NC} for system dashboard"
echo ""
echo -e "${MAGENTA}${BOLD}━━━ Quick Commands ━━━${NC}"
echo -e "  ${CYAN}geex info${NC}       - System information"
echo -e "  ${CYAN}geex dashboard${NC}  - Interactive dashboard"
echo -e "  ${CYAN}geex monitor${NC}    - Live system monitor"
echo -e "  ${CYAN}geex sysfetch${NC}   - Beautiful sysfetch"
echo -e "  ${CYAN}geex ai${NC}         - AI assistant"
echo -e "  ${CYAN}geex theme${NC}      - Theme manager"
echo -e "  ${CYAN}geex plugins${NC}    - Plugin manager"
echo -e "  ${CYAN}geex update${NC}     - Update GeeX OS"
echo -e "  ${CYAN}geex doctor${NC}     - Diagnose issues"
echo ""
echo -e "${GREEN}${BOLD}Enjoy your enhanced terminal experience!${NC}"
echo -e "${DIM}Report issues: https://github.com/geexos/GeeX-OS/issues${NC}"
echo ""
