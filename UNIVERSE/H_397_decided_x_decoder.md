# H_397 — 의식적결정 × DECODER 🔵

의식적결정 × DECODER — decision-bounded output length: each substrate decision yields a bounded token budget.

## 가설
H1 BUDGET-BOUND: ∀ decision d, output_token_count(d) ≤ budget(d)
H2 BUDGET-FROM-M: budget(d) = floor(M(d) · budget_max)
H3 NON-DECISION-EMPTY: ¬decided → output_token_count = 0
H4 DETERMINISTIC
H5 BOUND
