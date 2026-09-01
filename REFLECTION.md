# Reflection

**What changes at 50,000 codes?**
Draft points to expand: TF-IDF index build time and memory are still fine
at that scale (still just term-frequency dicts), but bag-of-words
precision degrades further as the catalog gets denser — many codes will
share near-identical vocabulary (e.g. dozens of "cellulitis of X" variants),
so lexical top-K will increasingly return near-duplicates rather than
genuinely distinct candidates. At that scale you'd likely want a real
embedding-based retrieval layer (accepting the extra call/cost) with a
reranking step, and probably a hierarchical catalog structure (chapter ->
subchapter -> code) to narrow search space before ranking individual
codes at all.

**What changes when notes are handwritten and photographed instead of typed?**
Draft points to expand: an OCR/handwriting-recognition step becomes a new,
noisy first stage before any of this pipeline runs, and its errors
propagate — this pipeline currently trusts note text as accurately
transcribed. You'd need explicit uncertainty markers from OCR (e.g. low-
confidence spans) surfaced into the synthesis step so the model can
say "illegible" rather than guessing, and evidence-quote verification
(`verify_quotes()`) would need fuzzy matching instead of exact substring
matching, since OCR output won't match a "verbatim" quote exactly even
when it's substantively correct.

> Expand both sections with your own view before submitting — these are
> starting points, not final answers.
