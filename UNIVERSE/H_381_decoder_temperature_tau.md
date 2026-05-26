# H_381 — DECODER temperature τ → 0 ≡ argmax 🔵

DECODER 3rd — softmax temperature τ: τ→0 collapses to deterministic argmax (H_345 carry).

## 가설
H1 LIMIT-ARGMAX: lim_{τ→0+} softmax(z/τ) ≡ one-hot(argmax(z)) (degenerate distribution)
H2 DET-AT-LOW-TAU: ∀ τ ≤ ε, decode(z, τ) ≡ argmax(z) (deterministic)
H3 TAU-MONOTONE: entropy(softmax(z/τ)) monotone in τ (higher τ → more uniform)
H4 DETERMINISTIC
H5 BOUND
