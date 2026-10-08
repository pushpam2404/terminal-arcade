"""Hangman.

Guess the hidden word one letter at a time. Six wrong guesses and the drawing
is finished.
"""

from __future__ import annotations

import random

from arcade import art
from arcade.input_utils import ask_letter

NAME = "Hangman"
DESCRIPTION = "Guess the word before the drawing is finished"

MAX_WRONG = 6

WORDS = [
    "python",
    "commit",
    "branch",
    "merge",
    "repository",
    "terminal",
    "variable",
    "function",
    "keyboard",
    "compile",
    "debug",
    "syntax",
    "pointer",
    "recursion",
    "boolean",
    "iterate",
    "package",
    "version",
]


def mask_word(word: str, guessed: set[str]) -> str:
    """Show the word with unguessed letters hidden.

    Args:
        word: The secret word.
        guessed: Letters the player has already guessed.

    Returns:
        The word with underscores for letters not yet found, spaced out so it
        is readable, e.g. "p _ t h _ n".
    """
    return " ".join(letter if letter in guessed else "_" for letter in word)


def is_solved(word: str, guessed: set[str]) -> bool:
    """Return True if every letter in the word has been guessed."""
    return all(letter in guessed for letter in word)


def score_for(word: str, wrong: int) -> int:
    """Score a completed game.

    Longer words and fewer mistakes score higher.

    Args:
        word: The word that was being guessed.
        wrong: How many wrong guesses the player made.

    Returns:
        Points, never below zero.
    """
    return max(0, len(word) * 10 - wrong * 10)


def play() -> int:
    """Run one round of Hangman.

    Returns:
        The player's score for this round.
    """
    print(art.HANGMAN_BANNER)

    word = random.choice(WORDS)
    guessed: set[str] = set()
    wrong = 0

    while wrong < MAX_WRONG and not is_solved(word, guessed):
        print(art.GALLOWS[wrong])
        print(f"\n  Word:  {art.bold(mask_word(word, guessed))}")
        print(f"  Wrong guesses left: {MAX_WRONG - wrong}")
        if guessed:
            print(f"  Already tried: {' '.join(sorted(guessed))}")
        print()

        letter = ask_letter("  Guess a letter:")

        if letter in guessed:
            print(art.yellow(f"  You already tried '{letter}'."))
        elif letter in word:
            guessed.add(letter)
            print(art.green(f"  Yes — '{letter}' is in the word."))
        else:
            guessed.add(letter)
            wrong += 1
            print(art.red(f"  No — '{letter}' is not in the word."))

    print(art.GALLOWS[min(wrong, MAX_WRONG)])

    if is_solved(word, guessed):
        points = score_for(word, wrong)
        print(art.green(f"\n  You got it. The word was '{word}'."))
        print(f"  {points} points.\n")
        return points

    print(art.red(f"\n  Out of guesses. The word was '{word}'.\n"))
    return 0
