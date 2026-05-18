#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# GeeX OS - Smart Updater
# =============================================================================
# Checks for updates from GitHub, downloads, and applies them safely
# with rollback support on failure.
# =============================================================================

import sys
import os
import json
import shutil
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    NC = '\033[0m'


class Updater:
    """GeeX OS Smart Updater"""
    
    CURRENT_VERSION = "2.0.0"
    GITHUB_API = "https://api.github.com/repos/geexos/GeeX-OS/releases/latest"
    GITHUB_RAW = "https://raw.githubusercontent.com/geexos/GeeX-OS/main"
    
    def __init__(self):
        self.geex_dir = Path.home() / ".geex"
        self.install_dir = self.geex_dir / "os"
        self.backup_dir = self.geex_dir / "backups"
        self.cache_file = self.geex_dir / "data" / "cache.json"
    
    def print_banner(self):
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print('   ╔═══════════════════════════════════════════╗')
        print('   ║           GeeX OS Updater                 ║')
        print('   ╚═══════════════════════════════════════════╝')
        print(f"{Colors.NC}")
        print(f"  Current Version: {Colors.CYAN}{Colors.BOLD}{self.CURRENT_VERSION}{Colors.NC}")
        print("")
    
    def check_internet(self) -> bool:
        """Check if internet is available."""
        try:
            urllib.request.urlopen('https://github.com', timeout=5)
            return True
        except:
            return False
    
    def get_latest_version(self) -> dict:
        """Check GitHub for latest release."""
        try:
            req = urllib.request.Request(
                self.GITHUB_API,
                headers={'User-Agent': 'GeeX-OS-Updater'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                return {
                    'version': data.get('tag_name', 'unknown').lstrip('v'),
                    'url': data.get('html_url', ''),
                    'notes': data.get('body', 'No release notes'),
                    'published': data.get('published_at', ''),
                }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {'version': self.CURRENT_VERSION, 'url': '', 'notes': 'No releases yet', 'published': ''}
            return None
        except Exception as e:
            print(f"  {Colors.RED}Error checking updates: {e}{Colors.NC}")
            return None
    
    def version_compare(self, current: str, latest: str) -> int:
        """Compare version strings. Returns -1, 0, or 1."""
        try:
            c = [int(x) for x in current.split('.')]
            l = [int(x) for x in latest.split('.')]
            for i in range(max(len(c), len(l))):
                cv = c[i] if i < len(c) else 0
                lv = l[i] if i < len(l) else 0
                if cv < lv:
                    return -1
                elif cv > lv:
                    return 1
            return 0
        except:
            return 0
    
    def create_rollback_backup(self):
        """Create backup before update for rollback."""
        print(f"{Colors.BLUE}Creating rollback backup...{Colors.NC}")
        rollback_dir = self.backup_dir / f"rollback-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if self.install_dir.exists():
            shutil.copytree(self.install_dir, rollback_dir / 'os', dirs_exist_ok=True)
        print(f"  {Colors.GREEN}✓{Colors.NC} Backup created at {rollback_dir}")
        return rollback_dir
    
    def perform_update(self, version_info: dict):
        """Download and apply update."""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}━━━ Updating GeeX OS ━━━{Colors.NC}\n")
        
        # Create rollback point
        rollback = self.create_rollback_backup()
        
        print(f"{Colors.BLUE}Downloading update...{Colors.NC}")
        
        try:
            # Update from git if available
            if (self.install_dir / '.git').exists():
                result = subprocess.run(
                    ['git', '-C', str(self.install_dir), 'pull'],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    print(f"  {Colors.GREEN}✓{Colors.NC} Updated via git pull")
                else:
                    print(f"  {Colors.YELLOW}Git pull failed, trying manual update...{Colors.NC}")
                    self._manual_update()
            else:
                self._manual_update()
            
            # Update config version
            config_path = self.geex_dir / 'data' / 'config.json'
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                config['version'] = version_info['version']
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
            
            # Update cache
            self._update_cache(version_info['version'])
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}╔═══════════════════════════════════════════╗{Colors.NC}")
            print(f"{Colors.GREEN}{Colors.BOLD}║    Updated to v{version_info['version']}!                    ║{Colors.NC}")
            print(f"{Colors.GREEN}{Colors.BOLD}╚═══════════════════════════════════════════╝{Colors.NC}")
            print(f"\n{Colors.CYAN}Please restart your terminal.{Colors.NC}\n")
            return True
            
        except Exception as e:
            print(f"\n{Colors.RED}Update failed: {e}{Colors.NC}")
            print(f"{Colors.YELLOW}Rolling back...{Colors.NC}")
            self._rollback(rollback)
            return False
    
    def _manual_update(self):
        """Manual file-by-file update from GitHub raw."""
        files_to_update = [
            'launcher.py', 'installer.py', 'uninstall.py', 'updater.py',
            'requirements.txt',
        ]
        
        for filename in files_to_update:
            url = f"{self.GITHUB_RAW}/{filename}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'GeeX-OS-Updater'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read()
                    dest = self.install_dir / filename
                    with open(dest, 'wb') as f:
                        f.write(content)
                    print(f"  {Colors.GREEN}✓{Colors.NC} Updated {filename}")
            except Exception as e:
                print(f"  {Colors.YELLOW}⚠{Colors.NC} Could not update {filename}: {e}")
    
    def _rollback(self, rollback_dir: Path):
        """Rollback to previous version."""
        try:
            if (rollback_dir / 'os').exists():
                if self.install_dir.exists():
                    shutil.rmtree(self.install_dir)
                shutil.copytree(rollback_dir / 'os', self.install_dir)
                print(f"  {Colors.GREEN}✓{Colors.NC} Rolled back successfully")
        except Exception as e:
            print(f"  {Colors.RED}Rollback failed: {e}{Colors.NC}")
    
    def _update_cache(self, version: str):
        """Update cache with version info."""
        try:
            cache = {}
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            cache['last_update_check'] = datetime.now().isoformat()
            cache['version_check'] = {
                'current': self.CURRENT_VERSION,
                'latest': version,
                'checked_at': datetime.now().isoformat()
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except:
            pass
    
    def run(self):
        """Run update check and process."""
        self.print_banner()
        
        if not self.check_internet():
            print(f"{Colors.RED}No internet connection.{Colors.NC}")
            print(f"{Colors.YELLOW}Please check your network and try again.{Colors.NC}\n")
            return 1
        
        print(f"{Colors.BLUE}Checking for updates...{Colors.NC}\n")
        
        version_info = self.get_latest_version()
        if version_info is None:
            print(f"{Colors.YELLOW}Could not check for updates.{Colors.NC}\n")
            return 1
        
        latest = version_info['version']
        comparison = self.version_compare(self.CURRENT_VERSION, latest)
        
        if comparison < 0:
            print(f"{Colors.GREEN}New version available!{Colors.NC}")
            print(f"  Current: {Colors.YELLOW}{self.CURRENT_VERSION}{Colors.NC}")
            print(f"  Latest:  {Colors.GREEN}{Colors.BOLD}{latest}{Colors.NC}")
            
            if version_info.get('notes'):
                print(f"\n{Colors.CYAN}Release Notes:{Colors.NC}")
                print(f"  {version_info['notes'][:500]}...")
            
            choice = input(f"\n{Colors.MAGENTA}Update now? [Y/n]: {Colors.NC}").strip().lower()
            
            if choice not in ('n', 'no'):
                return 0 if self.perform_update(version_info) else 1
            else:
                print(f"\n{Colors.BLUE}Update cancelled.{Colors.NC}\n")
        
        elif comparison == 0:
            print(f"{Colors.GREEN}✓ You are on the latest version!{Colors.NC}")
            print(f"  GeeX OS v{self.CURRENT_VERSION}\n")
        
        else:
            print(f"{Colors.CYAN}You are ahead of the latest release!{Colors.NC}")
            print(f"  Current: {Colors.GREEN}{self.CURRENT_VERSION}{Colors.NC}")
            print(f"  Latest:  {Colors.YELLOW}{latest}{Colors.NC}\n")
        
        self._update_cache(latest)
        return 0


def main():
    updater = Updater()
    return updater.run()


if __name__ == "__main__":
    sys.exit(main())
