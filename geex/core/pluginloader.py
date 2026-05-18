#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Plugin Loader - Plugin discovery and loading system."""

import os
import sys
import importlib
from pathlib import Path

class PluginLoader:
    """GeeX OS Plugin System"""

    PLUGIN_DIR = Path.home() / ".geex" / "plugins"

    def __init__(self):
        self.plugins = {}
        self.loaded = {}

    def discover(self):
        """Discover available plugins."""
        # Built-in plugins
        builtin_dir = Path(__file__).parent.parent / "plugins"
        if builtin_dir.exists():
            for f in builtin_dir.glob("*.py"):
                if not f.name.startswith('_'):
                    self.plugins[f.stem] = {'path': str(f), 'builtin': True}

        # User plugins
        if self.PLUGIN_DIR.exists():
            for f in self.PLUGIN_DIR.glob("*.py"):
                if not f.name.startswith('_'):
                    self.plugins[f.stem] = {'path': str(f), 'builtin': False}

        return list(self.plugins.keys())

    def load(self, name):
        """Load a plugin by name."""
        if name not in self.plugins:
            return None

        try:
            spec = importlib.util.spec_from_file_location(
                f"geex_plugin_{name}", 
                self.plugins[name]['path']
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.loaded[name] = module
            return module
        except Exception as e:
            print(f"[Plugin] Error loading {name}: {e}")
            return None

    def run(self, name):
        """Run a plugin."""
        if name not in self.loaded:
            self.load(name)

        if name in self.loaded:
            module = self.loaded[name]
            if hasattr(module, 'run'):
                module.run()
            elif hasattr(module, 'main'):
                module.main()

# Backwards compatibility
def list_plugins():
    """List available plugins."""
    loader = PluginLoader()
    for name in loader.discover():
        print(f"  {name}")
