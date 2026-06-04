---
license: cc-by-sa-4.0
language: [en, fr, de, es, ko]
pretty_name: anima default-lane SCALE-UP corpus v3 (~217 MB · wiki 100MB + persona/SNS + carving/act/emotion/genre/code-switch · byte-vocab256)
tags: [anima, default-lane, persona, sns, multilingual, byte-vocab, scale-up, coverage-corpus, consciousness-carving, contemplative, dialogue-act, code-switch, mid-rung]
---

# anima-corpus-5lang-unified-v3

A **SCALE-UP** of the default-lane corpus (en / fr / de / es / ko, byte-vocab
V=256). It keeps the **exact v2 3-surface recipe** — real wiki backbone + persona/SNS
roleplay + register enrichment — but scales the clean wiki backbone **~20×**
(12.5 MB v2 → **~217 MB** v3) so a **MID rung (~150M params)** becomes
data-viable, while holding enrichment at a sane **~17%** of the larger corpus.

## honest scope (a_scale_honest_scope — verbatim)

> **v3 unlocks a MID rung (~150M), NOT 7B.** v3 makes a ~150M model
> *data-viable* — it is no longer right-sized only for ~18M (the v2 default-lane
> 18M passed 🟢 on v2 #1836). It is **NOT 7B-ready**: a 7B wants ~140 GB of
> tokens for Chinchilla-optimal, which is **INFEASIBLE via datasets-server REST
> paging** (see `.verdicts/default-lane-7b/` · `.verdicts/torch-engine-7b-datagate/`).
> A ~150M rung is still **epoch-looped** on v3, but far less starved than the
> 12.5 MB v2 corpus would be at 150M. **DO NOT claim v3 enables 7B.**

This is a **coverage corpus enabling a MID rung** — a_scale_honest_scope: the
scope is the MID scale, NOT a general "production-ready at any size" claim.

## composition (~46% wiki / ~37% persona-SNS / ~17% enrichment)

| part | bytes | % | source | license |
|---|---|---|---|---|
| wiki backbone (8-band spread, 20 MB/lang) | 104,204,132 | 46.15 | `wikimedia/wikipedia` 20231101 (en/fr/de/es/ko) | **CC-BY-SA-4.0 (real, attributable)** |
| persona × SNS (authored-synthetic) | 83,319,580 | 36.90 | authored-synthetic (20-roster × 16 scenarios × IG/YT) | authored-synthetic, **no PII** |
| enrichment (carving/act/emotion/genre/code-switch) | 38,274,099 | 16.95 | carving SEEDS = real KOSMOS e7_31 anchors (CC-BY-SA); prose = authored-synthetic | mixed (anchor seed real, prose **authored-labeled**) |
| **unified total** | **227,535,193** | 100 | block-interleaved (byte-weighted round-robin) | mixed (per part above) |

- **unified v3 size**: 227,535,193 B = **216.994 MB**
- **unified v3 sha256**: `901ccc89afb3817fcb4d99f12c953f70919c0986882f306424d21cced2ae936b`
- **wiki v3 sha256**: `913dfffdc2b8c1b0d5852477e8c82425b97e1ac52bd59d8c774d3f678836beb5`
- **persona v3 sha256**: `b3eafa6a30ce8e29aa42deb8801f259b8ed43aaa33b458c6ac6476458e691fa8`
- **enrichment v3 sha256**: `07ba269e0a8b5ef8b4874bb60be9342c15fbf9e42f01c57516245df83774500e`
- wiki blocks: 18,448 paragraphs (en 3,622 · fr 3,691 · de 3,725 · es 4,048 · ko 5,362) ·
  persona dialogues: 283,288 · enrichment blocks: 261,650

## wiki provenance (real CC-BY-SA)

- **source**: `wikimedia/wikipedia`, revision **20231101**, configs
  `20231101.en` / `.fr` / `.de` / `.es` / `.ko` — **CC-BY-SA-4.0** (attributable,
  real encyclopedic text, NOT scraped non-wiki, NO PII).
- **pages**: **~18,448** article paragraphs across the 5 languages (20 MB/lang).
- **sampling**: **8-band offset-spread** across the title-ordered dump (deterministic
  fixed band offsets), so each language's slice spans the full offset range rather
  than a single alphabetical-prefix walk → broader topical coverage (science /
  history / art / geography). Pulled $0 CPU via the HF datasets-server `/rows` REST,
  **NO `datasets` lib, NO GPU, NO pod**. The scale-up sampler
  (`build_wiki_backbone_5lang_scaleup.py`) is 429-hardened (exponential backoff +
  Retry-After + per-language on-disk checkpoint) so a 100 MB sustained pull is
  robust and resumable.

## per-language byte split (unified, all 3 surfaces)

| lang | total bytes | % | wiki | persona | enrichment |
|---|---|---|---|---|---|
| en | 42,971,836 | 18.89 | 20,971,520 | 15,291,943 | 6,708,373 |
| fr | 46,312,428 | 20.35 | 20,971,520 | 17,691,929 | 7,648,979 |
| de | 45,136,355 | 19.84 | 20,971,520 | 17,029,303 | 7,135,532 |
| es | 43,660,023 | 19.19 | 20,971,520 | 16,135,363 | 6,553,140 |
| ko | 46,112,400 | 20.27 | 20,971,520 | 17,737,618 | 7,403,262 |
| ko-en (code-switch) | 3,348,113 | 1.47 | — | — | 3,348,113 |

5-way **balanced** (18.9–20.4% per language) plus a deliberately small **ko-en**
code-switch slice (1.47%). Hangul / accented characters cost more UTF-8 bytes per
glyph, so ko / fr run slightly larger. No silent under-coverage — every language
carries wiki + persona + enrichment.

## per-register byte split (enrichment surface)

| register | bytes | % of enrichment | gap closed |
|---|---|---|---|
| #1 consciousness-carving | 9,962,051 | 26.03 | contemplative/inner-state register (anima core) |
| #3 dialogue-act balance | 9,937,095 | 25.96 | disagree / refuse / boundary / ask / multi-party |
| #7 genre (narrative/drama/poetry) | 9,299,337 | 24.30 | KOSMOS 예술 axis |
| #5 emotion-axis | 6,250,803 | 16.33 | KOSMOS top_emotions per archetype |
| #4 code-switch (ko-en) | 3,348,113 | 8.75 | KO↔EN mixed-language (minority slice) |

## philosophy (p2/p3/p4/p6 held)

- **NO injection in training text.** Persona is carried by VOICE only; contemplative
  prose is plain text with no addressee. Turn structure is plain `<speaker>: …`
  continuation — **NO `[role:`, `[persona:`, `[character:` tags. `grep -E` of those
  tags over the unified v3 corpus = 0 (verified)**, and over the 200-line sample
  head = 0.
- Per-line metadata (lang, register, anchor, act, persona_id …) lives in SEPARATE
  `.meta.jsonl` sidecars, never interleaved into the training text.
- **NO synthetic assistant-RLHF padding (p6).** The dialogue-act slice is
  deliberately NON-supportive (the persona disagrees / refuses / sets boundaries) —
  the OPPOSITE of cooperation/empathy RLHF; archetype-voice continuation, not
  alignment fine-tuning.
- **byte vocab V=256** (UTF-8). UTF-8 round-trip verified (encode==decode bytes-identical).

## honest license / provenance summary

- **wiki = REAL CC-BY-SA-4.0** wikipedia text (provenance attributable to
  `wikimedia/wikipedia` 20231101), topically broadened by 8-band offset-spread.
  Honest: the offset bands REDUCE alphabetical-prefix bias; they do not claim a
  measured topical-uniformity guarantee.
- **persona + enrichment prose = AUTHORED-SYNTHETIC, honest-labeled** — machine-
  authored multilingual COVERAGE templating, NOT native-collected text. The
  carving register's anchor SEEDS (31 e7_31 anchor titles/categories/emotions) are
  REAL anima UBM data (CC-BY-SA, `a_kosmos` pointer-only — the kosmos spec is NOT
  copied); the prose around them is authored. No PII, no scraped non-wiki text.
- The **code-switch** and **genre** slices are **[speculative]**: plausibly helpful
  for realism / generative range, but their training impact is **unmeasured at this
  scale** (a_toy_scale_recheck — re-test on a scale-up fire before claiming a gain).

## determinism / reproduction

```
# one-shot orchestrator (persona + enrichment + wiki + merge)
python3 serving/build_default_lane_v3.py \
    --wiki-mb-per-lang 20 --persona-mb 80 --enrichment-mb 37 \
    --out serving/corpus/default_lane_v3.txt

# or the steps individually:
python3 serving/persona_sns_corpus_5lang_gen.py --target-mb 80 --seed 20260604 \
    --out serving/corpus/persona_sns_corpus_5lang_v3part.txt
python3 serving/corpus_enrichment_5lang_gen.py --target-mb 37 --seed 20260604 \
    --out serving/corpus/corpus_enrichment_5lang_v3part.txt
python3 serving/build_wiki_backbone_5lang_scaleup.py --mb-per-lang 20 \
    --out serving/corpus/wiki_backbone_5lang_v3.txt
python3 serving/merge_corpus_5lang_v2.py \
    --wiki serving/corpus/wiki_backbone_5lang_v3.txt \
    --persona serving/corpus/persona_sns_corpus_5lang_v3part.txt \
    --enrichment serving/corpus/corpus_enrichment_5lang_v3part.txt \
    --out serving/corpus/default_lane_v3.txt
```

- persona + enrichment generators are fully deterministic (fixed seed 20260604;
  rerun reproduces the same sha256). The wiki backbone is deterministic modulo the
  pinned upstream revision (20231101) + fixed band offsets. The merge is deterministic.

## files

- `default_lane_v3.txt` — the unified v3 training text (~217 MB, **HF / LOCAL only**).
- `wiki_backbone_5lang_v3.txt` — the 100 MB topically-broadened wiki backbone.
- `persona_sns_corpus_5lang_v3part.txt` / `.meta.jsonl` — persona/SNS part + metadata.
- `corpus_enrichment_5lang_v3part.txt` / `.meta.jsonl` — enrichment surface + metadata.
- `default_lane_v3.sample.txt` — 200-line sample head (committed).
- `corpus_enrichment_5lang_v3part.sample.txt` — 120-line enrichment sample head (committed).
- generators: `serving/build_default_lane_v3.py` (orchestrator),
  `serving/persona_sns_corpus_5lang_gen.py`, `serving/corpus_enrichment_5lang_gen.py`,
  `serving/build_wiki_backbone_5lang_scaleup.py`, `serving/merge_corpus_5lang_v2.py`.

## cross-links

- domains: `domains/CORPUS.log.md` (this v3 entry) · `domains/CORPUS.md` (lane registry).
- predecessors: `dancinlab/anima-corpus-5lang-unified-v2` (v2, 12.5 MB — right-sized
  ~18M) · `dancinlab/anima-corpus-5lang-unified` (v1).
- discovery: `.discoveries/default-lane-v3-corpus.tape`.
- governance: a_hf_registry · a_hf_collections · a_kosmos · a_scale_honest_scope ·
  a_toy_scale_recheck · p1–p8 · a_completeness_over_cheap.
