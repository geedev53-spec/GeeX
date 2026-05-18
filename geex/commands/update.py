#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Update Command - Wrapper for updater."""

class UpdateCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        from updater import main
        return main()

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return UpdateCommand(Config(), Theme()).run(args)
