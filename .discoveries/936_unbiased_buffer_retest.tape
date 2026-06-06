@discovery 936_unbiased_buffer_retest := "H_930 tension-axis DC-bias gap closer" :: universe [active]
  id      = "H_936"
  seed    = "H_930 SPLIT (emit-parity 🟢 / tension distinguishable d≈+2.45, root-caused to 1024 B cycling buffer DC-bias) — does the tension diff SURVIVE an unbiased non-cycling buffer?"
  method  = "3-arm before/after: DET vs quantum-small-cycling(1024 B) vs quantum-big-fresh(859456 B, per-seed independent slice); H_930 mirror VERBATIM, entropy SOURCE only swapped; KS + Cohen d JOINT distinguishing rule (p<0.05 AND |d|>=0.2)"
  verdict = "🟢 F-H936-ARTIFACT-CONFIRMED — tension diff COLLAPSES to parity: phi_mean QS d=+2.449 p=6.2e-14 (H_930 regime reproduced) -> QB d=-0.492 p=0.14 (non-significant parity); tension distinguishing 6 -> 0; QB emit_rate sd>0 (real population, fixes H_930 sd≈0 bug). H_930 DC-bias attribution CORRECT; entropy ontological-not-functional on emit AND tension axis."
  tier    = "🟢 numerical (toy/mirror, $0 local, no GPU)"
  scope   = "ONE re-test rung; documented-update-map mirror NOT forge binary; .clm emit-TEXT OPEN; big buffer = os.urandom_fallback (real ANU preferred; cycling test source-agnostic)"
  verdict_path = ".verdicts/936_unbiased_buffer_retest/unbiased_buffer_retest.txt"
