#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: Network Scanner - Basic network scanning."""

import socket
import subprocess
import concurrent.futures

class NetworkScannerPlugin:
    def __init__(self):
        self.name = "network_scanner"
        self.version = "1.0.0"

    def scan_port(self, host, port, timeout=1):
        """Scan a single port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return port if result == 0 else None
        except Exception:
            return None

    def scan_ports(self, host="127.0.0.1", start=1, end=1024, max_workers=50):
        """Scan port range."""
        print(f"\033[96mScanning {host} ports {start}-{end}...\033[0m")
        open_ports = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.scan_port, host, p): p for p in range(start, end+1)}
            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                result = future.result()
                if result:
                    service = self._get_service_name(result)
                    open_ports.append((result, service))
                    print(f"  \033[92m✓ Port {result} open\033[0m \033[94m({service})\033[0m")

        return open_ports

    def _get_service_name(self, port):
        """Get common service name for port."""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 3306: 'MySQL', 8080: 'HTTP-Alt',
        }
        return services.get(port, 'Unknown')

    def ping(self, host="8.8.8.8", count=3):
        """Ping a host."""
        print(f"\033[96mPinging {host}...\033[0m")
        try:
            result = subprocess.run(
                ['ping', '-c', str(count), host],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'time=' in line or 'bytes from' in line:
                        print(f"  \033[92m{line}\033[0m")
            else:
                print(f"  \033[91mHost unreachable\033[0m")
        except Exception as e:
            print(f"  \033[91mError: {e}\033[0m")

def run():
    """Plugin entry point."""
    scanner = NetworkScannerPlugin()
    scanner.ping()
    print("")
    scanner.scan_ports(start=1, end=100, max_workers=20)

if __name__ == "__main__":
    run()
