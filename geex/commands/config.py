#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Config Command - Interactive configuration editor."""

import json

class ConfigCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        args = args or []

        if not args:
            print(f"\n  {t.a2()}{t.bold()}⚙ Configuration{t.reset()}\n")
            print(f"  {t.a1()}Current settings:{t.reset()}\n")

            settings = [
                ("theme", self.config.get("theme", "cyberpunk"), "Active theme"),
                ("startup_enabled", self.config.get("startup_enabled", True), "Startup animation"),
                ("animations_enabled", self.config.get("animations_enabled", True), "Animations"),
                ("truecolor", self.config.get("truecolor", True), "True color support"),
                ("auto_update_check", self.config.get("auto_update_check", True), "Auto update check"),
                ("log_level", self.config.get("log_level", "INFO"), "Log level"),
                ("low_resource_mode", self.config.get("low_resource_mode", False), "Low resource mode"),
                ("dashboard_refresh", self.config.get("dashboard_refresh", 2.0), "Dashboard refresh (s)"),
            ]

            for key, value, desc in settings:
                print(f"    {t.a2()}{key:<25}{t.reset()} {t.fg_color()}{str(value):<15}{t.reset()} {t.dimmed()}{desc}{t.reset()}")

            print(f"\n  {t.dimmed()}Usage: geex config <key> <value>{t.reset()}")
            print(f"  {t.dimmed()}Example: geex config theme matrix{t.reset()}")
            print("")
            return 0

        if len(args) >= 2:
            key = args[0]
            value = args[1]

            # Convert value types
            if value.lower() in ("true", "yes", "1"):
                value = True
            elif value.lower() in ("false", "no", "0"):
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace(".", "").isdigit():
                value = float(value)

            self.config.set(key, value)
            print(f"  {t.ok()}✓ Set {key} = {value}{t.reset()}")
        else:
            # Show specific key
            value = self.config.get(args[0])
            print(f"  {t.a2()}{args[0]}{t.reset()} = {t.fg_color()}{value}{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return ConfigCommand(Config(), Theme()).run(args)
