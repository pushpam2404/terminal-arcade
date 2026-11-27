"""Tests for Rock Paper Scissors Lizard Spock."""

from unittest.mock import patch

import pytest

from arcade.games import rpsls

WINNING_MATCHUPS = [
    ("scissors", "paper", "cuts"),
    ("paper", "rock", "covers"),
    ("rock", "lizard", "crushes"),
    ("lizard", "spock", "poisons"),
    ("spock", "scissors", "smashes"),
    ("scissors", "lizard", "decapitates"),
    ("lizard", "paper", "eats"),
    ("paper", "spock", "disproves"),
    ("spock", "rock", "vaporizes"),
    ("rock", "scissors", "crushes"),
]


@pytest.mark.parametrize("player,computer,verb", WINNING_MATCHUPS)
def test_player_wins_the_expected_matchups(player, computer, verb):
    assert rpsls.decide(player, computer) == "player"
    assert rpsls.reason(player, computer) == f"{player} {verb} {computer}"


@pytest.mark.parametrize("player,computer,_verb", WINNING_MATCHUPS)
def test_computer_wins_the_expected_matchups(player, computer, _verb):
    assert rpsls.decide(computer, player) == "computer"


@pytest.mark.parametrize("move", rpsls.MOVES)
def test_the_same_move_is_always_a_draw(move):
    assert rpsls.decide(move, move) == "draw"


def test_every_move_beats_exactly_two_other_moves():
    for move in rpsls.MOVES:
        losers = [other for other in rpsls.MOVES if rpsls.decide(move, other) == "player"]
        assert len(losers) == 2


def test_every_move_is_beaten_by_exactly_two_other_moves():
    for move in rpsls.MOVES:
        winners = [other for other in rpsls.MOVES if rpsls.decide(other, move) == "player"]
        assert len(winners) == 2


@pytest.mark.parametrize(
    "player,computer,expected",
    [
        ("Lizard", "Spock", "player"),
        ("spock", "LIZARD", "computer"),
        ("rOcK", "Scissors", "player"),
        ("PAPER", "Paper", "draw"),
    ],
)
def test_matching_ignores_capital_letters(player, computer, expected):
    assert rpsls.decide(player, computer) == expected


def test_game_attributes():
    assert hasattr(rpsls, "NAME")
    assert hasattr(rpsls, "DESCRIPTION")
    assert callable(rpsls.play)
    assert len(rpsls.MOVES) == 5


def test_play_simulation_player_wins():
    with (
        patch("arcade.games.rpsls.ask_choice", return_value="rock"),
        patch("random.choice", return_value="scissors"),
    ):
        score = rpsls.play()
        assert score == 100


def test_play_simulation_computer_wins():
    with (
        patch("arcade.games.rpsls.ask_choice", return_value="rock"),
        patch("random.choice", return_value="paper"),
    ):
        score = rpsls.play()
        assert score == 0
