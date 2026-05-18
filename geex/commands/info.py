#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Info Command
# =============================================================================
# Comprehensive system information display.
# =============================================================================

import os
import sys
import platform


class InfoCommand:
    """System information command."""
    
    def __init__(self, config, theme):
        from geex.core.systeminfo import SystemInfo
        self.config = config
        self.theme = theme
        self.sysinfo = SystemInfo()
    
    def run(self, args: list) -> int:
        """Execute info command."""
        t = self.theme
        
        print(f"\n  {t.a2()}{t.bold()}System Information{t.reset()}\n")
        
        info = self.sysinfo.get_all()
        os_info = info['os']
        
        # OS Section
        print(f"  {t.a1()}{t.bold()}Operating System{t.reset()}")
        print(f"    {t.fg_color()}System:{t.reset()}     {os_info.get('system', 'N/A')}")
        print(f"    {t.fg_color()}Node:{t.reset()}       {os_info.get('node', 'N/A')}")
        print(f"    {t.fg_color()}Release:{t.reset()}    {os_info.get('release', 'N/A')}")
        print(f"    {t.fg_color()}Version:{t.reset()}    {os_info.get('version', 'N/A')[:50]}")
        print(f"    {t.fg_color()}Machine:{t.reset()}    {os_info.get('machine', 'N/A')}")
        
        if os_info.get('is_termux'):
            print(f"    {t.fg_color()}Termux:{t.reset()}     v{os_info.get('termux_version', 'N/A')}")
            print(f"    {t.fg_color()}Android:{t.reset()}    v{os_info.get('android_version', 'N/A')}")
        
        # CPU Section
        cpu = info['cpu']
        print(f"\n  {t.a1()}{t.bold()}CPU{t.reset()}")
        print(f"    {t.fg_color()}Model:{t.reset()}      {cpu.get('model', 'N/A')}")
        print(f"    {t.fg_color()}Cores:{t.reset()}      {cpu.get('cores', 'N/A')}")
        print(f"    {t.fg_color()}Frequency:{t.reset()}  {cpu.get('freq_mhz', 0)} MHz")
        print(f"    {t.fg_color()}Usage:{t.reset()}      {cpu.get('usage_percent', 0):.1f}%")
        
        # Memory Section
        mem = info['memory']
        print(f"\n  {t.a1()}{t.bold()}Memory{t.reset()}")
        print(f"    {t.fg_color()}Total:{t.reset()}      {mem.get('total_mb', 0):.0f} MB")
        print(f"    {t.fg_color()}Used:{t.reset()}       {mem.get('used_mb', 0):.0f} MB")
        print(f"    {t.fg_color()}Free:{t.reset()}       {mem.get('free_mb', 0):.0f} MB")
        print(f"    {t.fg_color()}Usage:{t.reset()}      {mem.get('percent', 0):.1f}%")
        
        # Storage Section
        storage = info['storage']
        print(f"\n  {t.a1()}{t.bold()}Storage{t.reset()}")
        print(f"    {t.fg_color()}Total:{t.reset()}      {storage.get('total_gb', 0):.1f} GB")
        print(f"    {t.fg_color()}Used:{t.reset()}       {storage.get('used_gb', 0):.1f} GB")
        print(f"    {t.fg_color()}Free:{t.reset()}       {storage.get('free_gb', 0):.1f} GB")
        print(f"    {t.fg_color()}Usage:{t.reset()}      {storage.get('percent', 0):.1f}%")
        
        # Battery
        battery = info['battery']
        if battery:
            print(f"\n  {t.a1()}{t.bold()}Battery{t.reset()}")
            print(f"    {t.fg_color()}Level:{t.reset()}      {battery.get('percentage', 0)}%")
            print(f"    {t.fg_color()}Status:{t.reset()}     {'Charging' if battery.get('plugged') else 'Discharging'}")
        
        # System
        print(f"\n  {t.a1()}{t.bold()}System{t.reset()}")
        print(f"    {t.fg_color()}Uptime:{t.reset()}     {info.get('uptime', 'N/A')}")
        print(f"    {t.fg_color()}Load:{t.reset()}       {', '.join(f'{l:.2f}' for l in info.get('load_avg', [0,0,0]))}")
        print(f"    {t.fg_color()}Python:{t.reset()}     {info.get('python', 'N/A')}")
        print(f"    {t.fg_color()}Shell:{t.reset()}      {info.get('shell', 'N/A')}")
        
        print("")
        return 0


def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return InfoCommand(Config(), Theme()).run(args or [])
