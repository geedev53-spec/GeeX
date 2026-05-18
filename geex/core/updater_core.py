#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Updater Core - Update logic shared with updater."""

import os
import json
import urllib.request
from pathlib import Path

class UpdaterCore:
    """Core update functionality."""

    CURRENT_VERSION = "2.0.0"
    GITHUB_API = "https://api.github.com/repos/geexos/GeeX-OS/releases/latest"

    def check_internet(self):
        """Check internet connectivity."""
        try:
            urllib.request.urlopen('https://github.com', timeout=5)
            return True
        except Exception:
            return False

    def get_latest_version(self):
        """Get latest release info from GitHub."""
        try:
            req = urllib.request.Request(
                self.GITHUB_API,
                headers={'User-Agent': 'GeeX-OS'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception:
            return None

# Backwards compatibility
def check_update():
    """Quick update check."""
    updater = UpdaterCore()
    if updater.check_internet():
        data = updater.get_latest_version()
        if data:
            print(f"Latest release: {data.get('tag_name', 'unknown')}")
