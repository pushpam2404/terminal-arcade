"""ASCII banners and terminal colours.

No external libraries. Colours are plain ANSI escape codes, which every modern
terminal understands (including Windows Terminal and PowerShell).

If you are adding a banner for a new game, keep it under 60 characters wide so
it does not wrap on a small terminal.
"""

from __future__ import annotations

import os
import shutil
import sys

# --- Colours -----------------------------------------------------------------

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"


def colours_supported() -> bool:
    """Return True if we should emit colour codes.

    Respects the NO_COLOR convention (https://no-color.org) and turns colour
    off when output is being piped to a file.

    Returns:
        True when stdout is a terminal and NO_COLOR is unset or empty.
    """
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


def colour(text: str, code: str) -> str:
    """Wrap text in an ANSI style when terminal colours are enabled.

    Args:
        text: The text to style.
        code: An ANSI colour or style escape sequence.

    Returns:
        Styled text followed by a reset code, or unchanged text when disabled.
    """
    if not colours_supported():
        return text
    return f"{code}{text}{RESET}"


def red(text: str) -> str:
    """Apply the red terminal style when colours are enabled.

    Args:
        text: The text to style.

    Returns:
        Text with the red style and a reset, or unchanged text when disabled.
    """
    return colour(text, RED)


def green(text: str) -> str:
    """Apply the green terminal style when colours are enabled.

    Args:
        text: The text to style.

    Returns:
        Text with the green style and a reset, or unchanged text when disabled.
    """
    return colour(text, GREEN)


def yellow(text: str) -> str:
    """Apply the yellow terminal style when colours are enabled.

    Args:
        text: The text to style.

    Returns:
        Text with the yellow style and a reset, or unchanged text when disabled.
    """
    return colour(text, YELLOW)


def cyan(text: str) -> str:
    """Apply the cyan terminal style when colours are enabled.

    Args:
        text: The text to style.

    Returns:
        Text with the cyan style and a reset, or unchanged text when disabled.
    """
    return colour(text, CYAN)


def bold(text: str) -> str:
    """Apply the bold terminal style when colours are enabled.

    Args:
        text: The text to style.

    Returns:
        Text with the bold style and a reset, or unchanged text when disabled.
    """
    return colour(text, BOLD)


def dim(text: str) -> str:
    """Apply the dim terminal style when colours are enabled.

    Args:
        text: The text to style.

    Returns:
        Text with the dim style and a reset, or unchanged text when disabled.
    """
    return colour(text, DIM)


# --- Banners -----------------------------------------------------------------

ARCADE_BANNER = r"""
  _____                  _             _
 |_   _|__ _ _ _ __  ___(_)_ _  __ _ | |
   | |/ -_) '_| '  \/ -_) | ' \/ _` || |
   |_|\___|_| |_|_|_\___|_|_||_\__,_||_|
         _   ___  ___   _   ___  ___
        /_\ | _ \/ __| /_\ |   \| __|
       / _ \|   / (__ / _ \| |) | _|
      /_/ \_\_|_\\___/_/ \_\___/|___|
"""

GUESS_BANNER = r"""
   ___                   _   _
  / __|_  _ ___ ______  | |_| |_  ___
 | (_ | || / -_|_-<_-<  |  _| ' \/ -_)
  \___|\_,_\___/__/__/   \__|_||_\___|
        _  _             _
       | \| |_  _ _ __ | |__  ___ _ _
       | .` | || | '  \| '_ \/ -_) '_|
       |_|\_|\_,_|_|_|_|_.__/\___|_|
"""

HANGMAN_BANNER = r"""
  _  _                                 
 | || |__ _ _ _  __ _ _ __  __ _ _ _   
 | __ / _` | ' \/ _` | '  \/ _` | ' \  
 |_||_\__,_|_||_\__, |_|_|_\__,_|_||_| 
                |___/                  
"""

