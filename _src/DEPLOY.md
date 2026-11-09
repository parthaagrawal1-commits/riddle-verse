# riddleverse.com — how it works

- Static site + one tiny PHP API (`/api/index.php`, SQLite in `/api/data/`) for daily stats and the global leaderboard. Hostinger runs PHP; nothing else to configure.
- Build: `cd _src && python3 build.py` → writes site to repo root. Push to `main`; Hostinger auto-deploys.
- Global reset at **00:00 UTC**. The client picks today's UTC date and fetches `/p/YYYY-MM-DD.json`. The build publishes puzzle JSON only for dates ≤ today+2 (UTC), so future puzzles are never on the server early. **The build must run at least once a day.**
- Answers are shipped as SHA-256 hashes of normalised answers (lowercase, punctuation stripped, leading a/an/the removed), plus a "close" set (each answer with one character deleted) for the "so close" nudge. Explanations/trivia are lightly obfuscated (`ob()` = base64 of the reversed string).

## Data: `_src/data/puzzles.json` (keyed by UTC date)
```
"2026-11-09": { "n": 1,
  "riddle": {"q": "...", "a": ["answer","variant"...], "display": "answer", "hints": [h1,h2,h3], "why": "...", "trivia": "...", "difficulty": 1-5, "category": "kids|classic|wordplay|logic|math"},
  "rebus":  {"q": "🐝 + 🍃", "a": [...], "display": "believe", "hints": [3], "why": "...", "difficulty": 1-5},
  "chain":  {"clues": [{"q": "...", "a": ["word"]} x5], "final": ["word"], "why": "..."} }
```
Rules for new puzzles:
- `a` must include every reasonable spelling/variant (with and without article, singular/plural, "I see"/"eye sea"). Normalise mentally: lowercase, no punctuation.
- Chain: five single-word answers whose FIRST LETTERS spell the final word; clues must be unambiguous for a 10-year-old.
- Riddles: mix public-domain classics with originals; never two similar riddles within 60 days; difficulty curve across the week (Mon easier → Sat hardest, Sun playful).
- Rebus: emoji that render on all platforms; say-it-aloud logic; include the literal compound ("rain bow") in `a`.
- Hints go from vague to nearly giving it away; `why` is one sentence; `trivia` is one true, sourced-in-your-head fact (no numbers you are not sure of; prefer well-known facts).
- `n` increments by one per day without gaps.
- `_src/data/library.json`: extra riddles for the collection pages: `{"q","a","category","difficulty"}`.

## Quality gates before pushing
- `python3 build.py` succeeds; `node --check assets/app.js`; `php -l api/index.php`.
- Every date from today through today+30 exists in puzzles.json with all three games.
- No duplicate riddle text across puzzles.json + library.json.
