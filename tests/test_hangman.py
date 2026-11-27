"""Tests for the Hangman game."""

from arcade import art
from arcade.games import hangman


def test_mask_hides_unguessed_letters():
    assert hangman.mask_word("python", set()) == "_ _ _ _ _ _"


def test_mask_reveals_guessed_letters():
    assert hangman.mask_word("python", {"p", "n"}) == "p _ _ _ _ n"


def test_mask_reveals_every_occurrence_of_a_letter():
    # Both 'o's should appear, not just the first.
    assert hangman.mask_word("moon", {"o"}) == "_ o o _"


def test_is_solved_is_false_when_letters_remain():
    assert hangman.is_solved("python", {"p", "y"}) is False


def test_is_solved_is_true_when_all_letters_found():
    assert hangman.is_solved("python", set("python")) is True


def test_longer_words_score_more():
    assert hangman.score_for("recursion", 0) > hangman.score_for("debug", 0)


def test_mistakes_reduce_the_score():
    assert hangman.score_for("python", 3) < hangman.score_for("python", 0)


def test_score_for_timed_mode_bonus():
    # 60 base score (6 letters * 10 - 0 wrong) + 25 seconds remaining = 85
    assert hangman.score_for("python", 0, time_remaining=25.4) == 85
    assert hangman.score_for("python", 0, time_remaining=0.0) == 60


def test_every_word_in_the_list_is_lowercase_letters_only():
    # A word with a capital or a hyphen would be impossible to guess,
    # because ask_letter() only accepts single lowercase letters.
    for word in hangman.WORDS:
        assert word.isalpha(), f"{word!r} has a non-letter character"
        assert word.islower(), f"{word!r} is not lowercase"


def test_there_is_a_gallows_drawing_for_every_wrong_guess():
    # One drawing for the empty gallows plus one per wrong guess.
    assert len(art.GALLOWS) == hangman.MAX_WRONG + 1


def test_reguessing_letter_does_not_cost_a_life(fake_input, monkeypatch, capsys, no_colour):
    monkeypatch.setattr(hangman.random, "choice", lambda _: "python")
    fake_input(["relaxed", "z", "z", "p", "y", "t", "h", "o", "n"])
    score = hangman.play()

    captured = capsys.readouterr().out
    assert "You already tried 'z'." in captured
    assert score == 50


def test_reguessing_correct_letter_warns_player(fake_input, monkeypatch, capsys, no_colour):
    monkeypatch.setattr(hangman.random, "choice", lambda _: "python")
    fake_input(["relaxed", "p", "p", "y", "t", "h", "o", "n"])
    score = hangman.play()

    captured = capsys.readouterr().out
    assert "You already tried 'p'." in captured
    assert score == 60


def test_six_distinct_wrong_letters_still_loses_with_repeats(
    fake_input, monkeypatch, capsys, no_colour
):
    monkeypatch.setattr(hangman.random, "choice", lambda _: "python")
    fake_input(["relaxed", "z", "z", "a", "b", "c", "d", "e"])
    score = hangman.play()

    captured = capsys.readouterr().out
    assert "Out of guesses. The word was 'python'." in captured
    assert score == 0


def test_timed_mode_win_awards_time_bonus(fake_input, monkeypatch, capsys, no_colour):
    monkeypatch.setattr(hangman.random, "choice", lambda _: "python")

    # Fake clock: start at 100.0, each call advances by 2.0s
    clock_state = {"time": 100.0}

    def fake_monotonic():
        val = clock_state["time"]
        clock_state["time"] += 2.0
        return val

    monkeypatch.setattr(hangman.time, "monotonic", fake_monotonic)
    fake_input(["timed", "p", "y", "t", "h", "o", "n"])
    score = hangman.play()

    captured = capsys.readouterr().out
    assert "Time left:" in captured
    assert "time bonus" in captured
    assert score > 60  # includes time bonus


def test_timed_mode_running_out_of_time_loses(fake_input, monkeypatch, capsys, no_colour):
    monkeypatch.setattr(hangman.random, "choice", lambda _: "python")

    # Fake clock: first call is 0.0, next call jumps to 70.0 (> TIME_LIMIT)
    calls = [0.0, 70.0, 75.0, 80.0]

    def fake_monotonic():
        if calls:
            return calls.pop(0)
        return 100.0

    monkeypatch.setattr(hangman.time, "monotonic", fake_monotonic)
    fake_input(["timed", "p"])
    score = hangman.play()

    captured = capsys.readouterr().out
    assert "Time's up! The word was 'python'." in captured
    assert score == 0
