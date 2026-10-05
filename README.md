<h1 align="center">Terminal Arcade</h1>

<p align="center">A collection of small games you play in your terminal.<br>
Built as a friendly place to make your first ever pull request.</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/dependencies-none-1F883D" alt="No dependencies">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="MIT">
</p>

---

## Play it

You need **Python 3.10 or newer**. Nothing else — no `pip install`, no
dependencies, no setup.

```bash
git clone https://github.com/pushpam2404/terminal-arcade.git
cd terminal-arcade
python3 -m arcade
```

```
  _____                  _             _
 |_   _|__ _ _ _ __  ___(_)_ _  __ _ | |
   | |/ -_) '_| '  \/ -_) | ' \/ _` || |
   |_|\___|_| |_|_|_\___|_|_||_\__,_||_|
         _   ___  ___   _   ___  ___
        /_\ | _ \/ __| /_\ |   \| __|
       / _ \|   / (__ / _ \| |) | _|
      /_/ \_\_|_\\___/_/ \_\___/|___|

  1. Guess the Number
     Find the secret number in as few guesses as you can
  2. Hangman
     Guess the word before the drawing is finished
  3. Rock Paper Scissors
     Best of five against the computer
  4. Tic Tac Toe
     The classic, against a computer that plays at random

  5. High scores
  6. Quit

  What would you like to play?
```

---

## Where to look, and what to ignore

A repository looks like a lot of folders the first time you open one. Almost
none of them are yours to worry about. Here is the honest breakdown.

### 🎯 Your work goes here

| Folder | What is in it |
|---|---|
| **`arcade/games/`** | **One file per game.** Nearly every beginner issue is "add a game" or "fix a game", and it happens in exactly one file in this folder. If you only ever open one directory in this repo, open this one. |
| `arcade/` | The shared bits every game uses — the menu (`main.py`), the ASCII art (`art.py`), asking the player questions (`input_utils.py`), high scores (`scoreboard.py`). Intermediate issues live here. |
| `tests/` | The automated tests. Some issues ask you to add one; `tests/test_<name>.py` matches `arcade/<name>.py`. |

### 📖 Worth reading, not editing

| File | Why |
|---|---|
| **`docs/how-to-add-a-game.md`** | The single most useful file in the repo. Follow it start to finish and you have a merged PR. |
| `docs/architecture.md` | How the pieces fit together. Read it when you get curious, not before. |
| `CONTRIBUTING.md` | The workflow: claim an issue, branch, commit, open a PR. |

### 🙈 Safe to ignore completely

You will never need to touch any of these, and nothing in your issue will
require it.

| Thing | What it actually is |
|---|---|
| `.github/` | Robots. The checks that run on your PR, the issue templates, the bot that assigns you an issue when you comment `/claim`. Maintainer territory. |
| `ruff.toml`, `pyproject.toml` | Settings for the code checker. |
| `.gitignore` | A list of files Git should not track. |
| `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md` | Standard paperwork every open source project carries. |
| `.pytest_cache/`, `.ruff_cache/`, `__pycache__/` | Junk your own computer generates when you run the tests. Already ignored by Git. |

**The short version:** open an issue, it tells you the file. That file is
almost always in `arcade/games/`. Everything else is scenery.

---

## 🎃 Contributing — read this bit

**This repository exists so you can make your first pull request.** That is not
marketing. The issues were written specifically for people who have never
contributed to open source before.

### The fastest way in

1. Browse [issues labelled `good first issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
2. Comment **`/claim`** on one — a bot assigns it to you within seconds
3. Read [CONTRIBUTING.md](CONTRIBUTING.md)
4. Open a pull request with `Closes #<issue number>` in the description

### Three kinds of work here

| | |
|---|---|
| 🎮 **Add a game** | One new file, one line in a list. [Step-by-step guide with working code](docs/how-to-add-a-game.md) |
| 🐛 **Fix a bug** | There are real bugs in here on purpose. Each issue names the exact file and function |
| ✨ **Improve a game** | Difficulty levels, better ASCII art, an opponent that actually tries to win |

Every issue tells you the file to open, what "done" looks like, and how to
check your work. If an issue does not do that, it is our mistake — say so and
we will fix it.

---

## Full file tree, for reference

Everything marked *ignore* is infrastructure. It is listed only so that nothing
in the repo looks mysterious.

```
terminal-arcade/
├── arcade/
│   ├── __main__.py      # python -m arcade starts here
│   ├── main.py          # the menu and the list of games
│   ├── art.py           # ASCII banners and colours
│   ├── input_utils.py   # asking the player questions
│   ├── scoreboard.py    # high scores
│   └── games/           # ← one file per game. YOUR WORK GOES HERE
├── tests/               # pytest — some issues ask you to add one
├── docs/
│   ├── how-to-add-a-game.md   # ← read this first
│   └── architecture.md
│
├── .github/             # ignore — CI checks, issue templates, bots
├── ruff.toml            # ignore — code-checker settings
├── pyproject.toml       # ignore — packaging metadata
├── .gitignore           # ignore
├── LICENSE              # ignore — MIT
├── SECURITY.md          # ignore
└── CODE_OF_CONDUCT.md   # ignore
```

## What CI checks, and what can actually stop your PR

Two things, and only two:

| Blocks the merge | Why |
|---|---|
| **A test fails** | Something in `tests/` broke. |
| **A real bug is found** | An undefined variable, an unused import, a mutable default argument — code that is genuinely wrong. |

Everything else is advice. **Formatting never blocks you** — untidy spacing,
single quotes instead of double, imports in the wrong order, a missing newline
at the end of a file. Those appear as suggestions in the log and are ignored by
the gate. Your pull request merges either way.

This is deliberate. Nobody's first contribution should be rejected by a robot
over four spaces of whitespace.

## Running the tests

Tests need `pytest`, which is the only thing in this project that does:

```bash
python3 -m pip install pytest
python3 -m pytest
```

## Design rules

- **Standard library only.** Ever. This gets used at events on campus Wi-Fi,
  and `pip install` failing must never be why someone cannot take part
- **One file per game.** So contributors never collide with each other
- **Every game returns a score** from `play()`, and `main.py` decides what to
  do with it
- **Only `input_utils` calls `input()`**, so "that is not a number" behaves the
  same everywhere

More detail in [docs/architecture.md](docs/architecture.md).

## Events

Maintained by **OS & DevX**, GITHUB Community GITAM.

| Date | Event |
|---|---|
| Mon, Oct 5 | Open Source Kickoff & Live PR Lab |
| Mon, Oct 12 | PR Debug Clinic #1 — bring a broken branch |
| Wed, Oct 21 | PR Debug Clinic #2 |


## Contribution Test
This change verifies the contribution workflow for the event.


## License

[MIT](LICENSE)
