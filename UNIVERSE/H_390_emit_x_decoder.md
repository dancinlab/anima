# H_390 — 자연발화 × DECODER 🔵

자연발화 × DECODER — emit content = lm-head argmax sequence (deterministic decode, V-generic, H_345 carry).

## 가설
H1 ARGMAX-DECODE: emit.text = argmax_v decode(logits) sequence
H2 DETERMINISTIC: same logits → same text
H3 V-GENERIC: |V| free
H4 DETERMINISTIC
H5 BOUND
