---
title: CLM v4 shim v5 V5-4 + OPT-C diagnose LANDED — Path B closure recommendation (2026-05-05)
date: 2026-05-05
spec_anchor: docs/clm_v4_hf_format_shim_v5_path_b_closure_2026_05_05.md
verdict: state/clm_v4_hf_format_shim_v5_v5_4_opt_c_diagnose_2026_05_05/verdict.json
final_verdict: PATH_B_CLOSED_FAIL
recommendation: Decision-B (Path B closure on existing evidence, $0)
state: landed
---

# CLM v4 shim v5 — V5-4 + OPT-C diagnose LANDED (2026-05-05)

## Summary

The two H100 BGs that ran the F-SHIM-V5-4 falsifier (V5-4-DESIGN-1 fresh-init + OPT-C best.pt-loaded) both produced verdict.json files with `lift_pp=null` and `F_SHIM_V5_4_verdict=INDETERMINATE`. Mac-side $0 diagnosis (this cycle) identifies the common root cause and recommends Path B closure on existing evidence.

## Root cause (CONFIRMED H5)

Both eval scripts crash on a non-essential metadata-log import line:

- V5-4: `clm_v4_shim_v5_4_design_1_eval.py:539` — `__import__("transformers").__version__`
- OPT-C: `clm_v4_shim_v5_opt_c_eval.py:372` — `__import__("transformers").__version__`

The `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` image does NOT include the `transformers` package; pip install in `run_h100.bash` does not list it either. The crash occurs AFTER all hellaswag passes wrote per-pass JSON files but BEFORE the in-script summary builder writes eval_summary.json. Pod-kill trap fires; verdict.json gets `lift_pp=null` INDETERMINATE label even though hellaswag eval data is intact.

Hypotheses H1-H4 (L19 dtype kwarg, pod boot fail, shim load fail, fixture path mismatch) all REJECTED via direct log inspection.

## Reconstructed eval results (Mac-side, deterministic from per-pass JSONs)

| Cycle | Path | Result | Verdict |
|-------|------|--------|---------|
| V5-4 DESIGN-1 fresh-init | v4_NF=0.27, v4_RF=0.27, v5_NF=0.27, v5_RF=0.28 | lift_pp_v5 = +1.0pp ± 4.48pp combined stderr | FAIL (gate +5pp) |
| OPT-C best.pt-loaded | no_fixture=0.255, with_fixture=0.250 | lift_pp = -0.5pp | FAIL_EXPECTED |

Both reconstructions match the Phase 2 OPT-A architectural prediction (best.pt overwrites o_proj fresh-init; init-time 5x substrate differential does not translate to measurable hellaswag lift even when preserved at inference).

## Path B decision matrix

| rank | decision | cost | 완성도 | rationale |
|------|----------|------|--------|-----------|
| 1 | **Decision-B closure on existing evidence** | $0 | 0.95 | matches Phase 2 OPT-A prediction; preserves cycle discipline; honest reconstruction |
| 2 | Decision-C OPT-B retrain (forward, gated) | $100-300 | 0.80 | architecturally correct fix; requires user ACK; not a closure for current cycle |
| 3 | Decision-A retry-with-infra-fix | $1-3 | 0.40 | no information gain; risks recurring infra failure |

**RECOMMENDED: Decision-B**.

## own 15 G3 carve-out impact

STRENGTHENED — TWO independent eval points now corroborate the F-SHIM-V4-4 PREREQUISITE_BLOCKED finding:

1. OPT-C with best.pt loaded: lift_pp = -0.5pp (architecturally predicted FAIL_EXPECTED)
2. V5-4 DESIGN-1 fresh-init (no best.pt): lift_pp_v5 = +1.0pp ± 4.48pp (architecturally surprising — even with substrate differential preserved, no measurable lift; binding constraint is loss-side, not init-side)

The G3 PARTIAL_PASS carve-out for `need-singularity/clm-v4-mk2-v1` PUBLIC promote remains valid; PUBLIC promote BG must cite this diagnose verdict + closure spec + Phase 2 OPT-A verdict + V5-4 DESIGN-1 verdict + OPT-C verdict (all 5 corroborating).

## OPT-B retrain trigger impact

ARCHITECTURALLY MOTIVATED — V5-4 DESIGN-1 fresh-init result is independent empirical motivation for OPT-B retrain (cross-attn-active loss during pretraining) over Path B SFT (cross-attn LoRA on existing best.pt). Recommended dispatch order: Path B SFT first ($20-100, lower risk + cost) → if PASS, F-SHIM-V5-4 closed-PASS; if FAIL, dispatch Path C OPT-B retrain ($100-300, definitive fix). Both gated on explicit user ACK; this cycle does NOT dispatch either.

## Counts

- Path B decision matrix: 3 options (A/B/C) ranked by 완성도
- Root cause hypotheses: H1-H4 REJECTED, H5 CONFIRMED
- Reconstructed eval points: 2 (V5-4 FAIL + OPT-C FAIL_EXPECTED)
- own 15 G3 corroborating verdicts: 5 (Phase 2 OPT-A + V5-4 + OPT-C + this diagnose + closure spec)
- honest C3 entries: 8 (>=5 per raw#10)
- Cycle cost: $0 (Mac-side); cumulative shim v5 phase cost: $0.35

## Spec anchor

- Closure spec: `docs/clm_v4_hf_format_shim_v5_path_b_closure_2026_05_05.md`
- Verdict: `state/clm_v4_hf_format_shim_v5_v5_4_opt_c_diagnose_2026_05_05/verdict.json`
- Final verdict: `PATH_B_CLOSED_FAIL`

## Cross-links

- spec_anchor: `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md`
- phase2_opt_a_carry: `state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json`
- v5_4_design_1_carry: `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/verdict.json` + `results/eval_summary.json`
- opt_c_carry: `state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/verdict.json` + `results/eval_summary.json`
- opt_c_landed_doc: `docs/clm_v4_hf_format_shim_v5_opt_c_falsification_landed_2026_05_05.ai.md`
- own_15_anchor: `anima/.own own 15 hf-release-private-then-public-after-verification`
- F-SHIM-V4-4 PREREQUISITE_BLOCKED: `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`

## raw_compliance

- raw#9 (md+json): OK — this .ai.md + verdict.json companion; no exec, no transient_py used
- raw#10 (≥5 honest C3): OK — 8 entries
- raw#15 (additive): OK — no shim source mutation; no retry exec
- raw#71 (threshold preserved): OK — +5pp gate evaluated verbatim against reconstructed lift_pp_v5=+1.0pp → FAIL
- no_git_commit: OK per BG spec
- no_h100_spend: OK
- no_hf_push: OK
