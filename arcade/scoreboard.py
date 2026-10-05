"""Keeps track of high scores between sessions.

Scores are stored as JSON in the player's home directory, so they survive
closing the terminal. The file is created the first time a score is saved.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

SCORES_PATH = Path.home() / ".terminal-arcade" / "scores.json"


def _ensure_file() -> None:
    """Create the scores file and its folder if they do not exist yet."""
    SCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SCORES_PATH.exists():
        SCORES_PATH.write_text("[]", encoding="utf-8")


def load_scores(path: Path | None = None) -> list[dict[str, Any]]:
    """Read every saved score.

    A corrupt or unreadable file is treated as empty rather than crashing the
    arcade — losing a scoreboard is annoying, losing the whole game is worse.

    Args:
        path: Where to read from. Defaults to the player's scores file.

    Returns:
        A list of score entries. Empty if nothing has been saved yet.
    """
    target = path or SCORES_PATH
    if not target.exists():
        return []
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    return data


def save_score(
    game: str,
    player: str,
    score: int,
    path: Path | None = None,
) -> dict[str, Any]:
    """Add one score to the scoreboard and write it to disk.

    Args:
        game: Which game the score is for, e.g. "hangman".
        player: The player's name.
        score: The points scored. Higher is better.
        path: Where to write. Defaults to the player's scores file.

    Returns:
        The entry that was saved.
    """
    target = path or SCORES_PATH
    if path is None:
        _ensure_file()
    else:
        target.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "game": game,
        "player": player,
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    scores = load_scores(target)
    scores.append(entry)
    target.write_text(json.dumps(scores, indent=2), encoding="utf-8")
    return entry


def top_scores(
    game: str | None = None,
    limit: int = 5,
    path: Path | None = None,
) -> list[dict[str, Any]]:
    """Return the best scores, highest first.

    Args:
        game: Only show scores for this game. None means all games.
        limit: How many to return.
        path: Where to read from. Defaults to the player's scores file.

    Returns:
        Up to `limit` score entries, best first.
    """
    scores = load_scores(path)
    if game is not None:
        scores = [s for s in scores if s.get("game") == game]

    def numeric_score(entry: dict[str, Any]) -> float:
        """Read legacy numeric strings, treating invalid scores as zero."""
        try:
            score = float(entry.get("score", 0))
        except (TypeError, ValueError, OverflowError):
            return 0.0
        return score if math.isfinite(score) else 0.0

    ranked = sorted(scores, key=numeric_score, reverse=True)
    return ranked[:limit]


def format_scoreboard(entries: list[dict[str, Any]]) -> str:
    """Render score entries as a plain text table.

    Args:
        entries: Score entries, already in the order you want them shown.

    Returns:
        A multi-line string ready to print.
    """
    if not entries:
        return "  No scores yet. Be the first."

    lines = [
        "  #  Player          Game            Score  Date",
        "  -  --------------  --------------  -----  ----------------",
    ]
    for i, entry in enumerate(entries, start=1):
        player = str(entry.get("player", "?"))[:14]
        game = str(entry.get("game", "?"))[:14]
        score = entry.get("score", 0)
        date = entry.get("date", "")
        lines.append(f"  {i}  {player:<14}  {game:<14}  {score:>5}  {date}")
    return "\n".join(lines)
