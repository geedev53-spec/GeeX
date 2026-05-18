#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: CyberClock - Digital clock with cyberpunk styling."""

import time
import datetime

class CyberClockPlugin:
    def __init__(self):
        self.name = "cyberclock"
        self.version = "1.0.0"

    def display(self, format_24h=True, show_seconds=True):
        """Display digital clock."""
        digits = {
            '0': ['████','█  █','█  █','█  █','████'],
            '1': [' ██ ','█ █','  █','  █','████'],
            '2': ['████','   █','████','█   ','████'],
            '3': ['████','   █','████','   █','████'],
            '4': ['█  █','█  █','████','   █','   █'],
            '5': ['████','█   ','████','   █','████'],
            '6': ['████','█   ','████','█  █','████'],
            '7': ['████','   █','  █ ',' █  ','█   '],
            '8': ['████','█  █','████','█  █','████'],
            '9': ['████','█  █','████','   █','████'],
            ':': ['  ', '██', '  ', '██', '  '],
        }

        try:
            while True:
                now = datetime.datetime.now()
                if format_24h:
                    time_str = now.strftime("%H:%M:%S" if show_seconds else "%H:%M")
                else:
                    time_str = now.strftime("%I:%M:%S %p" if show_seconds else "%I:%M %p")

                print(f"\r\033[96m{'='*40}\033[0m", end='')
                print(f"\r\033[96m  {time_str}  \033[0m", end='', flush=True)
                time.sleep(0.5 if show_seconds else 1.0)
        except KeyboardInterrupt:
            print("\n")

def run():
    """Plugin entry point."""
    clock = CyberClockPlugin()
    clock.display()

if __name__ == "__main__":
    run()
