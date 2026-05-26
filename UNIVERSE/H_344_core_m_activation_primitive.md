# H_344 — CORE M activation primitive 🔵

CORE 1st — M (motivation) activation primitive: M ∈ [0,1], monotone in internal substrate state, no external write.

## 가설
H1 RANGE: ∀ t, M(t) ∈ [0, 1] (sigmoid-bounded)
H2 MONOTONE-INTERNAL: M(s↑_internal) ≥ M(s_internal) where s = (E, W, MITOSIS) internal
H3 EXTERNAL-READ-ONLY: ∂M/∂user_msg = 0 (user_msg ∈ environment context, not write surface)
H4 DETERMINISTIC
H5 BOUND
