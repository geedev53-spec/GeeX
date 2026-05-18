#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - System Dashboard
# =============================================================================
# Full interactive system dashboard with CPU/RAM/storage graphs,
# process list, network status, and live auto-refresh.
# =============================================================================

import os
import sys
import time
import shutil
import signal
from datetime import datetime
from typing import List, Dict


class Dashboard:
    """GeeX OS System Dashboard"""
    
    def __init__(self, config=None, theme=None, sysinfo=None):
        from geex.core.config import Config
        from geex.core.theme import Theme
        from geex.core.systeminfo import SystemInfo
        
        self.config = config or Config()
        self.theme = theme or Theme(self.config)
        self.sysinfo = sysinfo or SystemInfo()
        self.running = True
        self.refresh_rate = self.config.get("dashboard_refresh", 2.0)
        self.history = {
            'cpu': [0] * 30,
            'memory': [0] * 30,
        }
        self.setup_signals()
    
    def setup_signals(self):
        """Setup signal handlers for graceful exit."""
        signal.signal(signal.SIGINT, self._signal_handler)
        try:
            signal.signal(signal.SIGTERM, self._signal_handler)
        except AttributeError:
            pass
    
    def _signal_handler(self, signum, frame):
        self.running = False
    
    def _bar(self, value: float, max_val: float, width: int = 20) -> str:
        """Draw a horizontal bar."""
        pct = min(1.0, max(0.0, value / max_val)) if max_val > 0 else 0
        filled = int(pct * width)
        
        if pct < 0.5:
            color = '\033[92m'
        elif pct < 0.8:
            color = '\033[93m'
        else:
            color = '\033[91m'
        
        bar = f"{'█' * filled}{'░' * (width - filled)}"
        return f"{color}{bar}\033[0m"
    
    def _sparkline(self, data: List[float], width: int = 30) -> str:
        """Draw a sparkline chart."""
        if not data:
            return ""
        
        blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        max_val = max(data) if max(data) > 0 else 1
        
        result = []
        step = max(1, len(data) // width)
        for i in range(0, len(data), step):
            val = data[i]
            idx = min(int((val / max_val) * (len(blocks) - 1)), len(blocks) - 1)
            result.append(blocks[idx])
        
        return ''.join(result[-width:])
    
    def _clear(self):
        """Clear terminal."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def _draw_header(self):
        """Draw dashboard header."""
        t = self.theme
        cols, _ = shutil.get_terminal_size()
        now = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n{t.a1()}{'━' * cols}{t.reset()}")
        print(f"{t.a1()}┃{t.reset()}  {t.a2()}{t.bold()}GEEX OS DASHBOARD{t.reset()}                    {t.dimmed()}{now}{t.reset()}  {t.a1()}┃{t.reset()}")
        print(f"{t.a1()}{'━' * cols}{t.reset()}")
    
    def _draw_cpu_section(self):
        """Draw CPU information section."""
        t = self.theme
        cpu = self.sysinfo.get_cpu_info()
        
        # Update history
        self.history['cpu'].append(cpu.get('usage_percent', 0))
        self.history['cpu'] = self.history['cpu'][-30:]
        
        print(f"\n  {t.a2()}{t.bold()}⚡ CPU{t.reset()}")
        print(f"  {t.dimmed()}{'─' * 50}{t.reset()}")
        print(f"  {t.fg_color()}{cpu.get('model', 'Unknown')[:40]:<40}{t.reset()}")
        print(f"  {t.fg_color()}Cores:{t.reset()} {cpu.get('cores', 0)}  "
              f"{t.fg_color()}Freq:{t.reset()} {cpu.get('freq_mhz', 0)} MHz  "
              f"{t.fg_color()}Usage:{t.reset()} {cpu.get('usage_percent', 0):.1f}%")
        print(f"  {self._bar(cpu.get('usage_percent', 0), 100, 40)} {cpu.get('usage_percent', 0):.1f}%")
        print(f"  {t.a3()}{self._sparkline(self.history['cpu'])}{t.reset()}")
    
    def _draw_memory_section(self):
        """Draw memory information section."""
        t = self.theme
        mem = self.sysinfo.get_memory()
        
        self.history['memory'].append(mem.get('percent', 0))
        self.history['memory'] = self.history['memory'][-30:]
        
        print(f"\n  {t.a2()}{t.bold()}🧠 Memory{t.reset()}")
        print(f"  {t.dimmed()}{'─' * 50}{t.reset()}")
        print(f"  {t.fg_color()}Used:{t.reset()} {mem.get('used_mb', 0):.0f} MB / "
              f"{mem.get('total_mb', 0):.0f} MB  "
              f"({mem.get('percent', 0):.1f}%)")
        print(f"  {self._bar(mem.get('used_mb', 0), max(mem.get('total_mb', 1), 1), 40)} {mem.get('percent', 0):.1f}%")
        print(f"  {t.a3()}{self._sparkline(self.history['memory'])}{t.reset()}")
    
    def _draw_storage_section(self):
        """Draw storage information section."""
        t = self.theme
        storage = self.sysinfo.get_storage()
        
        print(f"\n  {t.a2()}{t.bold()}💾 Storage{t.reset()}")
        print(f"  {t.dimmed()}{'─' * 50}{t.reset()}")
        print(f"  {t.fg_color()}Used:{t.reset()} {storage.get('used_gb', 0):.1f} GB / "
              f"{storage.get('total_gb', 0):.1f} GB  "
              f"({storage.get('percent', 0):.1f}%)")
        print(f"  {self._bar(storage.get('used_gb', 0), max(storage.get('total_gb', 1), 1), 40)} {storage.get('percent', 0):.1f}%")
    
    def _draw_battery_section(self):
        """Draw battery information section."""
        t = self.theme
        battery = self.sysinfo.get_battery()
        
        if not battery:
            return
        
        print(f"\n  {t.a2()}{t.bold()}🔋 Battery{t.reset()}")
        print(f"  {t.dimmed()}{'─' * 50}{t.reset()}")
        
        pct = battery.get('percentage', 0)
        plugged = battery.get('plugged', False)
        status = "⚡ Charging" if plugged else "🔋 Discharging"
        temp = battery.get('temperature', 0)
        
        print(f"  {t.fg_color()}Level:{t.reset()} {pct}%  {t.fg_color()}Status:{t.reset()} {status}", end="")
        if temp:
            print(f"  {t.fg_color()}Temp:{t.reset()} {temp:.1f}°C")
        else:
            print("")
        
        print(f"  {self._bar(pct, 100, 40)} {pct}%")
    
    def _draw_network_section(self):
        """Draw network information section."""
        t = self.theme
        net = self.sysinfo.get_network()
        
        print(f"\n  {t.a2()}{t.bold()}🌐 Network{t.reset()}")
        print(f"  {t.dimmed()}{'─' * 50}{t.reset()}")
        print(f"  {t.fg_color()}Hostname:{t.reset()} {net.get('hostname', 'unknown')}")
        
        for iface in net.get('interfaces', [])[:4]:
            print(f"  {t.a3()}  {iface['name']:<10}{t.reset()} {t.fg_color()}{iface['ip']}{t.reset()}")
    
    def _draw_processes_section(self):
        """Draw top processes section."""
        t = self.theme
        processes = self.sysinfo.get_processes(8)
        
        if not processes:
            return
        
        print(f"\n  {t.a2()}{t.bold()}📋 Top Processes{t.reset()}")
        print(f"  {t.dimmed()}{'─' * 50}{t.reset()}")
        print(f"  {t.dimmed()}{'PID':<8}{'Name':<20}{'RAM (MB)':<10}{t.reset()}")
        
        for proc in processes:
            print(f"  {t.fg_color()}{proc['pid']:<8}{proc['name']:<20}{proc['rss_mb']:<10}{t.reset()}")
    
    def _draw_system_info(self):
        """Draw general system information."""
        t = self.theme
        os_info = self.sysinfo.get_os_info()
        uptime = self.sysinfo.get_uptime()
        load = self.sysinfo.get_load_avg()
        temp = self.sysinfo.get_temperature()
        
        print(f"\n  {t.a2()}{t.bold()}📟 System{t.reset()}")
        print(f"  {t.dimmed()}{'─' * 50}{t.reset()}")
        print(f"  {t.fg_color()}OS:{t.reset()}     {os_info.get('system', '?')} {os_info.get('machine', '')}")
        print(f"  {t.fg_color()}Kernel:{t.reset()} {os_info.get('release', '?')}")
        print(f"  {t.fg_color()}Uptime:{t.reset()} {uptime}")
        print(f"  {t.fg_color()}Load:{t.reset()}   {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")
        if temp:
            print(f"  {t.fg_color()}Temp:{t.reset()}   {temp:.1f}°C")
        if os_info.get('is_termux'):
            print(f"  {t.fg_color()}Termux:{t.reset()} v{os_info.get('termux_version', '?')}")
            print(f"  {t.fg_color()}Android:{t.reset} v{os_info.get('android_version', '?')}")
        print(f"  {t.fg_color()}Python:{t.reset} {sys.version.split()[0]}")
        print(f"  {t.fg_color()}Shell:{t.reset}  {os_info.get('shell', os.path.basename(os.environ.get('SHELL', 'bash')))}")
    
    def _draw_footer(self):
        """Draw dashboard footer."""
        t = self.theme
        cols, _ = shutil.get_terminal_size()
        print(f"\n  {t.dimmed()}{'─' * 50}{t.reset()}")
        print(f"  {t.dimmed()}Press Ctrl+C to exit | Auto-refresh: {self.refresh_rate}s{t.reset()}")
        print(f"{t.a1()}{'━' * cols}{t.reset()}")
    
    def draw(self):
        """Draw complete dashboard."""
        self._clear()
        self._draw_header()
        self._draw_cpu_section()
        self._draw_memory_section()
        self._draw_storage_section()
        self._draw_battery_section()
        self._draw_network_section()
        self._draw_processes_section()
        self._draw_system_info()
        self._draw_footer()
    
    def run(self):
        """Run dashboard with auto-refresh."""
        self.running = True
        
        try:
            while self.running:
                self.draw()
                
                # Refresh countdown
                for i in range(int(self.refresh_rate * 10)):
                    if not self.running:
                        break
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            pass
        finally:
            self._clear()
            print(f"{self.theme.a1()}[GeeX Dashboard]{self.theme.reset()} Goodbye!\n")


def run():
    """Standalone dashboard runner."""
    dashboard = Dashboard()
    dashboard.run()
    return 0


if __name__ == "__main__":
    sys.exit(run())
