#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Restore - Configuration restore manager."""

import os
import shutil
from pathlib import Path

class RestoreManager:
    """Restore GeeX OS configuration from backups."""

    def __init__(self):
        self.geex_dir = Path.home() / ".geex"
        self.backup_dir = self.geex_dir / "backups"

    def get_available_backups(self):
        """Get list of available backups."""
        if not self.backup_dir.exists():
            return []
        return sorted(self.backup_dir.iterdir())

    def restore(self, backup_name):
        """Restore from named backup."""
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            return False

        data_backup = backup_path / "data"
        data_current = self.geex_dir / "data"

        if data_backup.exists():
            if data_current.exists():
                shutil.rmtree(data_current)
            shutil.copytree(data_backup, data_current)
            return True
        return False

# Backwards compatibility
def list_backups():
    """List available backups."""
    manager = RestoreManager()
    for b in manager.get_available_backups():
        print(f"  {b.name}")
