#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: AI Assistant - Smart command suggestions and tips."""

import random

class AIAssistantPlugin:
    def __init__(self):
        self.name = "ai_assistant"
        self.version = "1.0.0"
        self.description = "Smart command suggestions and contextual tips"

    def get_tip(self):
        """Get a random tip."""
        tips = [
            "Use 'geex dashboard' for real-time system monitoring",
            "Press Ctrl+C to cancel any running animation",
            "Run 'geex benchmark' to test your device performance",
            "Use 'geex theme list' to see available themes",
            "Backup your config with 'geex backup' regularly",
        ]
        return random.choice(tips)

    def suggest_for(self, query):
        """Suggest commands based on query."""
        suggestions = {
            "system": ["geex info", "geex sysfetch", "geex monitor"],
            "performance": ["geex benchmark", "geex cpu", "geex memory"],
            "battery": ["geex battery", "geex doctor"],
            "network": ["geex network"],
            "storage": ["geex storage", "geex clean"],
        }
        for keyword, cmds in suggestions.items():
            if keyword in query.lower():
                return cmds
        return ["geex help"]

def run():
    """Plugin entry point."""
    ai = AIAssistantPlugin()
    print(f"[AI Assistant] {ai.get_tip()}")

if __name__ == "__main__":
    run()
