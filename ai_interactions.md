# AI Interactions Log

This file covers the extra AI work I did for the stretch features.

## AI tools and workflow

Claude is the main tool taught in this class, so I followed the class workflow
of giving the AI one focused problem, checking the answer, and testing the result
before moving on. For the actual project files, I used Codex as a coding agent to
inspect the repository, edit the files, run the tests, and check the rubric.

## Agent workflow for the Guess History feature

### What I asked for

I asked the coding agent to find the bugs in the starter game, move the main
logic into `logic_utils.py`, add tests, and make the game easier to follow. I
also asked it to keep a visible history of each valid guess.

### What the agent changed

1. It updated `logic_utils.py` with functions for parsing guesses, comparing the
   guess, choosing a hint, setting the difficulty range, and updating the score.
2. It updated `app.py` so New Game clears the full session state.
3. It added a Guess History table that shows the attempt number, guess, and
   result.
4. It expanded `tests/test_game_logic.py` and helped finish the README and
   reflection.

### What I checked myself

I read through the changed files, ran pytest, ran Ruff, and played the game in
the browser. I tried bad input, a low guess, the correct guess, and New Game. I
also skipped a type syntax suggestion that did not work with Python 3.9.

## Test generation

### Prompt

> Create focused pytest cases for parse_guess and the game logic. Include blank
> input, text, decimals, negative numbers, numbers outside the range, hint
> directions, and scoring. Keep the tests simple and repeatable.

| Edge Case | Test Idea | Passed? | Why I Included It |
|-----------|-----------|---------|-------------------|
| Blank input | Try `None`, an empty string, and spaces | Yes | A blank submission should not count as a guess. |
| Text and decimals | Try `hello`, `4.5`, and `1e2` | Yes | The game asks for a whole number and should not quietly change the input. |
| Outside the range | Try `0`, `101`, and `-5` in a 1 to 100 game | Yes | The selected difficulty range should matter. |
| Hint direction | Check that Too High says lower and Too Low says higher | Yes | This was one of the main starter bugs. |
| Wrong guess scoring | Check that a miss leaves the score alone | Yes | A wrong answer should not give points. |

## Style check

### Prompt

> Check the Python files for readable docstrings, import order, and basic style
> problems. Keep the code compatible with Python 3.9.

The first check found two import order problems. I fixed those, kept the Python
3.9 compatible type annotations, and ran the check again.

```text
$ ruff check --select E,F,I app.py logic_utils.py tests/test_game_logic.py
All checks passed!
```
