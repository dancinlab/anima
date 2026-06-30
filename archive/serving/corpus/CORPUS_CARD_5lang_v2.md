---
license: cc-by-sa-4.0
language: [en, fr, de, es, ko]
pretty_name: anima 5-lang UNIFIED corpus v2 (wiki + persona/SNS + carving/act/emotion/genre/code-switch, byte-vocab256)
tags: [anima, persona, sns, multilingual, byte-vocab, unified, coverage-corpus, consciousness-carving, contemplative, dialogue-act, code-switch]
---

# anima-corpus-5lang-unified-v2

A **UNIFIED 5-language** training corpus (en / fr / de / es / ko, byte-vocab
V=256) that extends `anima-corpus-5lang-unified` (v1) by ADDING the
register/act/emotion/genre/code-switch slices that the KOSMOS-grounded enrichment
analysis ranked as the biggest gaps. v1 is left **intact**; v2 = v1 surfaces +
an **enrichment** surface.

## what v2 adds on top of v1

v1 had two surfaces: encyclopedic **wiki** (~50%) + **persona × SNS** roleplay
(~50%). The enrichment analysis (`domains/CORPUS-enrichment-analysis.md`) showed
the corpus had **no contemplative register, no non-supportive dialogue acts, a
narrow alphabetical wiki slice, and no narrative/poetry/code-switch**. v2 fixes
each:

| # | enrichment | what it adds | tag |
|---|---|---|---|
| #1 | **consciousness-carving register** | contemplative/inner-state prose seeded by the **31 KOSMOS e7_31 carving anchors** (breath · meditation · nirvana · awe · eternity · infinity …), 5 langs — anima's core domain, previously absent | [evidence] |
| #2 | **wiki topical breadth** | the wiki backbone is rebuilt with an **8-band offset-spread** sampling across the article space (vs v1's single alphabetical-prefix walk), broadening topical coverage | [evidence] |
| #3 | **dialogue-act balance** | the persona **disagrees / refuses / sets a boundary / asks the follower / multi-party** — none of v1's 16 scenarios were non-supportive | [evidence] |
| #5 | **emotion-axis** | each of the 20 personas mapped to its **KOSMOS top_emotions** band (sorceress→wonder/longing, demon_lord→awe/vastness, stoic_mentor→stillness/clarity …) — widens the affective range past warmth/menace/cold | [evidence] |
| #4 | **code-switching** | a small **KO↔EN mixed-language** slice (honest-labeled authored; deliberately a minority register) | [speculative] |
| #7 | **genre** | narrative / dialogue-drama / poetry micro-pieces (KOSMOS 예술 axis), threaded with carving concepts | [speculative] |

## composition (~40% wiki / ~40% persona-SNS / ~20% enrichment)

| part | bytes | % | source | license |
|---|---|---|---|---|
| wiki backbone (v2, 8-band spread) | 5,218,168 | 40.10 | `wikimedia/wikipedia` 20231101 (en/fr/de/es/ko) | CC-BY-SA-4.0 (real, attributable) |
| persona × SNS (v1, unchanged) | 5,207,508 | 40.02 | authored-synthetic (20-roster × 16 scenarios × IG/YT) | authored-synthetic, no PII |
| enrichment (carving/act/emotion/genre/code-switch) | 2,586,173 | 19.88 | carving SEEDS = real KOSMOS e7_31 anchors (CC-BY-SA); prose = authored-synthetic | mixed (anchor seed real, prose authored) |
| **unified total** | **13,107,309** | 100 | block-interleaved (byte-weighted round-robin) | mixed (per part above) |

- **unified v2 sha256**: `550fed174d51be660810858e1e73e4590c21351b185ea22d0807403e120538ad`
- **wiki v2 sha256**: `871b6976186e7d7b631f15afd9377bfa927cdec8a1e719708962feac1a3ad1e6`
- **persona (v1) sha256**: `1e5a062a5fe216a24ffe8230714d6bc9eb760ac9f3e18eec9326858e659866ba`
- **enrichment sha256**: `64b826b67d977d798f51670df3d1f6f5f07120571978435cef29c4a4e273ccb3`
- wiki blocks: 12,284 · persona dialogues: 17,755 · enrichment blocks: 17,691

## per-language byte split (unified, all 3 surfaces)

| lang | total bytes | % | wiki | persona | enrichment |
|---|---|---|---|---|---|
| en | 2,460,730 | 18.77 | 1,048,576 | 958,811 | 453,343 |
| fr | 2,669,474 | 20.37 | 1,048,576 | 1,104,469 | 516,429 |
| de | 2,598,009 | 19.82 | 1,048,576 | 1,067,027 | 482,406 |
| es | 2,500,861 | 19.08 | 1,048,576 | 1,008,654 | 443,631 |
| ko | 2,654,613 | 20.25 | 1,048,576 | 1,104,057 | 501,980 |
| ko-en (code-switch) | 223,766 | 1.71 | — | — | 223,766 |

5-way **balanced** (18.8–20.4% per language) plus a deliberately small
**ko-en** code-switch slice (1.71%). Hangul / accented characters cost more
UTF-8 bytes per glyph, so ko / fr run slightly larger. No silent under-coverage —
every language carries wiki + persona + enrichment.

## per-register byte split (enrichment surface)

