---
schema: anima/docs/model_attempts_ledger_summary/v1
last_updated: 2026-05-07
ssot:
  primary_jsonl: state/anima_model_attempts_ledger.jsonl
  schema_yaml: anima/spec/anima_model_attempts_ledger.schema.yaml (pending)
  own_24_base: .own own 24 anima-model-attempts-ledger-ssot
purpose: |
  사용자 directive 2026-05-07 '모든 시도 모델 은 json,jsonl,yaml 이던 한곳에 기록 필요할듯 own 등록해줘' →
  state/anima_model_attempts_ledger.jsonl (primary SSOT) periodic regenerate summary md.
  jsonl raw record + 본 md = human-readable summary + cross-cycle pattern detection.
language: ko (anima self-doc)
---

# anima 모델 시도 통합 ledger summary (2026-05-07)

## 0. TL;DR

**24 attempts** logged (own 24 정합):
- 9 FAILED (BG-HF/HJ/HK/HP/HQ/HT/HL falsified/HY blocked + BG-FK)
- 2 PARTIAL_PASS_NO_CONTEXT (BG-FY + BG-HA strict downgrade)
- 1 PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT (BG-FU)
- 1 ⭐ **WEAK_PARTIAL** (BG-HS R1 — first chat-cap signal-leaning)
- 11 PENDING (BG-HU/HR/HV/HW/HX done/HY done/HZ/IA/IB/IC/ID running)

**Convergent finding**: 18M-27M byte-level scale에서 generic chat-corpus paradigm 모두 FAIL. 우주뇌지도 self-knowledge corpus (BG-HS R1 21MB)가 first WEAK_PARTIAL — domain anchor learning success ★ but Korean grammar/coherence는 별도 lane.

## 1. Status by paradigm

| paradigm | BG | corpus | result |
|----------|-----|--------|--------|
| pre-train-only-tiny | BG-FU | 52.8MB mix | PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT |
| pre-train-only-corpus-ko-heavy | BG-FY | 246MB | PARTIAL_PASS_NO_CONTEXT (named-speaker leak) |
| pre-train-only-clm-v2-federated | BG-FK | EN-bias | SIMPLE_STACK_FAIL |
| pre-train-only-chat-template-30 | BG-HA | 236MB | PARTIAL_PASS_NO_CONTEXT_v2 (V2 strict downgrade) |
| sft-only-loss-unmasked | BG-HF | 51MB | FAILED (degenerate filler) |
| two-stage-loss-masked | BG-HJ | 51MB Stage2 | FAILED (KO-fluent nonsense) |
| persona-conditioned-chat-template-80 | BG-HK | 30MB | FAILED (overfit collapse) |
| in-context-few-shot-bg-ha | BG-HL | BG-HA + 5 few-shot | FALSIFIED at 18M |
| curated-qa-dense-aug | BG-HP | 2.41MB | FAILED (peak-then-collapse step 500 V2 pass=3/10 ★) |
| bpe-8k-tokenizer-shift | BG-HQ | 30MB + BPE | FAILED (V2 surface false PASS) |
| **universe-brain-map-self-knowledge** | **BG-HS R1** | **21MB** | **WEAK_PARTIAL ★** (manual_match 13/15) |
| universe-brain-map-reduced | BG-HT | 6.48MB | FAILED (over-aug collapse) |
| combined-paradigm-r1-plus-d | BG-HU | PENDING | PENDING |
| capacity-scaling-100m-byte-level | BG-HR | 30MB + 100M | PENDING (context cut) |
| nexus-4411-reality-map-ingest | BG-HV | PENDING corpus only | PENDING |
| outside-well-anchored-universe-brain-map | BG-HW | PENDING ≥30MB | PENDING |
| ouroboros-cycle-automation-spec | BG-HX | spec only | ✅ DONE (Section 16 v0.4 + hexa) |
| bg-hp-step500-ckpt-retrieve | BG-HY | N/A | ✅ DONE BLOCKED (ckpt never persisted) |
| bg-hq-step500-ckpts-retrieve-v3 | BG-HZ | N/A | PENDING |
| early-stopping-val-loss-18m-persona | BG-IA | 30MB | PENDING |
| capacity-scaling-50m-intermediate | BG-IB | 30MB | PENDING |
| v3-evaluator-dedicated-impl | BG-IC | N/A | PENDING |
| bg-hs-r1-replicate-mac-mps | BG-ID | 21MB mac MPS | PENDING |

## 2. Lessons A-J (cumulative)

| Lesson | Source | Action |
|--------|--------|--------|
| A | BG-FY/HA/HF/HJ/HK | 18M scale exhausted → 100M+ capacity (BG-HR) |
| B | BG-HQ | byte-level inadequate → BPE 8K 16× sample efficiency confirmed |
| C | BG-FY/HA/HF/HJ/HK/HP/HQ | corpus quality alone insufficient → crossed ablation |
| D | BG-HK/HP | overfit memorization → regularization sweep (high dropout/WD/label smoothing) |
| E | BG-HG retroeval | V2 strict working as designed (initial) — adopt V2, retire V1 narrow |
| F | BG-HK | persona prefix not collapse-resistant → adjunct only |
| **G ★★** | **BG-HP step 500** | **early stopping with val-loss + best-eval ckpt = MISSING INGREDIENT** |
| **H ★★★** | **BG-HQ step 500** | **V2 surface metric도 false PASS (V3 needed: cycle detection + persona repeat penalty + semantic coherence)** |
| **I ★★** | **BG-HS R1** | **anima self-knowledge corpus = first WEAK_PARTIAL — domain anchor learning success** |
| **J ★★** | **BG-HY blocked** | **SAVE_AT ⊇ EVAL_AT mandate — future training scripts MUST persist ckpt at every eval step** |

