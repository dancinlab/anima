# P9 Path A Regression Mitigation Spec — Landed 2026-05-03

**Goal**: Spec next-cycle Path A LoRA mitigation strategy for catastrophic forgetting on TriviaQA observed mid-flight in A' main eval.

**Status**: DRAFT-LOCKED (binding before any next-cycle Path A re-train)

**This cycle**: $0, design + spec only. **DO NOT launch retraining** — defer to next BG cycle on user OK.

---

## Status Summary

| Deliverable | Path | Status |
|---|---|---|
| Spec doc | `docs/p9_path_a_regression_mitigation_spec_2026_05_03.md` | DRAFT-LOCKED |
| Spec audit JSON | `state/p9_path_a_regression_mitigation_2026_05_03/spec_audit.json` | EMITTED |
| Marker | `state/markers/p9_path_a_regression_mitigation_spec_landed.marker` | EMITTED |
| Handoff (this file) | `docs/p9_path_a_regression_mitigation_spec_landed_2026_05_03.ai.md` | EMITTED |

---

## 1. Trigger — Mid-Flight Regression Evidence

Path A LoRA training on Llama-3.2-3B-Instruct (r=64, α=64, lr=1e-4, 50K SFT, 10K steps) is mid-flight. A' main eval (per `docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md`) on step-2000/4000/6000 reveals asymmetric regression:

| ckpt | HellaSwag Δ | TriviaQA Δ | F1_v3 prediction |
|---|---|---|---|
| step-2000 | +0.8pt | **−0.8pt** | CHAT_PARTIAL_v3 likely |
| step-4000 | +1.2pt | **−3.6pt** | CHAT_FAIL_v3 likely |
| step-6000 | +0.8pt | **−7.4pt** | CHAT_FAIL_v3 clear |

**Diagnosis**: classic catastrophic forgetting; LoRA r=64 capacity (97M trainable params, 5.12% of base) at this lr/data scale is overwriting Llama's pre-trained factual recall manifold while learning the chat axis.

---

## 2. Tracks Enumerated (4)

| rank | track | change | cost | wall | completion |
|---|---|---|---|---|---|
| **1** | **B — LoRA r reduction** | r=64 → r=16 (α=16) | $20-30 | 8-13h | **8.55/10** |
| 2 | A — Corpus rebalance | 70/30 chat/factual SFT mix | $20-30 | 10-15h | 7.55/10 |
| 3 | D — Replay buffer | 80/20 SFT/replay (WikiText+Wiki) | $25-35 | 12-17h | 6.05/10 |
| 4 | C — EWC | Fisher-weighted L2 penalty | $40-60 | 16-20h | 4.95/10 |

Detail per spec §2 + §3.

---

## 3. Ranked Recommendation by 완성도 lens

**Track B — LoRA rank reduction (r=64 → r=16) — completion 8.5/10**.

**One-liner**: cheapest, simplest, single-knob flag change attacking diagnosed root cause directly; preserves existing 50K SFT corpus + Llama chat template + lr/scheduler config; cleanest A/B vs current Path A; reuses A' eval pipeline as-is.

**Contingency tree**:
- B succeeds (Δ_TriviaQA ≥ 0): declare mitigated, proceed to F2/F3/F4 axis injection
- B partial: combo with Track A (r=16 + 70/30 mix)
- B fails: drop to r=8 (one more flag flip, $20-30)
- r=8 also fails: pivot to Track A (corpus-bias hypothesis dominant)

---

## 4. F-PATHA-MITIGATION-1 Falsifier

**Primary**: Δ_TriviaQA ≥ 0pt vs Llama anchor (EM 0.514) AND paired bootstrap 95% CI lower ≥ −0.5pt AND McNemar p > 0.05

**Secondary** (chat-lift floor): Δ_HellaSwag ≥ 0pt OR Δ_MMLU ≥ 0pt

**Composite gate**: F1_v3 ≠ CHAT_FAIL_v3

