# 🎮 Game Glitch Investigator

This project started as a simple number guessing game made by AI. It looked fine
at first, but once I played it, I noticed that the hints pointed the wrong way,
the attempt count was off, and the score did not make much sense. I worked
through each problem, cleaned up the code, and tested the game until it behaved
the way I expected.

## How to run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

To run the checks:

```bash
pytest -q
ruff check --select E,F,I app.py logic_utils.py tests/test_game_logic.py
```

## What I found and fixed

1. The hints were backward. A low guess told me to go lower, and a high guess
   told me to go higher. I fixed the messages so they point the player in the
   right direction.
2. The secret number changed between an integer and a string on different
   attempts. I kept both the guess and secret as integers so the comparison is
   consistent.
3. Wrong guesses could add or remove points depending on the attempt number. I
   changed the score so points are only added after a win.
4. The game started with one attempt already used, and bad input counted as an
   attempt. It now starts at zero and only counts a valid guess.
5. New Game did not clear everything. I updated `reset_game()` so it resets the
   score, attempts, status, history, and secret number.
6. `logic_utils.py` only had placeholder errors. I moved the real game logic
   into that file and added tests for it.

## Demo Walkthrough

Here is the final game session I used to check everything:

1. I started a Normal game with a range of 1 to 100. It showed 8 attempts and a
   score of 0.
2. I entered `abc`. The game told me to enter a whole number and did not use an
   attempt.
3. The debug secret was `16`, so I tried `10`. The game correctly told me to go
   higher, kept the score at 0, and saved the guess in the history table.
4. I entered `16`. The game ended with a win and gave me a score of 90.
5. I clicked New Game. The score and history cleared, and all 8 attempts came
   back.

## Test results

I tested regular guesses, hint directions, scoring, difficulty ranges, blank
input, text input, decimals, negative numbers, and numbers outside the active
range.

```text
$ pytest -q
.....................                                                    [100%]
21 passed in 0.03s
```

```text
$ ruff check --select E,F,I app.py logic_utils.py tests/test_game_logic.py
All checks passed!
```

## How I used AI

Claude is the main AI tool for this class, so I followed the class workflow of
looking at one bug at a time and checking each suggestion before accepting it.
I also used Codex to inspect the files, make the code changes, write tests, and
check the finished project against the rubric. I did not treat either tool as
automatically correct. I checked the code, ran the tests, and played the game
myself before calling it finished.

More details are in [`reflection.md`](reflection.md) and
[`ai_interactions.md`](ai_interactions.md).

## Stretch work

1. I added more than three edge case tests and included the passing results.
2. I used an AI coding agent to add a Guess History table with the attempt,
   guess, and result.
3. I added docstrings to every function in `logic_utils.py` and checked the
   style with Ruff.
4. I made the page easier to follow with score and attempt metrics, clear
   feedback messages, and a history table.
