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
from arcade.input_utils import ask_choice, ask_int

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


def find_completing_square(board: list[str], mark: str) -> int | None:
    """Find a free square that would complete a three-in-a-row for `mark`.

    Args:
        board: The current board.
        mark: PLAYER ("X") or COMPUTER ("O").

    Returns:
        The zero-based index of the completing square, or None if none exists.
    """
    for a, b, c in WINNING_LINES:
        line = [board[a], board[b], board[c]]
        if line.count(mark) == 2 and line.count(EMPTY) == 1:
            for idx in (a, b, c):
                if board[idx] == EMPTY:
                    return idx
    return None


def minimax(
    board: list[str],
    depth: int,
    is_maximizing: bool,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> int:
    """Recursively score every reachable board state to choose the optimal move.

    How minimax works:
    ------------------
    Minimax is a game-theory algorithm for two-player, turn-based games of perfect
    information (like Tic Tac Toe or Chess). One player wants to maximize their score
    (the Computer, 'O'), while the other wants to minimize it (the Player, 'X').

    At any given turn, the computer looks ahead into every legal move available:
    1. Base cases (game over):
       - If Computer ('O') wins: return +10 - depth. Subtracting depth rewards faster
         wins over slower ones.
       - If Player ('X') wins: return depth - 10. Adding depth rewards delaying a loss
         as long as possible.
       - If the board is full (draw): return 0.
    2. Recursive step:
       - On Computer's turn (maximizing): try each free square, call minimax recursively,
         and select the move with the highest score.
       - On Player's turn (minimizing): try each free square, call minimax recursively,
         and select the move with the lowest score.

    Alpha-beta pruning:
    -------------------
    'alpha' tracks the best score the maximizer is already guaranteed, and 'beta' tracks
    the best score the minimizer is guaranteed. If beta <= alpha, the opponent would
    never allow this branch of play to occur, so we prune (skip) the remaining moves in
    this branch.

    Args:
        board: Nine squares representing the current board state.
        depth: Number of moves explored from the starting state.
        is_maximizing: True if it is Computer's turn ('O'), False if Player's ('X').
        alpha: Best score the maximizer can guarantee so far.
        beta: Best score the minimizer can guarantee so far.

    Returns:
        The minimax evaluation score for this board state.
    """
    win = winner(board)
    if win == COMPUTER:
        return 10 - depth
    if win == PLAYER:
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = float("-inf")
        for sq in free_squares(board):
            board[sq] = COMPUTER
            eval_score = minimax(board, depth + 1, False, alpha, beta)
            board[sq] = EMPTY
            if eval_score > max_eval:
                max_eval = eval_score
            if max_eval > alpha:
                alpha = max_eval
            if beta <= alpha:
                break
        return int(max_eval)
    else:
        min_eval = float("inf")
        for sq in free_squares(board):
            board[sq] = PLAYER
            eval_score = minimax(board, depth + 1, True, alpha, beta)
            board[sq] = EMPTY
            if eval_score < min_eval:
                min_eval = eval_score
            if min_eval < beta:
                beta = min_eval
            if beta <= alpha:
                break
        return int(min_eval)


def minimax_move(board: list[str]) -> int:
    """Determine the unbeatable move for the computer using minimax search.

    Args:
        board: The current board.

    Returns:
        The zero-based index of the chosen square.
    """
    best_score = float("-inf")
    best_move = -1

    for sq in free_squares(board):
        board[sq] = COMPUTER
        score = minimax(board, 0, False)
        board[sq] = EMPTY
        if score > best_score:
            best_score = score
            best_move = sq

    return best_move


def computer_move(board: list[str], difficulty: str = "impossible") -> int:
    """Choose a square for the computer based on the selected difficulty.

    - easy: Picks a random unoccupied square.
    - medium: Three-rule heuristic (take win, block player win, center/corners).
    - impossible: Unbeatable minimax search with alpha-beta pruning.

    Args:
        board: The current board.
        difficulty: One of 'easy', 'medium', or 'impossible'.

    Returns:
        The zero-based index of the square to play.
    """
    diff = (difficulty or "impossible").lower()
    if diff == "easy":
        return random.choice(free_squares(board))

    if diff in ("medium", "heuristic"):
        win = find_completing_square(board, COMPUTER)
        if win is not None:
            return win

        block = find_completing_square(board, PLAYER)
        if block is not None:
            return block

        if board[4] == EMPTY:
            return 4

        corners = [i for i in (0, 2, 6, 8) if board[i] == EMPTY]
        if corners:
            return random.choice(corners)

        return random.choice(free_squares(board))

    return minimax_move(board)


def play(difficulty: str | None = None) -> int:
    """Run one game of Tic Tac Toe.

    Args:
        difficulty: Optional difficulty level ('easy', 'medium', or 'impossible').
                    If None, the player is asked to select one.

    Returns:
        100 points for a win, 0 otherwise.
    """
    print(art.TICTACTOE_BANNER)

    if difficulty is None:
        try:
            difficulty = ask_choice(
                "  Select difficulty", ["easy", "medium", "impossible"]
            ).lower()
        except (EOFError, Exception):
            difficulty = "medium"

    print(f"\n  You are {PLAYER}. The computer is {COMPUTER} ({difficulty.capitalize()}).")

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

        move = computer_move(board, difficulty=difficulty)
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
