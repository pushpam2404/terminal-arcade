"""Tests for the Scramble."""

from arcade.games import scramble


def test_is_solved_correct_guess():
    assert scramble.is_solved("apple", "apple")

def test_is_solved_incorrect_guess():
    assert not scramble.is_solved("apple", "paple")

def test_first_guess_scores_the_most():
    assert scramble.total_score(0) > scramble.total_score(2)

def test_shuffle_word_preserves_letters():
    word = "apple"
    shuffled_word = scramble.shuffle_word(word) 
    assert sorted(word) == sorted(shuffled_word)
    assert word != shuffled_word


def test_wrong_guess_feedback_is_coloured_red(monkeypatch, fake_input, capsys):
    # pytest captures output, so stdout is never a tty. Force colours on to
    # check the message is wrapped rather than printed raw.
    monkeypatch.setattr(scramble.art, "colours_supported", lambda: True)
    monkeypatch.setattr(scramble.random, "choice", lambda _: "python")
    fake_input(["zzz", "zzz", "zzz"])

    scramble.play()

    assert f"{scramble.art.RED} Wrong Guess {scramble.art.RESET}" in capsys.readouterr().out


def test_wrong_guess_feedback_stays_plain_without_colour(
    monkeypatch, fake_input, capsys, no_colour
):
    # A wrong guess is a loss, so it goes through art.red() and still comes out
    # plain when colours are off. Raw escape codes would leak NO_COLOR.
    monkeypatch.setattr(scramble.random, "choice", lambda _: "python")
    fake_input(["zzz", "zzz", "zzz"])

    scramble.play()

    captured = capsys.readouterr().out
    assert " Wrong Guess " in captured
    assert scramble.art.RED not in captured
