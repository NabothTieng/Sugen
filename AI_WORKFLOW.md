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
Use the real one from `PROGRESS_LOG.md`: the retrieval symmetry bug (EP-04
guideline retrieved, linked code JA63 missing from candidates) found by
smoke-testing the retrieval layer against all 6 episodes *before* spending
any LLM calls on it. Also mention the EP-06 negation limitation that was
found but not fully fixed — describe the reasoning for documenting vs.
patching it under time pressure.

**4. Tool and model routing**
Draft answer to build on: pure-python TF-IDF for retrieval (no embedding
API calls, deterministic, free) vs. Gemini for the 3 reasoning-heavy
steps that need actual clinical judgment; `gemini-2.5-flash` chosen over
`2.5-flash-lite` for reasoning quality, and over `2.5-pro` for free-tier
rate-limit headroom (only 5 RPM / ~50-100 RPD free) given the pipeline
easily exceeds that in a single full run.

**5. Something you deliberately did not delegate to AI**
> Fill in from your own local session — this needs to be a real "I did
> this part myself and here's why" answer, not generated.
