#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Configuration Manager
# =============================================================================
# Advanced configuration system with JSON persistence, validation,
# interactive editing, and auto-save.
# =============================================================================

import os
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, List


class Config:
    """GeeX OS Configuration Manager"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self._config_dir = Path(config_dir) if config_dir else Path.home() / ".geex" / "data"
        self._config_dir.mkdir(parents=True, exist_ok=True)
        
        self._config_file = self._config_dir / "config.json"
        self._themes_file = self._config_dir / "themes.json"
        self._plugins_file = self._config_dir / "plugins.json"
        self._cache_file = self._config_dir / "cache.json"
        
        self._data = self._load_default()
        self._themes = self._load_default_themes()
        self._plugins = self._load_default_plugins()
        self._cache = {}
        
        self.load()
    
    def _load_default(self) -> dict:
        """Load default configuration."""
        geex_dir = str(Path.home() / ".geex")
        return {
            "version": "2.0.0",
            "first_run": True,
            "theme": "cyberpunk",
            "shell": "bash",
            "shell_rc": str(Path.home() / ".bashrc"),
            "startup_enabled": True,
            "startup_quick": True,
            "animations_enabled": True,
            "truecolor": True,
            "unicode": True,
            "sound": False,
            "auto_update_check": True,
            "update_channel": "stable",
            "backup_auto": True,
            "backup_keep": 5,
            "log_level": "INFO",
            "debug": False,
            "low_resource_mode": False,
            "dashboard_refresh": 2.0,
            "monitor_refresh": 1.0,
            "prompt": {
                "enabled": True,
                "style": "powerline",
                "show_time": True,
                "show_user": True,
                "show_host": True,
                "show_git": True,
                "show_battery": True,
                "show_cpu": False,
                "show_ram": False,
                "show_path": True,
                "show_exit_code": True,
                "newline": True,
                "color_scheme": "neon"
            },
            "paths": {
                "home": geex_dir,
                "os": f"{geex_dir}/os",
                "backups": f"{geex_dir}/backups",
                "themes": f"{geex_dir}/themes",
                "cache": f"{geex_dir}/cache",
                "logs": f"{geex_dir}/logs",
                "plugins": f"{geex_dir}/plugins",
                "data": f"{geex_dir}/data"
            },
            "aliases": {"ls": "fancy", "cat": "fancy", "grep": "colored", "clear": "animated"}
        }
    
    def _load_default_themes(self) -> dict:
        """Load default themes."""
        return {
            "active": "cyberpunk",
            "available": ["cyberpunk", "matrix", "ocean", "neon", "minimal", "hackerman"],
            "cyberpunk": {
                "name": "Cyberpunk", "bg": "#0a0a0f", "fg": "#00d4ff",
                "accent1": "#00d4ff", "accent2": "#ff00ff", "accent3": "#00ff88",
                "warning": "#ffaa00", "error": "#ff0044", "success": "#00ff88", "dim": "#555577"
            },
            "matrix": {
                "name": "Matrix", "bg": "#000000", "fg": "#00ff00",
                "accent1": "#00ff00", "accent2": "#00cc00", "accent3": "#55ff55",
                "warning": "#ffaa00", "error": "#ff0044", "success": "#00ff00", "dim": "#008800"
            },
            "ocean": {
                "name": "Ocean", "bg": "#001020", "fg": "#44aaff",
                "accent1": "#44aaff", "accent2": "#0088ff", "accent3": "#66ccff",
                "warning": "#ffcc00", "error": "#ff4466", "success": "#44ffaa", "dim": "#336688"
            },
            "neon": {
                "name": "Neon", "bg": "#0f0010", "fg": "#ff00ff",
                "accent1": "#ff00ff", "accent2": "#00ffff", "accent3": "#ffff00",
                "warning": "#ff8800", "error": "#ff0044", "success": "#00ff88", "dim": "#663366"
            },
            "minimal": {
                "name": "Minimal", "bg": "#1a1a1a", "fg": "#cccccc",
                "accent1": "#ffffff", "accent2": "#999999", "accent3": "#666666",
                "warning": "#ffaa00", "error": "#ff4444", "success": "#44ff44", "dim": "#555555"
            },
            "hackerman": {
                "name": "Hackerman", "bg": "#050505", "fg": "#00ff41",
                "accent1": "#00ff41", "accent2": "#008f11", "accent3": "#003b00",
                "warning": "#d4ff00", "error": "#ff0000", "success": "#00ff41", "dim": "#005500"
            }
        }
    
    def _load_default_plugins(self) -> dict:
        """Load default plugin configuration."""
        return {
            "ai_assistant": {"enabled": True, "config": {}},
            "cyberclock": {"enabled": True, "config": {"format": "24h", "show_seconds": True}},
            "weather": {"enabled": False, "config": {"location": "auto", "unit": "celsius"}},
            "network_scanner": {"enabled": False, "config": {}},
            "terminal_games": {"enabled": False, "config": {}},
            "productivity": {"enabled": True, "config": {}},
            "filesystem": {"enabled": True, "config": {}},
            "animations": {"enabled": True, "config": {}}
        }
    
    def load(self):
        """Load all configuration files."""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r') as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
        except Exception:
            pass
        
        try:
            if self._themes_file.exists():
                with open(self._themes_file, 'r') as f:
                    loaded = json.load(f)
                    self._themes.update(loaded)
        except Exception:
            pass
        
        try:
            if self._plugins_file.exists():
                with open(self._plugins_file, 'r') as f:
                    loaded = json.load(f)
                    self._plugins.update(loaded)
        except Exception:
            pass
        
        try:
            if self._cache_file.exists():
                with open(self._cache_file, 'r') as f:
                    self._cache = json.load(f)
        except Exception:
            pass
    
    def save(self):
        """Save all configuration files."""
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)
            with open(self._config_file, 'w') as f:
                json.dump(self._data, f, indent=2)
            with open(self._themes_file, 'w') as f:
                json.dump(self._themes, f, indent=2)
            with open(self._plugins_file, 'w') as f:
                json.dump(self._plugins, f, indent=2)
            with open(self._cache_file, 'w') as f:
                json.dump(self._cache, f, indent=2)
        except Exception as e:
            print(f"[Config] Warning: Could not save config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation supported)."""
        keys = key.split('.')
        value = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (dot notation supported)."""
        keys = key.split('.')
        target = self._data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        self.save()
    
    def get_theme(self, name: Optional[str] = None) -> dict:
        """Get theme configuration."""
        if name is None:
            name = self._themes.get("active", "cyberpunk")
        return self._themes.get(name, self._themes.get("cyberpunk", {}))
    
    def set_theme(self, name: str):
        """Set active theme."""
        if name in self._themes:
            self._themes["active"] = name
            self._data["theme"] = name
            self.save()
            return True
        return False
    
    def list_themes(self) -> List[str]:
        """List available themes."""
        return self._themes.get("available", ["cyberpunk"])
    
    def get_plugin(self, name: str) -> dict:
        """Get plugin configuration."""
        return self._plugins.get(name, {"enabled": False, "config": {}})
    
    def set_plugin(self, name: str, enabled: bool, config: dict = None):
        """Set plugin configuration."""
        if name not in self._plugins:
            self._plugins[name] = {"enabled": enabled, "config": config or {}}
        else:
            self._plugins[name]["enabled"] = enabled
            if config:
                self._plugins[name]["config"].update(config)
        self.save()
    
    def list_plugins(self) -> List[str]:
        """List available plugins."""
        return list(self._plugins.keys())
    
    def get_cache(self, key: str) -> Any:
        """Get cached value."""
        return self._cache.get(key)
    
    def set_cache(self, key: str, value: Any):
        """Set cached value."""
        self._cache[key] = value
        # Auto-save cache periodically
        if len(self._cache) % 5 == 0:
            self.save()
    
    def clear_cache(self):
        """Clear all cached data."""
        self._cache = {}
        self.save()
    
    def reset_to_defaults(self):
        """Reset all configuration to defaults."""
        self._data = self._load_default()
        self._themes = self._load_default_themes()
        self._plugins = self._load_default_plugins()
        self._cache = {}
        self.save()
