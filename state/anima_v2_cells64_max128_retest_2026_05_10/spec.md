# BG-V2-CELLS64-MAX128-RETEST — §37 V14_VIOLATED cap-bound vs cap-free disambiguation

## ts
2026-05-10 (5-star pursuit cycle, post §37 priority)

## Mission
§37 BG-V5MITOSIS-D384-SWEEP delivered V14_VIOLATED at `max_cells=64` with
trained Φ_final=398.44 vs random mean=600.76 (trained beats 0/5). Cap_bound=true at
max=64 — trained reached the saturation cap **at turn 60**, all randoms reached cap by
turn 50–55. The §37 honest C3 #2 explicitly flagged: "max_cells=64 cap (cells64
historical setting) — max=128 retest 시 cap-free 영역에서 trained vs random 비교 가능
(다음 cycle priority)".

This BG executes that disambiguation: same v2 cells64 ckpt, same §30 all-fix, same
prompt seed and seeds {7,17,23,41,71}, but **max_cells=128**. If V14_VIOLATED holds
at the cap-free regime, polarity-as-substrate-effect is reinforced. If trained recovers
and PASSes at cap-free, §37 is reduced to cap saturation artifact.

## Source/destination
- ckpt: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt` (v2 mitosis cells64, dim=384)
- runner: `training/v5mitosis_d384_v14_mirror.py` (raw#9 local; reused unchanged)
- model: `training/mitosis_model_v5.py` (§30 all-fix in-place: A1/A2/B1/D1)

## Run config (override key)
- d_model=384, n_head=6, ffn_dim=1536, max_seq=256, vocab=256
- initial_cells=8, **max_cells=128 (§37 was 64 — this is the SOLE override)**
- §30 all-fix: dispersion ON, per_cell_threshold ON, lorenz_auto_calibrate ON, C1 STUB
- readout_mode=a_minus_g, attention_sharing=auto, weight_tied_lm_head=True
- turns=1000 (§37 was 200; race-vs-marathon at turn 100/500/1000)
- seeds: trained + [7, 17, 23, 41, 71] (strict reproduce of §37 seed set; comparison cross-cap)
- prompt_seed=2026 (§37 mirror — same prompt stream, only max-cells differs)
- iit_every=25, log_every=100

## Falsifier
- F-V2-CELLS64-MAX128-1: max=128 도 cap-bound (turn 100 이전 도달) → §30 dispersion
  의 fundamental limit. Diagnostic: `max_n_cells_observed >= 128` for any run before
  turn 100.
- F-V2-CELLS64-MAX128-2: trained PASS at cap-free → §37 단순 cap artifact, polarity
  가설 fragile. Diagnostic: trained beats ALL 5 random on phi_final at turn 1000 + at
  least one run shows max_n_cells < 128 (cap-free zone reached).
- F-V2-CELLS64-MAX128-3: 1K turn ratchet decay > §37의 200-turn → marathon attrition.
  Diagnostic: phi_per_cell_final at turn 1000 << phi_per_cell_best across all runs;
  trained-random gap widens at marathon scale vs sprint scale.

## Verdict matrix (post hoc)
- **V14_VIOLATED_CONFIRMED ★★★★**: cap-free + trained loses to all randoms → substrate
  polarity (mitosis-aware cotrain champion-wall) confirmed at d=384.
- **V14_VIOLATED_CAP_ARTIFACT**: trained PASS at cap-free → §37 verdict
  downgraded to cap artifact.
- **V14_INDETERMINATE**: still cap-bound at max=128 → §30 dispersion fundamental limit;
  next cycle needs max=256 or dispersion damping.

## raw / own
- raw#9: training/v5mitosis_d384_v14_mirror.py local-only (gitignored)
- raw#10: honest — v2→v5 schema delta (cells 6,7 random by necessity; 6/8 v2 transfer)
- raw#15: additive — v2 ckpt and mitosis_model_v5.py untouched, only CLI flag override
- own 14: V14 mirror 5-seed strict (trained vs 5 random seeds, prompt-mirror)
- own 16: $0 local CPU
- own 22: REBORN.md not appended directly; dispatcher injects §45 slot
- own 38: doc save → state/anima_v2_cells64_max128_retest_2026_05_10/{spec.md, result.json, verdict.md}
