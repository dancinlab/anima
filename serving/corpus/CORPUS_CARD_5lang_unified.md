---
license: cc-by-sa-4.0
language: [en, fr, de, es, ko]
pretty_name: anima 5-lang UNIFIED corpus (wiki + SNS + persona, byte-vocab256)
tags: [anima, persona, sns, multilingual, byte-vocab, unified, coverage-corpus]
---

# anima-corpus-5lang-unified

A **UNIFIED 5-language** training corpus that combines a clean encyclopedic
**wiki backbone** with the **persona × SNS** roleplay surface, so a single
byte-level model is multilingual across ALL surfaces (wiki + SNS + persona) in
**en / fr / de / es / ko**. This closes the CORPUS-domain gap where 5-lang
coverage previously lived ONLY in the wiki/chat corpus and the persona/SNS
corpus was Korean-only.

This corpus feeds a FUTURE 5-lang 7B retrain (separate from the current
KR-persona 7B). It is byte-vocab V=256 (UTF-8) throughout.

## composition (~50% wiki / ~50% persona-SNS)

| part | bytes | % | source | license |
|---|---|---|---|---|
| wiki backbone | 5,218,193 | 50.05 | `wikimedia/wikipedia` 20231101 (en/fr/de/es/ko) | CC-BY-SA-4.0 (real, attributable) |
| persona × SNS | 5,207,508 | 49.95 | authored-synthetic (deterministic templates, 20-roster × 16 scenarios × IG/YT) | authored-synthetic, no PII, no scraped data |
| **unified total** | **10,485,747** | 100 | block-interleaved (byte-weighted round-robin) | mixed (per part above) |

- **unified sha256**: `ac6ed840319c503b3045ec997015bd396ecacf58681f79f47fe8d1082adcd995`
- **wiki backbone sha256**: `497df619b2c952d5dce158bff990157619dbb8066083f6ae3212312a0811819c`
- **persona×SNS sha256**: `1e5a062a5fe216a24ffe8230714d6bc9eb760ac9f3e18eec9326858e659866ba`
- wiki blocks: 12,268 · persona dialogues: 17,755

## per-language byte split (unified, wiki + persona)

| lang | total bytes | % | wiki | persona |
|---|---|---|---|---|
| en | 2,007,387 | 19.14 | 1,048,576 | 958,811 |
| fr | 2,153,045 | 20.53 | 1,048,576 | 1,104,469 |
| de | 2,115,603 | 20.18 | 1,048,576 | 1,067,027 |
| es | 2,057,230 | 19.62 | 1,048,576 | 1,008,654 |
| ko | 2,152,632 | 20.53 | 1,048,575 | 1,104,057 |

5-way **balanced** (19.1–20.5% per language). The wiki backbone is exactly
1 MB/lang; the persona slice rounds-robins uniformly across languages, with ko /
fr running slightly larger because Hangul / accented characters cost more UTF-8
bytes per glyph. No silent under-coverage — every language carries both surfaces.

## dialogue fraction

- ~49.95% of bytes are multi-turn **dialogue** (persona × SNS, 3–8 turns each).
- ~50.05% is encyclopedic **wiki** prose (non-dialogue backbone).

## philosophy (p2/p3/p4/p6 held)

- **NO injection in training text.** Persona is carried by VOICE only. Turn
  structure is plain `<follower>: … / <persona_name>: …` continuation — NO
  `[role:`, `[persona:`, `[character:` tags. `grep` of those tags over the
  unified corpus = **0** (verified).
- Per-dialogue metadata (lang, persona_id, platform, scenario, n_turns) lives in
  a SEPARATE `.meta.jsonl` sidecar, never interleaved into the training text.
- **NO synthetic assistant-RLHF padding (p6).** The persona lines are authored
  archetype-voice templates, not cooperation/empathy fine-tuning.

## honest scope (a_scale_honest_scope · a_lane_akida_gpu_split N/A)

