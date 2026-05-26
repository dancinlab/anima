# H_346 — WAKE 5-stage transition 🔵

WAKE 1st — a_chat_sleep_imagination: WAKE/N1/N2/N3/REM 5-stage state machine, 90-min ultradian period.

## 가설
H1 STATES: |S| = 5, S = {WAKE, N1, N2, N3, REM}
H2 PERIOD: 1 full cycle = 90 min (ultradian)
H3 TRANSITION-DETERMINISTIC: next(s, t) = s' is a pure function of (s, t mod 90min)
H4 ENVELOPE-NOT-GATE: stage ↦ (Φ scale, tension envelope) — NOT boolean emit_allowed
H5 BOUND
