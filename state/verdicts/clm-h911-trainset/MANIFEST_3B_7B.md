# H_911 Training-Set — 3B / 7B Token-Budget Manifest (HONEST)

Data layer for a future, separate GPU pre-training run (g8 dispatch, OUT OF SCOPE here).
This document states the token budget HONESTLY and distinguishes the **max reachable
real-data set** from a **down-scoped H_911 validation set**. No exaggeration.

## 1. What was actually built

| set | source | concepts | anchors (×5 langs) | byte-tokens (vocab=256) | real frac |
|-----|--------|---------:|-------------------:|------------------------:|----------:|
| FULL real | FLORES-200 dev+devtest | 2,009 | 10,045 | 1,643,965 | 1.00 |
| pilot (committed) | FLORES-200 (first 20c) | 20 | 100 | ~16k | 1.00 |

- Both orderings (parallel concept-major c>0 · concat language-major c~0) carry the
  **byte-identical** anchor-payload multiset; they differ ONLY in `.limen` member ordering.
- VERIFY = ALL-GREEN (merkle recompute · member sha256 · payload-multiset-identical · shard-bytes-differ).
- per-lang byte split: en 257,386 · zh 238,065 · ru 512,640 · ja 327,157 · ko 308,717.

## 2. Full-pretrain targets vs reality

| target | tokens needed | real built (FLORES) | coverage | gap |
|--------|--------------:|--------------------:|---------:|----:|
| 3B full pretrain | ~60,000,000,000 | 1,643,965 | 0.00274 % | ×36,497 |
| 7B full pretrain | ~140,000,000,000 | 1,643,965 | 0.00117 % | ×85,160 |

Repeating the real set to hit 60B would need ~36,497 epochs — that is overfitting,
not pretraining. **Public 5-language true-parallel corpora cannot reach full-pretrain scale.**

## 3. Max reachable REAL 5-language data (ceiling)

The largest honestly-reachable real 5-lang set, combining every source surveyed:

| source | reachable | 5-way truly aligned? | license |
|--------|-----------|----------------------|---------|
| FLORES-200 (fbaipublicfiles CDN) | 2,009 concepts × 5 = 10,045 anchors | YES (line-aligned) | CC-BY-SA-4.0 |
| OPUS-100 (HF, ungated, streamable) | ~1M en-X pairs × 4 (en-ko/zh/ru/ja) | NO — en-centric pairs, not one 5-way row | "unknown" (per HF card) |
| Tatoeba (HF `Helsinki-NLP/tatoeba`, ungated) | partial pairs | NO — pair graph, needs custom 5-way join | CC-BY-2.0 |
| FLORES-200 / flores_plus on HF Hub | **GATED** (manual access) — not reachable via token | — | CC-BY-SA-4.0 |

- **Max reachable, true 5-way parallel**: ~10,045 anchors (~1.64M byte-tok) = FLORES-200 only.
- **Max reachable, including en-pivot pseudo-5way (OPUS-100, noisy, NOT concept-aligned)**:
  ~0.4B byte-tok ceiling = **0.67 % of 3B target, 0.29 % of 7B target.**
- Even the absolute ceiling of public 5-lang data is **under 1 %** of a 3B full pretrain.

## 4. Honest scope split (g63 · a_scale_honest_scope)

- **MAX REACHABLE REAL-DATA SET** = FLORES-200 (10,045 true-parallel anchors). 100 % real,
  CC-BY-SA-4.0, true cross-lingual concept alignment — the cleanest H_911 signal, but tiny.
- **DOWN-SCOPED H_911 VALIDATION SET** (recommended) = the FLORES-200 full set used NOT as
  a pretraining corpus but as a **controlled parallel-vs-concat probe**: same bytes, two
  orderings, measure super-additive integration (the C5 / F-CLM-AKIDA-MULTILING-SEMANTIC
  contract). This is what the 10,045-anchor build is FOR. It validates the H_911 *ordering
  effect*, it does NOT pretrain a 3B/7B model.
- A genuine 3B/7B *pretrain* would require monolingual web-scale corpora (out of the
  "5-language parallel" frame) + this parallel set as a small alignment/eval slice.
  Building that is a separate, larger data effort and a separate cost-bearing GPU run.

## 5. Synthetic augmentation policy

- FLORES-200 is true 5-way parallel, so the default build is **0 % synthetic**.
- `build_trainset.py --synth-fill M` can top up M concepts via the subscription `claude`
  CLI (`claude -p`, NO API key — s14), with backoff 30/60/120/240s and flush-early
  (`synth_partial.json`). The manifest records `concepts_synthetic_claude` and
  `real_fraction` HONESTLY. Synthetic is for gap-fill toward a larger anchor target only;
  it does NOT change the full-pretrain feasibility verdict above.

## 6. Provenance / reproduce

```
curl -sL https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz -o flores200.tar.gz
tar xzf flores200.tar.gz
python3 scripts/build_trainset.py --raw flores200_dataset/<dev|devtest dir> --out OUT --split both
python3 scripts/verify_corpus.py OUT     # -> VERIFY: ALL-GREEN
```

HF: corpus shards uploaded to `dancinlab/clm-h911-trainset-5lang-parallel` (dataset, PRIVATE).
Builders + pilot + this manifest are committed to the repo; the full ~4MB `.limen` shards
live on HF (not committed) per the "no large raw blobs in git" constraint.
