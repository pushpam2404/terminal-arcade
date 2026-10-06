"""Tests for the Magic 8-Ball game."""

from arcade.games import eightball


def test_get_answer_returns_a_valid_answer():
    assert eightball.get_answer() in eightball.ANSWERS


def test_answers_are_not_empty():
    assert eightball.ANSWERS


def test_game_has_name_and_description():
    assert eightball.NAME
    assert eightball.DESCRIPTION