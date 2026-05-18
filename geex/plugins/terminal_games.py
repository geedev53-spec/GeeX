#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeeX OS Plugin: Terminal Games - Mini games for the terminal."""

import random
import os

class TerminalGamesPlugin:
    def __init__(self):
        self.name = "terminal_games"
        self.version = "1.0.0"

    def quiz(self):
        """Simple tech quiz."""
        questions = [
            ("What does CPU stand for?", "Central Processing Unit"),
            ("What is the default port for HTTP?", "80"),
            ("What does RAM stand for?", "Random Access Memory"),
            ("What command lists files in Linux?", "ls"),
            ("What is Python's file extension?", ".py"),
        ]

        q = random.choice(questions)
        print(f"\n\033[96m❓ {q[0]}\033[0m")
        answer = input("\033[93mYour answer: \033[0m").strip().lower()

        if answer in q[1].lower() or answer == q[1].lower():
            print("\033[92m✓ Correct!\033[0m\n")
        else:
            print(f"\033[91m✗ Wrong! The answer is: {q[1]}\033[0m\n")

    def dice(self):
        """Roll dice."""
        result = random.randint(1, 6)
        dice_faces = {
            1: ["┌─────┐", "│     │", "│  ●  │", "│     │", "└─────┘"],
            2: ["┌─────┐", "│ ●   │", "│     │", "│   ● │", "└─────┘"],
            3: ["┌─────┐", "│ ●   │", "│  ●  │", "│   ● │", "└─────┘"],
            4: ["┌─────┐", "│ ● ● │", "│     │", "│ ● ● │", "└─────┘"],
            5: ["┌─────┐", "│ ● ● │", "│  ●  │", "│ ● ● │", "└─────┘"],
            6: ["┌─────┐", "│ ● ● │", "│ ● ● │", "│ ● ● │", "└─────┘"],
        }

        print("\033[96m🎲 Rolling...\033[0m")
        for line in dice_faces[result]:
            print(f"  \033[97m{line}\033[0m")
        print(f"\033[92m  You rolled: {result}\033[0m\n")

    def coin(self):
        """Flip a coin."""
        result = random.choice(["Heads", "Tails"])
        print(f"\033[96m🪙 Flipping coin...\033[0m")
        print(f"\033[97m  Result: {result}!\033[0m\n")

def run():
    """Plugin entry point."""
    games = TerminalGamesPlugin()
    print("\033[96m🎮 GeeX Mini Games\033[0m\n")
    print("  \033[94m1. Tech Quiz\033[0m")
    print("  \033[94m2. Roll Dice\033[0m")
    print("  \033[94m3. Flip Coin\033[0m")

    choice = input("\n\033[93mChoose (1-3): \033[0m").strip()

    if choice == "1":
        games.quiz()
    elif choice == "2":
        games.dice()
    elif choice == "3":
        games.coin()

if __name__ == "__main__":
    run()
