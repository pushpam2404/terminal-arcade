"""Tests for the Guess the Number game."""

from unittest.mock import patch

import pytest

from arcade.games import guess


def test_evaluate_detects_correct_guess():
    assert guess.evaluate(42, 42) == "correct"


def test_evaluate_detects_too_low():
    assert guess.evaluate(10, 50) == "too low"


def test_evaluate_detects_too_high():
    assert guess.evaluate(90, 50) == "too high"


def test_first_guess_scores_the_most():
    assert guess.score_for(1) > guess.score_for(2)


def test_score_is_never_negative():
    assert guess.score_for(guess.MAX_GUESSES * 10) == 0


def test_difficulty_configurations():
    easy = guess.DIFFICULTIES["easy"]
    assert (easy["lowest"], easy["highest"], easy["max_guesses"]) == (1, 50, 8)

    normal = guess.DIFFICULTIES["normal"]
    assert (normal["lowest"], normal["highest"], normal["max_guesses"]) == (1, 100, 7)

    hard = guess.DIFFICULTIES["hard"]
    assert (hard["lowest"], hard["highest"], hard["max_guesses"]) == (1, 500, 9)


@pytest.mark.parametrize("attempt", [1, 2, 3, 4, 5, 6, 7])
def test_hard_scores_higher_than_easy_for_same_guesses(attempt):
    easy_cfg = guess.DIFFICULTIES["easy"]
    hard_cfg = guess.DIFFICULTIES["hard"]

    easy_score = guess.score_for(
        attempt,
        max_guesses=easy_cfg["max_guesses"],
        multiplier=easy_cfg["multiplier"],
    )
    hard_score = guess.score_for(
        attempt,
        max_guesses=hard_cfg["max_guesses"],
        multiplier=hard_cfg["multiplier"],
    )
    assert hard_score > easy_score


def test_score_for_each_difficulty():
    # Easy: (8 - 1 + 1) * 5 = 40
    assert guess.score_for(1, max_guesses=8, multiplier=5) == 40
    # Normal: (7 - 1 + 1) * 10 = 70
    assert guess.score_for(1, max_guesses=7, multiplier=10) == 70
    # Hard: (9 - 1 + 1) * 20 = 180
    assert guess.score_for(1, max_guesses=9, multiplier=20) == 180


def test_score_for_independent_of_globals():
    # Verify score_for does not rely on module-level MAX_GUESSES when parameters are passed
    custom_score = guess.score_for(guesses_used=2, max_guesses=20, multiplier=3)
    assert custom_score == (20 - 2 + 1) * 3


def test_play_simulation_with_difficulty():
    with patch("arcade.games.guess.ask_choice", return_value="easy"), \
         patch("random.randint", return_value=25), \
         patch("arcade.games.guess.ask_int", return_value=25):
        score = guess.play()
        assert score == (8 - 1 + 1) * 5
        assert guess.NAME == "Guess (Easy)"
