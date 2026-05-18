#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Sysfetch Command - Beautiful system info display."""

import os
import sys
import platform

class SysfetchCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        from geex.core.systeminfo import SystemInfo
        si = SystemInfo()
        info = si.get_all()

        # ASCII Logo
        logo = [
            f"{t.a1()}   ▄███████▄  ▄██████▄   ▄██████▄   ▄███████▄ {t.reset()}",
            f"{t.a1()}  ███    ███ ███    ███ ███    ███ ███    ███ {t.reset()}",
            f"{t.a1()}  ███    ███ ███    ███ ███    ███ ███    ███ {t.reset()}",
            f"{t.a1()}  ███    ███ ███    ███ ███    ███ █▄▄▄▄▄███  {t.reset()}",
            f"{t.a1()}  ███    ███ ███    ███ ███    ███ ▀▀▀▀▀▀███  {t.reset()}",
            f"{t.a1()}  ███    ███ ███    ███ ███    ███ ███    ███ {t.reset()}",
            f"{t.a1()}   ▀██████▀   ▀██████▀   ▀██████▀   ▀███████▀  {t.reset()}",
        ]

        data = [
            f"{t.a2()}{t.bold()}OS{t.reset}      {info['os'].get('system', '?')} {info['os'].get('machine', '')}",
            f"{t.a2()}{t.bold()}Kernel{t.reset}   {info['os'].get('release', '?')}",
            f"{t.a2()}{t.bold()}Uptime{t.reset}   {info.get('uptime', '?')}",
            f"{t.a2()}{t.bold()}Shell{t.reset}    {info.get('shell', '?')}",
            f"{t.a2()}{t.bold()}Python{t.reset}   {info.get('python', '?')}",
            f"{t.a2()}{t.bold()}CPU{t.reset}      {info['cpu'].get('model', '?')[:30]}",
            f"{t.a2()}{t.bold()}Memory{t.reset}   {info['memory'].get('used_mb', 0):.0f}MB / {info['memory'].get('total_mb', 0):.0f}MB",
            f"{t.a2()}{t.bold()}Storage{t.reset}  {info['storage'].get('used_gb', 0):.1f}GB / {info['storage'].get('total_gb', 0):.1f}GB",
        ]

        print("")
        for i in range(max(len(logo), len(data))):
            left = logo[i] if i < len(logo) else " " * 45
            right = data[i] if i < len(data) else ""
            print(f"  {left}  {right}")
        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return SysfetchCommand(Config(), Theme()).run(args)
