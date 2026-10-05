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
