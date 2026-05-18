#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Smart Prompt Builder
# =============================================================================
# Futuristic multi-line shell prompt with powerline-style segments
# showing time, user, git, battery, CPU, RAM, and more.
# =============================================================================

import os
import sys
import socket
import subprocess
from datetime import datetime
from pathlib import Path


class PromptBuilder:
    """GeeX OS Smart Prompt Builder"""
    
    SYMBOLS = {
        'powerline': {'sep': '\ue0b0', 'thin': '\ue0b1', 'rsep': '\ue0b2'},
        'round': {'sep': '\ue0b4', 'thin': '\ue0b5', 'rsep': '\ue0b6'},
        'arrow': {'sep': '⮀', 'thin': '⮁', 'rsep': '⮂'},
        'triangle': {'sep': '▶', 'thin': '▷', 'rsep': '◀'},
        'slant': {'sep': '', 'thin': '│', 'rsep': ''},
    }
    
    def __init__(self, config=None):
        from geex.core.config import Config
        self.config = config or Config()
        self.prompt_cfg = self.config.get("prompt", {})
        self.style = self.prompt_cfg.get("style", "powerline")
        self.symbols = self.SYMBOLS.get(self.style, self.SYMBOLS['powerline'])
    
    def _segment(self, text: str, fg: str, bg: str, next_bg: str = None) -> str:
        """Build a powerline segment."""
        sep = self.symbols['sep']
        
        # Convert hex to ANSI
        fg_ansi = self._hex_to_ansi(fg)
        bg_ansi = self._hex_to_bg(bg)
        reset = '\033[0m'
        
        segment = f"{bg_ansi}{fg_ansi} {text} {reset}"
        
        if next_bg:
            next_bg_ansi = self._hex_to_bg(next_bg)
            segment += f"\033[38;2;{self._hex_to_rgb(bg)}m{next_bg_ansi}{sep}{reset}"
        
        return segment
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex to ANSI RGB string."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r};{g};{b}"
    
    def _hex_to_ansi(self, hex_color: str) -> str:
        """Convert hex to ANSI foreground."""
        return f"\033[38;2;{self._hex_to_rgb(hex_color)}m"
    
    def _hex_to_bg(self, hex_color: str) -> str:
        """Convert hex to ANSI background."""
        return f"\033[48;2;{self._hex_to_rgb(hex_color)}m"
    
    def _get_time(self) -> str:
        """Get formatted time."""
        return datetime.now().strftime("%H:%M:%S")
    
    def _get_user_host(self) -> str:
        """Get user@hostname."""
        user = os.environ.get('USER', 'user')
        host = socket.gethostname().split('.')[0]
        return f"{user}@{host}"
    
    def _get_path(self) -> str:
        """Get current directory (shortened)."""
        cwd = os.getcwd()
        home = str(Path.home())
        if cwd.startswith(home):
            cwd = '~' + cwd[len(home):]
        if len(cwd) > 30:
            parts = cwd.split('/')
            if len(parts) > 4:
                cwd = '/'.join(parts[:2]) + '/.../' + '/'.join(parts[-2:])
        return cwd
    
    def _get_git_branch(self) -> str:
        """Get git branch if in a repo."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, timeout=2,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return ""
    
    def _get_git_status(self) -> str:
        """Get git status indicator."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, timeout=2,
                cwd=os.getcwd()
            )
            if result.stdout.strip():
                return "●"  # Modified
            return "○"  # Clean
        except Exception:
            return ""
    
    def _get_battery(self) -> str:
        """Get battery percentage."""
        try:
            paths = [
                '/sys/class/power_supply/battery/capacity',
                '/sys/class/power_supply/Battery/capacity',
            ]
            for path in paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        pct = int(f.read().strip())
                    icon = "🔌" if pct > 80 else "🔋"
                    return f"{icon} {pct}%"
        except Exception:
            pass
        return ""
    
    def _get_cpu_usage(self) -> str:
        """Get CPU usage."""
        try:
            with open('/proc/stat', 'r') as f:
                line = f.readline()
                fields = list(map(int, line.split()[1:]))
                idle = fields[3]
                total = sum(fields)
                usage = ((total - idle) / total) * 100 if total > 0 else 0
                return f"CPU {usage:.0f}%"
        except Exception:
            return ""
    
    def _get_ram_usage(self) -> str:
        """Get RAM usage."""
        try:
            with open('/proc/meminfo', 'r') as f:
                data = {}
                for line in f:
                    if ':' in line:
                        key, val = line.split(':', 1)
                        data[key.strip()] = int(val.split()[0])
                total = data.get('MemTotal', 1)
                free = data.get('MemAvailable', data.get('MemFree', 0))
                used = total - free
                pct = (used / total) * 100
                return f"RAM {pct:.0f}%"
        except Exception:
            return ""
    
    def _get_exit_code(self, code: int) -> str:
        """Get exit code indicator."""
        if code == 0:
            return "✓"
        return f"✗ {code}"
    
    def _get_venv(self) -> str:
        """Get virtualenv name."""
        venv = os.environ.get('VIRTUAL_ENV', '')
        if venv:
            return os.path.basename(venv)
        return ""
    
    def _is_root(self) -> bool:
        """Check if running as root."""
        return os.geteuid() == 0 if hasattr(os, 'geteuid') else False
    
    def build(self, exit_code: int = 0) -> str:
        """Build the complete prompt string."""
        cfg = self.prompt_cfg
        if not cfg.get("enabled", True):
            return ""
        
        segments = []
        
        # Line 1: Status segments
        if cfg.get("show_time", True):
            segments.append(self._segment(self._get_time(), "#0a0a0f", "#00d4ff", "#555577"))
        
        if cfg.get("show_user", True):
            user_host = self._get_user_host()
            root_indicator = " ⚠ ROOT" if self._is_root() else ""
            segments.append(self._segment(user_host + root_indicator, "#ffffff", "#555577", "#0a0a0f"))
        
        venv = self._get_venv()
        if venv:
            segments.append(self._segment(f"🐍 {venv}", "#0a0a0f", "#00ff88"))
        
        # Git info
        if cfg.get("show_git", True):
            branch = self._get_git_branch()
            if branch:
                status = self._get_git_status()
                bg = "#ffaa00" if status == "●" else "#00ff88"
                segments.append(self._segment(f" {branch} {status}", "#0a0a0f", bg))
        
        # Battery
        if cfg.get("show_battery", True):
            batt = self._get_battery()
            if batt:
                segments.append(self._segment(batt, "#0a0a0f", "#ff00ff"))
        
        # CPU
        if cfg.get("show_cpu", False):
            cpu = self._get_cpu_usage()
            if cpu:
                segments.append(self._segment(cpu, "#ffffff", "#555577"))
        
        # RAM
        if cfg.get("show_ram", False):
            ram = self._get_ram_usage()
            if ram:
                segments.append(self._segment(ram, "#ffffff", "#555577"))
        
        # Exit code
        if cfg.get("show_exit_code", True):
            code_str = self._get_exit_code(exit_code)
            color = "#00ff88" if exit_code == 0 else "#ff0044"
            segments.append(self._segment(code_str, "#ffffff", color))
        
        # Line 2: Path
        path_segments = []
        if cfg.get("show_path", True):
            path = self._get_path()
            sep = '\n' if cfg.get("newline", True) else ' '
            path_segments.append(f"{sep}\033[96m❱❱❱ \033[1m{path}\033[0m ")
        
        # Build final prompt
        prompt = ''.join(segments) + ''.join(path_segments)
        return prompt


def main():
    """Entry point for shell integration."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', type=int, nargs='?', default=None, help='Initialize prompt')
    parser.add_argument('--preview', action='store_true', help='Show preview')
    args = parser.parse_args()
    
    builder = PromptBuilder()
    
    if args.preview:
        print("GeeX OS Prompt Preview:")
        print(builder.build(0))
        print("\nWith error exit code:")
        print(builder.build(1))
        return 0
    
    if args.init is not None:
        # Output shell integration code
        print(f'export PS1="{builder.build(args.init)}"')
    else:
        print(builder.build(0))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
