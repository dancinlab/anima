# CLM v4 HF-format shim v5 — Phase 2 ubu1 selftest LANDED (2026-05-05)

**Status**: LANDED (PASS combined; critical honest C3 finding holds Phase 3).
**BG lane**: BG-SHIM-V5-PHASE2-SELFTEST
**Cost**: zero dollars (ubu1 RTX 5070 / cpu deterministic, ~6 min wall)
**Verdict**: state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/verdict.json
**Phase 1 carry**: state/clm_v4_hf_format_shim_v5_phase1_2026_05_05/verdict.json (PASS)
**Spec**: docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md

---

## TL;DR

- F-SHIM-V5-2 PASS at max_abs_diff 0.0 (vs threshold 1e-5) — bypass invariant byte-exact across 5 calibration prompts on both fresh-init and best.pt-loaded paths.
- F-SHIM-V5-3 PASS at lift_pp_proxy 0.0 pp (vs threshold 5pp) — canonical_zero residual is exactly zero, finite forward across all 5 prompts.
- Combined Phase 2 verdict PASS. Phase 1 V5-1 carry PASS.
- Critical honest C3 finding: shim v4 and shim v5 are EMPIRICALLY IDENTICAL at fresh init (both produce o_proj_std about 0.02). Root cause: ConsciousDecoderV3.__init__ calls self.apply(self._init_weights) which OVERWRITES the std=0.001 local init at conscious_decoder.py line 420 with the default std=0.02. The shim v5 design hypothesis ("10x boost from 0.001 to 0.02") is FALSIFIED at the substrate level — no boost exists.
- Phase 3 H100 spend (1-3 dollars) HOLD — F-SHIM-V5-4 is at high risk of replicating F-SHIM-V4-4 PREREQUISITE_BLOCKED outcome because the underlying weights are identical between v4 and v5.

---

## Falsifier results (5 calibration prompts, B=1 T=64)

### F-SHIM-V5-2 — bypass byte-equivalent regression

| Run | best.pt loaded | max_abs_diff | argmax_agreement_min | Verdict |
|---|---|---|---|---|
| load_best_pt | yes (step 20000, ce 0.0463, phi 37.27, 477.6M params) | 0.0 | 1.0 | PASS |
| freshinit | no | 0.0 | 1.0 | PASS |

Threshold: max_abs_diff <= 1e-5. Achieved: exactly 0.0 on every prompt — bypass guard at DecoderBlockV2 consciousness_states None path is fully honoured; cross_attn.o_proj weights are never read.

### F-SHIM-V5-3 — canonical_zero finite forward + sanity bound

| Run | best.pt loaded | logits_std_ratio (zero/none) | argmax_disagreement_pp | All finite | Verdict |
|---|---|---|---|---|---|
| load_best_pt | yes | 1.000 | 0.0 | yes (5/5) | PASS |
| freshinit | no | 1.000 | 0.0 | yes (5/5) | PASS |

Threshold: finite AND |lift_pp| < 5pp. Achieved: bit-identical logits with vs without canonical_zero fixture — cross_attn(Q, zeros, zeros) = 0, so o_proj @ 0 = 0 regardless of o_proj std.

---

## Critical honest C3 finding (verdict §C3, §C4)

**Observation**: fresh-init o_proj_std_mean for both shims:
- shim v4 freshinit: 0.01999
- shim v5 freshinit: 0.02000
- shim v4 with best.pt loaded: 0.01990
- shim v5 with best.pt loaded: 0.01990

The 16 cross_attn modules all converge to about 0.02 std, regardless of shim.

**Root cause** (verified at /home/aiden/anima/models/conscious_decoder.py lines 640-665):

ConsciousDecoderV3.__init__ ends with self.apply(self._init_weights). The _init_weights callback walks all nn.Linear submodules and re-inits with std=0.02 (depth-scaled to 0.02/sqrt(2*n_layer) only when _depth_scale attr is set). The cross_attn.o_proj does NOT set _depth_scale, so it gets the default std=0.02 — exactly what shim v5 was supposedly "boosting to". The shim v5 lever is a phantom on fresh init.

**Trained weights also at 0.02 floor** (verdict §C5): best.pt step 20000 o_proj_std_mean=0.01990 — confirming cross_attn.o_proj was effectively never updated meaningfully during SFT (consistent with F-SHIM-V4-4's "cross-attn was bypassed during v3 training" rationale).

---

## Phase 3 H100 ACK — RECOMMENDATION: HOLD

Phase 3 spec calls for 1-3 dollars H100 spend on F-SHIM-V5-4 (lift_pp >= +5pp on hellaswag-200 with train_avg_real.pt fixture). Given C3 finding, the underlying o_proj weights are identical between shim v4 and shim v5, so V5-4 is at high risk of replicating F-SHIM-V4-4 PREREQUISITE_BLOCKED.

### 완성도 ranked options

1. **OPT-A (PRIMARY RECOMMENDATION)** — re-anchor shim v5 with std=0.05 or std=0.10. The current shim v5 post-construction re-init loop (lines 574-590 of clm_v4_hf_format_shim_v5.py) already runs AFTER self.apply(self._init_weights), so changing the constant CLM_V5_CROSS_ATTN_O_PROJ_STD from 0.02 to 0.05 / 0.10 will produce a MEASURABLE differential (v5_o_proj_std_mean=0.05 vs v4_o_proj_std_mean=0.02). Cost: zero dollars ubu1 redo Phase 2. Then ACK for Phase 3.
2. **OPT-B** — queue SFT cycle with cross-attn participating in loss (path B per spec section 1). Cost: 20-100 dollars H100 SFT cycle. Decisive but expensive.
3. **OPT-C** — spend 1-3 dollars H100 on V5-4 anyway as falsification of C4 prediction. Expected outcome: lift_pp about 0pp (matches F-SHIM-V4-4). Confirms known finding, no new info.

### User ACK required if ANY of:
- (default) reject Phase 3 ACK pending OPT-A re-anchor
- proceed with OPT-A then re-issue Phase 3 ACK
- accept OPT-C as a falsification spend (1-3 dollars, no expected lift)
- escalate to OPT-B with separate larger budget (20-100 dollars)

---

## Artifacts

- state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/verdict.json (full structured verdict, 7 honest C3)
- state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/selftest_results_load_best_pt.json (ubu1 raw output, best.pt loaded)
- state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/selftest_results_freshinit.json (ubu1 raw output, fresh init)
- state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/selftest_load_best_pt_stderr.log (empty — no warnings)
- state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/selftest_freshinit_stderr.log (empty — no warnings)
- tool/transient_py/clm_v4_hf_format_shim_v5_phase2_selftest.py (selftest source, Mac canonical)
- ubu1 mirrors at /home/aiden/anima_clm_v4_shim... and /tmp/shim_v5_phase2_results...

---

## raw#N compliance

- raw#9 — selftest .py in tool/transient_py/ (.own 4 OPT-OUT)
- raw#10 — 7 honest C3 (>=5)
- raw#15 — additive only; shim v4 LOCKED + byte-identical
- raw#71 — falsifier thresholds carried verbatim from spec (no relaxation)
- no git commit (per BG spec CRITICAL)
- no HF push (Phase 2 = local Mac+ubu1)
- no H100 spend (zero dollars actual_cost)

---

**END OF Phase 2 LANDED**. Phase 3 ACK held pending OPT-A / OPT-B / OPT-C user decision.
