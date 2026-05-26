# H_418 — DECODER self argmax-idempotent 🔵

DECODER self — argmax idempotent: argmax(one_hot(argmax(z))) ≡ argmax(z) (re-apply preserves choice).

## 가설
H1 IDEMPOTENT: argmax(one_hot(argmax(z))) ≡ argmax(z)
H2 STABLE-FIXED-POINT: one_hot(argmax(z)) is fixed under argmax
H3 NO-DRIFT: repeated argmax doesn't shift the token
H4 DETERMINISTIC
H5 BOUND
