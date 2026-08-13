"""Streamlit interface for the repaired number-guessing game."""

import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 10,
}


def reset_game(low: int, high: int, difficulty: str) -> None:
    """Create a clean game while preserving the selected difficulty."""
    # FIX: Reset every piece of game state and honor the active range.
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.feedback = None
    st.session_state.game_difficulty = difficulty
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1


def show_feedback() -> None:
    """Render the latest stored game message, if one exists."""
    feedback = st.session_state.feedback
    if not feedback:
        return

    level, message = feedback
    if level == "success":
        st.success(message)
    elif level == "error":
        st.error(message)
    else:
        st.warning(message)


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("A repaired AI-generated guessing game with testable logic.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

needs_initial_state = "secret" not in st.session_state
difficulty_changed = (
    st.session_state.get("game_difficulty") != difficulty
)
if needs_initial_state or difficulty_changed:
    reset_game(low, high, difficulty)

st.subheader("Make a guess")

raw_guess = st.text_input(
    f"Enter a whole number from {low} to {high}:",
    key=f"guess_input_{st.session_state.game_id}",
    disabled=st.session_state.status != "playing",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button(
        "Submit Guess 🚀",
        disabled=st.session_state.status != "playing",
    )
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_game(low, high, difficulty)
    st.rerun()

if submit and st.session_state.status == "playing":
    ok, guess_int, error = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: Invalid input no longer consumes a valid attempt.
        st.session_state.feedback = ("error", error)
    else:
        st.session_state.attempts += 1
        outcome = check_guess(guess_int, st.session_state.secret)
        st.session_state.history.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Result": outcome,
            }
        )
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.feedback = (
                "success",
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}",
            )
            st.balloons()
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.session_state.feedback = (
                "error",
                f"Out of attempts! The secret was "
                f"{st.session_state.secret}. Score: {st.session_state.score}",
            )
        elif show_hint:
            st.session_state.feedback = (
                "warning",
                get_hint_message(outcome),
            )
        else:
            st.session_state.feedback = None

attempts_left = attempt_limit - st.session_state.attempts
metric1, metric2 = st.columns(2)
metric1.metric("Attempts left", attempts_left)
metric2.metric("Score", st.session_state.score)

show_feedback()

if st.session_state.status == "won":
    st.info("Start a new game to play again.")
elif st.session_state.status == "lost":
    st.info("Start a new game to try again.")

if st.session_state.history:
    st.subheader("Guess History")
    st.table(st.session_state.history)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI, repaired with human review and automated tests.")
