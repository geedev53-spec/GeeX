#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Performance - Performance monitoring and optimization."""

import time
import os
import psutil

class PerformanceMonitor:
    """Monitor system performance."""

    def __init__(self):
        self.samples = []

    def get_stats(self):
        """Get current performance stats."""
        stats = {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
        }

        # Get Android-specific info
        try:
            with open('/proc/loadavg', 'r') as f:
                load = f.read().strip().split()
                stats['load_avg_1'] = float(load[0])
        except Exception:
            stats['load_avg_1'] = 0.0

        return stats

    def benchmark_cpu(self, duration=3.0):
        """Run CPU benchmark."""
        import math
        start = time.time()
        ops = 0

        while time.time() - start < duration:
            for _ in range(10000):
                math.sqrt(12345.6789)
            ops += 10000

        elapsed = time.time() - start
        return {
            'operations': ops,
            'time': elapsed,
            'ops_per_sec': ops / elapsed,
        }

def get_quick_stats():
    """Get quick performance snapshot."""
    pm = PerformanceMonitor()
    return pm.get_stats()
