#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS CPU Command - CPU info and monitoring."""

class CPUCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        from geex.core.systeminfo import SystemInfo
        si = SystemInfo()
        cpu = si.get_cpu_info()
        load = si.get_load_avg()
        temp = si.get_temperature()

        print(f"\n  {t.a2()}{t.bold()}⚡ CPU{t.reset()}\n")

        print(f"  {t.a1()}Model:{t.reset}       {t.fg_color()}{cpu.get('model', 'Unknown')}{t.reset()}")
        print(f"  {t.a1()}Cores:{t.reset}       {t.fg_color()}{cpu.get('cores', 'N/A')}{t.reset()}")
        print(f"  {t.a1()}Frequency:{t.reset}   {t.fg_color()}{cpu.get('freq_mhz', 0)} MHz{t.reset()}")
        print(f"  {t.a1()}Usage:{t.reset}       {t.fg_color()}{cpu.get('usage_percent', 0):.1f}%{t.reset()}")
        print(f"  {t.a1()}Load Avg:{t.reset}    {t.fg_color()}{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}{t.reset()}")

        if temp:
            temp_color = t.ok() if temp < 60 else (t.warn() if temp < 80 else t.err())
            print(f"  {t.a1()}Temp:{t.reset}        {temp_color}{temp:.1f}°C{t.reset()}")

        # CPU usage bar
        pct = cpu.get('usage_percent', 0)
        width = 40
        filled = int((pct / 100) * width)
        color = t.ok() if pct < 50 else (t.warn() if pct < 80 else t.err())
        bar = f"{'█' * filled}{'░' * (width - filled)}"
        print(f"\n  {color}{bar}{t.reset()} {pct:.1f}%")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return CPUCommand(Config(), Theme()).run(args)
