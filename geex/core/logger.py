#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Logging System
# =============================================================================
# Advanced logging with file output, rotation, and colored console output.
# =============================================================================

import os
import sys
import logging
import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """GeeX OS Logging System"""
    
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    COLORS = {
        'DEBUG': '\033[96m',
        'INFO': '\033[94m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[95m',
        'RESET': '\033[0m'
    }
    
    def __init__(self, name: str = "geex", log_dir: Optional[str] = None, level: str = "INFO"):
        self.name = name
        self.log_dir = Path(log_dir) if log_dir else Path.home() / ".geex" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.log_dir / f"{name}.log"
        self.level = self.LEVELS.get(level.upper(), logging.INFO)
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging handlers."""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # File handler
        try:
            fh = logging.FileHandler(str(self.log_file))
            fh.setLevel(logging.DEBUG)
            file_fmt = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            fh.setFormatter(file_fmt)
            self.logger.addHandler(fh)
        except Exception:
            pass
    
    def _log(self, level: str, message: str):
        """Internal log method."""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        color = self.COLORS.get(level, '')
        reset = self.COLORS['RESET']
        
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)
    
    def debug(self, message: str):
        self._log('DEBUG', message)
    
    def info(self, message: str):
        self._log('INFO', message)
    
    def warning(self, message: str):
        self._log('WARNING', message)
    
    def error(self, message: str):
        self._log('ERROR', message)
    
    def critical(self, message: str):
        self._log('CRITICAL', message)
    
    def section(self, title: str):
        """Log a section header."""
        self.info(f"{'='*50}")
        self.info(f"  {title}")
        self.info(f"{'='*50}")
    
    def get_recent_logs(self, count: int = 20) -> list:
        """Get recent log entries."""
        if not self.log_file.exists():
            return []
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            return lines[-count:]
        except Exception:
            return []
    
    def clear_logs(self):
        """Clear all log files."""
        try:
            if self.log_file.exists():
                self.log_file.unlink()
            # Clean old logs
            for f in self.log_dir.glob("*.log*"):
                try:
                    stat = f.stat()
                    age = datetime.datetime.now().timestamp() - stat.st_mtime
                    if age > 7 * 86400:  # 7 days
                        f.unlink()
                except Exception:
                    pass
        except Exception as e:
            print(f"[Logger] Error clearing logs: {e}")
