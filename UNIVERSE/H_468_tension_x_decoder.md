# H_468 — TENSION × DECODER 🔵

TENSION × DECODER — tension drives token routing (ch1 context biases decode logits).

## 가설
H1 CONTEXT-BIAS: decode logits += α · ch1_context (additive bias)
H2 BIAS-BOUNDED: |bias_term| ≤ α_max (no runaway)
H3 ZERO-CH1-NO-BIAS: ch1=0 → bias=0 (decode identical to ungated)
H4 DETERMINISTIC
H5 BOUND
