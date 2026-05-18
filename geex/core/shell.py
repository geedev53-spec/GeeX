#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Shell Integration & Command Dispatcher
# =============================================================================
# Main command router, shell hook integration, and interactive mode.
# =============================================================================

import sys
import os
import argparse
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(SCRIPT_DIR))


class ShellIntegration:
    """GeeX OS Shell Integration Manager"""
    
    def __init__(self, config=None):
        from geex.core.config import Config
        from geex.core.theme import Theme
        self.config = config or Config()
        self.theme = Theme(self.config)
    
    def initialize(self):
        """Initialize shell integration."""
        pass  # Shell hooks are added by installer
    
    def get_prompt_command(self, exit_code: int = 0) -> str:
        """Generate shell prompt string."""
        from geex.core.prompt import PromptBuilder
        builder = PromptBuilder(self.config)
        return builder.build(exit_code)


class CommandDispatcher:
    """GeeX OS Command Router"""
    
    COMMANDS = {
        "info": ("geex.commands.info", "InfoCommand", "System information"),
        "dashboard": ("geex.commands.monitor", "MonitorCommand", "Interactive dashboard"),
        "monitor": ("geex.commands.monitor", "MonitorCommand", "Live system monitor"),
        "doctor": ("geex.commands.doctor", "DoctorCommand", "System diagnostics"),
        "benchmark": ("geex.commands.benchmark", "BenchmarkCommand", "Performance benchmark"),
        "sysfetch": ("geex.commands.sysfetch", "SysfetchCommand", "System fetch display"),
        "update": ("geex.commands.update", "UpdateCommand", "Update checker"),
        "backup": ("geex.commands.backup", "BackupCommand", "Backup manager"),
        "restore": ("geex.commands.restore", "RestoreCommand", "Restore from backup"),
        "config": ("geex.commands.config", "ConfigCommand", "Configuration editor"),
        "clean": ("geex.commands.clean", "CleanCommand", "System cleaner"),
        "reset": ("geex.commands.reset", "ResetCommand", "Reset to defaults"),
        "help": ("geex.commands.help", "HelpCommand", "Show help"),
        "plugins": ("geex.commands.plugins", "PluginsCommand", "Plugin manager"),
        "theme": ("geex.commands.theme", "ThemeCommand", "Theme manager"),
        "ai": ("geex.commands.ai", "AICommand", "AI assistant"),
        "network": ("geex.commands.network", "NetworkCommand", "Network tools"),
        "battery": ("geex.commands.battery", "BatteryCommand", "Battery info"),
        "storage": ("geex.commands.storage", "StorageCommand", "Storage info"),
        "memory": ("geex.commands.memory", "MemoryCommand", "Memory info"),
        "cpu": ("geex.commands.cpu", "CPUCommand", "CPU info"),
        "terminal": ("geex.commands.terminal", "TerminalCommand", "Terminal enhancements"),
    }
    
    ALIASES = {
        "i": "info", "d": "dashboard", "dash": "dashboard",
        "m": "monitor", "mon": "monitor", "top": "monitor",
        "doc": "doctor", "bench": "benchmark", "fetch": "sysfetch",
        "u": "update", "bak": "backup", "rest": "restore",
        "cfg": "config", "conf": "config", "h": "help",
        "p": "plugins", "t": "theme", "th": "theme",
        "net": "network", "bat": "battery", "sto": "storage",
        "mem": "memory", "ram": "memory", "term": "terminal",
    }
    
    def __init__(self):
        from geex.core.config import Config
        from geex.core.theme import Theme
        self.config = Config()
        self.theme = Theme(self.config)
    
    def resolve_command(self, name: str) -> str:
        """Resolve command name including aliases."""
        if name in self.ALIASES:
            return self.ALIASES[name]
        return name
    
    def dispatch(self, command: str, args: list) -> int:
        """Dispatch command to handler."""
        command = self.resolve_command(command)
        
        if command not in self.COMMANDS:
            self._unknown_command(command)
            return 1
        
        module_path, class_name, _ = self.COMMANDS[command]
        
        try:
            # Dynamic import
            module = __import__(module_path, fromlist=[class_name])
            handler_class = getattr(module, class_name)
            handler = handler_class(self.config, self.theme)
            
            if hasattr(handler, "run"):
                return handler.run(args) or 0
            elif hasattr(handler, "main"):
                return handler.main(args) or 0
            else:
                print(f"[GeeX] Command '{command}' has no run() method.")
                return 1
                
        except ImportError as e:
            print(f"[GeeX] Error loading command '{command}': {e}")
            return 1
        except Exception as e:
            print(f"[GeeX] Command '{command}' failed: {e}")
            return 1
    
    def _unknown_command(self, command: str):
        """Handle unknown command."""
        t = self.theme
        print(f"\n{t.err()}[GeeX]{t.reset()} Unknown command: '{command}'")
        
        # Suggest similar commands
        similar = self._find_similar(command)
        if similar:
            print(f"\n{t.a1()}Did you mean?{t.reset()}")
            for cmd in similar[:3]:
                _, _, desc = self.COMMANDS[cmd]
                print(f"  {t.a2()}  {cmd:<12}{t.reset()} {t.dimmed()}{desc}{t.reset()}")
        
        print(f"\n{t.dimmed()}Run 'geex help' for all available commands.{t.reset()}\n")
    
    def _find_similar(self, command: str) -> list:
        """Find similar command names."""
        from difflib import get_close_matches
        all_names = list(self.COMMANDS.keys()) + list(self.ALIASES.keys())
        return get_close_matches(command, all_names, n=3, cutoff=0.4)
    
    def list_commands(self) -> dict:
        """Return all available commands."""
        return {k: v[2] for k, v in self.COMMANDS.items()}


