#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Complete Uninstaller
# =============================================================================
# Safely removes ALL GeeX OS modifications and restores backups.
# =============================================================================

import sys
import os
import shutil
import argparse
from pathlib import Path


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    NC = '\033[0m'


class Uninstaller:
    """GeeX OS Complete Uninstaller"""
    
    def __init__(self):
        self.geex_dir = Path.home() / ".geex"
        self.shell = os.path.basename(os.environ.get('SHELL', 'bash'))
        self.shell_rc = str(Path.home() / ('.zshrc' if self.shell == 'zsh' else '.bashrc'))
        self.removed = []
        self.errors = []
    
    def print_banner(self):
        print(f"{Colors.RED}{Colors.BOLD}")
        print('   ╔═══════════════════════════════════════════╗')
        print('   ║         GeeX OS Uninstaller               ║')
        print('   ╚═══════════════════════════════════════════╝')
        print(f"{Colors.NC}\n")
    
    def remove_from_shell_rc(self):
        """Remove GeeX hooks from shell config."""
        print(f"{Colors.YELLOW}Removing shell integration...{Colors.NC}")
        
        if not Path(self.shell_rc).exists():
            return
        
        with open(self.shell_rc, 'r') as f:
            lines = f.readlines()
        
        # Find and remove GeeX blocks
        new_lines = []
        skip = False
        removed_any = False
        
        for line in lines:
            if '# ═════ GeeX OS' in line or '# GeeX OS' in line:
                skip = True
                removed_any = True
                continue
            if skip and ('# ═════ End GeeX' in line or (line.strip() and not line.startswith('#'))):
                skip = False
            if not skip:
                new_lines.append(line)
        
        with open(self.shell_rc, 'w') as f:
            f.writelines(new_lines)
        
        if removed_any:
            print(f"  {Colors.GREEN}✓{Colors.NC} Removed from {self.shell_rc}")
        
        self.removed.append("shell hooks")
    
    def remove_binaries(self):
        """Remove geex binaries from PATH."""
        print(f"{Colors.YELLOW}Removing command binaries...{Colors.NC}")
        
        geex_bin = self.geex_dir / 'bin'
        if geex_bin.exists():
            for f in geex_bin.iterdir():
                if f.name.startswith('geex'):
                    f.unlink(missing_ok=True)
            geex_bin.rmdir()
            print(f"  {Colors.GREEN}✓{Colors.NC} Removed binaries")
            self.removed.append("binaries")
    
    def remove_installation(self):
        """Remove main installation directory."""
        print(f"{Colors.YELLOW}Removing installation files...{Colors.NC}")
        
        install_dir = self.geex_dir / 'os'
        if install_dir.exists():
            shutil.rmtree(install_dir)
            print(f"  {Colors.GREEN}✓{Colors.NC} Removed {install_dir}")
            self.removed.append("installation files")
    
    def offer_full_removal(self):
        """Offer to remove everything including backups and configs."""
        print(f"\n{Colors.MAGENTA}Do you want to remove ALL GeeX data including backups and configs?{Colors.NC}")
        print(f"  {Colors.YELLOW}Backups at:{Colors.NC} {self.geex_dir / 'backups'}")
        print(f"  {Colors.YELLOW}Configs at:{Colors.NC} {self.geex_dir / 'data'}")
        print(f"  {Colors.YELLOW}Logs at:{Colors.NC}    {self.geex_dir / 'logs'}")
        print("")
        
        choice = input(f"Remove everything? [y/N]: ").strip().lower()
        
        if choice in ('y', 'yes'):
            if self.geex_dir.exists():
                shutil.rmtree(self.geex_dir)
                print(f"  {Colors.GREEN}✓{Colors.NC} Removed {self.geex_dir} completely")
                self.removed.append("all data")
        else:
            print(f"  {Colors.BLUE}ℹ{Colors.NC} Kept user data at {self.geex_dir}")
    
    def restore_backup(self):
        """Offer to restore pre-installation backup."""
        backups_dir = self.geex_dir / 'backups'
        if not backups_dir.exists():
            return
        
        backups = sorted(backups_dir.iterdir())
        pre_install = [b for b in backups if 'pre-install' in b.name]
        
        if pre_install:
            print(f"\n{Colors.CYAN}Found pre-installation backup:{Colors.NC} {pre_install[-1].name}")
            choice = input(f"Restore shell config from backup? [Y/n]: ").strip().lower()
            
            if choice not in ('n', 'no'):
                backup = pre_install[-1]
                rc_backup = backup / Path(self.shell_rc).name
                if rc_backup.exists():
                    shutil.copy2(rc_backup, self.shell_rc)
                    print(f"  {Colors.GREEN}✓{Colors.NC} Restored {self.shell_rc}")
    
    def run(self):
        """Run uninstallation."""
        self.print_banner()
        
        print(f"{Colors.RED}WARNING:{Colors.NC} This will remove GeeX OS from your system.")
        confirm = input(f"{Colors.YELLOW}Type 'uninstall' to confirm: {Colors.NC}").strip()
        
        if confirm != 'uninstall':
            print(f"\n{Colors.BLUE}Uninstallation cancelled.{Colors.NC}")
            return 0
        
        print("")
        
        self.restore_backup()
        self.remove_from_shell_rc()
        self.remove_binaries()
        self.remove_installation()
        self.offer_full_removal()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔═══════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.GREEN}{Colors.BOLD}║    GeeX OS Uninstalled Successfully       ║{Colors.NC}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚═══════════════════════════════════════════╝{Colors.NC}")
        
        if self.removed:
            print(f"\nRemoved: {', '.join(self.removed)}")
        
        print(f"\n{Colors.CYAN}Please restart your terminal for changes to take effect.{Colors.NC}\n")
        return 0


def main():
    parser = argparse.ArgumentParser(description='GeeX OS Uninstaller')
    parser.add_argument('--force', action='store_true', help='Skip confirmation')
    parser.add_argument('--full', action='store_true', help='Remove everything including data')
    args = parser.parse_args()
    
    uninstaller = Uninstaller()
    return uninstaller.run()


if __name__ == "__main__":
    sys.exit(main())
