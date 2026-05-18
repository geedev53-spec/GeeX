#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Terminal Effects - Special visual effects."""

import time
import random
import shutil

def scanline_effect(duration=3.0):
    """CRT scanline effect."""
    cols, rows = shutil.get_terminal_size()
    print("\033[?25l", end='')

    try:
        start = time.time()
        while time.time() - start < duration:
            for row in range(rows):
                print(f"\033[{row};0H\033[48;2;0;10;20m{' ' * cols}\033[0m", end='', flush=True)
                time.sleep(0.02)
                print(f"\033[{row};0H\033[0m{' ' * cols}\033[0m", end='', flush=True)
    except KeyboardInterrupt:
        pass

    print("\033[?25h", end='')

def glitch_screen(duration=2.0):
    """Screen glitch effect."""
    chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
    cols, rows = shutil.get_terminal_size()

    try:
        start = time.time()
        while time.time() - start < duration:
            x = random.randint(0, cols-10)
            y = random.randint(0, rows-1)
            glitch = ''.join(random.choice(chars) for _ in range(random.randint(5, 15)))
            color = random.choice(['91', '92', '93', '94', '95', '96'])
            print(f"\033[{y};{x}H\033[{color}m{glitch}\033[0m", end='', flush=True)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    import os
    os.system('clear' if os.name != 'nt' else 'cls')

def neon_glow(text, pulses=3):
    """Neon glow text effect."""
    colors = [100, 150, 200, 255, 200, 150, 100]

    for _ in range(pulses):
        for intensity in colors:
            print(f"\r\033[38;2;0;{intensity};255m{text}\033[0m", end='', flush=True)
            time.sleep(0.06)
    print("")

def run_effect(name="scanline"):
    """Run named effect."""
    effects = {
        'scanline': scanline_effect,
        'glitch': glitch_screen,
        'neon': lambda: neon_glow("GEEX OS", 3),
    }
    effect = effects.get(name, scanline_effect)
    effect()
