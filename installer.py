#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Advanced Installer
# =============================================================================
# Auto-detects environment, installs dependencies, configures shell,
# and sets up GeeX OS completely for Termux and Linux.
# =============================================================================

import sys
import os
import json
import shutil
import subprocess
import platform
import argparse
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    NC = '\033[0m'


class Installer:
    """GeeX OS Advanced Installer"""
    
    VERSION = "2.0.0"
    
    def __init__(self):
        self.is_termux = self._detect_termux()
        self.shell = os.path.basename(os.environ.get('SHELL', 'bash'))
        self.shell_rc = self._get_shell_rc()
        self.geex_dir = Path.home() / ".geex"
        self.install_dir = self.geex_dir / "os"
        self.backup_dir = self.geex_dir / "backups"
        self.log_file = self.geex_dir / "logs" / "install.log"
        self.errors = []
        self.warnings = []
        
    def _detect_termux(self) -> bool:
        """Detect if running in Termux."""
        indicators = [
            'TERMUX_VERSION' in os.environ,
            os.path.exists('/data/data/com.termux'),
            os.environ.get('PREFIX', '').endswith('com.termux'),
        ]
        return any(indicators)
    
    def _get_shell_rc(self) -> str:
        """Get shell config file path."""
        if self.shell == 'zsh':
            return str(Path.home() / '.zshrc')
        return str(Path.home() / '.bashrc')
    
    def _log(self, msg: str):
        """Write to install log."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    
    def _run(self, cmd: list, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
        """Run shell command safely."""
        try:
            result = subprocess.run(
                cmd, capture_output=capture, text=True,
                check=False, timeout=300
            )
            if check and result.returncode != 0:
                self.errors.append(f"Command failed: {' '.join(cmd)}: {result.stderr}")
            self._log(f"CMD: {' '.join(cmd)} -> {result.returncode}")
            return result
        except Exception as e:
            self.errors.append(str(e))
            self._log(f"ERROR: {e}")
            return subprocess.CompletedProcess(cmd, 1)
    
    def print_banner(self):
        """Print installer banner."""
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"{Colors.CYAN}")
        print('   ██████╗ ███████╗███████╗██╗  ██╗      ██████╗ ███████╗')
        print('  ██╔════╝ ██╔════╝██╔════╝╚██╗██╔╝      ██╔═══██╗██╔════╝')
        print('  ██║  ███╗█████╗  █████╗   ╚███╔╝ █████╗██║   ██║███████╗')
        print('  ██║   ██║██╔══╝  ██╔══╝   ██╔██╗ ╚════╝██║   ██║╚════██║')
        print('  ╚██████╔╝███████╗███████╗██╔╝ ██╗      ╚██████╔╝███████║')
        print(f"  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═════╝ ╚══════╝{Colors.NC}")
        print(f"{Colors.MAGENTA}         ═══ Advanced Terminal Installer ═══{Colors.NC}")
        print(f"{Colors.BLUE}              Version {self.VERSION}{Colors.NC}\n")
    
    def print_status(self, step: str, status: str, color: str = Colors.GREEN):
        """Print installation status."""
        symbols = {"ok": "✓", "warn": "⚠", "error": "✗", "info": "ℹ", "run": "▶"}
        sym = symbols.get(status, "•")
        print(f"  {color}{sym}{Colors.NC} {step}")
    
    def check_python(self) -> bool:
        """Check and ensure Python 3 is available."""
        self.print_status("Checking Python 3...", "run", Colors.BLUE)
        result = self._run(['python3', '--version'], check=False)
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            self.print_status(f"Python found: {version}", "ok")
            return True
        
        # Try to install Python
        self.print_status("Python not found, attempting install...", "warn", Colors.YELLOW)
        if self.is_termux:
            self._run(['pkg', 'update', '-y'])
            self._run(['pkg', 'install', '-y', 'python'])
        else:
            self._run(['apt-get', 'update'], check=False)
            self._run(['apt-get', 'install', '-y', 'python3', 'python3-pip'], check=False)
        
        # Recheck
        result = self._run(['python3', '--version'], check=False)
        if result.returncode == 0:
            self.print_status("Python installed successfully", "ok")
            return True
        
        self.print_status("Failed to install Python", "error", Colors.RED)
        return False
    
    def install_system_deps(self):
        """Install system-level dependencies."""
        self.print_status("Installing system dependencies...", "run", Colors.BLUE)
        
        deps = ['git', 'curl', 'wget', 'ncurses-utils']
        if self.is_termux:
            self._run(['pkg', 'update', '-y'])
            for dep in deps:
                self._run(['pkg', 'install', '-y', dep], check=False)
        else:
            self._run(['apt-get', 'update'], check=False)
            self._run(['apt-get', 'install', '-y'] + deps, check=False)
        
        self.print_status("System dependencies installed", "ok")
    
    def install_python_deps(self):
        """Install Python packages from requirements.txt."""
        self.print_status("Installing Python dependencies...", "run", Colors.BLUE)
        
        req_file = Path(SCRIPT_DIR) / "requirements.txt"
        if req_file.exists():
            self._run(['pip3', 'install', '--user', '-r', str(req_file)])
        else:
            # Install core packages individually
            packages = [
                'rich', 'psutil', 'pyfiglet', 'prompt_toolkit', 'pygments',
                'requests', 'colorama', 'humanize', 'click', 'halo', 'tqdm'
            ]
            for pkg in packages:
                self.print_status(f"  Installing {pkg}...", "run", Colors.DIM)
                self._run(['pip3', 'install', '--user', pkg], check=False)
        
        self.print_status("Python dependencies installed", "ok")
    
    def setup_directories(self):
        """Create GeeX OS directory structure."""
        self.print_status("Setting up directories...", "run", Colors.BLUE)
        
        dirs = [
            self.geex_dir,
            self.install_dir,
            self.geex_dir / 'backups',
            self.geex_dir / 'themes',
            self.geex_dir / 'cache',
            self.geex_dir / 'logs',
            self.geex_dir / 'plugins',
            self.geex_dir / 'data',
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        
        # Copy project files
        if Path(SCRIPT_DIR / 'geex').exists():
            shutil.copytree(SCRIPT_DIR / 'geex', self.install_dir / 'geex', dirs_exist_ok=True)
        
        for f in ['launcher.py', 'installer.py', 'uninstall.py', 'updater.py',
                   'requirements.txt', 'README.md', 'LICENSE']:
            src = Path(SCRIPT_DIR) / f
            if src.exists():
                shutil.copy2(src, self.install_dir / f)
        
        self.print_status("Directories configured", "ok")
    
    def backup_existing(self):
        """Backup existing shell configs."""
        self.print_status("Backing up existing configuration...", "run", Colors.BLUE)
        
        backup_path = self.backup_dir / f"pre-install-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        if Path(self.shell_rc).exists():
            shutil.copy2(self.shell_rc, backup_path / Path(self.shell_rc).name)
            self.print_status(f"Backed up {self.shell_rc}", "ok")
    
    def configure_shell(self):
        """Configure shell integration."""
        self.print_status("Configuring shell integration...", "run", Colors.BLUE)
        
        geex_bin = self.geex_dir / 'bin'
        geex_bin.mkdir(exist_ok=True)
        
        # Create main geex wrapper
        geex_wrapper = geex_bin / 'geex'
        geex_wrapper.write_text(f'''#!/bin/bash
GEEX_DIR="{self.install_dir}"
python3 "$GEEX_DIR/launcher.py" "$@"
''')
        geex_wrapper.chmod(0o755)
        
        # Create shortcuts
        for cmd in ['geex-uninstall', 'geex-update', 'geex-repair']:
            shortcut = geex_bin / cmd
            py_file = 'uninstall.py' if 'uninstall' in cmd else ('updater.py' if 'update' in cmd else 'installer.py')
            shortcut.write_text(f'''#!/bin/bash
python3 "{self.install_dir}/{py_file}" "$@"
''')
            shortcut.chmod(0o755)
        
        # Add to PATH in shell RC
        path_line = f'export PATH="{geex_bin}:$PATH"'
        rc_content = Path(self.shell_rc).read_text() if Path(self.shell_rc).exists() else ''
        
        if path_line not in rc_content:
            with open(self.shell_rc, 'a') as f:
                f.write(f"\n# GeeX OS Path\n{path_line}\n")
        
        # Add shell hooks
        hook_marker = "# ═════ GeeX OS Integration ═════"
        if hook_marker not in rc_content:
            with open(self.shell_rc, 'a') as f:
                f.write(f'''
{hook_marker}
export GEEX_OS_VERSION="{self.VERSION}"
export GEEX_OS_HOME="{self.geex_dir}"

# GeeX startup (disable with GEEX_NO_STARTUP=1)
if [ -z "$GEEX_NO_STARTUP" ] && [ -f "{self.install_dir}/geex/core/startup.py" ]; then
    python3 "{self.install_dir}/geex/core/startup.py" --quick 2>/dev/null
fi

# GeeX smart prompt
if [ -f "{self.install_dir}/geex/core/prompt.py" ]; then
    eval "$(python3 "{self.install_dir}/geex/core/prompt.py" --init $? 2>/dev/null)"
fi

# GeeX aliases
if [ -f "{self.geex_dir}/data/aliases.sh" ]; then
    source "{self.geex_dir}/data/aliases.sh"
fi
# ═════ End GeeX OS ═════
''')
        
        self.print_status("Shell integration configured", "ok")
    
    def create_config_files(self):
        """Create all configuration files."""
        self.print_status("Creating configuration files...", "run", Colors.BLUE)
        
        data_dir = self.geex_dir / 'data'
        
        # Main config
        config = {
            "version": self.VERSION,
            "first_run": True,
            "theme": "cyberpunk",
            "shell": self.shell,
            "shell_rc": self.shell_rc,
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
                "show_cpu": False,
                "show_ram": False,
                "show_path": True,
                "show_exit_code": True,
                "newline": True,
                "color_scheme": "neon"
            },
            "paths": {
                "home": str(self.geex_dir),
                "os": str(self.install_dir),
                "backups": str(self.geex_dir / 'backups'),
                "themes": str(self.geex_dir / 'themes'),
                "cache": str(self.geex_dir / 'cache'),
                "logs": str(self.geex_dir / 'logs'),
                "plugins": str(self.geex_dir / 'plugins'),
                "data": str(self.geex_dir / 'data')
            }
        }
        
        with open(data_dir / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        # Themes
        themes = {
            "active": "cyberpunk",
            "available": ["cyberpunk", "matrix", "ocean", "neon", "minimal", "hackerman"],
            "cyberpunk": {
                "name": "Cyberpunk", "bg": "#0a0a0f", "fg": "#00d4ff",
                "accent1": "#00d4ff", "accent2": "#ff00ff", "accent3": "#00ff88",
                "warning": "#ffaa00", "error": "#ff0044", "success": "#00ff88", "dim": "#555577"
            },
            "matrix": {
                "name": "Matrix", "bg": "#000000", "fg": "#00ff00",
                "accent1": "#00ff00", "accent2": "#00cc00", "accent3": "#55ff55",
                "warning": "#ffaa00", "error": "#ff0044", "success": "#00ff00", "dim": "#008800"
            },
            "ocean": {
                "name": "Ocean", "bg": "#001020", "fg": "#44aaff",
                "accent1": "#44aaff", "accent2": "#0088ff", "accent3": "#66ccff",
                "warning": "#ffcc00", "error": "#ff4466", "success": "#44ffaa", "dim": "#336688"
            },
            "neon": {
                "name": "Neon", "bg": "#0f0010", "fg": "#ff00ff",
                "accent1": "#ff00ff", "accent2": "#00ffff", "accent3": "#ffff00",
                "warning": "#ff8800", "error": "#ff0044", "success": "#00ff88", "dim": "#663366"
            },
            "minimal": {
                "name": "Minimal", "bg": "#1a1a1a", "fg": "#cccccc",
                "accent1": "#ffffff", "accent2": "#999999", "accent3": "#666666",
                "warning": "#ffaa00", "error": "#ff4444", "success": "#44ff44", "dim": "#555555"
            },
            "hackerman": {
                "name": "Hackerman", "bg": "#050505", "fg": "#00ff41",
                "accent1": "#00ff41", "accent2": "#008f11", "accent3": "#003b00",
                "warning": "#d4ff00", "error": "#ff0000", "success": "#00ff41", "dim": "#005500"
            }
        }
        
        with open(data_dir / 'themes.json', 'w') as f:
            json.dump(themes, f, indent=2)
        
        # Plugins
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
        
        with open(data_dir / 'plugins.json', 'w') as f:
            json.dump(plugins, f, indent=2)
        
        # Cache
        cache = {"last_update_check": None, "weather_cache": {}, "system_cache": {}, "version_check": {}}
        with open(data_dir / 'cache.json', 'w') as f:
            json.dump(cache, f, indent=2)
        
        # Aliases shell script
        aliases_sh = data_dir / 'aliases.sh'
        aliases_sh.write_text('''#!/bin/bash
# GeeX OS Enhanced Aliases
alias ls='ls --color=auto'
alias grep='grep --color=auto'
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
alias gxhelp='geex help'
''')
        aliases_sh.chmod(0o755)
        
        self.print_status("Configuration files created", "ok")
    
    def verify_installation(self) -> bool:
        """Verify the installation is working."""
        self.print_status("Verifying installation...", "run", Colors.BLUE)
        
        checks = {
            "Config dir": self.geex_dir.exists(),
            "Install dir": self.install_dir.exists(),
            "Data dir": (self.geex_dir / 'data').exists(),
            "Config file": (self.geex_dir / 'data' / 'config.json').exists(),
            "Themes file": (self.geex_dir / 'data' / 'themes.json').exists(),
            "Launcher": (self.install_dir / 'launcher.py').exists(),
        }
        
        all_ok = True
        for name, result in checks.items():
            if result:
                self.print_status(f"  {name}: OK", "ok", Colors.DIM)
            else:
                self.print_status(f"  {name}: MISSING", "error", Colors.RED)
                all_ok = False
        
        if all_ok:
            self.print_status("Installation verified successfully!", "ok")
        else:
            self.print_status("Some components are missing", "warn", Colors.YELLOW)
        
        return all_ok
    
    def print_summary(self):
        """Print installation summary."""
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.GREEN}{Colors.BOLD}║           GeeX OS Installation Complete!                     ║{Colors.NC}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.NC}\n")
        
        print(f"{Colors.CYAN}Installation Directory:{Colors.NC} {self.install_dir}")
        print(f"{Colors.CYAN}Config Directory:{Colors.NC}       {self.geex_dir}")
        print(f"{Colors.CYAN}Shell:{Colors.NC}                  {self.shell}")
        print(f"{Colors.CYAN}Shell Config:{Colors.NC}           {self.shell_rc}")
        print(f"{Colors.CYAN}Termux:{Colors.NC}                 {'Yes' if self.is_termux else 'No'}")
        print("")
        
        print(f"{Colors.YELLOW}{Colors.BOLD}━━━ Next Steps ━━━{Colors.NC}")
        print(f"  {Colors.WHITE}1.{Colors.NC} Restart your terminal or run: {Colors.BOLD}source {self.shell_rc}{Colors.NC}")
        print(f"  {Colors.WHITE}2.{Colors.NC} Run {Colors.BOLD}geex{Colors.NC} to launch GeeX OS")
        print(f"  {Colors.WHITE}3.{Colors.NC} Run {Colors.BOLD}geex help{Colors.NC} to see all commands")
        print("")
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}━━━ Quick Commands ━━━{Colors.NC}")
        print(f"  {Colors.CYAN}geex info{Colors.NC}       - System information")
        print(f"  {Colors.CYAN}geex dashboard{Colors.NC}  - Interactive dashboard")
        print(f"  {Colors.CYAN}geex monitor{Colors.NC}    - Live system monitor")
        print(f"  {Colors.CYAN}geex sysfetch{Colors.NC}   - Beautiful sysfetch")
        print(f"  {Colors.CYAN}geex ai{Colors.NC}         - AI assistant")
        print(f"  {Colors.CYAN}geex theme{Colors.NC}      - Theme manager")
        print(f"  {Colors.CYAN}geex plugins{Colors.NC}    - Plugin manager")
        print(f"  {Colors.CYAN}geex update{Colors.NC}     - Update GeeX OS")
        print(f"  {Colors.CYAN}geex doctor{Colors.NC}     - Diagnose issues")
        print("")
        
        if self.warnings:
            print(f"{Colors.YELLOW}Warnings:{Colors.NC}")
            for w in self.warnings:
                print(f"  {Colors.YELLOW}⚠{Colors.NC} {w}")
            print("")
        
        if self.errors:
            print(f"{Colors.RED}Errors encountered:{Colors.NC}")
            for e in self.errors:
                print(f"  {Colors.RED}✗{Colors.NC} {e}")
            print(f"\n{Colors.YELLOW}Run 'geex doctor' to diagnose and fix issues.{Colors.NC}\n")
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}✨ Enjoy your enhanced terminal experience!{Colors.NC}\n")
    
    def run(self):
        """Run the full installation process."""
        self.print_banner()
        
        print(f"{Colors.BOLD}Environment:{Colors.NC}")
        print(f"  Platform: {platform.system()} {platform.machine()}")
        print(f"  Python: {sys.version.split()[0]}")
        print(f"  Shell: {self.shell}")
        print(f"  Termux: {'Yes' if self.is_termux else 'No'}")
        print("")
        
        input(f"{Colors.CYAN}Press Enter to begin installation...{Colors.NC}")
        print("")
        
        # Run installation steps
        steps = [
            ("Checking Python", self.check_python),
            ("System Dependencies", self.install_system_deps),
            ("Python Dependencies", self.install_python_deps),
            ("Setup Directories", self.setup_directories),
            ("Backup Configs", self.backup_existing),
            ("Configure Shell", self.configure_shell),
            ("Create Configs", self.create_config_files),
            ("Verify Install", self.verify_installation),
        ]
        
        for name, step_func in steps:
            print(f"\n{Colors.MAGENTA}{Colors.BOLD}━━━ {name} ━━━{Colors.NC}")
            try:
                result = step_func()
                if result is False:
                    self.print_status(f"{name} failed critically", "error", Colors.RED)
                    if name == "Checking Python":
                        print(f"\n{Colors.RED}Cannot continue without Python.{Colors.NC}")
                        return 1
            except Exception as e:
                self.print_status(f"{name} error: {e}", "error", Colors.RED)
                self.errors.append(str(e))
        
        self.print_summary()
        return 0 if not self.errors else 1


def main():
    """Entry point for the installer."""
    parser = argparse.ArgumentParser(description='GeeX OS Installer')
    parser.add_argument('--shell', default=None, help='Target shell (bash/zsh)')
    parser.add_argument('--rc', default=None, help='Shell config file path')
    parser.add_argument('--no-deps', action='store_true', help='Skip dependency installation')
    parser.add_argument('--minimal', action='store_true', help='Minimal installation')
    args = parser.parse_args()
    
    installer = Installer()
    
    if args.shell:
        installer.shell = args.shell
    if args.rc:
        installer.shell_rc = args.rc
    
    return installer.run()


if __name__ == "__main__":
    sys.exit(main())
