#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Clean Command - Clean cache and temp files."""

import os
import shutil
from pathlib import Path

class CleanCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.a2()}{t.bold()}🧹 System Cleaner{t.reset()}\n")

        freed = 0

        # Clean GeeX cache
        cache_dir = Path.home() / ".geex" / "cache"
        if cache_dir.exists():
            size = sum(f.stat().st_size for f in cache_dir.rglob("*") if f.is_file())
            for f in cache_dir.iterdir():
                if f.is_file():
                    f.unlink()
                elif f.is_dir():
                    shutil.rmtree(f)
            freed += size
            print(f"  {t.ok()}✓ Cleaned GeeX cache ({size/1024:.1f} KB){t.reset()}")

        # Clean Python cache
        for pattern in ["__pycache__", "*.pyc", "*.pyo"]:
            os.system(f"find {Path.home()}/.geex -type d -name '__pycache__' -exec rm -rf {{}} + 2>/dev/null")

        print(f"\n  {t.a2()}{t.bold()}Total freed: {freed/1024:.1f} KB{t.reset()}")
        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return CleanCommand(Config(), Theme()).run(args)
