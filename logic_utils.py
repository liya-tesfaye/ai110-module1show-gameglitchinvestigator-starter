import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard was returning 1-50 which is easier than Normal (1-100). Corrected ranges.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIXME: Logic breaks here — original code converted secret to a string on even
# attempts, causing int-vs-string comparisons that broke the hint direction.
def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"

    FIX: Removed the broken even/odd attempt string conversion from app.py.
    Both guess and secret are now always compared as integers.
    #FIX: Refactored logic into logic_utils.py using agent mode.
    """
    if not isinstance(guess, int) or not isinstance(secret, int):
        raise TypeError(f"guess and secret must both be int, got {type(guess)} and {type(secret)}")

    if guess == secret:
        return "Win", "🎉 Correct!"
    elif guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIXME: Logic breaks here — original code rewarded +5 points for wrong
    # "Too High" guesses on even attempts, which incentivized bad guesses.
    # FIX: Wrong guesses now always deduct points regardless of outcome type.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score