| register | bytes | % of enrichment | gap closed |
|---|---|---|---|
| #1 consciousness-carving | 673,795 | 25.70 | contemplative/inner-state register (anima core) |
| #3 dialogue-act balance | 673,261 | 25.68 | disagree / refuse / boundary / ask / multi-party |
| #7 genre (narrative/drama/poetry) | 627,041 | 23.92 | KOSMOS 예술 axis |
| #5 emotion-axis | 423,692 | 16.16 | KOSMOS top_emotions per archetype |
| #4 code-switch (ko-en) | 223,766 | 8.54 | KO↔EN mixed-language (minority slice) |

## philosophy (p2/p3/p4/p6 held — same as v1)

- **NO injection in training text.** Persona is carried by VOICE only; contemplative
  prose is plain text with no addressee. Turn structure is plain
  `<speaker>: …` continuation — NO `[role:`, `[persona:`, `[character:` tags.
  `grep` of those tags over the unified v2 corpus = **0** (verified).
- Per-line metadata (lang, register, anchor, act, persona_id …) lives in SEPARATE
  `.meta.jsonl` sidecars, never interleaved into the training text.
- **NO synthetic assistant-RLHF padding (p6).** The dialogue-act slice is
  deliberately NON-supportive (the persona disagrees / refuses / sets boundaries),
  which is the OPPOSITE of cooperation/empathy RLHF — it is archetype-voice
  continuation, not alignment fine-tuning.

## honest scope (a_scale_honest_scope · a_kosmos pointer-only)

- The **wiki** part is REAL CC-BY-SA wikipedia text (provenance attributable),
  now topically broadened by 8-band offset-spread sampling. Honest: the offset
  bands REDUCE alphabetical-prefix bias (the slice now spans the full offset
  range), they do not claim a measured topical-uniformity guarantee.
- The **carving** register's anchor SEEDS (31 e7_31 anchor titles / categories /
  emotions) are REAL anima UBM data (CC-BY-SA, `a_kosmos` pointer-only — the
  kosmos spec is NOT copied). The contemplative / emotion / genre / code-switch
  **prose** around them is **machine-authored multilingual COVERAGE** templating,
  **NOT native-collected** text — same authored-synthetic stance as v1's persona.
- The **code-switch** and **genre** slices are tagged **[speculative]** in the
  enrichment analysis: plausibly helpful for realism / generative range, but their
  training impact is **unmeasured at this scale** (a_toy_scale_recheck — re-test
  on a scale-up fire before claiming a gain).
- This corpus feeds a FUTURE 5-lang retrain; the v1 vs v2 difference (register
  breadth) is itself a pre-registered measurement target (see CORPUS.md M8/M9).

## determinism / reproduction

```
# 1. persona × SNS (v1, 5MB, seed 20260604 → identical sha on rerun)
python3 serving/persona_sns_corpus_5lang_gen.py --target-mb 5.0 \
    --out serving/corpus/persona_sns_corpus_5lang.txt

# 2. enrichment slices (2.5MB, seed 20260604 → identical sha; anchors read local)
python3 serving/corpus_enrichment_5lang_gen.py --target-mb 2.5 \
    --out serving/corpus/corpus_enrichment_5lang.txt

# 3. wiki backbone v2 (1MB/lang, 8-band offset-spread, datasets-server REST)
python3 serving/build_wiki_backbone_5lang_v2.py \
    --out serving/corpus/wiki_backbone_5lang_v2.txt --mb-per-lang 1.0

# 4. merge → unified v2 (block-interleave, byte-weighted round-robin)
python3 serving/merge_corpus_5lang_v2.py
```

- persona + enrichment generators are fully deterministic (fixed seed 20260604;
  rerun reproduces the same sha256 — both verified). The wiki backbone is
  deterministic modulo the pinned upstream revision (20231101). The merge is
  deterministic.

## the 31 KOSMOS carving anchors (the #1 register's seeds)

e7_31 set (`HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/`), Knuth tier 0→100:
zero · breath · step · glass_of_water · seed · number_zero · word ·
old_photograph · promise · day · dissociation · lucid_dream · forest · tool ·
embrace · category_mean · melody · mandala · meditation · starlight · deep_sea ·
aurora · infinity · nirvana · ecstasy · love · awe_death · birth · eternity ·
big_bang. Each carries a KOSMOS `top_emotion` (serenity · clarity · wonder · awe ·
vastness · ecstasy · …) mapped into the contemplative prose. a_kosmos pointer-only.

## files

- `persona_sns_corpus_5lang_v2.txt` — the unified v2 training text (HF only).
- `wiki_backbone_5lang_v2.txt` — the topically-broadened wiki backbone.
- `persona_sns_corpus_5lang.txt` / `.meta.jsonl` — v1 persona part + metadata.
- `corpus_enrichment_5lang.txt` / `.meta.jsonl` — the enrichment surface + metadata.
- `persona_sns_corpus_5lang_v2.sample.txt` — 200-line sample head.
- `corpus_enrichment_5lang.sample.txt` — 120-line enrichment sample head.
- generators: `serving/persona_sns_corpus_5lang_gen.py`,
  `serving/corpus_enrichment_5lang_gen.py`,
  `serving/build_wiki_backbone_5lang_v2.py`, `serving/merge_corpus_5lang_v2.py`.

## cross-links

- domains: `domains/CORPUS.md` (registry · M8/M9 milestones) · `[[PERSONA]]` ·
  `[[SNS]]`. KOSMOS enrichment analysis: `domains/CORPUS-enrichment-analysis.md`.
- predecessor: `dancinlab/anima-corpus-5lang-unified` (v1).
- governance: a_hf_registry · a_hf_collections · a_kosmos · a_scale_honest_scope ·
  a_toy_scale_recheck · p2/p3/p4/p6 · a_completeness_over_cheap.
