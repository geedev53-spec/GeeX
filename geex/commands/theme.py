#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Theme Command - Theme manager."""

class ThemeCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        args = args or []

        if not args or args[0] == "list":
            print(f"\n  {t.a2()}{t.bold()}🎨 Available Themes{t.reset()}\n")
            current = self.config.get("theme", "cyberpunk")
            for name in self.config.list_themes():
                marker = f"{t.ok()}●{t.reset}" if name == current else f"{t.dimmed()}○{t.reset}"
                print(f"    {marker} {t.a2()}{name:<12}{t.reset()} {t.dimmed()}{self._get_desc(name)}{t.reset()}")
            print(f"\n  {t.dimmed()}Usage: geex theme <name>{t.reset()}")
        elif args[0] == "preview":
            theme_name = args[1] if len(args) > 1 else self.config.get("theme")
            preview_theme = self.config.get_theme(theme_name)
            print(f"\n  Preview: {theme_name}")
            print(f"  Primary:   {preview_theme.get('fg', 'N/A')}")
            print(f"  Accent 1:  {preview_theme.get('accent1', 'N/A')}")
            print(f"  Accent 2:  {preview_theme.get('accent2', 'N/A')}")
            print(f"  Accent 3:  {preview_theme.get('accent3', 'N/A')}")
            print(f"  Success:   {preview_theme.get('success', 'N/A')}")
            print(f"  Warning:   {preview_theme.get('warning', 'N/A')}")
            print(f"  Error:     {preview_theme.get('error', 'N/A')}")
        else:
            theme_name = args[0]
            if self.theme.set_theme(theme_name):
                print(f"\n  {t.ok()}✓ Theme set to '{theme_name}'{t.reset()}")
            else:
                print(f"\n  {t.err()}✗ Theme '{theme_name}' not found{t.reset()}")
                print(f"  {t.dimmed()}Run 'geex theme list' to see available themes.{t.reset()}")

        print("")
        return 0

    def _get_desc(self, name):
        descs = {
            "cyberpunk": "Neon blue cyberpunk (default)",
            "matrix": "Green Matrix-style",
            "ocean": "Deep blue ocean",
            "neon": "Vibrant neon colors",
            "minimal": "Clean minimal design",
            "hackerman": "Classic hacker green",
        }
        return descs.get(name, "")

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return ThemeCommand(Config(), Theme()).run(args)
