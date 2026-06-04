# SNS — step log (append-only)

> Snapshot/state = `domains/SNS.md`. This file = append-only step log.

## 2026-06-04 — persona × SNS dialogue corpus (Instagram main + YouTube secondary)

- **what**: dialogue corpus covering the SNS publishing surface
  (Instagram main + YouTube secondary) in the [[PERSONA]] 20-roster voice, to
  make the anima general 7B chat-capable on that surface. Platform formats:
  `instagram_dm`, `instagram_comment`, `instagram_live_qna`, `youtube_comment`,
  `youtube_community`.
- **platform split**: Instagram **MAJORITY ~70%** (9,330 dialogues:
  dm 3,968 / comment 2,981 / live_qna 2,381), YouTube the rest **~30%**
  (3,992: comment 2,461 / community 1,531). Total 13,322.
- **generator**: `serving/persona_sns_corpus_gen.py` (deterministic, seed
  20260604, $0 CPU, no network/PII). Corpus
  `serving/corpus/persona_sns_corpus.txt` = 4.0 MB, sha256 `1ea7d8e0…`.
- **design stance preserved**: the corpus carries persona by VOICE, never a
  role-tag prefix (p2/p3/p4; grep `[role:`/`[persona:`/`[character:` = 0). The
  persona on a post = the substrate steering vector, not a prompt prefix
  (SNS.md design stance). Metadata kept in a separate `.meta.jsonl` sidecar.
- **honest scope**: authored-templated voice-coverage corpus, NOT
  human-collected and NOT a fabricated engagement log (a_scale_honest_scope;
  SNS.md M4 honest-provenance stance).
- **KOSMOS**: representative anchor `persona_sns_corpus.kosmos` (tier 52) +
  hub pointer in `HEXAD/KOSMOS.md` (pointer-only).
- **HF**: dataset `dancinlab/anima-persona-sns-corpus` (PUBLIC, sha256-verified).
  `HF.jsonl` row appended. card: `serving/corpus/CORPUS_CARD.md`.
- **relates to milestone**: SNS.md M4 (per-persona consistency / honest
  provenance) — voice-coverage corpus for the 20 roster on the SNS surface.
- cross-link: [[PERSONA]] (the no-injection roster mechanism this surface voices).

## 2026-06-04 — STAGE-2: SNS-surface persona chat fine-tune (18M) — PASS

- **what**: stage-2 specialization of the chat-PASS 18M rung onto the persona ×
  SNS corpus (Instagram 70% / YouTube 30%) — anima now produces persona-voiced
  replies on the SNS dialogue surface. Detail in `domains/PERSONA.log.md` (same date).
- **surface fit**: replies adopt the SNS register (short, casual, emoji-bearing,
  per-platform tone) — e.g. on an Instagram-DM probe `사용자: 시험 망한 것 같아요…`
  the senpai voice answers `한 번 망했다고 인생 안 끝나. 일단 오늘은 푹 자`.
- **VERDICT (p7, g5 verbatim)**: base-chat retained (A: PASS 4/5, mirror 0/5) +
  persona-voice signal real (B: top-1 self-id 20/40 = 0.50 = 10× chance, mirror
  at chance). anti_goodhart_ok = TRUE. honest scope = 18M-only, signal partial
  (15/20). Full verdict: `.verdicts/chat-persona-sns/SUMMARY.txt`.
- **HF**: `dancinlab/anima-clm-persona-sns-rung0-byte-18m` (PUBLIC, CLM+KOSMOS).
- **PHILOSOPHY**: SNS persona carried by learned dialogue-continuation only — no
  system prompt / role tag / persona injection / RLHF (p1–p4/p6 HELD).
