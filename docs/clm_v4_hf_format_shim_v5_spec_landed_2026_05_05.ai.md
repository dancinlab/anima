# shim v5 spec landed — 2026-05-05 (companion handoff)

**BG lane**: BG-SHIM-V5-SPEC
**Spec doc**: `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md`
**Status**: SPEC ONLY ($0, mac, ~45 min). No exec. No commit. No impl.

## TL;DR (5 bullets)

- **Problem**: shim v4 is architecturally unfalsifiable on F-SHIM-V4-4 because `cross_attn.o_proj init std=0.001` makes the cross-attention residual contribution to next-token logits below benchmark stderr (~3pp at limit=200). `lift_pp >= 5pp` is unreachable through ANY harvest method on shim v4 (per `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json` honest_c3 #C5).
- **Proposed change**: shim v5 = shim v4 + 1-line init change — re-init `cross_attn.o_proj.weight` at `std=0.02` (10× larger), per F-SHIM-V4-4 verdict §recommendations.shim_v5_design_hint. shim v5 lives as a NEW sibling file `tool/transient_py/clm_v4_hf_format_shim_v5.py`; shim v4 stays LOCKED.
- **New falsifier suite F-SHIM-V5-1..5 pre-registered (raw#71)**: V5-1 dry-run finite (Mac), V5-2 v3 byte-equivalent regression (`max_abs_diff <= 1e-5`), V5-3 canonical_zero finite + sanity bound, V5-4 runtime-proxy fixture lift `>= +5pp` on hellaswag-200 (the decisive gate), V5-5 φ★ post-shim ≥ pre-shim - 10pp. Thresholds LOCKED at spec land.
- **Risks gated by suite**: Risk A (φ★ stability — 10× perturbation may flip φ★ sign/magnitude) gated by V5-5; Risk B (v3 byte-equivalent regression — bypass guard leak) gated by V5-2; Risk C (existing PEFT adapters Pβ + CLM-2 LoRA trained on shim v4 substrate transferring poorly to shim v5) is SCOPE-OUT — existing adapters retain shim v4 substrate, shim v5 is opt-in.
- **5-phase implementation plan, $1-3 total**: Phase 1 Mac impl + V5-1 ($0, ~30 min); Phase 2 ubu1 V5-2 + V5-3 ($0, ~30 min); Phase 3 H100 V5-4 ($1-3, ~30 min, **user ACK required**); Phase 4 ubu1/Mac V5-5 φ★ ($0, ~25 min); Phase 5 spec amend `.roadmap.clm` cond.2 G3 promote gate per .own 15 if all PASS ($0, additive-only per raw#15).

## 5 Decision Q's queued (user input needed)

- **Q1** — `cross_attn.o_proj` re-init std value. Default 0.02 (10× v4); alternatives 0.05 / 0.1 / 0.005 / 0.01. **Recommendation**: lock 0.02 for Phase 1; calibration sweep deferred unless V5-4 or V5-5 FAIL.
- **Q2** — re-init q/k/v in addition to o_proj? Default NO (only o_proj). **Recommendation**: NO for Phase 1; revisit only if V5-4 FAILs at o_proj-only.
- **Q3** — shim v5 file structure. Default: separate file `tool/transient_py/clm_v4_hf_format_shim_v5.py` (raw#15 additive). **Recommendation**: separate file.
- **Q4** — Phase 3 H100 cost ACK ($1-3). **Recommendation**: ACK required before Phase 3 launch; Phases 1, 2, 4, 5 can proceed at $0 without H100 ACK.
- **Q5** — existing Pβ + CLM-2 LoRA adapter compatibility with shim v5. Default SCOPE-OUT (existing adapters retain shim v4 substrate). **Recommendation**: SCOPE-OUT for this spec; adapter compatibility matrix is a follow-up cycle (BG-ADAPTER-MATRIX-AUDIT).

## Honest C3 (≥5)

- **C1** — std=0.02 calibration is heuristic (10× shim v4's 0.001). PASS at 0.02 proves sufficiency, not optimality. Calibration sweep (Q1 alternatives) deferred unless V5-4 FAIL.
- **C2** — F-SHIM-V5-4 `+5pp` threshold is anchored to hellaswag-200 stderr ~3pp (~1.7σ MDE). Switching benchmark requires per-benchmark stderr re-anchoring.
- **C3** — Risk B (v3 regression) may force smaller std (0.005-0.01 compromise band). Below 0.005 returns to shim v4 unfalsifiability. The bypass invariant `max_abs_diff <= 1e-5` is the hard floor.
- **C4** — Existing PEFT adapters (Pβ-SCALE + CLM-2 LoRA r=32 a=64 qkvo) likely include `cross_attn.o_proj` in target_modules. Grafting v4-trained delta onto v5-base with 10× larger init scale = unknown transfer characteristics. Risk C scope-out, but open question.
- **C5** — shim v5 does NOT retroactively fix F-SHIM-V4-4 FAIL on shim v4. The PRIVATE upload `need-singularity/clm-v4-mk2-v1` remains architecturally unfalsifiable on V4-4; shim v5 is forward-only.
- **C6** — raw#71 falsifier pre-register: F-SHIM-V5-1..5 thresholds LOCKED at spec land. V5-4 `+5pp` and V5-5 `-10pp` thresholds CANNOT relax without explicit amendment + parallel BG-CLM-2 verdict update.
- **C7** — In-pipeline base φ★ = 35.81 (per `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` §phi_star_base_in_pipeline.phi_mean_K8) is the F-SHIM-V5-5 anchor — NOT the legacy carry value 41.86, to avoid the ~6pp methodology drift confound documented in BG-CLM-2-PHI-CANONICAL.

## Artifacts

- Spec doc (this BG): `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md`
- Companion handoff: `docs/clm_v4_hf_format_shim_v5_spec_landed_2026_05_05.ai.md`
- Failure-mode reference: `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`
- shim v4 LOCKED (diff base, do NOT modify): `tool/transient_py/clm_v4_hf_format_shim.py`
- φ★ canonical reference: `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json`
- Runtime-proxy fixture (V5-4 input): `state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt`

## Conformance

- raw#9 (md only): YES (no code emitted, only diff snippets in fenced blocks for illustration)
- raw#10 (≥5 honest C3): YES (7 in spec, 7 here)
- raw#15 (additive): YES (shim v5 = sibling file; shim v4 LOCKED)
- raw#71 (falsifier pre-register): YES (F-SHIM-V5-1..5 thresholds locked)
- No git commit, no shim v4 mutation, no shim v5 .py written: CONFORMING

## Next action

User ACK on Q1-Q5 → Phase 1 (Mac impl + V5-1) launches in next cycle. Phase 3 (H100 V5-4) requires explicit Q4 cost ACK before launch.
