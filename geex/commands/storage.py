#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Storage Command - Disk usage info."""

import os

class StorageCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        from geex.core.systeminfo import SystemInfo
        si = SystemInfo()
        storage = si.get_storage()

        print(f"\n  {t.a2()}{t.bold()}💾 Storage{t.reset()}\n")

        total = storage.get('total_gb', 0)
        used = storage.get('used_gb', 0)
        free = storage.get('free_gb', 0)
        pct = storage.get('percent', 0)

        # Visual bar
        width = 40
        filled = int((pct / 100) * width)
        color = t.ok() if pct < 70 else (t.warn() if pct < 90 else t.err())
        bar = f"{'█' * filled}{'░' * (width - filled)}"

        print(f"  {t.a1()}Usage:{t.reset}  {color}{bar}{t.reset()} {pct:.1f}%")
        print(f"\n  {t.a1()}Total:{t.reset}  {t.fg_color()}{total:.1f} GB{t.reset()}")
        print(f"  {t.a1()}Used:{t.reset}   {t.fg_color()}{used:.1f} GB{t.reset()}")
        print(f"  {t.a1()}Free:{t.reset}   {t.fg_color()}{free:.1f} GB{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return StorageCommand(Config(), Theme()).run(args)
