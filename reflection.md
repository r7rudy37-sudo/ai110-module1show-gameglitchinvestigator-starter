# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first opened the game, it looked normal, but it already said I had used
one attempt before I guessed anything. I opened the debug section and used the
secret number `65` to try guesses above and below it. The biggest issue was in
`check_guess()` because the result said Too High or Too Low, but the message told
me to move in the opposite direction. The app also changed the secret between a
number and text on alternating attempts, which made the comparison unreliable.
The score changed on wrong guesses, and New Game left the old history behind.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output or Error |
|-------|-------------------|-----------------|-------------------------|
| Start Normal mode without guessing | Show all 8 attempts | Showed only 7 attempts because the count started at 1 | `Secret: 65, Attempts: 1, Score: 0` |
| Guess `50` with secret `65` | Tell me to guess higher | Displayed `📉 Go LOWER!` | No error. The message in `check_guess()` was backward. |
| Guess `80` with secret `65` | Tell me to guess lower and keep the score stable | Displayed `📈 Go HIGHER!`. The score changed from `0` to `-5`, then back to `0` after the same wrong guess. | No error. `update_score()` changed points based on whether the attempt was odd or even. |
| Click New Game after several guesses | Clear the attempts, score, status, and history | Attempts reset, but the old history stayed there. | No error. Only part of `st.session_state` was reset. |

**What I saw before fixing it**

```text
Normal mode: secret=65, attempts=1, score=0, attempts_left=7
guess=50 -> displayed "📉 Go LOWER!"
guess=80 -> displayed "📈 Go HIGHER!", score=-5
guess=80 -> displayed "📈 Go HIGHER!", score=0
New Game -> secret=52, attempts=0, old history still present
pytest -q -> 3 failed because logic_utils.py still had placeholder errors
```

## 2. How did you use AI as a teammate?

Claude is the main AI tool we use in this class, and I followed the class habit
of focusing on one bug at a time instead of asking for one giant fix. I also
used Codex to inspect the full project, update the files, and create tests.
Codex correctly suggested moving the game logic into `logic_utils.py`, and I
checked that idea by running pytest and playing through a full game. One style
suggestion was to use `str | None`, but I checked my Python version and found
that the project runs on Python 3.9.6, so I kept `Optional[...]` instead. That
reminded me that AI suggestions can sound confident even when they do not fit
the exact setup I am using.

## 3. Debugging and testing your fixes

I did not count a bug as fixed just because the code looked better. I ran a
small test for the behavior and then checked the same thing in the Streamlit
game. All 21 tests passed after the changes. In the live game, bad input did not
use an attempt, `10` against secret `16` told me to go higher, and `16` ended the
game with a score of 90. New Game also cleared the score and history, so I knew
the state reset was working.

## 4. What did you learn about Streamlit and state?

Streamlit runs the script again whenever I click a button or change a widget.
Regular variables get created again during that run, but `st.session_state`
keeps the important game information. I used it for the secret, score, attempts,
status, and guess history. A normal guess should update only a few of those
values, while New Game needs to clear all of them.

## 5. Looking ahead: your developer habits

The main habit I want to keep is writing down the exact input, expected result,
and actual result before changing the code. After a fix, I want to add a small
test so the same bug does not come back later. Next time I will tell the AI my
Python version and project limits at the beginning. This project made me more
careful with AI generated code because something can look clean and still have
several small logic problems.
