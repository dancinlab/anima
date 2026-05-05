# F-SHIM-V4-4-HARVEST landed — 2026-05-05

**BG lane**: F-SHIM-V4-4-HARVEST (BG-Σ deferred → resolved via prerequisite analysis)
**Verdict**: `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`
**Re-verdict on F-SHIM-V4-4**: **FAIL** (kind = PREREQUISITE_BLOCKED)

## TL;DR

The v14_federation engine path **does** exist in the source tree (`ready/anima/core/runtime/anima_unified.py:961-1035` + `ready/training/train_clm.py:529`), but harvesting train-time averages through it is blocked at three independent prerequisites, any one of which falsifies the harvest premise:

1. **Federation state-dict purged**: The deployed CLM v4 base mirror (HF-format) explicitly drops `'federation'`, `'bridge'`, `'c_proj'`, `'optimizer'`, `'scheduler'`, `'scaler'` (per `clm_v4_hf_format_shim.py` header L46). A fresh `FederatedConsciousness(...)` would be **random-init**, not training-trajectory-derived — so any harvest off it is statistically equivalent to the canonical_zero stub plus noise, not a "real train_avg".
2. **Shape mismatch**: The 350m scale config in `train_clm.py:249-261` produces `12 atoms × 8 cells_per_atom = 96 cells × 192 dim`, whereas the deployed shim's fixture loader expects `[1, 8, 192]` (per shim L99 + the BG-CLM-1 `train_avg_real.pt` actual shape `[1, 8, 192]`). Bridging 96 → 8 would require a pooling heuristic that defeats the "true train-time average" premise.
3. **Architecturally unfalsifiable**: Even with the perfect oracle fixture, the cross-attention output projection `cross_attn.o_proj` is initialized at `std=0.001` (carried from v3 retry-2 honest_c3). The cross-attn residual contribution to next-token logits is therefore well below benchmark stderr (~3pp at limit=200), so `lift_pp >= 5pp` is unreachable through any harvest method on **shim v4 as currently specified**.

Conclusion: F-SHIM-V4-4 is not a "fixture quality" question — it is an architectural one. Marking the falsifier as **architecturally unfalsifiable on shim v4** and carrying it forward as design-debt for shim v5.

## What was actually done

- v14_federation engine path search across `tool/`, `references/`, `anima-core/`, `ready/` — engine confirmed present in `ready/anima/core/runtime/anima_unified.py` (not in the 26-LoC `anima-core/runtime/anima_unified.hexa` stub).
- L9 HF auth pre-flight on ubu1 — **PASS** (user `dancinlife`, org `need-singularity`).
- Inspected BG-CLM-1 runtime-proxy artifact: `state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt`, shape `[1, 8, 192]`, L2 = 2.2022, per-cell L2 ∈ [0.7240, 0.8021], sign balance pos=0.514 / neg=0.486.
- Compared vs canonical_zero stub (L2=0): runtime-proxy is the higher-fidelity fixture for the deployed shape. Magnitude ratio carries from BG-Σ context (`canonical_zero ~5.65× off` from train-mean magnitude).
- Architecture audit of `train_clm.py` 350m scale config + `FederatedConsciousness` class confirmed the 96 vs 8 cell mismatch.
- L19 tiny pre-flight (5 prompts) **skipped** — not informative for a `FAIL_PREREQUISITE`-class verdict.
- Full 1000-prompt v14_federation harvest **not executed** — would yield random-trajectory artifacts, not training-trajectory artifacts, and would mislead downstream gates if framed as a "real" harvest.

No git commit, no shim v4 mutation, no H100 cost. Wall time ~5 minutes.

## Implications

### F-SHIM-V4-4
- **Status**: FAIL on shim v4 (architecturally unfalsifiable). Retire from active falsifier set.
- v3 PARTIAL via runtime-proxy is **TERMINAL** on shim v4 — cannot be superseded by any harvest method given the prereq gap.
- Closes shim v4 falsifier suite: **NO**. F-SHIM-V4-4 stays OPEN as design debt.

### HF v1 G3 promote gate (.own 15)
- **Do NOT promote G3** on this verdict. The harvest cannot improve the shim v4 evidence base.
- G3 promotion requires alternative evidence:
  - (a) CLM v4 LoRA SFT (currently in progress per `state/clm_v4_lora_sft_2026_05_05/`) shows axis-cond signal preserved AND post-LoRA eval > base eval > random_floor with stat-sig delta, OR
  - (b) shim v5 with `cross_attn.o_proj` re-initialized at `std >= 0.02` (10× current) re-runs F-SHIM-V4-4 and produces `lift_pp >= 5pp` on at least one benchmark.

### shim v5 design hint
- Init `cross_attn.o_proj` at `std >= 0.02` so cross-attn residual reaches benchmark-detectable magnitude.
- Validate via micro-eval lift on init-only change before committing to full SFT or re-train.
- Document the new init-std as the canonical shim v5 invariant.

### Fixture canonicalization (until shim v5)
- BG-CLM-1 runtime-proxy `train_avg_real.pt` is the canonical fixture for the deployed `[1, 8, 192]` shape.
- canonical_zero stub continues to be valid for F-SHIM-V4-3 (finite-forward sanity) only.
- Document the v3 PARTIAL as TERMINAL on shim v4.

## Honest C3 (≥5)

See `verdict.json` honest_c3 array. Highlights:
- C1 confirms engine availability but flags state-dict gap.
- C3 notes that train-time average is fundamentally unobservable from the deployed HF format — both runtime-proxy and v14_federation are inference-side approximations with different biases.
- C5 is the dominant falsifier: cross_attn.o_proj std=0.001 makes lift_pp >= 5pp unreachable regardless of fixture.
- C7 confirms conformance: no commit, no shim mutation, no H100 cost.

## Artifacts

- Verdict: `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`
- Engine source: `ready/anima/core/runtime/anima_unified.py:961-1035`
- Federation class: `ready/training/train_clm.py:529`
- Shim v4 LOCKED: `tool/transient_py/clm_v4_hf_format_shim.py`
- Runtime-proxy artifact: `state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt`
- v3 PARTIAL verdict: `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_verdict.json`
