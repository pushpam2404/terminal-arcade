"""Tests for the arcade menu itself."""

from arcade import main


def test_every_registered_game_has_a_name():
    for game in main.GAMES:
        assert isinstance(game.NAME, str) and game.NAME


def test_every_registered_game_has_a_description():
    for game in main.GAMES:
        assert isinstance(game.DESCRIPTION, str) and game.DESCRIPTION


def test_every_registered_game_is_playable():
    for game in main.GAMES:
        assert callable(game.play)


def test_game_names_are_unique():
    names = [game.NAME for game in main.GAMES]
    assert len(names) == len(set(names))


def test_the_menu_lists_every_game(capsys):
    main.show_menu()
    output = capsys.readouterr().out
    for game in main.GAMES:
        assert game.NAME in output


def test_the_menu_offers_high_scores_and_quit(capsys):
    main.show_menu()
    output = capsys.readouterr().out
    assert "High scores" in output
    assert "Quit" in output


def test_version_flag_outputs_version_and_exits():
    import subprocess
    import sys

    from arcade import __version__

    for flag in ["--version", "-V"]:
        result = subprocess.run(
            [sys.executable, "-m", "arcade", flag],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == f"terminal-arcade {__version__}"

