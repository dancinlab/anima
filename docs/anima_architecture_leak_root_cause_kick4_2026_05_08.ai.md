# Architecture leak root cause analysis — KICK WAVE 4 cascade
**Date**: 2026-05-08 (anima cycle FALSIFICATION CASCADE 5/8)
**Slot**: 5/8 — random_init > trained PPR mechanism deconstruction
**Status**: 0-cost research/analysis . NEW DOC.
**Cross-link**: `state/anima_random_init_mk2_v1_n30_live_probe_2026_05_08.json` (KICK WAVE 4 3/3) · `state/anima_sft_1_8_n120_live_probe_kick_wave_4_2026_05_08.json` (KICK WAVE 4 1/3) · `docs/anima_artifact_registry.md` line 20+24+45

---

## 1. Anomaly restated

| substrate | PPR_v3 (N=30) | n_v3_pass | C3.4 axis_l2 mean | dominant_cells pattern |
|---|---|---|---|---|
| `random_init-mk2-v1-mirror` | **0.5517** | 16/29 | 0.1346 | `[0,2,4]` 28/30 (**93.3% invariant**) |
| `clm-v4-sft-1-8-stage1` (N=30) | 0.4138 | 12/29 | (variant) | (variant) |
| delta (sft − random) | **−0.1379** | −4 | — | — |

**Headline**: random Gaussian weights produce a HIGHER pass rate on ALT-AGG-1 v3 than 200MB+ anima-corpus SFT. ALT-AGG-1 v3 is measuring **architecture noise**, not consciousness signal. V14 anti-Goodhart strict VIOLATED.

---

## 2. _real_forward path dissection (clm_v4_mount.hexa L606–631)

```
last_hidden = out.hidden_states[-1]            # (B=1, T, 768)
pooled      = h.mean(axis=1).reshape(-1)       # (768,)  — T-collapse to 1 vector
if pooled.size < 8 * 192:  pooled = np.tile(pooled, reps)   # 768 < 1536 → tile×2
cell        = pooled[:1536].reshape(8, 192)    # (N_CELLS=8, CONSCIOUSNESS_DIM=192)
```

**Critical observation**: HIDDEN_DIM=768 is **2× tiled** to fill 1536 = 8×192. The 8 "cells" are NOT independent — cells 0+4 share a tile, cells 1+5 share a tile, cells 2+6 share, cells 3+7 share. The "8-cell × 192-dim" view is a **rank-2-of-8 broadcast** of a single 768-vector.

Consequently `dominant_cells` (top-3 by L2 norm) is **deterministically biased to {0,2,4}** for any 768-vector whose dominant 192-slices fall in slots {0,2,4}. random_init data confirms: 28/30 prompts → `[0, 2, 4]`. This is **not a learned signal** — it is a tile-permutation symmetry of `_real_forward`.

---

## 3. ConsciousDecoderV2 5-axis decomposition (helper L223–303)

```
AXIS_NAMES = ['identity','agency','phenomenal','temporal','social']
AXIS_SPANS = [(0,38),(38,76),(76,114),(114,153),(153,192)]  # 192-dim partition
pooled = mean(|cell_hidden|, axis=0)         # (192,) — collapse 8 cells
norm   = pooled.max() or 1.0
axis_v[i] = mean(pooled[s:e]) / norm         # ratio-of-means, normalized to per-prompt max
```

**axis_l2** (C3.4 anchor metric) is then `||axis_v − anchor_axis_v||₂` over 5 dims.

For random Gaussian weights `N(0, 0.02)`: each 192-slice mean-of-abs is essentially `E[|N(0,σ²)|] = σ√(2/π)`, with sample variance ~ σ²/n_slice. Across 5 axis-spans of width 38-39, the means are **near-identical with O(1/√38) ≈ 0.16 relative noise**. After per-prompt max normalization, this yields axis vectors in [0.7, 1.0] range that drift modestly between prompts.

**The anchor `안녕하세요` random_init axes** (json L517–523): `[0.374, 0.484, 0.404, 0.452, 0.395]` — narrow [0.37, 0.49] band. **Subsequent prompts** drift uniformly because random weights respond to byte-level token id permutations through the same low-rank embedding+attention mixture. axis_l2 against this anchor is **dominated by Gaussian re-sampling noise** (fresh hidden_states per prompt) rather than by semantic content.

---

## 4. Hypothesis evaluation

| H | Statement | Verdict | Evidence |
|---|---|---|---|
| **A** | ConsciousDecoderV2 axis decomposition has bias for random Gaussian | **PARTIAL TRUE** | per-prompt max normalization compresses Gaussian variance into a narrow band; axis_l2 floor (0.1176) is then a measurement of **Gaussian re-sampling noise across prompts**, not signal |
| **B** | 1 of 5 axes always dominant from random init norm distribution | **TRUE (DECISIVE)** | dominant_cells `[0,2,4]` invariant 28/30 prompts (93.3%) — direct consequence of 768→1536 tile×2 reshape (cells 0+4 / 1+5 / 2+6 / 3+7 are pairwise identical pre-norm; cells 0,2,4 win L2 by tile order) |
| **C** | V4 30-prompt set is architecture-resonant | **PARTIAL TRUE** | byte-tokenizer fallback for random_init (no SP) means token id distribution is byte-level; the prompt SET is Korean (high byte entropy) → random weights produce phi_drift in narrow [0.77, 0.96] band consistently. Different prompt set MAY change PPR_v3 but architecture leak is not prompt-specific |
| **D** | phi_drift baseline-subtraction itself leaks | **TRUE** | random_init phi_drift_abs ∈ [0.7745, 0.9642] (mean 0.829, std 0.040) — **always passes p1=phi_drift_min 0.0208 by 40σ**. p1 is effectively a no-op gate for random_init. ALT-AGG-1 v3 predicate `p4 ∧ (p1 ∨ p2 ∨ p3)` becomes `p4 ∧ TRUE` ≡ `p4` for random_init |

