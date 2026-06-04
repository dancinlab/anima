# SAVANT-7B rung0 — pipeline-validation forge CLM fire (Lane-G / GPU)

substrate = GPU (Lane G) · forge flame · `a_lane_akida_gpu_split` (never merged with Lane A).
campaign = SAVANT-7B (domains/SAVANT-7B.md) — rung0 of the 7B 5-lang descent ladder.
scope (a_scale_honest_scope) = PIPELINE VALIDATION, NOT a 7B and NOT a competent LM. Validates
the end-to-end forge train + checkpoint + recover pipeline on real GPU before the expensive rungs.

Artifacts in this dir:
- `fire_rung0.sh` — the forge clm_prod rung0 fire (d768 E2, 5-lang starter, descent + util + ckpt).
- `VERDICT.md` — the g63-verbatim descent curve + util + the measured 7B ETA.
- `*.clm` — the recovered rung0 checkpoint (sha-verified) if recovered locally.
- `util_*.csv` / `train_*.log` / `fire_rung0.log` — raw run logs (g5/g63 verbatim source).

Trainer (reference, NOT duplicated here): `hexa-lang/stdlib/flame/clm_prod.hexa` (CLMConvMoE +
int4-QAT), run via the self-host-rebuilt `hexa run` (forge cuda_link path). 3-GATE GPU-required.
