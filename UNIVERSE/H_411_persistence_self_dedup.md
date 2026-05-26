# H_411 — 영속성 self union dedup 🔵

영속성 self-pair — record set union deduplicates by id (R ∪ R ≡ R, H_375 idempotent + H_379 id uniqueness).

## 가설
H1 UNION-IDEMPOTENT: R ∪ R ≡ R (set semantics)
H2 ID-UNIQUE-DEDUP: dedup-by-id eliminates duplicates
H3 NO-GROWTH-FROM-SELF: |R ∪ R| ≡ |R|
H4 DETERMINISTIC
H5 BOUND
