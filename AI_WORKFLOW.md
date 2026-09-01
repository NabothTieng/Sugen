# AI Workflow

**1. Context management** — What did you give the AI, and when?
Draft answer to build on: the full brief text, then the four data files
(catalog/guidelines/episodes/eval) once uploaded, so architecture
decisions (retrieval strategy, call budget) were made against the real
data shape rather than assumptions.

**2. Planning before code**
Draft answer to build on: clarified 3 open design decisions (retrieval
method, model, file layout) via structured questions before writing
`main.py`, rather than guessing and rewriting later.

**3. Verification — with one concrete caught mistake from this project**
The clearest one: the first live run against Gemini failed on all 21
cases with `404 NOT_FOUND — models/gemini-2.5-flash is no longer
available to new users`. The model I'd defaulted to during design (built
and prompt-tested in a sandbox with no network route to Google's API)
had been retired for new API keys by the time of the actual run; the
current equivalent is `gemini-3.6-flash`. Caught immediately because the
pipeline logs every attempt with the raw error rather than swallowing it,
so it was a one-line fix (`main.py` + `.env.example`) plus a standalone
`test_connection.py` added afterward specifically so a bad model/key
combination fails in ~2 seconds next time instead of after a multi-minute
full run. Also worth mentioning: the retrieval symmetry bug (EP-04
guideline retrieved, linked code JA63 missing from candidates) found by
smoke-testing the retrieval layer against all 6 episodes *before*
spending any LLM calls on it, and the EP-06 negation limitation that was
found but deliberately documented rather than patched under time
pressure.

**4. Tool and model routing**
Draft answer to build on: pure-python TF-IDF for retrieval (no embedding
API calls, deterministic, free) vs. Gemini for the 3 reasoning-heavy
steps that need actual clinical judgment; `gemini-2.5-flash` chosen over
`2.5-flash-lite` for reasoning quality, and over `2.5-pro` for free-tier
rate-limit headroom (only 5 RPM / ~50-100 RPD free) given the pipeline
easily exceeds that in a single full run.

