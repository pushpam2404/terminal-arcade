"""Coin Flip.

Call heads or tails. Get it right three times in a row to win.
"""

from __future__ import annotations

import random

from arcade import art
from arcade.input_utils import ask_choice

NAME = "Coin Flip"
DESCRIPTION = "Call it right three times in a row"

ROUNDS = 3


def flip() -> str:
    """Flip a coin. Returns "heads" or "tails"."""
    return random.choice(["heads", "tails"])


def play() -> int:
    """Run one game of Coin Flip.

    Returns:
        The player's score. 0 if they got one wrong.
    """
    print(art.banner("COIN FLIP"))
    print(f"\n  Call it right {ROUNDS} times in a row.\n")

    for round_number in range(1, ROUNDS + 1):
        call = ask_choice(f"  Round {round_number} — heads or tails?", ["heads", "tails"])
        result = flip()
        print(f"  The coin lands on {art.bold(result)}.")

        if call != result:
            print(art.red(f"\n  Wrong. You got {round_number - 1} in a row.\n"))
            return 0

        print(art.green("  Correct.\n"))

    print(art.green(f"  {ROUNDS} in a row. Very nice.\n"))
    return ROUNDS * 30
