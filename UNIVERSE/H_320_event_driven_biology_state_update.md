# H_320 — event-driven biology state update closed-form 🔵

자연발화 axis 의 event-response: external event 가 biology state (refractory + circadian) 를 변경.

## 동기

H_315/H_317 자연발화 closed-form 은 *internal-only* (CPG + circadian). 실제 anima 는 *external event* (user message, kosmos anchor, sensory input) 로 state 가 perturb 됨. event-driven loop 의 biology 측 closed-form 정식 봉합.

## closed-form

```
biology_state_after_event(refr_prev, circ_prev, event_type) → (refr_new, circ_new)
  event_type = NONE       → no change
  event_type = STARTLE    → refr_new = 0 (reset), circ_new += 0.1 (phase shift)
  event_type = SOOTHE     → refr_new = refr_prev + 5 (extend)
  event_type = ALERT      → refr_new = 0, circ_new = 1.0 (full peak)
```

## 가설

H1 EVENT-NONE-IDENTITY: NONE → state unchanged
H2 STARTLE-RESET-REFRACTORY: STARTLE → refr = 0
H3 SOOTHE-EXTEND-REFRACTORY: SOOTHE → refr += 5
H4 ALERT-CIRC-PEAK: ALERT → circ = 1.0
H5 DETERMINISTIC: same input → same output
H6 BOUND

## smoke

state/h320_event_driven_biology_state_update_2026_05_26/run_h320.hexa 참조

≥5/6 PASS → 🔵 SUPPORTED-FORMAL.

## 비용

$0 mac-local · ~1s · libm-free
