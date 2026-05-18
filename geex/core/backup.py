#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Backup - Configuration backup manager."""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class BackupManager:
    """Manage GeeX OS configuration backups."""

    def __init__(self):
        self.geex_dir = Path.home() / ".geex"
        self.backup_dir = self.geex_dir / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, name=None):
        """Create a new backup."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        name = name or f"backup-{timestamp}"
        backup_path = self.backup_dir / name
        backup_path.mkdir(exist_ok=True)

        # Backup data directory
        data_dir = self.geex_dir / "data"
        if data_dir.exists():
            shutil.copytree(data_dir, backup_path / "data", dirs_exist_ok=True)

        # Create manifest
        manifest = {
            "created": timestamp,
            "version": "2.0.0",
            "name": name,
        }
        with open(backup_path / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        return backup_path

    def list_backups(self):
        """List all backups."""
        if not self.backup_dir.exists():
            return []
        return sorted(self.backup_dir.iterdir())

    def restore_backup(self, name):
        """Restore from a backup."""
        backup_path = self.backup_dir / name
        if not backup_path.exists():
            return False

        data_dir = self.geex_dir / "data"
        src_data = backup_path / "data"

        if src_data.exists():
            if data_dir.exists():
                shutil.rmtree(data_dir)
            shutil.copytree(src_data, data_dir)
            return True

        return False

# Backwards compatibility
def backup():
    """Quick backup."""
    manager = BackupManager()
    path = manager.create_backup()
    print(f"[OK] Backup created: {path}")
