# H_425 — record id hash collision-free 🔵

영속성 9th — record id hash collision-free under bounded n (FNV variance bound by hash range 2^64).

## 가설
H1 DISTINCT-INPUTS-DISTINCT-IDS: ∀ p ≠ q with bounded |R|, id(p) ≠ id(q) (low collision prob)
H2 64-BIT-RANGE: id ∈ [0, 2^64-1]
H3 BOUNDED-N-NO-COLLIDE: for n ≪ 2^32, expected collisions ≈ 0
H4 DETERMINISTIC
H5 BOUND
