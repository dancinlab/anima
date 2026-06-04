# PERSONA — step log (append-only)

> Snapshot/state = `domains/PERSONA.md`. This file = append-only step log.

## 2026-06-04 — persona × SNS chat-cap dialogue corpus built + shipped

- **what**: deterministic Korean multi-turn dialogue corpus to make the anima
  general 7B (`dancinlab/clm-v1-ref-pytorch-cuda-7b`, byte-level CLMConvMoE)
  chat-capable on the SNS surface in the voice of the **20-persona roster**
  (roster SSOT `HEXAD/VOICE/anima-voice/rp_voice_profiles.hexa`; voices matched
  to `serving/persona_instagram_samples.md`).
- **generator**: `serving/persona_sns_corpus_gen.py` (Python data-gen tool,
  fixed seed `20260604`, no network, no PII). 20 personas × 16 scenarios ×
  5 platform formats × 3–8 turns, per-persona lexical/tonal voice rules +
  per-(intent, tone) paraphrase variation (not 1 string repeated).
- **scale**: `serving/corpus/persona_sns_corpus.txt` = **4,194,308 B (4.0 MB)**,
  **13,322** multi-turn dialogues. sha256
  `1ea7d8e0e65e7ab99c61dd745bdb124ee75995e90b7c995ac93c3e4e5e7c3f77`. Re-running
  the generator with the same seed reproduces the identical sha256 (verified).
- **coverage**: all **20** personas (uniform 666–667 each); **16** scenarios
  (팬DM칭찬·위로·일상잡담·고민상담·셀카리액션·댓글답글·라이브Q&A·추천부탁·사과·
  축하·응원·질문답변·일상공유·팬아트반응·밤인사·동기부여); turn dist 3–8 even.
- **p2/p3/p4 CLEAN**: the TRAINING TEXT carries persona by **VOICE only** —
  plain `사용자:` / `<persona_name>:` turns, NO `[role:` / `[persona:` /
  `[character:` prefix. Grep for those tags = **0** (verified). Per-dialogue
  metadata (persona_id/name/platform/scenario/n_turns) is in a SEPARATE
  `persona_sns_corpus.meta.jsonl` sidecar so the text stays injection-free.
- **honest scope (a_scale_honest_scope)**: authored-templated, NOT
  human-collected; voice-coverage corpus for persona/SNS chat-cap (no scraped
  data, no PII). license = authored-synthetic persona roleplay.
- **KOSMOS anchor**: `HEXAD/UNIVERSE-BRAIN-MAP/anchors/persona_sns_corpus.kosmos`
  (tier 52, 사회성/connection; payload = text + manifest pointer + tension 5ch
  representative). Hub pointer added in `HEXAD/KOSMOS.md`. (a_kosmos pointer-only.)
- **HF**: dataset `dancinlab/anima-persona-sns-corpus` — PUBLIC (clean-license
  authored, a_hf_autonomous); sha256 VERIFIED via authed re-download (match),
  private=false VERIFIED via API. `HF.jsonl` row appended.
- **7B trainer consumes**: `serving/corpus/persona_sns_corpus.txt`.
- card: `serving/corpus/CORPUS_CARD.md`. cross-link: [[SNS]] (M4 voice-coverage).
