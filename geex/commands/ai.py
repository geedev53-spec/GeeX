#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS AI Command - Smart assistant and tips."""

import random

class AICommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        args = args or []

        if not args:
            print(f"\n  {t.a2()}{t.bold()}🤖 GeeX AI Assistant{t.reset()}\n")

            tips = [
                "Use 'geex dashboard' for real-time system monitoring",
                "Press Ctrl+C to cancel any running animation",
                "Run 'geex benchmark' to test your device performance",
                "Use 'geex theme list' to see available themes",
                "Backup your config with 'geex backup' regularly",
                "'geex doctor' can diagnose and fix common issues",
                "Add GEEX_NO_STARTUP=1 to skip startup animations",
                "Use tab completion for faster command entry",
                "'geex sysfetch' shows a beautiful system overview",
                "Run 'geex clean' to free up storage space",
            ]

            tip = random.choice(tips)
            print(f"  {t.a3()}💡 Tip: {tip}{t.reset()}\n")

            # Smart suggestion based on context
            print(f"  {t.a1()}Smart Suggestions:{t.reset()}")
            print(f"    {t.fg_color()}• Try 'geex monitor' for live system stats{t.reset()}")
            print(f"    {t.fg_color()}• Try 'geex sysfetch' for system info{t.reset()}")
            print(f"    {t.fg_color()}• Try 'geex benchmark' to test performance{t.reset()}")
            print("")
        elif args[0] == "ask":
            query = " ".join(args[1:]) if len(args) > 1 else ""
            if query:
                print(f"\n  {t.a2()}🤖 Query: {query}{t.reset()}")
                print(f"  {t.dimmed()}I suggest trying these commands:{t.reset()}\n")

                suggestions = {
                    "system": ["geex info", "geex sysfetch", "geex monitor"],
                    "performance": ["geex benchmark", "geex cpu", "geex memory"],
                    "battery": ["geex battery", "geex doctor"],
                    "network": ["geex network"],
                    "storage": ["geex storage", "geex clean"],
                    "update": ["geex update"],
                    "help": ["geex help"],
                }

                found = False
                for keyword, cmds in suggestions.items():
                    if keyword in query.lower():
                        for cmd in cmds:
                            print(f"    {t.a2()}  {cmd}{t.reset()}")
                        found = True
                        break

                if not found:
                    print(f"    {t.fg_color()}  geex help{t.reset()} - See all commands")
            else:
                print(f"  {t.err()}Please provide a question. Example: geex ask how to check battery{t.reset()}")
        else:
            print(f"  {t.a1()}Usage: geex ai [ask <question>]{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return AICommand(Config(), Theme()).run(args)
