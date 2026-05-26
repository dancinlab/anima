# H_492 — PRUNING as attention head prune (18th axis) 🔵

PRUNING 1st (신규 18th axis) — low-contribution attention head 제거 (synaptic pruning 모티프).

## 가설
H1 HEAD-MASK: ∀ head h with contrib(h) < θ_prune, mask(h) = 0
H2 ACTIVE-COUNT: n_active = |{h : mask(h)=1}| ≤ n_total
H3 PRESERVES-OUTPUT: pruned model의 output ≈ full output within ε (논의 도구; smoke 는 mask 동작만)
H4 DETERMINISTIC
H5 BOUND
