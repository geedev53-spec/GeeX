#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Core: Aliases - Enhanced shell aliases."""

# Default aliases for GeeX OS
ALIASES = {
    # Enhanced defaults
    'ls': 'ls --color=auto -la',
    'grep': 'grep --color=auto',

    # GeeX shortcuts
    'gxx': 'geex',
    'gxinfo': 'geex info',
    'gxdash': 'geex dashboard',
    'gxmon': 'geex monitor',
    'gxdoc': 'geex doctor',
    'gxbench': 'geex benchmark',
    'gxupdate': 'geex update',
    'gxbackup': 'geex backup',
    'gxtheme': 'geex theme',
    'gxplugins': 'geex plugins',
    'gxai': 'geex ai',
    'gxfetch': 'geex sysfetch',
    'gxhelp': 'geex help',

    # Developer shortcuts
    'gs': 'git status',
    'ga': 'git add',
    'gc': 'git commit -m',
    'gp': 'git push',
    'gl': 'git log --oneline',
    'gd': 'git diff',

    # Utilities
    'ports': 'netstat -tulan 2>/dev/null || ss -tulan',
    'serve': 'python3 -m http.server',
    'weather': 'python3 -m geex.plugins.weather',
    'sysfetch': 'geex sysfetch',
    'extract': 'python3 -m geex.commands.terminal',
}

def get_aliases():
    """Get all aliases as shell export strings."""
    lines = []
    for alias, command in ALIASES.items():
        lines.append(f'alias {alias}=\'{command}\'')
    return '\n'.join(lines)

def generate_alias_file():
    """Generate aliases.sh content."""
    content = "#!/bin/bash\n# GeeX OS Enhanced Aliases\n\n"
    content += get_aliases()
    return content

if __name__ == "__main__":
    print(generate_alias_file())
