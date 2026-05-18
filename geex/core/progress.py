#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Progress - Progress bar implementations."""

import time
import shutil

class ProgressBar:
    """Advanced progress bar with ETA and speed."""

    def __init__(self, total, label="Progress", width=None):
        self.total = total
        self.current = 0
        self.label = label
        self.width = width or (shutil.get_terminal_size()[0] - 30)
        self.start_time = time.time()

    def update(self, increment=1):
        """Update progress."""
        self.current += increment
        self._draw()

    def _draw(self):
        """Draw progress bar."""
        pct = min(1.0, self.current / max(self.total, 1))
        filled = int(pct * self.width)
        bar = f"{'█' * filled}{'░' * (self.width - filled)}"

        elapsed = time.time() - self.start_time
        if self.current > 0 and pct > 0:
            eta = elapsed / pct - elapsed
            eta_str = f"{eta:.0f}s"
        else:
            eta_str = "?s"

        color = "\033[92m" if pct > 0.9 else ("\033[93m" if pct > 0.5 else "\033[96m")
        print(f"\r  {self.label}: {color}[{bar}]\033[0m {pct*100:.1f}% ({self.current}/{self.total}) ETA: {eta_str}", 
              end='', flush=True)

    def finish(self):
        """Mark as complete."""
        self.current = self.total
        self._draw()
        print("")

# Backwards compatibility
def show_progress(current, total, label="Progress", width=30):
    """Quick progress bar."""
    pb = ProgressBar(total, label, width)
    pb.current = current
    pb._draw()
