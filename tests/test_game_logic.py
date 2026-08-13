"""Automated verification for the extracted guessing-game logic."""

import pytest

from logic_utils import (
    check_guess,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


@pytest.mark.parametrize(
    ("guess", "secret", "expected"),
    [
        (50, 50, "Win"),
        (60, 50, "Too High"),
        (40, 50, "Too Low"),
    ],
)
def test_check_guess(guess, secret, expected):
    """Comparison outcomes should match the numeric relationship."""
    assert check_guess(guess, secret) == expected


def test_hint_directions_match_outcomes():
    """Player-facing directions should guide a guess toward the secret."""
    assert "LOWER" in get_hint_message("Too High")
    assert "HIGHER" in get_hint_message("Too Low")


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_parse_guess_rejects_empty_input(raw):
    """Empty input should fail without producing an integer."""
    ok, value, error = parse_guess(raw, 1, 100)
    assert (ok, value) == (False, None)
    assert error == "Enter a guess."


@pytest.mark.parametrize("raw", ["hello", "4.5", "1e2"])
def test_parse_guess_rejects_non_integers(raw):
    """Non-integer text should produce a useful validation error."""
    ok, value, error = parse_guess(raw, 1, 100)
    assert (ok, value) == (False, None)
    assert error == "Enter a whole number."


@pytest.mark.parametrize("raw", ["0", "101", "-5"])
def test_parse_guess_rejects_values_outside_range(raw):
    """Numeric guesses outside the active range should be rejected."""
    ok, value, error = parse_guess(raw, 1, 100)
    assert (ok, value) == (False, None)
    assert error == "Guess must be between 1 and 100."


def test_parse_guess_accepts_trimmed_integer():
    """Whitespace around a valid integer should be harmless."""
    assert parse_guess(" 42 ", 1, 100) == (True, 42, None)


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_wrong_guess_does_not_change_score(outcome):
    """A wrong guess should never add or subtract points."""
    assert update_score(0, outcome, 2) == 0


def test_earlier_win_is_worth_more_points():
    """The scoring rule should reward solving the game sooner."""
    first_attempt = update_score(0, "Win", 1)
    fifth_attempt = update_score(0, "Win", 5)
    assert first_attempt == 100
    assert fifth_attempt == 60
    assert first_attempt > fifth_attempt


@pytest.mark.parametrize(
    ("difficulty", "expected"),
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 500)),
        ("Unknown", (1, 100)),
    ],
)
def test_difficulty_ranges(difficulty, expected):
    """Every difficulty should resolve to an intentional range."""
    assert get_range_for_difficulty(difficulty) == expected
