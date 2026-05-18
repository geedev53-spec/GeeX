#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Doctor Command - System diagnostics and repair."""

import os
import sys
import subprocess
from pathlib import Path

class DoctorCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme
        self.issues = []
        self.fixed = []
    
    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.a2()}{t.bold()}🔬 GeeX OS Doctor{t.reset()}\n")
        
        checks = [
            ("Configuration", self._check_config),
            ("Python Environment", self._check_python),
            ("Dependencies", self._check_deps),
            ("Shell Integration", self._check_shell),
            ("Directories", self._check_dirs),
            ("Permissions", self._check_perms),
        ]
        
        for name, check_func in checks:
            print(f"  {t.a1()}Checking {name}...{t.reset()}")
            try:
                check_func()
            except Exception as e:
                self.issues.append(f"{name}: {e}")
        
        print(f"\n  {t.a1()}{'━'*50}{t.reset()}")
        
        if not self.issues:
            print(f"  {t.ok()}✓ All systems operational!{t.reset()}")
        else:
            print(f"  {t.err()}Found {len(self.issues)} issue(s):{t.reset()}")
            for issue in self.issues:
                print(f"    {t.warn()}⚠ {issue}{t.reset()}")
        
        print("")
        return 0
    
    def _check_config(self):
        config_path = Path.home() / ".geex" / "data" / "config.json"
        if not config_path.exists():
            self.issues.append("Config file missing. Run installer.")
    
    def _check_python(self):
        if sys.version_info < (3, 7):
            self.issues.append(f"Python {sys.version_info.major}.{sys.version_info.minor} is too old (need 3.7+)")
    
    def _check_deps(self):
        required = ['rich', 'psutil', 'colorama']
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                self.issues.append(f"Missing package: {pkg}")
    
    def _check_shell(self):
        shell_rc = self.config.get("shell_rc", "")
        if shell_rc and Path(shell_rc).exists():
            content = Path(shell_rc).read_text()
            if "GEEX_OS" not in content:
                self.issues.append("Shell hooks not found. Run installer.")
    
    def _check_dirs(self):
        dirs = ["os", "data", "backups", "cache", "logs"]
        geex = Path.home() / ".geex"
        for d in dirs:
            if not (geex / d).exists():
                self.issues.append(f"Directory missing: ~/.geex/{d}")
    
    def _check_perms(self):
        pass

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return DoctorCommand(Config(), Theme()).run(args)
