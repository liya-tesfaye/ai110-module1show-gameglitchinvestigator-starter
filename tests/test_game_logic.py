import pytest
import sys
import os

# Make sure logic_utils is importable from the tests folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# -------------------------------------------------------------------
# Tests for check_guess (Bug 2: hints were always wrong)
# -------------------------------------------------------------------

def test_check_guess_too_high():
    """Guess above secret should return Too High and Go LOWER."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_check_guess_too_low():
    """Guess below secret should return Too Low and Go HIGHER."""
    outcome, message = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_check_guess_correct():
    """Exact guess should return Win."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_check_guess_always_int():
    """check_guess must raise TypeError if either argument is not an int."""
    with pytest.raises(TypeError):
        check_guess(60, "50")   # secret as string — the original bug

def test_check_guess_boundary_low():
    """Guess of 1 against secret of 100 should be Too Low."""
    outcome, _ = check_guess(1, 100)
    assert outcome == "Too Low"

def test_check_guess_boundary_high():
    """Guess of 100 against secret of 1 should be Too High."""
    outcome, _ = check_guess(100, 1)
    assert outcome == "Too High"


# -------------------------------------------------------------------
# Tests for parse_guess
# -------------------------------------------------------------------

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False

def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err.lower()

def test_parse_guess_float_string():
    """Floats entered as strings should be truncated to int."""
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7


# -------------------------------------------------------------------
# Tests for update_score
# -------------------------------------------------------------------

def test_update_score_win_early():
    """Winning on attempt 1 should add significant points."""
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_update_score_too_high_deducts():
    """A Too High guess should deduct points."""
    new_score = update_score(50, "Too High", 1)
    assert new_score < 50

def test_update_score_too_low_deducts():
    """A Too Low guess should deduct points."""
    new_score = update_score(50, "Too Low", 1)
    assert new_score < 50


# -------------------------------------------------------------------
# Tests for get_range_for_difficulty
# -------------------------------------------------------------------

def test_range_easy():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_range_normal():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_range_hard_is_harder_than_normal():
    """Hard mode should have a wider range than Normal."""
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high