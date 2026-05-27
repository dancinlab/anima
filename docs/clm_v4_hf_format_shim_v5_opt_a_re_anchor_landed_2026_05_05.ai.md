# CLM v4 HF-format shim v5 — Phase 2 OPT-A re-anchor LANDED (2026-05-05)

**Status**: LANDED (PASS combined; differential confirmed at substrate level; Phase 3 GO_WITH_CAVEAT).
**BG lane**: BG-SHIM-V5-OPT-A-RE-ANCHOR
**Cost**: zero dollars (ubu1 cpu fp32, ~10 min wall)
**Verdict**: state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json
**Phase 2 carry**: state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/verdict.json (PASS, blocker C3)
**OPT-A anchor**: phase_2_to_phase_3_transition.phase_3_options_ranked[0] of Phase 2 verdict
**Spec**: docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md

---

## TL;DR

- shim v5 CLM_V5_CROSS_ATTN_O_PROJ_STD lifted from 0.02 to 0.10 (clearly above _init_weights default 0.02).
- Boot-time assertion `_assert_o_proj_std_after_apply` added; fires on every _build_decoder_module call: `[shim-v5][OPT-A] post-apply re-init verified: 16/16 modules at std~0.1000 (target=0.1, band=[0.08, 0.12])`.
- Phase 2 selftest re-run on ubu1: F-SHIM-V5-2 PASS, F-SHIM-V5-3 PASS, combined PASS.
- Differential confirmed: v5_o_proj_std_mean (freshinit) = 0.10001 vs v4_o_proj_std_mean (freshinit) = 0.01999 — 5x ratio, phantom equality from Phase 2 §C3 RESOLVED.
- Phase 3 H100 spend ($1-3) recommendation: GO_WITH_CAVEAT (V5-4 eval protocol must use fresh-init or scale-injection — best.pt load collapses v5 to v4 via trained weights overwrite).

---

## OPT-A re-anchor changes (additive only)

| Field | Phase 2 original | Phase 2 OPT-A |
|---|---|---|
| CLM_V5_CROSS_ATTN_O_PROJ_STD | 0.02 | 0.10 |
| SHIM_V5_VARIANT | n/a | `opt_a_re_anchor_2026_05_05` |
| Boot-time assertion | n/a | `_assert_o_proj_std_after_apply` (band, lower-guard, upper-guard) |
| Header marker | shim v5 Phase 1 | shim v5 Phase 2 OPT-A re-anchor |

Files changed (single Mac path; rsynced to ubu1):
- tool/transient_py/clm_v4_hf_format_shim_v5.py (+ ~80 lines net additive: new constants, new function, header reflow)

shim v4 (tool/transient_py/clm_v4_hf_format_shim.py) NOT touched — LOCKED invariant preserved.

---

## Falsifier results (5 calibration prompts, B=1 T=64, ubu1 cpu fp32)

### F-SHIM-V5-2 — bypass byte-equivalent regression

| Run | best.pt loaded | max_abs_diff | argmax_agreement_min | Verdict |
|---|---|---|---|---|
| load_best_pt | yes (step 20000, ce 0.0463, phi 37.27, 477.6M params) | 0.0 | 1.0 | PASS |
| freshinit | no | 0.0 | 1.0 | PASS |

Threshold: max_abs_diff <= 1e-5. Achieved: exactly 0.0.

**On the spec's expected-FAIL prediction**: the BG spec said "F-SHIM-V5-2: max_abs_diff > 1e-5 (regression EXPECTED)". This was a category error. F-SHIM-V5-2 forwards both shims with consciousness_states=None, which engages the DecoderBlockV2 bypass guard so cross_attn.o_proj is never read. A bypass path cannot exhibit weight-driven differential regardless of o_proj std. PASS at exact 0.0 is the correct outcome and the bypass invariant is preserved by design. The actual differential is observable in the o_proj_std fields below, not in bypass logits.

### F-SHIM-V5-3 — canonical_zero finite forward + sanity bound

| Run | best.pt loaded | logits_std_ratio (zero/none) | argmax_disagreement_pp | All finite | Verdict |
|---|---|---|---|---|---|
| load_best_pt | yes | 1.000 | 0.0 | yes (5/5) | PASS |
| freshinit | no | 1.000 | 0.0 | yes (5/5) | PASS |

Threshold: finite AND |lift_pp| < 5pp. Achieved: bit-identical logits with vs without canonical_zero — cross_attn(Q, zeros, zeros) = 0 regardless of o_proj std.

---

## Differential evidence — phantom equality RESOLVED