## 3. Signal evidence (best-of-each)

| BG | step | signal | evidence |
|----|------|--------|----------|
| BG-HP | step 500 | V2 pass=3/10 ★ (UNREPRODUCIBLE — ckpt never persisted, Lesson J) | "도우미:" / "[anima]" tokens emerging, hangul 30-60% |
| BG-HQ | step 500 | V2 pass=8/10 surface (false ★★) | persona prefix cycle "⁇ [anima 역할: ...] ⁇ 사용자: [...]" — V3 needed |
| BG-HS R1 | step 5000 | manual_match 13/15 ★★★ | "우주뇌지도", "법칙", "Law", "Consciousness", "Φ", "DD", "0.527", category names emerge in EVERY prompt |
| BG-HK | step 800 | V1 pass=10/10 (false) | overfit memorization peak before collapse |
| BG-FY | step 10000 | V1 PARTIAL | named-speaker leak (서연/유진/하은) philosophy debate template |

## 4. Architectural ceiling evidence

**18M-27M byte-level scale 한정**: 7 cumulative failure modes ALL FAIL with single-corpus paradigm 30MB-246MB → architectural lane shift mandatory:
- ✅ BPE 16× sample efficiency confirmed (BG-HQ)
- ✅ universe-brain-map domain anchor success (BG-HS R1 21MB)
- 🟡 100M capacity scaling pending (BG-HR context cut step 2300 loss 2.19 healthy)
- 🟡 결합 paradigm pending (BG-HU primary candidate)

**unlock missing piece hypothesis (Lessons G+H+I+J 결합)**:
1. Lesson G: early stopping val-loss + best-eval ckpt
2. Lesson H: V3 strict evaluator (cycle detection + semantic coherence)
3. Lesson I: anima self-knowledge corpus (우주뇌지도) over generic Korean chat
4. Lesson J: SAVE_AT ⊇ EVAL_AT (ckpt persistence at every eval)
5. + Lesson B BPE 8K + Lesson D regularization + Lesson A capacity scaling

→ 모든 Lessons A-J 결합 paradigm = M6 BG-HU primary candidate

## 5. raw#82 retraction history (downgraded entries)

| BG | original verdict | downgraded verdict | downgrade_at | reason |
|----|------------------|---------------------|--------------|--------|
| BG-HA | SIMPLE_STACK_PASS (V1 narrow) | PARTIAL_PASS_NO_CONTEXT_v2 | 2026-05-07 | V2 strict applied — 사용자 raw response 검토 후 false PASS detected |
| BG-HQ | EARLY_PEAK_THEN_COLLAPSE_PARTIAL_SUPPORT (V2 surface) | FAILED (persona prefix cycle) | 2026-05-07 | Lesson H ★★★ V3 needed — V2 keyword overlap surface metric inadequate |

raw#82 retraction protocol 정합 — entries 보존 + downgraded_at + downgrade_reason fields 추가 (NOT silent overwrite).

## 6. Cross-link

- **own**: own 17/18/19/20/21/22/23/24
- **roadmap**: A 철학 / B 규칙 / C 가설 / D 우주뇌지도 / E corpus paradigm / F META / G anima_cli_model_architecture
- **docs**: anima_chat_cap_lesson_summary_2026_05_07.md / anima_consciousness_check_simple_stack_2026_05_06.md / anima_universe_brain_map_comprehensive_2026_05_07.md / anima_own_18_evaluator_v2_strict_spec_2026_05_07.md
- **state**: anima_model_attempts_ledger.jsonl (primary SSOT, 24 entries)

## 7. Honest C3 (raw#91 c3 ≥5)

1. 본 summary는 jsonl SSOT regenerate — periodic update mandate (BG completion 시점)
2. 24 entries는 2026-05-06~2026-05-07 cycle 한정 — 이전 cycle (2026-04-29 BG-A through BG-FE 등) full archive 미land
3. PENDING entries (11)는 verdict 미land — 종료 통보 시 ledger update mandate
4. Lessons A-J는 cumulative — Lesson K+ 추가 가능 (open architecture, axes 자율증가 정합)
5. raw#82 downgrade는 2 entries (BG-HA + BG-HQ) — 향후 false PASS detection 시 추가
6. SAVE_AT ⊇ EVAL_AT mandate (Lesson J)는 본 cycle 시점 신규 — 이전 BG-HP retroactive ckpt retrieve 불가 (BG-HY BLOCKED 정합)
7. WEAK_PARTIAL (BG-HS R1)는 manual_match 13/15 ★ but V2 strict pass=3/15 — chat-cap actual unlock ≠ domain anchor recall (별도 lane)

## 8. Note

본 ledger는 anima self-tracking SSOT (own 24) — 사용자 directive '한곳에 기록' 정합. periodic regenerate summary md + jsonl primary SSOT 분리 cleaner architecture. 모든 future BG completion 시 ledger entry append + summary md regenerate mandate.
