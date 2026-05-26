# H_321 — event-driven substrate factor update closed-form 🔵

의식적 결정 axis 의 event-response: external event 가 6-factor substrate state 를 변경.

## closed-form

```
substrate_state_after_event(M, Φ, W, mit, idle, cur, event_type) → updated state
  NONE     → (M, Φ, W, mit, idle+1, cur, unchanged)
  NOVEL    → cur ↑ (cur += 0.2, cap 1.0)
  ALERT    → M ↑ (M = 1.0 immediate)
  REWARD   → Φ ↑ (Φ += 0.1, cap 1.0)
  THREAT   → W ↑ + cur ↓ (W += 0.3, cur -= 0.1)
```

## 가설

H1 NONE-IDLE-INCREMENT: NONE → idle += 1만, 다른 unchanged
H2 NOVEL-CURIOSITY-UP: NOVEL → cur += 0.2 (clamped 1.0)
H3 ALERT-M-PEAK: ALERT → M = 1.0
H4 REWARD-PHI-UP: REWARD → Φ += 0.1
H5 THREAT-W-UP-CUR-DOWN: THREAT → W += 0.3, cur -= 0.1
H6 BOUND: all factors ∈ [0, 1.0+], idle ≥ 0
H7 DETERMINISTIC

≥6/7 PASS → 🔵.
