#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Reset Command - Reset to defaults."""

class ResetCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.warn()}⚠ This will reset ALL settings to defaults!{t.reset()}")
        confirm = input(f"  {t.err()}Type 'reset' to confirm: {t.reset()}").strip()

        if confirm == "reset":
            self.config.reset_to_defaults()
            print(f"\n  {t.ok()}✓ All settings reset to defaults.{t.reset()}")
        else:
            print(f"\n  {t.a1()}Cancelled.{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return ResetCommand(Config(), Theme()).run(args)
