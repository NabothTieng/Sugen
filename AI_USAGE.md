# AI Usage

This project was built with AI assistance (Claude, in the Claude.ai chat
interface — not Claude Code) for design and code generation, and calls
Gemini (`gemini-3.6-flash` by default — see `PROGRESS_LOG.md` for why the
original `gemini-2.5-flash` default changed) at runtime as the clinical
reasoning engine inside the pipeline itself. These are two different
uses — keep them distinct when describing this:

- **Claude**: designed the 3-call architecture (synthesis → coding →
  verification), local TF-IDF retrieval, and caching/replay scheme;
  wrote `main.py`, `test_connection.py`, `CLAUDE.md`, `README.md`, and
  the templates for this set of files; caught the retrieval bugs
  documented in `PROGRESS_LOG.md` and `README.md` (the EP-04 guideline↔
  code retrieval gap, fixed; the EP-06 negation limitation, documented);
  caught and fixed the retired-model (`gemini-2.5-flash` →
  `gemini-3.6-flash`) and Windows/PowerShell `.env`-loading issues after
  they surfaced in live runs; drafted the 5 custom eval cases in
  `data/custom_eval.json`; and drafted first-pass answers for
  `AI_WORKFLOW.md` and `REFLECTION.md`.
- **Gemini**: is the model the *pipeline itself* calls at runtime to
  synthesize episodes, propose codes, and verify them. Claude never
  substitutes for this at runtime — it only wrote the code that calls
  Gemini.

## What I did myself

- Ran the pipeline locally on Windows (PowerShell), which surfaced two
  issues Claude's own sandboxed testing couldn't catch since it has no
  network route to Google's API: the retired-model 404, and the
  `export $(cat .env | xargs)` bash idiom not working in PowerShell.
- Patched `test_connection.py` myself to load the key via
  `python-dotenv` before Claude applied the same fix to `main.py` —
  i.e. I found and fixed half of that bug independently.
- Ran the actual live eval (`--mode all`), which is where the free-tier
  rate-limit ceiling showed up (7 of 10 `provided_eval.json` cases never
  completed on the first run) and where the real 2/3-correct-among-
  completed-cases result came from — my own first read of that result as
  an "85% win rate" was incorrect (Claude caught and corrected it), and I
  want the correction on the record here as well as in
  `REFLECTION.md`/`EVAL_CASES.md`: the actual number is 2/3 (67%) among
  completed cases, 2/10 (20%) against the full set, with the remainder
  incomplete rather than wrong.

