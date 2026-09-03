# AI Workflow

**1. Context management** — What did you give the AI, and when?

Gave it the full brief text first, then the four provided data files
(`icd_catalog.json`, `guideline_snippets.json`, `episodes.json`, `provided_eval.json`)
once uploaded, so architecture decisions — retrieval strategy, call budget, how to
handle the free-text East African clinical shorthand — were made against the real
data shape instead of assumptions about what "a clinic note" would look like.

**2. Planning before code**

Clarified 3 open design decisions — retrieval method, model choice, file layout — via
structured questions before writing `main.py`, rather than guessing and rewriting
later. In particular, the decision to keep retrieval as pure-Python TF-IDF rather than
an embedding call was made at this stage, before any code existed, specifically to
protect the 3-call budget.

**3. Verification — with one concrete caught mistake from this project**

The clearest one: the first live run against Gemini failed on all 21 cases with
`404 NOT_FOUND — models/gemini-2.5-flash is no longer available to new users`. The
model I'd defaulted to during design (built and prompt-tested in a sandbox with no
network route to Google's API) had been retired for new API keys by the time of the
actual run; the current equivalent is `gemini-3.6-flash`. Caught immediately because
the pipeline logs every attempt with the raw error rather than swallowing it, so it
was a one-line fix (`main.py` + `.env.example`) plus a standalone `test_connection.py`
added afterward specifically so a bad model/key combination fails in ~2 seconds next
time instead of after a multi-minute full run.

Also worth naming: the retrieval symmetry bug (EP-04 guideline retrieved, linked code
JA63 missing from candidates) was found by smoke-testing the retrieval layer against
all 6 episodes *before* spending any LLM calls on it, and stayed fixed on the first
live run against EP-04 afterward. The EP-06 negation limitation was found the same
way and deliberately documented rather than patched under time pressure — see
`README.md`'s "Known limitation" section.

A second round of verification happened after external review: the reviewer pointed
out that `confidence` was `"high"` on every completed case and that the audit step
never demonstrably changed a draft — i.e., the verification call looked structurally
present but wasn't provably doing anything. I did not just take the model's word that
this was fixed by re-wording the prompt more strongly. I changed the call-3 output
schema to require five independently-scored checks instead of one free-text summary,
and added a separate, non-LLM `calibrate_confidence()` function that recomputes
confidence from measurable signals (shortlist membership, confirmation level,
quote-verification warnings) rather than trusting the model's self-report — see
question 5 below for why that specific piece was kept out of the LLM's hands.

**4. Tool and model routing**

Pure-Python TF-IDF for retrieval (no embedding API calls, deterministic, free,
inspectable) vs. Gemini for the 3 reasoning-heavy steps that need actual clinical
judgment; `gemini-2.5-flash` chosen over `2.5-flash-lite` for reasoning quality, and
over `2.5-pro` for free-tier rate-limit headroom (only 5 RPM / ~50-100 RPD free) given
the pipeline easily exceeds that in a single full run — confirmed in practice, since
the free tier was in fact exhausted mid-run on the actual submission run (see
`EVAL_CASES.md`).

**5. Something deliberately not delegated to AI**

Two things, both because trusting the model's own judgment on them would have
undermined the point of having them at all:

- **Confidence scoring.** Early versions let call 3 assign its own `confidence`
  label. In practice this produced `"high"` on every completed case regardless of how
  much the draft actually held up — a self-report with no discriminating signal isn't
  worth having. `calibrate_confidence()` is deterministic Python: it downgrades
  confidence when a code came from outside the local shortlist, when confirmation
  level isn't "confirmed," or — hard floor to `"low"` — when the independent,
  non-LLM `verify_quotes()` check catches a hallucinated quote. The model's own label
  is kept alongside as `model_reported_confidence` for comparison, but it does not get
  to decide the number that actually ships.
- **Adjudicating label disagreements.** The brief is explicit that this is graded on
  judgment, not score: *"you are graded on your judgment about the labels, not on your
  score against them."* That is deliberately a human call, argued with evidence from
  the catalog/guidelines in `EVAL_CASES.md`, not something to ask the model to decide
  and then transcribe. (As of this writing no eval case has actually completed to
  produce a disagreement to argue — see `EVAL_CASES.md` — but the intent is that when
  one does surface, it gets argued by me, not auto-accepted from either the model or
  the provided label by default.)
