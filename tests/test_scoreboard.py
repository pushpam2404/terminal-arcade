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
    assert "verylongplaye…" in table
    assert long_player not in table


def test_long_player_name_truncates_with_ellipsis():
    table = scoreboard.format_scoreboard([
        {"player": "Venkateswara Rao", "game": "guess", "score": 100, "date": "2026-10-15 00:00"}
    ])
    assert "Venkateswara…" in table
    assert "Venkateswara Rao" not in table


def test_short_player_name_is_unaffected():
    table = scoreboard.format_scoreboard([
        {"player": "asha", "game": "guess", "score": 100, "date": "2026-10-15 00:00"}
    ])
    assert "asha" in table
    assert "…" not in table


def test_player_name_with_wide_characters_preserves_row_alignment():
    entries = [
        {"player": "Venkateswara Rao", "game": "hangman", "score": 100, "date": "2026-11-28 01:00"},
        {"player": "asha", "game": "guess", "score": 80, "date": "2026-11-28 01:05"},
        {"player": "龍王伝説の勇者", "game": "rpsls", "score": 60, "date": "2026-11-28 01:10"},
        {"player": "🎮Gamer🎮", "game": "diceroll", "score": 40, "date": "2026-11-28 01:15"},
    ]
    table = scoreboard.format_scoreboard(entries)
    rows = [
        line
        for line in table.splitlines()
        if line.strip() and not line.strip().startswith("-") and "Player" not in line
    ]
    widths = [scoreboard._str_width(row) for row in rows]
    assert len(set(widths)) == 1


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
    lines = [line for line in table.splitlines() if line.strip() and not line.strip().startswith("-") and "Player" not in line]
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



def test_a_long_player_name_is_truncated_without_shifting_the_game_column():
    row = scoreboard.format_scoreboard([{"player": "abcdefghijklmnop", "game": "snake", "score": 9}]).splitlines()[2]
    assert row[5:19] == "abcdefghijklm…"
    assert row[21:35] == "snake         "
    assert row[37:42] == "    9"


def test_a_long_game_name_is_truncated_without_shifting_the_score_column():
    row = scoreboard.format_scoreboard([{"player": "asha", "game": "abcdefghijklmnop", "score": 12}]).splitlines()[2]
    assert row[21:35] == "abcdefghijklmn"
    assert row[37:42] == "   12"


def test_a_missing_player_name_displays_a_question_mark_in_its_column():
    row = scoreboard.format_scoreboard([{"game": "snake", "score": 4}]).splitlines()[2]
    assert row[5:19] == "?             "
    assert row[37:42] == "    4"


def test_a_missing_score_displays_zero_without_raising_an_error():
    row = scoreboard.format_scoreboard([{"player": "asha", "game": "snake"}]).splitlines()[2]
    assert row[37:42] == "    0"


def test_multiple_entries_keep_their_input_order_and_receive_sequential_ranks():
    rows = scoreboard.format_scoreboard([
        {"player": "first", "score": 2}, {"player": "second", "score": 99}, {"player": "third", "score": 7},
    ]).splitlines()[2:]
    assert [row[2:3] for row in rows] == ["1", "2", "3"]
    assert [row[5:19].strip() for row in rows] == ["first", "second", "third"]


def test_a_nonempty_scoreboard_starts_with_the_header_and_separator_rows():
    lines = scoreboard.format_scoreboard([{}]).splitlines()
    assert lines[0] == "  #  Player          Game            Score  Date"
    assert lines[1] == "  -  --------------  --------------  -----  ----------------"


def test_stats_for_with_no_scores_returns_empty_summary(tmp_path):
    stats = scoreboard.stats_for("guess", path=tmp_path / "empty.json")
    assert stats["games_played"] == 0
    assert stats["best_score"] is None
    assert stats["average_score"] is None
    assert stats["last_played"] is None


def test_stats_for_with_exactly_one_score(tmp_path):
    path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "asha", 80, path=path)
    stats = scoreboard.stats_for("guess", path=path)
    assert stats["games_played"] == 1
    assert stats["best_score"] == 80
    assert stats["average_score"] == 80
    assert stats["last_played"] is not None


def test_stats_for_with_several_scores_calculates_sensible_average(tmp_path):
    path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "a", 10, path=path)
    scoreboard.save_score("guess", "b", 20, path=path)
    scoreboard.save_score("guess", "c", 25, path=path)
    stats = scoreboard.stats_for("guess", path=path)
    assert stats["games_played"] == 3
    assert stats["best_score"] == 25
    assert stats["average_score"] == 18.3
    assert stats["last_played"] is not None


def test_stats_for_filters_by_specific_game(tmp_path):
    path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "a", 10, path=path)
    scoreboard.save_score("hangman", "b", 90, path=path)
    stats = scoreboard.stats_for("hangman", path=path)
    assert stats["games_played"] == 1
    assert stats["best_score"] == 90
    assert stats["average_score"] == 90


def test_scoreboard_drops_date_when_narrow():
    entry = [{"player": "alex", "game": "coinflip", "score": 100, "date": "2026-11-28 03:00"}]
    # Wide terminal: includes date
    wide = scoreboard.format_scoreboard(entry, width=80)
    assert "Date" in wide
    assert "2026-11-28 03:00" in wide

    # Narrow terminal: drops date
    narrow = scoreboard.format_scoreboard(entry, width=45)
    assert "Date" not in narrow
    assert "2026-11-28 03:00" not in narrow
    assert "Score" in narrow
    assert "alex" in narrow


