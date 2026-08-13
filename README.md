# 🎮 Game Glitch Investigator

Game Glitch Investigator is a Streamlit number-guessing game repaired from an
intentionally buggy AI-generated starter. The player selects a difficulty,
enters whole-number guesses, follows higher/lower hints, and earns more points
for solving the game in fewer valid attempts.

## Setup and Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the automated checks with:

```bash
pytest -q
ruff check --select E,F,I app.py logic_utils.py tests/test_game_logic.py
```

## Bugs Found and Fixed

- **Reversed hints:** a low guess displayed `Go LOWER`, while a high guess
  displayed `Go HIGHER`. `get_hint_message()` now maps each outcome to the
  correct direction.
- **Mixed comparison types:** the app converted the secret to a string on
  alternating attempts. The extracted `check_guess()` now compares integers
  consistently.
- **Unstable scoring:** repeated wrong guesses could alternately add and remove
  points. `update_score()` now changes the score only after a win and rewards
  earlier wins.
- **Attempt-count bugs:** the game began at attempt 1 and invalid input consumed
  attempts. It now begins at 0 and increments only after a valid, in-range
  integer.
- **Incomplete reset:** New Game left old history/status behind and ignored the
  active range. `reset_game()` now clears all game state and uses the selected
  difficulty.
- **Untestable placeholders:** `logic_utils.py` raised `NotImplementedError`.
  The game logic now lives in pure, documented functions with pytest coverage.

## Demo Walkthrough

This is the verified post-fix game session used for the final check:

1. Start a Normal game. The page shows a range of 1-100, 8 attempts left, and
   a score of 0.
2. Enter `abc`. The game returns `Enter a whole number.` and still shows all 8
   attempts because invalid input does not consume one.
3. With the debug secret set to `16`, enter `10`. The game displays
   `📈 Too low — guess HIGHER!`, records the result in Guess History, leaves the
   score at 0, and shows 7 attempts left.
4. Enter `16`. The game reports a win, records the second attempt, and awards a
   final score of 90.
5. Select New Game. The score returns to 0, the history is cleared, all 8
   attempts are available, and a new in-range secret is generated.

## Automated Test Results

The suite covers comparison outcomes, correct hint directions, empty input,
non-numeric input, decimal input, negative/out-of-range values, difficulty
ranges, and scoring behavior.

```text
$ pytest -q
.....................                                                    [100%]
21 passed in 0.03s
```

Style verification:

```text
$ ruff check --select E,F,I app.py logic_utils.py tests/test_game_logic.py
All checks passed!
```

## AI Collaboration

Codex helped identify the code-level causes, extract the logic, generate tests,
and review the full project against the rubric. I verified its changes by
reviewing the diffs, running all 21 tests, and completing the live walkthrough
above. The detailed helpful and rejected suggestions are recorded in
[`reflection.md`](reflection.md), and the stretch workflow is recorded in
[`ai_interactions.md`](ai_interactions.md).

## Stretch Features Completed

- **Advanced edge-case testing:** more than three specific input edge cases are
  covered, and the passing output is included above.
- **Agent-mode feature expansion:** Codex added a functional Guess History table
  that records the attempt number, guess, and result.
- **Professional documentation and style:** every function in
  `logic_utils.py` has a docstring, and Ruff reports no E/F/I issues.
- **Enhanced UI and formatting:** attempts and score use metrics, feedback is
  clearly categorized, and the structured `st.table()` history makes each game
  easy to follow.
