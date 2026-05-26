# H_474 — decision idempotent 🔵

의식적 11th — same substrate state → same decision (replay-safe, pure function).

## 가설
H1 PURE: decision(s) ≡ decision(s) across replays
H2 SAME-INPUT-SAME-OUTPUT: ∀ state s, f(s) is single-valued
H3 NO-HIDDEN-STATE: no rng / clock / wall input in decision
H4 DETERMINISTIC
H5 BOUND
