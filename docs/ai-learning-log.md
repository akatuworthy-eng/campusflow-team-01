# AI-assisted learning log — CampusFlow

**IMPORTANT:** Complete each entry personally and truthfully. The items below are starting prompts, NOT claims that independent experiments or verification were completed. Each fellow needs at least three verified interactions, including one critically evaluated AI suggestion.

## Engineer A — Interaction 1: Boolean conditions and priority rules
- Problem: Understand why `and` and `or` produce different priority outcomes.
- Initial understanding (in my words): **[fill in]**
- Actual AI prompt: **[paste one of your actual questions or messages]**
- Guidance learned: `and` needs both conditions; `or` needs either condition; `if/elif` uses the first matching branch.
- My independent experiment and predicted output: **[run a small Python example and record exactly what you tried]**
- Actual output and verification: **[paste actual terminal result / source]**
- What I can explain now: **[fill in]**
- Related code: `campusflow/tickets.py` — `calculate_priority`

## Engineer A — Interaction 2: Automated unittest discovery
- Problem: Six new test functions had been defined at module level instead of as methods in `unittest.TestCase` classes.
- AI guidance to evaluate: Re-indent the six test functions into their respective test classes so discovery includes them.
- My independent experiment: **[pull updated branch; run `python3 -m unittest discover -s tests -v`; record test count/output]**
- Verification: **[paste actual output]**
- Decision: **[what you accepted or changed, and why]**
- Related file: `tests/test_tickets.py`

## Engineer A — Interaction 3: Unique ticket ID validation (critical evaluation)
- Problem: An earlier ID generator took the numeric portion of every ID without checking format or duplication.
- AI guidance: Validate `T...` shape, positive numeric suffix, canonical padding and duplicates before calculating the next ID.
- Independent experiment: **[show malformed-ID and duplicate-ID tests you personally ran]**
- Actual result: **[fill in]**
- Decision (accepted / improved / rejected): **[say exactly what you concluded after testing]**
- Related file: `campusflow/tickets.py`

## Engineer B
Create three separate genuine entries following the same fields: problem, prior understanding, exact AI prompt, guidance, independent experiment, actual verification, decision, related commit/PR, and your own explanation.
