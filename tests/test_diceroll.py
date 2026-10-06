"""Dice Roll scoring and bounded player input."""

import pytest

from arcade.games import diceroll


@pytest.mark.parametrize("target,total,expected", [
    (2, 2, 100), (12, 12, 100), (7, 7, 100),
    (7, 6, 40), (7, 8, 40), (2, 3, 40), (12, 11, 40),
    (7, 5, 0), (7, 9, 0), (2, 12, 0),
])
def test_score_for(target, total, expected):
    assert diceroll.score_for(target, total) == expected


@pytest.mark.parametrize("target,expected", [(7, 100), (6, 40), (2, 0)])
def test_play_shows_both_dice_and_total(monkeypatch, capsys, target, expected):
    dice = iter([3, 4])
    def roll(low, high):
        assert (low, high) == (1, 6)
        return next(dice)
    monkeypatch.setattr(diceroll.random, "randint", roll)
    monkeypatch.setattr("builtins.input", lambda _: str(target))
    assert diceroll.play() == expected
    assert "Dice: 3 and 4. Total: 7." in capsys.readouterr().out


def test_invalid_targets_are_retried(monkeypatch, capsys):
    answers = iter(["one", "1", "13", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(diceroll.random, "randint", lambda _low, _high: 1)
    assert diceroll.play() == 100
    output = capsys.readouterr().out
    assert "not a whole number" in output
    assert "smallest allowed is 2" in output
    assert "largest allowed is 12" in output
