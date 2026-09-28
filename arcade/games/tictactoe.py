"""Tic Tac Toe.

You are X, the computer is O. Squares are numbered 1-9 like a phone keypad:

    1 | 2 | 3
    --+---+--
    4 | 5 | 6
    --+---+--
    7 | 8 | 9
"""

from __future__ import annotations

import random

from arcade import art
from arcade.input_utils import ask_int

NAME = "Tic Tac Toe"
DESCRIPTION = "The classic, against a computer that plays at random"

EMPTY = " "
PLAYER = "X"
COMPUTER = "O"

WINNING_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),  # rows
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),  # columns
    (0, 4, 8),
    (2, 4, 6),  # diagonals
]


def new_board() -> list[str]:
    """Create a fresh board with nine unoccupied squares.

    Returns:
        A new list containing EMPTY in every position, indexed from 0 to 8.
    """
    return [EMPTY] * 9


def render(board: list[str]) -> str:
    """Draw the board as text.

    Empty squares show their number, so the player can see what to type.

    Args:
        board: Nine squares, each "X", "O", or a space.

    Returns:
        A multi-line string ready to print.
    """
    cells = [board[i] if board[i] != EMPTY else str(i + 1) for i in range(9)]
    return (
        f"\n     {cells[0]} | {cells[1]} | {cells[2]}\n"
        f"    ---+---+---\n"
        f"     {cells[3]} | {cells[4]} | {cells[5]}\n"
        f"    ---+---+---\n"
        f"     {cells[6]} | {cells[7]} | {cells[8]}\n"
    )


def winner(board: list[str]) -> str | None:
    """Return the mark that has won, or None if nobody has yet.

    Args:
        board: The current board.

    Returns:
        "X", "O", or None.
    """
    for a, b, c in WINNING_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def free_squares(board: list[str]) -> list[int]:
    """Find the unoccupied positions without changing the board.

    Args:
        board: Nine squares containing PLAYER, COMPUTER, or EMPTY.

    Returns:
        Zero-based indexes of empty squares, in ascending order.
    """
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def is_full(board: list[str]) -> bool:
    """Check whether all squares are occupied, regardless of who has won.

    Args:
        board: Nine squares containing PLAYER, COMPUTER, or EMPTY.

    Returns:
        True if EMPTY does not appear on the board, otherwise False.
    """
    return EMPTY not in board


def outcome_message(result: str | None) -> str:
    """Return the user-facing message for a completed game."""
    if result == PLAYER:
        return "  You win!\n"
    if result == COMPUTER:
        return "  Computer wins!\n"
    return "  It's a draw!\n"


def computer_move(board: list[str]) -> int:
    """Choose a square for the computer.

    Currently picks at random from the free squares. There is an open issue to
    make this cleverer if you fancy it.

    Args:
        board: The current board.

    Returns:
        The index of the square to play.
    """
    return random.choice(free_squares(board))


def play() -> int:
    """Run one game of Tic Tac Toe.

    Returns:
        100 points for a win, 0 otherwise.
    """
    print(art.banner("TIC TAC TOE"))
    print(f"\n  You are {PLAYER}. The computer is {COMPUTER}.")

    board = new_board()
    result = None

    while result is None and not is_full(board):
        print(render(board))

        while True:
            choice = ask_int("  Your move (1-9):", minimum=1, maximum=9)
            if board[choice - 1] == EMPTY:
                board[choice - 1] = PLAYER
                break
            print(art.red("  That square is taken. Pick another."))

        result = winner(board)
        if result is not None or is_full(board):
            break

        move = computer_move(board)
        board[move] = COMPUTER
        print(art.dim(f"\n  Computer plays square {move + 1}."))
        result = winner(board)

    print(render(board))

    if result == PLAYER:
        print(art.green(outcome_message(result)))
        return 100
    elif result == COMPUTER:
        print(art.red(outcome_message(result)))
        return 0
    else:
        print(art.yellow(outcome_message(result)))
        return 0
