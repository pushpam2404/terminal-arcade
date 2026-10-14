"""Tests for the scoreboard."""

import json

import pytest

from arcade import scoreboard


def test_loading_a_missing_file_gives_an_empty_list(tmp_path):
    assert scoreboard.load_scores(tmp_path / "nothing.json") == []


def test_loading_a_corrupt_file_gives_an_empty_list_instead_of_crashing(tmp_path):
    broken = tmp_path / "scores.json"
    broken.write_text("{ this is not valid json", encoding="utf-8")
    assert scoreboard.load_scores(broken) == []


def test_saving_a_score_writes_it_to_disk(tmp_path):
    path = tmp_path / "scores.json"
    scoreboard.save_score("hangman", "asha", 70, path=path)
    saved = scoreboard.load_scores(path)
    assert len(saved) == 1
    assert saved[0]["player"] == "asha"
    assert saved[0]["score"] == 70


def test_a_saved_score_records_the_game_and_a_date(tmp_path):
    path = tmp_path / "scores.json"
    entry = scoreboard.save_score("guess", "ravi", 50, path=path)
    assert entry["game"] == "guess"
    assert entry["date"]


def test_scores_accumulate(tmp_path):
    path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "a", 1, path=path)
    scoreboard.save_score("guess", "b", 2, path=path)
    assert len(scoreboard.load_scores(path)) == 2


def test_top_scores_puts_the_best_first(tmp_path):
    path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "low", 3, path=path)
    scoreboard.save_score("guess", "high", 9, path=path)
    scoreboard.save_score("guess", "mid", 5, path=path)

    top = scoreboard.top_scores(path=path)
    assert [e["player"] for e in top] == ["high", "mid", "low"]


def test_top_scores_can_filter_by_game(tmp_path):
    path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "a", 5, path=path)
    scoreboard.save_score("hangman", "b", 7, path=path)

    top = scoreboard.top_scores(game="hangman", path=path)
    assert len(top) == 1
    assert top[0]["player"] == "b"


def test_top_scores_respects_the_limit(tmp_path):
    path = tmp_path / "scores.json"
    for i in range(9):
        scoreboard.save_score("guess", f"p{i}", i, path=path)
    assert len(scoreboard.top_scores(limit=3, path=path)) == 3


def test_an_empty_scoreboard_renders_a_friendly_message():
    assert "No scores yet" in scoreboard.format_scoreboard([])


def test_the_scoreboard_table_includes_the_player_and_score():
    table = scoreboard.format_scoreboard(
        [{"player": "asha", "game": "hangman", "score": 70, "date": "2026-10-05 15:30"}]
    )
    assert "asha" in table
    assert "70" in table


def test_top_scores_compares_numbers_and_legacy_strings(tmp_path):
    path = tmp_path / "scores.json"
    path.write_text(json.dumps([
        {"score": 9}, {"score": 100}, {"score": "50"}, {"score": 20},
    ]), encoding="utf-8")
    assert [entry["score"] for entry in scoreboard.top_scores(path=path)] == [100, "50", 20, 9]


@pytest.mark.parametrize("bad_score", ["not a score", None, [], {}, "NaN", "Infinity"])
def test_top_scores_handles_invalid_scores(tmp_path, bad_score):
    path = tmp_path / "scores.json"
    path.write_text(json.dumps([
        {"score": bad_score, "player": "invalid"},
        {"score": 9, "player": "valid"},
    ]), encoding="utf-8")
    assert [entry["player"] for entry in scoreboard.top_scores(path=path)] == ["valid", "invalid"]


def test_player_name_longer_than_14_characters_is_truncated():
    long_player = "verylongplayernameexceedingfourteen"
    table = scoreboard.format_scoreboard([
        {"player": long_player, "game": "guess", "score": 100, "date": "2026-10-15 00:00"}
    ])
    assert long_player[:14] in table
    assert long_player not in table


def test_game_name_longer_than_14_characters_is_truncated():
    long_game = "superduperlonggamename"
    table = scoreboard.format_scoreboard([
        {"player": "samar", "game": long_game, "score": 50, "date": "2026-10-15 00:00"}
    ])
    assert long_game[:14] in table
    assert long_game not in table


def test_missing_player_or_score_key_does_not_raise():
    table = scoreboard.format_scoreboard([
        {"game": "hangman"},
        {"player": "bob"}
    ])
    assert "?" in table
    assert "0" in table
    assert "hangman" in table
    assert "bob" in table


def test_multiple_entries_are_numbered_sequentially_starting_from_one():
    entries = [
        {"player": "alice", "game": "guess", "score": 10},
        {"player": "bob", "game": "hangman", "score": 20},
        {"player": "carol", "game": "tictactoe", "score": 30},
    ]
    table = scoreboard.format_scoreboard(entries)
    lines = [line for line in table.splitlines() if line.strip() and not line.strip().startswith("-") and not "Player" in line]
    assert len(lines) == 3
    assert lines[0].strip().startswith("1  ")
    assert lines[1].strip().startswith("2  ")
    assert lines[2].strip().startswith("3  ")


def test_scoreboard_table_includes_the_header_and_divider_rows():
    table = scoreboard.format_scoreboard([
        {"player": "alice", "game": "guess", "score": 10, "date": "2026-10-15 00:00"}
    ])
    lines = table.splitlines()
    assert len(lines) >= 3
    assert "Player" in lines[0] and "Game" in lines[0] and "Score" in lines[0] and "Date" in lines[0]
    assert "--------------" in lines[1]

