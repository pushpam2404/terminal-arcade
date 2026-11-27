"""Guess the Number.

The computer picks a secret number and you try to find it. After each guess it
tells you whether to go higher or lower.
"""

from __future__ import annotations

import random
from typing import Any

from arcade import art
from arcade.input_utils import ask_choice, ask_int

NAME = "Guess the Number"
DESCRIPTION = "Find the secret number in as few guesses as you can"

LOWEST = 1
HIGHEST = 100
MAX_GUESSES = 7

DIFFICULTIES: dict[str, dict[str, Any]] = {
    "easy": {
        "name": "Easy",
        "lowest": 1,
        "highest": 50,
        "max_guesses": 8,
        "multiplier": 5,
    },
    "normal": {
        "name": "Normal",
        "lowest": 1,
        "highest": 100,
        "max_guesses": 7,
        "multiplier": 10,
    },
    "hard": {
        "name": "Hard",
        "lowest": 1,
        "highest": 500,
        "max_guesses": 9,
        "multiplier": 20,
    },
}


def score_for(
    guesses_used: int,
    max_guesses: int = MAX_GUESSES,
    multiplier: int = 10,
) -> int:
    """Work out a score from how many guesses the player needed.

    Fewer guesses is better, so the first guess is worth the most.

    Args:
        guesses_used: How many guesses the player took.
        max_guesses: The maximum guesses allowed for this round.
        multiplier: Points multiplier based on difficulty.

    Returns:
        Points, never below zero.
    """
    if guesses_used > max_guesses:
        return 0
    return max(0, (max_guesses - guesses_used + 1) * multiplier)


def evaluate(guess: int, secret: int) -> str:
    """Compare a guess with the secret number.

    Args:
        guess: What the player guessed.
        secret: The number they are trying to find.

    Returns:
        One of "correct", "too low", or "too high".
    """
    if guess == secret:
        return "correct"
    if guess < secret:
        return "too low"
    return "too high"


def play() -> int:
    """Run one round of Guess the Number.

    Returns:
        The player's score for this round.
    """
    global NAME
    print(art.GUESS_BANNER)
    level = ask_choice("  Select difficulty", ["easy", "normal", "hard"]).lower()
    config = DIFFICULTIES[level]

    lowest = config["lowest"]
    highest = config["highest"]
    max_guesses = config["max_guesses"]
    multiplier = config["multiplier"]
    NAME = f"Guess ({config['name']})"

    print(f"\n  Difficulty: {art.bold(config['name'])}")
    print(f"  I am thinking of a number between {lowest} and {highest}.")
    print(f"  You have {max_guesses} guesses.\n")

    secret = random.randint(lowest, highest)

    for attempt in range(1, max_guesses + 1):
        remaining = max_guesses - attempt + 1
        guess = ask_int(
            f"  Guess {attempt}/{max_guesses} ({remaining} left):",
            minimum=lowest,
            maximum=highest,
        )

        result = evaluate(guess, secret)
        if result == "correct":
            points = score_for(attempt, max_guesses=max_guesses, multiplier=multiplier)
            print(art.green(f"\n  Got it. The number was {secret}."))
            print(f"  You found it in {attempt} guess(es) — {points} points.\n")
            return points

        if result == "too low":
            print(art.yellow("  Too low. Aim higher."))
        else:
            print(art.yellow("  Too high. Aim lower."))

    print(art.red(f"\n  Out of guesses. The number was {secret}.\n"))
    return 0
