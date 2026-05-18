#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Animations Engine - Low-level animation primitives."""

import time
import sys

class AnimationEngine:
    """Low-level terminal animation engine."""

    @staticmethod
    def move_cursor(x, y):
        """Move cursor to position."""
        print(f"\033[{y};{x}H", end='')

    @staticmethod
    def clear_line():
        """Clear current line."""
        print("\033[K", end='')

    @staticmethod
    def hide_cursor():
        """Hide cursor."""
        print("\033[?25l", end='')

    @staticmethod
    def show_cursor():
        """Show cursor."""
        print("\033[?25h", end='')

    @staticmethod
    def set_color(fg=None, bg=None):
        """Set ANSI color."""
        codes = []
        if fg:
            codes.append(f"38;5;{fg}")
        if bg:
            codes.append(f"48;5;{bg}")
        if codes:
            print(f"\033[{' ;'.join(codes)}m", end='')

    @staticmethod
    def reset():
        """Reset all attributes."""
        print("\033[0m", end='')

# Backwards compatibility
def animate_text(text, delay=0.03):
    """Type out text with animation."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("")
