
"""The arcade menu — pick a game, play it, come back to the menu.

Games are registered in GAMES below. Each entry points at a module that
provides NAME, DESCRIPTION, and a play() function returning a score.
"""

from __future__ import annotations

import random
import sys
from types import ModuleType

from arcade import __version__, art, scoreboard
from arcade.games import coinflip, diceroll, eightball, guess, hangman, rps, scramble, tictactoe
from arcade.input_utils import ask, confirm, pause, read_key


# To add a game: write arcade/games/yourgame.py, import it above, and add it
GAMES: list[ModuleType] = [
    guess,
    hangman,
    rps,
    tictactoe,
    coinflip,
    diceroll,
    eightball,
    scramble,
]


def show_menu() -> None:
    """Print the list of games and the extra options."""
    print(art.ARCADE_BANNER)
    print(art.dim(f"  v{__version__}  ·  github-community-gitam\n"))

    for number, game in enumerate(GAMES, start=1):
        print(f"  {number}. {art.bold(game.NAME)}")
        print(f"     {art.dim(game.DESCRIPTION)}")

    print("\n  S. Surprise me")
    print("  H. High scores")
    print("  Q. Quit\n")


def show_high_scores() -> None:
    """Print the overall top scores."""
    print(f"\n{art.bold('  HIGH SCORES')}\n")
    print(scoreboard.format_scoreboard(scoreboard.top_scores(limit=10)))
    print()


def run_game(game: ModuleType) -> None:
    """Play one game and offer to save the score."""
    print()
    score = game.play()

    while True:
        if score and score > 0:
            if confirm("  Save this score to the scoreboard?"):
                name = ask("  Your name:").strip() or "anonymous"
                scoreboard.save_score(game.NAME, name, score)
                print(art.green("  Saved.\n"))
                pause()

        if confirm("  Want to play again?"):
            score = game.play()
        else:
            break


def main() -> None:
    """Start the arcade. Loops until the player chooses to quit."""
    while True:
        show_menu()
        key = read_key("  What would you like to play? ").lower()

        if key == "q":
            print(art.cyan("\n  Thanks for playing. See you next time.\n"))
            return

        if key == "h":
            show_high_scores()
            pause()
            continue

        if key == "s":
            game = random.choice(GAMES)
            print(f"\n  Surprise! You're playing {game.NAME}!")
            run_game(game)
            pause()
            continue

        if key.isdigit() and 1 <= int(key) <= len(GAMES):
            run_game(GAMES[int(key) - 1])
            pause()
            continue

        print(art.red("  Please press a valid menu key."))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!", file=sys.stderr)
        sys.exit(130)
    except EOFError:
        print("\nGoodbye!", file=sys.stderr)
        sys.exit(0)