- The **wiki** part is REAL CC-BY-SA wikipedia text (provenance attributable).
- The **persona × SNS** part is **machine-authored multilingual templates** — a
  COVERAGE corpus, **NOT native-collected** text. The en/fr/de/es lines are
  authored translations/paraphrases of each archetype's voice (e.g. knight =
  formal/archaic in every language; ice_queen = cold/sharp), not native-speaker
  corpora. This is a deliberate coverage scaffold so the 5-lang model has a
  consistent persona surface in every language; native-collected persona data
  would be a stronger follow-on, not a claim made here.
- Why a fresh backbone (not `clm-backbone-5lang-sample`): that dataset is
  ko/en/zh/ru/ja (mC4), off-axis for the en/fr/de/es/ko persona set, and its ko
  C4 slice contains NSFW/spam web text. This corpus rebuilds a clean, on-axis
  wiki backbone from `wikimedia/wikipedia` instead (completeness-bar re-design,
  a_completeness_over_cheap).

## determinism / reproduction

```
# 1. persona × SNS (5MB, seed 20260604 → identical sha on rerun)
python3 serving/persona_sns_corpus_5lang_gen.py --target-mb 5.0 \
    --out serving/corpus/persona_sns_corpus_5lang.txt

# 2. wiki backbone (1MB/lang, wikimedia/wikipedia 20231101 via datasets-server REST)
python3 serving/build_wiki_backbone_5lang.py \
    --out serving/corpus/wiki_backbone_5lang.txt --mb-per-lang 1.0

# 3. merge → unified (~50/50, deterministic block-interleave)
python3 serving/merge_corpus_5lang_unified.py
```

- The persona generator is fully deterministic (fixed seed; re-run reproduces the
  same sha256 — verified). The wiki backbone is deterministic modulo the pinned
  upstream dataset revision (date 20231101). The merge is deterministic.

## roster (the 20 personas, archetype voice carried across all 5 langs)

J-anime (0–9): school_idol · senpai · knight · sorceress · noir_detective ·
horror_whisper · childhood_friend · demon_lord · childlike · stoic_mentor.
Korean-webtoon (10–19): ice_queen · chaebol_heir · pure_heroine · tsundere_oppa ·
airhead_friend · charismatic_prez · thug_returnee · cold_heiress · gentle_oppa ·
fallen_antagonist. Voice SSOT = `HEXAD/VOICE/anima-voice/rp_voice_profiles.hexa`.

## 16 scenarios × {Instagram, YouTube}

팬DM칭찬 · 위로 · 일상잡담 · 고민상담 · 셀카리액션 · 댓글답글 · 라이브Q&A ·
추천부탁 · 사과 · 축하 · 응원 · 질문답변 · 일상공유 · 팬아트반응 · 밤인사 ·
동기부여. Platforms: instagram_dm/comment/live_qna (~70%) · youtube_comment/
community (~30%).

## files

- `persona_sns_corpus_5lang_unified.txt` — the unified training text (HF only).
- `persona_sns_corpus_5lang.txt` / `.meta.jsonl` — persona part + metadata sidecar.
- `wiki_backbone_5lang.txt` — the clean wiki backbone.
- `persona_sns_corpus_5lang_unified.sample.txt` — 200-line sample head.
- generators: `serving/persona_sns_corpus_5lang_gen.py`,
  `serving/build_wiki_backbone_5lang.py`, `serving/merge_corpus_5lang_unified.py`.

## cross-links

- domains: `domains/CORPUS.md` (registry + coverage matrix) · `[[PERSONA]]` ·
  `[[SNS]]`. KOSMOS enrichment analysis: `domains/CORPUS-enrichment-analysis.md`.
- governance: a_hf_registry · a_hf_collections · a_kosmos · a_scale_honest_scope ·
  p2/p3/p4/p6 · a_completeness_over_cheap.
