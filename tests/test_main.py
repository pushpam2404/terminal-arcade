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


def test_ctrl_d_at_menu_exits_cleanly():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "arcade"],
        input="",
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Goodbye!" in result.stderr
    assert "Traceback" not in result.stderr


def test_keyboard_interrupt_outer_safety_net_exits_130(monkeypatch, capsys):
    import runpy

    import pytest

    def fake_main():
        raise KeyboardInterrupt()

    monkeypatch.setattr("arcade.main.main", fake_main)
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("arcade.__main__", run_name="__main__")
    assert exc_info.value.code == 130
    assert "Goodbye!" in capsys.readouterr().err


def test_eof_error_outer_safety_net_exits_0(monkeypatch, capsys):
    import runpy

    import pytest

    def fake_main():
        raise EOFError()

    monkeypatch.setattr("arcade.main.main", fake_main)
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("arcade.__main__", run_name="__main__")
    assert exc_info.value.code == 0
    assert "Goodbye!" in capsys.readouterr().err


def test_the_menu_offers_surprise_me(capsys):
    main.show_menu()
    output = capsys.readouterr().out
    assert "Surprise me" in output


def test_surprise_me_plays_a_random_game(monkeypatch, capsys):
    game = main.GAMES[0]

    monkeypatch.setattr(main.random, "choice", lambda games: game)
    monkeypatch.setattr(
        main,
        "run_game",
        lambda selected_game: print(f"Playing {selected_game.NAME}"),
    )
    monkeypatch.setattr(main, "pause", lambda: None)

    keys = iter(["s", "q"])
    monkeypatch.setattr(main, "read_key", lambda prompt="": next(keys))

    main.main()

    output = capsys.readouterr().out
    assert f"Surprise! You're playing {game.NAME}!" in output
    assert f"Playing {game.NAME}" in output


def test_menu_shows_ctrl_c_hint_dimmed(capsys):
    main.show_menu()
    output = capsys.readouterr().out
    assert "Press Ctrl+C at any time to quit" in output


def test_menu_shows_game_count_when_scores_exist(tmp_path, capsys):
    from arcade import scoreboard

    path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "player1", 10, path=path)
    scoreboard.save_score("hangman", "player2", 20, path=path)

    main.show_menu(scores_path=path)
    output = capsys.readouterr().out
    assert "High scores (2 played)" in output


def test_menu_shows_no_count_when_no_scores_exist(tmp_path, capsys):
    empty_path = tmp_path / "empty_scores.json"
    main.show_menu(scores_path=empty_path)
    output = capsys.readouterr().out
    assert "High scores\n" in output
    assert "played" not in output


def test_menu_fits_in_24_rows(capsys):
    main.show_menu()
    output = capsys.readouterr().out
    lines = output.strip().splitlines()
    assert len(lines) <= 24


def test_the_menu_offers_statistics(capsys):
    main.show_menu()
    output = capsys.readouterr().out
    assert "Statistics" in output


def test_show_statistics_with_no_scores(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr("arcade.main.ask_int", lambda *args, **kwargs: 1)
    main.show_statistics(scores_path=tmp_path / "empty.json")
    out = capsys.readouterr().out
    assert "No games of" in out


def test_show_statistics_with_scores(tmp_path, capsys, monkeypatch):
    from arcade import scoreboard

    path = tmp_path / "scores.json"
    game_name = main.GAMES[0].NAME
    scoreboard.save_score(game_name, "player1", 40, path=path)
    scoreboard.save_score(game_name, "player2", 80, path=path)

    monkeypatch.setattr("arcade.main.ask_int", lambda *args, **kwargs: 1)
    main.show_statistics(scores_path=path)
    out = capsys.readouterr().out
    assert "Games played:   2" in out
    assert "Best score:     80" in out
    assert "Average score:  60" in out

