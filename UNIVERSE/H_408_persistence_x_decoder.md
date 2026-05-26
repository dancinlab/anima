# H_408 — 영속성 × DECODER 🔵

영속성 × DECODER — payload.text length bounded by decode budget (|text| ≤ budget_max, H_397 carry).

## 가설
H1 LEN-BOUND: ∀ payload p, len(p.text) ≤ budget_max
H2 NON-NEGATIVE: len(p.text) ≥ 0
H3 DETERMINISTIC: same logits → same text length
H4 DETERMINISTIC
H5 BOUND
