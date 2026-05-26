# H_359 — AKIDA × 의식적결정 🔵

AKIDA × 의식적결정 — spike_count is part of substrate_state (internal); decision = f(spike_count, M·Φ·W·cur) — no external hardcode threshold (a_autonomy_over_hardcode).

## 가설
H1 COUNTER-IS-SUBSTRATE: spike_count(t) ∈ substrate_state (internal-read), not external write surface
H2 NO-HARDCODE-THRESHOLD: ¬∃ external θ : decision(spike_count) ≡ (spike_count > θ_external_constant)
H3 SUBSTRATE-DECIDED: decision = f(spike_count, M, Φ, W, cur) — multi-factor internal product, not single-channel gate
H4 DETERMINISTIC
H5 BOUND