def main():
    """Main entry point for CLI."""
    # Check if called as prompt generator
    if len(sys.argv) >= 2 and sys.argv[1] == '--prompt':
        try:
            exit_code = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            from geex.core.prompt import PromptBuilder
            from geex.core.config import Config
            builder = PromptBuilder(Config())
            print(builder.build(exit_code))
            return 0
        except Exception:
            return 1
    
    # Normal command dispatch
    if len(sys.argv) < 2:
        # No command - show interactive menu
        _interactive_mode()
        return 0
    
    # Global flags
    if sys.argv[1] in ('-v', '--version'):
        print("GeeX OS v2.0.0")
        return 0
    
    if sys.argv[1] in ('-h', '--help'):
        from geex.commands.help import HelpCommand
        from geex.core.config import Config
        from geex.core.theme import Theme
        HelpCommand(Config(), Theme()).run([])
        return 0
    
    if sys.argv[1] in ('-b', '--banner'):
        from geex.core.theme import Theme
        from geex.core.config import Config
        Theme(Config()).print_banner()
        return 0
    
    # Dispatch command
    dispatcher = CommandDispatcher()
    command = sys.argv[1]
    args = sys.argv[2:]
    
    return dispatcher.dispatch(command, args)


def _interactive_mode():
    """Run interactive mode with menu."""
    from geex.core.config import Config
    from geex.core.theme import Theme
    from geex.core.animations import AnimationEngine
    
    config = Config()
    theme = Theme(config)
    anim = AnimationEngine(config)
    
    theme.print_banner()
    
    dispatcher = CommandDispatcher()
    commands = dispatcher.list_commands()
    
    print(f"\n  {theme.a1()}Available Commands:{theme.reset()}\n")
    
    # Group commands
    groups = {
        "System": ["info", "dashboard", "monitor", "doctor", "benchmark", "sysfetch"],
        "Tools": ["network", "battery", "storage", "memory", "cpu", "terminal"],
        "Config": ["config", "theme", "plugins", "backup", "restore", "clean", "reset"],
        "Other": ["ai", "update", "help"],
    }
    
    for group, cmds in groups.items():
        print(f"  {theme.a2()}{group}:{theme.reset()}")
        for cmd in cmds:
            if cmd in commands:
                print(f"    {theme.a1()}{cmd:<12}{theme.reset()} {theme.dimmed()}{commands[cmd]}{theme.reset()}")
        print("")
    
    print(f"  {theme.dimmed()}Run 'geex <command>' to execute, or 'geex help' for details.{theme.reset()}\n")


if __name__ == "__main__":
    sys.exit(main())
