#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - System Information Collector
# =============================================================================
# Gathers comprehensive Android/Termux/Linux system information including
# CPU, memory, storage, battery, network, and device details.
# =============================================================================

import os
import sys
import time
import socket
import subprocess
from pathlib import Path
from typing import Dict, Optional, List


class SystemInfo:
    """GeeX OS System Information Collector"""
    
    def __init__(self):
        self._cache = {}
        self._cache_time = 0
        self._cache_ttl = 5  # Cache for 5 seconds
    
    def _is_termux(self) -> bool:
        return (
            'TERMUX_VERSION' in os.environ or
            os.path.exists('/data/data/com.termux') or
            os.environ.get('PREFIX', '').endswith('com.termux')
        )
    
    def _run(self, cmd: list, fallback: str = "") -> str:
        """Safely run a shell command."""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else fallback
        except Exception:
            return fallback
    
    def get_os_info(self) -> Dict:
        """Get operating system information."""
        uname = os.uname()
        return {
            'system': uname.sysname,
            'node': uname.nodename,
            'release': uname.release,
            'version': uname.version,
            'machine': uname.machine,
            'is_termux': self._is_termux(),
            'termux_version': os.environ.get('TERMUX_VERSION', 'N/A'),
            'android_version': self._get_android_version(),
        }
    
    def _get_android_version(self) -> str:
        """Get Android version if available."""
        if not self._is_termux():
            return "N/A"
        try:
            # Try to get Android version
            result = subprocess.run(
                ['getprop', 'ro.build.version.release'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        
        try:
            with open('/system/build.prop', 'r') as f:
                for line in f:
                    if 'ro.build.version.release' in line:
                        return line.split('=')[-1].strip()
        except Exception:
            pass
        
        return "Unknown"
    
    def get_cpu_info(self) -> Dict:
        """Get CPU information."""
        info = {
            'model': 'Unknown',
            'cores': os.cpu_count() or 1,
            'architecture': os.uname().machine,
            'freq_mhz': 0,
            'usage_percent': 0,
        }
        
        # Try to get CPU model
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'Hardware' in line or 'model name' in line:
                        info['model'] = line.split(':')[-1].strip()
                        break
                    elif 'Processor' in line and info['model'] == 'Unknown':
                        info['model'] = line.split(':')[-1].strip()
        except Exception:
            pass
        
        # Try to get CPU frequency
        freq_paths = [
            '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq',
            '/proc/cpuinfo',
        ]
        for path in freq_paths:
            try:
                if path.endswith('cpuinfo'):
                    with open(path, 'r') as f:
                        for line in f:
                            if 'CPU MHz' in line or 'clock' in line.lower():
                                val = line.split(':')[-1].strip()
                                info['freq_mhz'] = int(float(val))
                                break
                else:
                    with open(path, 'r') as f:
                        info['freq_mhz'] = int(f.read().strip()) // 1000
                break
            except Exception:
                continue
        
        # CPU usage via /proc/stat
        try:
            with open('/proc/stat', 'r') as f:
                line = f.readline()
                fields = list(map(int, line.split()[1:]))
                idle = fields[3]
                total = sum(fields)
                usage = ((total - idle) / total) * 100 if total > 0 else 0
                info['usage_percent'] = round(usage, 1)
        except Exception:
            pass
        
        return info
    
    def get_memory(self) -> Dict:
        """Get memory information."""
        mem = {'total_mb': 0, 'used_mb': 0, 'free_mb': 0, 'percent': 0}
        
        try:
            with open('/proc/meminfo', 'r') as f:
                data = {}
                for line in f:
                    if ':' in line:
                        key, val = line.split(':', 1)
                        data[key.strip()] = int(val.split()[0]) // 1024  # Convert to MB
                
                mem['total_mb'] = data.get('MemTotal', 0)
                mem['free_mb'] = data.get('MemAvailable', data.get('MemFree', 0))
                mem['used_mb'] = mem['total_mb'] - mem['free_mb']
                if mem['total_mb'] > 0:
                    mem['percent'] = round((mem['used_mb'] / mem['total_mb']) * 100, 1)
        except Exception:
            pass
        
        return mem
    
    def get_storage(self) -> Dict:
        """Get storage information."""
        storage = {'total_gb': 0, 'used_gb': 0, 'free_gb': 0, 'percent': 0}
        
        try:
            stat = os.statvfs('/')
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            
            storage['total_gb'] = round(total / (1024**3), 2)
            storage['free_gb'] = round(free / (1024**3), 2)
            storage['used_gb'] = round(used / (1024**3), 2)
            if total > 0:
                storage['percent'] = round((used / total) * 100, 1)
        except Exception:
            pass
        
        return storage
    
    def get_battery(self) -> Optional[Dict]:
        """Get battery information (Android/Termux)."""
        if not self._is_termux():
            return None
        
        battery = {'percentage': 0, 'plugged': False, 'temperature': 0, 'health': 'Unknown'}
        
        # Try termux-api
        result = self._run(['termux-battery-status'], '')
        if result and result.startswith('{'):
            try:
                import json
                data = json.loads(result)
                battery['percentage'] = data.get('percentage', 0)
                battery['plugged'] = data.get('plugged', 'UNPLUGGED') != 'UNPLUGGED'
                battery['temperature'] = data.get('temperature', 0)
                battery['health'] = data.get('health', 'UNKNOWN')
                return battery
            except Exception:
                pass
        
        # Fallback to sysfs
        paths = [
            '/sys/class/power_supply/battery/capacity',
            '/sys/class/power_supply/Battery/capacity',
        ]
        for path in paths:
            try:
                with open(path, 'r') as f:
                    battery['percentage'] = int(f.read().strip())
                
                status_path = os.path.join(os.path.dirname(path), 'status')
                with open(status_path, 'r') as f:
                    status = f.read().strip().lower()
                    battery['plugged'] = status in ('charging', 'full')
                
                return battery
            except Exception:
                continue
        
        return battery if battery['percentage'] > 0 else None
    
    def get_network(self) -> Dict:
        """Get network information."""
        net = {
            'hostname': socket.gethostname(),
            'interfaces': [],
            'wifi_connected': False,
            'mobile_connected': False,
        }
        
        try:
            import netifaces
            for iface in netifaces.interfaces():
                if iface.startswith(('lo', 'dummy')):
                    continue
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip = addrs[netifaces.AF_INET][0].get('addr', '')
                    if ip:
                        net['interfaces'].append({'name': iface, 'ip': ip})
        except ImportError:
            # Fallback
            result = self._run(['ip', 'addr', 'show'], '')
            if not result:
                result = self._run(['ifconfig'], '')
        
        return net
    
    def get_uptime(self) -> str:
        """Get system uptime as human-readable string."""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_sec = float(f.readline().split()[0])
            
            days = int(uptime_sec // 86400)
            hours = int((uptime_sec % 86400) // 3600)
            minutes = int((uptime_sec % 3600) // 60)
            
            parts = []
            if days > 0:
                parts.append(f"{days}d")
            if hours > 0:
                parts.append(f"{hours}h")
            parts.append(f"{minutes}m")
            
            return ' '.join(parts)
        except Exception:
            return "Unknown"
    
    def get_load_avg(self) -> List[float]:
        """Get system load averages."""
        try:
            return list(os.getloadavg())
        except Exception:
            return [0.0, 0.0, 0.0]
    
    def get_processes(self, limit: int = 10) -> List[Dict]:
        """Get top processes by memory usage."""
        processes = []
        
        try:
            for pid_dir in Path('/proc').glob('[0-9]*'):
                try:
                    pid = int(pid_dir.name)
                    
                    with open(pid_dir / 'status', 'r') as f:
                        name = 'unknown'
                        rss = 0
                        for line in f:
                            if line.startswith('Name:'):
                                name = line.split()[1]
                            elif line.startswith('VmRSS:'):
                                rss = int(line.split()[1])  # kB
                    
                    if rss > 0:
                        processes.append({
                            'pid': pid,
                            'name': name,
                            'rss_mb': rss // 1024,
                        })
                except (PermissionError, FileNotFoundError):
                    continue
            
            processes.sort(key=lambda x: x['rss_mb'], reverse=True)
            return processes[:limit]
            
        except Exception:
            return []
    
    def get_temperature(self) -> Optional[float]:
        """Get CPU temperature if available."""
        temp_paths = [
            '/sys/class/thermal/thermal_zone0/temp',
            '/sys/class/thermal/thermal_zone1/temp',
        ]
        
        for path in temp_paths:
            try:
                with open(path, 'r') as f:
                    temp = int(f.read().strip())
                    return temp / 1000.0 if temp > 1000 else temp
            except Exception:
                continue
        
        return None
    
    def get_all(self) -> Dict:
        """Get all system information."""
        return {
            'os': self.get_os_info(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory(),
            'storage': self.get_storage(),
            'battery': self.get_battery(),
            'network': self.get_network(),
            'uptime': self.get_uptime(),
            'load_avg': self.get_load_avg(),
            'temperature': self.get_temperature(),
            'processes': self.get_processes(),
            'python': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'shell': os.path.basename(os.environ.get('SHELL', 'bash')),
        }
