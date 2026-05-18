#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Main Entry Point
# =============================================================================
# The futuristic terminal enhancement framework for Android Termux.
# Run this file directly or use the 'geex' command after installation.
# =============================================================================

import sys
import os

# Add project root to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from geex.core.config import Config
from geex.core.logger import Logger
from geex.core.startup import Startup
from geex.core.shell import ShellIntegration

__version__ = "2.0.0"
__author__ = "GeeX OS Team"
__license__ = "MIT"


def main():
    """Main entry point for GeeX OS."""
    try:
        # Initialize core systems
        config = Config()
        logger = Logger()
        
        logger.info(f"GeeX OS v{__version__} starting...")
        
        # Show startup sequence if enabled
        if config.get("startup_enabled", True):
            startup = Startup(config, logger)
            startup.run()
        
        # Initialize shell integration
        shell = ShellIntegration(config)
        shell.initialize()
        
        # Launch the command system
        from geex.core.shell import main as shell_main
        return shell_main()
        
    except KeyboardInterrupt:
        print("\n\n[GEEX] Interrupted by user. Goodbye!")
        return 0
    except Exception as e:
        print(f"\n[GEEX ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
