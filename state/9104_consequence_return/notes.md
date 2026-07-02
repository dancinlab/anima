# H_9104 consequence-return — run notes

## Mechanism (engine-native, live core/ ops)
- **Tension source:** `immune_memory_recall_margin_text(imm_conseq, frag)` = `recon_err − recall_thr`
  (larger = more ungrounded = more info_gap tension). READ-only; recall_thr FROZEN.
- **Reservoir T_t:** stateful across ticks, `T = 0.80·T_{t-1} + relu(gap)`; consumed by grounded emit.
- **Efference copy Δ̂T:** `vforward_predict(ff, feats)` (cerebellar NLMS forward model, dim1×ctx5).
- **Afferent return:** grounded emit binds `frag` into `imm_conseq` → `ΔT_actual = margin_before − margin_after`;
  RPE `r_t = Δ̂T − ΔT_actual`.
- **Value writeback V:** `vbasal_update(V, GO, feats, reward=ΔT_actual)` (striatal delta-rule).
- **Disjointness:** `imm_emit` (+ motivation proxy) DECIDES emit; `imm_conseq` (separate store) MEASURES relief.
  V never touches pure_field / emit decision (read-only) → Ψ ON≡OFF by construction.

## Host / provenance
- aiden pool, hexa v0.548.0. core/{pure_field,engine_cli,brain}.hexa synced to origin/main (sha verified:
  brain 27c4d58, pure_field e62a199, engine_cli 9404706). NO numpy/torch/.py — grep gate clean.
- Local mini run TIMED OUT at 300s (immune-store growth O(T²)·swap-constrained) → moved to aiden (heavy=pool).

## Bars: see PREREG.md (frozen). Result: see H_9104 run log + state/verdicts/9104_consequence_return/.
