#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugins Command - Plugin manager."""

class PluginsCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        args = args or []

        if not args or args[0] == "list":
            print(f"\n  {t.a2()}{t.bold()}🔌 Plugins{t.reset()}\n")

            plugins = self.config._plugins
            for name, data in plugins.items():
                status = f"{t.ok()}ON{t.reset}" if data.get("enabled") else f"{t.err()}OFF{t.reset}"
                print(f"    {status}  {t.a2()}{name:<20}{t.reset()}")

            print(f"\n  {t.dimmed()}Usage: geex plugins enable <name> | geex plugins disable <name>{t.reset()}")
        elif args[0] == "enable" and len(args) > 1:
            self.config.set_plugin(args[1], True)
            print(f"  {t.ok()}✓ Plugin '{args[1]}' enabled{t.reset()}")
        elif args[0] == "disable" and len(args) > 1:
            self.config.set_plugin(args[1], False)
            print(f"  {t.ok()}✓ Plugin '{args[1]}' disabled{t.reset()}")
        else:
            print(f"  {t.err()}Unknown subcommand. Use 'list', 'enable', or 'disable'.{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return PluginsCommand(Config(), Theme()).run(args)
