#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: Productivity - Timer and productivity tools."""

import time
import datetime

class ProductivityPlugin:
    def __init__(self):
        self.name = "productivity"
        self.version = "1.0.0"

    def pomodoro(self, work=25, break_time=5):
        """Pomodoro timer."""
        print(f"\033[96m🍅 Pomodoro Timer\033[0m")
        print(f"\033[94mWork: {work}min | Break: {break_time}min\033[0m\n")

        # Work session
        print(f"\033[92m▶ Work session started! ({work} min)\033[0m")
        self._countdown(work * 60, "\033[92mWork\033[0m")

        # Break
        print(f"\n\033[93m☕ Break time! ({break_time} min)\033[0m")
        self._countdown(break_time * 60, "\033[93mBreak\033[0m")

        print(f"\n\033[92m✓ Pomodoro complete!\033[0m\n")

    def _countdown(self, seconds, label):
        """Countdown timer."""
        for remaining in range(seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\r  {label}: {mins:02d}:{secs:02d}", end='', flush=True)
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n\033[91mCancelled\033[0m")
                return
        print("")

    def timer(self, seconds=60):
        """Simple countdown timer."""
        print(f"\033[96m⏱ Timer: {seconds} seconds\033[0m\n")
        self._countdown(seconds, "\033[96mTimer\033[0m")
        print(f"\033[92m⏰ Time's up!\033[0m\n")

def run():
    """Plugin entry point."""
    prod = ProductivityPlugin()
    print("\033[96m📋 Productivity Tools\033[0m\n")
    print("  \033[941. Pomodoro Timer\033[0m")
    print("  \033[94m2. Countdown Timer\033[0m")

    choice = input("\n\033[93mChoose (1-2): \033[0m").strip()

    if choice == "1":
        prod.pomodoro()
    elif choice == "2":
        seconds = int(input("\033[93mSeconds: \033[0m").strip() or "60")
        prod.timer(seconds)

if __name__ == "__main__":
    run()
