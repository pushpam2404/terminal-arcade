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


def test_discover_games_finds_all_standard_games():
    games = main.discover_games()
    names = {g.__name__.rsplit(".", 1)[-1] for g in games}
    expected = {"guess", "hangman", "rps", "rpsls", "tictactoe", "coinflip", "diceroll", "eightball", "scramble"}
    assert expected.issubset(names)


def test_discover_games_skips_underscore_modules(tmp_path, monkeypatch, capsys):
    pkg_dir = tmp_path / "fake_games"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "_internal.py").write_text("NAME = 'Internal'\nDESCRIPTION = 'x'\ndef play(): pass", encoding="utf-8")
    (pkg_dir / "valid.py").write_text("NAME = 'Valid'\nDESCRIPTION = 'desc'\ndef play(): return 0", encoding="utf-8")

    import sys
    monkeypatch.syspath_prepend(str(tmp_path))
    import importlib
    fake_pkg = importlib.import_module("fake_games")

    games = main.discover_games(package=fake_pkg)
    names = [g.NAME for g in games]
    assert "Valid" in names
    assert "Internal" not in names


def test_discover_games_warns_and_skips_incomplete_module(tmp_path, monkeypatch, capsys):
    pkg_dir = tmp_path / "incomplete_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "bad_game.py").write_text("NAME = 'Bad'\n# missing DESCRIPTION and play", encoding="utf-8")

    monkeypatch.syspath_prepend(str(tmp_path))
    import importlib
    fake_pkg = importlib.import_module("incomplete_pkg")

    games = main.discover_games(package=fake_pkg)
    assert len(games) == 0

    err = capsys.readouterr().err
    assert "missing" in err.lower()
    assert "bad_game" in err


def test_discover_games_warns_and_skips_broken_syntax(tmp_path, monkeypatch, capsys):
    pkg_dir = tmp_path / "broken_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "syntax_error.py").write_text("def broken(: invalid python syntax", encoding="utf-8")

    monkeypatch.syspath_prepend(str(tmp_path))
    import importlib
    fake_pkg = importlib.import_module("broken_pkg")

    games = main.discover_games(package=fake_pkg)
    assert len(games) == 0

    err = capsys.readouterr().err
    assert "syntax_error" in err


def test_discover_games_order_is_deterministic():
    order1 = [g.NAME for g in main.discover_games()]
    order2 = [g.NAME for g in main.discover_games()]
    assert order1 == order2


def test_run_game_remembers_player_and_defaults_on_enter(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from arcade import scoreboard

    scores_path = tmp_path / "scores.json"
    dummy_game = SimpleNamespace(NAME="TestGame", play=lambda: 100)

    # First game: player enters "Asha"
    prompts = []

    def fake_ask_first(prompt):
        prompts.append(prompt)
        return "Asha"

    monkeypatch.setattr("arcade.main.ask", fake_ask_first)
    monkeypatch.setattr("arcade.main.confirm", lambda prompt: prompt.startswith("  Save"))
    monkeypatch.setattr("arcade.main.pause", lambda: None)

    main.run_game(dummy_game, scores_path=scores_path)
    assert scoreboard.get_last_player(scores_path) == "Asha"
    assert "Your name:" in prompts[0]

    # Second game: player presses Enter (empty string)
    prompts.clear()

    def fake_ask_second(prompt):
        prompts.append(prompt)
        return ""  # Enter accepted

    monkeypatch.setattr("arcade.main.ask", fake_ask_second)
    main.run_game(dummy_game, scores_path=scores_path)

    scores = scoreboard.load_scores(scores_path)
    assert len(scores) == 2
    assert scores[1]["player"] == "Asha"
    assert "Your name [Asha]:" in prompts[0]


def test_show_high_scores_filters_by_player(tmp_path, capsys, monkeypatch):
    from arcade import scoreboard

    scores_path = tmp_path / "scores.json"
    scoreboard.save_score("guess", "Asha", 50, path=scores_path)
    scoreboard.save_score("hangman", "Bob", 70, path=scores_path)

    # Ask will filter by "Asha"
    monkeypatch.setattr("arcade.main.ask", lambda prompt: "Asha")
    main.show_high_scores(scores_path=scores_path)

    out = capsys.readouterr().out
    assert "HIGH SCORES" in out
    assert "SCORES FOR ASHA" in out