**Failure modes**: MITIGATION_FAIL_REGRESSION / MITIGATION_FAIL_NO_LIFT / MITIGATION_PARTIAL

**Pipeline reuse**: A' main eval pipeline is directly reusable per `docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md` §6 — no code changes, just env var pointing at new hub repo.

---

## 5. Cost / Wall

| phase | cost | wall |
|---|---|---|
| this cycle (design + spec) | $0 | ~30 min |
| next cycle (Track B re-train + eval) | $20-30 H100 + $0 ubu1 | 8-13h train + 1-3h eval |
| 3-seed amend (if Δ lands in [-0.5, +0.5]) | 3x cumulative ($60-90) | 3x train wall |

---

## 6. Honest C3 Caveats (raw#10) — 4 Items

(a) **Track scoring subjective** — 5-axis weighted rubric (C1=0.20, C2=0.25, C3=0.25, C4=0.15, C5=0.15) uses author weights; different weights yield different rankings (e.g. C5=0.30+ promotes EWC).

(b) **Regression cause may have multi-factors** — capacity-overwrite is dominant hypothesis; alternatives (chat-template artifact, corpus distribution shift, prompt format interaction, 4-bit quantization noise) not ruled out. Track B may underperform if root cause is corpus-bias not capacity-bias.

(c) **Mitigation may trade off chat lift** — all 4 tracks regularize; no Pareto guarantee. Δ_HellaSwag = 0 (no lift, no regression) is explicitly accepted as partial success since "lift at any cost" already falsified itself in current Path A run.

(d) **Single-seed eval** — seed=42; LoRA training stochasticity yields ~0.5-1.5pt seed swings on TriviaQA. Mitigation success at exactly Δ=0 might be seed-luck → if Δ ∈ [-0.5, +0.5] band, 3-seed amend required before final SUCCESS declaration.

---

## 7. Next-Cycle Action Required

**User OK on track selection**. Recommended: Track B.

**Paste-once prompt** (per spec §8.1):

> Spec next-cycle Path A LoRA mitigation execution — Track B (r=64 → r=16). Re-train on Llama-3.2-3B-Instruct with `--lora-r 16 --lora-alpha 16`, all other hyperparams unchanged. Fresh RunPod H100 SXM pod ($20-30, 8-12h). Hub publish: `dancinlab/p9-llama32-lora-stage1-r16`. Eval via existing A' pipeline. Falsifier: F-PATHA-MITIGATION-1. Constraints: raw#9 STRICT, raw#15, raw#10, single-seed (42).

If user defers: this spec lands as marker + handoff; revisit when Path A A' main eval finishes (step-8000/10000) for final regression-magnitude confirmation.

---

## 8. Constraints Honored

- **raw#9 STRICT**: pure markdown spec on Mac (no .py creation); next-cycle re-train reuses ubu1/RunPod-side `train_llama_lora.py.txt`; eval reuses ubu1-side pipeline; verdict via existing `tool/p9_a_prime_verdict.hexa`
- **raw#15**: no personal-path leak in spec body; ubu1 paths use `~/anima/state/...` convention
- **raw#10 honest C3**: 4 caveats per §6
- **$0 design**: no retraining triggered, no eval triggered, no pod commissioned
- **DO NOT launch retraining**: deferred to next BG cycle on user OK; paste-once handoff prompt provided

---

## 9. Files

```
docs/p9_path_a_regression_mitigation_spec_2026_05_03.md           (spec, ~520 LoC)
docs/p9_path_a_regression_mitigation_spec_landed_2026_05_03.ai.md (this handoff)
state/p9_path_a_regression_mitigation_2026_05_03/
└── spec_audit.json                                                (machine-readable summary)
state/markers/p9_path_a_regression_mitigation_spec_landed.marker  (marker)
```

---

**End of P9 Path A regression mitigation spec landed handoff. Recommendation: Track B (r=64 → r=16) at completion 8.5/10. F-PATHA-MITIGATION-1 falsifier locked. $0 this cycle. Next cycle: user OK on track selection → commission Track B re-train.**
