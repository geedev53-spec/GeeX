#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Theme Engine
# =============================================================================
# Dynamic color engine with truecolor support, theme switching,
# and cyberpunk/neon/minimal presets.
# =============================================================================

import os
import re
from typing import Dict, List, Optional, Tuple


class Theme:
    """GeeX OS Dynamic Theme Engine"""
    
    def __init__(self, config=None):
        from geex.core.config import Config
        self.config = config or Config()
        self._current = self.config.get_theme()
        self._truecolor = self.config.get("truecolor", True)
    
    @property
    def name(self) -> str:
        return self._current.get("name", "Cyberpunk")
    
    @property
    def bg(self) -> str:
        return self._current.get("bg", "#0a0a0f")
    
    @property
    def fg(self) -> str:
        return self._current.get("fg", "#00d4ff")
    
    @property
    def accent1(self) -> str:
        return self._current.get("accent1", "#00d4ff")
    
    @property
    def accent2(self) -> str:
        return self._current.get("accent2", "#ff00ff")
    
    @property
    def accent3(self) -> str:
        return self._current.get("accent3", "#00ff88")
    
    @property
    def warning(self) -> str:
        return self._current.get("warning", "#ffaa00")
    
    @property
    def error(self) -> str:
        return self._current.get("error", "#ff0044")
    
    @property
    def success(self) -> str:
        return self._current.get("success", "#00ff88")
    
    @property
    def dim(self) -> str:
        return self._current.get("dim", "#555577")
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def hex_to_ansi(self, hex_color: str, bg: bool = False) -> str:
        """Convert hex to ANSI truecolor code."""
        if not self._truecolor:
            return ''
        r, g, b = self.hex_to_rgb(hex_color)
        code = 48 if bg else 38
        return f'\033[{code};2;{r};{g};{b}m'
    
    def reset(self) -> str:
        return '\033[0m'
    
    def bold(self) -> str:
        return '\033[1m'
    
    def dim_style(self) -> str:
        return '\033[2m'
    
    def italic(self) -> str:
        return '\033[3m'
    
    def underline(self) -> str:
        return '\033[4m'
    
    def color(self, hex_color: str) -> str:
        """Get ANSI color code for hex."""
        return self.hex_to_ansi(hex_color)
    
    def fg_color(self) -> str:
        return self.hex_to_ansi(self.fg)
    
    def bg_color(self) -> str:
        return self.hex_to_ansi(self.bg, bg=True)
    
    def a1(self) -> str:
        return self.hex_to_ansi(self.accent1)
    
    def a2(self) -> str:
        return self.hex_to_ansi(self.accent2)
    
    def a3(self) -> str:
        return self.hex_to_ansi(self.accent3)
    
    def warn(self) -> str:
        return self.hex_to_ansi(self.warning)
    
    def err(self) -> str:
        return self.hex_to_ansi(self.error)
    
    def ok(self) -> str:
        return self.hex_to_ansi(self.success)
    
    def dimmed(self) -> str:
        return self.hex_to_ansi(self.dim)
    
    def gradient(self, text: str, start_hex: str, end_hex: str) -> str:
        """Apply gradient to text."""
        if not text or not self._truecolor:
            return text
        
        sr, sg, sb = self.hex_to_rgb(start_hex)
        er, eg, eb = self.hex_to_rgb(end_hex)
        length = len(text.replace('\033[', '\033[@').split('\033[0m')[-1]) if '\033[' in text else len(text)
        
        result = []
        for i, char in enumerate(text):
            if char == ' ':
                result.append(char)
                continue
            ratio = i / max(len(text) - 1, 1)
            r = int(sr + (er - sr) * ratio)
            g = int(sg + (eg - sg) * ratio)
            b = int(sb + (eb - sb) * ratio)
            result.append(f'\033[38;2;{r};{g};{b}m{char}')
        
        return ''.join(result) + '\033[0m'
    
    def styled(self, text: str, color: str = None, bold: bool = False, dim: bool = False) -> str:
        """Apply styling to text."""
        styles = []
        if bold:
            styles.append('\033[1m')
        if dim:
            styles.append('\033[2m')
        if color:
            styles.append(self.hex_to_ansi(color) if color.startswith('#') else color)
        
        return ''.join(styles) + text + '\033[0m' if styles else text
    
    def list_themes(self) -> List[str]:
        """List available themes."""
        return self.config.list_themes()
    
    def set_theme(self, name: str) -> bool:
        """Switch to a theme."""
        if self.config.set_theme(name):
            self._current = self.config.get_theme()
            return True
        return False
    
    def print_banner(self):
        """Print themed banner."""
        c = self
        print(f"{c.a1()}")
        print('   ██████╗ ███████╗███████╗██╗  ██╗      ██████╗ ███████╗')
        print('  ██╔════╝ ██╔════╝██╔════╝╚██╗██╔╝      ██╔═══██╗██╔════╝')
        print('  ██║  ███╗█████╗  █████╗   ╚███╔╝ █████╗██║   ██║███████╗')
        print('  ██║   ██║██╔══╝  ██╔══╝   ██╔██╗ ╚════╝██║   ██║╚════██║')
        print('  ╚██████╔╝███████╗███████╗██╔╝ ██╗      ╚██████╔╝███████║')
        print(f'   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═════╝ ╚══════╝')
        print(f"{c.a2()}")
        print('         ═══ Futuristic Terminal Framework ═══')
        print(f"{c.dimmed()}              v2.0.0 | Production Ready{c.reset()}")
        print("")
    
    def box(self, text: str, width: int = 60, title: str = "") -> str:
        """Draw a themed box around text."""
        c = self
        lines = text.split('\n')
        result = []
        
        top = f"{c.a1()}┌{'─' * (width - 2)}┐{c.reset()}"
        if title:
            title_str = f" {title} "
            pos = (width - len(title_str)) // 2
            top = f"{c.a1()}┌{'─' * (pos - 1)}{c.a2()}{title_str}{c.a1()}{'─' * (width - pos - len(title_str) - 1)}┐{c.reset()}"
        result.append(top)
        
        for line in lines[:20]:
            truncated = line[:width-4]
            padded = truncated + ' ' * (width - 4 - len(truncated))
            result.append(f"{c.a1()}│{c.fg_color()} {padded} {c.a1()}│{c.reset()}")
        
        result.append(f"{c.a1()}└{'─' * (width - 2)}┘{c.reset()}")
        return '\n'.join(result)
    
    def separator(self, width: int = 60) -> str:
        """Draw a themed separator line."""
        return f"{self.dimmed()}{'─' * width}{self.reset()}"
    
    def header(self, text: str, width: int = 60) -> str:
        """Draw a themed header."""
        c = self
        pad = (width - len(text) - 4) // 2
        return f"{c.a1()}{'━' * pad} {c.a2()}{c.bold()}{text}{c.reset()}{c.a1()} {'━' * (width - pad - len(text) - 3)}{c.reset()}"
