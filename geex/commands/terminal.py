#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Terminal Command - Terminal enhancements."""

import os
import sys

class TerminalCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        args = args or []

        if not args:
            print(f"\n  {t.a2()}{t.bold()}📟 Terminal Tools{t.reset()}\n")
            print(f"  {t.a1()}Available commands:{t.reset()}")
            print(f"    {t.a2()}geex terminal matrix{t.reset()}  - Matrix rain effect")
            print(f"    {t.a2()}geex terminal clear{t.reset()}   - Animated clear")
            print(f"    {t.a2()}geex terminal logo{t.reset()}    - Show GeeX logo")
        elif args[0] == "matrix":
            from geex.core.animations import matrix_rain
            matrix_rain(duration=10.0)
        elif args[0] == "clear":
            from geex.core.animations import clear_animated
            clear_animated()
        elif args[0] == "logo":
            self.theme.print_banner()
        else:
            print(f"  {t.err()}Unknown subcommand: {args[0]}{t.reset()}")

        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return TerminalCommand(Config(), Theme()).run(args)

def fancy_ls():
    """Enhanced ls with colors."""
    os.system("ls --color=auto -la")

def fancy_cat(filename=None):
    """Syntax highlighted cat."""
    if filename:
        filename = filename.replace(">>>", " ")
        for f in filename.split():
            if os.path.exists(f):
                # Try syntax highlighting
                try:
                    from pygments import highlight
                    from pygments.lexers import guess_lexer_for_filename
                    from pygments.formatters import TerminalFormatter
                    with open(f, 'r') as file:
                        content = file.read()
                        lexer = guess_lexer_for_filename(f, content)
                        print(highlight(content, lexer, TerminalFormatter()))
                except Exception:
                    with open(f, 'r') as file:
                        print(file.read())

def extract_archive(filename=None):
    """Extract various archive formats."""
    if not filename:
        print("Usage: extract <archive_file>")
        return
    filename = filename.replace(">>>", " ")
    for f in filename.split():
        if os.path.exists(f):
            if f.endswith('.tar.gz') or f.endswith('.tgz'):
                os.system(f"tar -xzf '{f}'")
            elif f.endswith('.tar.bz2'):
                os.system(f"tar -xjf '{f}'")
            elif f.endswith('.zip'):
                os.system(f"unzip '{f}'")
            elif f.endswith('.tar'):
                os.system(f"tar -xf '{f}'")
            else:
                print(f"Unknown archive format: {f}")

def mkcd(dirname=None):
    """Create directory and cd into it."""
    if dirname:
        os.makedirs(dirname, exist_ok=True)
        os.chdir(dirname)
        print(f"Created and entered: {os.getcwd()}")
