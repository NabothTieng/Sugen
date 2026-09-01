# Reflection

**What changes at 50,000 codes?**

The bottleneck is precision, not raw speed. Bag-of-words TF-IDF retrieval
degrades as the catalog gets denser: at 50,000 codes there will be dozens
of near-identical entries (e.g. many "cellulitis of X" variants), so
lexical top-K increasingly returns near-duplicates instead of genuinely
distinct candidates — the EP-06 erysipelas/cellulitis negation confusion
in this project is a preview of that failure mode, just at 288 codes
instead of 50,000. At that scale I'd move to embedding-based retrieval
with a reranking step, and a hierarchical catalog (chapter -> subchapter
-> code) to narrow the search space before ranking individual codes.

Throughput also becomes a real constraint, but the fix is concurrency
within your rate-limit budget, not more machines. Running episodes
through multiple VMs against the *same* free-tier key doesn't help —
they'd all queue behind the same per-project rate limit. And using
several free-tier keys/projects specifically to route around that limit
is against Gemini's terms of service (limits are enforced per project,
and Google's docs explicitly call out creating multiple projects to
bypass quota as a violation). The legitimate path is a paid tier with
higher RPM, and processing episodes concurrently (e.g. asyncio with a
semaphore capped at your RPM ceiling) — that's a code change, not a
budget-for-hardware change.

At 50,000 codes/day the real cost and consistency levers are:

1. **Shared cache, not per-machine cache.** If work is ever split across
   multiple workers, `cache/` can't stay local JSON files — two workers
   could process the same case differently or duplicate spend on it. The
   fix is a shared backend (Redis, a database table, or a shared bucket)
   keyed the same way the current cache already is (case id + call name),
   since the design is backend-agnostic — it's just get/set by key. A
   lightweight claim step avoids two workers computing the same missing
   key at once; for a system this size, occasionally accepting a
   duplicate computation is simpler than full distributed locking.
2. **Tiered model routing.** Route "obvious" cases (retrieval found one
   clearly dominant candidate, high lexical confidence) to a cheaper/
   faster model tier, and reserve the stronger reasoning tier for
   ambiguous cases — flagged by low retrieval confidence or a low-
   confidence result from a first pass.
3. **Dedup near-identical episodes** before spending calls on them, since
   at high volume many presentations will be near-templated repeats.

**What changes when notes are handwritten and photographed instead of typed?**

Cost rises for a real reason, not just "images are billed differently" —
a photographed note puts more of the *reasoning burden* inside the same
call. Today, synthesis only has to read clean text. With a photo, the
model is simultaneously doing handwriting recognition, layout parsing
(is this a table, a marginal note, a stamp?), and clinical reasoning in
one pass — that's a harder task per call even before counting tokens.

Three concrete changes to the pipeline:

1. **OCR errors become a new, silent source of wrong diagnoses.** The
   pipeline currently trusts note text as ground truth. With handwriting,
   it can't — a misread "no" as "now," or a misread dose, changes the
   clinical picture. This needs explicit uncertainty surfaced from
   whatever reads the image (low-confidence spans flagged, not silently
   guessed) into the synthesis step, so the model can say "illegible" or
   "low confidence" rather than confidently coding from a misread.
2. **Evidence-quote verification breaks and needs to change shape.**
   `verify_quotes()` currently requires an exact substring match against
   the source text. That's meaningless against imprecise OCR output —
   either it needs fuzzy matching (edit distance / normalized similarity
   instead of exact match), or verification needs to happen against
   bounding boxes / regions of the original image rather than a
   transcribed string at all.
3. **The injection-resistance guardrail needs to extend to the visual
   channel, not just quoted text.** A photographed note isn't just
   handwriting — it can contain a QR code, a sticker, a stamp, or text
   deliberately formatted to look like a system instruction, none of
   which the current text-only guardrail (`SYSTEM_GUARDRAIL` in
   `main.py`) was written to anticipate. Where possible, the safer
   design is to keep the LLM from ever "seeing" the raw image at all:
   run OCR as a separate, non-agentic pre-processing step that only
   outputs plain text, so the multimodal attack surface (image-embedded
   instructions) never reaches the reasoning model in the first place.
   If visual reasoning genuinely can't be avoided (e.g. layout matters,
   or there are diagrams), the same "this is data, not instructions"
   guardrail needs to be stated for image content explicitly, since
   nothing about the current wording covers a QR code or a stamp.

One more thing worth naming: a photographed note is a stronger
patient-privacy exposure than typed text (image metadata, whatever's
visible in the background of the photo), which is a handling question
that needs solving before the image reaches an LLM call at all, not
something this reflection can wave away as a prompt-engineering detail.
