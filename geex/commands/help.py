#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Help Command"""

class HelpCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme
    
    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.a2()}{t.bold()}GeeX OS v2.0.0 - Available Commands{t.reset()}\n")
        
        groups = {
            "System": [
                ("info", "Show system information"),
                ("dashboard", "Interactive system dashboard"),
                ("monitor", "Live system monitor"),
                ("sysfetch", "Beautiful system info display"),
                ("doctor", "Diagnose and fix issues"),
                ("benchmark", "Performance benchmark"),
            ],
            "Hardware": [
                ("cpu", "CPU information and monitoring"),
                ("memory", "Memory/RAM information"),
                ("storage", "Storage/disk information"),
                ("battery", "Battery status and info"),
                ("network", "Network information"),
            ],
            "Configuration": [
                ("config", "Edit configuration settings"),
                ("theme", "Switch and manage themes"),
                ("plugins", "Manage plugins"),
                ("backup", "Backup configuration"),
                ("restore", "Restore from backup"),
                ("clean", "Clean cache and temp files"),
                ("reset", "Reset to defaults"),
                ("update", "Check for updates"),
            ],
            "Tools": [
                ("ai", "AI assistant and smart tips"),
                ("terminal", "Terminal enhancements"),
                ("help", "Show this help message"),
            ],
        }
        
        for group, commands in groups.items():
            print(f"  {t.a1()}{t.bold()}{group}{t.reset()}")
            for cmd, desc in commands:
                print(f"    {t.a2()}{cmd:<14}{t.reset()} {t.fg_color()}{desc}{t.reset()}")
            print("")
        
        print(f"  {t.dimmed()}Use 'geex <command> --help' for command-specific help{t.reset()}")
        print(f"  {t.dimmed()}Shortcuts: gxx=geex, gxinfo=geex info, gxdash=geex dashboard{t.reset()}\n")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return HelpCommand(Config(), Theme()).run(args)
