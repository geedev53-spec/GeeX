#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Installer Core - Installation logic shared between installer and setup."""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

class InstallerCore:
    """Core installation functionality."""

    GEEX_VERSION = "2.0.0"
    REQUIRED_PACKAGES = ['rich', 'psutil', 'colorama', 'pygments']

    def __init__(self):
        self.geex_dir = Path.home() / ".geex"
        self.install_dir = self.geex_dir / "os"
        self.is_termux = self._detect_termux()
        self.shell = os.path.basename(os.environ.get('SHELL', 'bash'))

    def _detect_termux(self):
        return (
            'TERMUX_VERSION' in os.environ or
            os.path.exists('/data/data/com.termux') or
            os.environ.get('PREFIX', '').endswith('com.termux')
        )

    def check_python(self):
        """Verify Python 3.7+ is available."""
        if sys.version_info < (3, 7):
            print("[ERROR] Python 3.7+ required")
            return False
        return True

    def install_dependencies(self):
        """Install required Python packages."""
        for pkg in self.REQUIRED_PACKAGES:
            try:
                __import__(pkg)
            except ImportError:
                print(f"[INFO] Installing {pkg}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', pkg], 
                              capture_output=True)

    def setup_directories(self):
        """Create directory structure."""
        dirs = ['os', 'data', 'backups', 'cache', 'logs', 'plugins', 'themes']
        for d in dirs:
            (self.geex_dir / d).mkdir(parents=True, exist_ok=True)

    def create_configs(self):
        """Create default configuration files."""
        from geex.core.config import Config
        config = Config()
        config.save()

# Backwards compatibility
def install():
    """Run core installation steps."""
    core = InstallerCore()
    if core.check_python():
        core.install_dependencies()
        core.setup_directories()
        core.create_configs()
        print("[OK] Core installation complete")
