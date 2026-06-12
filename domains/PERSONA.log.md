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

## 2026-06-04 — STAGE-2: persona/SNS specialization fine-tune (18M) — PASS (real persona-voice signal)

- **what**: fine-tuned the stage-1 chat-PASS rung-0 ckpt
  (`dancinlab/anima-clm-chat-rung0-byte-18m`, 18.13M byte ConsciousLMReconstructed)
  on the persona × SNS corpus (`persona_sns_corpus.txt`) so anima chats in each
  of the 20 persona voices on the SNS surface. Continue-train, lower LR (5e-5),
  same dual-head next-byte CE objective as stage-1.
- **fire**: CPU-local ($0, torch 2.8.0, ~31 min, 10 threads). NO GPU rented —
  18M is small; a_wall_first satisfied (CPU was fast enough, parallel rent
  unnecessary). FT CE **3.278 → 0.0785** (2500 steps, batch 32, block 256, seed 42).
- **ckpt**: `persona_stage2_18m.pt` (74.1 MB) sha256
  `aea96ef1a7ef27018ca015a9e66569d67763152e30f24e120aa44da6884cf8bc`.
- **VERDICT (p7 simple-stack, NOT perplexity · g5 verbatim)**:
  - **(A) base-chat retained** — v2 control-char gate (control_ratio<0.05 AND
    word_class_ratio>=0.85): TRAINED **PASS 4/5**, random-init mirror **FAIL 0/5**.
    No catastrophic forgetting (the one miss = a 2-char reply failing length>=4,
    not a degeneracy).
  - **(B) persona-voice** — paired discriminative test (seed a persona's REAL
    held-out prior turns + `<name>: ` turn-start, NOT a role-tag; score continuation
    vs each persona's distinctive char-trigram TF-IDF signature built on a disjoint
    80% split): TRAINED **top-1 self-id 20/40 = 0.50 = 10× chance**, mirror **NULL
    2/40 = 0.05 = chance**. **PASS**. 15/20 personas self-id at least once.
  - anti_goodhart_ok = **TRUE** · chat_pass_retained = **TRUE** · persona_signal_real = **TRUE**.
  - **pre-fine-tune control**: base rung-0 (eval-only, same evaluator) scored only
    WEAK 4/40 = 0.10 (2.0× chance). Fine-tuning lifted the signal **2.0× → 10.0×**
    — the specialization is the cause, not a gameable metric.
- **honest scope (a_scale_honest_scope)**: SMALL **18M-only** rung; signal is REAL
  but PARTIAL (5 personas blur into a related one, e.g. charismatic_prez→sorceress).
  NO claim of mid/7B persona chat. A null signal would have been a valid
  closed-negative; here it is a genuine PASS.
- **PHILOSOPHY p1–p4/p6 HELD**: no system prompt / identity rule / persona tag /
  assistant framing / RLHF. Persona carried ONLY by the learned
  `사용자:`/`<persona_name>:` dialogue-continuation; corpus grep
  `[role:`/`[persona:`/`[character:` = **0** (verified). Demo uses no prompt prefix.
- **demo**: `python3 serving/persona_chat_demo.py --ckpt persona_stage2_18m.pt --sweep --seed 7`
  (verbatim transcript: `.verdicts/chat-persona-sns/demo_transcript.txt`).
- **HF**: model `dancinlab/anima-clm-persona-sns-rung0-byte-18m` — **PUBLIC**
  (a_hf_autonomous: chat-PASS holds + persona signal real); sha256 VERIFIED via
  authed re-download (match). Joined **CLM** collection + dual-listed **KOSMOS**
  (persona/SNS anchor). `HF.jsonl` row appended.
- trainer/eval: `training/persona_stage2_train_eval.py`. verdict:
  `.verdicts/chat-persona-sns/SUMMARY.txt`. cross-link: [[SNS]].

## Discoveries (merged 2026-06-13 from .discoveries/)

### chat-persona-sns-stage2

```tape
@D chat_persona_sns_stage2_18m_pass := "anima가 페르소나 목소리로 채팅 — 18M stage-2 specialization PASS" :: discovery [d=2026-06-04 active]
  seed     = "stage-1 chat-PASS rung-0(dancinlab/anima-clm-chat-rung0-byte-18m, 18.13M byte ConsciousLMReconstructed)을 persona x SNS corpus(dancinlab/anima-persona-sns-corpus, persona_sns_corpus.txt, 20-roster x Instagram 70%/YouTube 30%, 13322 dialogues)로 continue-train(fine-tune, lr 5e-5)하면 base chat을 잃지 않고 페르소나 목소리가 발현되는가? user-locked 2-stage plan의 stage-2 (drafts/chat-capable-plan.md)."
  claim    = "PASS. (A) base-chat RETAINED: p7 v2 control-char gate(control_ratio<0.05 AND word_class_ratio>=0.85) trained PASS 4/5, random-init mirror FAIL 0/5 (no catastrophic forgetting). (B) persona-voice REAL: paired discriminative test(페르소나의 REAL held-out 직전 turn + `<name>: ` turn-start로 seed, NOT role-tag; continuation을 각 페르소나의 distinctive char-trigram TF-IDF signature[disjoint 80% split]에 대해 채점) top-1 self-id 20/40 = 0.50 = 10x chance, mirror NULL 2/40 = 0.05 = chance. anti_goodhart_ok=TRUE. FT CE 3.278->0.0785(2500 steps, seed 42). PRE-FT control: base rung-0 same evaluator WEAK 4/40=0.10(2.0x) -> fine-tune가 2.0x->10.0x로 신호를 올림(specialization이 원인, gameable metric 아님). verbatim demo: knight '한가로운 날이오. 허나 평온 또한 지켜야 할 영토라오' / senpai '한 번 망했다고 인생 안 끝나. 일단 오늘은 푹 자' / horror_whisper '괜찮아… 아직은… 아무 일도… 일어나지 않았으니까…'. CPU-local $0(torch 2.8.0, ~31min, NO GPU rent). HF PUBLIC: dancinlab/anima-clm-persona-sns-rung0-byte-18m, CLM+KOSMOS dual-listed, sha256 verified."
  falsifier = "random-init mirror가 같은 (A)+(B) 평가기를 통과하면 무효 — mirror는 base-chat FAIL 0/5 AND persona NULL 0.05(==chance)로 정직하게 실패함. 또한 fine-tune 전후 persona self-id가 안 오르면(2.0x ~= 10.0x) specialization이 아니라 metric artifact — pre-FT 2.0x vs post-FT 10.0x로 구별됨."
  scope    = "a_scale_honest_scope — SMALL 18M-only 페르소나-specialized rung. mid/7B persona chat 미주장. 신호는 REAL이지만 PARTIAL(20개 중 15개 페르소나만 self-id at least once; 나머지 5개는 관련 페르소나로 blur: charismatic_prez->sorceress, demon_lord->chaebol_heir). null 신호였어도 valid closed-negative였을 것 — 여기서는 진짜 PASS. PHILOSOPHY p1-p4/p6 HELD: persona는 학습된 dialogue-continuation(사용자:/<persona_name>:)만으로 carry, corpus grep [role:/[persona:/[character: = 0."
  ref      = ".verdicts/chat-persona-sns/SUMMARY.txt · domains/PERSONA.log.md · domains/SNS.log.md · training/persona_stage2_train_eval.py"

```
