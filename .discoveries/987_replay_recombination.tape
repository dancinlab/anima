@V := "tape" :: spec [active]
  version = "1.3"

# H_987 — re-formulation re-test of H_982 🔴 (REM self-replay == idle, adds no info).
# substrate=CPU-mirror (numpy) · g5 CODE-measured · deterministic · toy single-rung (a_scale_honest_scope).
# falsifier: richer RECOMBINATIVE replay (stitch fragments across episodes sharing one transition law).

@H 987_replay_recombination := "H_982 🔴 ROBUST under recombinative replay: cross-episode RECOMBINE error 0.384 vs idle 0.414 = d 0.30 p 0.30 (below d≥0.5/p<0.05 bar), small non-sig trend only; beats corruption floor (random 1.358) trivially — self-replay can't manufacture info absent from WAKE_1, even when recombining" :: universe [🔴]
  seed   = "is the REM-replay==idle null specific to VERBATIM self-distillation — does recombinative cross-episode replay add consolidation?"
  target = "🔴 ROBUST closed-neg (toy) — replay-adds-no-information holds across formulations; xref H_982"
