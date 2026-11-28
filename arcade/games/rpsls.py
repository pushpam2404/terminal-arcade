"""Rock Paper Scissors Lizard Spock.

Best of five against the computer with five moves.
"""

from __future__ import annotations

import random

from arcade import art
from arcade.input_utils import ask_choice

NAME = "Rock Paper Scissors Lizard Spock"
DESCRIPTION = "The five-move expansion: best of five against the computer"

MOVES = ["rock", "paper", "scissors", "lizard", "spock"]
ROUNDS = 5

# What each move defeats.
BEATS: dict[str, set[str]] = {
    "rock": {"scissors", "lizard"},
    "paper": {"rock", "spock"},
    "scissors": {"paper", "lizard"},
    "lizard": {"paper", "spock"},
    "spock": {"rock", "scissors"},
}

# Verbs explaining why a move defeats another.
VERBS: dict[tuple[str, str], str] = {
    ("scissors", "paper"): "cuts",
    ("paper", "rock"): "covers",
    ("rock", "lizard"): "crushes",
    ("lizard", "spock"): "poisons",
    ("spock", "scissors"): "smashes",
    ("scissors", "lizard"): "decapitates",
    ("lizard", "paper"): "eats",
    ("paper", "spock"): "disproves",
    ("spock", "rock"): "vaporizes",
    ("rock", "scissors"): "crushes",
}

EMOJI = {
    "rock": "(rock)",
    "paper": "(paper)",
    "scissors": "(scissors)",
    "lizard": "(lizard)",
    "spock": "(spock)",
}


def reason(winner: str, loser: str) -> str:
    """Return the phrase explaining why winner defeats loser.

    Example:
        reason("lizard", "spock") -> "lizard poisons spock"

    Args:
        winner: The winning move name.
        loser: The defeated move name.

    Returns:
        An explanatory string, e.g. 'lizard poisons spock'.
    """
    verb = VERBS.get((winner, loser), "beats")
    return f"{winner} {verb} {loser}"


def decide(player: str, computer: str) -> str:
    """Work out who won a single round.

    Args:
        player: The player's move (matching ignores capital letters).
        computer: The computer's move (matching ignores capital letters).

    Returns:
        "player", "computer", or "draw".
    """
    p = player.lower()
    c = computer.lower()
    if p == c:
        return "draw"
    if c in BEATS.get(p, set()):
        return "player"
    return "computer"


def play() -> int:
    """Run one best-of-five match.

    Returns:
        The player's score: 20 points per round won.
    """
    print(
        art.fit(
            art.RPSLS_BANNER, fallback_title="Rock Paper Scissors Lizard Spock"
        ).strip("\r\n")
    )
    print(f"\n  First to win the most of {ROUNDS} rounds.\n")

    player_wins = 0
    computer_wins = 0

    for round_number in range(1, ROUNDS + 1):
        print(art.rule())
        print(
            f"  Round {round_number} of {ROUNDS}   (you {player_wins} — {computer_wins} computer)\n"
        )

        player_move = ask_choice("  Your move?", MOVES).lower()
        computer_move = random.choice(MOVES)

        print(f"\n  You:      {EMOJI[player_move]} {player_move}")
        print(f"  Computer: {EMOJI[computer_move]} {computer_move}\n")

        outcome = decide(player_move, computer_move)
        if outcome == "player":
            player_wins += 1
            print(art.green(f"  You win the round — {reason(player_move, computer_move)}."))
        elif outcome == "computer":
            computer_wins += 1
            print(art.red(f"  Computer wins — {reason(computer_move, player_move)}."))
        else:
            print(art.yellow("  A draw. Nobody scores."))
        print()

    print(art.rule("="))
    print(f"  Final score — you {player_wins}, computer {computer_wins}\n")

    if player_wins > computer_wins:
        print(art.green("  You win the match.\n"))
    elif computer_wins > player_wins:
        print(art.red("  The computer wins the match.\n"))
    else:
        print(art.yellow("  The match is a draw.\n"))

    return player_wins * 20