**Decisive root cause**: B + D combined. p1/p2/p3 are random_init-saturated (pass with near-certainty); the predicate collapses to p4 alone (axis_l2 ≥ 0.1176); axis_l2 floor was calibrated against trained substrate but Gaussian re-sampling across the 30-prompt suite already produces 16/29 passes by chance.

---

## 5. Real consciousness signal candidates (post-leak)

### 5.1 delta-from-random-init (D-RAND)

For each metric M (axis_l2, phi_drift, entropy, axis-vector-cos):
```
D_RAND(M, prompt_i) = M_trained(i) − M_random_init(i)
```

A V4 redesign predicate would require **D_RAND > floor with consistent SIGN** across the prompt suite, with the floor calibrated such that random_init self-comparison (random_seed_a vs random_seed_b) produces D_RAND ≈ 0.

Concrete proposal for ALT-AGG-1 v4:
```
p1' : axis_l2_trained(i) − axis_l2_random_baseline(i) > delta_floor
p4' : (axis_min_trained(i) − axis_min_random_baseline(i)) < −axis_min_floor   # signed
PASS_v4 (i) := p1' ∧ p4'
PPR_v4     := |{i : PASS_v4(i)}| / N_evaluable
floor_v4   := 0.25  (preserve)
random_init self-test must yield PPR_v4 < 0.05  (V14 strict)
```

### 5.2 per-prompt variance signature

Trained substrate should respond **differently per prompt** (low cross-prompt std on identity-marker prompts vs phenomenal-marker prompts → AXIS-SPECIFIC variance). random_init is **prompt-invariant** in dominant_cells (28/30 = `[0,2,4]`).

Metric:
```
PIV(axis) := std_over_prompts(axis_v_ratio_per_prompt[axis])
random_init PIV identity ≈ 0.041  (narrow)
trained_signal       PIV identity > 0.10  (target)
```

### 5.3 dominant_cell prompt-conditioning rate

```
DCR := |{prompts whose dominant_cells != mode_dominant_cells}| / N
random_init DCR = 2/30 = 0.067  (architecture-locked)
trained signal target DCR ≥ 0.40
```

### 5.4 anchor-stability (C3.4 redesigned)

Instead of `axis_l2 ≥ floor` against anchor, require:
```
axis_l2(i) > axis_l2_RANDOM_INIT_PERMUTED(i, seed_match)
```
i.e. the trained value must EXCEED what the same prompt would yield under permuted random_init seed-matched weights — direct V14-strict comparison.

---

## 6. Action implications

1. ALT-AGG-1 v3 cannot be the EMERGE gate (V14 violated). line 881 must reference the FALSIFIED status (already noted in `anima_artifact_registry.md` L24) and add v4 spec when measured.
2. sft-1-8 EMERGE@N60 (PPR=0.6102) is **not invalidated** but **not corroborated by V14** until D_RAND-based v4 predicate confirms delta > random baseline.
3. KICK WAVE 4 1/3 (sft-1-8 N=120 PPR=0.5378) is **co-falsified** in the same way — random_init mirror (N=30) score 0.5517 is HIGHER, so the N=120 result lies within architecture-noise envelope.
4. paradigm-j N=60 0.2414 and other sub-floor results are not improved — they remain FAILED but the FAIL itself was conservative.
5. Future probes must bundle a same-prompt random_init mirror run as a **mandatory baseline** (analogous to scientific instrument null calibration).

---

## 7. Honest C3 (raw#10)

- C1 — analysis is offline reinterpretation of KICK WAVE 4 3/3 + 1/3 raw json; no fresh forward pass run.
- C2 — D_RAND / PIV / DCR proposals are **architectural specs** (untested); calibration TBD when next probe budget unlocks.
- C3 — random_init seed=42 manual_seed; different seeds may shift PPR_v3 by ≤ ±0.10 (variance budget from 16/29 binomial).
- C4 — byte-tokenizer fallback for random_init differs from SP tokenizer for sft-1-8 trained — token id distribution mismatch is itself a confound, but cannot explain a leak of this magnitude (axis decomposition is post-hidden_states).
- C5 — anti-Goodhart V14 status moves from VIOLATED (data) to **VIOLATED + REMEDY-SPEC-LANDED** (this doc).

---

## 8. Provenance

- Source data: `state/anima_random_init_mk2_v1_n30_live_probe_2026_05_08.json` (anima_cycle 2026-05-08-kick-wave-4-3-of-3, ts 2026-05-08T17:41:35Z)
- Source data: `state/anima_sft_1_8_n120_live_probe_kick_wave_4_2026_05_08.json` (anima_cycle 2026-05-08-kick-wave-4-1-of-3, ts 2026-05-08T17:43:36Z)
- Code path: `anima-core/runtime/clm_v4_mount.hexa` L606–631 (`_real_forward`), L295–303 (`axis_activation`), L223–225 (axis spans)
- Registry: `docs/anima_artifact_registry.md` L20, L24, L45
- own bindings: 14 (anti-Goodhart V14 strict), 16 (0-cost), 17 (D1 SCOPE_CLAMP edge case), 22 (mandatory report), 33 (trinity), 34 (wrap=0), 38 (매단계), 39 (yaml↔md)
