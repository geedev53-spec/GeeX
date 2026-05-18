#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Backup Command - Configuration backup."""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class BackupCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.a2()}{t.bold()}💾 Backup Manager{t.reset()}\n")

        geex_dir = Path.home() / ".geex"
        backup_dir = geex_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = backup_dir / f"backup-{timestamp}"
        backup_path.mkdir(exist_ok=True)

        # Backup data
        data_dir = geex_dir / "data"
        if data_dir.exists():
            shutil.copytree(data_dir, backup_path / "data", dirs_exist_ok=True)

        # Backup config files
        for cfg_file in ["config.json", "themes.json", "plugins.json"]:
            src = data_dir / cfg_file
            if src.exists():
                shutil.copy2(src, backup_path / cfg_file)

        # Create backup manifest
        manifest = {
            "created": timestamp,
            "version": "2.0.0",
            "files": [str(f.name) for f in backup_path.iterdir()],
        }
        with open(backup_path / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"  {t.ok()}✓ Backup created: {backup_path}{t.reset()}")

        # List backups
        backups = sorted(backup_dir.iterdir())
        print(f"\n  {t.a1()}Available backups ({len(backups)}):{t.reset()}")
        for b in backups[-5:]:
            size = sum(f.stat().st_size for f in b.rglob("*") if f.is_file())
            print(f"    {t.fg_color()}{b.name:<25} {size/1024:.1f} KB{t.reset()}")
        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return BackupCommand(Config(), Theme()).run(args)
