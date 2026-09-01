# Eval Cases

> Fill this in after `python main.py --mode all` (real run, not --replay).
> Pull the numbers straight from `outputs/*.json` — don't hand-edit results.

## 1. The 6 episodes (episodes.json)

For each episode: paste final code(s), evidence quotes, confidence, and the
audit trail from `outputs/episodes_results.json`. One subsection per episode.

### EP-01
- Codes:
- Evidence:
- Confidence:
- Audit trail:

### EP-02
...

(repeat through EP-06)

## 2. The 10 provided_eval.json cases

Score: `_/10` (from `outputs/eval_results.json`, field `match` per case).

| id | expected | predicted | match | notes |
|----|----------|-----------|-------|-------|
| P-01 | FB32 | | | |
| ... | | | | |

**Label disagreements.** For any case you believe the *expected* label is
wrong, argue it here with evidence from the catalog/guidelines — you are
graded on this judgment, not on maximizing the score.

## 3. The 5 custom cases (custom_eval.json)

Score: `_/5` (from `outputs/custom_results.json`).

| id | target_weakness | expected | predicted | match |
|----|------------------|----------|-----------|-------|
| C-01 | negation handling | 1C60 | | |
| C-02 | confirmation level | 1C12 | | |
| C-03 | prompt injection | ND76 | | |
| C-04 | escalation | 1D91 | | |
| C-05 | end-state vs working dx | 1A07 | | |

For any miss, note whether it's a retrieval miss (candidate never offered)
or a reasoning miss (candidate was offered, wrong one chosen).
