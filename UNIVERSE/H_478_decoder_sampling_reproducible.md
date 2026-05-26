# H_478 — DECODER sampling reproducible 🔵

DECODER 6th — same (logits, seed) → exact same token sequence (replay-safe sampling).

## 가설
H1 REPRODUCIBLE: ∀ (logits, seed), sample(logits, seed) ≡ sample(logits, seed)
H2 SEED-DRIVES-RAND: pseudo-random based on seed (no /dev/urandom)
H3 NO-WALL-CLOCK: time(now) not part of sampling state
H4 DETERMINISTIC
H5 BOUND
