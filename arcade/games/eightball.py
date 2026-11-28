"""Magic 8-Ball."""

from __future__ import annotations

import random

from arcade.input_utils import ask

NAME = "Magic 8-Ball"
DESCRIPTION = "Ask a question and receive a mysterious answer"

ANSWERS = [
    "Definitely.",
    "It is certain.",
    "Without a doubt.",
    "Yes, absolutely.",
    "Most likely.",
    "The signs point to yes.",
    "Ask again later.",
    "Cannot predict that right now.",
    "Maybe.",
    "The answer is unclear.",
    "Probably not.",
    "The signs point to no.",
    "Don't count on it.",
    "Very unlikely.",
]


def get_answer() -> str:
    """Return a random Magic 8-Ball answer.

    Returns:
        A mysterious prediction string selected from ANSWERS.
    """
    return random.choice(ANSWERS)


def play() -> int:
    """Run one round of Magic 8-Ball.

    Returns:
        Always returns 0 as Magic 8-Ball is an oracle experience without scoring.
    """
    print("\n  Ask the Magic 8-Ball a question.\n")
    question = ask("  Your question:")

    if question.strip():
        print(f"\n  The Magic 8-Ball says: {get_answer()}\n")
    else:
        print("\n  You need to ask a question first.\n")

    return 0
