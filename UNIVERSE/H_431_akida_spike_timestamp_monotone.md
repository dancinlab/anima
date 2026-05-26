# H_431 — AKIDA spike timestamp monotone 🔵

AKIDA 3rd — spike timestamps strictly monotone: t(spike_i) < t(spike_{i+1}) (no out-of-order ingest).

## 가설
H1 STRICTLY-MONOTONE: ∀ i, t_i < t_{i+1}
H2 NO-DUP-TS: ¬∃ i ≠ j : t_i = t_j (timestamps distinct)
H3 NONNEGATIVE: ∀ i, t_i ≥ 0
H4 DETERMINISTIC
H5 BOUND
