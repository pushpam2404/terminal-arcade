""" Scramble.

Unscramble the word. A player get three attempts.
"""
import random

from arcade import art
from arcade.games.hangman import WORDS
from arcade.input_utils import ask

NAME = "Scramble"
DESCRIPTION = "Scramble is a classic word game where you unscramble letters to find words."

MAX_TRY = 3

def shuffle_word(word:str ) -> str:    
    """Shuffle the letters of a word until the result differs from the original.

    Args:
        word: The original word.

    Returns:
        The word with its letters shuffled into a different arrangement.
    """
    shuffled_chars = random.sample(word, len(word))
    shuffled_word = ''.join(shuffled_chars)

    while word == shuffled_word:
        shuffled_chars = random.sample(word, len(word))
        shuffled_word = ''.join(shuffled_chars)

    return shuffled_word

def is_solved(word, guess):
    """Check whether the player's guess matches the original word.

    Args:
        word: The original word.
        guess: The word entered by the player.

    Returns:
        True if the guess matches the word, otherwise False.
    """
    return True if word == guess else False

def total_score(attempt):
    """Calculate the score based on the attempt used to guess the word.

    Args:
        attempt: The zero-based index of the attempt on which the player succeeds.

    Returns:
        The points earned for solving the word on that attempt.
    """
    return ((MAX_TRY - attempt) * 20)

def play() -> int:
    """Run a round of Scramble.

    The player gets three attempts to guess the original word.

    Returns:
        The points earned for a correct guess, or zero if all attempts fail.
    """

    print(art.banner("SCRAMBLE"))

    word = random.choice(WORDS)
    shuffled_word = shuffle_word(word)

    print(f" Unscramble the word: {shuffled_word}")
    print(f" You have {MAX_TRY} attempts.\n")

    for attempt in range(MAX_TRY):

        guess = ask(f" Attempt {attempt + 1}/3: Guess the word: ")

        result = is_solved(word, guess)

        if result:
            points = total_score(attempt)
            print(art.green(f"\n  You found the right word. It was {word}"))
            print(f"  You scored {points} points.\n")
            return points
        else:
            # A wrong guess is a loss, so it reads red like every other game's
            # failure message. Going through art.red also means NO_COLOR and
            # piped output stay plain, which a bare print() cannot do.
            print(art.red(" Wrong Guess "))

    print(art.red(f"\n Out of attempts. The word was {word}.\n"))
    return 0
