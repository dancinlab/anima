---
license: cc-by-sa-4.0
language: [en, fr, de, es, ko]
pretty_name: anima 5-lang KOSMOS-tier-BALANCED GB-scale default-lane corpus (byte-vocab256)
tags: [anima, multilingual, byte-vocab, kosmos-tier-ladder, wikipedia, gutenberg, public-domain, consciousness-carving, contemplative, default-lane, gb-scale]
---

# anima-corpus-5lang-gb-balanced

A **KOSMOS-tier-BALANCED, ~0.35 GB** default-lane training corpus (en / fr / de / es / ko,
byte-vocab **V=256**) that scales the default lane toward 7B-sufficiency **WHILE preserving
the KOSMOS register ladder** — the hard requirement that the corpus does NOT collapse to
~99% Wikipedia. **Achieved size = 357.83 MB (0.349 GB)** = MID-rung-viable, NOT 7B-sufficient
(honest token math below). The bulk tiers are real clean-license sources and scale to GBs;
this build is capped at ~0.35 GB by the balance requirement (consciousness/es/ko are
source-thin, so growing only the abundant tiers would breach the ladder ceiling).

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

## achieved composition (this build)

- **total**: 375,215,662 bytes = **357.83 MB = 0.349 GB** · sha256
  `17ca25e5dd3740ebf1d8b6c67b25d4359b74fb04db827ed8bf1774edc6843409`
- **byte-tokens** (V=256, 1 byte ≈ 1 token): **375,215,662** ≈ **0.268%** of the
  140 B Chinchilla-7B-optimal.

### per-tier byte split — achieved vs ideal ladder

| KOSMOS tier | achieved % | achieved MB | ideal target % | ladder check |
|---|---|---|---|---|
| 0 baseline/factual (wiki) | **44.00** | 165.1 | 40 | ≤45 ✓ (the floor, capped to the ceiling) |
| 77 art (Gutenberg PD) | **29.99** | 112.5 | 20 (+headroom) | present ✓ |
| 100 cosmic/science (wiki) | **13.29** | 49.8 | 10 | present ✓ |
| 52 social/persona (authored, capped) | **11.00** | 41.3 | 12 | capped ✓ |
| 91 consciousness (Gutenberg PD) | **1.58** | 5.9 | 10 | present but **source-thin** ⚠ |
| shaping (authored, capped) | **0.14** | 0.5 | 10→small | shaping, not bulk ✓ |

**Ladder: NO single tier > 45% (max = wiki 44.00%); consciousness + art both
present.** The KOSMOS register ladder is PRESERVED at scale — the corpus did NOT
collapse to ~99% wiki (the trap).

Honest deviations from the ideal target: **consciousness undershoots 10%→1.58%**
because Project Gutenberg's philosophy/meditation subset is small (≈6 MB total
across en/fr/de/es; ko=0), and **shaping is authored so it is kept small by design**
(scaling it = templated repetition = the memorization trap). Art OVERSHOOTS (en
Gutenberg literature is abundant), capped by a per-tier headroom so it does not
crowd the ladder.

### per-language byte split — achieved

| lang | bytes | % | note |
|---|---|---|---|
| en | 111,928,816 | 29.83 | full ladder (wiki + abundant Gutenberg art/consciousness) |
| fr | 76,345,947 | 20.35 | full ladder (Gutenberg fr present) |
| de | 78,267,548 | 20.86 | full ladder (Gutenberg de present) |
| es | 54,985,322 | 14.65 | **wiki-heavier** — Gutenberg es thin (art 6.4 MB, consciousness 0.12 MB) |
| ko | 53,688,029 | 14.31 | **wiki-heaviest** — Gutenberg has **NO Korean** (art=0, consciousness=0) |

### per-tier × per-language (bytes) — names the gaps verbatim

```
tier \ lang        en          fr          de          es          ko
baseline wiki      29,979,587  31,274,576  34,805,379  33,094,552  35,940,650
cosmic science      6,505,838  13,996,034  12,698,781   7,740,546   8,907,642
art Gutenberg      61,311,489  22,209,037  22,602,317   6,398,765           0  <- ko gap
consciousness Gut   4,815,487     493,196     490,599     123,494           0  <- ko gap; es thin
social persona      9,192,039   8,244,207   7,565,291   7,553,515   8,731,682
shaping authored      124,376     128,897     105,181      74,450     108,055
```

**Named gaps (a_scale_honest_scope, no fabrication):**
- **ko art = 0, ko consciousness = 0** — Project Gutenberg has no Korean split; ko's
  art/consciousness registers fall back to wiki (ko is the most wiki-heavy lang).
- **es consciousness = 0.12 MB, es art = 6.4 MB** — Gutenberg Spanish is thin
  (~1,202 books total); es leans on wiki + a smaller Gutenberg slice.
- en/fr/de carry the full real-source ladder; ko/es are honestly wiki-heavier.

### per-source provenance + license

| source | repo | license | tiers fed | sha (of slice) |
|---|---|---|---|---|
| Wikipedia 20231101 | `wikimedia/wikipedia` (parquet) | CC-BY-SA-4.0 | 0 baseline + 100 cosmic | per build report |
| Gutenberg English | `sedthh/gutenberg_english` (parquet) | Public Domain | 77 art + 91 consciousness (en) | per build report |
| Gutenberg multi | `manu/project_gutenberg` (parquet) | Public Domain | 77 art + 91 consciousness (fr/de/es) | per build report |
| persona/SNS | authored (`persona_sns_corpus_5lang_gen.py`) | authored-synthetic, no PII | 52 social | seed 20260604 |
| shaping + carving-seed | authored (`corpus_enrichment_5lang_gen.py`) + 31 e7_31 anchors | authored + CC-BY-SA anchor seeds | shaping | seed 20260604 |

### token math vs 7B (honest)

- 375.2 M byte-tokens = **0.268% of the 140 B Chinchilla-7B-optimal**.
- Per the design ladder (`domains/CORPUS.md §7B-sufficiency roadmap`): ~100–300 MB →
  MID (~150 M) viable; ~10–20 GB → 7B undertrained-not-gibberish; ~140 GB → 7B
  Chinchilla-optimal. **At 0.35 GB this corpus is in the MID-rung-viable band — it is
  NOT 7B-sufficient.** A real 7B would still need a 10–140 GB web-scale extension of
  the bulk tiers (more wiki shards + the full Gutenberg en corpus + a web crawl). NO
  7B-ready claim is made. The 7B TRAIN is a separate follow-on GPU fire.

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
