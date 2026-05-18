#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Android - Android/Termux-specific utilities."""

import os
import subprocess
from pathlib import Path

class AndroidUtils:
    """Android and Termux utilities."""

    def is_termux(self):
        """Check if running in Termux."""
        return (
            'TERMUX_VERSION' in os.environ or
            os.path.exists('/data/data/com.termux') or
            os.environ.get('PREFIX', '').endswith('com.termux')
        )

    def get_android_version(self):
        """Get Android OS version."""
        try:
            result = subprocess.run(
                ['getprop', 'ro.build.version.release'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass

        try:
            with open('/system/build.prop', 'r') as f:
                for line in f:
                    if 'ro.build.version.release' in line:
                        return line.split('=')[-1].strip()
        except Exception:
            pass

        return "Unknown"

    def get_termux_version(self):
        """Get Termux app version."""
        return os.environ.get('TERMUX_VERSION', 'Unknown')

    def get_device_model(self):
        """Get device model."""
        try:
            result = subprocess.run(
                ['getprop', 'ro.product.model'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "Unknown"

    def get_battery_info(self):
        """Get battery information via termux-api."""
        try:
            result = subprocess.run(
                ['termux-battery-status'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.startswith('{'):
                import json
                return json.loads(result.stdout)
        except Exception:
            pass
        return None

# Backwards compatibility
def detect_android():
    """Quick Android detection."""
    utils = AndroidUtils()
    if utils.is_termux():
        print(f"Termux: v{utils.get_termux_version()}")
        print(f"Android: v{utils.get_android_version()}")
