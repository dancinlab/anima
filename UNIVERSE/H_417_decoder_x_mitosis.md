# H_417 — DECODER × MITOSIS 🔵

DECODER × MITOSIS — post-split cells decode independently: no shared logits state across siblings.

## 가설
H1 INDEPENDENT-DECODE: decode_a(z_a) ⊥ decode_b(z_b) (no cross-cell coupling)
H2 PER-CELL-LOGITS: each cell maintains its own logits buffer
H3 SUM-COUNT: total tokens decoded = sum over cells
H4 DETERMINISTIC
H5 BOUND
