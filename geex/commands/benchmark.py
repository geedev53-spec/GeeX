#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Benchmark Command - Performance testing."""

import time
import math
import os

class BenchmarkCommand:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme

    def run(self, args=None):
        t = self.theme
        print(f"\n  {t.a2()}{t.bold()}⚡ GeeX OS Benchmark{t.reset()}\n")

        # CPU Benchmark
        print(f"  {t.a1()}CPU Benchmark...{t.reset()}")
        start = time.time()
        for _ in range(1000000):
            math.sqrt(12345.6789)
        cpu_time = time.time() - start
        cpu_score = max(1, int(1000000 / (cpu_time * 1000)))
        print(f"  {t.ok()}  Math ops: {cpu_time:.3f}s  Score: {cpu_score}{t.reset()}")

        # Memory Benchmark
        print(f"\n  {t.a1()}Memory Benchmark...{t.reset()}")
        start = time.time()
        data = []
        for i in range(100000):
            data.append("x" * 100)
        mem_time = time.time() - start
        print(f"  {t.ok()}  Alloc: {mem_time:.3f}s  ({len(data)*100/1024:.0f} KB){t.reset()}")
        del data

        # Disk Benchmark
        print(f"\n  {t.a1()}Disk Benchmark...{t.reset()}")
        test_file = "/tmp/geex_bench_test"
        start = time.time()
        with open(test_file, 'w') as f:
            f.write("x" * 1000000)
        write_time = time.time() - start

        start = time.time()
        with open(test_file, 'r') as f:
            f.read()
        read_time = time.time() - start

        os.remove(test_file)
        print(f"  {t.ok()}  Write: {write_time:.3f}s  Read: {read_time:.3f}s{t.reset()}")

        # Summary
        total_score = cpu_score + int(10/write_time) + int(10/read_time)
        print(f"\n  {t.a1()}{'━'*40}{t.reset()}")
        print(f"  {t.a2()}{t.bold()}Total Score: {total_score}{t.reset()}")
        rating = "🔥 Excellent" if total_score > 5000 else ("⚡ Good" if total_score > 2000 else "🐢 Slow")
        print(f"  {t.fg_color()}Rating: {rating}{t.reset()}")
        print("")
        return 0

def run(args=None):
    from geex.core.config import Config
    from geex.core.theme import Theme
    return BenchmarkCommand(Config(), Theme()).run(args)
