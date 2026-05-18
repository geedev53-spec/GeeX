#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Startup Sequence
# =============================================================================
# Animated boot sequence, welcome dashboard, daily tips panel,
# and live status display on terminal startup.
# =============================================================================

import sys
import os
import time
import random
import datetime
from pathlib import Path


class Startup:
    """GeeX OS Startup Manager"""
    
    TIPS = [
        "Tip: Use 'geex dashboard' for a real-time system overview",
        "Tip: Press Ctrl+C anytime to cancel animations",
        "Tip: Run 'geex ai' for smart command suggestions",
        "Tip: Use 'geex monitor' to watch system resources live",
        "Tip: Customize your prompt with 'geex config prompt'",
        "Tip: Try different themes with 'geex theme list'",
        "Tip: Use 'geex benchmark' to test your device performance",
        "Tip: Plugins can be managed with 'geex plugins'",
        "Tip: Backup your config with 'geex backup'",
        "Tip: 'geex doctor' diagnoses common issues",
        "Tip: Use tab completion for faster command entry",
        "Tip: Add 'GEEX_NO_STARTUP=1' to skip startup animations",
        "Tip: Run 'geex sysfetch' for a beautiful system info display",
        "Tip: The network command shows real-time connection stats",
        "Tip: Use 'geex clean' to free up storage space",
    ]
    
    def __init__(self, config=None, logger=None):
        from geex.core.config import Config
        from geex.core.logger import Logger
        from geex.core.theme import Theme
        from geex.core.animations import AnimationEngine
        from geex.core.systeminfo import SystemInfo
        
        self.config = config or Config()
        self.logger = logger or Logger()
        self.theme = Theme(self.config)
        self.anim = AnimationEngine(self.config)
        self.sysinfo = SystemInfo()
    
    def run(self, quick: bool = False):
        """Run the full startup sequence."""
        if not self.config.get("startup_enabled", True):
            return
        
        self.logger.info("Startup sequence initiated")
        
        try:
            if not quick and self.config.get("startup_quick", True) == False:
                self.anim.boot_sequence(quick=False)
            else:
                self.anim.boot_sequence(quick=True)
            
            self._show_welcome()
            self._show_status_panel()
            self._show_tip()
            
        except KeyboardInterrupt:
            print("\n\033[96m[GeeX] \033[93mStartup interrupted. Welcome!\033[0m\n")
    
    def _show_welcome(self):
        """Display welcome message with logo."""
        t = self.theme
        
        print(f"\n{t.a1()}")
        print('    ╔═══════════════════════════════════════════════════════════╗')
        print('    ║                                                           ║')
        print('    ║              G E E X    O S    v 2 . 0 . 0                ║')
        print('    ║                                                           ║')
        print('    ║        The Futuristic Terminal Enhancement Framework        ║')
        print('    ║                                                           ║')
        print(f'    ╚═══════════════════════════════════════════════════════════╝{t.reset()}')
        
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%H:%M:%S")
        
        print(f"\n  {t.a1()}⏱{t.reset()}  {t.fg_color()}{time_str}{t.reset()}  {t.dimmed()}|{t.reset()}  {t.a2()}📅{t.reset()}  {t.fg_color()}{date_str}{t.reset()}")
    
    def _show_status_panel(self):
        """Display live system status panel."""
        t = self.theme
        
        try:
            # Get system info
            uname = os.uname()
            hostname = uname.nodename
            user = os.environ.get('USER', 'user')
            
            # Battery
            battery = self.sysinfo.get_battery()
            if battery:
                bat_icon = "🔋" if battery.get('plugged') else "🔋"
                bat_pct = battery.get('percentage', '?')
                bat_str = f"{bat_icon} {bat_pct}%"
            else:
                bat_str = "🔌 AC Power"
            
            # Storage
            storage = self.sysinfo.get_storage()
            storage_str = f"{storage.get('used_gb', 0):.1f}GB / {storage.get('total_gb', 0):.1f}GB"
            
            # Memory
            memory = self.sysinfo.get_memory()
            mem_str = f"{memory.get('used_mb', 0):.0f}MB / {memory.get('total_mb', 0):.0f}MB"
            
            # Uptime
            uptime = self.sysinfo.get_uptime()
            
            # Python version
            py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            
            # Terminal info
            term = os.environ.get('TERM', 'unknown')
            
            print(f"\n  {t.a1()}┌─ System Status ─────────────────────────────────────────┐{t.reset()}")
            print(f"  {t.a1()}│{t.reset()}  {t.a2()}👤{t.reset()} {t.fg_color()}{user}@{hostname:<20}{t.reset()} {t.a2()}🐍{t.reset()} Python {py_ver:<12} {t.a1()}│{t.reset()}")
            print(f"  {t.a1()}│{t.reset()}  {t.a2()}🔋{t.reset()} {t.fg_color()}{bat_str:<20}{t.reset()} {t.a2()}💾{t.reset()} {t.fg_color()}{storage_str:<15} {t.a1()}│{t.reset()}")
            print(f"  {t.a1()}│{t.reset()}  {t.a2()}🧠{t.reset()} {t.fg_color()}{mem_str:<20}{t.reset()} {t.a2()}⏰{t.reset()} {t.fg_color()}{uptime:<15} {t.a1()}│{t.reset()}")
            print(f"  {t.a1()}│{t.reset()}  {t.a2()}📟{t.reset()} {t.fg_color()}{term:<20}{t.reset()} {t.a2()}📱{t.reset()} {t.fg_color()}{'Termux' if self._is_termux() else 'Linux':<15} {t.a1()}│{t.reset()}")
            print(f"  {t.a1()}└──────────────────────────────────────────────────────────┘{t.reset()}")
            
        except Exception as e:
            self.logger.debug(f"Status panel error: {e}")
    
    def _show_tip(self):
        """Display a random daily tip."""
        t = self.theme
        tip = random.choice(self.TIPS)
        print(f"\n  {t.a3()}💡 {tip}{t.reset()}\n")
    
    def _is_termux(self) -> bool:
        """Detect Termux environment."""
        return (
            'TERMUX_VERSION' in os.environ or
            os.path.exists('/data/data/com.termux') or
            os.environ.get('PREFIX', '').endswith('com.termux')
        )
    
    def quick_startup(self):
        """Run quick startup (minimal)."""
        self.run(quick=True)


def main():
    """Entry point for startup script."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='Quick startup')
    parser.add_argument('--silent', action='store_true', help='Silent mode')
    args = parser.parse_args()
    
    startup = Startup()
    
    if args.silent:
        return
    
    startup.run(quick=args.quick)


if __name__ == "__main__":
    main()
