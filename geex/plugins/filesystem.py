#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: Filesystem - File management tools."""

import os
from pathlib import Path

class FilesystemPlugin:
    def __init__(self):
        self.name = "filesystem"
        self.version = "1.0.0"

    def du(self, path=".", max_depth=1):
        """Disk usage by directory."""
        target = Path(path)
        if not target.exists():
            print(f"\033[91mPath not found: {path}\033[0m")
            return

        sizes = []
        for item in target.iterdir():
            try:
                if item.is_dir() and max_depth > 0:
                    size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                    sizes.append((size, item.name, 'dir'))
                elif item.is_file():
                    sizes.append((item.stat().st_size, item.name, 'file'))
            except PermissionError:
                continue

        sizes.sort(reverse=True)

        print(f"\033[96m📁 {target.absolute()}\033[0m\n")
        for size, name, type_ in sizes[:20]:
            icon = '📁' if type_ == 'dir' else '📄'
            size_str = self._human_size(size)
            color = "\033[97m" if type_ == 'dir' else "\033[94m"
            print(f"  {icon} {color}{name:<30}\033[0m {size_str:>10}")

    def _human_size(self, size_bytes):
        """Convert bytes to human readable."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

    def find_large_files(self, path=".", min_size_mb=10):
        """Find large files."""
        target = Path(path)
        min_bytes = min_size_mb * 1024 * 1024

        print(f"\033[96m🔍 Files > {min_size_mb}MB in {target.absolute()}\033[0m\n")

        found = []
        for f in target.rglob("*"):
            try:
                if f.is_file() and f.stat().st_size > min_bytes:
                    found.append((f.stat().st_size, f))
            except (PermissionError, OSError):
                continue

        found.sort(reverse=True)

        for size, f in found[:20]:
            print(f"  \033[94m{self._human_size(size):>10}\033[0m  \033[97m{f}\033[0m")

def run():
    """Plugin entry point."""
    fs = FilesystemPlugin()
    fs.du()

if __name__ == "__main__":
    run()
