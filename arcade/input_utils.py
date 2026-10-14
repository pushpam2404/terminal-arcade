"""Helpers for reading input from the player.

Every game uses these instead of calling input() directly, so that asking a
question behaves the same way everywhere.
"""

from __future__ import annotations

import sys

from arcade import art


def _handle_interrupt(exc: BaseException) -> None:
    """Print a goodbye message to stderr and exit cleanly.

    Ctrl+C exits with status 130; Ctrl+D exits with status 0.
    """
    print("\nGoodbye!", file=sys.stderr)
    if isinstance(exc, KeyboardInterrupt):
        sys.exit(130)
    sys.exit(0)


def ask(prompt: str) -> str:
    """Ask the player a question and return whatever they typed.

    Args:
        prompt: The question to show, without a trailing space.

    Returns:
        The raw text the player typed.
    """
    try:
        return input(f"{prompt} ")
    except (KeyboardInterrupt, EOFError) as exc:
        _handle_interrupt(exc)


def ask_int(prompt: str, minimum: int | None = None, maximum: int | None = None) -> int:
    """Ask for a whole number, and keep asking until we get a valid one.

    Args:
        prompt: The question to show.
        minimum: Smallest allowed value, or None for no lower bound.
        maximum: Largest allowed value, or None for no upper bound.

    Returns:
        A number the player typed that is within range.
    """
    while True:
        raw = ask(prompt)
        try:
            value = int(raw)
        except ValueError:
            print(art.red(f"  '{raw}' is not a whole number. Try again."))
            continue

        if minimum is not None and value < minimum:
            print(art.red(f"  Too low — the smallest allowed is {minimum}."))
            continue
        if maximum is not None and value > maximum:
            print(art.red(f"  Too high — the largest allowed is {maximum}."))
            continue

        return value


def ask_choice(prompt: str, choices: list[str]) -> str:
    """Ask the player to pick one of several options.

    Matching ignores capital letters, so "ROCK", "Rock" and "rock" all work.

    Args:
        prompt: The question to show.
        choices: The allowed answers.

    Returns:
        The matching entry from `choices`, in its original spelling.
    """
    lowered = {c.lower(): c for c in choices}
    options = "/".join(choices)
    while True:
        raw = ask(f"{prompt} ({options})")
        if raw.lower() in lowered:
            return lowered[raw.lower()]
        print(art.red(f"  Please type one of: {options}"))


def ask_letter(prompt: str) -> str:
    """Ask for a single letter A-Z and return it in lowercase."""
    while True:
        raw = ask(prompt).lower()
        if len(raw) == 1 and raw.isalpha():
            return raw
        print(art.red("  Please type exactly one letter."))


def confirm(prompt: str) -> bool:
    """Ask a yes/no question. Returns True for yes."""
    answer = ask_choice(prompt, ["y", "n"])
    return answer == "y"


def pause(message: str = "Press Enter to continue...") -> None:
    """Wait for the player to press Enter."""
    try:
        input(art.dim(message))
    except (KeyboardInterrupt, EOFError) as exc:
        _handle_interrupt(exc)
