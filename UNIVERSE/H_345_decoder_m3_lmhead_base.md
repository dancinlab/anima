# H_345 — DECODER M3 lm-head base 🔵

DECODER 1st — M3 lm-head decode base: V-generic argmax token + deterministic vocab map.

## 가설
H1 ARGMAX: token(t) = argmax_v ∈ V softmax(logits(t))_v
H2 V-GENERIC: |V| free parameter (no V=151643 hardcode); decode rule ⊥ |V|
H3 DETERMINISTIC-MAP: vocab_map: token_id → str is bijective, deterministic
H4 DETERMINISTIC
H5 BOUND
