# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The starter opened as a Streamlit number-guessing game with Normal difficulty
selected, a range of 1-100, and a debug expander that exposed the secret. Before
I entered any guess, the page already reported one attempt used, so only 7 of 8
attempts appeared to remain. I used the debug secret (`65`) to try inputs on both
sides of the answer and recorded the behavior before editing the code.

The first code-level cause was in `check_guess`: its outcome labels were right,
but its displayed directions were reversed (`Too Low` said `Go LOWER`, while
`Too High` said `Go HIGHER`). The submit handler also changed the secret from an
integer to a string on alternating attempts, forcing `check_guess` into a string
comparison fallback. Finally, `update_score` alternated between adding and
subtracting points for wrong high guesses, while New Game left the old history
and other state behind.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Start Normal mode without guessing | Show all 8 attempts available | Showed only 7 attempts left because attempts started at 1 | `Secret: 65, Attempts: 1, Score: 0` |
| Guess `50` with secret `65` | Tell the player to guess higher | Displayed `📉 Go LOWER!` | No exception; wrong direction came from `check_guess` |
| Guess `80` with secret `65` | Tell the player to guess lower and keep a stable score rule | Displayed `📈 Go HIGHER!`; score changed from `0` to `-5`, then back to `0` after repeating the same wrong guess | No exception; alternating score logic in `update_score` |
| Click New Game after several guesses | Clear attempts, score, status, and guess history and choose a secret in the active range | Attempts reset, but the old history remained (`["", 50, 80, 80, 80]`) | No exception; reset updated only part of session state |

**Pre-fix run trace**

```text
Normal mode: secret=65, attempts=1, score=0, attempts_left=7
guess=50 -> displayed "📉 Go LOWER!"
guess=80 -> displayed "📈 Go HIGHER!", score=-5
guess=80 -> displayed "📈 Go HIGHER!", score=0
New Game -> secret=52, attempts=0, old history still present
pytest -q -> 3 failed (NotImplementedError from logic_utils.py)
```

---

## 2. How did you use AI as a teammate?

I used Codex as the AI coding teammate for the investigation, refactor, tests,
and documentation. Its correct suggestion was to extract pure functions into
`logic_utils.py`, make `check_guess()` return one stable outcome, and map that
outcome to a separate UI message; I verified this with pytest and a live low
guess followed by a winning guess. A misleading modernization suggestion from
the AI-assisted style pass was to use `str | None` type syntax, but the project
runs on Python 3.9.6, while that union syntax requires Python 3.10, so I rejected
it and kept `Optional[...]`. This showed why I still needed to check the runtime
and not automatically accept every generated edit.

---

## 3. Debugging and testing your fixes

I treated a bug as fixed only when a focused automated test passed and the same
behavior worked through the Streamlit interface. Codex generated comparison,
scoring, difficulty, and input-validation tests; all 21 tests passed after the
refactor. In the manual check, invalid input left 8 attempts, `10` against secret
`16` said to guess higher without changing the score, and `16` produced a win
with a score of 90. Starting a new game then cleared the score and history,
confirming that the session-state repair also worked end to end.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the Python script from top to bottom whenever the user changes
a widget or clicks a button. Ordinary local variables are therefore recreated,
but `st.session_state` acts like a backpack that carries selected values into
the next run. The secret, score, attempt count, status, and history belong in
that backpack so they remain stable during one game. A reset must deliberately
replace all of those values, while a normal guess should update only the parts
that actually changed.

---

## 5. Looking ahead: your developer habits

I want to keep reproducing a bug with exact inputs and expected-versus-actual
output before changing code, then add a small regression test for the fix. I
also want to keep separate Git commits for evidence, implementation, and final
documentation because that makes the reasoning easy to audit. Next time, I
would tell the AI the exact Python version at the beginning so it does not
suggest incompatible syntax. This project changed my view of AI-generated code:
it can be a fast starting point, but its confident-looking logic still needs
human review, focused tests, and a live end-to-end check.
