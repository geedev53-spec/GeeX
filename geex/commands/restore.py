#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Restore Command - Restore from backup."""

import os
import json
import shutil
from pathlib import Path

class RestoreCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.a2()}{t.bold()}📂 Restore Manager{t.reset()}\n")

        backup_dir = Path.home() / ".geex" / "backups"
        if not backup_dir.exists():
            print(f"  {t.err()}No backups found.{t.reset()}")
            return 1

        backups = sorted(backup_dir.iterdir())
        if not backups:
            print(f"  {t.err()}No backups found.{t.reset()}")
            return 1

        print(f"  {t.a1()}Available backups:{t.reset()}")
        for i, b in enumerate(backups, 1):
            print(f"    {t.a2()}[{i}]{t.reset()} {t.fg_color()}{b.name}{t.reset()}")

        choice = input(f"\n  {t.a1()}Select backup (number): {t.reset()}").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(backups):
                selected = backups[idx]
                data_dir = Path.home() / ".geex" / "data"

                # Restore
                src_data = selected / "data"
                if src_data.exists():
                    if data_dir.exists():
                        shutil.rmtree(data_dir)
                    shutil.copytree(src_data, data_dir)

                print(f"\n  {t.ok()}✓ Restored from {selected.name}{t.reset()}")
            else:
                print(f"  {t.err()}Invalid selection.{t.reset()}")
        except ValueError:
            print(f"  {t.err()}Invalid input.{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return RestoreCommand(Config(), Theme()).run(args)
