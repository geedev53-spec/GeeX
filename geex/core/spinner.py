#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Spinner - Terminal spinner animations."""

import time
import sys

class Spinner:
    """Terminal spinner with multiple styles."""

    STYLES = {
        'classic': ['|', '/', '-', '\\'],
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'pulse': ['◐', '◓', '◑', '◒'],
        'bounce': ['( ●    )', '(  ●   )', '(   ●  )', '(    ● )', '(     ●)', '(    ● )', '(   ●  )', '(  ●   )'],
    }

    def __init__(self, label="Loading", style="dots"):
        self.label = label
        self.chars = self.STYLES.get(style, self.STYLES['dots'])
        self.running = False
        self._index = 0

    def start(self):
        """Start spinner."""
        self.running = True
        try:
            while self.running:
                char = self.chars[self._index % len(self.chars)]
                print(f"\r  \033[96m{char}\033[0m \033[97m{self.label}...\033[0m", end='', flush=True)
                time.sleep(0.08)
                self._index += 1
        except KeyboardInterrupt:
            self.stop()

    def stop(self, message="Done"):
        """Stop spinner."""
        self.running = False
        print(f"\r  \033[92m✓\033[0m \033[97m{message}\033[0m{' ' * 30}")

# Backwards compatibility
def spin(label="Loading", duration=2.0, style="dots"):
    """Quick spinner."""
    spinner = Spinner(label, style)
    start = time.time()
    try:
        while time.time() - start < duration:
            char = spinner.chars[spinner._index % len(spinner.chars)]
            print(f"\r  \033[96m{char}\033[0m \033[97m{label}...\033[0m", end='', flush=True)
            time.sleep(0.08)
            spinner._index += 1
        print(f"\r  \033[92m✓\033[0m \033[97m{label} done!\033[0m{' ' * 20}")
    except KeyboardInterrupt:
        print("\r\033[91m✗ Cancelled\033[0m")
