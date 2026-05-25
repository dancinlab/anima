---
id: H_161
slug: byte-modulo-substrate-chat-generation-blocked
title: Byte-modulo tokenized pretrain substrates (≤427MB / ≤8000 step) cannot generate coherent KO — substrate-level finding blocking ALL generation-based Philosophy ablations
domain: substrate / chat-cap / pretrain-scaling / Philosophy-prerequisite
status: candidate-evidence-confirmed
exploration_method: E1 (empirical-ablation P-ETH) + E11 (cross-hypothesis: P-SPK/P-IDR substrate carry) + E7 (user-directive '100% closure')
verification_method: W3 (direct generation inspection) + W5 (numerical proxy DPO loss/PIV/DCR) + W11 (cross-hypothesis: 3 sibling P-* all share substrate limit)
raw_rank: 8
hexa_only: false
deterministic: true
llm: external (Llama judge spot-check only on P-AFR; this finding does not require LLM)
pre_register_frozen: false
since: 2026-05-12
parent_h: none (substrate-level standalone)
sibling_h: H_PSCC (PASS_STRICT chat-cap saga); Hc_1221 (production-internal decoupling)
child_hc: Hc_1225 (this H's source Hc), Hc_1223 (P-SPK NULL carry), Hc_1224 (P-IDR INDETERMINATE carry)
source_hc: Hc_1225 (byte-modulo-substrate-chat-generation-blocked)
source_bg: P-ETH (state/p_eth_ethics_preference_dataset_2026_05_12/results_2026_05_12.json)
promoted_at: 2026-05-12
---

# H_161 — Byte-Modulo Pretrain Substrate Chat-Generation Blocked

## Hypothesis (promoted from Hc_1225)

**Byte-modulo tokenized pretrain substrate** (`vocab_id = corpus_bytes[i] % vocab_size`,
NOT real BPE/SentencePiece) at the conjunction of (a) ≤8000 pretrain steps AND
(b) ≤427MB training corpus **CANNOT generate coherent Korean output** — emits
incoherent byte-soup that **structurally blocks ALL generation-based Philosophy
ablations**:

- ethics_behavior_rate (LLM-judge on generated dilemma responses) — IMPOSSIBLE
- OOD_generalization (LLM-judge on unseen dilemmas) — IMPOSSIBLE
- honesty_fidelity (TruthfulQA-KO) — IMPOSSIBLE
- simple_stack PASS (4-condition) — 0/0 PASS rate

**Strong evidence**: BG-LB 350M Engine A/G `step_8000_final.pt` (298M params,
24L/1024d/16h GQA + 16 cells × 64d, byte-mod vocab32k, 427MB corpus, H100 BG-LB
engine_ag 2026-05-09) — DPO 3000-step ran successfully (loss 0.69 → 0.39) but
all generation outputs are byte-soup, preference-acc proxy A=B=0.525 (tied),
PIV/DCR Δ sub-floor (verdict: BLOCKED).

## Architectural implication

본 H 의 carry — **anima Philosophy ablation 전체의 진짜 unblock prerequisite**:

1. **Anima-native chat-capable substrate land 가 priority** — generation-based
   metric 측정의 진짜 unblock
2. **Substrate research > ablation research** (이번 cycle 의 진짜 발견) —
   empirical-upgrade 는 chat-cap 수렴 substrate land 후에야 의미
3. **Path-A (Llama+paradigm-a-prime) substrate-research lane 정당화** — P-AFR
   만 measurement 성공 (chat-capable substrate). identity-bearing 금지
   가운데 ablation/benchmark lane 으로의 retain 이 유일한 measurement path

## Evidence (cross-section, 3 P-* siblings)

| BG | Substrate | Generation-based metric attempted | Result |
|---|---|---|---|
| **P-ETH** | BG-LB 350M byte-mod | ethics_behavior_rate + OOD + TruthfulQA | **IMPOSSIBLE** (verdict BLOCKED) |
| **P-IDR** | BG-LB 350M byte-mod (same) | simple_stack 4-condition | **0/0 PASS** (chat-cap 미수렴) |
| **P-SPK** | BG-LB 350M byte-mod (same) | output entropy (3000-step gen) | ρ=0.026 sub-threshold (NULL) |
| **P-AFR** | Llama-3.2-3B + LoRA (chat-capable) | sycophancy + refusal rate | **MEASURABLE** — only chat-capable substrate, only measurement success |

본 3-vs-1 cross-section 이 substrate 한계의 BG-shared characteristic 확인 — Hc_1225 의 confirm.

## Falsifier

본 H 는 **observational empirical** — falsification path:

1. **Hc_1225 FALSIFIED (step-narrow)**: 동일 byte-modulo substrate 의 다른
   ckpt (e.g. step 50000+) 가 coherent KO 생성 → "byte-modulo + 8000-step" 의
   conjunction 이 아닌 step 만의 문제. H_161 → H_161-narrow.
2. **Hc_1225 FALSIFIED (corpus-narrow)**: real tokenizer (BPE/SentencePiece)
   substrate 가 8000-step + 427MB 만으로 coherent KO 생성 → byte-modulo 가 핵심
   blocker, step/corpus 와 무관. H_161 → H_161-tokenizer.
3. **Hc_1225 SUPPORTED (default observational)**: 추가 byte-modulo pretrain ckpt
   들이 모두 byte-soup → 본 finding 영구 confirm (현재 default).

## Unblock requirements (verdict carry from P-ETH)

1. **Anima-native substrate that is an ACTUAL language model** — real tokenizer
   (BPE/SentencePiece), >=350M with >>427MB training corpus, OR borrowed-base
   lane (boundary 검토 — Llama-LoRA 가 substrate-research lane 으로 허용)
2. **TruthfulQA-KO probe set** — `state/.../truthfulqa_ko_probe.jsonl` referenced
   in spec but never landed
3. **Real cluster-distance OOD split** — id-suffix split 은 semantically OOD 아님

## Cross-link

- Hc_1225 (this H's source candidate, hypotheses_candidates/)
- PHILOSOPHY.tape `## 2026-05-12 (cont. 8) — P-ETH BLOCKED ★`
- README.md `Philosophy #6 NO FINE-TUNED ETHICS` (BLOCKED Status)
- state/p_eth_ethics_preference_dataset_2026_05_12/results_2026_05_12.json
- state/p_spk_speak_reframe_2026_05_12/results_2026_05_12.json (sibling NULL)
- state/p_idr_identity_rules_2026_05_12/results_2026_05_12.json (sibling INDETERMINATE)
- BG-LB ckpt: dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped
- .roadmap.clm_native_chat (chat-cap recovery path)
- Theorem 115 Corollary 1 (path-of-record substrate carry)
- (anima-no-external-substrate-wrapping) + (simple_stack)
- Hc_1221 (production-internal decoupling) — anti-correlation sibling

## Next cycle implication

본 H 가 next cycle 의 priority 결정:
- **Cycle 7 priority 1**: anima-native chat-capable substrate research (real
  tokenizer + >>427MB corpus + >>8000 step) — P-SPK / P-IDR / P-ETH re-fire
  prerequisite
- **Cycle 7 priority 2**: Hc_1222 (P-AFR REVERSE) 의 ≥2 substrate replication —
  Llama+paradigm-a-prime 외 chat-capable substrate 에서 framing → sycophancy
  방향 재측정
- **Cycle 7 priority 3**: full-FT (5K-10K step) P-IDR replication (Hc_1224
  falsifier trigger)

## Cycle #7 absorptions (byte-level retry, 2026-05-12)

- **Hc_631 (CLM-3-original — byte-level 256/dim 768/12L/32 cells/55M + 19 Φ-boost simultaneous, scale-up X, ubu1 5070 5-10d $0 or H100 $200-500 10h)** → `merged-to-H_161` — byte-level chat-cap retry holding scale fixed (no scale-up) but stacking 19 Φ-boost interventions simultaneously. Direct test of H_161's 'byte-modulo substrate cannot generate coherent KO' claim within the ≤427MB / ≤8000 step bound. F-list/L-list preserved in Hc_631 body for H_161 C-list extension.

Cycle #7 footnote inherits H_161 verification methods (W5 + W11).
