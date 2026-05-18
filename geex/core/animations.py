#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Animation Engine
# =============================================================================
# Terminal animations including Matrix rain, glitch effects, cyberpunk
# loading screens, neon pulse effects, and smooth transitions.
# =============================================================================

import os
import sys
import time
import random
import shutil
import threading
from typing import List, Optional, Callable


class AnimationEngine:
    """GeeX OS Terminal Animation Engine"""
    
    def __init__(self, config=None):
        from geex.core.config import Config
        self.config = config or Config()
        self.enabled = self.config.get("animations_enabled", True)
        self._stop_event = threading.Event()
    
    def clear(self):
        """Clear terminal."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def sleep(self, duration: float):
        """Sleep with interrupt support."""
        self._stop_event.wait(duration)
    
    def matrix_rain(self, duration: float = 10.0, density: float = 0.05):
        """Matrix digital rain effect."""
        if not self.enabled:
            return
        
        chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEF"
        cols, rows = shutil.get_terminal_size()
        drops = [random.randint(-20, 0) for _ in range(cols)]
        
        start = time.time()
        try:
            while time.time() - start < duration:
                self._stop_event.wait(0.05)
                print('\033[H', end='')
                
                for row in range(rows):
                    line = []
                    for col in range(cols):
                        if random.random() < density:
                            char = random.choice(chars)
                            if drops[col] > row:
                                if row == drops[col] - 1:
                                    line.append(f'\033[97m{char}\033[0m')
                                elif row > drops[col] - 8:
                                    green = max(0, 255 - (drops[col] - row) * 30)
                                    line.append(f'\033[38;2;0;{green};0m{char}\033[0m')
                                else:
                                    line.append(f'\033[38;2;0;80;0m{char}\033[0m')
                            else:
                                line.append(' ')
                        else:
                            line.append(' ')
                    print(''.join(line[:cols]))
                
                for i in range(cols):
                    drops[i] += random.randint(0, 2)
                    if drops[i] > rows + 20:
                        drops[i] = random.randint(-10, 0)
        except KeyboardInterrupt:
            pass
        finally:
            self.clear()
    
    def boot_sequence(self, quick: bool = False):
        """GeeX OS BIOS-style boot sequence."""
        if not self.enabled:
            return
        
        sleep_time = 0.05 if quick else 0.15
        
        self.clear()
        
        # BIOS header
        boot_lines = [
            ("GEEX OS BIOS v2.0.0", 0),
            ("Copyright (C) 2025 GeeX Technologies", 0),
            ("", 0),
            ("CPU: ARM64 Virtual Processor @ 2.84GHz", 0.3),
            ("Memory Test: ", 0),
        ]
        
        for text, delay in boot_lines:
            print(f"\033[96m{text}\033[0m", end='', flush=True)
            if delay > 0:
                self._stop_event.wait(delay)
        
        # Memory test animation
        mem_total = 8192
        for i in range(0, mem_total + 512, 512):
            pct = (i / mem_total) * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"\r\033[96mMemory Test: \033[92m{bar}\033[96m {int(pct)}% ({i}K/{mem_total}K)\033[0m", end='', flush=True)
            self._stop_event.wait(sleep_time * 0.3)
        
        print("\n")
        
        # Hardware detection
        hw_checks = [
            ("Detecting storage devices...", "✓ Found 128GB eMMC"),
            ("Initializing network...", "✓ WiFi: Connected | LTE: Ready"),
            ("Loading kernel modules...", "✓ All modules loaded"),
            ("Mounting filesystems...", "✓ /data mounted"),
            ("Starting system services...", "✓ 12 services active"),
        ]
        
        for check, result in hw_checks:
            print(f"\033[96m{check}\033[0m", end='', flush=True)
            self._stop_event.wait(sleep_time)
            print(f" \033[92m{result}\033[0m")
        
        print("")
        
        # Loading GeeX OS
        phases = ["Loading core modules", "Initializing UI engine", "Mounting plugins", "Starting dashboard service"]
        for phase in phases:
            print(f"\033[96m{phase}...\033[0m", end='', flush=True)
            self._stop_event.wait(sleep_time * 1.5)
            print(" \033[92m[OK]\033[0m")
        
        self._stop_event.wait(0.3)
        self.clear()
    
    def loading_bar(self, label: str = "Loading", steps: int = 20, delay: float = 0.1):
        """Animated loading bar."""
        if not self.enabled:
            for i in range(steps + 1):
                time.sleep(delay)
            return
        
        width = 30
        for i in range(steps + 1):
            pct = int((i / steps) * 100)
            filled = int((i / steps) * width)
            bar = f"\033[96m{'█' * filled}\033[90m{'░' * (width - filled)}\033[0m"
            print(f"\r\033[96m{label}: \033[0m[{bar}] \033[92m{pct}%\033[0m", end='', flush=True)
            self._stop_event.wait(delay)
        print("")
    
    def spinner(self, label: str = "Working", duration: float = 2.0):
        """Animated spinner."""
        if not self.enabled:
            self._stop_event.wait(duration)
            return
        
        spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start = time.time()
        i = 0
        while time.time() - start < duration:
            char = spinners[i % len(spinners)]
            print(f"\r\033[96m{char}\033[0m \033[97m{label}...\033[0m", end='', flush=True)
            self._stop_event.wait(0.08)
            i += 1
        print(f"\r\033[92m✓\033[0m \033[97m{label} done!\033[0m{' ' * 20}")
    
    def typing_effect(self, text: str, speed: float = 0.03):
        """Typewriter text effect."""
        if not self.enabled:
            print(text)
            return
        
        for char in text:
            print(char, end='', flush=True)
            if char == ' ':
                self._stop_event.wait(speed * 0.5)
            else:
                self._stop_event.wait(speed)
        print("")
    
    def glitch_text(self, text: str, duration: float = 1.5):
        """Glitch text effect."""
        if not self.enabled:
            print(text)
            return
        
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        start = time.time()
        iterations = 0
        
        while time.time() - start < duration:
            iterations += 1
            glitched = list(text)
            for _ in range(random.randint(1, 3)):
                pos = random.randint(0, max(len(text) - 1, 0))
                glitched[pos] = random.choice(glitch_chars)
            
            color = random.choice(['91', '92', '93', '94', '95', '96', '97'])
            print(f"\r\033[{color}m{''.join(glitched)}\033[0m", end='', flush=True)
            self._stop_event.wait(0.05 if iterations > duration * 10 else 0.08)
        
        print(f"\r\033[96m{text}\033[0m{' ' * 10}")
    
    def neon_pulse(self, text: str, pulses: int = 3):
        """Neon pulse glow effect."""
        if not self.enabled:
            print(text)
            return
        
        colors = [
            (0, 150, 255), (0, 180, 255), (0, 200, 255),
            (50, 212, 255), (0, 200, 255), (0, 180, 255), (0, 150, 255)
        ]
        
        for _ in range(pulses):
            for r, g, b in colors:
                print(f"\r\033[38;2;{r};{g};{b}m{text}\033[0m", end='', flush=True)
                self._stop_event.wait(0.08)
        print("")
    
    def progress_bar(self, current: int, total: int, label: str = "", width: int = 30):
        """Draw a progress bar."""
        pct = min(100, int((current / max(total, 1)) * 100))
        filled = int((pct / 100) * width)
        
        colors = {
            'low': '\033[91m', 'mid': '\033[93m', 'high': '\033[92m', 'reset': '\033[0m'
        }
        c = colors['low'] if pct < 30 else (colors['mid'] if pct < 70 else colors['high'])
        
        bar = f"{'█' * filled}{'░' * (width - filled)}"
        print(f"\r{c}[{bar}]{colors['reset']} \033[97m{pct}%\033[0m {label}", end='', flush=True)
    
    def fade_in(self, text: str, duration: float = 0.5):
        """Fade in effect using ANSI brightness."""
        if not self.enabled:
            print(text)
            return
        
        steps = 10
        for i in range(1, steps + 1):
            intensity = int((i / steps) * 255)
            r, g, b = 0, min(212, intensity), min(255, intensity)
            print(f"\r\033[38;2;{r};{g};{b}m{text}\033[0m", end='', flush=True)
            self._stop_event.wait(duration / steps)
        print("")
    
    def cyber_scan(self, label: str = "Scanning", duration: float = 2.0):
        """Cyber scanning animation."""
        if not self.enabled:
            self._stop_event.wait(duration)
            return
        
        scan_chars = "▓▒░"
        width = 40
        start = time.time()
        
        while time.time() - start < duration:
            elapsed = time.time() - start
            pos = int((elapsed / duration) * width)
            line = ""
            for i in range(width):
                if i == pos:
                    line += f"\033[96m▓\033[0m"
                elif abs(i - pos) < 3:
                    line += f"\033[36m{random.choice(scan_chars)}\033[0m"
                else:
                    line += f"\033[90m░\033[0m"
            
            pct = int((elapsed / duration) * 100)
            print(f"\r\033[96m{label}: \033[0m[{line}] \033[92m{pct}%\033[0m", end='', flush=True)
            self._stop_event.wait(0.05)
        
        bar = "\033[92m█\033[0m" * width
        print(f"\r\033[96m{label}: \033[0m[{bar}] \033[92m100%\033[0m{' ' * 10}")
    
    def ascii_logo(self):
        """Print animated ASCII logo."""
        logo = [
            "    ██████╗ ███████╗███████╗██╗  ██╗     ██████╗ ███████╗   ",
            "   ██╔════╝ ██╔════╝██╔════╝╚██╗██╔╝     ██╔═══██╗██╔════╝   ",
            "   ██║  ███╗█████╗  █████╗   ╚███╔╝█████╗██║   ██║███████╗   ",
            "   ██║   ██║██╔══╝  ██╔══╝   ██╔██╗╚════╝██║   ██║╚════██║   ",
            "   ╚██████╔╝███████╗███████╗██╔╝ ██╗     ╚██████╔╝███████║   ",
            "    ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝      ╚═════╝ ╚══════╝   ",
        ]
        
        for i, line in enumerate(logo):
            color_intensity = int(150 + (i / len(logo)) * 105)
            print(f"\033[38;2;0;{color_intensity};255m{line}\033[0m")
            self._stop_event.wait(0.05)


def clear_animated():
    """Animated clear screen."""
    print('\033[?25l', end='')
    for i in range(25):
        print(f"\033[{i};0H\033[K\033[90m~\033[0m")
        time.sleep(0.01)
    print('\033[?25h', end='')
    os.system('clear' if os.name != 'nt' else 'cls')


def matrix_rain(duration: float = 10.0):
    """Standalone Matrix rain function."""
    AnimationEngine().matrix_rain(duration)


def boot_sequence(quick: bool = False):
    """Standalone boot sequence."""
    AnimationEngine().boot_sequence(quick)
