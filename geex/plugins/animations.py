#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: Animations - Extra terminal animations."""

import time
import random
import shutil

class AnimationsPlugin:
    def __init__(self):
        self.name = "animations"
        self.version = "1.0.0"

    def stars(self, duration=10):
        """Star field animation."""
        cols, rows = shutil.get_terminal_size()
        stars = []

        for _ in range(50):
            stars.append({
                'x': random.randint(0, cols - 1),
                'y': random.randint(0, rows - 1),
                'brightness': random.random(),
            })

        start = time.time()
        try:
            while time.time() - start < duration:
                print('\033[H', end='')
                grid = [[' ' for _ in range(cols)] for _ in range(rows)]

                for star in stars:
                    chars = ['.', '*', '+', '✦']
                    idx = min(int(star['brightness'] * len(chars)), len(chars) - 1)
                    if 0 <= star['y'] < rows and 0 <= star['x'] < cols:
                        grid[star['y']][star['x']] = chars[idx]
                    star['brightness'] = (star['brightness'] + 0.1) % 1.0

                for row in grid:
                    print(''.join(row[:cols]))

                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

        os.system('clear' if os.name != 'nt' else 'cls')

def run():
    """Plugin entry point."""
    anim = AnimationsPlugin()
    anim.stars()

import os
if __name__ == "__main__":
    run()
