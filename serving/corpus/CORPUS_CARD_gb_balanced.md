---
license: cc-by-sa-4.0
language: [en, fr, de, es, ko]
pretty_name: anima 5-lang KOSMOS-tier-BALANCED GB-scale default-lane corpus (byte-vocab256)
tags: [anima, multilingual, byte-vocab, kosmos-tier-ladder, wikipedia, gutenberg, public-domain, consciousness-carving, contemplative, default-lane, gb-scale]
---

# anima-corpus-5lang-gb-balanced

A **GB-scale, KOSMOS-tier-BALANCED** default-lane training corpus (en / fr / de / es / ko,
byte-vocab **V=256**) that scales the default lane toward 7B-sufficiency **WHILE preserving
the KOSMOS register ladder** — the hard requirement that the corpus does NOT collapse to
~99% Wikipedia.

This is the GB implementation of the FINAL 7B composition design in `domains/CORPUS.md`
(§7B-sufficiency roadmap, #1850). Predecessor: `anima-corpus-5lang-unified-v2` (12.5 MB,
right-sized for 18M; data-starved at 7B).

## the balance trap and the fix

v2 balance was wiki **40.10%** / persona·dialogue **40.02%** / enrichment **19.88%**.
Naively scaling wiki to GB while keeping authored persona (40%) + enrichment (20%) at that
ratio = authoring **GBs of templated text** (the 20-roster persona, the 31 carving anchors)
= **MEMORIZATION** — in practice the only scalable axis is wiki, so the corpus drifts to
**~99% wiki** and the KOSMOS ladder is **DESTROYED**.

**The fix**: map each KOSMOS tier to a **REAL scalable clean-license source**; the 31 e7_31
carving anchors stay the consciousness-register **DEFINITION/seed**, FILLED at scale with
real Public-Domain contemplative text — **NOT repeated**. AUTHORED registers (persona/SNS +
the register-shaping slices) stay **CAPPED** — they define anima's identity-voice and shape
the distribution, they do not bulk-fill.

## tier → real source

| KOSMOS tier | source | license | role | scale |
|---|---|---|---|---|
| 0 baseline/factual | `wikimedia/wikipedia` 20231101 5-lang, multi-shard breadth | CC-BY-SA-4.0 | factual floor | GB |
| 100 cosmic/science | the same wiki, SQL science-keyword filtered | CC-BY-SA-4.0 | cosmic | 100s MB |
| 77 art | Gutenberg literature/poetry (PD) — `sedthh/gutenberg_english` en + `manu/project_gutenberg` fr/de/es | Public Domain | art | 100s MB (en≫fr/de≫es; ko=0) |
| 91 consciousness | Gutenberg philosophy/meditation/contemplative (PD) — the 31 e7_31 anchors DEFINE the register, FILLED with real PD text | Public Domain | 의식 register (#1 KOSMOS) | 100s MB |
| 52 social/daily | authored persona/SNS (20-roster × IG/YT), CAPPED | authored-synthetic, no PII | anima identity-voice | capped |
| shaping | authored dialogue-act + emotion + KO↔EN code-switch + genre + carving-seed def | mixed (anchor seed real, prose authored) | shape distribution | small |

<!-- BUILD_NUMBERS_START -->
_Achieved byte split, sha256, per-lang/per-tier tables, and the token-vs-7B line are
filled from the build report (`serving/corpus/_src/gb_balanced_report.json`) below._
<!-- BUILD_NUMBERS_END -->

## philosophy (p1..p6 held)

- **NO injection in training text.** Wiki + Gutenberg are plain text; persona is carried by
  VOICE only; contemplative prose has no addressee. Turn structure is plain `<speaker>:`
  continuation — NO `[role:` / `[persona:` / `[character:` tags. `grep` of those over the
  corpus = **0** (verified).
- **NO synthetic assistant-RLHF padding (p6).** The persona/SNS register is anima's
  identity-voice (honest-labeled authored COVERAGE), not cooperation/empathy fine-tuning;
  the dialogue-act slice is deliberately NON-supportive.
- **Control-byte clean**: 0xFE / 0xFF byte frequency = **0** (default lane has no tool
  sentinels). UTF-8 round-trip clean (V=256).

## honest scope (a_scale_honest_scope)

- **Per-lang availability DIFFERS and is reported verbatim, never fabricated.** Project
  Gutenberg has **0** Korean books and only ~1,202 Spanish vs ~48k English → **ko art +
  consciousness are absent from Gutenberg and fall back to wiki; es is thin**. Those langs
  are wiki-heavier; the per-lang/per-tier table below names the gaps.
- **Token math vs 7B.** Chinchilla-optimal 7B = 7e9 × 20 = **140B tokens ≈ 140 GB** byte-text.
  This corpus reaches the byte-token count reported below; the §finding states plainly what
  fraction of 7B-optimal that is. A real 7B may still need web-scale — **no 7B-ready claim** is
  made unless the token count AND the ladder balance genuinely support it.
- The **7B TRAIN is a separate follow-on GPU fire** (a_fire_autonomous) once this corpus exists.

## determinism / reproduction

```bash
# bulk tiers read HF parquet via duckdb httpfs (GB-scale, no REST 429); $0 CPU, no GPU
HF_TOKEN=$(secret get hf.token) bash serving/gb_balanced/build_all.sh
# knobs: MB_T0 MB_T100 MB_ART MB_CON SHAPING_MB PERSONA_MB
```

- `fetch_wiki_tiers.py` (t0 + t100) and `fetch_gutenberg_tiers.py` (t77 + t91) are
  deterministic modulo the pinned upstream revisions; the authored generators
  (`corpus_enrichment_5lang_gen.py`, `persona_sns_corpus_5lang_gen.py`) are seed-deterministic;
  `balance_merge.py` (dedup + ladder + UTF-8 round-trip + accounting) is deterministic.

## the 31 KOSMOS carving anchors (the #1 register's definition/seed)

e7_31 set (`HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/`, Knuth tier 0→100): zero · breath ·
step · glass_of_water · seed · word · promise · meditation · starlight · aurora · infinity ·
nirvana · ecstasy · awe_death · eternity · big_bang … Each carries a KOSMOS `top_emotion`.
At GB scale they DEFINE the consciousness register; the **bulk** of tier-91 is REAL
Public-Domain contemplative text. a_kosmos pointer-only.

## files

- `serving/corpus/default_lane_gb_balanced.txt` — the merged training text (HF-only, gitignored).
- `serving/gb_balanced/{fetch_wiki_tiers,fetch_gutenberg_tiers,balance_merge}.py` + `build_all.sh`.
- `serving/corpus/default_lane_gb_balanced.head.txt` — committed sample head.
- `serving/corpus/_src/gb_balanced_report.json` — the achieved-split build report.

## cross-links

- `domains/CORPUS.md` (registry · §7B-sufficiency roadmap · §KOSMOS balance at scale).
- predecessors: `dancinlab/anima-corpus-5lang-unified-v2` (12.5 MB) · `…-unified` (v1).
- governance: a_hf_registry · a_hf_collections · a_kosmos · a_scale_honest_scope ·
  a_completeness_over_cheap · p1..p6.
