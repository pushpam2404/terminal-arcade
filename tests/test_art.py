"""Tests for the art helpers."""

from arcade import art


def test_banner_draws_a_box_around_the_text():
    output = art.banner("HELLO")
    lines = output.splitlines()
    assert len(lines) == 3
    assert "HELLO" in lines[1]
    assert lines[0] == lines[2]


def test_banner_box_lines_are_all_the_same_width():
    lines = art.banner("TIC TAC TOE").splitlines()
    assert len({len(line) for line in lines}) == 1


def test_rule_has_the_requested_width():
    assert len(art.rule(width=20)) == 20


def test_colour_is_skipped_when_no_color_is_set(no_colour):
    assert art.green("plain") == "plain"


def test_there_are_seven_gallows_stages():
    assert len(art.GALLOWS) == 7


def test_terminal_width_defaults_and_env(monkeypatch):
    monkeypatch.setenv("COLUMNS", "120")
    assert art.terminal_width() == 120

    monkeypatch.delenv("COLUMNS", raising=False)
    w = art.terminal_width()
    assert isinstance(w, int)
    assert w >= 1


def test_rule_defaults_to_terminal_width(monkeypatch):
    monkeypatch.setenv("COLUMNS", "64")
    assert len(art.rule()) == 64
    assert len(art.rule("=", width=15)) == 15


def test_fit_centers_art_when_room():
    text = "###\n###"
    fitted = art.fit(text, width=20)
    for line in fitted.strip("\r\n").splitlines():
        assert line.startswith("        ###")  # (20 - 3) // 2 = 8 spaces padding


def test_fit_falls_back_to_title_when_narrow():
    wide_art = "A" * 50
    fitted = art.fit(wide_art, width=25, fallback_title="Short Title")
    assert "Short Title" in fitted
    assert wide_art not in fitted


def test_fit_never_crashes_on_extreme_widths():
    for w in [1, 2, 5, 10, 80, 200]:
        res = art.fit(art.ARCADE_BANNER, width=w, fallback_title="Arcade")
        assert isinstance(res, str)
        assert len(res) > 0


def test_color_shortcuts_format_ansi_codes(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)

    assert art.blue("test") == f"{art.BLUE}test{art.RESET}"
    assert art.magenta("test") == f"{art.MAGENTA}test{art.RESET}"
    assert art.white("test") == f"{art.WHITE}test{art.RESET}"


def test_all_game_banners_are_under_60_characters_wide():
    banners = [
        art.ARCADE_BANNER,
        art.GUESS_BANNER,
        art.HANGMAN_BANNER,
        art.RPS_BANNER,
        art.TICTACTOE_BANNER,
        art.COINFLIP_BANNER,
        art.DICEROLL_BANNER,
        art.EIGHTBALL_BANNER,
        art.SCRAMBLE_BANNER,
        art.RPSLS_BANNER,
    ]
    for b in banners:
        assert isinstance(b, str)
        assert len(b.strip()) > 0
        for line in b.splitlines():
            assert len(line) <= 60, f"Banner line too wide ({len(line)} > 60): {line}"



