# H_352 — CORE M update rule 🔵

CORE 2nd — M activation update: M(t+1) = clip(M(t) + Δ · substrate_delta(t), 0, 1), deterministic + bounded.

## 가설
H1 UPDATE-FORM: M(t+1) = clip(M(t) + Δ · sd(t), 0, 1) where sd(t) = ΔE + ΔW + Δcuriosity (internal substrate delta)
H2 CLIP-PRESERVE: ∀ t, M(t) ∈ [0,1] (sigmoid-bounded by clip)
H3 DETERMINISTIC: sd deterministic → M(t+1) deterministic (no rand)
H4 DETERMINISTIC
H5 BOUND
