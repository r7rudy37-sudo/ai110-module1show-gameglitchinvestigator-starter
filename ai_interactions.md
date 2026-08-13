# AI Interactions Log

This log documents the AI-supported stretch work completed with Codex.

## Agent Workflow (Feature Expansion)

**Task given to the agent**

> Inspect the official Project 1 rubric and starter repository, reproduce the
> bugs, repair the game without hiding the original evidence, generate tests,
> and prepare the required documentation.

**What the agent completed**

- Inspected the course instructions and the 18-point required-feature rubric.
- Ran the broken Streamlit app and captured specific incorrect behavior.
- Updated `logic_utils.py` with pure comparison, parsing, hint, range, and score
  functions.
- Updated `app.py` to use the extracted logic, reset all session state, validate
  inputs, and add a structured Guess History table.
- Expanded `tests/test_game_logic.py` and completed `README.md`,
  `reflection.md`, and this interaction log.
- Created three meaningful local commits: bug evidence, repairs/tests, and final
  documentation.

**Manual verification and corrections**

I reviewed the changed files and did not accept incompatible type-syntax advice
for this Python 3.9 project. I ran the full pytest and Ruff checks, then tested
invalid input, a low guess, a winning guess, and New Game in the live interface.
The New Game check confirmed that attempts, score, feedback, and Guess History
were all cleared.

## Test Generation (Advanced Edge Cases)

**Prompt used**

> Generate focused pytest cases for `parse_guess()` and the extracted game
> logic. Include empty, non-numeric, decimal, negative, and out-of-range input,
> plus hint direction and scoring regressions. Keep every test deterministic.

| Edge Case | AI-Suggested Test | Did It Pass? | Why It Matters |
|-----------|-------------------|--------------|----------------|
| Empty or whitespace input | Parameterize `None`, `""`, and `"   "`; expect `Enter a guess.` | Yes | Prevents blank submissions from becoming attempts |
| Non-integer input | Parameterize `"hello"`, `"4.5"`, and `"1e2"`; expect a whole-number error | Yes | Prevents silent decimal truncation and confusing conversions |
| Out-of-range input | Parameterize `"0"`, `"101"`, and `"-5"` for a 1-100 game | Yes | Enforces the active difficulty boundaries |
| Wrong hint direction | Assert `Too High` contains `LOWER` and `Too Low` contains `HIGHER` | Yes | Protects the main starter bug from returning |
| Wrong-guess scoring | Assert high and low misses leave the score unchanged | Yes | Prevents repeated misses from adding points |

## Linting and Style

**Prompt used**

> Review the extracted Python logic for readable docstrings, PEP 8 issues, and
> import ordering without dropping Python 3.9 compatibility.

**First linting output**

```text
I001 Import block is un-sorted or un-formatted
Found 2 import-ordering errors.
```

The broader modernization pass also proposed `X | None`. I did not apply that
suggestion because the verified runtime is Python 3.9.6. I applied only the safe
import-order fixes and retained compatible `Optional`/`Tuple` annotations.

**Final linting output**

```text
$ ruff check --select E,F,I app.py logic_utils.py tests/test_game_logic.py
All checks passed!
```
