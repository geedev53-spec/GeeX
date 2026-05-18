#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Auto Completion - Command completion engine."""

class AutoCompletion:
    """GeeX OS Command Auto-Completion"""

    COMMANDS = [
        "info", "dashboard", "monitor", "doctor", "benchmark", "sysfetch",
        "update", "backup", "restore", "config", "clean", "reset", "help",
        "plugins", "theme", "ai", "network", "battery", "storage",
        "memory", "cpu", "terminal",
    ]

    def __init__(self):
        self.commands = self.COMMANDS

    def complete(self, partial):
        """Get completions for partial input."""
        partial = partial.lower()
        matches = [cmd for cmd in self.commands if cmd.startswith(partial)]
        return matches

    def suggest(self, query):
        """Suggest commands based on query."""
        query = query.lower()
        suggestions = []

        mapping = {
            "system": ["info", "sysfetch", "monitor", "doctor"],
            "hardware": ["cpu", "memory", "storage", "battery"],
            "config": ["config", "theme", "plugins", "backup"],
            "tools": ["network", "terminal", "benchmark"],
        }

        for keyword, cmds in mapping.items():
            if keyword in query:
                suggestions.extend(cmds)

        return suggestions if suggestions else self.commands[:5]

# Backwards compatibility
def get_completions(partial):
    """Get completions for partial input."""
    ac = AutoCompletion()
    return ac.complete(partial)
