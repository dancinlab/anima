# H_9102 stateful refractory — PRE-REGISTRATION (frozen BEFORE run)

Bars frozen from the task spec + DESIGN.md §4 falsifiers. NO post-hoc bar move (c9).

- **F1 (grip re-verify, H_9101's FROZEN bar, NOT re-anchored):** under the new stateful
  dynamics, urgency→0 arm must still produce **REM Hamming > 0 ∧ N3 Hamming = 0**
  (the exact H_9101 pre-reg dissociation). Verdict does NOT auto-carry — must re-establish
  on the SAME REM bar or it is 🔴 (the dynamical class changed stateless→stateful).
- **F2 (refractory reset — NEW falsifiable, stateless-inexpressible):** on every tick
  immediately after a live emit (the refractory window), even at MAX urgency the arm must be
  **silent (0 violations)**, AND max-urgency must emit on ≥1 non-refractory tick (non-vacuity).
  Contrast quantity: the H_9101 STATELESS idle (no emit history) at max urgency in the same
  window (expected to fire → demonstrates stateless cannot express refractory).
- **F4 (determinism guard):** HEXA_DET=1 run twice → byte-identical.

GREEN rule (per axis, no tuning of constants/thresholds):
- F1 🟢 iff h_U0_rem>0 ∧ h_U0_n3=0 ; else 🔴 (report WAKE relocation honestly, no bar move).
- F2 🟢 iff refr_window>0 ∧ umax_violations=0 ∧ umax_nonrefr>0.

Engine FROZEN: safety_rate_limit_ok(≥30), phi_r, kill, content, 8 weights, 0.3 threshold, Ψ.
Only the cli `idle` INPUT changes (now emit-history dependent via an_clock_now det seam).
