#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Notifications - Terminal notification system."""

import time

class NotificationManager:
    """Simple terminal notification manager."""

    def __init__(self, theme=None):
        from geex.core.config import Config
        from geex.core.theme import Theme
        self.theme = theme or Theme(Config())

    def notify(self, title, message, level="info"):
        """Show a notification."""
        t = self.theme
        colors = {
            "info": t.a1(),
            "success": t.ok(),
            "warning": t.warn(),
            "error": t.err(),
        }
        color = colors.get(level, t.a1())

        print(f"\n  {color}┌{'─' * (len(title) + 4)}┐{t.reset()}")
        print(f"  {color}│  {t.bold()}{title}  │{t.reset()}")
        print(f"  {color}├{'─' * (len(title) + 4)}┤{t.reset()}")
        print(f"  {color}│  {t.fg_color()}{message:<{len(title)}}  │{t.reset()}")
        print(f"  {color}└{'─' * (len(title) + 4)}┘{t.reset()}\n")

    def success(self, title, message):
        self.notify(title, message, "success")

    def warning(self, title, message):
        self.notify(title, message, "warning")

    def error(self, title, message):
        self.notify(title, message, "error")

# Backwards compatibility
def notify(title, message, level="info"):
    """Quick notification."""
    nm = NotificationManager()
    nm.notify(title, message, level)
