#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Network Command - Network tools."""

import os
import socket
import subprocess

class NetworkCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.a2()}{t.bold()}🌐 Network Information{t.reset()}\n")

        # Hostname
        print(f"  {t.a1()}Hostname:{t.reset()} {t.fg_color()}{socket.gethostname()}{t.reset()}")

        # Network interfaces
        print(f"\n  {t.a1()}Interfaces:{t.reset()}")
        try:
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and '127.0.0.1' not in line:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            ip = parts[1].split('/')[0]
                            iface = parts[-1]
                            print(f"    {t.a3()}{iface:<12}{t.reset()} {t.fg_color()}{ip}{t.reset()}")
        except Exception:
            pass

        # DNS
        print(f"\n  {t.a1()}DNS:{t.reset()}")
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.startswith('nameserver'):
                        ip = line.split()[1]
                        print(f"    {t.fg_color()}{ip}{t.reset()}")
        except Exception:
            pass

        # Connection test
        print(f"\n  {t.a1()}Connectivity:{t.reset()}")
        hosts = [
            ("DNS", "8.8.8.8", 53),
            ("Google", "google.com", 443),
            ("GitHub", "github.com", 443),
        ]

        for name, host, port in hosts:
            try:
                sock = socket.create_connection((host, port), timeout=3)
                sock.close()
                print(f"    {t.ok()}✓{t.reset()} {t.fg_color()}{name:<10} {host}:{port}{t.reset()}")
            except Exception:
                print(f"    {t.err()}✗{t.reset()} {t.fg_color()}{name:<10} {host}:{port}{t.reset()}")

        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return NetworkCommand(Config(), Theme()).run(args)
