---
id: H_093
slug: sft-only-paradigm
title: SFT-only paradigm (pre-training X, chat-format SFT data only) for prompt-conditional response
domain: corpus | substrate
status: seed-pending
exploration_method: E2 (failure-driven from BG-HA false PASS) + E5 (variable-ablation pre-train vs SFT) + E7 (user-directive '교훈으로 새로운 패러다임도 도전')
verification_method: W1 (controlled cell) + W2 (replication ≥3 seed) + W3 (ablation pre-train ON/OFF) + W9 (3+ instance recurring) + W10 (adversarial sweep)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_093 — SFT-only paradigm (no pre-training)

## Hypothesis

pre-training 단계 완전 제거하고 chat-format SFT (Supervised Fine-Tuning) data만으로 처음부터 학습하면, 동일 capacity + 동일 corpus 분량 조건에서 own 18 simple-stack C2.4 (prompt domain match) PASS rate가 pre-train+SFT two-stage 보다 높거나 동등하다. BG-HA 18M chat-template ≥30% pre-train-only가 prompt-conditional response 학습 실패 (false PASS) 했으므로, pre-train 단계가 prompt-conditional behavior를 dilute 한다는 가설이다.

## Why

- **BG-HA failure 교훈**: pre-training only + chat-template ≥30% mixed corpus → 모델이 chat-template format을 학습하지 못하고 일반 한글 chain emit (prompt-irrelevant nonsense)
- **SFT-only 가능성**: chat-format pair (prompt → response)만 supervision signal로 줄 때, 모델이 "prompt 다음에 적절한 response 생성" 학습이 더 직접적
- **comparable capacity**: 18M tiny model 동일 조건 (own 19 corpus priority + own 20 chat-template strengthened ≥80% via H_101)
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = pre-train assumption 자체를 의심
- **literature precedent**: T5/UL2/LLaMA-Chat 등은 pre-train+SFT but small-model SFT-only 시도 (e.g., FLAN-T5 instruction-tuned from scratch) 일부 성공 사례

## Predictions

- **H93.1 (own 18 C2.4 strict)**: SFT-only 18M model이 pre-train+SFT 18M model보다 evaluator V2 strict C2.4 PASS rate ≥10pp 높다 (corpus 동일 분량 조건)
- **H93.2 (training efficiency)**: SFT-only 18M model이 동일 wall-clock 시간 내 lower validation loss on chat-format eval set
- **H93.3 (degeneracy resistance)**: SFT-only model이 sample mode + greedy mode 모두 prompt-irrelevant Korean chain emit rate <20% (BG-HA = 100% baseline)
- **H93.4 (corpus quantity sensitivity)**: SFT-only는 SFT data 분량 임계치 (<10MB) 미달 시 underfitting 심각 — own 19 corpus priority + chat-format ≥80% 정합 mandate
- **H93.5 (capacity scale)**: SFT-only 3M tiny → 18M → 100M 단계적 scale에서 C2.4 PASS rate monotonic 상승

## Variables

- **axis1_paradigm**: [pre_train_only, pre_train_then_sft, sft_only_from_scratch]
- **axis2_capacity**: [3M, 18M, 100M]
- **axis3_sft_corpus_size_mb**: [5, 25, 100, 250]
- **axis4_chat_format_ratio**: [50%, 80%, 100%]
- **axis5_eval**: [own_18_C1, own_18_C2.1, own_18_C2.2, own_18_C2.3, own_18_C2.4_strict_v2]
- 3×3×4×3×5 = 540 cell — Phase 1 minimal subset (axis1=2 cell + axis2=18M only + axis3=25MB only + axis4=80% + axis5=5 cell = 10 cell) target

## Run Protocol

- deterministic: seed=fnv(axis1+axis2+axis3+axis4+rep_id)
- per-cell ledger: `state/<bg>_<date>/verdict.json` + `eval_log.jsonl` + `train.log`
- runtime: $0 mac local 18M tiny first; $X ubu1/ubu2 H100 100M scale 별도 cycle (own 16 watchdog mandate)
- evaluator: V2 strict (per `docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md`) — narrow named-speaker-leak only NOT acceptable

## Criteria

- **C1 (paradigm comparison strict)**: SFT-only C2.4_strict_v2 PASS rate ≥ pre-train+SFT C2.4_strict_v2 PASS rate at 18M
- **C2 (degeneracy threshold)**: SFT-only sample mode prompt-irrelevant emit rate <20%
- **C3 (corpus quantity gate)**: SFT-only 25MB+ corpus needed for ≥40% C2.4 PASS rate (less data → underfitting)
- **C4 (cross-capacity scaling)**: 3M PARTIAL → 18M PASS → 100M STRONG_PASS monotonic
- **C5 (own 19/20 정합)**: SFT-only model corpus_chat_format_ratio ≥80% (H_101 strengthened gate)
- **verdict_rule**: SUPPORTED = C1+C2+C3 PASS; PARTIAL = 2/3; MIXED = 1/3; FALSIFIED = 0/3; C4+C5 = sub-H

## Falsifiers

