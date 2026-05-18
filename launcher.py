#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Command Launcher & Dispatcher
# =============================================================================
# Dispatches all CLI commands to their respective handlers.
# Usage: geex <command> [options]
# =============================================================================

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Setup paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from geex.core.config import Config
from geex.core.logger import Logger
from geex.core.theme import Theme
from geex.core.animations import AnimationEngine


class GeeXLauncher:
    """Main command dispatcher for GeeX OS."""
    
    VERSION = "2.0.0"
    
    COMMANDS = {
        # System
        "info": "geex.commands.info",
        "dashboard": "geex.commands.monitor",
        "monitor": "geex.commands.monitor",
        "doctor": "geex.commands.doctor",
        "benchmark": "geex.commands.benchmark",
        "sysfetch": "geex.commands.sysfetch",
        "update": "geex.commands.update",
        "backup": "geex.commands.backup",
        "restore": "geex.commands.restore",
        "config": "geex.commands.config",
        "clean": "geex.commands.clean",
        "reset": "geex.commands.reset",
        "help": "geex.commands.help",
        # Tools
        "plugins": "geex.commands.plugins",
        "theme": "geex.commands.theme",
        "ai": "geex.commands.ai",
        "network": "geex.commands.network",
        "battery": "geex.commands.battery",
        "storage": "geex.commands.storage",
        "memory": "geex.commands.memory",
        "cpu": "geex.commands.cpu",
        "terminal": "geex.commands.terminal",
        # Plugins
        "clock": "geex.plugins.cyberclock",
        "weather": "geex.plugins.weather",
        "scan": "geex.plugins.network_scanner",
        "game": "geex.plugins.terminal_games",
    }
    
    ALIASES = {
        "i": "info",
        "d": "dashboard",
        "m": "monitor",
        "doc": "doctor",
        "bench": "benchmark",
        "fetch": "sysfetch",
        "u": "update",
        "bak": "backup",
        "rest": "restore",
        "cfg": "config",
        "h": "help",
        "p": "plugins",
        "t": "theme",
        "net": "network",
        "bat": "battery",
        "sto": "storage",
        "mem": "memory",
        "top": "monitor",
        "ps": "monitor",
        "cls": "clean",
    }
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.theme = Theme(self.config)
        self.anim = AnimationEngine(self.config)
    
    def print_banner(self):
        """Print the GeeX OS banner."""
        self.theme.print_banner()
    
    def print_help(self):
        """Print comprehensive help."""
        from geex.commands.help import HelpCommand
        HelpCommand(self.config, self.theme).run()
    
    def print_version(self):
        """Print version information."""
        print(f"\n  GeeX OS v{self.VERSION}")
        print(f"  The Futuristic Terminal Enhancement Framework")
        print(f"  Python {sys.version.split()[0]} | {sys.platform}")
        print("")
    
    def dispatch(self, command: str, args: list) -> int:
        """Dispatch command to appropriate handler."""
        # Resolve alias
        if command in self.ALIASES:
            command = self.ALIASES[command]
        
        if command not in self.COMMANDS:
            print(f"[GeeX] Unknown command: '{command}'")
            print("Run 'geex help' for available commands.")
            return 1
        
        module_path = self.COMMANDS[command]
        
        try:
            # Dynamic import and execution
            module = __import__(module_path, fromlist=["main", "run", command])
            
            # Look for standard entry points
            if hasattr(module, "run"):
                return module.run(args) or 0
            elif hasattr(module, "main"):
                return module.main(args) or 0
            else:
                # Try class-based command
                class_name = command.title().replace("_", "") + "Command"
                if hasattr(module, class_name):
                    cmd_class = getattr(module, class_name)
                    instance = cmd_class(self.config, self.theme)
                    if hasattr(instance, "run"):
                        return instance.run(args) or 0
                
                print(f"[GeeX] Command '{command}' not properly implemented.")
                return 1
                
        except ImportError as e:
            print(f"[GeeX] Error loading command '{command}': {e}")
            return 1
        except Exception as e:
            print(f"[GeeX] Error executing '{command}': {e}")
            self.logger.error(f"Command '{command}' failed: {e}")
            return 1
    
    def run(self, argv: list = None) -> int:
        """Main launcher entry point."""
        if argv is None:
            argv = sys.argv[1:]
        
        if len(argv) == 0:
            # No command - show interactive mode
            self.print_banner()
            self._interactive_mode()
            return 0
        
        # Parse global flags
        if argv[0] in ("-v", "--version"):
            self.print_version()
            return 0
        
        if argv[0] in ("-h", "--help"):
            self.print_help()
            return 0
        
        if argv[0] in ("-b", "--banner"):
            self.print_banner()
            return 0
        
        # Dispatch command
        command = argv[0]
        args = argv[1:]
        return self.dispatch(command, args)
    
    def _interactive_mode(self):
        """Run interactive shell mode."""
        from prompt_toolkit import prompt
        from prompt_toolkit.styles import Style
        from prompt_toolkit.key_binding import KeyBindings
        
        style = Style.from_dict({
            'prompt': '#00d4ff bold',
        })
        
        kb = KeyBindings()
        
        @kb.add('c-c')
        @kb.add('c-d')
        def _(event):
            event.app.exit()
        
        print("  Entering interactive mode. Type 'exit' or press Ctrl+C to quit.")
        print("")
        
        while True:
            try:
                user_input = prompt(
                    'geex> ',
                    style=style,
                    key_bindings=kb
                ).strip()
                
                if not user_input:
                    continue
                if user_input.lower() in ('exit', 'quit', 'q'):
                    print("Goodbye!")
                    break
                
                parts = user_input.split()
                self.dispatch(parts[0], parts[1:])
                print("")
                
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Entry point for the launcher."""
    launcher = GeeXLauncher()
    return launcher.run()


if __name__ == "__main__":
    sys.exit(main())
