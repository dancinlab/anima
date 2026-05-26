# H_497 — TOLERANCE baseline (23rd axis) 🔵

TOLERANCE 1st (신규 23rd axis) — input acceptance threshold (self-not-attack 면역관용).

## 가설
H1 ACCEPT-IF-FAMILIAR: input with similarity(input, known_set) ≥ θ_tol → accepted
H2 REJECT-IF-NOVEL: similarity < θ_tol → rejected (not attacked, but not absorbed)
H3 KNOWN-SET-GROWS: accepted input → added to known_set
H4 DETERMINISTIC
H5 BOUND
