"""The arcade menu — pick a game, play it, come back to the menu.

Games are registered in GAMES below. Each entry points at a module that
provides NAME, DESCRIPTION, and a play() function returning a score.
"""

from __future__ import annotations

import random
import importlib
import pkgutil
import sys
from pathlib import Path
from types import ModuleType

from arcade import __version__, art, scoreboard
import arcade.games
from arcade.input_utils import ask, ask_int, confirm, pause, read_key

CANONICAL_ORDER = [
    "guess",
    "hangman",
    "rps",
    "rpsls",
    "tictactoe",
    "coinflip",
    "diceroll",
    "eightball",
    "scramble",
]


def discover_games(package=arcade.games) -> list[ModuleType]:
    """Discover and return all valid game modules from arcade.games.

    Modules starting with '_' are ignored.
    Modules missing NAME, DESCRIPTION, or play are skipped with a warning.
    Modules with syntax or import errors are skipped with a warning.
    Results are sorted deterministically so menu order remains stable.

    Args:
        package: The package containing game modules. Defaults to arcade.games.

    Returns:
        A list of valid game modules.
    """
    discovered: list[ModuleType] = []

    for module_info in pkgutil.iter_modules(package.__path__):
        name = module_info.name
        if name.startswith("_"):
            continue

        full_name = f"{package.__name__}.{name}"
        try:
            mod = importlib.import_module(full_name)
        except Exception as err:
            print(f"Warning: could not import game module '{name}': {err}", file=sys.stderr)
            continue

        missing = [attr for attr in ("NAME", "DESCRIPTION", "play") if not hasattr(mod, attr)]
        if missing:
            print(
                f"Warning: skipping game module '{name}': missing {', '.join(missing)}",
                file=sys.stderr,
            )
            continue

        if not callable(getattr(mod, "play", None)):
            print(
                f"Warning: skipping game module '{name}': 'play' is not callable",
                file=sys.stderr,
            )
            continue

        discovered.append(mod)

    discovered.sort(
        key=lambda m: (
            CANONICAL_ORDER.index(m.__name__.rsplit(".", 1)[-1])
            if m.__name__.rsplit(".", 1)[-1] in CANONICAL_ORDER
            else 999,
            m.__name__,
        )
    )
    return discovered


GAMES: list[ModuleType] = discover_games()


def show_menu(scores_path: Path | None = None) -> None:
    """Print the list of games and the extra options."""
    print(art.fit(art.ARCADE_BANNER, fallback_title="Terminal Arcade").strip("\r\n"))
    print(art.dim(f"  v{__version__}  ·  github-community-gitam"))

    for number, game in enumerate(GAMES, start=1):
        print(f"  {number}. {art.bold(game.NAME)} - {art.dim(game.DESCRIPTION)}")

    scores = scoreboard.load_scores(scores_path)
    count = len(scores)
    score_suffix = f" ({count} played)" if count > 0 else ""

    print()
    print("  S. Surprise me")
    print(f"  H. High scores{score_suffix}")
    print("  T. Statistics")
    print("  Q. Quit")
    print(art.dim("  Press Ctrl+C at any time to quit"))


def show_statistics(scores_path: Path | None = None) -> None:
    """Print per-game statistics."""
    print(f"\n{art.bold('  GAME STATISTICS')}\n")
    for number, game in enumerate(GAMES, start=1):
        print(f"  {number}. {game.NAME}")
    print()
    choice = ask_int("  Which game? ", minimum=1, maximum=len(GAMES))
    selected_game = GAMES[choice - 1]
    stats = scoreboard.stats_for(selected_game.NAME, path=scores_path)

    print(f"\n{art.bold(f'  {selected_game.NAME.upper()} STATS')}")
    print(art.dim("  " + "-" * 32))
    if stats["games_played"] == 0:
        print(f"  No games of {selected_game.NAME} played yet.\n")
    else:
        print(f"  Games played:   {stats['games_played']}")
        print(f"  Best score:     {stats['best_score']}")
        print(f"  Average score:  {stats['average_score']}")
        print(f"  Last played:    {stats['last_played']}\n")


def show_high_scores(scores_path: Path | None = None) -> None:
    """Print the overall top scores, with an optional player filter."""
    print(f"\n{art.bold('  HIGH SCORES')}\n")
    print(scoreboard.format_scoreboard(scoreboard.top_scores(limit=10, path=scores_path)))
    print()
    default_player = scoreboard.get_last_player(scores_path)
    prompt = (
        f"  Filter by player (Enter to skip) [{default_player}]: "
        if default_player
        else "  Filter by player (Enter to skip): "
    )
    filter_name = ask(prompt).strip()
    if not filter_name and default_player:
        # If user pressed enter and there is a default player, don't auto-filter unless requested,
        # but if they typed '.', use the default.
        pass
    if filter_name:
        if filter_name == "." and default_player:
            filter_name = default_player
        player_scores = scoreboard.scores_for_player(filter_name, path=scores_path)
        if player_scores:
            print(f"\n{art.bold(f'  SCORES FOR {filter_name.upper()}')}\n")
            print(scoreboard.format_scoreboard(player_scores))
            print()
        else:
            print(f"\n  No scores found for '{filter_name}'.\n")


def run_game(game: ModuleType, scores_path: Path | None = None) -> None:
    """Play one game and offer to save the score."""
    print()
    score = game.play()

    while True:
        if score and score > 0:
            if confirm("  Save this score to the scoreboard?"):
                default_name = scoreboard.get_last_player(scores_path)
                prompt = f"  Your name [{default_name}]:" if default_name else "  Your name:"
                entered = ask(prompt).strip()
                name = entered if entered else (default_name or "anonymous")
                scoreboard.save_score(game.NAME, name, score, path=scores_path)
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

        if key == "t":
            show_statistics()
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
