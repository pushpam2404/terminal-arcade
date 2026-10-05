"""Pick a target total and try to match it with two dice."""

from __future__ import annotations

import random

from arcade import art
from arcade.input_utils import ask_int

NAME = "Dice Roll"
DESCRIPTION = "Pick a total and see how close two dice land"


def score_for(target: int, total: int) -> int:
    """Award points for matching or nearly matching the target.

    Args:
        target: The player's chosen total, from 2 to 12.
        total: The sum of the two dice.

    Returns:
        100 for an exact match, 40 when off by one, otherwise 0.
    """
    difference = abs(target - total)
    if difference == 0:
        return 100
    if difference == 1:
        return 40
    return 0


def play() -> int:
    """Roll two dice against the player's target.

    Returns:
        Points earned for how closely the dice match the target.
    """
    print(art.banner("DICE ROLL"))
    target = ask_int("  Pick a target total (2–12):", minimum=2, maximum=12)
    first = random.randint(1, 6)
    second = random.randint(1, 6)
    total = first + second
    print(f"  Dice: {first} and {second}. Total: {total}.")
    points = score_for(target, total)
    if points == 100:
        print(art.green("  Exact match! 100 points."))
    elif points == 40:
        print(art.yellow("  Just one away! 40 points."))
    else:
        print(art.red("  No match this time. 0 points."))
    return points
