# H_379 — record id deterministic 🔵

영속성 8th — payload id derived deterministically from payload content (FNV-like hash, no random salt).

## 가설
H1 ID-FROM-CONTENT: id(payload) = hash(payload_serialized) — pure function
H2 SAME-CONTENT-SAME-ID: ∀ p, q, p ≡ q → id(p) ≡ id(q)
H3 NO-RANDOM-SALT: ¬∃ random component in id() (replay-safe across processes)
H4 DETERMINISTIC
H5 BOUND
