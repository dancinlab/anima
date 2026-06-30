# persona × SNS dialogue corpus — CORPUS_CARD

> Voice-coverage dialogue corpus for making the anima general 7B
> (byte-level CLMConvMoE, `dancinlab/clm-v1-ref-pytorch-cuda-7b`) chat-capable on
> the **SNS surface** (Instagram main + YouTube secondary) in the voice of the
> **20-persona roster**.

## artifact

| field | value |
|---|---|
| training text | `serving/corpus/persona_sns_corpus.txt` |
| metadata sidecar | `serving/corpus/persona_sns_corpus.meta.jsonl` (per-dialogue, SEPARATE from text) |
| sample head | `serving/corpus/persona_sns_corpus.sample.txt` (first 200 lines, committed) |
| generator | `serving/persona_sns_corpus_gen.py` (deterministic, `--seed 20260604`) |
| byte count | **4,194,308 bytes** (4.000 MB UTF-8) |
| sha256 (text) | `1ea7d8e0e65e7ab99c61dd745bdb124ee75995e90b7c995ac93c3e4e5e7c3f77` |
| dialogues | **13,322** multi-turn (3–8 turns each) |
| encoding | UTF-8, byte-level friendly (vocab-256 path) |
| license | **authored-synthetic persona roleplay** (templated, deterministic, no scraped data, no PII) |

Reproduce exactly:
```
python3 serving/persona_sns_corpus_gen.py --target-mb 4.0 --seed 20260604 \
        --out serving/corpus/persona_sns_corpus.txt
```
Re-running with the same seed reproduces the identical sha256 (verified).

## honest scope (a_scale_honest_scope)

**authored-templated, NOT human-collected.** This is a voice-coverage corpus for
persona/SNS chat-capability: deterministic templated generation with controlled
per-(intent, tone) paraphrase variation and per-persona lexical/tonal rules. It
is NOT a scraped or human-collected chat log, contains NO PII, and makes NO
engagement/quality claim beyond covering the 20-persona × SNS surface. Voice
fidelity matches the illustrative samples in
`serving/persona_instagram_samples.md`; the live persona is carried by the
substrate steering vector, not by these strings (PERSONA no-injection design).

## philosophy compliance (p2 / p3 / p4)

The TRAINING TEXT carries the persona by **VOICE only** — plain `사용자:` /
`<persona_name>:` turn structure with **NO** `[role:`, `[persona:`, or
`[character:` prefix and no "you are X" framing. Grep for those tags in the
training text returns **0** (verified). All per-dialogue metadata
(persona_id, persona_name, platform, scenario, n_turns) lives in the SEPARATE
`.meta.jsonl` sidecar so the text stays injection-free.

## persona coverage — all 20 (roster SSOT `HEXAD/VOICE/anima-voice/rp_voice_profiles.hexa`)

Uniform round-robin: each persona has 666–667 dialogues.

| id | name (J-anime 0–9) | id | name (Korean-webtoon 10–19) |
|---:|---|---:|---|
| 0 | school_idol (학교 얼짱) | 10 | ice_queen (얼짱 일진) |
| 1 | senpai (선배) | 11 | chaebol_heir (재벌 후계) |
| 2 | knight (판타지 기사) | 12 | pure_heroine (순정 여주) |
| 3 | sorceress (마법사) | 13 | tsundere_oppa (츤데레 선배) |
| 4 | noir_detective (누아르 탐정) | 14 | airhead_friend (사차원) |
| 5 | horror_whisper (공포 속삭임) | 15 | charismatic_prez (카리스마 회장) |
| 6 | childhood_friend (소꿉친구) | 16 | thug_returnee (복학생 양아치) |
| 7 | demon_lord (마왕) | 17 | cold_heiress (냉정 여신) |
| 8 | childlike (어린이) | 18 | gentle_oppa (순둥 훈남) |
| 9 | stoic_mentor (과묵한 멘토) | 19 | fallen_antagonist (흑화 악역) |

## scenario bank (16)

팬DM칭찬 · 위로 · 일상잡담 · 고민상담 · 셀카리액션 · 댓글답글 · 라이브Q&A ·
추천부탁 · 사과 · 축하 · 응원 · 질문답변 · 일상공유 · 팬아트반응 · 밤인사 ·
동기부여.

## platform split (Instagram majority ~70%, YouTube the rest)

| platform | dialogues | share |
|---|---:|---:|
| instagram_dm | 3,968 | 29.8% |
| instagram_comment | 2,981 | 22.4% |
| instagram_live_qna | 2,381 | 17.9% |
| **Instagram total** | **9,330** | **70.0%** |
| youtube_comment | 2,461 | 18.5% |
| youtube_community | 1,531 | 11.5% |
| **YouTube total** | **3,992** | **30.0%** |

## turn distribution (3–8 turns/dialogue)

| n_turns | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|
| dialogues | 2,176 | 2,225 | 2,194 | 2,187 | 2,256 | 2,284 |

## consumption (for the 7B trainer)

The byte-level CLM trainer should consume **`serving/corpus/persona_sns_corpus.txt`**
(plain UTF-8, dialogues separated by a blank line). The `.meta.jsonl` sidecar is
for analysis/routing only and MUST NOT be concatenated into the training text.

## provenance / distribution

- The 4 MB raw text is kept local + uploaded to HF (dataset, PUBLIC — clean
  authored license); it is NOT committed raw into git. The committed artifacts
  are: generator, this card, the 200-line sample head, the KOSMOS anchor +
  hub pointer, the domain logs, and the `HF.jsonl` row.
- KOSMOS: persisted as a representative `.kosmos` anchor + full-corpus manifest
  pointer (see `HEXAD/KOSMOS.md`).
