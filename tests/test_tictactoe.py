"""Tests for Tic Tac Toe."""

from arcade.games import tictactoe as ttt


def test_a_new_board_is_empty():
    assert ttt.new_board() == [ttt.EMPTY] * 9


def test_detects_a_winning_row():
    board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
    assert ttt.winner(board) == "X"


def test_detects_a_winning_column():
    board = ["O", " ", " ", "O", " ", " ", "O", " ", " "]
    assert ttt.winner(board) == "O"


def test_detects_a_winning_diagonal():
    board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
    assert ttt.winner(board) == "X"


def test_no_winner_on_an_empty_board():
    assert ttt.winner(ttt.new_board()) is None


def test_three_empty_squares_in_a_line_do_not_count_as_a_win():
    assert ttt.winner([" "] * 9) is None


def test_free_squares_lists_only_empty_ones():
    board = ["X", " ", "O", " ", " ", " ", " ", " ", " "]
    assert ttt.free_squares(board) == [1, 3, 4, 5, 6, 7, 8]


def test_is_full_is_false_with_a_gap():
    assert ttt.is_full(["X"] * 8 + [" "]) is False


def test_is_full_is_true_with_no_gaps():
    assert ttt.is_full(["X", "O"] * 4 + ["X"]) is True


def test_the_computer_only_plays_free_squares():
    board = ["X", "O", "X", "O", " ", "O", "X", "O", "X"]
    assert ttt.computer_move(board) == 4


def test_render_shows_numbers_for_empty_squares():
    output = ttt.render(ttt.new_board())
    for number in range(1, 10):
        assert str(number) in output


def test_outcome_messages_are_formatted(capsys):
    from unittest.mock import patch

    # Player wins
    with patch("arcade.games.tictactoe.ask_int", side_effect=[1, 2, 3]):
        with patch("arcade.games.tictactoe.computer_move", side_effect=[3, 4]):
            board = ["X", "X", " ", " ", " ", " ", " ", " ", " "]
            with patch("arcade.games.tictactoe.new_board", return_value=board):
                score = ttt.play()
                assert score == 100
                out = capsys.readouterr().out
                assert "You win!" in out


def test_play_announces_a_draw_for_a_full_board(capsys):
    from unittest.mock import patch

    board = ["X", "O", "X", "X", "O", "O", "O", "X", " "]
    with patch("arcade.games.tictactoe.new_board", return_value=board):
        with patch("arcade.games.tictactoe.ask_int", return_value=9):
            score = ttt.play()

    assert score == 0
    output = capsys.readouterr().out
    assert "It's a draw!" in output
    assert "None" not in output


def test_outcome_message_for_a_draw_does_not_expose_none():
    assert ttt.outcome_message(None) == "  It's a draw!\n"


def test_outcome_message_identifies_the_winner():
    assert ttt.outcome_message(ttt.PLAYER) == "  You win!\n"
    assert ttt.outcome_message(ttt.COMPUTER) == "  Computer wins!\n"


def test_find_completing_square_finds_row_win():
    board = ["O", "O", " ", " ", " ", " ", " ", " ", " "]
    assert ttt.find_completing_square(board, ttt.COMPUTER) == 2


def test_find_completing_square_returns_none_when_no_completing_move():
    board = ["O", " ", " ", " ", " ", " ", " ", " ", " "]
    assert ttt.find_completing_square(board, ttt.COMPUTER) is None


def test_computer_takes_immediate_win():
    board = ["O", "O", " ", "X", "X", " ", " ", " ", " "]
    assert ttt.computer_move(board) == 2


def test_computer_blocks_player_immediate_win():
    board = ["X", "X", " ", "O", " ", " ", " ", " ", " "]
    assert ttt.computer_move(board) == 2


def test_computer_prefers_winning_over_blocking():
    board = [
        "X", "X", " ",
        " ", " ", " ",
        "O", "O", " ",
    ]
    assert ttt.computer_move(board) == 8


def test_computer_prefers_centre_when_no_win_or_block():
    board = [
        "X", " ", " ",
        " ", " ", " ",
        " ", " ", " ",
    ]
    assert ttt.computer_move(board) == 4


def test_computer_prefers_corners_when_centre_is_occupied():
    board = [
        " ", " ", " ",
        " ", "X", " ",
        " ", " ", " ",
    ]
    move = ttt.computer_move(board)
    assert move in (0, 2, 6, 8)


def test_computer_never_picks_an_occupied_square():
    board = [
        "X", "O", "X",
        "O", "X", "O",
        "O", "X", " ",
    ]
    assert ttt.computer_move(board) == 8

