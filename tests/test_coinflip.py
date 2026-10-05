"""Coin Flip outcomes, input handling, and early termination."""

import pytest

from arcade.games import coinflip


@pytest.mark.parametrize("side", ["heads", "tails"])
def test_flip_returns_a_coin_side(monkeypatch, side):
    def choose(options):
        assert options == ["heads", "tails"]
        return side
    monkeypatch.setattr(coinflip.random, "choice", choose)
    assert coinflip.flip() == side


def test_three_correct_calls_win(monkeypatch, capsys):
    calls = iter(["HEADS", "tails", "heads"])
    flips = iter(["heads", "tails", "heads"])
    monkeypatch.setattr("builtins.input", lambda _: next(calls))
    monkeypatch.setattr(coinflip, "flip", lambda: next(flips))
    assert coinflip.play() == 90
    assert "3 in a row" in capsys.readouterr().out


@pytest.mark.parametrize("correct_before_loss", [0, 1, 2])
def test_wrong_call_ends_the_game(monkeypatch, capsys, correct_before_loss):
    flips = iter(["heads"] * correct_before_loss + ["tails"])
    monkeypatch.setattr("builtins.input", lambda _: "heads")
    monkeypatch.setattr(coinflip, "flip", lambda: next(flips))
    assert coinflip.play() == 0
    assert f"You got {correct_before_loss} in a row" in capsys.readouterr().out


def test_invalid_call_is_retried(monkeypatch):
    calls = iter(["edge", "heads"])
    monkeypatch.setattr("builtins.input", lambda _: next(calls))
    monkeypatch.setattr(coinflip, "flip", lambda: "tails")
    assert coinflip.play() == 0
