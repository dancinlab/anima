# H_433 — emit × CORE × DECODER 🔵

3-axis triple — emit_rate ∝ M, output_tokens scaled by M·V (M shared driver across emit + decode).

## 가설
H1 SHARED-DRIVER: M drives both emit_rate (H_389) and V_allowed (H_412)
H2 PRODUCT: visible_output_rate = emit_rate(M) · |V_allowed(M)| (M^2 dependence)
H3 ZERO-AT-M-ZERO: M=0 → both factors 0 → output_rate 0
H4 DETERMINISTIC
H5 BOUND