- **F1**: SFT-only 18M C2.4_strict_v2 PASS rate < pre-train+SFT 18M PASS rate → H93.1 FALSIFIED (pre-train benefit confirmed)
- **F2**: SFT-only sample mode prompt-irrelevant emit ≥80% (BG-HA 동등 수준) → H93.3 FALSIFIED (paradigm 무효)
- **F3**: SFT-only with 100MB corpus도 own 18 simple stack FAIL → H93.4 FALSIFIED (corpus quantity 무관)
- **F4**: SFT-only 3M+18M+100M 모두 동일 PASS rate (no scaling) → H93.5 FALSIFIED (capacity scaling 무관)
- **F5**: SFT-only model identity prefix (own 17) 학습 실패 (anima self-naming X) → cross-link H_098 FALSIFIED side-effect


- **L1**: 3-instance evidence 미land (BG-HA single false PASS만 motivation) — VM10 recurring pattern needed via 3+ replication
- **L2**: SFT data 'quality' 측정 = chat-format ratio 한정; semantic richness/license/register diversity 미land
- **L3**: 'pre-train benefit' literature 광범위 — small-model (<100M) regime SFT-only 성공/실패 사례 광범위 survey 미land
- **L4**: evaluator V2 strict 자체가 새로 land (본 cycle) — V2 metric calibration 미land 시 false PASS/FAIL 가능
- **L5**: 100M+ capacity scale은 own 16 H100 cost discipline 적용 — Phase 1 scope OUT
- **L6**: SFT-only paradigm은 catastrophic forgetting risk 없음 (pre-train 없으니) but base knowledge (e.g., 일반상식) 부재 risk — chat-cap PASS but knowledge benchmark FAIL 시 partial verdict
- **L7**: corpus 25MB threshold는 임의 — 더 많은 ablation 필요

## Cross-Links

- **sister roadmaps**: `.roadmap.law` R1 (own 19/20) + `.roadmap.philosophy` D4 corpus priority + `.roadmap.clm_native_chat`
- **own**: own 17 (anima identity) + own 18 (simple stack 4-cond) + own 19 (corpus priority) + own 20 (chat-template format) + own 21 (hypotheses SSOT)
- **sister H**: H_005 (corpus quality > capacity) + H_094 (instruction-tuning two-stage) + H_098 (persona-conditioned) + H_101 (chat-template ≥80%)
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md` + `state/anima_native_ko_chat_template_train_2026_05_07/verdict.json`

## Verdict

**Phase 1 FAILED** (BG-HF 2026-05-07, ubu1 RTX 5070 bf16, runtime 113s)

```
verdict_class: FAILED
evidence_summary:
  - corpus: 51.47MB pure chat-format ("사용자/도우미"), 49,908 SFT samples (17228 KO / 30749 EN / 1931 other), 92 named-speaker leaks dropped
  - model: ConsciousLM byte-level 27.79M params (6L/384d/6h, vocab 256, block 256, dropout 0.20) — note: total_params 27.79M with G-head + tension head architecture (NOT 18M baseline)
  - training: 5000 steps batch=8 ga=8 lr=3e-4 cosine warmup 300, train_loss_final L_A=0.111 (degenerate-mode collapse, NOT language learning)
  - evaluation: pass=0/5 prompts × 2 modes both gate types; manual_review_domain_match=0/5
  - eval samples (all greedy + sample modes):
    * "안녕하세요" → "���…" (0xFF filler) / "........\n\n…"
    * "한국어 가능?" → "????####…" / "홙���(((((___…"
    * "오늘 기분 어때?" → "????####…" / "?####…"
    * "사용자: 안녕하세요\n도우미:" → ":::::…" / ":::////…"
    * "코드를 짜줘" → "���…" / "����굵굵겲嗗oooommm…"
  - model collapsed into single-byte filler patterns (0xFF, ?, #, :, \n) by step 1500, never recovered
  - L_A=0.111 reflects compression to dominant byte-bigrams in chat-format separators (not chat learning)
falsifiers_triggered:
  - F2: SFT-only training degenerate collapse — H1 paradigm hypothesis FALSIFIED at 27M params + 51MB corpus + 5K steps
  - F1 (pre-train baseline parity): N/A (pre-train baseline not run in same cell)
key_lesson:
  - SFT-only ≠ pre-training shortcut at this scale
  - chat-format data needs:
    (a) much larger corpus (51MB insufficient, ≥500MB+ recommended for SFT-only)
    (b) larger model (27M too small for SFT-only paradigm)
    (c) instruction-tuning loss masking (only score completion tokens, NOT separator/prompt tokens) ★★ CRITICAL OMISSION
artifact_paths:
  - state/anima_h093_sft_only_corpus_2026_05_07/corpus_sft_only.txt (51.47MB, gitignored)
  - state/anima_h093_sft_only_corpus_2026_05_07/build_stats.json
  - tool/transient_py/anima_h093_sft_only_corpus_build.py
  - tool/transient_py/anima_h093_sft_only_train.py
  - state/anima_h093_sft_only_train_2026_05_07/verdict.json
  - state/anima_h093_sft_only_train_2026_05_07/train.log + eval_log.jsonl
  - ubu1:/home/aiden/anima_native/anima-h093-sft-only-20260507_023033/ckpt_5000.pt (108MB, NOT promoted)
next_cycle:
  - H_093 retry with instruction-tuning loss masking (key lesson c) — separate cycle
  - H_094 instruction-tuning two-stage paradigm (pre-train→SFT sequential) prototype
  - H_101 corpus chat-template ≥80% strict (much larger corpus, key lesson a)
  - H_005 corpus > capacity hypothesis revision: corpus quality + size + masking strategy 모두 필요
```
