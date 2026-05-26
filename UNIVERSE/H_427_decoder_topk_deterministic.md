# H_427 — DECODER top-k deterministic 🔵

DECODER 4th — top-k sampling deterministic given (logits, seed): replay-safe, no rng drift.

## 가설
H1 SEED-DETERMINISTIC: (logits, seed) → same sample tokens across runs
H2 K-BOUND: top-k returns exactly k tokens
H3 K-SUBSET-OF-V: top-k ⊆ V (no out-of-vocab token)
H4 DETERMINISTIC
H5 BOUND
