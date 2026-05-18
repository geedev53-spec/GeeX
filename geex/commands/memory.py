#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Memory Command - RAM info."""

class MemoryCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        from geex.core.systeminfo import SystemInfo
        si = SystemInfo()
        mem = si.get_memory()

        print(f"\n  {t.a2()}{t.bold()}🧠 Memory{t.reset()}\n")

        total = mem.get('total_mb', 0)
        used = mem.get('used_mb', 0)
        free = mem.get('free_mb', 0)
        pct = mem.get('percent', 0)

        # Visual bar
        width = 40
        filled = int((pct / 100) * width)
        color = t.ok() if pct < 70 else (t.warn() if pct < 90 else t.err())
        bar = f"{'█' * filled}{'░' * (width - filled)}"

        print(f"  {t.a1()}Usage:{t.reset}  {color}{bar}{t.reset()} {pct:.1f}%")
        print(f"\n  {t.a1()}Total:{t.reset}  {t.fg_color()}{total:.0f} MB ({total/1024:.1f} GB){t.reset()}")
        print(f"  {t.a1()}Used:{t.reset}   {t.fg_color()}{used:.0f} MB{t.reset()}")
        print(f"  {t.a1()}Free:{t.reset}   {t.fg_color()}{free:.0f} MB{t.reset()}")

        # Top memory processes
        print(f"\n  {t.a1()}Top Processes:{t.reset}")
        procs = si.get_processes(5)
        for p in procs:
            print(f"    {t.fg_color()}{p['name']:<20} {p['rss_mb']:.0f} MB{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return MemoryCommand(Config(), Theme()).run(args)