RPS_BANNER = r"""
  ___         _     ___                  
 | _ \___  __| |__ | _ \__ _ _ __  ___ _ _ 
 |   / _ \/ _| / / |  _/ _` | '_ \/ -_) '_|
 |_|_\___/\__|_\_\ |_| \__,_| .__/\___|_|  
     ___     _              |_|            
    / __| __(_)_______ ___ _ _ ___         
    \__ \/ _| |_ / _ (_-< _ \ '_(_-<       
    |___/\__|_/__\___/__/___/_| /__/       
"""



TICTACTOE_BANNER = r"""
 _____ _ ____   _____  _   ____    _____ ___  _____
|_   _|_ |__  | |_   _|/ \ |  _ \  |_   _/ _ \| ____|
  | | | |  / /    | | / _ \| |_) |   | || | | |  _|
  | | | | / /     | |/ ___ \  __/   | || |_| | |___
  |_| |___/____|  |_/_/   \_\_|      |_| \___/|_____|
"""



GALLOWS = [
    # 0 wrong guesses through 6 (lost)
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========""",
]


def banner(text: str) -> str:
    """Put a single line of text inside a three-line ASCII box.

    Args:
        text: The banner title, without newline characters.

    Returns:
        A box with one space on each side of the title and no trailing newline.
    """
    width = len(text) + 4
    top = "+" + "-" * (width - 2) + "+"
    middle = f"| {text} |"
    return f"{top}\n{middle}\n{top}"


def terminal_width(default: int = 80) -> int:
    """Return the terminal width in columns, with a safe fallback.

    Args:
        default: Fallback width if terminal size cannot be detected. Defaults to 80.

    Returns:
        The number of terminal columns (at least 1).
    """
    try:
        env_cols = os.environ.get("COLUMNS")
        if env_cols:
            try:
                c = int(env_cols)
                if c > 0:
                    return c
            except ValueError:
                pass
        cols = shutil.get_terminal_size(fallback=(default, 24)).columns
        return max(1, cols)
    except Exception:
        return max(1, default)


def fit(text: str, width: int | None = None, fallback_title: str | None = None) -> str:
    """Format and layout art or text to fit the terminal width.

    Centres each line of the ASCII art if it fits within `width`.
    If the art's maximum line width exceeds `width`, falls back to a plain text title
    that fits comfortably within the narrow terminal without line-wrapping noise.

    Args:
        text: Multi-line ASCII art or string.
        width: Available columns. Defaults to terminal_width().
        fallback_title: Plain text title to display if art does not fit.

    Returns:
        Formatted string fitted to width. Never crashes for any width >= 1.
    """
    if width is None:
        width = terminal_width()
    width = max(1, width)

    raw_lines = text.strip("\r\n").split("\n")
    max_line_len = max((len(line.rstrip("\r")) for line in raw_lines), default=0)

    if max_line_len <= width:
        centered_lines: list[str] = []
        for line in raw_lines:
            stripped = line.rstrip("\r")
            if not stripped.strip():
                centered_lines.append("")
            else:
                pad = max(0, (width - len(stripped)) // 2)
                centered_lines.append(" " * pad + stripped)
        return "\n" + "\n".join(centered_lines) + "\n"

    title = fallback_title or "Terminal Arcade"
    if width < 6:
        return title[:width]

    divider = rule("=", min(width, max(len(title) + 4, 10)))
    pad = max(0, (width - len(title)) // 2)
    return f"\n{divider}\n{' ' * pad}{title[:width]}\n{divider}\n"


def rule(char: str = "-", width: int | None = None) -> str:
    """Build a divider by repeating the supplied text up to width.

    Args:
        char: The text to repeat. Defaults to "-".
        width: Number of characters to fill. Defaults to terminal_width().

    Returns:
        The repeated text truncated to width, or empty string if width <= 0.
    """
    if width is None:
        width = terminal_width()
    if width <= 0 or not char:
        return ""
    repeats = (width // len(char)) + 1
    return (char * repeats)[:width]
