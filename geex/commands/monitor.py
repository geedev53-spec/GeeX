#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Monitor Command - Interactive dashboard and live system monitor."""

import sys

class MonitorCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme
    
    def run(self, args=None):
        from geex.core.dashboard import Dashboard
        dashboard = Dashboard(self.config, self.theme)
        dashboard.run()
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return MonitorCommand(Config(), Theme()).run(args)

def top_app():
    """Entry point for 'top' alias."""
    return run()