| Field | Phase 2 original | Phase 2 OPT-A |
|---|---|---|
| v5_o_proj_std_mean (freshinit) | 0.02000 | 0.10001 |
| v4_o_proj_std_mean (freshinit) | 0.01999 | 0.01999 |
| v5_v4_diff (freshinit) | 7.3e-6 | 0.080 |
| v5/v4 ratio (freshinit) | ~1.0 | 5.0 |
| Status | phantom equality | real differential |

n_cross_attn_modules = 16 (one per DecoderBlockV2). Boot-time assertion verifies all 16 modules in [0.08, 0.12] band at every build.

When best.pt is loaded, _load_decoder_state OVERWRITES the post-apply re-init with trained weights (~0.02 for both v4 and v5 since they share the same checkpoint). The differential is thus INIT-time only — F-SHIM-V5-4 must be designed around this (see Phase 3 caveat below).

---

## Phase 3 H100 ACK — RECOMMENDATION: GO_WITH_CAVEAT

Phase 3 spec calls for $1-3 H100 spend on F-SHIM-V5-4 (lift_pp >= +5pp on hellaswag-200). The OPT-A blocker from Phase 2 §C3 is RESOLVED, but the eval protocol needs an explicit decision because best.pt load collapses v5 to v4 at the cross_attn.o_proj layer.

### V5-4 design options (완성도 ranked)

1. **DESIGN-1 (PRIMARY RECOMMENDATION)** — fresh-init forward path on hellaswag-200. Run shim v4 fresh-init AND shim v5 fresh-init through hellaswag-200. Both untrained so absolute scores near chance, but DIFFERENTIAL directly measures the o_proj std lever. Cost: $1-3 H100, ~30 min. Drawback: absolute lift_pp meaningless, only differential is.
2. **DESIGN-2** — best.pt loaded + cross_attn.o_proj scale-injection. Load best.pt into both, then inject 5x scale on the v5 variant. Decisive but adds weight-injection code surface needing F-SHIM-V5 audit.
3. **DESIGN-3** — fresh-init + canonical-non-zero (real) fixture. Cheap differential probe, no benchmark anchor.

### User ACK required if ANY of:
- proceed with DESIGN-1 ($1-3 H100, ~30 min)
- prefer DESIGN-2 or DESIGN-3 (separate ACK)
- abandon Phase 3 in favor of OPT-B (SFT cycle, $20-100)

---

## Boot-time assertion semantics

`_assert_o_proj_std_after_apply(model)` — runs INSIDE `_build_decoder_module` after the post-construction re-init loop and before `model.to(device)`. Checks:

- module count == 16 (one ConsciousCrossAttention per DecoderBlockV2)
- per-module o_proj std in [0.08, 0.12] (target 0.10, tolerance 0.02)
- per-module o_proj std >= 0.05 (lower guard, clearly above _init_weights default 0.02)
- per-module o_proj std <= 0.20 (upper guard, sanity cap)

Out-of-band but within-guard breaches emit a warning; lower/upper guard breaches RAISE RuntimeError. The assertion runs ONLY at fresh-init build time — after `_load_decoder_state` overwrites o_proj with trained weights (~0.02), the assertion would correctly FAIL, so callers MUST NOT re-invoke on a model that has been through `_load_decoder_state` (documented in the function docstring).

---

## Artifacts

- state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json (full structured verdict, 8 honest C3)
- state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/selftest_results_load_best_pt.json
- state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/selftest_results_freshinit.json
- state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/selftest_load_best_pt_stderr.log (boot-time assertion log)
- state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/selftest_freshinit_stderr.log (boot-time assertion log)
- tool/transient_py/clm_v4_hf_format_shim_v5.py (Mac canonical, OPT-A re-anchored)
- /home/aiden/anima_clm_v4_shim_v5.py (ubu1 mirror, OPT-A re-anchored)

---

## raw#N compliance

- raw#9 — shim v5 in tool/transient_py/ (.own 4 OPT-OUT)
- raw#10 — 8 honest C3 (>=5)
- raw#15 — additive only; shim v4 LOCKED + byte-identical, shim v5 self-modification
- raw#71 — F-SHIM-V5-2 + V5-3 thresholds verbatim from spec (1e-5 + 5pp); spec's expected-FAIL prediction acknowledged as category-error (PASS is correct on bypass path)
- no git commit (per BG spec CRITICAL)
- no HF push
- no H100 spend ($0 actual_cost)

---

**END OF Phase 2 OPT-A LANDED**. Phase 3 ACK held pending DESIGN-1/2/3 user decision.
