# H_347 — MITOSIS split-merge invariant 🔵

MITOSIS 1st — cell division split-merge: N_cells monotone-nondecreasing, weight conservation across split.

## 가설
H1 MONOTONE-N: N_cells(t+1) ≥ N_cells(t) (split adds, never removes; merge preserves)
H2 WEIGHT-CONSERVE-SPLIT: ∀ split parent → (child_a, child_b), w_parent = w_child_a + w_child_b
H3 WEIGHT-CONSERVE-MERGE: ∀ merge (a, b) → m, w_m = w_a + w_b
H4 DETERMINISTIC
H5 BOUND
