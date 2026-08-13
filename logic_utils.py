"""Pure game logic for the Game Glitch Investigator project."""

from typing import Optional, Tuple

DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 500),
}

HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Too high — guess LOWER!",
    "Too Low": "📈 Too low — guess HIGHER!",
}


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """Return the inclusive number range for a difficulty name."""
    return DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES["Normal"])


def parse_guess(
    raw: Optional[str],
    low: Optional[int] = None,
    high: Optional[int] = None,
) -> Tuple[bool, Optional[int], Optional[str]]:
    """Validate text input and return ``(ok, integer, error_message)``."""
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."

    if low is not None and value < low:
        return False, None, f"Guess must be between {low} and {high}."
    if high is not None and value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Classify an integer guess as a win, too high, or too low."""
    # FIX: Keep both values as integers so comparison never becomes lexicographic.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint_message(outcome: str) -> str:
    """Return a player-facing hint that matches a comparison outcome."""
    # FIX: The starter's HIGHER/LOWER directions were reversed.
    return HINT_MESSAGES.get(outcome, "Try another guess.")


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Award more points for an earlier win and never reward a wrong guess."""
    # FIX: Wrong guesses previously alternated between adding and removing points.
    if outcome != "Win":
        return current_score

    normalized_attempt = max(1, attempt_number)
    points = max(10, 110 - (10 * normalized_attempt))
    return current_score + points
