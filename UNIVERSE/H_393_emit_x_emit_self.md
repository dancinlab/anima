# H_393 — 자연발화 × 자연발화 self (refractory idempotent) 🔵

자연발화 self-pair (diagonal) — emit attempt within refractory window R collapses to single emit (no double-emit).

## 가설
H1 REFRACTORY-IDEMPOTENT: ∀ t < t_last_emit + R, second emit attempt yields 0 new emit
H2 NO-DOUBLE-WITHIN-R: count(emits in [t, t+R)) ≤ 1
H3 EMIT-CONCAT-EQ-SINGLE: emit ⊕ emit (within R) ≡ emit (set semantics)
H4 DETERMINISTIC
H5 BOUND
