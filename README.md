# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Purpose:** This is a number guessing game where the player tries to guess a secret 
number within a limited number of attempts. The game gives hints after each guess 
("Go Higher" or "Go Lower") and tracks a score that increases on a correct guess 
and decreases on wrong ones. Difficulty settings change the number range and attempt limit.

**Bugs Found:**
1. **Hint logic was broken** — On every even-numbered attempt, the secret number was 
   secretly converted to a string. This caused Python to compare an integer to a string, 
   which broke the greater-than/less-than comparison and made hints almost always wrong.
2. **New Game button did not work** — The button reset the attempt counter but never 
   reset `st.session_state.status`. Since status was still "lost" or "won", the game 
   immediately hit its end-state guard and called `st.stop()`, freezing the page.
3. **Enter key did not submit a guess** — The text input and submit button were not 
   connected. In Streamlit, pressing Enter in a text field only submits if the input 
   is wrapped inside an `st.form`.

**Fixes Applied:**
1. Removed the string conversion from `app.py` entirely. `check_guess` in `logic_utils.py` 
   now enforces that both `guess` and `secret` must be integers and raises a `TypeError` 
   if they are not.
2. Updated the New Game button to reset all five session state keys: `secret`, `attempts`, 
   `score`, `status`, and `history`.
3. Wrapped the text input and submit button inside `st.form("guess_form")` with 
   `st.form_submit_button`, which enables Enter-to-submit behavior automatically.
4. Moved all game logic (`check_guess`, `parse_guess`, `update_score`, 
   `get_range_for_difficulty`) out of `app.py` and into `logic_utils.py` so the UI 
   and logic are cleanly separated.

## 📸 Demo Walkthrough

1. Player opens the app and selects **Normal** difficulty (range: 1–100, 8 attempts)
2. Player types **40** and presses Enter — game returns **"📈 Go HIGHER!"** and deducts 5 points
3. Player types **70** — game returns **"📉 Go LOWER!"** and deducts another 5 points
4. Player types **55** — game returns **"📈 Go HIGHER!"**
5. Player types **62** — game returns **"🎉 Correct!"**, score increases by 60 points, balloons appear
6. Player clicks **New Game** — all state resets, a new secret number is chosen, and the game starts fresh

## 🧪 Test Results
$ python -m pytest tests/test_game_logic.py -v
tests/test_game_logic.py::test_check_guess_too_high          PASSED

tests/test_game_logic.py::test_check_guess_too_low           PASSED

tests/test_game_logic.py::test_check_guess_correct           PASSED

tests/test_game_logic.py::test_check_guess_always_int        PASSED

tests/test_game_logic.py::test_check_guess_boundary_low      PASSED

tests/test_game_logic.py::test_check_guess_boundary_high     PASSED

tests/test_game_logic.py::test_parse_guess_valid_integer     PASSED

tests/test_game_logic.py::test_parse_guess_empty_string      PASSED

tests/test_game_logic.py::test_parse_guess_none              PASSED

tests/test_game_logic.py::test_parse_guess_non_numeric       PASSED

tests/test_game_logic.py::test_parse_guess_float_string      PASSED

tests/test_game_logic.py::test_update_score_win_early        PASSED

tests/test_game_logic.py::test_update_score_too_high_deducts PASSED

tests/test_game_logic.py::test_update_score_too_low_deducts  PASSED

tests/test_game_logic.py::test_range_easy                    PASSED

tests/test_game_logic.py::test_range_normal                  PASSED

tests/test_game_logic.py::test_range_hard_is_harder_than_normal PASSED
================== 17 passed in 0.12s ==================
