# chat-capable dialogue-mix byte corpus — CORPUS CARD

substrate-agnostic dataset card · g63 honest provenance · a_scale_honest_scope · 2026-06-04
Lane-G/torch-cuda reference lane (a_lane_akida_gpu_split — NOT AKIDA).

## what this is

`chat_corpus_mix` — a 70%-wiki / 30%-REAL-dialogue **byte-level** (vocab 256) corpus for the
chat-capable LADDER rung-0 (≈18M byte transformer). The 30% dialogue bucket is REAL multi-turn
conversation reformatted into the PROVEN byte-level continuation format `사용자: <u> | 도우미: <a>`
(the same mechanism that made the prior byte chat rung PASS). This is learned continuation
conditioning, **NOT** a system prompt / persona / identity rule / RLHF template (p1·p2·p3·p4·p6).

- builder: `training/build_chat_corpus.py` (deterministic, no RNG, idempotent on identical sources)
- out: `state/chat_corpus_mix/chat_corpus_mix.txt` (gitignored — >stdlib size; HF dataset on ship)
- total bytes: **3,766,315**
- sha256: `05179fb6684d41e4cefa928fe1c24683294c17997666eed5c03a00480e5acb70`
- vocab: byte (256)
- ratio: **70.01% wiki / 29.99% dialogue** (by bytes)
- n_conversations (dialogue bucket): **2,310** multi-turn (≥2 turns each)

## sources (all local, REAL, honest provenance — NO synthetic RLHF padding, p6)

| role | source path | provenance | synthetic? |
|------|-------------|------------|------------|
| dialogue (30%) | `data/corpus.txt` | REAL KO/EN multi-turn conversations (consciousness · work · daily themes), A:/B: speaker-turn format, blank-line-separated. Reformatted A:→`사용자:`, B:→`도우미:`, turns joined by ` \| `, one conversation per line. | **no** |
| wiki (70%, a) | `CORE/testdata/clm_mid_5lang_c4.txt` | 5-language aphorisms (en·zh·ru·ja·ko), the backbone the d768 production model trained on. | no |
| wiki (70%, b) | `data/.corpus_cache/.corpus_cache/ko_wiki.txt` | Korean Wikipedia prose. | no |

## honesty lines (CRITICAL)

- **NO synthetic assistant-RLHF padding** (p6). The dialogue is real human/model conversation text,
  not generated instruction-tuning pairs. The `사용자:/도우미:` markers are byte-continuation
  CONDITIONING (the model learns to continue the bytes it sees), not injected role instructions.
- **Provenance scope**: `data/corpus.txt` is the project's own real conversation corpus (KO/EN mix on
  consciousness / engineering / daily topics). A downstream claim needing a specific clean-license
  external dump (OpenSubtitles / wiki-talk) MUST re-source; this rung uses the project-local real
  dialogue that was already present and license-clean for project use.
- **Construction**: PATH-B-1 concat (wiki block first, then dialogue block); training-time shuffle
  recovers interleave. Reproducible via `build_chat_corpus.py`.

## ratio derivation

dialogue is the anchor (scarcer, higher-value bucket): wiki backbone truncated at a UTF-8 boundary to
`dialogue_bytes * 70/30`. Result lands 70.01/29.99 by bytes (drift < 0.02 pp).
