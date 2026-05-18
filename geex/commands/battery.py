#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Battery Command - Battery info."""

class BatteryCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        from geex.core.systeminfo import SystemInfo
        si = SystemInfo()
        battery = si.get_battery()

        print(f"\n  {t.a2()}{t.bold()}🔋 Battery{t.reset()}\n")

        if not battery:
            print(f"  {t.warn()}No battery information available{t.reset()}")
            print("")
            return 0

        pct = battery.get('percentage', 0)
        plugged = battery.get('plugged', False)

        # Visual bar
        width = 30
        filled = int((pct / 100) * width)
        color = t.ok() if pct > 50 else (t.warn() if pct > 20 else t.err())
        bar = f"{'█' * filled}{'░' * (width - filled)}"

        print(f"  {t.a1()}Level:{t.reset}     {color}{bar}{t.reset()} {pct}%")
        print(f"  {t.a1()}Status:{t.reset}    {'⚡ Charging' if plugged else '🔋 Discharging'}")

        temp = battery.get('temperature')
        if temp:
            print(f"  {t.a1()}Temp:{t.reset}      {temp:.1f}°C")

        health = battery.get('health')
        if health and health != 'Unknown':
            print(f"  {t.a1()}Health:{t.reset}    {health}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return BatteryCommand(Config(), Theme()).run(args)
