"""Keeps track of high scores between sessions.

Scores are stored as JSON in the player's home directory, so they survive
closing the terminal. The file is created the first time a score is saved.
"""

from __future__ import annotations

import json
import math
import os
import sqlite3
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

SCORES_PATH = Path.home() / ".terminal-arcade" / "scores.json"
SQLITE_SCORES_PATH = Path.home() / ".terminal-arcade" / "scores.db"


def is_sqlite_enabled() -> bool:
    """Return True if the SQLite scores backend is activated."""
    return os.environ.get("ARCADE_STORAGE", "").strip().lower() == "sqlite"


def _sqlite_target(path: Path | None = None) -> Path:
    """Determine the SQLite database path given an optional override path."""
    if path is not None:
        if path.suffix == ".db":
            return path
        return path.with_suffix(".db")
    return SQLITE_SCORES_PATH


def _init_sqlite_db(db_path: Path, json_source: Path | None = None) -> sqlite3.Connection:
    """Initialize the SQLite database schema and auto-migrate existing JSON data.

    Args:
        db_path: Path to the SQLite database file.
        json_source: Optional path to an existing JSON scores file to import.

    Returns:
        An open sqlite3.Connection.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), timeout=30.0)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL,
            player TEXT NOT NULL,
            score REAL NOT NULL,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM scores")
    count = cursor.fetchone()[0]
    if count == 0:
        json_path = json_source or (
            db_path.with_suffix(".json") if db_path.suffix == ".db" else SCORES_PATH
        )
        if json_path.exists():
            try:
                raw = json_path.read_text(encoding="utf-8")
                entries = json.loads(raw)
                if isinstance(entries, list):
                    for e in entries:
                        if isinstance(e, dict):
                            g = str(e.get("game", ""))
                            p = str(e.get("player", ""))
                            s = float(e.get("score", 0))
                            d = str(e.get("date", ""))
                            cursor.execute(
                                "INSERT INTO scores (game, player, score, date) VALUES (?, ?, ?, ?)",
                                (g, p, s, d),
                            )
                    conn.commit()
            except Exception:
                pass
    return conn


def _ensure_file() -> None:
    """Create the scores file and its folder if they do not exist yet."""
    SCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SCORES_PATH.exists():
        SCORES_PATH.write_text("[]", encoding="utf-8")


def load_scores(path: Path | None = None) -> list[dict[str, Any]]:
    """Read every saved score.

    A corrupt or unreadable file or database is treated as empty rather than
    crashing the arcade — losing a scoreboard is annoying, losing the whole game is worse.

    Args:
        path: Where to read from. Defaults to the player's scores file.

    Returns:
        A list of score entries. Empty if nothing has been saved yet.
    """
    if is_sqlite_enabled():
        db_path = _sqlite_target(path)
        json_src = (
            path
            if (path and path.suffix == ".json")
            else (db_path.with_suffix(".json") if db_path.suffix == ".db" else SCORES_PATH)
        )
        try:
            conn = _init_sqlite_db(db_path, json_source=json_src)
            cursor = conn.cursor()
            cursor.execute("SELECT game, player, score, date FROM scores ORDER BY id ASC")
            rows = cursor.fetchall()
            conn.close()
            result: list[dict[str, Any]] = []
            for g, p, s, d in rows:
                score_val = int(s) if float(s).is_integer() else s
                result.append({"game": g, "player": p, "score": score_val, "date": d})
            return result
        except (sqlite3.DatabaseError, sqlite3.OperationalError, OSError):
            return []

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
    entry = {
        "game": game,
        "player": player,
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    if is_sqlite_enabled():
        db_path = _sqlite_target(path)
        json_src = (
            path
            if (path and path.suffix == ".json")
            else (db_path.with_suffix(".json") if db_path.suffix == ".db" else SCORES_PATH)
        )
        try:
            conn = _init_sqlite_db(db_path, json_source=json_src)
            with conn:
                conn.execute(
                    "INSERT INTO scores (game, player, score, date) VALUES (?, ?, ?, ?)",
                    (entry["game"], entry["player"], float(entry["score"]), entry["date"]),
                )
            conn.close()
            return entry
        except (sqlite3.DatabaseError, sqlite3.OperationalError, OSError):
            return entry

    target = path or SCORES_PATH
    if path is None:
        _ensure_file()
    else:
        target.parent.mkdir(parents=True, exist_ok=True)

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


def stats_for(game: str, path: Path | None = None) -> dict[str, Any]:
    """Calculate summary statistics for a particular game.

    Args:
        game: Only show statistics for this game.
        path: Where to read from. Defaults to the player's scores file.

    Returns:
        A dict with games_played, best_score, average_score, and last_played.
    """
    entries = top_scores(game=game, limit=100_000, path=path)
    if not entries:
        return {
            "games_played": 0,
            "best_score": None,
            "average_score": None,
            "last_played": None,
        }

    scores: list[float] = []
    for entry in entries:
        try:
            val = float(entry.get("score", 0))
            if math.isfinite(val):
                scores.append(val)
        except (TypeError, ValueError, OverflowError):
            continue

    games_played = len(entries)
    if not scores:
        return {
            "games_played": games_played,
            "best_score": 0,
            "average_score": 0.0,
            "last_played": entries[-1].get("date", ""),
        }

    best = max(scores)
    best_score: int | float = int(best) if best.is_integer() else best

    avg = sum(scores) / len(scores)
    rounded_avg = round(avg, 1)
    average_score: int | float = int(rounded_avg) if rounded_avg.is_integer() else rounded_avg

    dates = [e.get("date", "") for e in entries if e.get("date")]
    last_played = max(dates) if dates else entries[-1].get("date", "")

    return {
        "games_played": games_played,
        "best_score": best_score,
        "average_score": average_score,
        "last_played": last_played,
    }


def _char_width(char: str) -> int:
    """Return the terminal display width of a single character."""
    return 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1


def _str_width(text: str) -> int:
    """Return the terminal display width of a string."""
    return sum(_char_width(c) for c in text)


def _format_name(name: str, width: int = 14) -> str:
    """Format and pad a player name to fit exactly `width` display columns.

    If the name exceeds `width` display columns, it is truncated with an
    ellipsis ('…') so the total display width is exactly `width`.
    """
    total_width = _str_width(name)
    if total_width <= width:
        return name + (" " * (width - total_width))

    target_width = width - _str_width("…")
    current_width = 0
    chars: list[str] = []
    for c in name:
        cw = _char_width(c)
        if current_width + cw > target_width:
            break
        chars.append(c)
        current_width += cw

    truncated = "".join(chars).rstrip() + "…"
    pad = width - _str_width(truncated)
    return truncated + (" " * pad)


def format_scoreboard(
    entries: list[dict[str, Any]],
    width: int | None = None,
) -> str:
    """Render score entries as a plain text table.

    Drops the Date column if the available width is narrower than 60 columns.

    Args:
        entries: Score entries, already in the order you want them shown.
        width: Terminal column width. Defaults to art.terminal_width().

    Returns:
        A multi-line string ready to print.
    """
    if not entries:
        return "  No scores yet. Be the first."

    if width is None:
        try:
            from arcade import art
            width = art.terminal_width()
        except Exception:
            width = 80

    include_date = width >= 60

    if include_date:
        lines = [
            "  #  Player          Game            Score  Date",
            "  -  --------------  --------------  -----  ----------------",
        ]
        for i, entry in enumerate(entries, start=1):
            player = _format_name(str(entry.get("player", "?")), 14)
            game = str(entry.get("game", "?"))[:14]
            score = entry.get("score", 0)
            date = entry.get("date", "")
            lines.append(f"  {i}  {player}  {game:<14}  {score:>5}  {date}")
    else:
        lines = [
            "  #  Player          Game            Score",
            "  -  --------------  --------------  -----",
        ]
        for i, entry in enumerate(entries, start=1):
            player = _format_name(str(entry.get("player", "?")), 14)
            game = str(entry.get("game", "?"))[:14]
            score = entry.get("score", 0)
            lines.append(f"  {i}  {player}  {game:<14}  {score:>5}")

    return "\n".join(lines)
