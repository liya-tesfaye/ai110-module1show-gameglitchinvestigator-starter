# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?


The input field accepted numbers, but pressing Enter did nothing (I had to click the "Submit Guess" button every time). The hint was giging wrong answers, always telling me to "Go Higher" regardless of what number I entered or what the secret number actually was. And also, the "New Game" button did nothing when I clicked it, so once the game ended there was no way to restart without manually refreshing the page.

Two concrete bugs I noticed right away:
- **Hints were always wrong:** No matter what number I guessed, the game always said "Go Higher" — even when my guess was clearly above the secret number.
- **New Game button was broken:** Clicking "New Game" had no effect. The game state never reset, so I was stuck with the same ended game and could not start over.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 75 (secret number was lower) | Hint displays "Go Lower" | Hint displayed "Go Higher" | none |
| Clicked "New Game" after game ended | Game resets with a new secret number and fresh score | Nothing happened; game state did not change | none |
| Typed a guess and pressed Enter | Guess is submitted | Nothing happened; had to click "Submit Guess" button manually | none |

--- 

## 2. How did you use AI as a teammate?

I used an AI coding assistant to help identify and fix three bugs in the game. 
The AI correctly diagnosed that the hint bug was caused by the secret number being 
converted to a string on even-numbered attempts, which broke the comparison logic in 
check_guess. It suggested removing the string conversion entirely and enforcing that 
both arguments must always be integers — this was correct and I verified it by running 
the pytest tests and confirming hints now show "Go LOWER" and "Go HIGHER" accurately 
in the live game.

The AI also correctly identified that the New Game button was broken because the status 
field in session state was never being reset, only the attempts counter. I verified this 
fix by playing a full game to completion and clicking New Game — the game successfully 
reset to a fresh state. One thing I had to review carefully was the AI's suggested reset 
logic, because it initially reset attempts to 0 instead of 1, which would have caused an 
off-by-one error in the attempt counter display. I caught this by reading the diff and 
corrected it before accepting the change.

## 3. Debugging and testing your fixes

I verified each fix in two ways: automated tests and live playtesting. For the hint bug, 
I ran pytest on test_game_logic.py which includes tests like test_check_guess_too_high 
(guess 60, secret 50 should return "Too High") and test_check_guess_string_raises 
(passing a string secret should raise TypeError). All 9 tests passed. For the New Game 
bug, I played the game to a loss and clicked the button — the game correctly reset. For 
the Enter key bug, I typed a guess and pressed Enter — it now submits without needing 
to click the button. The pytest suite gave me confidence that the core logic was sound 
before I even opened the browser.

## 4. What did you learn about Streamlit and state?

Streamlit works by rerunning your entire Python script from top to bottom every single 
time the user does anything — clicks a button, types in a box, or changes a setting. 
Think of it like refreshing a webpage, except the whole program reruns. The problem is 
that normal Python variables disappear on every rerun, so Streamlit gives you 
st.session_state, which is like a small notebook that survives each refresh. You store 
anything important there — the secret number, the score, the attempt count — and 
Streamlit picks it back up on the next rerun. That's why the New Game bug was so sneaky: 
the attempts counter got reset, but status was still sitting in the notebook saying 
"lost", so the game gave up before it even started.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is adding FIXME comments directly in the code before touching 
anything. It forced me to slow down, find the exact line causing the problem, and 
explain it in plain English before jumping to a fix. That made it much easier to write 
a focused prompt for the AI and to verify the fix actually targeted the right spot.

Next time I work with AI on a coding task, I would read the diff more carefully before 
accepting changes. In this project the AI's New Game fix had an off-by-one error in the 
attempt counter that I almost missed. A quick line-by-line review before clicking accept 
would have caught it immediately.

This project changed how I think about AI-generated code because I used to assume that 
if the code ran without crashing it was probably correct. Now I know that subtle logic 
bugs — like comparing an integer to a string — can pass silently and cause wrong behavior 
that only shows up when you actually play the game or write a targeted test.
