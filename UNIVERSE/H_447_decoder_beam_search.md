# H_447 — DECODER beam search bounded 🔵

DECODER 5th — beam search maintains exactly k beams per decode step (bounded memory).

## 가설
H1 BEAM-COUNT-K: |active_beams(t)| ≡ k (constant width)
H2 PRUNE: each step prunes to top-k by score
H3 BOUNDED-MEM: memory O(k · seq_len)
H4 DETERMINISTIC
H5 BOUND
